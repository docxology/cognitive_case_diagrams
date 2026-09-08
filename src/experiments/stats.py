"""Confidence-interval helpers used by the experiment reports.

Two well-defined interval families are provided:

- Wilson score intervals for binomial proportions (coverage rates, mode-match
  frequencies). The sample unit is one Bernoulli trial.
- Normal-approximation intervals for replicate-level means,
  ``mean +/- z * sd / sqrt(n)``. The sample unit is one replicate; the
  interval is exact only under the stated normal approximation and every
  reported block names its estimator and sample unit.

The two-sided normal quantile is derived from the configured confidence level
via ``statistics.NormalDist().inv_cdf((1 + level) / 2)`` (stdlib), so a
configurable ``confidence_level`` always drives the computation. No p-values
are computed anywhere in this package.
"""
from __future__ import annotations

import math
from statistics import NormalDist

import numpy as np

__all__ = [
    "Z95",
    "wilson_score_interval",
    "normal_z",
    "mean_ci",
    "paired_mean_ci",
    "ci_block",
]

# Two-sided 95% normal quantile, derived from the same NormalDist used by
# normal_z so no second source of truth exists.
Z95 = float(NormalDist().inv_cdf(0.975))


def normal_z(confidence_level: float) -> float:
    """Two-sided normal quantile for a confidence level in (0, 1).

    Raises:
        ValueError: If the level is not strictly inside (0, 1).
    """
    if not math.isfinite(confidence_level) or not 0.0 < confidence_level < 1.0:
        raise ValueError(f"confidence_level must be strictly inside (0, 1), got {confidence_level}")
    return float(NormalDist().inv_cdf((1.0 + confidence_level) / 2.0))


def wilson_score_interval(
    successes: int | np.integer,
    trials: int | np.integer,
    z: float = Z95,
) -> tuple[float, float]:
    """Return the Wilson score interval for a binomial proportion.

    Args:
        successes: Integer number of successes (0 <= successes <= trials).
        trials: Integer number of Bernoulli trials (>= 1).
        z: Two-sided normal quantile (see :func:`normal_z`).

    Returns:
        ``(lo, hi)`` with 0 <= lo <= hi <= 1.

    Raises:
        TypeError: If counts are not integers (bools and fractional values
            are rejected before any conversion).
        ValueError: On out-of-range counts or non-positive z.
    """
    for name, value in (("successes", successes), ("trials", trials)):
        if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
            raise TypeError(
                f"{name} must be an integer count, got {value!r} of type "
                f"{type(value).__name__}"
            )
    n = int(trials)
    k = int(successes)
    if n < 1:
        raise ValueError(f"trials must be >= 1, got {trials}")
    if k < 0 or k > n:
        raise ValueError(f"successes must be in [0, trials], got {successes}/{trials}")
    if not math.isfinite(z) or z <= 0:
        raise ValueError(f"z must be finite and positive, got {z}")
    # The binomial boundary roots are exact; subtracting centre and half
    # can leave a platform-dependent rounding residual at zero or one.
    if k == 0:
        return (0.0, z * z / (n + z * z))
    if k == n:
        return (n / (n + z * z), 1.0)
    p_hat = k / n
    denom = 1.0 + z * z / n
    centre = (p_hat + z * z / (2.0 * n)) / denom
    half = (z / denom) * math.sqrt(p_hat * (1.0 - p_hat) / n + z * z / (4.0 * n * n))
    return (max(0.0, centre - half), min(1.0, centre + half))
def mean_ci(
    values: np.ndarray | list[float],
    z: float = Z95,
) -> tuple[float, float, float]:
    """Return ``(mean, lo, hi)`` for a replicate-level sample mean.

    The interval is ``mean +/- z * sd / sqrt(n)`` with ``sd`` the sample
    standard deviation (ddof=1). At least two values are required: a single
    replicate has undefined sample variance, and presenting it with a
    zero-width interval would report no-variance data as exact precision.

    Raises:
        ValueError: If fewer than two values are supplied or any entry is
            non-finite.
    """
    arr = np.asarray(values, dtype=np.float64)
    if arr.ndim != 1 or arr.size < 2:
        raise ValueError(
            "mean_ci requires at least two replicates (sample variance is "
            f"undefined for n < 2), got {arr.size if arr.ndim == 1 else 'non-1d'}"
        )
    if not np.all(np.isfinite(arr)):
        raise ValueError("values must be finite")
    if not math.isfinite(z) or z <= 0:
        raise ValueError(f"z must be finite and positive, got {z}")
    mean = float(arr.mean())
    sd = float(arr.std(ddof=1))
    half = z * sd / math.sqrt(arr.size)
    return (mean, mean - half, mean + half)

def paired_mean_ci(
    differences: np.ndarray | list[float],
    z: float = Z95,
) -> tuple[float, float, float]:
    """Return ``(mean_diff, lo, hi)`` for paired per-replicate differences.

    The design is paired because both arms consume the same per-replicate
    draws (common random numbers); the interval describes the mean of
    within-replicate differences, not the difference of marginal means.
    """
    return mean_ci(differences, z)


def ci_block(
    estimate: float,
    low: float,
    high: float,
    confidence_level: float,
    estimator: str,
    sample_unit: str,
) -> dict[str, float | str]:
    """Structured interval record consumed by plots, injection, and MCP.

    Shape: ``{"mean", "low", "high", "confidence_level", "estimator",
    "sample_unit"}`` with finite numbers and non-empty description strings.
    """
    for name, value in (("estimate", estimate), ("low", low), ("high", high)):
        value_f = float(value)
        if not math.isfinite(value_f):
            raise ValueError(f"{name} must be finite, got {value!r}")
    if not 0.0 < float(confidence_level) < 1.0:
        raise ValueError(f"confidence_level must be in (0, 1), got {confidence_level}")
    if not float(low) <= float(estimate) <= float(high):
        raise ValueError("interval bounds must satisfy low <= estimate <= high")
    if not isinstance(estimator, str) or not estimator.strip() or not isinstance(sample_unit, str) or not sample_unit.strip():
        raise ValueError("estimator and sample_unit must be non-empty strings")
    return {
        "mean": float(estimate),
        "low": float(low),
        "high": float(high),
        "confidence_level": float(confidence_level),
        "estimator": estimator,
        "sample_unit": sample_unit,
    }
