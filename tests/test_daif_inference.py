"""Tests for src/daif/inference.py — Distributional Case Assignment & VMP.

All tests use real numerical computations. Zero mocks.
"""

import numpy as np
import pytest

from src.case_systems.case_category import CaseRole
from src.cognitive.belief import CaseDiagramBelief
from src.daif.inference import (
    distributional_case_assignment,
    variational_message_passing,
    bethe_free_energy,
    expected_information_gain,
)
from src.daif.types import DAIFResult, DistributionalReturn


# --- Fixtures ---

@pytest.fixture
def three_roles():
    return [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]


@pytest.fixture
def uniform_belief(three_roles):
    return CaseDiagramBelief(three_roles, np.array([1/3, 1/3, 1/3]), name="uniform")


@pytest.fixture
def peaked_belief(three_roles):
    return CaseDiagramBelief(three_roles, np.array([0.8, 0.15, 0.05]), name="peaked")


@pytest.fixture
def stochastic_T():
    return np.array([[0.7, 0.2, 0.1], [0.1, 0.8, 0.1], [0.2, 0.1, 0.7]])


# --- distributional_case_assignment ---

class TestDistributionalCaseAssignment:

    def test_returns_daif_result(self, uniform_belief):
        result = distributional_case_assignment(
            uniform_belief, np.array([0.8, 0.15, 0.05])
        )
        assert isinstance(result, DAIFResult)

    def test_strong_evidence_concentrates_posterior(self, uniform_belief):
        likelihoods = np.array([0.95, 0.03, 0.02])
        result = distributional_case_assignment(uniform_belief, likelihoods, n_iterations=8)
        assert result.belief.most_likely_role() == CaseRole.NOM
        assert result.belief.probabilities[0] > 0.7

    def test_posterior_sums_to_one(self, uniform_belief):
        result = distributional_case_assignment(uniform_belief, np.array([0.4, 0.4, 0.2]))
        assert np.isclose(result.belief.probabilities.sum(), 1.0, atol=1e-8)

    def test_fe_trajectory_non_empty(self, peaked_belief):
        result = distributional_case_assignment(peaked_belief, np.array([0.6, 0.3, 0.1]))
        assert len(result.fe_trajectory) >= 1

    def test_fe_trajectory_bounded(self, uniform_belief):
        result = distributional_case_assignment(uniform_belief, np.array([0.5, 0.3, 0.2]), n_iterations=15)
        assert len(result.fe_trajectory) <= 15

    def test_convergence_stops_early(self, peaked_belief):
        result = distributional_case_assignment(
            peaked_belief, np.array([0.7, 0.2, 0.1]),
            n_iterations=50, convergence_threshold=1e-3
        )
        assert len(result.fe_trajectory) < 50

    def test_with_transition_matrix(self, uniform_belief, stochastic_T):
        result = distributional_case_assignment(
            uniform_belief, np.array([0.6, 0.3, 0.1]),
            transition_matrix=stochastic_T, n_iterations=5
        )
        assert len(result.belief.roles) == 3

    def test_return_distribution_present(self, uniform_belief):
        result = distributional_case_assignment(uniform_belief, np.array([0.5, 0.3, 0.2]))
        assert result.return_distribution is not None
        assert isinstance(result.return_distribution, DistributionalReturn)

    def test_diagnostics_keys(self, uniform_belief):
        result = distributional_case_assignment(uniform_belief, np.array([0.5, 0.3, 0.2]))
        for key in ("fe_reduction", "n_iterations_run", "final_entropy", "most_likely_role"):
            assert key in result.diagnostics

    def test_mismatched_likelihoods_raises(self, uniform_belief):
        with pytest.raises(ValueError, match="Likelihoods"):
            distributional_case_assignment(uniform_belief, np.array([0.5, 0.5]))

    def test_invalid_transition_shape_raises(self, uniform_belief):
        with pytest.raises(ValueError, match="Transition matrix shape"):
            distributional_case_assignment(uniform_belief, np.array([0.5, 0.3, 0.2]),
                                           transition_matrix=np.eye(5))


# --- variational_message_passing ---

class TestVariationalMessagePassing:

    def test_returns_mean_and_precision(self):
        obs = np.array([0.6, 0.3, 0.1])
        mu, lam = variational_message_passing(obs, prior_precision=1.0, likelihood_precision=2.0)
        assert mu.shape == (3,)
        assert lam.shape == (3,)

    def test_posterior_mean_sums_to_one(self):
        obs = np.array([0.7, 0.2, 0.1])
        mu, _ = variational_message_passing(obs, prior_precision=1.0, likelihood_precision=5.0, n_iterations=8)
        assert np.isclose(mu.sum(), 1.0, atol=1e-8)

    def test_strong_likelihood_dominates(self):
        obs = np.array([0.9, 0.05, 0.05])
        mu, _ = variational_message_passing(obs, prior_precision=0.1, likelihood_precision=10.0)
        assert np.argmax(mu) == 0

    def test_posterior_precision_ge_prior(self):
        obs = np.array([0.5, 0.3, 0.2])
        _, lam = variational_message_passing(obs, prior_precision=1.0, likelihood_precision=2.0)
        assert np.all(lam >= 1.0)

    def test_non_positive_prior_precision_raises(self):
        with pytest.raises(ValueError, match="prior_precision"):
            variational_message_passing(np.array([0.5, 0.5]), prior_precision=-1.0, likelihood_precision=1.0)

    def test_non_positive_likelihood_precision_raises(self):
        with pytest.raises(ValueError, match="likelihood_precision"):
            variational_message_passing(np.array([0.5, 0.5]), prior_precision=1.0, likelihood_precision=0.0)


# --- bethe_free_energy ---

class TestBetheeFreeEnergy:

    def test_returns_scalar(self, peaked_belief):
        factor_beliefs = [np.array([0.6, 0.3, 0.1]), np.array([0.5, 0.4, 0.1])]
        adjacency = np.array([[1, 1], [1, 0], [0, 1]])
        fe = bethe_free_energy(peaked_belief, factor_beliefs, adjacency)
        assert isinstance(fe, float)

    def test_uniform_adjacent_factors(self, uniform_belief):
        n, m = 3, 2
        factor_beliefs = [np.full(n, 1/n) for _ in range(m)]
        adjacency = np.ones((n, m))
        fe = bethe_free_energy(uniform_belief, factor_beliefs, adjacency)
        assert np.isfinite(fe)

    def test_identity_adjacency_factor(self, peaked_belief):
        factor_beliefs = [peaked_belief.probabilities.copy()]
        adjacency = np.ones((3, 1))
        fe = bethe_free_energy(peaked_belief, factor_beliefs, adjacency)
        assert np.isfinite(fe)

    def test_invalid_adjacency_shape_raises(self, peaked_belief):
        factor_beliefs = [np.array([0.5, 0.5, 0.0])]
        wrong_adj = np.ones((4, 1))  # wrong n_vars
        with pytest.raises(ValueError, match="Adjacency shape"):
            bethe_free_energy(peaked_belief, factor_beliefs, wrong_adj)

    def test_zero_variable_belief_raises(self, three_roles):
        bad_belief = CaseDiagramBelief(three_roles, np.array([1.0, 0.0, 0.0]), name="degenerate")
        factor_beliefs = [np.array([0.5, 0.3, 0.2])]
        adj = np.ones((3, 1))
        with pytest.raises(ValueError, match="strictly positive"):
            bethe_free_energy(bad_belief, factor_beliefs, adj)


# --- expected_information_gain ---

class TestExpectedInformationGain:

    def test_returns_correct_shape(self, uniform_belief):
        observations = np.array([[0.8, 0.1, 0.1], [0.3, 0.6, 0.1], [0.2, 0.2, 0.6]])
        eig = expected_information_gain(uniform_belief, observations)
        assert eig.shape == (3,)

    def test_informative_obs_higher_eig(self, uniform_belief):
        informative = np.array([[0.99, 0.005, 0.005]])
        uninformative = np.array([[1/3, 1/3, 1/3]])
        eig_info = expected_information_gain(uniform_belief, informative)
        eig_uninfo = expected_information_gain(uniform_belief, uninformative)
        assert eig_info[0] > eig_uninfo[0]

    def test_eig_non_negative(self, uniform_belief):
        observations = np.array([[0.7, 0.2, 0.1], [0.1, 0.8, 0.1]])
        eig = expected_information_gain(uniform_belief, observations)
        assert np.all(eig >= 0.0)

    def test_shape_mismatch_raises(self, uniform_belief):
        with pytest.raises(ValueError, match="columns"):
            expected_information_gain(uniform_belief, np.array([[0.5, 0.5]]))

    def test_negative_likelihoods_raises(self, uniform_belief):
        with pytest.raises(ValueError, match="non-negative"):
            expected_information_gain(uniform_belief, np.array([[-0.1, 0.6, 0.5]]))


# --- Phase A5 / A8: per-iteration KL and data-fit trajectories ---

class TestDiagnosticsKLandLoglik:
    """distributional_case_assignment must expose per-iteration
    KL(q_posterior ‖ q_pushed) and E_q[log p(o|s)] so the figure layer
    can plot the real F = KL − E_q[log p(o|s)] decomposition."""

    def test_kl_and_loglik_lists_match_fe_length(self, uniform_belief):
        obs = np.array([0.8, 0.15, 0.05])
        result = distributional_case_assignment(uniform_belief, obs, n_iterations=4)
        diag = result.diagnostics
        assert "kl_trajectory" in diag
        assert "loglik_trajectory" in diag
        assert len(diag["kl_trajectory"]) == len(result.fe_trajectory)
        assert len(diag["loglik_trajectory"]) == len(result.fe_trajectory)

    def test_kl_non_negative_and_fe_identity(self, uniform_belief):
        obs = np.array([0.8, 0.15, 0.05])
        result = distributional_case_assignment(uniform_belief, obs, n_iterations=4)
        kl = np.asarray(result.diagnostics["kl_trajectory"])
        ll = np.asarray(result.diagnostics["loglik_trajectory"])
        fe = np.asarray(result.fe_trajectory)
        assert np.all(kl >= -1e-9)
        # F = KL − E_q[log p(o|s)] to numerical precision
        np.testing.assert_allclose(fe, kl - ll, atol=1e-8)

    @pytest.mark.parametrize(
        "prior_probs, obs",
        [
            (np.array([0.6, 0.3, 0.1]), np.array([0.7, 0.2, 0.1])),
            (np.array([0.9, 0.05, 0.05]), np.array([0.4, 0.3, 0.3])),
            (np.array([0.34, 0.33, 0.33]), np.array([0.5, 0.3, 0.2])),
            (np.array([0.2, 0.5, 0.3]), np.array([0.1, 0.6, 0.3])),
        ],
    )
    def test_fe_kl_loglik_identity_across_settings(
        self, three_roles, prior_probs, obs
    ):
        """F^{(t)} = KL^{(t)} - E_q[log p(o|s)]^{(t)} must hold at every
        iteration, under varied prior/observation combinations."""
        prior = CaseDiagramBelief(three_roles, prior_probs, name="param_prior")
        result = distributional_case_assignment(prior, obs, n_iterations=6)
        fe = np.asarray(result.fe_trajectory)
        kl = np.asarray(result.diagnostics["kl_trajectory"])
        ll = np.asarray(result.diagnostics["loglik_trajectory"])
        assert fe.shape == kl.shape == ll.shape
        np.testing.assert_allclose(fe, kl - ll, atol=1e-8)
