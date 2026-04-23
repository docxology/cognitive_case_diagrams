"""Tests for src/daif/prediction.py — DPE, N400/P600, ERP waveform.

All tests use real numerical computations. Zero mocks.
"""

import numpy as np
import pytest

from src.case_systems.case_category import CaseRole
from src.cognitive.belief import CaseDiagramBelief
from src.daif.prediction import (
    distributional_prediction_error,
    wasserstein_prediction_error,
    n400_from_return_distribution,
    p600_from_precision_update,
    erp_amplitude_profile,
)
from src.daif.types import DistributionalReturn, ERPProfile


# --- Fixtures ---

@pytest.fixture
def three_role_belief():
    return CaseDiagramBelief(
        [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
        np.array([0.6, 0.3, 0.1]),
        name="test"
    )


@pytest.fixture
def flat_return_dist():
    taus = np.linspace(0.05, 0.95, 21)
    quantiles = np.linspace(0.5, 1.5, 21)
    return DistributionalReturn(mean=1.0, variance=0.1, quantiles=quantiles, quantile_levels=taus)


# --- distributional_prediction_error ---

class TestDistributionalPredictionError:

    def test_high_confidence_low_error(self, three_role_belief):
        dpe = distributional_prediction_error(three_role_belief, 0, enriched_weight=1.0)
        assert dpe < 1.0  # -log(0.6)≈0.51

    def test_low_confidence_high_error(self, three_role_belief):
        dpe = distributional_prediction_error(three_role_belief, 2, enriched_weight=1.0)
        assert dpe > 1.5  # -log(0.1)≈2.30

    def test_linear_precision_scaling(self, three_role_belief):
        dpe_full = distributional_prediction_error(three_role_belief, 0, enriched_weight=1.0)
        dpe_half = distributional_prediction_error(three_role_belief, 0, enriched_weight=0.5)
        assert np.isclose(dpe_half, dpe_full * 0.5, atol=1e-10)

    def test_zero_weight_zero_error(self, three_role_belief):
        assert distributional_prediction_error(three_role_belief, 0, enriched_weight=0.0) == 0.0

    def test_non_negative_for_all_roles(self, three_role_belief):
        for i in range(len(three_role_belief.roles)):
            assert distributional_prediction_error(three_role_belief, i) >= 0.0

    def test_out_of_range_index_raises(self, three_role_belief):
        with pytest.raises(ValueError, match="out of range"):
            distributional_prediction_error(three_role_belief, 5)

    def test_invalid_weight_raises(self, three_role_belief):
        with pytest.raises(ValueError, match="enriched_weight"):
            distributional_prediction_error(three_role_belief, 0, enriched_weight=1.5)


# --- wasserstein_prediction_error ---

class TestWassersteinPredictionError:

    def test_identical_distributions_zero_dpe(self, flat_return_dist):
        """Identical distributions → DPE = 0."""
        dpe = wasserstein_prediction_error(flat_return_dist, flat_return_dist)
        assert dpe == pytest.approx(0.0, abs=1e-10)

    def test_different_distributions_positive_dpe(self):
        """Different distributions → positive DPE."""
        q1 = np.linspace(0.0, 1.0, 51)
        q2 = np.linspace(0.5, 1.5, 51)
        tau = np.linspace(0.01, 0.99, 51)
        dist_a = DistributionalReturn(mean=0.5, variance=0.1, quantiles=q1, quantile_levels=tau)
        dist_b = DistributionalReturn(mean=1.0, variance=0.1, quantiles=q2, quantile_levels=tau)
        dpe = wasserstein_prediction_error(dist_a, dist_b, enriched_weight=0.8)
        assert dpe > 0.0

    def test_enriched_weight_scales(self):
        """DPE scales linearly with enriched weight."""
        q1 = np.linspace(0.0, 1.0, 51)
        q2 = np.linspace(0.5, 1.5, 51)
        tau = np.linspace(0.01, 0.99, 51)
        dist_a = DistributionalReturn(mean=0.5, variance=0.1, quantiles=q1, quantile_levels=tau)
        dist_b = DistributionalReturn(mean=1.0, variance=0.1, quantiles=q2, quantile_levels=tau)
        dpe_half = wasserstein_prediction_error(dist_a, dist_b, enriched_weight=0.5)
        dpe_full = wasserstein_prediction_error(dist_a, dist_b, enriched_weight=1.0)
        assert dpe_full == pytest.approx(2.0 * dpe_half, rel=1e-8)

    def test_invalid_weight_raises(self):
        """Enriched weight > 1 raises ValueError."""
        q = np.linspace(0.0, 1.0, 51)
        tau = np.linspace(0.01, 0.99, 51)
        dist = DistributionalReturn(mean=0.5, variance=0.1, quantiles=q, quantile_levels=tau)
        with pytest.raises(ValueError, match="enriched_weight"):
            wasserstein_prediction_error(dist, dist, enriched_weight=1.5)


# --- n400_from_return_distribution ---

class TestN400FromReturnDistribution:

    def test_congruent_parse_zero_n400(self, flat_return_dist):
        """When E[Z] == baseline, N400 = 0."""
        n400 = n400_from_return_distribution(flat_return_dist, baseline_return=1.0)
        assert n400 == 0.0

    def test_unexpected_parse_negative_n400(self, flat_return_dist):
        """When E[Z] < baseline, N400 < 0 (mismatch)."""
        n400 = n400_from_return_distribution(flat_return_dist, baseline_return=2.0)
        assert n400 < 0.0

    def test_above_baseline_still_negative_n400(self, flat_return_dist):
        """When E[Z] > baseline, N400 is still negative (absolute mismatch)."""
        n400 = n400_from_return_distribution(flat_return_dist, baseline_return=0.5)
        assert n400 < 0.0  # Any mismatch produces negative N400

    def test_congruent_severity_zero_n400(self, flat_return_dist):
        """When violation_severity=0 (congruent), N400 = 0 regardless of mismatch."""
        n400 = n400_from_return_distribution(
            flat_return_dist, baseline_return=2.0, violation_severity=0.0
        )
        assert n400 == 0.0

    def test_precision_scales_amplitude(self, flat_return_dist):
        n400_low = n400_from_return_distribution(flat_return_dist, baseline_return=2.0, precision=0.5)
        n400_high = n400_from_return_distribution(flat_return_dist, baseline_return=2.0, precision=1.0)
        assert abs(n400_high) > abs(n400_low) - 1e-10

    def test_negative_precision_raises(self, flat_return_dist):
        with pytest.raises(ValueError, match="precision"):
            n400_from_return_distribution(flat_return_dist, baseline_return=1.0, precision=-1.0)


# --- p600_from_precision_update ---

class TestP600FromPrecisionUpdate:

    def test_no_precision_increase_zero_p600(self):
        """When λ_post == λ_prior, ΔΛ=0 → P600=0."""
        p600 = p600_from_precision_update(1.0, 1.0, dpe=1.0)
        assert p600 == 0.0

    def test_precision_increase_positive_p600(self):
        p600 = p600_from_precision_update(1.0, 3.0, dpe=1.5)
        assert p600 > 0.0

    def test_scales_with_dpe(self):
        p600_low = p600_from_precision_update(1.0, 2.0, dpe=0.5)
        p600_high = p600_from_precision_update(1.0, 2.0, dpe=2.0)
        assert p600_high > p600_low

    def test_scales_with_scaling_factor(self):
        p600_s1 = p600_from_precision_update(1.0, 2.0, dpe=1.0, scaling=1.0)
        p600_s2 = p600_from_precision_update(1.0, 2.0, dpe=1.0, scaling=2.0)
        assert np.isclose(p600_s2, 2.0 * p600_s1)

    def test_negative_prior_precision_raises(self):
        with pytest.raises(ValueError, match="prior_precision"):
            p600_from_precision_update(-1.0, 2.0, dpe=1.0)

    def test_negative_posterior_precision_raises(self):
        with pytest.raises(ValueError, match="posterior_precision"):
            p600_from_precision_update(1.0, -1.0, dpe=1.0)

    def test_negative_dpe_raises(self):
        with pytest.raises(ValueError, match="dpe"):
            p600_from_precision_update(1.0, 2.0, dpe=-0.5)

    def test_negative_scaling_raises(self):
        with pytest.raises(ValueError, match="scaling"):
            p600_from_precision_update(1.0, 2.0, dpe=1.0, scaling=-1.0)


# --- erp_amplitude_profile ---

class TestERPAmplitudeProfile:

    def test_returns_erp_profile_type(self, three_role_belief):
        result = erp_amplitude_profile(three_role_belief, expected_role_index=0, condition="congruent")
        assert isinstance(result, ERPProfile)

    def test_congruent_small_n400(self, three_role_belief):
        """High-confidence role should produce small N400."""
        result = erp_amplitude_profile(three_role_belief, expected_role_index=0)
        assert abs(result.n400_amplitude) < 1.0

    def test_violation_large_n400(self, three_role_belief):
        """Low-probability role → large N400."""
        result = erp_amplitude_profile(three_role_belief, expected_role_index=2)
        assert abs(result.n400_amplitude) > 1.0

    def test_waveform_arrays_match_length(self, three_role_belief):
        result = erp_amplitude_profile(three_role_belief, 0, n_timepoints=500)
        assert len(result.waveform_ms) == 500
        assert len(result.waveform_uV) == 500

    def test_baseline_correction_near_zero(self, three_role_belief):
        """Pre-stimulus mean should be ≈0 after baseline correction."""
        result = erp_amplitude_profile(three_role_belief, 0, t_start_ms=-200, t_end_ms=900)
        pre_mask = result.waveform_ms < 0
        baseline_mean = float(result.waveform_uV[pre_mask].mean())
        assert abs(baseline_mean) < 0.5

    def test_peak_latency_n400_in_window(self, three_role_belief):
        result = erp_amplitude_profile(three_role_belief, 2, condition="violation")
        lat = result.peak_latency("N400")
        assert 200 <= lat <= 500

    def test_peak_latency_p600_in_window(self, three_role_belief):
        result = erp_amplitude_profile(three_role_belief, 2, condition="violation",
                                       prior_precision=1.0, posterior_precision=4.0)
        lat = result.peak_latency("P600")
        assert 500 <= lat <= 900

    def test_invalid_t_range_raises(self, three_role_belief):
        with pytest.raises(ValueError, match="t_start_ms"):
            erp_amplitude_profile(three_role_belief, 0, t_start_ms=500, t_end_ms=200)

    def test_condition_label_preserved(self, three_role_belief):
        result = erp_amplitude_profile(three_role_belief, 0, condition="my_cond")
        assert result.condition == "my_cond"
