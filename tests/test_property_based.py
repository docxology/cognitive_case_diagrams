"""Property-based tests for categorical axioms using Hypothesis.

Verifies that categorical axioms hold for randomly generated inputs,
complementing the hand-crafted examples in other test files.

All tests use real mathematical computations — no mocks.
"""

import math

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from src.case_systems.case_category import (
    CaseCategory,
    CaseRole,
    minimal_case_category,
    standard_case_category,
)
from src.cognitive.belief import CaseDiagramBelief
from src.cognitive.free_energy import kl_divergence
from src.daif.prediction import distributional_prediction_error
from src.enriched_cat.enriched import EnrichedCategory
from src.quantum.quantum_case import (
    case_probability,
    crisp_case_povm,
    semantic_state,
)
from src.security.cognitive_security import (
    TypeViolation,
    detect_type_violation,
    injection_score,
)


# --- Strategies ---

# Pick from a subset of roles to keep categories small
ROLE_POOL = [CaseRole.NOM, CaseRole.ACC, CaseRole.GEN, CaseRole.DAT, CaseRole.INS]

role_strategy = st.sampled_from(ROLE_POOL)
weight_strategy = st.floats(min_value=0.01, max_value=1.0, allow_nan=False)


@st.composite
def enriched_proximity_matrix(draw, n: int = 3):
    """Generate a valid [0,1]-enriched proximity matrix of size n."""
    roles = draw(st.just(ROLE_POOL[:n]))
    # Start with identity
    matrix = np.eye(n)
    # Fill off-diagonal with [0,1] values
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i, j] = draw(
                    st.floats(min_value=0.01, max_value=0.99, allow_nan=False)
                )
    return roles, matrix


# --- CaseCategory Axiom Tests ---


class TestCaseCategoryAxioms:
    """Property-based tests for categorical axioms."""


    def test_identity_left_unit(self) -> None:
        """id_A ; f = f for every morphism f of the minimal category.

        Deterministic and exhaustive: the composable space is tiny, so the
        previous hypothesis-sampled version skipped most examples (the
        sampled pair rarely landed on a composable morphism), making the
        property vacuous in practice.
        """
        cat = minimal_case_category()
        for f in cat.morphisms:
            id_a = cat.identity(f.source)
            result = cat.compose(id_a, f)
            assert result.source == f.source
            assert result.target == f.target
            assert math.isclose(result.weight, f.weight, rel_tol=1e-9)

    def test_identity_right_unit(self) -> None:
        """f ; id_B = f for every morphism f of the minimal category."""
        cat = minimal_case_category()
        for f in cat.morphisms:
            id_b = cat.identity(f.target)
            result = cat.compose(f, id_b)
            assert result.source == f.source
            assert result.target == f.target
            assert math.isclose(result.weight, f.weight, rel_tol=1e-9)


class TestEmptyMorphismCategory:
    """Edge case: category with objects but zero morphisms."""

    def test_discrete_category_well_formed(self):
        """A category with objects and only identity morphisms is well-formed."""
        cat = CaseCategory(name="Discrete")
        for role in [CaseRole.NOM, CaseRole.ACC, CaseRole.GEN]:
            cat.add_role(role)
        # No explicit morphisms — only identities
        assert cat.is_well_formed()

    def test_discrete_category_associativity(self):
        """Associativity trivially holds with zero non-identity morphisms."""
        cat = CaseCategory(name="Discrete")
        for role in [CaseRole.NOM, CaseRole.ACC]:
            cat.add_role(role)
        assert cat.associativity_holds()

    def test_discrete_category_get_morphisms_empty(self):
        """No morphisms from any role (only identities, not in morphisms list)."""
        cat = CaseCategory(name="Discrete")
        cat.add_role(CaseRole.NOM)
        assert cat.get_morphisms_from(CaseRole.NOM) == []

    def test_empty_category(self):
        """A category with no objects or morphisms is technically well-formed."""
        cat = CaseCategory(name="Empty")
        assert cat.is_well_formed()


# --- EnrichedCategory Axiom Tests ---


class TestEnrichedCategoryAxioms:
    """Property-based tests for enriched category axioms."""

    @given(enriched_proximity_matrix(n=3))
    @settings(max_examples=30)
    def test_non_unit_diagonal_raises(self, roles_matrix):
        """The real identity-axiom contract: a non-unit diagonal is rejected.

        (The previous version asserted the unit diagonal the strategy had
        already hardcoded, so it could never fail.)
        """
        roles, _ = roles_matrix
        bad = np.eye(3)
        bad[0, 0] = 0.5
        with pytest.raises(ValueError, match="Identity axiom"):
            EnrichedCategory(name="Bad3", roles=list(roles), proximity_matrix=bad)

    @given(enriched_proximity_matrix(n=3))
    @settings(max_examples=30)
    def test_magnitude_is_finite(self, roles_matrix):
        """Categorical magnitude is always finite for valid enriched categories."""
        roles, matrix = roles_matrix
        cat = EnrichedCategory(
            name="Random3",
            roles=list(roles),
            proximity_matrix=matrix,
        )
        mag = cat.magnitude()
        assert np.isfinite(mag)

    @given(enriched_proximity_matrix(n=3))
    @settings(max_examples=30)
    def test_weighting_sums_to_magnitude(self, roles_matrix):
        """Weighting vector sums to magnitude for random categories."""
        roles, matrix = roles_matrix
        cat = EnrichedCategory(
            name="Random3",
            roles=list(roles),
            proximity_matrix=matrix,
        )
        w = cat.weighting()
        assert np.isclose(np.sum(w), cat.magnitude(), rtol=1e-6)

    @given(enriched_proximity_matrix(n=3))
    @settings(max_examples=30, deadline=None)
    def test_magnitude_plus_deficit_equals_cardinality(self, roles_matrix):
        """Definitional identity: |C| + (n - |C|) == n for every sample."""
        roles, matrix = roles_matrix
        cat = EnrichedCategory(
            name="Random3",
            roles=list(roles),
            proximity_matrix=matrix,
        )
        mag = cat.magnitude()
        deficit = cat.magnitude_deficit()
        assert np.isfinite(mag)
        assert np.isfinite(deficit)
        assert np.isclose(mag + deficit, len(roles), rtol=1e-9, atol=1e-9)


class TestEnrichedWeightingDefiningEquation:
    """The weighting must satisfy its defining equation Z w = 1 (§5)."""

    @given(enriched_proximity_matrix(n=3))
    @settings(max_examples=30, deadline=None)
    def test_weighting_solves_defining_equation(self, roles_matrix):
        """Z @ w == 1 exactly (up to numerical tolerance)."""
        roles, matrix = roles_matrix
        cat = EnrichedCategory(
            name="Random3",
            roles=list(roles),
            proximity_matrix=matrix,
        )
        w = cat.weighting()
        np.testing.assert_allclose(matrix @ w, np.ones(3), rtol=1e-6, atol=1e-8)


class TestEnrichedCompositionInequality:
    """Property tests for the enriched composition inequality (§5)."""

    @given(enriched_proximity_matrix(n=3))
    @settings(max_examples=30, deadline=None)
    def test_inequality_holds_on_w_composition_closure(self, roles_matrix):
        """Closure under w-composition makes the inequality hold by
        construction: full_composition_check must report zero violations."""
        roles, matrix = roles_matrix
        closed = matrix.copy()
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if i == j or j == k:
                        continue
                    closed[i, k] = max(closed[i, k], closed[i, j] * closed[j, k])
        cat = EnrichedCategory(
            name="Closed3",
            roles=list(roles),
            proximity_matrix=closed,
        )
        result = cat.full_composition_check()
        assert result["violations"] == []
        assert result["total"] == 6  # ordered triples of 3 distinct roles


class TestDaifProperties:
    """Property tests for the DAIF subpackage (§7c)."""

    @given(
        st.lists(
            st.floats(min_value=0.001, max_value=1.0, allow_nan=False),
            min_size=2,
            max_size=8,
        )
    )
    @settings(max_examples=30, deadline=None)
    def test_distributional_prediction_error_non_negative(self, raw):
        """DPE-scalar is a positive weight times −log q, hence ≥ 0."""
        probabilities = np.asarray(raw) / np.sum(raw)
        belief = CaseDiagramBelief(
            roles=[CaseRole.NOM] * len(probabilities),
            probabilities=probabilities,
        )
        dpe = distributional_prediction_error(belief, 0, enriched_weight=0.7)
        assert np.isfinite(dpe)
        assert dpe >= 0.0


class TestQuantumProperties:
    """Property tests for the quantum POVM module (§8)."""

    @given(enriched_proximity_matrix(n=3))
    @settings(max_examples=15, deadline=None)
    def test_case_probability_bounded(self, roles_matrix):
        """P(c|ρ) ∈ [0,1] for a valid density matrix and POVM element."""
        roles, matrix = roles_matrix
        povm = crisp_case_povm(list(roles))
        row = matrix[0]
        density = semantic_state({role: float(w) for role, w in zip(roles, row)})
        for element in povm.elements.values():
            prob = case_probability(povm_element=element, density_matrix=density)
            assert -1e-9 <= prob <= 1.0 + 1e-9


class TestCognitiveProperties:
    """Property tests for scalar active inference (§7)."""

    @given(
        st.lists(
            st.floats(min_value=0.001, max_value=1.0, allow_nan=False),
            min_size=2,
            max_size=6,
        ),
        st.floats(min_value=0.001, max_value=1.0, allow_nan=False),
    )
    @settings(max_examples=30, deadline=None)
    def test_kl_divergence_non_negative(self, raw_q, eps):
        """KL(q || p) ≥ 0 for any two distributions (Gibbs' inequality)."""
        q = np.asarray(raw_q) / np.sum(raw_q)
        p = np.roll(q, 1) * (1.0 - eps) + eps / len(q)
        p = p / p.sum()
        kl = kl_divergence(q, p)
        assert np.isfinite(kl)
        assert kl >= -1e-9


class TestSecurityProperties:
    """Property tests for cognitive security (§9b)."""

    @given(role_strategy, weight_strategy, weight_strategy)
    @settings(max_examples=30, deadline=None)
    def test_injection_score_is_max_severity(self, role, sev_a, sev_b):
        """Aggregate score equals the max individual severity."""
        v_a = TypeViolation(source=role, target=role, violation_type="t",
                            severity=sev_a, description="a")
        v_b = TypeViolation(source=role, target=role, violation_type="t",
                            severity=sev_b, description="b")
        assert injection_score([v_a, v_b]) == pytest.approx(max(sev_a, sev_b))

    @given(role_strategy)
    @settings(max_examples=15, deadline=None)
    def test_identity_morphism_never_violates(self, role):
        """Identity morphisms are always well-typed."""
        cat = standard_case_category()
        assert detect_type_violation(cat, role, role) is None
