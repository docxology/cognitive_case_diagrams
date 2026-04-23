"""DAIF Inference: Distributional Case Assignment & Variational Message Passing.

Implements the full distributional inference machinery:
- distributional_case_assignment(): Iterative belief refinement with FE convergence
- variational_message_passing(): Factor-graph variational inference
- bethe_free_energy(): Bethe approximation of belief-propagation free energy
- expected_information_gain(): Epistemic value under full return distribution

References:
    Friston et al. (2017) — Active Inference and Epistemic Value
    Yedidia et al. (2001) — Bethe Free Energy & Loopy Belief Propagation
    Akgül et al. (2026) — Distributional Active Inference
"""
from __future__ import annotations

import logging
from typing import Optional

import numpy as np

from ..cognitive.belief import CaseDiagramBelief
from ..cognitive.free_energy import kl_divergence, variational_free_energy
from .types import DAIFResult, DistributionalReturn

logger = logging.getLogger(__name__)


def distributional_case_assignment(
    prior: CaseDiagramBelief,
    observation_likelihoods: np.ndarray,
    transition_matrix: Optional[np.ndarray] = None,
    n_iterations: int = 10,
    convergence_threshold: float = 1e-6,
    n_quantiles: int = 51,
) -> DAIFResult:
    """Compute distributional posterior over case diagrams via DAIF iteration.

    Iteratively refines the belief distribution using the full DAIF cycle:
      1. Push-forward belief through transition dynamics
      2. Bayesian update: q(s) ∝ p(o|s) · q_pushed(s)
      3. Compute variational free energy F = KL(q||q_pushed) - E_q[log p(o|s)]
      4. Track convergence and update quantile representation

    Returns a DAIFResult dataclass with the final belief, FE trajectory,
    convergence diagnostics, and the final DistributionalReturn.

    Args:
        prior: Initial belief distribution over case roles.
        observation_likelihoods: p(o|s_i) for each role, shape (n,).
        transition_matrix: Row-stochastic T[i,j], shape (n,n).
            If None, uses identity (no transition dynamics).
        n_iterations: Maximum number of DAIF iterations.
        convergence_threshold: Stop when |ΔF| < threshold.
        n_quantiles: Number of quantiles in the return distribution.

    Returns:
        DAIFResult with belief, fe_trajectory, convergence_iteration,
        return_distribution, and diagnostics.

    Raises:
        ValueError: On dimension mismatch.
    """
    likelihoods = np.asarray(observation_likelihoods, dtype=np.float64)
    n = len(prior.roles)

    if len(likelihoods) != n:
        raise ValueError(f"Likelihoods ({len(likelihoods)}) must match roles ({n})")

    if transition_matrix is None:
        logger.warning(
            "transition_matrix is None — using identity (no transition dynamics). "
            "Pass an explicit matrix to model temporal case-role dynamics."
        )
        T = np.eye(n)
    else:
        T = np.asarray(transition_matrix, dtype=np.float64)
        if T.shape != (n, n):
            raise ValueError(f"Transition matrix shape {T.shape} != ({n}, {n})")
        if not np.allclose(T.sum(axis=1), 1.0, atol=1e-8):
            raise ValueError("Transition matrix rows must sum to 1.0")

    current = prior
    fe_trajectory: list[float] = []
    kl_trajectory: list[float] = []       # D_KL(q_posterior || q_pushed) per iteration
    loglik_trajectory: list[float] = []   # E_q[log p(o|s)] per iteration
    signed_deltas: list[float] = []  # signed ΔF for oscillation detection
    convergence_iter = n_iterations

    # Reward proxy: log-likelihood as reward signal
    safe_log_lik = np.where(likelihoods > 0, np.log(likelihoods), -100.0)

    for iteration in range(n_iterations):
        q = current.probabilities

        # Step 1: Push-forward
        q_pushed = T.T @ q
        total_pushed = q_pushed.sum()
        if total_pushed <= 0:
            logger.warning("Push-forward degenerate at iteration %d; using uniform fallback", iteration)
            q_pushed = np.full(n, 1.0 / n)
        else:
            q_pushed = q_pushed / total_pushed

        # Step 2: Bayesian update q(s) ∝ p(o|s) · q_pushed(s)
        unnorm = likelihoods * q_pushed
        total = unnorm.sum()
        if total <= 0:
            logger.warning("DAIF: all posteriors zero at iteration %d", iteration)
            break
        posterior = unnorm / total

        # Step 3: Variational free energy with explicit KL / data-fit decomposition.
        # F = KL(q_posterior || q_pushed) − E_q[log p(o|s)]
        safe_log_prior = np.where(q_pushed > 0, np.log(q_pushed), -100.0)
        fe = variational_free_energy(posterior, safe_log_lik, safe_log_prior)
        kl_term = float(kl_divergence(posterior, q_pushed))
        expected_loglik = float(np.sum(posterior * safe_log_lik))
        fe_trajectory.append(fe)
        kl_trajectory.append(kl_term)
        loglik_trajectory.append(expected_loglik)

        # Step 4: Convergence & stability checks
        if len(fe_trajectory) > 1:
            signed_delta = fe_trajectory[-1] - fe_trajectory[-2]
            abs_delta = abs(signed_delta)
            signed_deltas.append(signed_delta)
            if len(signed_deltas) > 3:
                signed_deltas.pop(0)

            # Oscillation detection: 3 consecutive alternating-sign deltas
            if len(signed_deltas) == 3:
                signs = [d > 0 for d in signed_deltas]
                if signs[0] != signs[1] and signs[1] != signs[2]:
                    logger.warning(
                        "DAIF: oscillation detected at iteration %d "
                        "(ΔF history: %s); halting without convergence",
                        iteration, [f"{d:.2e}" for d in signed_deltas],
                    )
                    break

            # Backtracking guard: FE increased (inference is diverging)
            if signed_delta > 0:
                logger.warning(
                    "DAIF: free energy increased at iteration %d "
                    "(ΔF=+%.2e); halting — inference may have diverged",
                    iteration, signed_delta,
                )
                break

            # Normal convergence
            if abs_delta < convergence_threshold:
                convergence_iter = iteration
                logger.info("DAIF converged at iteration %d (ΔF=%.2e)", iteration, abs_delta)
                break

        current = CaseDiagramBelief(
            roles=prior.roles,
            probabilities=posterior,
            name=f"{prior.name}_daif_t{iteration + 1}",
        )
        logger.debug(
            "DAIF iter %d: H=%.4f, F=%.4f, mode=%s",
            iteration, current.entropy(), fe, current.most_likely_role().name,
        )

    # Build DistributionalReturn from final belief and reward proxy
    tau_levels = np.linspace(1 / (2 * n_quantiles), 1 - 1 / (2 * n_quantiles), n_quantiles)
    q_final = current.probabilities
    reward_proxy = safe_log_lik - safe_log_lik.min()
    z_vec = reward_proxy  # Single-step Bellman with identity transition
    mean_z = float(q_final @ z_vec)
    var_z = max(0.0, float(q_final @ z_vec ** 2) - mean_z ** 2)
    sorted_idx = np.argsort(z_vec)
    cum = np.cumsum(q_final[sorted_idx])
    cum = np.maximum.accumulate(cum)
    if cum[-1] > 0:
        cum = cum / cum[-1]
    else:
        cum = np.linspace(0, 1, n)
    quantile_vals = np.interp(tau_levels, cum, z_vec[sorted_idx])

    ret_dist = DistributionalReturn(
        mean=mean_z, variance=var_z,
        quantiles=quantile_vals, quantile_levels=tau_levels,
    )

    diagnostics = {
        "fe_reduction": (fe_trajectory[0] - fe_trajectory[-1]) if len(fe_trajectory) > 1 else 0.0,
        "n_iterations_run": len(fe_trajectory),
        "final_entropy": float(current.entropy()),
        "most_likely_role": current.most_likely_role().name,
        # Per-iteration decomposition F = KL − E_q[log p(o|s)] (Eq. 7-2)
        "kl_trajectory": list(kl_trajectory),
        "loglik_trajectory": list(loglik_trajectory),
    }

    return DAIFResult(
        belief=current,
        fe_trajectory=fe_trajectory,
        convergence_iteration=convergence_iter,
        return_distribution=ret_dist,
        diagnostics=diagnostics,
    )


def variational_message_passing(
    observations: np.ndarray,
    prior_precision: np.ndarray,
    likelihood_precision: np.ndarray,
    n_iterations: int = 16,
) -> tuple[np.ndarray, np.ndarray]:
    """Categorical variational message passing over discrete case roles (Eq. 7c-vmp).

    Implements the discrete VMP update from manuscript §7c:

        q^{t+1}(c_k) ∝ q^{t}(c_k) · exp(w_k · o_k)

    where w_k is the likelihood weight (enriched hom-value acting as precision)
    for role k, o_k is the
    observed evidence for role k, and the precision-weighted product
    encodes the expected log-likelihood message. The posterior is
    normalised after each sweep. Convergence is declared when
    ``||q^{t+1} - q^{t}||₁ < 10⁻⁶``.

    The posterior precision is returned as ``Λ_posterior = Λ_prior + Λ_lik``
    for downstream use (e.g., P600 computation).

    Args:
        observations: Observed evidence vector (e.g., morphological likelihood),
            shape (n,). Values should be non-negative.
        prior_precision: Prior precision Λ_prior, shape (n,) or scalar.
        likelihood_precision: Likelihood precision Λ_lik, shape (n,) or scalar.
        n_iterations: Maximum number of message-passing sweeps.

    Returns:
        Tuple (posterior_probs, posterior_precision) both shape (n,).
        posterior_probs sums to 1.0.

    Raises:
        ValueError: On non-positive precisions or shape mismatch.
    """
    o = np.asarray(observations, dtype=np.float64)
    n = len(o)

    lp = np.broadcast_to(np.asarray(prior_precision, dtype=np.float64), (n,)).copy()
    ll = np.broadcast_to(np.asarray(likelihood_precision, dtype=np.float64), (n,)).copy()

    if np.any(lp <= 0):
        raise ValueError("prior_precision must be positive")
    if np.any(ll <= 0):
        raise ValueError("likelihood_precision must be positive")

    # Posterior precision: sum of prior and likelihood precisions
    lambda_post = lp + ll

    # Initialise q as uniform distribution (uninformative prior)
    q = np.full(n, 1.0 / n)

    # Fixed message from single observation factor (constant w.r.t. q)
    log_message = ll * o
    for iteration in range(n_iterations):
        # Categorical VMP fixed-point: q ∝ prior · exp(incoming message)
        # Prior is uniform so log(prior) cancels in normalisation.
        log_unnorm = log_message
        # Numerically stable softmax normalisation
        log_unnorm = log_unnorm - log_unnorm.max()
        q_new = np.exp(log_unnorm)
        q_new = q_new / q_new.sum()

        # Convergence check: L1 norm
        delta = float(np.sum(np.abs(q_new - q)))
        q = q_new
        if delta < 1e-6:
            logger.debug("VMP converged at iteration %d (Δ=%.2e)", iteration, delta)
            break

    logger.debug("VMP posterior: max=%.3f, entropy=%.3f", q.max(),
                 float(-np.sum(q[q > 0] * np.log(q[q > 0]))))
    return q, lambda_post


def bethe_free_energy(
    belief: CaseDiagramBelief,
    factor_beliefs: list[np.ndarray],
    adjacency: np.ndarray,
) -> float:
    """Bethe approximation of the variational free energy (Eq. 7c-bethe).

    The Bethe free energy decomposes the global variational FE into local
    factor and variable contributions (Yedidia et al. 2001):

        F_Bethe = Σ_α E_{b_α}[log b_α - log f_α] − Σ_i (d_i − 1) H(b_i)

    where b_α are factor beliefs, f_α are factor potentials, b_i are
    variable (role) marginals, d_i is the degree of variable i in the
    factor graph, and H(b_i) = -Σ b_i log b_i is the entropy.

    Each factor belief must have the same length as the variable beliefs
    (one entry per case role). If a factor involves only a subset of
    variables, the adjacency matrix encodes this — but the belief array
    is still defined over all n roles (marginalised appropriately by
    the caller).

    Args:
        belief: CaseDiagramBelief — the variable (role) marginals b_i.
        factor_beliefs: List of factor belief arrays, each shape (n,).
            Each array is a probability distribution over case roles.
        adjacency: Binary adjacency matrix (n_vars × n_factors), shape (n,m).
            adjacency[i,j] = 1 if variable i participates in factor j.

    Returns:
        Bethe free energy (lower is better; approximates variational FE).

    Raises:
        ValueError: On shape mismatch or non-positive beliefs.
    """
    b_vars = belief.probabilities
    n = len(b_vars)
    m = len(factor_beliefs)

    if adjacency.shape != (n, m):
        raise ValueError(f"Adjacency shape {adjacency.shape} != ({n},{m})")
    if np.any(b_vars <= 0):
        raise ValueError("Variable beliefs must be strictly positive")

    # Variable degrees: d_i = number of factors variable i participates in
    degrees = adjacency.sum(axis=1)  # shape (n,)

    # Variable entropy: H(b_i) = -Σ b_i log b_i
    safe_log_b = np.log(b_vars)
    var_entropy = float(-np.sum(b_vars * safe_log_b))  # H(b)

    # Variable contribution: Σ_i (d_i - 1) * H(b_i)
    # Since b_vars is a single shared distribution, H(b_i) = var_entropy for all i.
    var_contrib = float(np.sum(degrees - 1)) * var_entropy if n > 0 else 0.0

    # Factor contribution: Σ_α E_{b_α}[log b_α - log f_α] = KL(b_α || f_α)
    factor_contrib = 0.0
    for alpha, fb in enumerate(factor_beliefs):
        fb_arr = np.asarray(fb, dtype=np.float64)
        # Pad or truncate to match n roles, then normalise
        if len(fb_arr) < n:
            fb_padded = np.full(n, 1e-300)
            fb_padded[:len(fb_arr)] = fb_arr
            fb_arr = fb_padded
        elif len(fb_arr) > n:
            fb_arr = fb_arr[:n]
        fb_norm = fb_arr / fb_arr.sum() if fb_arr.sum() > 0 else np.full(n, 1.0 / n)
        b_norm = b_vars / b_vars.sum()
        # KL(b || f_α)
        kl = float(np.sum(b_norm * (np.log(b_norm + 1e-300) - np.log(fb_norm + 1e-300))))
        factor_contrib += kl

    bethe_fe = factor_contrib - var_contrib
    logger.debug("Bethe FE = %.6f (factor_contrib=%.4f, var_contrib=%.4f)",
                 bethe_fe, factor_contrib, var_contrib)
    return bethe_fe


def expected_information_gain(
    current_belief: CaseDiagramBelief,
    candidate_observations: np.ndarray,
) -> np.ndarray:
    """Epistemic value: expected information gain for each candidate observation.

    Implements Eq. 7c-eig from the manuscript. Computes the expected KL
    divergence between predicted posterior and current prior for each candidate
    observation — the epistemic value (EIG) of making that observation:

        EIG(o*) = E_q[KL(q(s|o*) || q(s))]
                = Σ_s q(s|o*) log(q(s|o*)/q(s)) · q(s,o*)

    Provides a measure of how much each candidate word/morpheme would reduce
    uncertainty about the current case-role assignment.

    Args:
        current_belief: Current belief distribution q(s) over roles.
        candidate_observations: Matrix of likelihood vectors, shape (n_obs, n_roles).
            Each row is p(o_k | s_i) for candidate observation k.

    Returns:
        EIG values for each candidate observation, shape (n_obs,).

    Raises:
        ValueError: On shape mismatch or non-positive likelihoods.
    """
    O = np.asarray(candidate_observations, dtype=np.float64)
    n_obs, n_roles = O.shape
    q = current_belief.probabilities

    if n_roles != len(q):
        raise ValueError(f"Observation columns ({n_roles}) must match roles ({len(q)})")
    if np.any(O < 0):
        raise ValueError("Likelihoods must be non-negative")

    eig = np.zeros(n_obs)

    for k in range(n_obs):
        lik = O[k]
        # Joint: p(s, o_k) = p(o_k|s) * q(s)
        joint = lik * q
        marginal = joint.sum()
        if marginal <= 0:
            eig[k] = 0.0
            continue
        # Posterior: q(s|o_k) = p(o_k|s)*q(s) / p(o_k)
        posterior = joint / marginal
        # KL(posterior || prior)
        safe_log_post = np.where(posterior > 0, np.log(posterior), -100.0)
        safe_log_prior = np.where(q > 0, np.log(q), -100.0)
        kl = float(np.sum(posterior * (safe_log_post - safe_log_prior)))
        # Weight by marginal likelihood
        eig[k] = marginal * max(0.0, kl)

    logger.debug("EIG: max=%.4f (obs %d), min=%.4f", eig.max(), int(np.argmax(eig)), eig.min())
    return eig
