"""[0,1]-Enriched category theory for distributional measures of language.

Implements enriched categories where hom-values are real numbers in [0,1]
representing distributional proximity between case roles, following
Bradley, Terilla & Weyhrich (2021).

Key concepts:
    - Hom-values: C(A, B) ∈ [0,1] as distributional relatedness
    - Identity axiom: C(A, A) = 1
    - Composition inequality: C(A, C) >= C(A, B) · C(B, C)
    - Categorical magnitude: |C| = Σ_{i,j} (Z^{-1})_{ij}

References:
    Bradley et al. (2021) — An enriched category theory of language
    Bradley (2020) — Entropy as a topological operad derivation
"""

import logging
from dataclasses import dataclass, field

import numpy as np

from ..case_systems.case_category import CaseRole

logger = logging.getLogger(__name__)


# Standard 8-case proximity matrix (empirically motivated)
# Rows/columns: NOM, ACC, GEN, DAT, INS, LOC, ABL, VOC
STANDARD_ROLES = [
    CaseRole.NOM, CaseRole.ACC, CaseRole.GEN, CaseRole.DAT,
    CaseRole.INS, CaseRole.LOC, CaseRole.ABL, CaseRole.VOC,
]

STANDARD_PROXIMITY_MATRIX = np.array([
    # NOM   ACC   GEN   DAT   INS   LOC   ABL   VOC
    [1.00, 0.85, 0.60, 0.45, 0.35, 0.25, 0.20, 0.70],  # NOM
    [0.85, 1.00, 0.50, 0.55, 0.40, 0.30, 0.25, 0.40],  # ACC
    [0.60, 0.50, 1.00, 0.45, 0.30, 0.35, 0.40, 0.25],  # GEN
    [0.45, 0.55, 0.45, 1.00, 0.50, 0.40, 0.35, 0.30],  # DAT
    [0.35, 0.40, 0.30, 0.50, 1.00, 0.55, 0.50, 0.20],  # INS
    [0.25, 0.30, 0.35, 0.40, 0.55, 1.00, 0.65, 0.15],  # LOC
    [0.20, 0.25, 0.40, 0.35, 0.50, 0.65, 1.00, 0.15],  # ABL
    [0.70, 0.40, 0.25, 0.30, 0.20, 0.15, 0.15, 1.00],  # VOC
])


@dataclass
class EnrichedCategory:
    """A [0,1]-enriched category of case roles.

    Each pair of objects (case roles) has a hom-value in [0,1] representing
    distributional proximity. Composition is multiplicative (monoidal
    structure on [0,1] with product as tensor).

    Attributes:
        name: Name of the enriched category.
        roles: Ordered list of case roles (objects).
        proximity_matrix: n×n matrix of hom-values.
    """

    name: str
    roles: list[CaseRole] = field(default_factory=list)
    proximity_matrix: np.ndarray = field(default_factory=lambda: np.array([]))

    def __post_init__(self) -> None:
        """Validate the enriched category axioms after initialization."""
        if self.proximity_matrix.size > 0:
            self._validate()

    def _validate(self) -> None:
        """Validate enriched category axioms.

        Raises:
            ValueError: If identity axiom or shape constraints are violated.
        """
        n = len(self.roles)
        if self.proximity_matrix.shape != (n, n):
            raise ValueError(
                f"Proximity matrix shape {self.proximity_matrix.shape} "
                f"does not match {n} roles"
            ) from None

        # Identity axiom: C(A, A) = 1
        for i in range(n):
            if not np.isclose(self.proximity_matrix[i, i], 1.0):
                raise ValueError(
                    f"Identity axiom violated for {self.roles[i].name}: "
                    f"C({self.roles[i].name}, {self.roles[i].name}) = "
                    f"{self.proximity_matrix[i, i]} != 1.0"
                ) from None

        # All values in [0, 1]
        if np.any(self.proximity_matrix < 0) or np.any(self.proximity_matrix > 1):
            raise ValueError("Hom-values must be in [0, 1]") from None

        logger.info(
            "Validated enriched category %s with %d roles", self.name, n
        )

    def hom(self, source: CaseRole, target: CaseRole) -> float:
        """Return the hom-value (distributional proximity) between two roles.

        Args:
            source: Source case role.
            target: Target case role.

        Returns:
            Proximity value in [0, 1].

        Raises:
            ValueError: If either role is not in the category.
        """
        try:
            i = self.roles.index(source)
            j = self.roles.index(target)
        except ValueError as exc:
            raise ValueError(
                f"Role not in category: {source.name} or {target.name}"
            ) from exc
        return float(self.proximity_matrix[i, j])

    def check_composition_inequality(
        self, a: CaseRole, b: CaseRole, c: CaseRole
    ) -> bool:
        """Check the composition inequality: C(A,C) >= C(A,B) · C(B,C).

        This is the enriched analogue of composition existing in ordinary
        categories. When it holds, the indirect path through B is "no
        shorter" than the direct path A→C.

        Returns:
            True if the inequality holds, False otherwise.
        """
        cab = self.hom(a, c)
        product = self.hom(a, b) * self.hom(b, c)
        holds = cab >= product - 1e-10  # numerical tolerance
        if not holds:
            logger.warning(
                "Composition inequality fails: C(%s,%s)=%.4f < C(%s,%s)·C(%s,%s)=%.4f",
                a.name, c.name, cab, a.name, b.name, b.name, c.name, product,
            )
        return holds

    def magnitude(self) -> float:
        """Compute the categorical magnitude |C| = Σ_{i,j} (Z^{-1})_{ij}.

        Categorical magnitude is an information-theoretic invariant that
        quantifies the "effective size" of the case system — how much
        distributional information the category encodes.

        Returns:
            The magnitude as a scalar.

        Raises:
            np.linalg.LinAlgError: If proximity matrix is singular.
        """
        try:
            z_inv = np.linalg.inv(self.proximity_matrix)
            mag = float(np.sum(z_inv))
            logger.info("Categorical magnitude of %s: %.6f", self.name, mag)
            return mag
        except np.linalg.LinAlgError:
            logger.error("Proximity matrix for %s is singular", self.name)
            raise

    def weighting(self) -> np.ndarray:
        """Compute the weighting vector w where Zw = 1.

        Returns column sums of Z^{-1}, representing the "importance"
        of each role in the category.

        Raises:
            numpy.linalg.LinAlgError: If the proximity matrix is singular
                (i.e., roles are not linearly independent).
        """
        z_inv = np.linalg.inv(self.proximity_matrix)
        return np.sum(z_inv, axis=0)

    def coweighting(self) -> np.ndarray:
        """Compute the coweighting vector v where vZ = 1.

        Returns row sums of Z^{-1}.

        Raises:
            numpy.linalg.LinAlgError: If the proximity matrix is singular
                (i.e., roles are not linearly independent).
        """
        z_inv = np.linalg.inv(self.proximity_matrix)
        return np.sum(z_inv, axis=1)

    def magnitude_deficit(self) -> float:
        """Compute the magnitude deficit: n - |C|.

        The deficit quantifies information lost by distributional overlap.
        A deficit of 0 means all roles are maximally distinct;
        a large deficit means significant redundancy.

        Returns:
            Non-negative deficit value.
        """
        n = len(self.roles)
        deficit = n - self.magnitude()
        logger.info("Magnitude deficit for %s: %.4f", self.name, deficit)
        return deficit

    def full_composition_check(self) -> dict:
        """Check composition inequality for all triples.

        Returns:
            Dictionary with 'holds' (list of passing triples),
            'violations' (list of failing triples), and 'total' count.
        """
        holds = []
        violations = []
        for a in self.roles:
            for b in self.roles:
                for c in self.roles:
                    if a == b or b == c or a == c:
                        continue
                    if self.check_composition_inequality(a, b, c):
                        holds.append((a, b, c))
                    else:
                        violations.append((a, b, c))

        result = {
            "holds": holds,
            "violations": violations,
            "total": len(holds) + len(violations),
            "violation_rate": len(violations) / max(1, len(holds) + len(violations)),
        }
        logger.info(
            "Composition check: %d/%d violations (%.1f%%)",
            len(violations), result["total"], result["violation_rate"] * 100,
        )
        return result

    def role_clusters(self, threshold: float = 0.6) -> list:
        """Identify clusters of highly related case roles.

        Groups roles that share hom-values above the threshold,
        revealing the distributional structure of the case system.

        Args:
            threshold: Minimum hom-value to consider roles as clustered.

        Returns:
            List of sets, each containing mutually close roles.
        """
        n = len(self.roles)
        # Build adjacency based on threshold
        visited = [False] * n
        clusters = []

        for i in range(n):
            if visited[i]:
                continue
            cluster = {self.roles[i]}
            visited[i] = True
            queue = [i]
            while queue:
                current = queue.pop(0)
                for j in range(n):
                    if visited[j]:
                        continue
                    if self.proximity_matrix[current, j] >= threshold:
                        cluster.add(self.roles[j])
                        visited[j] = True
                        queue.append(j)
            clusters.append(cluster)

        logger.info(
            "Found %d role clusters at threshold %.2f",
            len(clusters), threshold,
        )
        return clusters


def standard_enriched_category() -> EnrichedCategory:
    """Create the standard 8-case enriched category.

    Uses the empirically motivated proximity matrix from the manuscript.
    """
    return EnrichedCategory(
        name="Standard8CaseEnriched",
        roles=list(STANDARD_ROLES),
        proximity_matrix=STANDARD_PROXIMITY_MATRIX.copy(),
    )

