"""Case diagram belief distribution — §7 of the manuscript.

Represents the listener's current belief about who-does-what-to-whom
as a probability distribution over possible case role assignments.
"""

import logging
from dataclasses import dataclass

import numpy as np

from ..case_systems.case_category import CaseRole

logger = logging.getLogger(__name__)


@dataclass
class CaseDiagramBelief:
    """Probability distribution over case diagram assignments.

    Represents the listener's current belief about who-does-what-to-whom
    as a probability distribution over possible case role assignments.

    Attributes:
        roles: List of case roles in the distribution.
        probabilities: Array of probabilities (sums to 1.0).
        name: Optional label for this belief state.
    """
    roles: list[CaseRole]
    probabilities: np.ndarray
    name: str = "belief"

    def __post_init__(self) -> None:
        """Validate probability distribution."""
        self.probabilities = np.asarray(self.probabilities, dtype=np.float64)
        if len(self.roles) != len(self.probabilities):
            raise ValueError(
                f"roles ({len(self.roles)}) and probabilities "
                f"({len(self.probabilities)}) must have same length"
            )
        if not np.isclose(self.probabilities.sum(), 1.0):
            raise ValueError(
                f"probabilities must sum to 1.0, got {self.probabilities.sum():.6f}"
            )
        if np.any(self.probabilities < 0):
            raise ValueError("probabilities must be non-negative")
        logger.debug("CaseDiagramBelief '%s' created with %d roles", self.name, len(self.roles))

    def entropy(self) -> float:
        """Compute Shannon entropy of the belief distribution.

        H(q) = -∑ q_i log q_i

        Returns:
            Entropy in nats (natural log).
        """
        nonzero = self.probabilities[self.probabilities > 0]
        return float(-np.sum(nonzero * np.log(nonzero)))

    def most_likely_role(self) -> CaseRole:
        """Return the case role with highest probability.

        Returns:
            Most probable CaseRole.
        """
        idx = int(np.argmax(self.probabilities))
        return self.roles[idx]

    def probability_of(self, role: CaseRole) -> float:
        """Return probability of a specific case role.

        Args:
            role: Case role to query.

        Returns:
            Probability of the given role.

        Raises:
            ValueError: If role not in this distribution.
        """
        if role not in self.roles:
            raise ValueError(f"Role {role} not in belief distribution")
        idx = self.roles.index(role)
        return float(self.probabilities[idx])
