"""Statistics helper tests for src.experiments (exact values, no mocks).

Pins the intended confidence-interval contract: the two-sided normal quantile
is derived from ``statistics.NormalDist`` at the declared level, Wilson score
intervals accept only integer Bernoulli counts, and mean intervals require at
least two replicates because a single replicate has undefined sample variance.
"""
from __future__ import annotations

import math
from statistics import NormalDist

import numpy as np
import pytest

from src.experiments import (
    Z95,
    ci_block,
    mean_ci,
    normal_z,
    paired_mean_ci,
    wilson_score_interval,
)


def test_normal_z_matches_normaldist_and_z95():
    assert normal_z(0.95) == Z95
    assert normal_z(0.95) == NormalDist().inv_cdf(0.975)
    assert normal_z(0.90) < normal_z(0.95) < normal_z(0.99)
    with pytest.raises(ValueError):
        normal_z(0.0)
    with pytest.raises(ValueError):
        normal_z(1.0)
    with pytest.raises(ValueError):
        normal_z(1.5)


def test_wilson_interval_known_values():
    lo, hi = wilson_score_interval(3, 10)
    z = normal_z(0.95)
    p = 0.3
    denom = 1 + z * z / 10
    centre = (p + z * z / 20) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / 10 + z * z / 400)
    assert lo == pytest.approx(max(0.0, centre - half))
    assert hi == pytest.approx(min(1.0, centre + half))
    assert 0.0 <= lo <= 0.3 <= hi <= 1.0


def test_wilson_extremes_and_numpy_integers():
    # k = 0: Wilson lower bound collapses to 0, upper bound is the closed
    # form z^2 / (n + z^2), NOT the trivial [0, 1] interval.
    z = normal_z(0.95)
    lo, hi = wilson_score_interval(0, 10)
    assert lo == 0.0
    assert hi == pytest.approx(z * z / (10 + z * z))
    lo_all, hi_all = wilson_score_interval(10, 10)
    assert lo_all == pytest.approx(1.0 - z * z / (10 + z * z))
    assert hi_all == 1.0
    lo_np, hi_np = wilson_score_interval(np.int64(3), np.int64(10))
    assert lo_np == pytest.approx(wilson_score_interval(3, 10)[0])
    assert hi_np == pytest.approx(wilson_score_interval(3, 10)[1])


@pytest.mark.parametrize("successes, trials", [
    (0.5, 1.5),   # fractional counts reproduced by independent control
    (True, 5),    # booleans are not counts
    (3, True),
    (2.0, 10),    # whole-valued floats are still not integer counts
    (np.float64(4), 10),
])
def test_wilson_rejects_non_integer_counts(successes, trials):
    with pytest.raises(TypeError):
        wilson_score_interval(successes, trials)


def test_wilson_rejects_out_of_range_and_bad_z():
    with pytest.raises(ValueError):
        wilson_score_interval(11, 10)
    with pytest.raises(ValueError):
        wilson_score_interval(-1, 10)
    with pytest.raises(ValueError):
        wilson_score_interval(3, 0)
    with pytest.raises(ValueError):
        wilson_score_interval(3, 10, z=0.0)
    with pytest.raises(ValueError):
        wilson_score_interval(3, 10, z=float("nan"))


def test_mean_ci_matches_manual_formula():
    values = [1.0, 2.0, 3.0, 4.0]
    z = normal_z(0.95)
    arr = np.asarray(values)
    sd = arr.std(ddof=1)
    half = z * sd / math.sqrt(arr.size)
    mean, lo, hi = mean_ci(values)
    assert mean == pytest.approx(2.5)
    assert lo == pytest.approx(2.5 - half)
    assert hi == pytest.approx(2.5 + half)


def test_mean_ci_requires_two_replicates():
    # A single replicate has undefined sample variance; presenting it with a
    # zero-width interval would report no-variance data as exact precision.
    with pytest.raises(ValueError, match="at least two"):
        mean_ci([5.0])
    with pytest.raises(ValueError):
        mean_ci([])
    with pytest.raises(ValueError):
        mean_ci([1.0, float("nan")])
    with pytest.raises(ValueError):
        mean_ci([1.0, float("inf")])


def test_paired_mean_ci_equals_mean_ci():
    diffs = [0.5, -0.25, 1.0, 0.0]
    assert paired_mean_ci(diffs) == mean_ci(diffs)


def test_ci_block_shape_and_validation():
    block = ci_block(0.5, 0.4, 0.6, 0.95, "mean +/- SE", "replicate")
    assert block == {
        "mean": 0.5, "low": 0.4, "high": 0.6,
        "confidence_level": 0.95,
        "estimator": "mean +/- SE", "sample_unit": "replicate",
    }
    with pytest.raises(ValueError):
        ci_block(float("nan"), 0.0, 1.0, 0.95, "e", "r")
    with pytest.raises(ValueError):
        ci_block(0.5, 0.4, 0.6, 1.5, "e", "r")
    with pytest.raises(ValueError):
        ci_block(0.5, 0.4, 0.6, 0.95, "", "r")
