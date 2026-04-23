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
from __future__ import annotations

import logging

import numpy as np

from .types import DistributionalReturn

logger = logging.getLogger(__name__)

# Risk distortion constants (Dabney et al. 2019 — IQN)
_IQN_ETA_DISTORTION = 0.71   # Power-law exponent for optimistic/pessimistic distortion
_CVAR_ALPHA = 0.25            # CVaR quantile level threshold


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
    *,
    eta_distortion: float | None = None,
    cvar_alpha: float | None = None,
) -> np.ndarray:
    """IQN-style quantile update with sampled quantile levels and risk distortion.

    Extends QR-DQN by using explicitly provided quantile levels τ (rather than
    fixed midpoints) and supporting risk-distored statistics. This enables
    risk-sensitive case-role inference (e.g. optimistic/pessimistic processing).

    Risk distortions ψ_IQN(τ) applied to current_levels before update (manuscript §7c
    IQN table; same formulas as below). The curvature parameters η_IQN and α_CVaR
    default to the module-level constants ``_IQN_ETA_DISTORTION`` (0.71, Dabney et
    al. 2019) and ``_CVAR_ALPHA`` (0.25); pass ``eta_distortion=`` and
    ``cvar_alpha=`` as keyword arguments to override per-call:

      - 'neutral': ψ_IQN(τ) = τ
      - 'optimistic': ψ_IQN(τ) = τ^(1/η_IQN)        (η_IQN < 1 ⇒ optimistic)
      - 'pessimistic': ψ_IQN(τ) = 1 − (1−τ)^(1/η_IQN)
      - 'CVaR': ψ_IQN(τ) = τ · α_CVaR                (α_CVaR ∈ (0,1])

    Args:
        current_quantiles: Current quantile estimates (one per quantile level).
        current_levels: Quantile levels τ ∈ (0,1) for current estimates.
        target_quantiles: Target quantile samples from push-forward.
        target_levels: Quantile levels for target samples.
        learning_rate: Step size α ∈ (0,1].
        kappa: Huber threshold.
        risk_distortion: One of 'neutral', 'optimistic', 'pessimistic', 'CVaR'.
        eta_distortion: Optional override for η_IQN (default ``_IQN_ETA_DISTORTION``
            = 0.71). Must satisfy 0 < η_IQN (typically < 1 for the stated convention).
        cvar_alpha: Optional override for α_CVaR (default ``_CVAR_ALPHA`` = 0.25).
            Must satisfy 0 < α_CVaR ≤ 1.

    Returns:
        Updated current_quantiles (same shape).

    Raises:
        ValueError: On invalid inputs, unknown risk distortion, or out-of-range
            ``eta_distortion`` / ``cvar_alpha``.
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

    # Resolve curvature parameters, allowing per-call override of the module defaults.
    eta = _IQN_ETA_DISTORTION if eta_distortion is None else float(eta_distortion)
    alpha = _CVAR_ALPHA if cvar_alpha is None else float(cvar_alpha)
    if eta <= 0:
        raise ValueError(f"eta_distortion must be > 0, got {eta}")
    if not 0.0 < alpha <= 1.0:
        raise ValueError(f"cvar_alpha must be in (0,1], got {alpha}")

    # Apply risk distortion to current quantile levels
    if risk_distortion == "neutral":
        tau_distorted = cl
    elif risk_distortion == "optimistic":
        tau_distorted = cl ** (1.0 / eta)
    elif risk_distortion == "pessimistic":
        tau_distorted = 1.0 - (1.0 - cl) ** (1.0 / eta)
    else:  # CVaR
        tau_distorted = cl * alpha

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
    """Compute a discrete-quantile approximation of the p-Wasserstein distance.

    The exact p-Wasserstein distance between two real-valued return
    distributions is the L^p norm of their inverse CDFs:

        W_p(Z_a, Z_b) = (∫₀¹ |F_a⁻¹(τ) − F_b⁻¹(τ)|^p dτ)^(1/p)

    For discretised quantile representations {(τ_i, z_i)}_{i=1..N} this
    integral is approximated by the *uniformly-weighted* sample mean

        Ŵ_p = (Σ_i |q_a(τ_i) − q_b(τ_i)|^p / N)^(1/p) ,

    which is exact only when the τ_i are equally spaced and
    Σ_i (τ_{i+1}−τ_i)=1. For the τ grids produced by
    ``DistributionalReturn`` (midpoint-spaced) the approximation is
    consistent to O(1/N). Note this is the canonical estimator used in
    quantile-regression RL (Dabney et al., 2018) rather than a formal
    optimal-transport computation.

    If ``dist_a`` and ``dist_b`` have different quantile grid sizes the
    shorter one is re-sampled via linear interpolation onto a common
    grid of ``max(len(qa), len(qb))`` midpoints in [0.01, 0.99]. That
    resampling is performed on *quantile values*, not on the underlying
    quantile function, so it introduces an additional O(N⁻²) error
    beyond the midpoint-discretisation error already present for a
    single grid; true distributional transport would require a full
    optimal-transport solve which this helper explicitly avoids.

    Args:
        dist_a: First DistributionalReturn.
        dist_b: Second DistributionalReturn.
        p: Wasserstein order, 1 (earth-mover's distance) or 2 (RMS).

    Returns:
        Non-negative float W_p(Z_a, Z_b).

    Raises:
        ValueError: If p ∉ {1, 2}.
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
