"""DAIF Core: Push-Forward & Distributional Bellman Operator.

Implements the foundational distributional RL machinery of DAIF:

- push_forward_return(): Distributional Bellman Z = R + γ T^⊤ q
- distributional_bellman_operator(): Multi-step Bellman iteration Tⁿ Z₀
- categorical_return_distribution(): C51-style atom projection

References:
    Akgül et al. (2026) — Distributional Active Inference
    Bellemare et al. (2017) — C51 distributional RL
    Dabney et al. (2018) — Quantile Regression DQN
"""
from __future__ import annotations

import logging
from typing import Optional

import numpy as np

from ..cognitive.belief import CaseDiagramBelief
from .types import DistributionalReturn

logger = logging.getLogger(__name__)


def _single_bellman_step(
    current_q: np.ndarray,
    transition_matrix: np.ndarray,
    reward_vector: np.ndarray,
    gamma: float,
    n_quantiles: int,
) -> DistributionalReturn:
    """Compute one step of the distributional Bellman operator.

    Shared computation extracted from push_forward_return() and the inner
    loop of distributional_bellman_operator(). Given belief weights q,
    transition matrix T, and reward vector R, computes a mean-field
    approximation of the distributional Bellman equation (Eq. 7c-bellman):

        z_vec = R + γ · T^⊤ q

    This is a mean-field approximation: instead of maintaining per-state
    return distributions Z(s) and pushing each forward independently,
    we compute a single belief-weighted return vector. The push-forward
    T^⊤ q propagates the belief through the transition dynamics, and
    the reward R provides immediate returns. The resulting z_vec gives
    the expected return contribution for each role under the current
    belief, from which we extract quantile statistics.

    Args:
        current_q: Belief probability vector, shape (n,).
        transition_matrix: Row-stochastic T[i,j], shape (n,n).
        reward_vector: Reward per role, shape (n,).
        gamma: Discount factor in [0,1].
        n_quantiles: Number of quantile levels.

    Returns:
        DistributionalReturn with mean, variance, quantiles, quantile_levels.

    Note on degenerate beliefs:
        If ``current_q`` assigns exactly zero probability to some role i,
        the induced cumulative distribution has a flat plateau at the
        z-value of role i, and quantile levels τ falling inside that
        plateau are mathematically indeterminate. The implementation
        uses ``np.interp`` which returns the left endpoint of the flat
        region — any value in the plateau would be an equally valid
        quantile, so this is an arbitrary-but-consistent choice. The
        quantile vector is still non-decreasing by construction.
    """
    T = transition_matrix
    R = reward_vector

    # Mean-field Bellman: per-role return under belief-weighted dynamics
    z_vec = R + gamma * T.T @ current_q

    if not np.all(np.isfinite(z_vec)):
        raise ValueError(
            f"Non-finite values in z_vec after Bellman step — check reward_vector "
            f"and transition_matrix for NaN/inf. z_vec={z_vec!r}"
        )

    mean_z = float(current_q @ z_vec)

    z_second_moment = float(current_q @ (z_vec ** 2))
    var_z = max(0.0, z_second_moment - mean_z ** 2)

    tau_levels = np.linspace(
        1 / (2 * n_quantiles), 1 - 1 / (2 * n_quantiles), n_quantiles
    )
    role_sorted_idx = np.argsort(z_vec)
    cumulative = np.cumsum(current_q[role_sorted_idx])
    cumulative = np.maximum.accumulate(cumulative)
    if cumulative[-1] <= 0:
        raise ValueError(
            "Degenerate quantile distribution: cumulative probability sums to zero. "
            "Ensure current_q is a valid probability distribution (non-negative, sums > 0)."
        )
    cumulative = cumulative / cumulative[-1]
    quantile_vals = np.interp(tau_levels, cumulative, z_vec[role_sorted_idx])

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
    """Compute the push-forward return distribution via distributional Bellman.

    Implements Eq. 7-1 from the manuscript (push-forward return integral).
    Given current belief q over case roles and transition matrix T[i,j] = P(s'=j|s=i),
    computes the one-step push-forward distribution:

        Z(s) = R(s) + γ Σ_{s'} T(s,s') Z(s')

    For the fixed-point single-step approximation:
        mean(Z) = R + γ T^⊤ q

    The full quantile representation is constructed by sampling from
    the resulting distribution.

    Args:
        belief: Current belief distribution over case roles.
        transition_matrix: Row-stochastic matrix T[i,j], shape (n,n).
        reward_vector: Reward for each case role, shape (n,).
        gamma: Discount factor ∈ [0,1].
        n_quantiles: Number of quantiles to compute for Z.

    Returns:
        DistributionalReturn with mean, variance, quantiles, quantile_levels.

    Raises:
        ValueError: On dimension mismatch or invalid parameters.
    """
    T = np.asarray(transition_matrix, dtype=np.float64)
    R = np.asarray(reward_vector, dtype=np.float64)
    q = belief.probabilities
    n = len(q)

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
    """Multi-step distributional Bellman iteration: Z_k = T Z_{k-1}.

    Iterates the distributional Bellman operator n_steps times, starting
    from the single-step push-forward. This approximates the fixed-point
    return distribution Z* = T Z* via contraction mapping.

    Args:
        belief: Current belief distribution over case roles.
        transition_matrix: Row-stochastic T[i,j], shape (n,n).
        reward_vector: Reward for each role, shape (n,).
        gamma: Discount factor ∈ [0,1].
        n_steps: Number of Bellman applications.
        n_quantiles: Quantiles to track.
        convergence_tol: If not None, terminate early when the absolute
            change in mean between successive steps is below this threshold.
            Default None preserves legacy behaviour (always run n_steps).

    Returns:
        List of DistributionalReturn, one per Bellman step.

    Raises:
        ValueError: On invalid inputs.
    """
    T = np.asarray(transition_matrix, dtype=np.float64)
    R = np.asarray(reward_vector, dtype=np.float64)
    q = belief.probabilities
    n = len(q)

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

    results: list[DistributionalReturn] = []
    current_q = q.copy()
    prev_mean: Optional[float] = None

    for step in range(n_steps):
        result = _single_bellman_step(current_q, T, R, gamma, n_quantiles)
        results.append(result)

        logger.debug(
            "Bellman step %d/%d: mean=%.4f, std=%.4f",
            step + 1, n_steps, result.mean, np.sqrt(result.variance),
        )

        # Convergence check (only when tolerance is explicitly provided)
        if convergence_tol is not None and prev_mean is not None:
            delta = abs(result.mean - prev_mean)
            if delta < convergence_tol:
                logger.info(
                    "Bellman operator converged at step %d/%d "
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
    if v_min >= v_max:
        raise ValueError(f"v_min ({v_min}) must be < v_max ({v_max})")
    if n_atoms < 2:
        raise ValueError(f"n_atoms must be >= 2, got {n_atoms}")

    atoms = np.linspace(v_min, v_max, n_atoms)
    delta_z = (v_max - v_min) / (n_atoms - 1)
    probs = np.zeros(n_atoms)

    # Distributional projection: each quantile contributes linearly to two atoms
    for tau_val in return_dist.quantiles:
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
