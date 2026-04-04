"""Tests for the active inference computations module.

Validates free energy, KL divergence, belief updating, sequential update,
prediction error, EFE, magnitude reanalysis cost, N400 proxy,
and P600 amplitude ratio.
All tests use real numpy computations — no mocks.
"""

import pytest
import numpy as np

from src.case_systems.case_category import CaseRole
from src.enriched_cat.enriched import EnrichedCategory
from src.cognitive.belief import CaseDiagramBelief
from src.cognitive.free_energy import kl_divergence, variational_free_energy
from src.cognitive.belief_updating import update_belief, sequential_belief_update
from src.cognitive.prediction_error import prediction_error, p600_amplitude_ratio
from src.cognitive.action_selection import expected_free_energy
from src.cognitive.reanalysis import magnitude_reanalysis_cost, n400_amplitude_proxy


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

    def test_name_default(self) -> None:
        """Default name is 'belief'."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        belief = CaseDiagramBelief(roles=roles, probabilities=np.array([0.5, 0.5]))
        assert belief.name == "belief"


class TestKLDivergence:
    """Tests for KL divergence computation."""

    def test_identical_distributions_zero(self) -> None:
        """KL(q || q) = 0 for any valid q."""
        q = np.array([0.7, 0.2, 0.1])
        assert kl_divergence(q, q) == pytest.approx(0.0, abs=1e-12)

    def test_non_negativity(self) -> None:
        """KL divergence is always non-negative (Gibbs' inequality)."""
        q = np.array([0.8, 0.1, 0.1])
        p = np.array([0.3, 0.4, 0.3])
        assert kl_divergence(q, p) >= 0.0

    def test_asymmetry(self) -> None:
        """KL(q || p) ≠ KL(p || q) in general (not a metric)."""
        q = np.array([0.9, 0.1])
        p = np.array([0.5, 0.5])
        kl_qp = kl_divergence(q, p)
        kl_pq = kl_divergence(p, q)
        assert kl_qp != pytest.approx(kl_pq)

    def test_unnormalized_q_raises(self) -> None:
        """Non-normalized q raises ValueError."""
        with pytest.raises(ValueError, match="sum to 1.0"):
            kl_divergence(np.array([0.3, 0.3]), np.array([0.5, 0.5]))

    def test_unnormalized_p_raises(self) -> None:
        """Non-normalized p raises ValueError."""
        with pytest.raises(ValueError, match="sum to 1.0"):
            kl_divergence(np.array([0.5, 0.5]), np.array([0.3, 0.3]))

    def test_length_mismatch_raises(self) -> None:
        """Mismatched lengths raise ValueError."""
        with pytest.raises(ValueError, match="same length"):
            kl_divergence(np.array([0.5, 0.5]), np.array([1/3, 1/3, 1/3]))

    def test_infinite_when_p_zero_q_nonzero(self) -> None:
        """KL is infinite when p_i = 0 but q_i > 0."""
        q = np.array([0.5, 0.5])
        p = np.array([1.0, 0.0])
        assert kl_divergence(q, p) == float('inf')


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

    def test_zero_likelihood_raises(self) -> None:
        """All-zero likelihoods raise ValueError (incompatible observation)."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        prior = CaseDiagramBelief(roles=roles, probabilities=np.array([0.5, 0.5]))
        with pytest.raises(ValueError, match="zero"):
            update_belief(prior, np.array([0.0, 0.0]))

    def test_name_propagation(self) -> None:
        """Updated belief has '_updated' name suffix."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        prior = CaseDiagramBelief(roles=roles, probabilities=np.array([0.5, 0.5]), name="test")
        posterior = update_belief(prior, np.array([0.3, 0.7]))
        assert posterior.name == "test_updated"


class TestSequentialBeliefUpdate:
    """Tests for multi-word sequential belief update (§7 five-step loop)."""

    def test_multi_step_convergence(self) -> None:
        """Repeated strong NOM evidence converges belief to NOM."""
        roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
        prior = CaseDiagramBelief(roles=roles, probabilities=np.array([1/3, 1/3, 1/3]))
        obs_seq = [
            np.array([0.7, 0.2, 0.1]),
            np.array([0.8, 0.1, 0.1]),
            np.array([0.9, 0.05, 0.05]),
        ]
        trajectory = sequential_belief_update(prior, obs_seq)
        assert len(trajectory) == 3
        assert trajectory[-1].most_likely_role() == CaseRole.NOM
        assert trajectory[-1].probability_of(CaseRole.NOM) > 0.9

    def test_entropy_monotonically_decreasing(self) -> None:
        """Entropy decreases with each informative observation."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        prior = CaseDiagramBelief(roles=roles, probabilities=np.array([0.5, 0.5]))
        obs_seq = [
            np.array([0.7, 0.3]),
            np.array([0.8, 0.2]),
        ]
        trajectory = sequential_belief_update(prior, obs_seq)
        entropies = [prior.entropy()] + [b.entropy() for b in trajectory]
        for i in range(1, len(entropies)):
            assert entropies[i] <= entropies[i - 1] + 1e-10

    def test_trajectory_length(self) -> None:
        """Trajectory length matches observation sequence length."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        prior = CaseDiagramBelief(roles=roles, probabilities=np.array([0.5, 0.5]))
        obs_seq = [np.array([0.6, 0.4])] * 5
        trajectory = sequential_belief_update(prior, obs_seq)
        assert len(trajectory) == 5

    def test_empty_sequence_returns_empty(self) -> None:
        """Empty observation sequence returns empty trajectory."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        prior = CaseDiagramBelief(roles=roles, probabilities=np.array([0.5, 0.5]))
        trajectory = sequential_belief_update(prior, [])
        assert trajectory == []

    def test_name_includes_step_index(self) -> None:
        """Each trajectory belief is named with step index."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        prior = CaseDiagramBelief(roles=roles, probabilities=np.array([0.5, 0.5]), name="prior")
        trajectory = sequential_belief_update(prior, [np.array([0.6, 0.4])])
        assert trajectory[0].name == "prior_t1"


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

    def test_boundary_weight_zero(self) -> None:
        """Weight=0.0 produces zero PE regardless of mismatch."""
        pe = prediction_error(0.0, 100.0, 0.0)
        assert pe == pytest.approx(0.0)

    def test_boundary_weight_one(self) -> None:
        """Weight=1.0 produces PE equal to absolute deviation."""
        pe = prediction_error(1.0, 3.0, 1.0)
        assert pe == pytest.approx(2.0)

    def test_negative_weight_raises(self) -> None:
        """Negative weight raises ValueError."""
        with pytest.raises(ValueError):
            prediction_error(-0.1, 1.0, 0.0)


class TestExpectedFreeEnergy:
    """Tests for expected free energy (action selection)."""

    def test_basic_computation(self) -> None:
        """EFE returns a finite float."""
        q = np.array([0.6, 0.4])
        log_lik = np.log([0.7, 0.3])
        epi = np.array([0.5, 0.3])
        prag = np.array([0.2, 0.1])
        efe = expected_free_energy(q, log_lik, epi, prag)
        assert isinstance(efe, float)
        assert np.isfinite(efe)

    def test_gamma_zero_epistemic_only(self) -> None:
        """With gamma=0, pragmatic value is ignored."""
        q = np.array([0.5, 0.5])
        log_lik = np.log([0.5, 0.5])
        epi = np.array([0.5, 0.5])
        prag = np.array([100.0, 100.0])  # large pragmatic — should be ignored
        efe_no_prag = expected_free_energy(q, log_lik, epi, prag, gamma=0.0)
        efe_prag = expected_free_energy(q, log_lik, epi, prag, gamma=1.0)
        assert efe_no_prag > efe_prag  # pragmatic value reduces EFE

    def test_high_pragmatic_reduces_efe(self) -> None:
        """Higher pragmatic value yields lower EFE (more preferred)."""
        q = np.array([0.5, 0.5])
        log_lik = np.log([0.5, 0.5])
        epi = np.array([0.1, 0.1])
        prag_low = np.array([0.1, 0.1])
        prag_high = np.array([1.0, 1.0])
        efe_low = expected_free_energy(q, log_lik, epi, prag_low)
        efe_high = expected_free_energy(q, log_lik, epi, prag_high)
        assert efe_high < efe_low

    def test_decomposition_ambiguity_minus_epistemic(self) -> None:
        """EFE decomposes into ambiguity - epistemic - pragmatic."""
        q = np.array([0.7, 0.3])
        log_lik = np.log([0.8, 0.2])
        epi = np.array([0.4, 0.2])
        prag = np.array([0.3, 0.1])
        gamma = 2.0
        efe = expected_free_energy(q, log_lik, epi, prag, gamma=gamma)
        # Manual decomposition
        ambiguity = -np.sum(q * log_lik)
        info_gain = np.sum(q * epi)
        prag_val = gamma * np.sum(q * prag)
        expected = ambiguity - info_gain - prag_val
        assert efe == pytest.approx(expected)


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

    def test_symmetry(self) -> None:
        """Reanalysis cost is symmetric: cost(A,B) == cost(B,A)."""
        ec1 = EnrichedCategory(
            name="a",
            roles=[CaseRole.NOM, CaseRole.ACC],
            proximity_matrix=np.array([[1.0, 0.9], [0.9, 1.0]]),
        )
        ec2 = EnrichedCategory(
            name="b",
            roles=[CaseRole.NOM, CaseRole.ACC],
            proximity_matrix=np.array([[1.0, 0.2], [0.2, 1.0]]),
        )
        assert magnitude_reanalysis_cost(ec1, ec2) == pytest.approx(
            magnitude_reanalysis_cost(ec2, ec1)
        )


class TestN400AmplitudeProxy:
    """Tests for N400 semantic violation proxy."""

    def test_identical_categories_zero(self) -> None:
        """Same category → zero N400 proxy."""
        ec = EnrichedCategory(
            name="test",
            roles=[CaseRole.NOM, CaseRole.ACC],
            proximity_matrix=np.array([[1.0, 0.5], [0.5, 1.0]]),
        )
        assert n400_amplitude_proxy(ec, ec) == pytest.approx(0.0)

    def test_different_categories_positive(self) -> None:
        """Different categories → positive N400 proxy."""
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
        assert n400_amplitude_proxy(ec1, ec2) > 0

    def test_symmetry(self) -> None:
        """N400 proxy is symmetric: proxy(A,B) == proxy(B,A)."""
        ec1 = EnrichedCategory(
            name="a",
            roles=[CaseRole.NOM, CaseRole.ACC],
            proximity_matrix=np.array([[1.0, 0.9], [0.9, 1.0]]),
        )
        ec2 = EnrichedCategory(
            name="b",
            roles=[CaseRole.NOM, CaseRole.ACC],
            proximity_matrix=np.array([[1.0, 0.2], [0.2, 1.0]]),
        )
        assert n400_amplitude_proxy(ec1, ec2) == pytest.approx(
            n400_amplitude_proxy(ec2, ec1)
        )


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

    def test_strong_weight_out_of_range_raises(self) -> None:
        """Strong weight > 1.0 raises ValueError."""
        with pytest.raises(ValueError):
            p600_amplitude_ratio(1.5, 0.5)

