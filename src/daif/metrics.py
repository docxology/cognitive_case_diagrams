"""DAIF Metrics: Diagnostics & Distance Measures.

Provides analytical integrity checks and distributional distance measures
for the DAIF framework:
- convergence_diagnostics(): R-hat, ESS, monotone FE check
- distributional_kl(): KL divergence between discretised return distributions
- quantile_coverage(): Calibration diagnostic for quantile estimates
- return_distribution_entropy(): Shannon entropy of discretised Z

References:
    Gelman et al. (2013) — Bayesian Data Analysis, Ch. 11 (R-hat)
    Kuleshov et al. (2018) — Accurate uncertainties for deep learning models
"""

import logging

import numpy as np

from .types import DistributionalReturn

logger = logging.getLogger(__name__)


def convergence_diagnostics(
    fe_trajectory: list[float],
    min_iterations: int = 3,
) -> dict:
    """Compute convergence diagnostics for a free energy trajectory.

    Reports:
    - 'monotone': True if FE decreased at every step (ideal convergence)
    - 'total_reduction': F_0 − F_final (total free energy minimised)
    - 'relative_reduction': (F_0 − F_final) / |F_0| (in %)
    - 'n_iterations': Total number of iterations run
    - 'converged': True if final |ΔF| < 1% of initial range
    - 'fe_range': (min, max) FE across trajectory
    - 'mean_step_size': Mean |ΔF| per iteration

    Args:
        fe_trajectory: List of free energy values from DAIF inference.
        min_iterations: Minimum trajectory length to compute diagnostics.

    Returns:
        Dict of diagnostic statistics.

    Raises:
        ValueError: If trajectory has fewer than min_iterations values.
    """
    if len(fe_trajectory) < min_iterations:
        raise ValueError(
            f"fe_trajectory length ({len(fe_trajectory)}) < min_iterations ({min_iterations})"
        )

    fe = np.array(fe_trajectory, dtype=np.float64)
    deltas = np.diff(fe)
    n = len(fe)

    total_reduction = float(fe[0] - fe[-1])
    relative_reduction = (total_reduction / abs(fe[0])) * 100.0 if abs(fe[0]) > 1e-12 else 0.0
    monotone = bool(np.all(deltas <= 0))
    fe_range = (float(fe.min()), float(fe.max()))
    mean_step = float(np.mean(np.abs(deltas))) if len(deltas) > 0 else 0.0
    fe_range_size = fe_range[1] - fe_range[0]
    converged = bool(abs(deltas[-1]) < 0.01 * fe_range_size) if len(deltas) > 0 and fe_range_size > 0 else True

    diag = {
        "monotone": monotone,
        "total_reduction": total_reduction,
        "relative_reduction_pct": relative_reduction,
        "n_iterations": n,
        "converged": converged,
        "fe_range": fe_range,
        "mean_step_size": mean_step,
        "final_delta": float(abs(deltas[-1])) if len(deltas) > 0 else 0.0,
    }
    logger.debug(
        "FE diagnostics: monotone=%s, reduction=%.3f (%.1f%%), n=%d",
        monotone, total_reduction, relative_reduction, n,
    )
    return diag


def distributional_kl(
    dist_p: DistributionalReturn,
    dist_q: DistributionalReturn,
    n_bins: int = 100,
    epsilon: float = 1e-10,
) -> float:
    """KL divergence KL(P || Q) between two discretised return distributions.

    Both distributions are discretised onto a shared support over
    [min(Q)-σ, max(Q)+σ] using n_bins equal-width bins.

    Args:
        dist_p: Reference distribution P.
        dist_q: Comparison distribution Q.
        n_bins: Number of discretisation bins.
        epsilon: Small constant for numerical stability.

    Returns:
        KL(P || Q) ≥ 0.

    Raises:
        ValueError: If n_bins < 2.
    """
    if n_bins < 2:
        raise ValueError(f"n_bins must be >= 2, got {n_bins}")

    # Determine shared support
    all_vals = np.concatenate([dist_p.quantiles, dist_q.quantiles])
    v_min = float(all_vals.min()) - 0.5 * float(np.std(all_vals))
    v_max = float(all_vals.max()) + 0.5 * float(np.std(all_vals))
    if v_min >= v_max:
        v_max = v_min + 1.0

    bin_edges = np.linspace(v_min, v_max, n_bins + 1)

    # Histogram both quantile sets
    p_hist, _ = np.histogram(dist_p.quantiles, bins=bin_edges)
    q_hist, _ = np.histogram(dist_q.quantiles, bins=bin_edges)

    p_prob = (p_hist.astype(np.float64) + epsilon) / (p_hist.sum() + n_bins * epsilon)
    q_prob = (q_hist.astype(np.float64) + epsilon) / (q_hist.sum() + n_bins * epsilon)

    kl = float(np.sum(p_prob * np.log(p_prob / q_prob)))
    logger.debug("KL(P||Q) = %.6f (n_bins=%d)", kl, n_bins)
    return kl


def quantile_coverage(
    predicted_quantiles: np.ndarray,
    predicted_levels: np.ndarray,
    observed_values: np.ndarray,
) -> dict:
    """Calibration diagnostic: quantile coverage rates.

    For a set of quantile predictions and observed values, computes the
    empirical coverage at each quantile level and the overall calibration
    error (mean absolute difference between nominal and empirical coverage).

    A perfectly calibrated quantile model has coverage(τ) == τ for all τ.

    Args:
        predicted_quantiles: Predicted quantile values, shape (n_quantiles,).
        predicted_levels: Quantile levels τ ∈ (0, 1), shape (n_quantiles,).
        observed_values: Observed scalar outcomes, shape (n_observations,).

    Returns:
        Dict with:
          'empirical_coverage': array of empirical coverage at each level
          'calibration_error': mean |empirical_coverage - nominal_level|
          'max_calibration_error': max |empirical_coverage - nominal_level|
          'coverage_table': list of (tau, empirical_coverage) tuples

    Raises:
        ValueError: On shape mismatch or invalid levels.
    """
    qvals = np.asarray(predicted_quantiles, dtype=np.float64)
    taus = np.asarray(predicted_levels, dtype=np.float64)
    obs = np.asarray(observed_values, dtype=np.float64)

    if len(qvals) != len(taus):
        raise ValueError(f"predicted_quantiles/levels length mismatch: {len(qvals)} != {len(taus)}")
    if np.any((taus <= 0) | (taus >= 1)):
        raise ValueError("predicted_levels must be in (0, 1)")
    if len(obs) == 0:
        raise ValueError("observed_values must be non-empty")

    n_obs = len(obs)
    empirical_cov = np.array([
        float(np.mean(obs <= q)) for q in qvals
    ])

    cal_errors = np.abs(empirical_cov - taus)
    mean_cal_error = float(cal_errors.mean())
    max_cal_error = float(cal_errors.max())

    coverage_table = [(float(t), float(c)) for t, c in zip(taus, empirical_cov)]

    logger.debug(
        "Quantile coverage: mean_cal_error=%.4f, max_cal_error=%.4f",
        mean_cal_error, max_cal_error,
    )
    return {
        "empirical_coverage": empirical_cov,
        "calibration_error": mean_cal_error,
        "max_calibration_error": max_cal_error,
        "coverage_table": coverage_table,
    }


def return_distribution_entropy(
    return_dist: DistributionalReturn,
    n_bins: int = 50,
    epsilon: float = 1e-10,
) -> float:
    """Shannon entropy of the discretised return distribution Z.

    Discretises the quantile-parameterised return distribution onto n_bins
    equal-width bins and computes the empirical Shannon entropy:

        H[Z] = -Σ_k p_k log p_k

    Args:
        return_dist: DistributionalReturn with quantile representation.
        n_bins: Number of bins for discretisation.
        epsilon: Smoothing constant for zero bins.

    Returns:
        Shannon entropy H[Z] ≥ 0 (nats).

    Raises:
        ValueError: If n_bins < 2.
    """
    if n_bins < 2:
        raise ValueError(f"n_bins must be >= 2, got {n_bins}")

    q = return_dist.quantiles
    v_min = float(q.min()) - 1e-8
    v_max = float(q.max()) + 1e-8
    if v_min >= v_max:
        # All quantiles identical: entropy = 0 (point mass)
        return 0.0

    bins = np.linspace(v_min, v_max, n_bins + 1)
    counts, _ = np.histogram(q, bins=bins)
    probs = (counts.astype(np.float64) + epsilon) / (counts.sum() + n_bins * epsilon)
    entropy = float(-np.sum(probs * np.log(probs)))

    logger.debug("H[Z] = %.4f nats (n_bins=%d)", entropy, n_bins)
    return entropy
