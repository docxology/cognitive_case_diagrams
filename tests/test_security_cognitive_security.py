"""Tests for the cognitive security framework.

Validates type-violation detection, case frame validation, injection
scoring, topological robustness, and semantic integrity checking.
All tests use real computations — no mocks.
"""

import pytest
import numpy as np

from src.case_systems.case_category import CaseRole, standard_case_category
from src.enriched_cat.enriched import EnrichedCategory
from src.security.cognitive_security import (
    TypeViolation,
    CaseFrameValidator,
    detect_type_violation,
    injection_score,
    topological_robustness,
    semantic_integrity_check,
)


class TestTypeViolationDetection:
    """Tests for detect_type_violation function."""

    def test_valid_morphism_no_violation(self) -> None:
        """Existing morphism NOM→ACC is not a violation."""
        cat = standard_case_category()
        result = detect_type_violation(cat, CaseRole.NOM, CaseRole.ACC)
        assert result is None

    def test_identity_always_valid(self) -> None:
        """Identity morphism NOM→NOM is always valid."""
        cat = standard_case_category()
        result = detect_type_violation(cat, CaseRole.NOM, CaseRole.NOM)
        assert result is None

    def test_missing_morphism_detected(self) -> None:
        """Non-existent morphism ACC→NOM is a violation."""
        cat = standard_case_category()
        result = detect_type_violation(cat, CaseRole.ACC, CaseRole.NOM)
        assert result is not None
        assert result.violation_type == "missing_morphism"
        assert result.severity > 0

    def test_violation_has_description(self) -> None:
        """Violation includes human-readable description."""
        cat = standard_case_category()
        result = detect_type_violation(cat, CaseRole.VOC, CaseRole.INS)
        assert result is not None
        assert "VOC" in result.description
        assert "INS" in result.description


class TestCaseFrameValidator:
    """Tests for the CaseFrameValidator class."""

    def test_valid_assignment(self) -> None:
        """Well-typed assignment produces no violations."""
        validator = CaseFrameValidator()
        # NOM→ACC is a valid morphism
        assignments = {"Alice": CaseRole.NOM, "Bob": CaseRole.ACC}
        violations = validator.validate_assignment(assignments)
        assert len(violations) == 0

    def test_invalid_assignment_detected(self) -> None:
        """Ill-typed assignment produces violations."""
        validator = CaseFrameValidator()
        # VOC→INS has no morphism in either direction
        assignments = {"Alice": CaseRole.VOC, "Bob": CaseRole.INS}
        violations = validator.validate_assignment(assignments)
        assert len(violations) > 0

    def test_three_entity_validation(self) -> None:
        """Three-entity assignment checks all pairs."""
        validator = CaseFrameValidator()
        assignments = {
            "Alice": CaseRole.NOM,
            "Bob": CaseRole.ACC,
            "Carol": CaseRole.DAT,
        }
        violations = validator.validate_assignment(assignments)
        # NOM→ACC, NOM→DAT, ACC→DAT all exist
        assert len(violations) == 0


class TestInjectionScore:
    """Tests for injection severity scoring."""

    def test_no_violations_zero_score(self) -> None:
        """No violations → score of 0."""
        assert injection_score([]) == 0.0

    def test_single_high_severity(self) -> None:
        """Single high-severity violation."""
        violations = [TypeViolation(
            source=CaseRole.NOM, target=CaseRole.ACC,
            violation_type="test", severity=0.9, description="test",
        )]
        score = injection_score(violations)
        assert score == pytest.approx(0.9)

    def test_multiple_violations_average(self) -> None:
        """Multiple violations produce average severity."""
        violations = [
            TypeViolation(CaseRole.NOM, CaseRole.ACC, "test", 0.6, ""),
            TypeViolation(CaseRole.ACC, CaseRole.DAT, "test", 0.4, ""),
        ]
        score = injection_score(violations)
        assert score == pytest.approx(0.5)

    def test_score_capped_at_one(self) -> None:
        """Score is capped at 1.0."""
        violations = [
            TypeViolation(CaseRole.NOM, CaseRole.ACC, "test", 1.0, ""),
        ]
        assert injection_score(violations) <= 1.0


class TestTopologicalRobustness:
    """Tests for magnitude-based robustness measure."""

    def test_identity_matrix_max_robustness(self) -> None:
        """Identity proximity (all roles distinct) → robustness = 1."""
        ec = EnrichedCategory(
            name="distinct",
            roles=[CaseRole.NOM, CaseRole.ACC],
            proximity_matrix=np.eye(2),
        )
        rob = topological_robustness(ec)
        assert rob == pytest.approx(1.0)

    def test_high_overlap_low_robustness(self) -> None:
        """High overlap → magnitude < n → robustness < 1."""
        ec = EnrichedCategory(
            name="overlapping",
            roles=[CaseRole.NOM, CaseRole.ACC],
            proximity_matrix=np.array([[1.0, 0.9], [0.9, 1.0]]),
        )
        rob = topological_robustness(ec)
        assert rob < 1.0

    def test_robustness_positive(self) -> None:
        """Robustness is always positive for valid categories."""
        ec = EnrichedCategory(
            name="test",
            roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
            proximity_matrix=np.array([
                [1.0, 0.5, 0.3],
                [0.5, 1.0, 0.4],
                [0.3, 0.4, 1.0],
            ]),
        )
        assert topological_robustness(ec) > 0


class TestSemanticIntegrity:
    """Tests for composition inequality as security boundary."""

    def test_well_formed_category_few_violations(self) -> None:
        """Well-structured category has few composition violations."""
        ec = EnrichedCategory(
            name="test",
            roles=[CaseRole.NOM, CaseRole.ACC],
            proximity_matrix=np.array([[1.0, 0.5], [0.5, 1.0]]),
        )
        violations = semantic_integrity_check(ec)
        # 2 roles, no distinct triples possible
        assert len(violations) == 0

    def test_three_role_integrity(self) -> None:
        """Three-role category has integrity results."""
        ec = EnrichedCategory(
            name="test3",
            roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
            proximity_matrix=np.array([
                [1.0, 0.9, 0.1],
                [0.9, 1.0, 0.9],
                [0.1, 0.9, 1.0],
            ]),
        )
        violations = semantic_integrity_check(ec)
        # C(NOM,DAT)=0.1 < C(NOM,ACC)*C(ACC,DAT)=0.81 → violation
        assert len(violations) > 0
