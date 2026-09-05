"""Tests for cognitive_security module: topological_robustness,
semantic_integrity_check, and the unknown-role violation path.
No mocks — real computations only.
"""

from src.case_systems.case_category import CaseRole, minimal_case_category
from src.enriched_cat.enriched import standard_enriched_category
from src.security.cognitive_security import (
    CaseFrameValidator,
    topological_robustness,
    semantic_integrity_check,
)


class TestTopologicalRobustness:
    def test_returns_float(self):
        ec = standard_enriched_category()
        r = topological_robustness(ec)
        assert isinstance(r, float)

    def test_robustness_finite(self):
        import math
        ec = standard_enriched_category()
        assert math.isfinite(topological_robustness(ec))

    def test_robustness_positive(self):
        ec = standard_enriched_category()
        assert topological_robustness(ec) > 0.0

    def test_robustness_at_most_one_for_standard(self):
        """Standard 8-case enriched category has some role overlap → R ≤ 1."""
        ec = standard_enriched_category()
        assert topological_robustness(ec) <= 1.0 + 1e-9

    def test_robustness_equals_magnitude_over_n(self):
        ec = standard_enriched_category()
        n = len(ec.roles)
        expected = ec.magnitude() / n
        assert abs(topological_robustness(ec) - expected) < 1e-9


class TestSemanticIntegrityCheck:
    def test_returns_list(self):
        ec = standard_enriched_category()
        result = semantic_integrity_check(ec)
        assert isinstance(result, list)

    def test_standard_category_returns_list(self):
        """semantic_integrity_check completes on standard category returning a list."""
        ec = standard_enriched_category()
        violations = semantic_integrity_check(ec)
        assert isinstance(violations, list)

    def test_violations_are_triples(self):
        """Each violation entry is a 3-tuple of CaseRole."""
        from src.case_systems.case_category import CaseRole
        import numpy as np
        from src.enriched_cat.enriched import EnrichedCategory

        # Construct a matrix that intentionally violates composition inequality
        # C(A,C) < C(A,B) * C(B,C): set C(NOM,GEN)=0.1 but C(NOM,ACC)*C(ACC,GEN)=0.6*0.5=0.3
        roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.GEN]
        mat = np.array([
            [1.0, 0.6, 0.1],
            [0.6, 1.0, 0.5],
            [0.1, 0.5, 1.0],
        ])
        ec = EnrichedCategory(name="ViolatingCat", roles=roles, proximity_matrix=mat)
        violations = semantic_integrity_check(ec)
        assert len(violations) > 0
        for v in violations:
            assert len(v) == 3
            for role in v:
                assert isinstance(role, CaseRole)


class TestUnknownRoleViolationPath:
    def test_unknown_role_detected(self):
        """Role not in category.objects triggers 'unknown_role' violation."""
        # Use minimal_case_category (only NOM, ACC, S/A/P subset)
        cat = minimal_case_category()
        validator = CaseFrameValidator(category=cat)

        # ABL is a valid CaseRole but not in minimal_case_category
        assignments = {"Alice": CaseRole.NOM, "book": CaseRole.ABL}
        violations = validator.validate_assignment(assignments)

        unknown = [v for v in violations if v.violation_type == "unknown_role"]
        assert len(unknown) >= 1

    def test_valid_roles_no_unknown_violation(self):
        cat = minimal_case_category()
        validator = CaseFrameValidator(category=cat)
        # Use only roles that are in minimal_case_category
        assignments = {"Alice": CaseRole.NOM, "Bob": CaseRole.ACC}
        violations = validator.validate_assignment(assignments)
        unknown = [v for v in violations if v.violation_type == "unknown_role"]
        assert len(unknown) == 0
