"""Tests for src/daif/core.py — Push-Forward & Distributional Bellman Operator.

All tests use real numerical computations. Zero mocks.
"""

import numpy as np
import pytest

from src.case_systems.case_category import CaseRole
from src.cognitive.belief import CaseDiagramBelief
from src.daif.core import (
    push_forward_return,
    distributional_bellman_operator,
    categorical_return_distribution,
)
from src.daif.types import DistributionalReturn


# --- Fixtures ---

@pytest.fixture
def three_role_belief():
    return CaseDiagramBelief(
        roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
        probabilities=np.array([0.6, 0.3, 0.1]),
        name="test_belief",
    )


@pytest.fixture
def uniform_belief():
    return CaseDiagramBelief(
        roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
        probabilities=np.array([1/3, 1/3, 1/3]),
        name="uniform",
    )


@pytest.fixture
def identity_T():
    return np.eye(3)


@pytest.fixture
def stochastic_T():
    return np.array([[0.7, 0.2, 0.1], [0.1, 0.8, 0.1], [0.2, 0.1, 0.7]])


# --- push_forward_return ---

class TestPushForwardReturn:

    def test_returns_distributional_return_type(self, three_role_belief, identity_T):
        R = np.array([1.0, 0.5, 0.0])
        result = push_forward_return(three_role_belief, identity_T, R)
        assert isinstance(result, DistributionalReturn)

    def test_mean_identity_transition(self, three_role_belief, identity_T):
        """With identity T: mean(Z) = q · (R + γ q)."""
        R = np.array([1.0, 0.5, 0.0])
        q = three_role_belief.probabilities
        result = push_forward_return(three_role_belief, identity_T, R, gamma=0.9)
        expected_z_vec = R + 0.9 * q
        expected_mean = float(q @ expected_z_vec)
        assert np.isclose(result.mean, expected_mean, atol=1e-8)

    def test_zero_gamma_mean_equals_reward(self, three_role_belief, stochastic_T):
        """With γ=0: mean(Z) = q · R."""
        R = np.array([1.0, 2.0, 3.0])
        result = push_forward_return(three_role_belief, stochastic_T, R, gamma=0.0)
        expected_mean = float(three_role_belief.probabilities @ R)
        assert np.isclose(result.mean, expected_mean, atol=1e-8)

    def test_quantile_levels_in_01(self, three_role_belief, identity_T):
        R = np.zeros(3)
        result = push_forward_return(three_role_belief, identity_T, R, n_quantiles=21)
        assert np.all(result.quantile_levels > 0) and np.all(result.quantile_levels < 1)

    def test_quantile_count(self, three_role_belief, identity_T):
        result = push_forward_return(three_role_belief, identity_T, np.zeros(3), n_quantiles=25)
        assert len(result.quantiles) == 25
        assert len(result.quantile_levels) == 25

    def test_variance_non_negative(self, three_role_belief, stochastic_T):
        R = np.array([0.5, 1.5, 2.5])
        result = push_forward_return(three_role_belief, stochastic_T, R)
        assert result.variance >= 0.0

    def test_ci_lower_le_mean_le_upper(self, three_role_belief, stochastic_T):
        R = np.array([1.0, 0.0, -1.0])
        result = push_forward_return(three_role_belief, stochastic_T, R)
        lo, hi = result.ci(alpha=0.05)
        assert lo <= result.mean <= hi

    def test_mismatched_matrix_raises(self, three_role_belief):
        with pytest.raises(ValueError, match="Transition matrix shape"):
            push_forward_return(three_role_belief, np.eye(4), np.zeros(3))

    def test_mismatched_reward_raises(self, three_role_belief, identity_T):
        with pytest.raises(ValueError, match="Reward vector length"):
            push_forward_return(three_role_belief, identity_T, np.zeros(4))

    def test_invalid_gamma_raises(self, three_role_belief, identity_T):
        with pytest.raises(ValueError, match="gamma"):
            push_forward_return(three_role_belief, identity_T, np.zeros(3), gamma=1.5)

    def test_non_stochastic_raises(self, three_role_belief):
        bad = np.array([[0.5, 0.5, 0.5], [0.3, 0.3, 0.4], [0.1, 0.1, 0.1]])
        with pytest.raises(ValueError, match="rows must sum"):
            push_forward_return(three_role_belief, bad, np.zeros(3))

    def test_n_quantiles_too_small_raises(self, three_role_belief, identity_T):
        with pytest.raises(ValueError, match="n_quantiles"):
            push_forward_return(three_role_belief, identity_T, np.zeros(3), n_quantiles=1)


# --- distributional_bellman_operator ---

class TestDistributionalBellmanOperator:

    def test_returns_list_of_correct_length(self, three_role_belief, identity_T):
        R = np.array([1.0, 0.5, 0.0])
        results = distributional_bellman_operator(three_role_belief, identity_T, R, n_steps=5)
        assert len(results) == 5

    def test_all_elements_are_distributional_return(self, three_role_belief, identity_T):
        results = distributional_bellman_operator(three_role_belief, identity_T, np.zeros(3), n_steps=3)
        for r in results:
            assert isinstance(r, DistributionalReturn)

    def test_mean_positive_with_positive_rewards(self, uniform_belief, stochastic_T):
        R = np.array([1.0, 2.0, 3.0])
        results = distributional_bellman_operator(uniform_belief, stochastic_T, R, n_steps=4)
        for r in results:
            assert r.mean > 0

    def test_variance_non_negative_all_steps(self, three_role_belief, stochastic_T):
        results = distributional_bellman_operator(three_role_belief, stochastic_T, np.array([0.5, 1.0, 1.5]), n_steps=5)
        for r in results:
            assert r.variance >= 0.0

    def test_invalid_n_steps_raises(self, three_role_belief, identity_T):
        with pytest.raises(ValueError, match="n_steps"):
            distributional_bellman_operator(three_role_belief, identity_T, np.zeros(3), n_steps=0)

    def test_invalid_matrix_raises(self, three_role_belief):
        with pytest.raises(ValueError, match="Transition matrix shape"):
            distributional_bellman_operator(three_role_belief, np.eye(5), np.zeros(3), n_steps=2)


# --- categorical_return_distribution ---

class TestCategoricalReturnDistribution:

    def test_returns_atoms_and_probs(self, three_role_belief, identity_T):
        R = np.array([0.0, 1.0, 2.0])
        ret = push_forward_return(three_role_belief, identity_T, R)
        atoms, probs = categorical_return_distribution(ret, v_min=-1.0, v_max=3.0, n_atoms=21)
        assert len(atoms) == 21
        assert len(probs) == 21

    def test_probs_sum_to_one(self, three_role_belief, stochastic_T):
        R = np.array([1.0, 2.0, 3.0])
        ret = push_forward_return(three_role_belief, stochastic_T, R)
        _, probs = categorical_return_distribution(ret, v_min=0.0, v_max=5.0, n_atoms=51)
        assert np.isclose(probs.sum(), 1.0, atol=1e-6)

    def test_probs_non_negative(self, three_role_belief, identity_T):
        R = np.ones(3)
        ret = push_forward_return(three_role_belief, identity_T, R)
        _, probs = categorical_return_distribution(ret, v_min=0.0, v_max=2.0, n_atoms=11)
        assert np.all(probs >= 0)

    def test_invalid_vmin_ge_vmax_raises(self, three_role_belief, identity_T):
        R = np.ones(3)
        ret = push_forward_return(three_role_belief, identity_T, R)
        with pytest.raises(ValueError, match="v_min"):
            categorical_return_distribution(ret, v_min=2.0, v_max=1.0)

    def test_invalid_n_atoms_raises(self, three_role_belief, identity_T):
        R = np.ones(3)
        ret = push_forward_return(three_role_belief, identity_T, R)
        with pytest.raises(ValueError, match="n_atoms"):
            categorical_return_distribution(ret, v_min=0.0, v_max=1.0, n_atoms=1)

    def test_to_categorical_helper(self, three_role_belief, identity_T):
        R = np.array([0.5, 1.0, 1.5])
        ret = push_forward_return(three_role_belief, identity_T, R)
        probs = ret.to_categorical(v_min=0.0, v_max=2.0, n_atoms=21)
        assert np.isclose(probs.sum(), 1.0, atol=1e-6)
