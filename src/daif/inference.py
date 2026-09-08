"""Repeated-observation Bayesian filtering and explicitly limited score utilities."""
from __future__ import annotations

import logging
from typing import Optional

import numpy as np

from ..cognitive.belief import CaseDiagramBelief
from ..cognitive.free_energy import kl_divergence, variational_free_energy
from .types import DAIFResult, DistributionalReturn
from ..numerics import finite_vector, stochastic_matrix, positive_integer, weighted_quantiles

logger = logging.getLogger(__name__)


def distributional_case_assignment(
    prior: CaseDiagramBelief,
    observation_likelihoods: np.ndarray,
    transition_matrix: Optional[np.ndarray] = None,
    n_iterations: int = 10,
    convergence_threshold: float = 1e-6,
    n_quantiles: int = 51,
) -> DAIFResult:
    """Apply the same observation likelihood on successive Markov filter steps.

Each step predicts T.T@q then normalizes likelihood*prediction, records
F = KL(posterior||prediction) - posterior@log(likelihood), and stores that
posterior. This reuses evidence intentionally; it is not repeated optimization
of one fixed posterior. n_iterations=1 consumes the likelihood once.
Convergence requires both belief L1 change and FE change below threshold.
Diagnostics identify the stop reason and retain all updated beliefs. The
return_distribution is a dimensionless log-likelihood score heuristic.
"""
    likelihoods = finite_vector(observation_likelihoods, "Likelihoods")
    if np.any(likelihoods < 0):
        raise ValueError("Likelihoods must be non-negative")
    positive_integer(n_iterations, "n_iterations")
    positive_integer(n_quantiles, "n_quantiles", 2)
    if not np.isfinite(convergence_threshold) or convergence_threshold <= 0:
        raise ValueError("convergence_threshold must be finite and positive")
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
        T = stochastic_matrix(transition_matrix, n)

    current = prior
    fe_trajectory: list[float] = []
    kl_trajectory: list[float] = []       # D_KL(q_posterior || q_pushed) per iteration
    loglik_trajectory: list[float] = []   # E_q[log p(o|s)] per iteration
    belief_trajectory: list[list[float]] = []
    stop_reason = "iteration_limit"
    convergence_iter = n_iterations

    # Reward proxy: log-likelihood as reward signal
    # np.where evaluates both branches, so np.log must never see a 0 — guard the
    # argument, not just the result, or numpy emits a divide-by-zero RuntimeWarning.
    _lik_attainable = likelihoods > 0
    safe_log_lik = np.where(
        _lik_attainable, np.log(np.where(_lik_attainable, likelihoods, 1.0)), -100.0
    )

    for iteration in range(n_iterations):
        q = current.probabilities

        # Step 1: Push-forward
        q_pushed = T.T @ q
        total_pushed = q_pushed.sum()
        q_pushed = q_pushed / total_pushed

        # Step 2: Bayesian update q(s) ∝ p(o|s) · q_pushed(s)
        scale = likelihoods.max()
        unnorm = (likelihoods / scale if scale > 0 else likelihoods) * q_pushed
        total = unnorm.sum()
        if total <= 0:
            raise ValueError("Observation incompatible with predicted prior: zero posterior mass")
        posterior = unnorm / total

        # Step 3: Variational free energy with explicit KL / data-fit decomposition.
        # F = KL(q_posterior || q_pushed) − E_q[log p(o|s)]
        _prior_nonzero = q_pushed > 0
        safe_log_prior = np.where(
            _prior_nonzero, np.log(np.where(_prior_nonzero, q_pushed, 1.0)), -100.0
        )
        fe = variational_free_energy(posterior, safe_log_lik, safe_log_prior)
        kl_term = float(kl_divergence(posterior, q_pushed))
        expected_loglik = float(np.sum(posterior * safe_log_lik))
        fe_trajectory.append(fe)
        kl_trajectory.append(kl_term)
        loglik_trajectory.append(expected_loglik)

        # Each iteration assimilates the same likelihood as another observation.
        # Priors change, so FE values do not share one fixed objective. An increase
        # is not evidence of optimizer divergence. Store the state before stopping.
        belief_delta = float(np.sum(np.abs(posterior - current.probabilities)))
        current = CaseDiagramBelief(
            roles=prior.roles, probabilities=posterior,
            name=f"{prior.name}_daif_t{iteration + 1}",
        )
        belief_trajectory.append(posterior.tolist())
        if (len(fe_trajectory) > 1
                and abs(fe_trajectory[-1] - fe_trajectory[-2]) < convergence_threshold
                and belief_delta < convergence_threshold):
            convergence_iter = iteration
            stop_reason = "stationary_filter"
            break
        logger.debug(
            "DAIF iter %d: H=%.4f, F=%.4f, mode=%s",
            iteration, current.entropy(), fe, current.most_likely_role().name,
        )

    # Build DistributionalReturn from final belief and reward proxy
    tau_levels = np.linspace(1 / (2 * n_quantiles), 1 - 1 / (2 * n_quantiles), n_quantiles)
    q_final = current.probabilities
    # Anchor the reward scale to ATTAINABLE roles only. Anchoring to
    # safe_log_lik.min() let the -100.0 unattainable-role sentinel set the zero
    # point, so an unreachable role shifted the reported return mean by ~100
    # (and by a different amount for every likelihood floor).
    reward_floor = float(np.log(likelihoods[_lik_attainable]).min())
    reward_proxy = np.where(_lik_attainable, safe_log_lik - reward_floor, 0.0)
    z_vec = reward_proxy  # Shifted log-likelihood score, not a Bellman return
    mean_z = float(q_final @ z_vec)
    var_z = max(0.0, float(q_final @ z_vec ** 2) - mean_z ** 2)
    quantile_vals = weighted_quantiles(z_vec, q_final, tau_levels)

    ret_dist = DistributionalReturn(
        mean=mean_z, variance=var_z,
        quantiles=quantile_vals, quantile_levels=tau_levels,
    )

    diagnostics = {
        "stop_reason": stop_reason,
        "belief_trajectory": belief_trajectory,
        "evidence_mode": "repeated_observation",
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
    """Single-factor categorical update with an implicit uniform prior.

Returns softmax(likelihood_precision*observations) and the bookkeeping sum
prior_precision+likelihood_precision. The latter does not parameterize the
categorical prior; changing prior_precision cannot change the probabilities.
Messages are constant, so additional sweeps do not incorporate new evidence.
This is not general factor-graph or loopy belief propagation.
"""
    o = finite_vector(observations, "observations")
    positive_integer(n_iterations, "n_iterations")
    n = len(o)

    lp = np.broadcast_to(np.asarray(prior_precision, dtype=np.float64), (n,)).copy()
    ll = np.broadcast_to(np.asarray(likelihood_precision, dtype=np.float64), (n,)).copy()

    if not np.all(np.isfinite(lp)) or np.any(lp <= 0):
        raise ValueError("prior_precision must be positive")
    if not np.all(np.isfinite(ll)) or np.any(ll <= 0):
        raise ValueError("likelihood_precision must be positive")

    # Posterior precision: sum of prior and likelihood precisions
    lambda_post = lp + ll

    # Initialise q as uniform distribution (uninformative prior)
    q = np.full(n, 1.0 / n)

    # Fixed message from single observation factor (constant w.r.t. q)
    log_message = ll * o
    if not np.all(np.isfinite(log_message)):
        raise ValueError("Precision-weighted evidence overflowed")
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
    """Legacy factor-consistency score; this is not Bethe free energy.

Computes sum_a KL(q||normalized factor_a) - sum_i(degree_i-1)*H(q).
There is one role distribution, not one marginal per graph variable, and
no factor potentials or joint factor beliefs. Use factor_consistency_score
for a name that states the implemented contract. Strictly positive q is
retained for compatibility; factors must be finite nonnegative vectors.
"""
    b_vars = belief.probabilities
    n = len(b_vars)
    m = len(factor_beliefs)

    adjacency = np.asarray(adjacency, dtype=float)
    if not np.all(np.isin(adjacency, [0, 1])):
        raise ValueError("Adjacency must be binary")
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
        fb_arr = finite_vector(fb, f"factor_beliefs[{alpha}]")
        if np.any(fb_arr < 0):
            raise ValueError("Factor beliefs must be non-negative")
        # Honour the documented contract. The previous pad-with-1e-300 /
        # truncate behaviour silently discarded probability mass in the dropped
        # slots and returned a plausible number, so a caller passing the wrong
        # shape got no signal at all.
        if len(fb_arr) != n:
            raise ValueError(
                f"factor_beliefs[{alpha}] has length {len(fb_arr)}, expected {n}"
            )
        fb_sum = fb_arr.sum()
        if fb_sum <= 0:
            raise ValueError(
                f"factor_beliefs[{alpha}] sums to {fb_sum}; expected a positive mass"
            )
        fb_norm = fb_arr / fb_sum
        b_norm = b_vars / b_vars.sum()
        # KL(b || f_α)
        kl = kl_divergence(b_norm, fb_norm)
        factor_contrib += kl

    bethe_fe = factor_contrib - var_contrib
    logger.debug("Factor-consistency score = %.6f (factor_contrib=%.4f, var_contrib=%.4f)",
                 bethe_fe, factor_contrib, var_contrib)
    return bethe_fe


def expected_information_gain(
    current_belief: CaseDiagramBelief,
    candidate_observations: np.ndarray,
) -> np.ndarray:
    """Return each observation contribution p(o)*KL(p(s|o)||q(s)).

Rows are nonnegative finite likelihood vectors p(o|s). Summing the output
gives mutual information only when columns sum to one over an exhaustive
observation alphabet. Otherwise these are unnormalized design scores.
"""
    likelihoods = np.asarray(candidate_observations, dtype=np.float64)
    if likelihoods.ndim != 2 or likelihoods.shape[0] == 0 or not np.all(np.isfinite(likelihoods)):
        raise ValueError("candidate_observations must be a nonempty finite matrix")
    n_obs, n_roles = likelihoods.shape
    q = current_belief.probabilities

    if n_roles != len(q):
        raise ValueError(f"Observation columns ({n_roles}) must match roles ({len(q)})")
    if np.any(likelihoods < 0):
        raise ValueError("Likelihoods must be non-negative")

    eig = np.zeros(n_obs)

    for k in range(n_obs):
        lik = likelihoods[k]
        # Joint: p(s, o_k) = p(o_k|s) * q(s)
        joint = lik * q
        marginal = joint.sum()
        if marginal <= 0:
            eig[k] = 0.0
            continue
        # Posterior: q(s|o_k) = p(o_k|s)*q(s) / p(o_k)
        posterior = joint / marginal
        # KL(posterior || prior)
        kl = kl_divergence(posterior, q)
        # Weight by marginal likelihood
        eig[k] = marginal * max(0.0, kl)

    logger.debug("EIG: max=%.4f (obs %d), min=%.4f", eig.max(), int(np.argmax(eig)), eig.min())
    return eig


# Canonical name; legacy API remains available.
factor_consistency_score = bethe_free_energy
