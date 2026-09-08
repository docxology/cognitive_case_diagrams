"""P1-07 acceptance controls: quantile_atom_gap semantics + value identity."""
import numpy as np
import pytest

from src.daif.metrics import quantile_atom_gap, quantile_coverage

# Base counterexample (reproduced on 9382dde before the patch): perfectly
# calibrated two-atom law {0: 0.9, 1: 0.1} reports calibration_error 0.2105.
LEVELS = np.linspace(1 / 102, 101 / 102, 51)
Q_PRED = np.where(LEVELS <= 0.9, 0.0, 1.0)
OBS = np.array([0.0, 1.0, 0.0, 1.0])
BASE_CAL_ERR = 0.21049596309111876
BASE_MAX_ERR = 0.49019607843137253


class TestQuantileCoverageValueIdentity:
    def test_outputs_value_identical_to_base(self):
        rep = quantile_coverage(Q_PRED, LEVELS, OBS)
        assert rep["calibration_error"] == BASE_CAL_ERR
        assert rep["max_calibration_error"] == BASE_MAX_ERR

    def test_docstring_no_longer_claims_exact_discrete_calibration(self):
        import inspect
        from src.daif import metrics
        doc = inspect.getdoc(metrics.quantile_coverage)
        assert "coverage(τ) == τ for all τ" not in doc
        assert "atom" in doc


class TestQuantileAtomGap:
    def test_two_atom_law_gap_nonnegative_and_structured(self):
        out = quantile_atom_gap(Q_PRED, LEVELS)
        gap = out["atom_gap"]
        assert np.all(gap >= 0.0)
        # F(Q(tau)) for the zero-atom levels is the top of the flat region.
        zero_region = LEVELS <= 0.9
        # Grid-represented F(Q=0) = top level of the zero flat region (index 45).
        assert np.allclose(gap[zero_region], LEVELS[45] - LEVELS[zero_region])
        # Ones region: grid-represented F(Q=1) = the grid's top level (101/102).
        ones_region = ~zero_region
        assert np.allclose(gap[ones_region], LEVELS[50] - LEVELS[ones_region])

    def test_zero_gap_at_atom_boundaries(self):
        out = quantile_atom_gap(Q_PRED, LEVELS)
        # The zero flat region's top level (index 45 = 91/102) has zero gap;
        # the ones flat region's top level (index 50 = 101/102) has zero gap.
        assert out["atom_gap"][45] == 0.0
        assert out["atom_gap"][50] == 0.0

    def test_continuous_grid_zero_gap(self):
        taus = np.linspace(0.05, 0.95, 19)
        qvals = taus.copy()  # strictly increasing grid = atom-free representation
        out = quantile_atom_gap(qvals, taus)
        assert np.all(out["atom_gap"] == 0.0)
        assert out["max_atom_gap"] == 0.0

    def test_max_gap_is_the_zero_region_top_offset(self):
        out = quantile_atom_gap(Q_PRED, LEVELS)
        # Max gap = top of the zero flat region minus the lowest level = 90/102.
        assert out["max_atom_gap"] == float(LEVELS[45] - LEVELS[0])
        # Ones-region start gap: F(Q=1) = 101/102 (grid top), gap = 8/102.
        assert abs(out["atom_gap"][46] - 8 / 102) < 1e-12

    def test_invalid_levels_raise(self):
        with pytest.raises(ValueError, match="must be in"):
            quantile_atom_gap(np.array([0.5]), np.array([1.5]))

    def test_length_mismatch_raises(self):
        with pytest.raises(ValueError, match="length mismatch"):
            quantile_atom_gap(np.array([0.5, 1.0]), np.array([0.5]))

    def test_decreasing_quantiles_raise(self):
        with pytest.raises(ValueError, match="nondecreasing"):
            quantile_atom_gap(np.array([1.0, 0.0]), np.array([0.25, 0.75]))
