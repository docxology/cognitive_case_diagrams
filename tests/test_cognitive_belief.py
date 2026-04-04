"""Tests for the belief module — CaseDiagramBelief dataclass.

Tests the probability distribution over case role assignments,
including validation, entropy, and role queries.
All tests use real numpy computations — no mocks.
"""

import pytest
import numpy as np

from src.case_systems.case_category import CaseRole
from src.cognitive.belief import CaseDiagramBelief


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
        with pytest.raises(ValueError, match="sum to 1.0"):
            CaseDiagramBelief(
                roles=[CaseRole.NOM, CaseRole.ACC],
                probabilities=np.array([0.3, 0.3]),
            )

    def test_negative_probabilities_raise(self) -> None:
        """Negative probabilities raise ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            CaseDiagramBelief(
                roles=[CaseRole.NOM, CaseRole.ACC],
                probabilities=np.array([-0.5, 1.5]),
            )

    def test_length_mismatch_raises(self) -> None:
        """Mismatched roles and probabilities raise ValueError."""
        with pytest.raises(ValueError, match="same length"):
            CaseDiagramBelief(
                roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
                probabilities=np.array([0.5, 0.5]),
            )

    def test_entropy_uniform(self) -> None:
        """Uniform distribution has maximum entropy."""
        uniform = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
            probabilities=np.array([1/3, 1/3, 1/3]),
        )
        assert uniform.entropy() == pytest.approx(np.log(3), abs=1e-10)

    def test_entropy_deterministic(self) -> None:
        """Deterministic distribution has zero entropy."""
        determ = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC],
            probabilities=np.array([1.0, 0.0]),
        )
        assert determ.entropy() == pytest.approx(0.0)

    def test_most_likely_role(self) -> None:
        """Most likely role is the argmax."""
        belief = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
            probabilities=np.array([0.1, 0.7, 0.2]),
        )
        assert belief.most_likely_role() == CaseRole.ACC

    def test_probability_of(self) -> None:
        """Query probability of a specific role."""
        belief = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC],
            probabilities=np.array([0.4, 0.6]),
        )
        assert belief.probability_of(CaseRole.ACC) == pytest.approx(0.6)

    def test_probability_of_missing_role_raises(self) -> None:
        """Querying missing role raises ValueError."""
        belief = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC],
            probabilities=np.array([0.4, 0.6]),
        )
        with pytest.raises(ValueError):
            belief.probability_of(CaseRole.DAT)

    def test_name_default(self) -> None:
        """Default name is 'belief'."""
        belief = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC],
            probabilities=np.array([0.5, 0.5]),
        )
        assert belief.name == "belief"

    def test_custom_name(self) -> None:
        """Custom name is preserved."""
        belief = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ACC],
            probabilities=np.array([0.5, 0.5]),
            name="agent_prior",
        )
        assert belief.name == "agent_prior"
