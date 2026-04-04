"""Tests for src/daif/metrics.py — Convergence Diagnostics & Distance Measures.

All tests use real numerical computations. Zero mocks.
"""

import numpy as np
import pytest

from src.daif.metrics import (
    convergence_diagnostics,
    distributional_kl,
    quantile_coverage,
    return_distribution_entropy,
)
from src.daif.types import DistributionalReturn


def _make_dist(offset=0.0, spread=1.0, n=31):
    taus = np.linspace(0.05, 0.95, n)
    q = np.sort(np.random.default_rng(7 + int(offset * 10)).normal(offset, spread, n))
    return DistributionalReturn(mean=float(np.mean(q)), variance=float(np.var(q)),
                                quantiles=q, quantile_levels=taus)


# --- convergence_diagnostics ---

class TestConvergenceDiagnostics:

    def test_monotone_decreasing_trajectory(self):
        fe = [5.0, 4.0, 3.2, 2.8, 2.75]
        diag = convergence_diagnostics(fe)
        assert diag["monotone"] is True
        assert diag["total_reduction"] == pytest.approx(2.25, abs=1e-8)

    def test_non_monotone_trajectory(self):
        fe = [5.0, 4.5, 4.7, 4.2]
        diag = convergence_diagnostics(fe)
        assert diag["monotone"] is False

    def test_n_iterations_correct(self):
        fe = [3.0, 2.5, 2.0]
        diag = convergence_diagnostics(fe)
        assert diag["n_iterations"] == 3

    def test_total_reduction_sign(self):
        fe = [10.0, 8.0, 6.0, 5.0]
        diag = convergence_diagnostics(fe)
        assert diag["total_reduction"] > 0.0

    def test_relative_reduction_pct(self):
        fe = [10.0, 8.0, 5.0]
        diag = convergence_diagnostics(fe)
        assert diag["relative_reduction_pct"] == pytest.approx(50.0, abs=0.01)

    def test_mean_step_size_positive(self):
        fe = [4.0, 3.0, 2.5, 2.1]
        diag = convergence_diagnostics(fe)
        assert diag["mean_step_size"] > 0.0

    def test_all_required_keys_present(self):
        fe = [3.0, 2.0, 1.5]
        diag = convergence_diagnostics(fe)
        for key in ("monotone", "total_reduction", "relative_reduction_pct",
                    "n_iterations", "converged", "fe_range", "mean_step_size", "final_delta"):
            assert key in diag

    def test_too_short_trajectory_raises(self):
        with pytest.raises(ValueError, match="min_iterations"):
            convergence_diagnostics([5.0, 4.0], min_iterations=3)


# --- distributional_kl ---

class TestDistributionalKL:

    def test_identical_distributions_near_zero(self):
        da = _make_dist(offset=0.0)
        kl = distributional_kl(da, da, n_bins=50)
        assert kl < 0.1  # epsilon-smoothed histogram: never exactly 0

    def test_different_means_positive_kl(self):
        da = _make_dist(offset=0.0)
        db = _make_dist(offset=3.0)
        kl = distributional_kl(da, db, n_bins=50)
        assert kl > 0.0

    def test_kl_non_negative(self):
        da = _make_dist(offset=0.0)
        db = _make_dist(offset=1.0, spread=2.0)
        assert distributional_kl(da, db) >= 0.0

    def test_invalid_n_bins_raises(self):
        da = _make_dist()
        with pytest.raises(ValueError, match="n_bins"):
            distributional_kl(da, da, n_bins=1)


# --- quantile_coverage ---

class TestQuantileCoverage:

    def test_returns_all_keys(self):
        taus = np.array([0.25, 0.50, 0.75])
        qvals = np.array([0.0, 1.0, 2.0])
        obs = np.array([0.5, 0.5, 1.5, 1.5])
        result = quantile_coverage(qvals, taus, obs)
        for key in ("empirical_coverage", "calibration_error", "max_calibration_error", "coverage_table"):
            assert key in result

    def test_empirical_coverage_in_01(self):
        taus = np.linspace(0.1, 0.9, 9)
        qvals = np.quantile(np.arange(100), taus)
        obs = np.arange(100, dtype=float)
        result = quantile_coverage(qvals, taus, obs)
        assert np.all((result["empirical_coverage"] >= 0) & (result["empirical_coverage"] <= 1))

    def test_calibration_error_non_negative(self):
        taus = np.array([0.25, 0.75])
        qvals = np.array([0.0, 1.0])
        obs = np.array([0.5, 0.5, 0.5])
        result = quantile_coverage(qvals, taus, obs)
        assert result["calibration_error"] >= 0.0

    def test_well_calibrated_model_low_error(self):
        """Quantiles matching data quantiles should have near-perfect calibration."""
        rng = np.random.default_rng(42)
        obs = rng.standard_normal(1000)
        taus = np.linspace(0.05, 0.95, 19)
        qvals = np.quantile(obs, taus)
        result = quantile_coverage(qvals, taus, obs)
        assert result["calibration_error"] < 0.05  # ideal calibration

    def test_mismatched_quantile_levels_raises(self):
        with pytest.raises(ValueError, match="length mismatch"):
            quantile_coverage(np.array([0.5]), np.array([0.25, 0.75]), np.array([0.5]))

    def test_empty_observations_raises(self):
        with pytest.raises(ValueError, match="non-empty"):
            quantile_coverage(np.array([0.5]), np.array([0.5]), np.array([]))

    def test_invalid_levels_raises(self):
        with pytest.raises(ValueError, match="must be in"):
            quantile_coverage(np.array([0.5]), np.array([1.5]), np.array([0.5]))


# --- return_distribution_entropy ---

class TestReturnDistributionEntropy:

    def test_point_mass_zero_entropy(self):
        taus = np.linspace(0.05, 0.95, 21)
        dist = DistributionalReturn(mean=1.0, variance=0.0, quantiles=np.ones(21), quantile_levels=taus)
        h = return_distribution_entropy(dist, n_bins=20)
        assert h < 1e-6  # epsilon-smoothed histogram: effectively zero

    def test_spread_distribution_positive_entropy(self):
        dist = _make_dist(spread=2.0)
        h = return_distribution_entropy(dist, n_bins=30)
        assert h > 0.0

    def test_wider_spread_higher_entropy(self):
        taus = np.linspace(0.05, 0.95, 101)
        # Concentrated: 90% of quantiles at 1.0, 10% at 2.0 → low entropy histogram
        narrow_q = np.concatenate([np.ones(91), np.full(10, 2.0)])
        d_narrow = DistributionalReturn(mean=1.1, variance=0.09, quantiles=narrow_q, quantile_levels=taus)
        # Uniform spread over [−5, 5] → high entropy histogram
        wide_q = np.linspace(-5.0, 5.0, 101)
        d_wide = DistributionalReturn(mean=0.0, variance=8.0, quantiles=wide_q, quantile_levels=taus)
        h_narrow = return_distribution_entropy(d_narrow, n_bins=50)
        h_wide = return_distribution_entropy(d_wide, n_bins=50)
        assert h_wide > h_narrow

    def test_finite_output(self):
        dist = _make_dist()
        h = return_distribution_entropy(dist)
        assert np.isfinite(h)

    def test_invalid_n_bins_raises(self):
        dist = _make_dist()
        with pytest.raises(ValueError, match="n_bins"):
            return_distribution_entropy(dist, n_bins=1)
