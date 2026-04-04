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
        T = np.eye(n)
    else:
        T = np.asarray(transition_matrix, dtype=np.float64)
        if T.shape != (n, n):
            raise ValueError(f"Transition matrix shape {T.shape} != ({n}, {n})")
        if not np.allclose(T.sum(axis=1), 1.0, atol=1e-8):
            raise ValueError("Transition matrix rows must sum to 1.0")

    current = prior
    fe_trajectory: list[float] = []
    convergence_iter = n_iterations

    # Reward proxy: log-likelihood as reward signal
    safe_log_lik = np.where(likelihoods > 0, np.log(likelihoods), -100.0)

    for iteration in range(n_iterations):
        q = current.probabilities

        # Step 1: Push-forward
        q_pushed = T.T @ q
        total_pushed = q_pushed.sum()
        if total_pushed <= 0:
            logger.warning("Push-forward degenerate at iteration %d", iteration)
            break
        q_pushed = q_pushed / total_pushed

        # Step 2: Bayesian update q(s) ∝ p(o|s) · q_pushed(s)
        unnorm = likelihoods * q_pushed
        total = unnorm.sum()
        if total <= 0:
            logger.warning("DAIF: all posteriors zero at iteration %d", iteration)
            break
        posterior = unnorm / total

        # Step 3: Variational free energy
        safe_log_prior = np.where(q_pushed > 0, np.log(q_pushed), -100.0)
        fe = variational_free_energy(posterior, safe_log_lik, safe_log_prior)
        fe_trajectory.append(fe)

        # Step 4: Convergence check
        if len(fe_trajectory) > 1:
            delta_fe = abs(fe_trajectory[-1] - fe_trajectory[-2])
            if delta_fe < convergence_threshold:
                convergence_iter = iteration
                logger.info("DAIF converged at iteration %d (ΔF=%.2e)", iteration, delta_fe)
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
    """Structured variational inference via precision-weighted message passing.

    Implements the VMP update equations for a Gaussian factor graph:

        μ_posterior = (Λ_prior + Λ_likelihood)⁻¹ (Λ_prior μ_prior + Λ_likelihood o)
        Λ_posterior = Λ_prior + Λ_likelihood

    For the distributional case: each role carries a precision parameter
    (from the enriched category hom-values), and messages are weighted
    accordingly across n_iterations of damped belief propagation.

    Args:
        observations: Observed evidence vector, shape (n,).
        prior_precision: Prior precision Λ_prior, shape (n,) or scalar.
        likelihood_precision: Likelihood precision Λ_lik, shape (n,) or scalar.
        n_iterations: Number of message-passing sweeps.

    Returns:
        Tuple (posterior_mean, posterior_precision) both shape (n,).

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

    # Prior mean: uniform (zero-centred normalised)
    mu_prior = np.zeros(n)

    # Damped VMP: initialise at prior
    mu = mu_prior.copy()
    lambda_post = lp.copy()

    for _ in range(n_iterations):
        # Posterior precision: sum of precisions
        lambda_post = lp + ll
        # Posterior mean: precision-weighted average
        mu = (lp * mu_prior + ll * o) / lambda_post

        # Convert to probability by softmax (for distributional interpretation)
        mu_soft = np.exp(mu - mu.max())
        mu = mu_soft / mu_soft.sum()

        # Update prior mean for next sweep (damped: 0.8 old + 0.2 new)
        mu_prior = 0.8 * mu_prior + 0.2 * mu

    logger.debug("VMP converged: mean=%.3f±%.3f", mu.mean(), mu.std())
    return mu, lambda_post


def bethe_free_energy(
    belief: CaseDiagramBelief,
    factor_beliefs: list[np.ndarray],
    adjacency: np.ndarray,
) -> float:
    """Bethe approximation of the variational free energy over a belief network.

    The Bethe free energy decomposes the global variational FE into local
    factor and variable contributions (Yedidia et al. 2001):

        F_Bethe = Σ_α E_b_α[log b_α/f_α] − Σ_i (d_i − 1) E_b_i[log b_i]

    where b_α are factor beliefs, f_α are factor potentials approximated
    by the observation likelihoods, b_i are variable (role) beliefs,
    and d_i is the degree of variable i in the factor graph.

    Args:
        belief: CaseDiagramBelief — the variable (role) marginals b_i.
        factor_beliefs: List of factor belief arrays, each shape (n_i,).
            Each array is a probability distribution over the factor's scope.
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

    # Variable entropy contribution: -(d_i - 1) * H(b_i)
    h_vars = float(np.sum(b_vars * np.log(b_vars + 1e-300)))  # -H
    var_contrib = float(np.sum((degrees - 1) * b_vars * np.log(b_vars + 1e-300)))

    # Factor contribution: KL(b_α || f_α) for each factor
    factor_contrib = 0.0
    for alpha, fb in enumerate(factor_beliefs):
        fb_arr = np.asarray(fb, dtype=np.float64)
        # Marginalise down from full factor belief to matching size
        n_alpha = min(n, len(fb_arr))
        fb_marg = fb_arr[:n_alpha]
        b_marg = b_vars[:n_alpha]
        # Normalise both
        fb_marg = fb_marg / fb_marg.sum() if fb_marg.sum() > 0 else np.full(n_alpha, 1.0 / n_alpha)
        b_marg = b_marg / b_marg.sum()
        # KL(b||f)
        safe_log = np.where(fb_marg > 0, np.log(fb_marg), -100.0)
        kl = float(np.sum(b_marg * (np.log(b_marg + 1e-300) - safe_log)))
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

    Computes the expected KL divergence between predicted posterior and current
    prior for each candidate observation — this is the epistemic value (EIG) of
    making that observation:

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
