"""DAIF Quantile Module: Quantile TD Learning.

Implements quantile-based temporal difference update methods including:
- quantile_td_update(): Quantile Huber loss TD (Dabney et al. 2018)
- implicit_quantile_network_update(): IQN-style update with risk-sensitive levels
- wasserstein_return_distance(): 1-Wasserstein metric between return distributions

References:
    Dabney et al. (2018) — Distributional RL with Quantile Regression
    Dabney et al. (2019) — Implicit Quantile Networks for Distributional RL
    Villani (2009) — Optimal Transport
"""

import logging

import numpy as np

from .types import DistributionalReturn

logger = logging.getLogger(__name__)


def quantile_td_update(
    current_quantiles: np.ndarray,
    target_quantiles: np.ndarray,
    learning_rate: float = 0.1,
    kappa: float = 1.0,
) -> np.ndarray:
    """Quantile-matching TD update via asymmetric Huber loss (QR-DQN).

    Updates current quantile estimates θ_i toward target quantiles z_j
    using the quantile Huber loss gradient:

        ρ_τ^κ(δ) = |τ − I(δ < 0)| · L_κ(δ)

    where L_κ is the Huber loss with threshold κ and τ_i = (2i+1)/(2N).

    Args:
        current_quantiles: Current quantile estimates θ (sorted ascending).
        target_quantiles: Target quantile values z from push-forward.
        learning_rate: Step size α ∈ (0,1].
        kappa: Huber loss threshold κ > 0.

    Returns:
        Updated quantile estimates (same shape as current_quantiles).

    Raises:
        ValueError: On shape mismatch or invalid parameters.
    """
    q = np.asarray(current_quantiles, dtype=np.float64)
    t = np.asarray(target_quantiles, dtype=np.float64)

    if len(q) != len(t):
        raise ValueError(f"Quantile arrays must match: {len(q)} != {len(t)}")
    if not 0.0 < learning_rate <= 1.0:
        raise ValueError(f"learning_rate must be in (0,1], got {learning_rate}")
    if kappa <= 0:
        raise ValueError(f"kappa must be positive, got {kappa}")

    n = len(q)
    taus = (2 * np.arange(n) + 1) / (2 * n)
    delta = t - q

    # Huber loss gradient
    huber_grad = np.where(np.abs(delta) <= kappa, delta, kappa * np.sign(delta))

    # Asymmetric weighting by quantile position
    weights = np.where(delta >= 0, taus, 1.0 - taus)
    updated = q + learning_rate * weights * huber_grad

    logger.debug(
        "QR-DQN update: mean_delta=%.4f, max_|delta|=%.4f",
        np.mean(np.abs(delta)), np.max(np.abs(delta)),
    )
    return updated


def implicit_quantile_network_update(
    current_quantiles: np.ndarray,
    current_levels: np.ndarray,
    target_quantiles: np.ndarray,
    target_levels: np.ndarray,
    learning_rate: float = 0.1,
    kappa: float = 1.0,
    risk_distortion: str = "neutral",
) -> np.ndarray:
    """IQN-style quantile update with sampled quantile levels and risk distortion.

    Extends QR-DQN by using explicitly provided quantile levels τ (rather than
    fixed midpoints) and supporting risk-distored statistics. This enables
    risk-sensitive case-role inference (e.g. optimistic/pessimistic processing).

    Risk distortions applied to current_levels before update:
      - 'neutral': identity (standard IQN)
      - 'optimistic': β(τ) = τ^(1/η), η=0.71, upweights high returns
      - 'pessimistic': β(τ) = 1 − (1-τ)^(1/η), upweights low returns
      - 'CVaR': τ' = τ · α (conditional value at risk, α=0.25)

    Args:
        current_quantiles: Current quantile estimates (one per quantile level).
        current_levels: Quantile levels τ ∈ (0,1) for current estimates.
        target_quantiles: Target quantile samples from push-forward.
        target_levels: Quantile levels for target samples.
        learning_rate: Step size α ∈ (0,1].
        kappa: Huber threshold.
        risk_distortion: One of 'neutral', 'optimistic', 'pessimistic', 'CVaR'.

    Returns:
        Updated current_quantiles (same shape).

    Raises:
        ValueError: On invalid inputs or unknown risk distortion.
    """
    cq = np.asarray(current_quantiles, dtype=np.float64)
    cl = np.asarray(current_levels, dtype=np.float64)
    tq = np.asarray(target_quantiles, dtype=np.float64)
    tl = np.asarray(target_levels, dtype=np.float64)

    if len(cq) != len(cl):
        raise ValueError(f"current_quantiles/levels length mismatch: {len(cq)} != {len(cl)}")
    if len(tq) != len(tl):
        raise ValueError(f"target_quantiles/levels length mismatch: {len(tq)} != {len(tl)}")
    if not 0.0 < learning_rate <= 1.0:
        raise ValueError(f"learning_rate must be in (0,1], got {learning_rate}")
    if kappa <= 0:
        raise ValueError(f"kappa must be positive, got {kappa}")
    if np.any((cl <= 0) | (cl >= 1)):
        raise ValueError("current_levels must be in (0,1)")
    if np.any((tl <= 0) | (tl >= 1)):
        raise ValueError("target_levels must be in (0,1)")

    valid_distortions = ("neutral", "optimistic", "pessimistic", "CVaR")
    if risk_distortion not in valid_distortions:
        raise ValueError(f"risk_distortion must be one of {valid_distortions}")

    # Apply risk distortion to current quantile levels
    eta = 0.71
    if risk_distortion == "neutral":
        tau_distorted = cl
    elif risk_distortion == "optimistic":
        tau_distorted = cl ** (1.0 / eta)
    elif risk_distortion == "pessimistic":
        tau_distorted = 1.0 - (1.0 - cl) ** (1.0 / eta)
    else:  # CVaR
        cvar_alpha = 0.25
        tau_distorted = cl * cvar_alpha

    # Pairwise Huber loss: N_current × N_target
    delta = tq[np.newaxis, :] - cq[:, np.newaxis]  # (N_curr, N_tgt)
    huber_grad = np.where(np.abs(delta) <= kappa, delta, kappa * np.sign(delta))

    # Asymmetric weights: τ' for positive errors, 1-τ' for negative
    tau_exp = tau_distorted[:, np.newaxis]  # (N_curr, 1)
    weights = np.where(delta >= 0, tau_exp, 1.0 - tau_exp)

    # Mean over target samples, sum over quantile batches
    grad = np.mean(weights * huber_grad, axis=1)
    updated = cq + learning_rate * grad

    logger.debug(
        "IQN update (%s): mean_grad=%.4f, max_|grad|=%.4f",
        risk_distortion, np.mean(np.abs(grad)), np.max(np.abs(grad)),
    )
    return updated


def wasserstein_return_distance(
    dist_a: DistributionalReturn,
    dist_b: DistributionalReturn,
    p: int = 1,
) -> float:
    """Compute the p-Wasserstein distance between two return distributions.

    For discretised quantile representations, the p-Wasserstein distance is:

        W_p(Z_a, Z_b) = (∫₀¹ |F_a⁻¹(τ) - F_b⁻¹(τ)|^p dτ)^(1/p)

    approximated by the sample mean over shared quantile levels.

    Args:
        dist_a: First DistributionalReturn.
        dist_b: Second DistributionalReturn.
        p: Wasserstein order (1 or 2). Default 1 (earth mover's distance).

    Returns:
        p-Wasserstein distance W_p(Z_a, Z_b) ≥ 0.

    Raises:
        ValueError: If quantile arrays have different lengths or p ∉ {1,2}.
    """
    if p not in (1, 2):
        raise ValueError(f"p must be 1 or 2, got {p}")

    qa = dist_a.quantiles
    qb = dist_b.quantiles

    if len(qa) != len(qb):
        # Interpolate onto a common grid
        common_taus = np.linspace(0.01, 0.99, max(len(qa), len(qb)))
        qa = np.interp(common_taus, dist_a.quantile_levels, qa)
        qb = np.interp(common_taus, dist_b.quantile_levels, qb)

    diff = np.abs(qa - qb)
    if p == 1:
        w = float(np.mean(diff))
    else:
        w = float(np.sqrt(np.mean(diff ** 2)))

    logger.debug("W_%d(Z_a, Z_b) = %.6f", p, w)
    return w
