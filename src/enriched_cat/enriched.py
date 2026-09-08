"""[0,1]-Enriched category theory for distributional measures of language.

Implements enriched categories where hom-values are real numbers in [0,1]
representing distributional proximity between case roles, following
Bradley, Terilla & Vlassopoulos (2021).

Key concepts:
    - Hom-values: C(A, B) ∈ [0,1] as distributional relatedness
    - Identity axiom: C(A, A) = 1
    - Composition inequality: C(A, C) >= C(A, B) · C(B, C)
    - Categorical magnitude: |C| = Σ_{i,j} (Z^{-1})_{ij}

References:
    Bradley et al. (2021) — An enriched category theory of language
    Bradley (2020) — Entropy as a topological operad derivation
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

import numpy as np

from ..case_systems.case_category import CaseRole

logger = logging.getLogger(__name__)


# Synthetic candidate similarities; not corpus estimates and not composition closed.
# Use composition_closure() explicitly before interpreting this as an enriched category.
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

    _z_matrix_cache: np.ndarray | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        """Validate the enriched category axioms after initialization."""
        self.proximity_matrix = np.asarray(self.proximity_matrix, dtype=np.float64).copy()
        if self.proximity_matrix.size > 0 or self.roles:
            self._validate()

    def _validate(self) -> None:
        """Validate enriched category axioms.

        Checks identity axiom (C(A,A)=1) and value bounds ([0,1]).
        The composition inequality C(A,C) ≥ C(A,B)·C(B,C) is NOT enforced
        here — call ``full_composition_check()`` explicitly on user-supplied
        corpus matrices to verify it before use.

        Raises:
            ValueError: If identity axiom or shape constraints are violated.
        """
        n = len(self.roles)
        if len(set(self.roles)) != n:
            raise ValueError("roles must be unique")
        if not np.all(np.isfinite(self.proximity_matrix)):
            raise ValueError("Hom-values must be finite")
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

    def _z_inverse(self) -> np.ndarray:
        """Return the (cached) inverse of the proximity matrix.

        Falls back to pseudo-inverse for singular or near-singular matrices,
        logging a warning. The result is cached for the lifetime of the instance.
        """
        self._validate()
        if (not hasattr(self, "_z_inv_cache") or self._z_matrix_cache is None
                or not np.array_equal(self.proximity_matrix, self._z_matrix_cache)):
            self._z_matrix_cache = self.proximity_matrix.copy()
            cond = np.linalg.cond(self.proximity_matrix)
            if cond > 1e12:
                logger.warning(
                    "Proximity matrix for %s is near-singular (cond=%.2e); "
                    "using pseudo-inverse — magnitude is approximate",
                    self.name, cond,
                )
                self._z_inv_cache: np.ndarray = np.linalg.pinv(self.proximity_matrix, rcond=1e-12)
            else:
                try:
                    self._z_inv_cache = np.linalg.inv(self.proximity_matrix)
                except np.linalg.LinAlgError:
                    logger.warning(
                        "Proximity matrix for %s is singular; "
                        "using pseudo-inverse — magnitude is approximate",
                        self.name,
                    )
                    self._z_inv_cache = np.linalg.pinv(self.proximity_matrix, rcond=1e-12)
        one = np.ones(len(self.roles))
        if (not np.allclose(self.proximity_matrix @ self._z_inv_cache @ one, one,
                            atol=1e-8, rtol=1e-8)
                or not np.allclose(one @ self._z_inv_cache @ self.proximity_matrix, one,
                                   atol=1e-8, rtol=1e-8)):
            raise ValueError("Magnitude undefined: no consistent weighting and coweighting")
        return self._z_inv_cache

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
        """Compute the weighting/coweighting sum for the supplied matrix.

Uses inverse sums when nonsingular and residual-checked pseudoinverse sums
otherwise. Raises if weighting equations cannot be satisfied numerically.
Interpretation as categorical magnitude requires an appropriate validated
similarity matrix; no generic information-theoretic interpretation is assumed.
"""
        z_inv = self._z_inverse()
        mag = float(np.sum(z_inv))
        logger.info("Categorical magnitude of %s: %.6f", self.name, mag)
        return mag

    def weighting(self) -> np.ndarray:
        """Compute the weighting vector w where Zw = 1.

        The solution of ``Z w = 1`` is ``Z^{-1} 1``, i.e. the ROW sums of
        ``Z^{-1}``. Weights need not be positive or represent empirical importance.
        Uses pseudo-inverse for singular matrices.

        Note: row and column sums coincide for symmetric hom-matrices, so the
        distinction only shows on asymmetric ones.
        """
        return np.sum(self._z_inverse(), axis=1)

    def coweighting(self) -> np.ndarray:
        """Compute the coweighting vector v where vZ = 1.

        The solution of ``v Z = 1`` is ``1^T Z^{-1}``, i.e. the COLUMN sums of
        ``Z^{-1}``. Uses pseudo-inverse for singular matrices.
        """
        return np.sum(self._z_inverse(), axis=0)

    def magnitude_deficit(self) -> float:
        """Return the signed statistic n - magnitude.

This is not automatically information loss, redundancy, or a security bound.
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

        total = len(holds) + len(violations)
        violation_rate = len(violations) / max(1, total)
        result = {
            "holds": holds,
            "violations": violations,
            "total": total,
            "violation_rate": violation_rate,
        }
        logger.info(
            "Composition check: %d/%d violations (%.1f%%)",
            len(violations), total, violation_rate * 100,
        )
        return result

    def role_clusters(self, threshold: float = 0.6) -> list:
        """Identify clusters of highly related case roles.

        Groups roles that share hom-values above the threshold,
        revealing the distributional structure of the case system.

        Args:
            threshold: Minimum hom-value to consider roles as clustered.

        Returns:
            Weakly connected components; pairs within a component need not all be close.
        """
        if not 0. <= threshold <= 1.:
            raise ValueError("threshold must be in [0,1]")
        n = len(self.roles)
        # Weakly connected components: either directed proximity passes threshold.
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
                    if max(self.proximity_matrix[current, j], self.proximity_matrix[j, current]) >= threshold:
                        cluster.add(self.roles[j])
                        visited[j] = True
                        queue.append(j)
            clusters.append(cluster)

        logger.info(
            "Found %d role clusters at threshold %.2f",
            len(clusters), threshold,
        )
        return clusters

    def composition_closure(self) -> EnrichedCategory:
        """Return the least entrywise majorant closed under max-product paths.

        Floyd-Warshall over the max-product semiring. This is a mathematical
        projection of the supplied matrix, not an empirical calibration.
        """
        self._validate()
        z = self.proximity_matrix.copy()
        for k in range(len(self.roles)):
            z = np.maximum(z, z[:, k, None] * z[None, k, :])
        return EnrichedCategory(f"{self.name}_closure", list(self.roles), z)


def standard_enriched_category() -> EnrichedCategory:
    """Create the standard 8-case enriched category.

    Uses a hand-chosen illustrative matrix, not corpus measurements.
    This candidate matrix is not composition-closed; inspect
    ``full_composition_check()`` or explicitly call ``composition_closure()``.
    """
    return EnrichedCategory(
        name="Standard8CaseEnriched",
        roles=list(STANDARD_ROLES),
        proximity_matrix=STANDARD_PROXIMITY_MATRIX.copy(),
    )

