"""Cognitive security framework for case-theoretic type checking.

Implements the formal characterization of prompt injection as
decidable categorical type violation (manuscript §9b).

The core insight: case frames impose categorical type constraints
on linguistic input. An adversarial prompt injection attempts to
insert an ill-typed case assignment that violates the categorical
composition rules. Detection of such violations is decidable
because type-checking in a finite category is decidable.

Key components:
    - CaseFrameValidator: type-checks case frames against categorical constraints
    - detect_type_violation(): identifies ill-typed case assignments
    - injection_score(): quantifies severity of case-frame injection
    - topological_robustness(): magnitude-based robustness measure
    - semantic_integrity_check(): validates enriched composition inequality

All computations use real methods — no mocks.
"""

import logging
from dataclasses import dataclass
from typing import Optional

import numpy as np

from ..case_systems.case_category import CaseRole, Morphism, CaseCategory, standard_case_category
from ..enriched_cat.enriched import EnrichedCategory

logger = logging.getLogger(__name__)


@dataclass
class TypeViolation:
    """Record of a detected categorical type violation.

    Attributes:
        source: Source case role of the violating morphism.
        target: Target case role of the violating morphism.
        violation_type: Category of violation (e.g., 'missing_morphism',
            'composition_violation', 'identity_violation').
        severity: Severity score in [0,1] (1.0 = critical).
        description: Human-readable description.
    """
    source: CaseRole
    target: CaseRole
    violation_type: str
    severity: float
    description: str


class CaseFrameValidator:
    """Validates case frames against categorical type constraints.

    A case frame assigns case roles to noun phrases in a sentence.
    This validator checks whether the assignment is well-typed with
    respect to the case category's morphism structure.

    Args:
        category: The case category defining legal morphisms.
        enriched: Optional enriched category for weight-based checks.
    """

    def __init__(
        self,
        category: Optional[CaseCategory] = None,
        enriched: Optional[EnrichedCategory] = None,
    ) -> None:
        """Initialize validator with a case category.

        Args:
            category: Case category (defaults to standard 8-case).
            enriched: Optional enriched category for weight checks.
        """
        self.category = category or standard_case_category()
        self.enriched = enriched
        self._valid_morphism_pairs = set()
        self._build_valid_pairs()
        logger.info(
            "CaseFrameValidator initialized: %d valid morphism pairs",
            len(self._valid_morphism_pairs),
        )

    def _build_valid_pairs(self) -> None:
        """Cache the set of valid (source, target) morphism pairs."""
        for m in self.category.morphisms:
            self._valid_morphism_pairs.add((m.source, m.target))
        # Identity morphisms are always valid
        for role in self.category.objects:
            self._valid_morphism_pairs.add((role, role))

    def validate_assignment(
        self,
        assignments: dict,
    ) -> list:
        """Validate a case frame assignment.

        Args:
            assignments: Dictionary mapping entity names to CaseRole.

        Returns:
            List of TypeViolation objects (empty if well-typed).
        """
        violations = []
        entities = list(assignments.keys())

        # Check that all assigned roles exist in the category
        for entity, role in assignments.items():
            if role not in self.category.objects:
                violations.append(TypeViolation(
                    source=role,
                    target=role,
                    violation_type="unknown_role",
                    severity=1.0,
                    description=f"Entity '{entity}' assigned unknown role {role.name}",
                ))

        # Check pairwise relational consistency
        for i, e1 in enumerate(entities):
            for e2 in entities[i + 1:]:
                r1 = assignments[e1]
                r2 = assignments[e2]
                if (r1, r2) not in self._valid_morphism_pairs and \
                   (r2, r1) not in self._valid_morphism_pairs:
                    violations.append(TypeViolation(
                        source=r1,
                        target=r2,
                        violation_type="missing_morphism",
                        severity=0.7,
                        description=(
                            f"No morphism {r1.name}→{r2.name} or "
                            f"{r2.name}→{r1.name} exists in category"
                        ),
                    ))

        logger.info(
            "Validated assignment of %d entities: %d violations",
            len(assignments), len(violations),
        )
        return violations


def detect_type_violation(
    category: CaseCategory,
    source: CaseRole,
    target: CaseRole,
) -> Optional[TypeViolation]:
    """Detect whether a proposed morphism violates categorical type constraints.

    This is the decidability result: type-checking in a finite category
    is decidable by enumerate-and-check.

    Args:
        category: Case category to check against.
        source: Proposed source role.
        target: Proposed target role.

    Returns:
        TypeViolation if ill-typed, None if well-typed.
    """
    # Identity morphisms are always well-typed
    if source == target:
        return None

    # Check if morphism exists
    for m in category.morphisms:
        if m.source == source and m.target == target:
            return None

    logger.warning(
        "Type violation detected: no morphism %s → %s",
        source.name, target.name,
    )
    return TypeViolation(
        source=source,
        target=target,
        violation_type="missing_morphism",
        severity=0.8,
        description=f"No morphism {source.name}→{target.name} in category",
    )


def injection_score(
    violations: list,
) -> float:
    """Compute aggregate injection severity score.

    Combines individual violation severities into a single score
    quantifying the overall severity of a potential case-frame injection.

    Args:
        violations: List of TypeViolation objects.

    Returns:
        Aggregate score in [0, 1] (0 = no injection, 1 = maximum severity).
    """
    if not violations:
        return 0.0

    # Weighted average of severities, capped at 1.0
    severities = [v.severity for v in violations]
    score = min(1.0, sum(severities) / len(severities))
    logger.info("Injection score: %.3f from %d violations", score, len(violations))
    return score


def topological_robustness(
    enriched: EnrichedCategory,
) -> float:
    """Compute magnitude-based topological robustness measure.

    Higher magnitude indicates more distinct relational structure,
    which provides more "surface area" for detecting type violations.

    Robustness R = |C| / n, where n = number of objects.
    R = 1.0 for maximally distinct roles (no overlap).
    R < 1.0 for systems with distributional redundancy.

    Args:
        enriched: Enriched category to measure.

    Returns:
        Robustness score in (0, 1].
    """
    n = len(enriched.roles)
    if n == 0:
        return 0.0

    mag = enriched.magnitude()
    robustness = mag / n
    logger.info(
        "Topological robustness: |C|/n = %.4f/%d = %.4f",
        mag, n, robustness,
    )
    return robustness


def semantic_integrity_check(
    enriched: EnrichedCategory,
) -> list:
    """Validate enriched composition inequality as a security boundary.

    Checks C(A,C) ≥ C(A,B) · C(B,C) for all triples.
    Violations indicate distributional inconsistencies that could
    be exploited by adversarial inputs.

    Args:
        enriched: Enriched category to check.

    Returns:
        List of (A, B, C) triples where the inequality is violated.
    """
    violations = []
    for a in enriched.roles:
        for b in enriched.roles:
            for c in enriched.roles:
                if a == b or b == c or a == c:
                    continue
                if not enriched.check_composition_inequality(a, b, c):
                    violations.append((a, b, c))

    logger.info(
        "Semantic integrity: %d/%d triples violate composition inequality",
        len(violations),
        len(enriched.roles) * (len(enriched.roles) - 1) * (len(enriched.roles) - 2),
    )
    return violations
