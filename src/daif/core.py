"""Finite distributions of dimensionless role scores and C51-style projection.

Legacy return/Bellman names are retained for compatibility. The score is
R + gamma * T.T @ q; it is not a discounted cumulative reward.
"""
from __future__ import annotations

import logging
from typing import Optional

import numpy as np

from ..cognitive.belief import CaseDiagramBelief
from .types import DistributionalReturn
from ..numerics import (finite_vector, stochastic_matrix, positive_integer,
                        weighted_quantiles, quantile_grid)

logger = logging.getLogger(__name__)


def _single_bellman_step(
    current_q: np.ndarray,
    transition_matrix: np.ndarray,
    reward_vector: np.ndarray,
    gamma: float,
    n_quantiles: int,
) -> DistributionalReturn:
    """Compute the law of score z_i = R_i + gamma*(T.T@q)_i with mass q_i.

Moments are exact finite sums. Quantiles use the generalized inverse CDF
(with zero-mass support removed), not interpolation between distinct atoms.
"""
    positive_integer(n_quantiles, "n_quantiles", 2)
    T = transition_matrix
    R = reward_vector

    # Dimensionless per-role score with predicted occupancy
    z_vec = R + gamma * T.T @ current_q

    if not np.all(np.isfinite(z_vec)):
        raise ValueError(
            f"Non-finite values in z_vec after score construction — check reward_vector "
            f"and transition_matrix for NaN/inf. z_vec={z_vec!r}"
        )
    # Stable moments via a reference-shifted computation: offsets from the
    # first score keep the arithmetic small, so a constant return law has
    # variance exactly 0 at any magnitude (the naive second moment and the
    # mean-centered form both lose the constant case to catastrophic
    # rounding at ~1e160 scales). ValueError is reserved for genuinely
    # unrepresentable results: a non-finite mean, or a centered variance
    # beyond float range.
    reference = z_vec[0]
    offsets = z_vec - reference
    mean_offset = float(current_q @ offsets)
    mean_z = float(reference + mean_offset)
    centered = offsets - mean_offset
    with np.errstate(over="ignore"):
        spread = float(current_q @ (centered ** 2))
    if not (np.isfinite(mean_z) and np.isfinite(spread)):
        raise ValueError(
            f"Score moments are not representable in floating point for z_vec={z_vec!r}."
        )
    var_z = max(0.0, spread)

    tau_levels = np.linspace(
        1 / (2 * n_quantiles), 1 - 1 / (2 * n_quantiles), n_quantiles
    )
    quantile_vals = weighted_quantiles(z_vec, current_q, tau_levels)

    return DistributionalReturn(
        mean=mean_z,
        variance=var_z,
        quantiles=quantile_vals,
        quantile_levels=tau_levels,
    )


def push_forward_return(
    belief: CaseDiagramBelief,
    transition_matrix: np.ndarray,
    reward_vector: np.ndarray,
    gamma: float = 0.99,
    n_quantiles: int = 51,
) -> DistributionalReturn:
    """Return the finite law of dimensionless scores R + gamma * (T.T @ q).

Inputs: normalized role belief, nonnegative row-stochastic square T, finite
role score R, gamma in [0,1], and integer n_quantiles >= 2. Mass q_i is
placed at score z_i. This push-forward is a heuristic score distribution,
not a distributional Bellman backup or a value function.
"""
    q = belief.probabilities
    n = len(q)
    T = stochastic_matrix(transition_matrix, n)
    R = finite_vector(reward_vector, "Reward vector", n)
    positive_integer(n_quantiles, "n_quantiles", 2)

    if T.shape != (n, n):
        raise ValueError(f"Transition matrix shape {T.shape} != ({n}, {n})")
    if len(R) != n:
        raise ValueError(f"Reward vector length {len(R)} != {n}")
    if not np.allclose(T.sum(axis=1), 1.0, atol=1e-8):
        raise ValueError("Transition matrix rows must sum to 1.0")
    if not 0.0 <= gamma <= 1.0:
        raise ValueError(f"gamma must be in [0,1], got {gamma}")
    if n_quantiles < 2:
        raise ValueError(f"n_quantiles must be >= 2, got {n_quantiles}")

    result = _single_bellman_step(q, T, R, gamma, n_quantiles)

    logger.debug(
        "push_forward_return: mean=%.4f, std=%.4f, Z_range=[%.3f,%.3f]",
        result.mean, np.sqrt(result.variance),
        result.quantiles.min(), result.quantiles.max(),
    )
    return result


def distributional_bellman_operator(
    belief: CaseDiagramBelief,
    transition_matrix: np.ndarray,
    reward_vector: np.ndarray,
    gamma: float = 0.99,
    n_steps: int = 10,
    n_quantiles: int = 51,
    convergence_tol: Optional[float] = None,
) -> list[DistributionalReturn]:
    """Multi-step belief push-forward with discounted immediate reward.

    At each step this returns the distribution of ``R + gamma * (T^T q_k)``,
    where ``q_k`` is the belief propagated forward ``k`` times through the
    transition matrix. It is a *forward* recursion over beliefs, not a value
    backup.

    It therefore does NOT converge to the Bellman fixed point ``Z* = T Z*``.
    For ``T = [[.5,.5],[.5,.5]]``, ``R = [1,0]``, ``gamma = 0.9`` this returns
    mean 0.95 at every step, while the true value function
    ``(I - gamma*T)^-1 R = [5.5, 4.5]`` gives a belief-weighted value of 5.0.
    Obtaining the fixed point would require the backup
    ``z <- R + gamma * (T @ z)`` seeded at ``z = R``; that is a different
    algorithm and would change every published §7c result, so it is not done
    here. Read the output as a discounted one-step return under an evolving
    belief, and do not cite it as a value function.

    Args:
        belief: Current belief distribution over case roles.
        transition_matrix: Row-stochastic T[i,j], shape (n,n).
        reward_vector: Reward for each role, shape (n,).
        gamma: Discount factor ∈ [0,1].
        n_steps: Number of score-and-belief updates.
        n_quantiles: Quantiles to track.
        convergence_tol: If not None, terminate early when the absolute
            change in mean between successive steps is below this threshold.
            Default None preserves legacy behaviour (always run n_steps).

    Returns:
        List of DistributionalReturn, one per score-and-belief update.

    Raises:
        ValueError: On invalid inputs.
    """
    q = belief.probabilities
    n = len(q)
    T = stochastic_matrix(transition_matrix, n)
    R = finite_vector(reward_vector, "Reward vector", n)
    positive_integer(n_quantiles, "n_quantiles", 2)

    if T.shape != (n, n):
        raise ValueError(f"Transition matrix shape {T.shape} != ({n}, {n})")
    if len(R) != n:
        raise ValueError(f"Reward vector length {len(R)} != {n}")
    if not np.allclose(T.sum(axis=1), 1.0, atol=1e-8):
        raise ValueError("Transition matrix rows must sum to 1.0")
    if not 0.0 <= gamma <= 1.0:
        raise ValueError(f"gamma must be in [0,1], got {gamma}")
    if n_steps < 1:
        raise ValueError(f"n_steps must be >= 1, got {n_steps}")

    positive_integer(n_steps, "n_steps")
    if convergence_tol is not None and (not np.isfinite(convergence_tol) or convergence_tol <= 0):
        raise ValueError("convergence_tol must be finite and positive")
    results: list[DistributionalReturn] = []
    current_q = q.copy()
    prev_mean: Optional[float] = None

    for step in range(n_steps):
        result = _single_bellman_step(current_q, T, R, gamma, n_quantiles)
        results.append(result)

        logger.debug(
            "Score step %d/%d: mean=%.4f, std=%.4f",
            step + 1, n_steps, result.mean, np.sqrt(result.variance),
        )

        # Convergence check (only when tolerance is explicitly provided)
        if convergence_tol is not None and prev_mean is not None:
            delta = abs(result.mean - prev_mean)
            if delta < convergence_tol:
                logger.info(
                    "Score iteration converged at step %d/%d "
                    "(|delta_mean|=%.2e < tol=%.2e)",
                    step + 1, n_steps, delta, convergence_tol,
                )
                break
        prev_mean = result.mean

        # Propagate belief through transition for next step
        current_q = T.T @ current_q
        total = current_q.sum()
        if total > 0:
            current_q = current_q / total

    return results


def categorical_return_distribution(
    return_dist: DistributionalReturn,
    v_min: float,
    v_max: float,
    n_atoms: int = 51,
) -> tuple[np.ndarray, np.ndarray]:
    """Project a DistributionalReturn onto a C51-style categorical support.

    Projects the quantile-parameterised return distribution Z onto a fixed
    set of n_atoms equally spaced support values in [v_min, v_max] using
    the distributional projection operator Φ (Bellemare et al. 2017).

    Args:
        return_dist: Quantile-parameterised DistributionalReturn.
        v_min: Minimum support value.
        v_max: Maximum support value.
        n_atoms: Number of atoms in the categorical support.

    Returns:
        Tuple (atoms, probs) where atoms are support values and probs
        are the projected probability masses (sums to 1).

    Raises:
        ValueError: If v_min >= v_max or n_atoms < 2.
    """
    quantiles, _ = quantile_grid(return_dist.quantiles, return_dist.quantile_levels)
    positive_integer(n_atoms, "n_atoms", 2)
    if not np.isfinite(v_min) or not np.isfinite(v_max) or v_min >= v_max:
        raise ValueError(f"v_min ({v_min}) must be < v_max ({v_max})")
    if n_atoms < 2:
        raise ValueError(f"n_atoms must be >= 2, got {n_atoms}")

    atoms = np.linspace(v_min, v_max, n_atoms)
    delta_z = (v_max - v_min) / (n_atoms - 1)
    probs = np.zeros(n_atoms)

    # Distributional projection: each quantile contributes linearly to two atoms
    for tau_val in quantiles:
        clipped = np.clip(tau_val, v_min, v_max)
        lo_idx = int(np.floor((clipped - v_min) / delta_z))
        hi_idx = min(lo_idx + 1, n_atoms - 1)
        lo_idx = max(lo_idx, 0)
        if lo_idx == hi_idx:
            probs[lo_idx] += 1.0
        else:
            # Linear interpolation weight
            hi_weight = (clipped - atoms[lo_idx]) / delta_z
            lo_weight = 1.0 - hi_weight
            probs[lo_idx] += lo_weight
            probs[hi_idx] += hi_weight

    n_q = len(return_dist.quantiles)
    if n_q > 0:
        probs /= n_q

    logger.debug(
        "Categorical projection: %d atoms, mode=%.3f, prob_mass_outside=%.4f",
        n_atoms, atoms[np.argmax(probs)],
        1.0 - probs.sum(),
    )
    return atoms, probs
