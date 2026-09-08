"""Validated numerical inputs and finite-distribution quantiles.

These helpers reject invalid data before NumPy broadcasting or normalization
can turn it into plausible-looking scientific output.
"""

from __future__ import annotations

import numpy as np


def _as_float_array(values, name: str) -> np.ndarray:
    """Cast to float64, rejecting booleans and complex input outright."""
    raw = np.asarray(values)
    if raw.dtype == np.bool_:
        raise ValueError(f"{name} must contain numeric values, not booleans")
    if np.issubdtype(raw.dtype, np.complexfloating):
        raise ValueError(f"{name} must be real-valued; complex input is rejected")
    return raw.astype(np.float64)


def finite_vector(values, name: str, size: int | None = None) -> np.ndarray:
    """Return a non-empty finite one-dimensional float array."""
    array = _as_float_array(values, name)
    if array.ndim != 1 or array.size == 0:
        raise ValueError(f"{name} must be a non-empty one-dimensional vector")
    if size is not None and array.shape != (size,):
        raise ValueError(f"{name} shape {array.shape} != ({size},)")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain finite values")
    return array


def probability_vector(values, name: str = "probabilities") -> np.ndarray:
    """Validate a normalized, nonnegative categorical distribution."""
    array = finite_vector(values, name)
    if np.any(array < 0):
        raise ValueError(f"{name} must be non-negative")
    if not np.isclose(array.sum(), 1., atol=1e-8, rtol=0.):
        raise ValueError(f"{name} must sum to 1.0, got {array.sum()}")
    return array


def stochastic_matrix(values, n: int) -> np.ndarray:
    """Validate row-stochastic transition probabilities."""
    n = positive_integer(n, "matrix dimension")
    array = _as_float_array(values, "Transition matrix")
    if array.shape != (n, n):
        raise ValueError(f"Transition matrix shape {array.shape} != ({n}, {n})")
    if not np.all(np.isfinite(array)) or np.any(array < 0):
        raise ValueError("Transition matrix must be finite and non-negative")
    if not np.allclose(array.sum(axis=1), 1., atol=1e-8, rtol=0.):
        raise ValueError("Transition matrix rows must sum to 1.0")
    return array


def positive_integer(value: int, name: str, minimum: int = 1) -> int:
    """Validate integer counts without accepting booleans or floats."""
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise ValueError(f"{name} must be an integer >= {minimum}")
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}, got {value}")
    return int(value)


def quantile_grid(values, levels) -> tuple[np.ndarray, np.ndarray]:
    """Validate increasing levels in (0,1) and nondecreasing quantile values."""
    q = finite_vector(values, "quantiles")
    tau = finite_vector(levels, "quantile_levels", q.size)
    if np.any((tau <= 0) | (tau >= 1)) or np.any(np.diff(tau) <= 0):
        raise ValueError("quantile_levels must be strictly increasing in (0,1)")
    if np.any(np.diff(q) < 0):
        raise ValueError("quantiles must be nondecreasing")
    return q, tau


def weighted_quantiles(values, probabilities, levels) -> np.ndarray:
    """Generalized inverse CDF of a finite distribution, without interpolation.

    Zero-mass support points are removed; the returned quantile is the smallest
    positive-mass value whose cumulative probability is at least the level.
    """
    x = finite_vector(values, "support")
    p = probability_vector(probabilities)
    tau = finite_vector(levels, "levels")
    if x.shape != p.shape or np.any((tau <= 0) | (tau >= 1)):
        raise ValueError("Support/probability shapes must match and levels must be in (0,1)")
    order = np.argsort(x[p > 0], kind="stable")
    support = x[p > 0][order]
    cumulative = np.cumsum(p[p > 0][order])
    cumulative[-1] = 1.
    return support[np.searchsorted(cumulative, tau, side="left")]
