"""Tests for the belief_updating module — Bayesian update and sequential processing.

All tests use real numpy computations — no mocks.
"""

import pytest
import numpy as np

from src.case_systems.case_category import CaseRole
from src.cognitive.belief import CaseDiagramBelief
from src.cognitive.belief_updating import update_belief, sequential_belief_update


class TestUpdateBelief:
    """Tests for single-step Bayesian belief update."""

    def test_shifts_toward_evidence(self) -> None:
        """Update with strong ACC evidence shifts belief toward ACC."""
        prior = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC],
            probabilities=np.array([0.5, 0.5]),
        )
        posterior = update_belief(prior, np.array([0.1, 0.9]))
        assert posterior.probability_of(CaseRole.ACC) > 0.5

    def test_preserves_normalization(self) -> None:
        """Posterior is a valid probability distribution."""
        prior = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
            probabilities=np.array([1/3, 1/3, 1/3]),
        )
        posterior = update_belief(prior, np.array([0.2, 0.5, 0.3]))
        assert sum(posterior.probabilities) == pytest.approx(1.0)

    def test_reduces_entropy(self) -> None:
        """Informative evidence reduces entropy."""
        prior = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC],
            probabilities=np.array([0.5, 0.5]),
        )
        posterior = update_belief(prior, np.array([0.1, 0.9]))
        assert posterior.entropy() < prior.entropy()

    def test_length_mismatch_raises(self) -> None:
        """Mismatched likelihood length raises ValueError."""
        prior = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC],
            probabilities=np.array([0.5, 0.5]),
        )
        with pytest.raises(ValueError, match="likelihoods"):
            update_belief(prior, np.array([0.5]))

    def test_zero_likelihood_raises(self) -> None:
        """All-zero likelihoods raise ValueError."""
        prior = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC],
            probabilities=np.array([0.5, 0.5]),
        )
        with pytest.raises(ValueError, match="zero"):
            update_belief(prior, np.array([0.0, 0.0]))

    def test_name_propagation(self) -> None:
        """Updated belief has '_updated' name suffix."""
        prior = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC],
            probabilities=np.array([0.5, 0.5]),
            name="test",
        )
        posterior = update_belief(prior, np.array([0.3, 0.7]))
        assert posterior.name == "test_updated"


class TestSequentialBeliefUpdate:
    """Tests for multi-word sequential belief update."""

    def test_convergence(self) -> None:
        """Repeated strong NOM evidence converges to NOM."""
        prior = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
            probabilities=np.array([1/3, 1/3, 1/3]),
        )
        trajectory = sequential_belief_update(prior, [
            np.array([0.7, 0.2, 0.1]),
            np.array([0.8, 0.1, 0.1]),
            np.array([0.9, 0.05, 0.05]),
        ])
        assert len(trajectory) == 3
        assert trajectory[-1].most_likely_role() == CaseRole.NOM
        assert trajectory[-1].probability_of(CaseRole.NOM) > 0.9

    def test_entropy_monotonically_decreasing(self) -> None:
        """Entropy decreases with each informative observation."""
        prior = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC],
            probabilities=np.array([0.5, 0.5]),
        )
        trajectory = sequential_belief_update(prior, [
            np.array([0.7, 0.3]),
            np.array([0.8, 0.2]),
        ])
        entropies = [prior.entropy()] + [b.entropy() for b in trajectory]
        for i in range(1, len(entropies)):
            assert entropies[i] <= entropies[i - 1] + 1e-10

    def test_trajectory_length(self) -> None:
        """Trajectory length matches observation sequence length."""
        prior = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC],
            probabilities=np.array([0.5, 0.5]),
        )
        trajectory = sequential_belief_update(prior, [np.array([0.6, 0.4])] * 5)
        assert len(trajectory) == 5

    def test_empty_sequence(self) -> None:
        """Empty observation sequence returns empty trajectory."""
        prior = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC],
            probabilities=np.array([0.5, 0.5]),
        )
        assert sequential_belief_update(prior, []) == []

    def test_name_includes_step_index(self) -> None:
        """Trajectory beliefs are named with step index."""
        prior = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC],
            probabilities=np.array([0.5, 0.5]),
            name="prior",
        )
        trajectory = sequential_belief_update(prior, [np.array([0.6, 0.4])])
        assert trajectory[0].name == "prior_t1"
