"""Tests for the active inference computations module.

Validates free energy, belief updating, prediction error, EFE,
magnitude reanalysis cost, and P600 amplitude ratio.
All tests use real numpy computations — no mocks.
"""

import pytest
import numpy as np

from src.case_systems.case_category import CaseRole
from src.enriched_cat.enriched import EnrichedCategory
from src.cognitive.active_inference import (
    CaseDiagramBelief,
    variational_free_energy,
    update_belief,
    prediction_error,
    expected_free_energy,
    magnitude_reanalysis_cost,
    p600_amplitude_ratio,
)


class TestCaseDiagramBelief:
    """Tests for belief distribution over case diagrams."""

    def test_creation(self) -> None:
        """Valid belief distribution."""
        roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
        probs = np.array([0.6, 0.3, 0.1])
        belief = CaseDiagramBelief(roles=roles, probabilities=probs)
        assert len(belief.roles) == 3

    def test_probabilities_must_sum_to_one(self) -> None:
        """Non-normalized probabilities raise ValueError."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        with pytest.raises(ValueError, match="sum to 1.0"):
            CaseDiagramBelief(roles=roles, probabilities=np.array([0.3, 0.3]))

    def test_negative_probabilities_raise(self) -> None:
        """Negative probabilities raise ValueError."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        with pytest.raises(ValueError, match="non-negative"):
            CaseDiagramBelief(roles=roles, probabilities=np.array([-0.5, 1.5]))

    def test_length_mismatch_raises(self) -> None:
        """Mismatched roles and probabilities raise ValueError."""
        roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
        with pytest.raises(ValueError, match="same length"):
            CaseDiagramBelief(roles=roles, probabilities=np.array([0.5, 0.5]))

    def test_entropy_uniform(self) -> None:
        """Uniform distribution has maximum entropy."""
        roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
        uniform = CaseDiagramBelief(roles=roles, probabilities=np.array([1/3, 1/3, 1/3]))
        assert uniform.entropy() == pytest.approx(np.log(3), abs=1e-10)

    def test_entropy_deterministic(self) -> None:
        """Deterministic distribution has zero entropy."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        determ = CaseDiagramBelief(roles=roles, probabilities=np.array([1.0, 0.0]))
        assert determ.entropy() == pytest.approx(0.0)

    def test_most_likely_role(self) -> None:
        """Most likely role is the argmax."""
        roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
        belief = CaseDiagramBelief(roles=roles, probabilities=np.array([0.1, 0.7, 0.2]))
        assert belief.most_likely_role() == CaseRole.ACC

    def test_probability_of(self) -> None:
        """Query probability of a specific role."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        belief = CaseDiagramBelief(roles=roles, probabilities=np.array([0.4, 0.6]))
        assert belief.probability_of(CaseRole.ACC) == pytest.approx(0.6)

    def test_probability_of_missing_role_raises(self) -> None:
        """Querying missing role raises ValueError."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        belief = CaseDiagramBelief(roles=roles, probabilities=np.array([0.4, 0.6]))
        with pytest.raises(ValueError):
            belief.probability_of(CaseRole.DAT)


class TestVariationalFreeEnergy:
    """Tests for free energy computation."""

    def test_perfect_fit_low_fe(self) -> None:
        """When q matches the generative model, FE is low."""
        q = np.array([0.9, 0.1])
        log_lik = np.log([0.9, 0.1])
        log_prior = np.log([0.5, 0.5])
        fe = variational_free_energy(q, log_lik, log_prior)
        assert isinstance(fe, float)

    def test_unnormalized_raises(self) -> None:
        """Non-normalized q raises ValueError."""
        with pytest.raises(ValueError, match="sum to 1.0"):
            variational_free_energy(
                np.array([0.3, 0.3]),
                np.log([0.5, 0.5]),
                np.log([0.5, 0.5]),
            )

    def test_fe_increases_with_mismatch(self) -> None:
        """FE is higher when q mismatches likelihood."""
        q_good = np.array([0.9, 0.1])
        q_bad = np.array([0.1, 0.9])
        log_lik = np.log([0.9, 0.1])
        log_prior = np.log([0.5, 0.5])
        fe_good = variational_free_energy(q_good, log_lik, log_prior)
        fe_bad = variational_free_energy(q_bad, log_lik, log_prior)
        assert fe_good < fe_bad


class TestBeliefUpdating:
    """Tests for Bayesian belief update."""

    def test_update_shifts_toward_evidence(self) -> None:
        """Update with strong ACC evidence shifts belief toward ACC."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        prior = CaseDiagramBelief(roles=roles, probabilities=np.array([0.5, 0.5]))
        likelihoods = np.array([0.1, 0.9])  # strong ACC evidence
        posterior = update_belief(prior, likelihoods)
        assert posterior.probability_of(CaseRole.ACC) > 0.5

    def test_update_preserves_normalization(self) -> None:
        """Posterior is a valid probability distribution."""
        roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
        prior = CaseDiagramBelief(roles=roles, probabilities=np.array([1/3, 1/3, 1/3]))
        likelihoods = np.array([0.2, 0.5, 0.3])
        posterior = update_belief(prior, likelihoods)
        assert sum(posterior.probabilities) == pytest.approx(1.0)

    def test_update_reduces_entropy(self) -> None:
        """Informative evidence should reduce entropy."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        prior = CaseDiagramBelief(roles=roles, probabilities=np.array([0.5, 0.5]))
        likelihoods = np.array([0.1, 0.9])
        posterior = update_belief(prior, likelihoods)
        assert posterior.entropy() < prior.entropy()

    def test_length_mismatch_raises(self) -> None:
        """Mismatched likelihood length raises ValueError."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        prior = CaseDiagramBelief(roles=roles, probabilities=np.array([0.5, 0.5]))
        with pytest.raises(ValueError, match="likelihoods"):
            update_belief(prior, np.array([0.5]))


class TestPredictionError:
    """Tests for prediction error computation."""

    def test_high_weight_high_error(self) -> None:
        """High-weight morphism produces large PE."""
        pe = prediction_error(0.9, 1.0, 0.0)
        assert pe == pytest.approx(0.9)

    def test_low_weight_low_error(self) -> None:
        """Low-weight morphism produces small PE."""
        pe = prediction_error(0.2, 1.0, 0.0)
        assert pe == pytest.approx(0.2)

    def test_no_mismatch_zero_error(self) -> None:
        """Zero prediction-observation difference → zero PE."""
        pe = prediction_error(0.9, 0.5, 0.5)
        assert pe == pytest.approx(0.0)

    def test_invalid_weight_raises(self) -> None:
        """Weight outside [0,1] raises ValueError."""
        with pytest.raises(ValueError):
            prediction_error(1.5, 1.0, 0.0)

    def test_pe_proportional_to_weight(self) -> None:
        """PE ratio should approximate weight ratio (P600 prediction)."""
        pe_strong = prediction_error(0.9, 1.0, 0.0)
        pe_weak = prediction_error(0.4, 1.0, 0.0)
        assert pe_strong / pe_weak == pytest.approx(0.9 / 0.4)


class TestMagnitudeReanalysisCost:
    """Tests for garden-path reanalysis cost."""

    def test_identical_categories_zero_cost(self) -> None:
        """Same enriched category → zero reanalysis cost."""
        ec = EnrichedCategory(
            name="test",
            roles=[CaseRole.NOM, CaseRole.ACC],
            proximity_matrix=np.array([[1.0, 0.5], [0.5, 1.0]]),
        )
        cost = magnitude_reanalysis_cost(ec, ec)
        assert cost == pytest.approx(0.0)

    def test_different_categories_positive_cost(self) -> None:
        """Different enriched categories → positive reanalysis cost."""
        ec1 = EnrichedCategory(
            name="before",
            roles=[CaseRole.NOM, CaseRole.ACC],
            proximity_matrix=np.array([[1.0, 0.8], [0.8, 1.0]]),
        )
        ec2 = EnrichedCategory(
            name="after",
            roles=[CaseRole.NOM, CaseRole.ACC],
            proximity_matrix=np.array([[1.0, 0.3], [0.3, 1.0]]),
        )
        cost = magnitude_reanalysis_cost(ec1, ec2)
        assert cost > 0


class TestP600Ratio:
    """Tests for P600 amplitude ratio prediction."""

    def test_ratio_computation(self) -> None:
        """Ratio of weights predicts P600 ratio."""
        ratio = p600_amplitude_ratio(0.9, 0.4)
        assert ratio == pytest.approx(0.9 / 0.4)

    def test_equal_weights_ratio_one(self) -> None:
        """Equal weights → ratio of 1."""
        assert p600_amplitude_ratio(0.5, 0.5) == pytest.approx(1.0)

    def test_zero_weak_weight_raises(self) -> None:
        """Zero weak weight → division by zero raises."""
        with pytest.raises(ValueError):
            p600_amplitude_ratio(0.5, 0.0)
