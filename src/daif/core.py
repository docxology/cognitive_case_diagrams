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

import logging
from typing import Optional

import numpy as np

from ..cognitive.belief import CaseDiagramBelief
from .types import DistributionalReturn

logger = logging.getLogger(__name__)


def push_forward_return(
    belief: CaseDiagramBelief,
    transition_matrix: np.ndarray,
    reward_vector: np.ndarray,
    gamma: float = 0.99,
    n_quantiles: int = 51,
) -> DistributionalReturn:
    """Compute the push-forward return distribution via distributional Bellman.

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

    # Distributional Bellman mean: Z̄ = R + γ T^⊤ q
    z_mean_vec = R + gamma * T.T @ q
    mean_z = float(q @ z_mean_vec)

    # Variance: Var[Z] = Var_q[R] + γ² · q^⊤ diag(T^⊤ q) − (γ T^⊤ q)²
    r_centered = R - (q @ R)
    var_r = float(q @ (r_centered ** 2))
    z_second_moment = float(q @ (z_mean_vec ** 2))
    var_z = max(0.0, z_second_moment - mean_z ** 2)

    # Quantile representation: discretise via role-weighted mixture
    tau_levels = np.linspace(1 / (2 * n_quantiles), 1 - 1 / (2 * n_quantiles), n_quantiles)
    # Each role contributes its z_mean_vec value with weight q[i]
    # Quantiles of the mixture approximated by sorted role values weighted by q
    role_sorted_idx = np.argsort(z_mean_vec)
    cumulative = np.cumsum(q[role_sorted_idx])
    # Interpolate quantile values
    quantile_vals = np.interp(tau_levels, cumulative, z_mean_vec[role_sorted_idx])

    logger.debug(
        "push_forward_return: mean=%.4f, std=%.4f, Z_range=[%.3f,%.3f]",
        mean_z, np.sqrt(var_z), quantile_vals.min(), quantile_vals.max(),
    )
    return DistributionalReturn(
        mean=mean_z,
        variance=var_z,
        quantiles=quantile_vals,
        quantile_levels=tau_levels,
    )


def distributional_bellman_operator(
    belief: CaseDiagramBelief,
    transition_matrix: np.ndarray,
    reward_vector: np.ndarray,
    gamma: float = 0.99,
    n_steps: int = 10,
    n_quantiles: int = 51,
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

    for step in range(n_steps):
        # Single-step Bellman application
        z_vec = R + gamma * T.T @ current_q
        mean_z = float(current_q @ z_vec)

        z2 = float(current_q @ (z_vec ** 2))
        var_z = max(0.0, z2 - mean_z ** 2)

        tau_levels = np.linspace(1 / (2 * n_quantiles), 1 - 1 / (2 * n_quantiles), n_quantiles)
        role_sorted_idx = np.argsort(z_vec)
        cumulative = np.cumsum(current_q[role_sorted_idx])
        quantile_vals = np.interp(tau_levels, cumulative, z_vec[role_sorted_idx])

        results.append(DistributionalReturn(
            mean=mean_z,
            variance=var_z,
            quantiles=quantile_vals,
            quantile_levels=tau_levels,
        ))

        # Propagate belief through transition for next step
        current_q = T.T @ current_q
        total = current_q.sum()
        if total > 0:
            current_q = current_q / total

        logger.debug("Bellman step %d/%d: mean=%.4f, std=%.4f", step + 1, n_steps, mean_z, np.sqrt(var_z))

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
