"""DAIF Quantile Module: Quantile TD Learning.

Implements quantile-based temporal difference update methods including:
- quantile_td_update(): Quantile Huber loss TD (Dabney et al. 2018)
- implicit_quantile_network_update(): IQN-style update with risk-sensitive levels
- wasserstein_return_distance(): 1-Wasserstein metric between return distributions

References:
    Dabney et al. (2018) — Distributional RL with Quantile Regression
    Dabney et al. (2018) — Implicit Quantile Networks for Distributional RL
    Villani (2009) — Optimal Transport
"""
from __future__ import annotations

import logging

import numpy as np

from .types import DistributionalReturn
from ..numerics import finite_vector, quantile_grid

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
    """Pairwise quantile Huber update with a mean over target samples.

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
    # Unnormalised Huber convention: rho = |tau - I(delta < 0)| L_kappa.
    # Each coordinate uses all target samples; current/target sizes may differ.
    q = finite_vector(current_quantiles, "current_quantiles")
    t = finite_vector(target_quantiles, "target_quantiles")

    if not 0.0 < learning_rate <= 1.0:
        raise ValueError(f"learning_rate must be in (0,1], got {learning_rate}")
    if not np.isfinite(kappa) or kappa <= 0:
        raise ValueError(f"kappa must be positive, got {kappa}")

    n = len(q)
    taus = (2 * np.arange(n) + 1) / (2 * n)
    delta = t[None, :] - q[:, None]

    # Huber loss gradient
    huber_grad = np.where(np.abs(delta) <= kappa, delta, kappa * np.sign(delta))

    # Asymmetric weighting by quantile position
    weights = np.where(delta >= 0, taus[:, None], 1.0 - taus[:, None])
    updated = q + learning_rate * np.mean(weights * huber_grad, axis=1)

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
    """Pairwise quantile-Huber update using distorted current probability levels.

Target values are treated as equally weighted samples. Their supplied levels
are checked for shape and range, not used as quadrature weights. No neural
network is learned and no quantile function is interpolated by this helper.
For 0 < eta < 1, optimistic distortion raises current tau and pessimistic
distortion lowers it. CVaR multiplies tau by alpha to emphasize the lower tail.
Uses unnormalized Huber loss and a target-averaged coordinate gradient.
"""
    cq = finite_vector(current_quantiles, "current_quantiles")
    cl = finite_vector(current_levels, "current_levels")
    tq = finite_vector(target_quantiles, "target_quantiles")
    tl = finite_vector(target_levels, "target_levels")

    if len(cq) != len(cl):
        raise ValueError(f"current_quantiles/levels length mismatch: {len(cq)} != {len(cl)}")
    if len(tq) != len(tl):
        raise ValueError(f"target_quantiles/levels length mismatch: {len(tq)} != {len(tl)}")
    if not 0.0 < learning_rate <= 1.0:
        raise ValueError(f"learning_rate must be in (0,1], got {learning_rate}")
    if not np.isfinite(kappa) or kappa <= 0:
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
    if not np.isfinite(eta) or eta <= 0:
        raise ValueError(f"eta_distortion must be > 0, got {eta}")
    if not 0.0 < alpha <= 1.0:
        raise ValueError(f"cvar_alpha must be in (0,1], got {alpha}")

    # Apply risk distortion to current quantile levels
    if risk_distortion == "neutral":
        tau_distorted = cl
    elif risk_distortion == "optimistic":
        tau_distorted = 1.0 - (1.0 - cl) ** (1.0 / eta)
    elif risk_distortion == "pessimistic":
        tau_distorted = cl ** (1.0 / eta)
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
    """Wasserstein distance between piecewise-linear quantile reconstructions.

    Both supplied level grids are used, including when their lengths match.
    Between levels quantiles are linearly interpolated; tails are held constant
    to 0 and 1. The integral is exact for these reconstructed distributions,
    not necessarily for the distributions that generated the stored quantiles.
    No universal discretization-error rate is assumed.
    """
    if p not in (1, 2):
        raise ValueError(f"p must be 1 or 2, got {p}")
    qa, ta = quantile_grid(dist_a.quantiles, dist_a.quantile_levels)
    qb, tb = quantile_grid(dist_b.quantiles, dist_b.quantile_levels)
    knots = np.unique(np.concatenate(([0., 1.], ta, tb)))
    delta = np.interp(knots, ta, qa) - np.interp(knots, tb, qb)
    a, b = delta[:-1], delta[1:]
    widths = np.diff(knots)
    if p == 2:
        integral = np.sum(widths * (a*a + a*b + b*b) / 3.)
        return float(np.sqrt(max(0., integral)))
    areas = (np.abs(a) + np.abs(b)) / 2.
    crosses = a * b < 0
    areas[crosses] = ((a[crosses]**2 + b[crosses]**2)
                      / (2. * (np.abs(a[crosses]) + np.abs(b[crosses]))))
    return float(np.sum(widths * areas))
