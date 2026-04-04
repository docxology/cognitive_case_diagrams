"""Tests for src/daif/policy.py — Expected Free Energy & Policy Selection.

All tests use real numerical computations. Zero mocks.
"""

import numpy as np
import pytest

from src.case_systems.case_category import CaseRole
from src.cognitive.belief import CaseDiagramBelief
from src.daif.policy import (
    G_policy,
    softmax_policy_selection,
    distributional_epistemic_value,
)
from src.daif.types import DistributionalReturn


@pytest.fixture
def uniform_belief():
    return CaseDiagramBelief(
        [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
        np.array([1/3, 1/3, 1/3]), name="uniform",
    )


@pytest.fixture
def peaked_belief():
    return CaseDiagramBelief(
        [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
        np.array([0.8, 0.15, 0.05]), name="peaked",
    )


def _make_dist(var=1.0, offset=0.0, n=21):
    taus = np.linspace(0.05, 0.95, n)
    q = np.linspace(offset - np.sqrt(var), offset + np.sqrt(var), n)
    return DistributionalReturn(mean=float(offset), variance=float(var), quantiles=q, quantile_levels=taus)


class TestGPolicy:

    def test_returns_finite_scalar(self, uniform_belief):
        g = G_policy(
            uniform_belief,
            log_likelihood=np.log([0.5, 0.3, 0.2]),
            epistemic_value=np.array([0.3, 0.2, 0.1]),
            pragmatic_value=np.array([1.0, 0.5, 0.0]),
        )
        assert isinstance(g, float) and np.isfinite(g)

    def test_high_epistemic_value_reduces_g(self, uniform_belief):
        g_base = G_policy(uniform_belief, np.zeros(3), np.zeros(3), np.zeros(3))
        g_eig = G_policy(uniform_belief, np.zeros(3), np.ones(3), np.zeros(3))
        assert g_eig < g_base

    def test_risk_penalty_increases_g(self, uniform_belief):
        high_var = _make_dist(var=4.0)
        g_no_risk = G_policy(uniform_belief, np.zeros(3), np.zeros(3), np.zeros(3), risk_sensitivity=0.0)
        g_risk = G_policy(uniform_belief, np.zeros(3), np.zeros(3), np.zeros(3),
                          return_dist=high_var, risk_sensitivity=1.0)
        assert g_risk > g_no_risk

    def test_invalid_gamma_raises(self, uniform_belief):
        with pytest.raises(ValueError, match="gamma"):
            G_policy(uniform_belief, np.zeros(3), np.zeros(3), np.zeros(3), gamma=0.0)

    def test_negative_risk_sensitivity_raises(self, uniform_belief):
        with pytest.raises(ValueError, match="risk_sensitivity"):
            G_policy(uniform_belief, np.zeros(3), np.zeros(3), np.zeros(3), risk_sensitivity=-1.0)

    def test_wrong_ll_shape_raises(self, uniform_belief):
        with pytest.raises(ValueError, match="log_likelihood"):
            G_policy(uniform_belief, np.zeros(5), np.zeros(3), np.zeros(3))

    def test_wrong_epistemic_shape_raises(self, uniform_belief):
        with pytest.raises(ValueError, match="epistemic_value"):
            G_policy(uniform_belief, np.zeros(3), np.zeros(5), np.zeros(3))


class TestSoftmaxPolicySelection:

    def test_sums_to_one(self):
        probs = softmax_policy_selection(np.array([1.0, 2.0, 0.5]))
        assert np.isclose(probs.sum(), 1.0, atol=1e-8)

    def test_min_g_gets_max_prob(self):
        g = np.array([5.0, 1.0, 3.0])
        probs = softmax_policy_selection(g)
        assert np.argmax(probs) == 1

    def test_high_temperature_near_uniform(self):
        probs = softmax_policy_selection(np.array([1.0, 2.0, 3.0]), temperature=1e4)
        assert np.all(np.abs(probs - 1/3) < 0.01)

    def test_low_temperature_concentrates(self):
        probs = softmax_policy_selection(np.array([1.0, 0.0, 2.0]), temperature=0.001)
        assert probs[1] > 0.99

    def test_single_policy(self):
        assert np.isclose(softmax_policy_selection(np.array([0.5]))[0], 1.0)

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="non-empty"):
            softmax_policy_selection(np.array([]))

    def test_negative_temperature_raises(self):
        with pytest.raises(ValueError, match="temperature"):
            softmax_policy_selection(np.array([1.0]), temperature=-1.0)


class TestDistributionalEpistemicValue:

    def test_high_var_positive_ev(self):
        ev = distributional_epistemic_value(_make_dist(var=4.0), reference_variance=0.5)
        assert ev > 0.0

    def test_low_var_negative_ev(self):
        ev = distributional_epistemic_value(_make_dist(var=0.01), reference_variance=1.0)
        assert ev < 0.0

    def test_matching_variance_near_zero(self):
        ev = distributional_epistemic_value(_make_dist(var=1.0), reference_variance=1.0)
        assert abs(ev) < 0.5  # close to zero (tolerance for discrete approx)

    def test_zero_variance_capped(self):
        taus = np.linspace(0.05, 0.95, 21)
        dist = DistributionalReturn(mean=0.0, variance=0.0, quantiles=np.ones(21), quantile_levels=taus)
        ev = distributional_epistemic_value(dist, reference_variance=1.0)
        assert ev < 0.0

    def test_invalid_reference_variance_raises(self):
        with pytest.raises(ValueError, match="reference_variance"):
            distributional_epistemic_value(_make_dist(), reference_variance=-1.0)
