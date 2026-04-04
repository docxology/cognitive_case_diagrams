"""Tests for src/daif — Distributional Active Inference (DAIF).

This file preserves the original four-function DAIF test coverage
using the new canonical import paths from `src.daif`.

The six dedicated test files (test_daif_core.py, test_daif_quantile.py,
test_daif_inference.py, test_daif_prediction.py, test_daif_policy.py,
test_daif_metrics.py) provide comprehensive module-level coverage.
This file is kept for pipeline continuity and backward test discovery.
"""

import numpy as np
import pytest

from src.case_systems.case_category import CaseRole
from src.cognitive.belief import CaseDiagramBelief
from src.daif import (
    push_forward_return,
    quantile_td_update,
    distributional_case_assignment,
    distributional_prediction_error,
)
from src.daif.types import DAIFResult, DistributionalReturn, ERPProfile


@pytest.fixture
def three_role_belief():
    return CaseDiagramBelief(
        roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
        probabilities=np.array([0.6, 0.3, 0.1]),
        name="integration_test_belief",
    )


@pytest.fixture
def stochastic_T():
    return np.array([[0.7, 0.2, 0.1], [0.1, 0.8, 0.1], [0.2, 0.1, 0.7]])


class TestIntegrationPushForwardReturn:
    def test_returns_distributional_return(self, three_role_belief, stochastic_T):
        R = np.array([1.0, 0.5, 0.0])
        result = push_forward_return(three_role_belief, stochastic_T, R)
        assert isinstance(result, DistributionalReturn)

    def test_mean_finite(self, three_role_belief, stochastic_T):
        R = np.array([1.0, 0.5, 0.0])
        result = push_forward_return(three_role_belief, stochastic_T, R)
        assert np.isfinite(result.mean)

    def test_variance_non_negative(self, three_role_belief, stochastic_T):
        result = push_forward_return(three_role_belief, stochastic_T, np.array([1.0, 0.5, 0.0]))
        assert result.variance >= 0.0


class TestIntegrationQuantileTDUpdate:
    def test_moves_toward_target(self):
        q = np.array([0.2, 0.5, 0.8])
        t = np.array([0.4, 0.6, 0.9])
        updated = quantile_td_update(q, t, learning_rate=0.5)
        assert np.all(updated >= q - 0.01)

    def test_output_shape(self):
        q = np.linspace(0.1, 0.9, 11)
        updated = quantile_td_update(q, q + 0.1)
        assert updated.shape == q.shape


class TestIntegrationDistributionalCaseAssignment:
    def test_returns_daif_result(self, three_role_belief):
        result = distributional_case_assignment(three_role_belief, np.array([0.7, 0.2, 0.1]))
        assert isinstance(result, DAIFResult)

    def test_posterior_sums_to_one(self, three_role_belief):
        result = distributional_case_assignment(three_role_belief, np.array([0.5, 0.3, 0.2]))
        assert np.isclose(result.belief.probabilities.sum(), 1.0, atol=1e-8)


class TestIntegrationDistributionalPredictionError:
    def test_non_negative(self, three_role_belief):
        dpe = distributional_prediction_error(three_role_belief, 0)
        assert dpe >= 0.0

    def test_low_probability_higher_error(self, three_role_belief):
        dpe_high_prob = distributional_prediction_error(three_role_belief, 0)
        dpe_low_prob = distributional_prediction_error(three_role_belief, 2)
        assert dpe_low_prob > dpe_high_prob


class TestDistributionalReturnHelpers:
    def test_std_matches_variance(self) -> None:
        dr = DistributionalReturn(
            mean=0.0,
            variance=0.25,
            quantiles=np.array([0.0, 0.5, 1.0]),
            quantile_levels=np.array([0.1, 0.5, 0.9]),
        )
        assert dr.std() == pytest.approx(0.5)

    def test_ci_interpolates(self) -> None:
        dr = DistributionalReturn(
            mean=0.0,
            variance=1.0,
            quantiles=np.array([0.0, 1.0, 2.0]),
            quantile_levels=np.array([0.25, 0.5, 0.75]),
        )
        lo, hi = dr.ci(0.5)
        assert lo <= hi

    def test_to_categorical_uniform_when_histogram_empty(self) -> None:
        """Quantiles outside [v_min, v_max] yield zero counts → uniform fallback."""
        dr = DistributionalReturn(
            mean=0.0,
            variance=1.0,
            quantiles=np.array([-100.0, -99.0]),
            quantile_levels=np.array([0.5, 0.9]),
        )
        cat = dr.to_categorical(v_min=0.0, v_max=1.0, n_atoms=5)
        assert cat.shape == (5,)
        assert np.isclose(cat.sum(), 1.0)
        assert np.allclose(cat, 1.0 / 5.0)


class TestDAIFResultProperties:
    def test_converged_when_iteration_before_trajectory_length(self, three_role_belief) -> None:
        r = DAIFResult(
            belief=three_role_belief,
            fe_trajectory=[1.0, 0.9, 0.8],
            convergence_iteration=1,
        )
        assert r.converged is True
        assert r.fe_reduction == pytest.approx(0.2)
        assert r.final_fe == pytest.approx(0.8)

    def test_fe_reduction_zero_for_short_trajectory(self, three_role_belief) -> None:
        r = DAIFResult(
            belief=three_role_belief,
            fe_trajectory=[0.5],
            convergence_iteration=0,
        )
        assert r.fe_reduction == 0.0
        assert not np.isnan(r.final_fe)
        assert r.final_fe == pytest.approx(0.5)

    def test_final_fe_nan_when_empty(self, three_role_belief) -> None:
        r = DAIFResult(
            belief=three_role_belief,
            fe_trajectory=[],
            convergence_iteration=0,
        )
        assert np.isnan(r.final_fe)


class TestERPProfilePeakLatency:
    def test_unknown_component_raises(self) -> None:
        prof = ERPProfile(
            n400_amplitude=-1.0,
            p600_amplitude=1.0,
            waveform_ms=np.array([0.0, 400.0, 800.0]),
            waveform_uV=np.array([0.0, -2.0, 1.0]),
        )
        with pytest.raises(ValueError, match="Unknown component"):
            prof.peak_latency("MMN")

    def test_peak_latency_nan_when_window_empty(self) -> None:
        prof = ERPProfile(
            n400_amplitude=-1.0,
            p600_amplitude=1.0,
            waveform_ms=np.array([0.0, 100.0]),
            waveform_uV=np.array([0.0, 0.0]),
        )
        assert np.isnan(prof.peak_latency("N400"))
        assert np.isnan(prof.peak_latency("P600"))
