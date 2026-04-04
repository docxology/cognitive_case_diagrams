"""Tests for previously uncovered methods in enriched.py and case_category.py.

Targets the specific methods that were missing coverage:
    - EnrichedCategory: weighting, coweighting, magnitude_deficit, 
      full_composition_check, role_clusters, standard_enriched_category
    - CaseCategory: associativity_holds, is_well_formed, minimal_case_category,
      accusative/ergative/tripartite/active_stative alignment functions

All tests use real mathematical computations — no mocks.
"""

import pytest
import numpy as np

from src.case_systems.case_category import (
    CaseRole, CaseCategory, Morphism,
    standard_case_category, minimal_case_category,
    accusative_alignment, ergative_alignment,
    tripartite_alignment, active_stative_alignment,
)
from src.enriched_cat.enriched import (
    EnrichedCategory,
    standard_enriched_category,
    STANDARD_ROLES,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _small_ec(roles=None, prox=None) -> EnrichedCategory:
    """Create a small 2- or 3-role enriched category for testing."""
    roles = roles or [CaseRole.NOM, CaseRole.ACC]
    n = len(roles)
    prox = prox if prox is not None else np.eye(n)
    return EnrichedCategory(name="test", roles=roles, proximity_matrix=prox)


def _three_role_ec(vals=(0.5, 0.3, 0.4)) -> EnrichedCategory:
    """Create a 3-role enriched category (NOM, ACC, DAT) with off-diagonal values."""
    a, b, c_ = vals
    prox = np.array([
        [1.0, a, b],
        [a, 1.0, c_],
        [b, c_, 1.0],
    ])
    return EnrichedCategory(
        name="three_role",
        roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
        proximity_matrix=prox,
    )


# ---------------------------------------------------------------------------
# EnrichedCategory: previously uncovered methods
# ---------------------------------------------------------------------------

class TestEnrichedCategoryWeighting:
    """Tests for weighting() and coweighting() methods."""

    def test_weighting_returns_ndarray(self) -> None:
        """weighting() returns a numpy array of length n."""
        ec = _small_ec()
        w = ec.weighting()
        assert isinstance(w, np.ndarray)
        assert len(w) == 2

    def test_weighting_identity_matrix_is_ones(self) -> None:
        """Identity proximity → Z = I → Z^{-1} = I → weighting = [1,1,...,1]."""
        roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
        ec = EnrichedCategory(name="identity", roles=roles, proximity_matrix=np.eye(3))
        w = ec.weighting()
        assert np.allclose(w, np.ones(3))

    def test_coweighting_returns_ndarray(self) -> None:
        """coweighting() returns a numpy array of length n."""
        ec = _small_ec()
        v = ec.coweighting()
        assert isinstance(v, np.ndarray)
        assert len(v) == 2

    def test_coweighting_identity_matrix_is_ones(self) -> None:
        """Identity proximity → coweighting = [1,1,...,1]."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        ec = EnrichedCategory(name="identity2", roles=roles, proximity_matrix=np.eye(2))
        v = ec.coweighting()
        assert np.allclose(v, np.ones(2))

    def test_weighting_sum_equals_magnitude(self) -> None:
        """Sum of weighting = categorical magnitude (both are sum of Z^{-1} entries)."""
        ec = _three_role_ec()
        w = ec.weighting()
        mag = ec.magnitude()
        assert np.sum(w) == pytest.approx(mag, abs=1e-8)

    def test_coweighting_symmetric_matrix_matches_weighting(self) -> None:
        """For symmetric proximity, weighting == coweighting."""
        ec = _three_role_ec()
        w = ec.weighting()
        v = ec.coweighting()
        # Symmetric Z → Z^{-1} also symmetric → row sums == column sums
        assert np.allclose(w, v, atol=1e-10)


class TestEnrichedCategoryMagnitudeDeficit:
    """Tests for magnitude_deficit()."""

    def test_identity_matrix_zero_deficit(self) -> None:
        """Identity proximity → magnitude = n → deficit = 0."""
        roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
        ec = EnrichedCategory(name="id3", roles=roles, proximity_matrix=np.eye(3))
        deficit = ec.magnitude_deficit()
        assert deficit == pytest.approx(0.0, abs=1e-8)

    def test_overlapping_matrix_positive_deficit(self) -> None:
        """Off-diagonal proximity < 1 → magnitude < n → deficit > 0."""
        ec = _three_role_ec()
        deficit = ec.magnitude_deficit()
        assert deficit > 0

    def test_deficit_nonnegative(self) -> None:
        """Deficit should be non-negative for valid proximity matrices."""
        ec = _three_role_ec()
        assert ec.magnitude_deficit() >= 0


class TestFullCompositionCheck:
    """Tests for full_composition_check()."""

    def test_two_role_no_distinct_triples(self) -> None:
        """2-role category has no distinct triples → empty holds/violations."""
        ec = _small_ec()
        result = ec.full_composition_check()
        assert result["total"] == 0
        assert result["holds"] == []
        assert result["violations"] == []

    def test_three_role_result_structure(self) -> None:
        """Result has correct keys and types."""
        ec = _three_role_ec()
        result = ec.full_composition_check()
        assert "holds" in result
        assert "violations" in result
        assert "total" in result
        assert "violation_rate" in result
        assert isinstance(result["holds"], list)
        assert isinstance(result["violations"], list)

    def test_three_role_total_matches_distinct_triples(self) -> None:
        """3 roles → 3 × 2 × 1 = 6 distinct ordered triples (a≠b≠c≠a)."""
        ec = _three_role_ec()
        result = ec.full_composition_check()
        assert result["total"] == 6

    def test_well_structured_category_few_violations(self) -> None:
        """Well-structured proximity satisfies most composition inequalities."""
        # Near-identity: very low off-diagonals → strict triangle inequality
        prox = np.array([[1.0, 0.1, 0.1], [0.1, 1.0, 0.1], [0.1, 0.1, 1.0]])
        ec = EnrichedCategory(
            name="well_structured",
            roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
            proximity_matrix=prox,
        )
        result = ec.full_composition_check()
        assert result["violation_rate"] <= 0.5


class TestRoleClusters:
    """Tests for role_clusters()."""

    def test_identity_matrix_all_singletons(self) -> None:
        """Identity proximity (all pairs exactly 0 off-diagonal) → each role alone."""
        # Need off-diagonals < threshold; identity has 0s off-diagonal
        roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
        ec = EnrichedCategory(name="id3", roles=roles, proximity_matrix=np.eye(3))
        clusters = ec.role_clusters(threshold=0.5)
        # With off-diagonal = 0 < 0.5, each role is its own cluster
        assert len(clusters) == 3

    def test_high_overlap_single_cluster(self) -> None:
        """High proximity (all off-diag > threshold) → single cluster."""
        prox = np.array([[1.0, 0.9, 0.9], [0.9, 1.0, 0.9], [0.9, 0.9, 1.0]])
        ec = EnrichedCategory(
            name="high_overlap",
            roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
            proximity_matrix=prox,
        )
        clusters = ec.role_clusters(threshold=0.8)
        assert len(clusters) == 1

    def test_mixed_clustering(self) -> None:
        """NOM/ACC close, DAT distant → 2 clusters."""
        prox = np.array([
            [1.0, 0.9, 0.1],  # NOM close to ACC, distant from DAT
            [0.9, 1.0, 0.1],  # ACC close to NOM, distant from DAT
            [0.1, 0.1, 1.0],  # DAT distant from both
        ])
        ec = EnrichedCategory(
            name="mixed",
            roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
            proximity_matrix=prox,
        )
        clusters = ec.role_clusters(threshold=0.7)
        assert len(clusters) == 2

    def test_default_threshold(self) -> None:
        """Default threshold of 0.6 returns a list of sets."""
        ec = standard_enriched_category()
        clusters = ec.role_clusters()
        assert isinstance(clusters, list)
        for c in clusters:
            assert isinstance(c, set)

    def test_all_roles_covered(self) -> None:
        """Every role appears in exactly one cluster."""
        ec = _three_role_ec()
        clusters = ec.role_clusters(threshold=0.3)
        all_roles = set()
        for c in clusters:
            # No overlap between clusters
            assert all_roles.isdisjoint(c)
            all_roles |= c
        assert all_roles == set(ec.roles)


class TestStandardEnrichedCategory:
    """Tests for standard_enriched_category() factory function."""

    def test_creates_8_role_category(self) -> None:
        """Standard enriched category has 8 case roles."""
        ec = standard_enriched_category()
        assert len(ec.roles) == 8

    def test_all_standard_roles_present(self) -> None:
        """All 8 standard roles are in the category."""
        ec = standard_enriched_category()
        for role in STANDARD_ROLES:
            assert role in ec.roles

    def test_magnitude_computable(self) -> None:
        """Standard category magnitude is a finite positive number."""
        ec = standard_enriched_category()
        mag = ec.magnitude()
        assert np.isfinite(mag)
        assert mag > 0

    def test_magnitude_less_than_n(self) -> None:
        """Standard 8-role category has magnitude < 8 (distributional overlap)."""
        ec = standard_enriched_category()
        assert ec.magnitude() < 8.0


# ---------------------------------------------------------------------------
# CaseCategory: previously uncovered methods
# ---------------------------------------------------------------------------

class TestCaseCategoryAssociativity:
    """Tests for associativity_holds()."""

    def test_standard_category_associative(self) -> None:
        """Standard 8-case category satisfies associativity."""
        cat = standard_case_category()
        assert cat.associativity_holds() is True

    def test_minimal_category_associative(self) -> None:
        """Minimal 3-role category satisfies associativity."""
        cat = minimal_case_category()
        assert cat.associativity_holds() is True

    def test_single_morphism_associative(self) -> None:
        """Single morphism is trivially associative."""
        cat = CaseCategory(name="test")
        cat.add_role(CaseRole.NOM)
        cat.add_role(CaseRole.ACC)
        cat.add_morphism(Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on"))
        assert cat.associativity_holds() is True


class TestCaseCategoryIsWellFormed:
    """Tests for is_well_formed()."""

    def test_minimal_category_well_formed(self) -> None:
        """Minimal transitive category satisfies all categorical axioms."""
        cat = minimal_case_category()
        assert cat.is_well_formed() is True

    def test_empty_category_well_formed(self) -> None:
        """Category with one role and no morphisms is trivially well-formed."""
        cat = CaseCategory(name="trivial")
        cat.add_role(CaseRole.NOM)
        assert cat.is_well_formed() is True

    def test_standard_category_well_formed(self) -> None:
        """Standard 8-case category is well-formed."""
        cat = standard_case_category()
        assert cat.is_well_formed() is True


class TestMinimalCaseCategory:
    """Tests for minimal_case_category()."""

    def test_creates_three_role_category(self) -> None:
        """Minimal category has exactly 3 roles: NOM, ACC, INS."""
        cat = minimal_case_category()
        assert len(cat.objects) == 3
        assert CaseRole.NOM in cat.objects
        assert CaseRole.ACC in cat.objects
        assert CaseRole.INS in cat.objects

    def test_creates_three_morphisms(self) -> None:
        """Minimal category has exactly 3 base morphisms."""
        cat = minimal_case_category()
        assert len(cat.morphisms) == 3

    def test_morphisms_are_composable(self) -> None:
        """acts_on and applied_to compose: NOM → ACC → via INS."""
        cat = minimal_case_category()
        m_nom_ins = next(m for m in cat.morphisms if m.source == CaseRole.NOM and m.target == CaseRole.INS)
        m_ins_acc = next(m for m in cat.morphisms if m.source == CaseRole.INS and m.target == CaseRole.ACC)
        composed = cat.compose(m_nom_ins, m_ins_acc)
        assert composed.source == CaseRole.NOM
        assert composed.target == CaseRole.ACC


class TestAlignmentFunctions:
    """Tests for accusative, ergative, tripartite, and active_stative alignments."""

    def test_accusative_alignment_structure(self) -> None:
        """Accusative alignment maps S,A→NOM and P→ACC."""
        alignment = accusative_alignment()
        assert alignment[CaseRole.S] == CaseRole.NOM
        assert alignment[CaseRole.A] == CaseRole.NOM
        assert alignment[CaseRole.P] == CaseRole.ACC

    def test_accusative_alignment_has_three_entries(self) -> None:
        """Accusative alignment covers S, A, P."""
        alignment = accusative_alignment()
        assert len(alignment) == 3
        assert CaseRole.S in alignment
        assert CaseRole.A in alignment
        assert CaseRole.P in alignment

    def test_ergative_alignment_structure(self) -> None:
        """Ergative alignment maps S,P→ABS and A→ERG."""
        alignment = ergative_alignment()
        assert alignment[CaseRole.S] == CaseRole.ABS
        assert alignment[CaseRole.P] == CaseRole.ABS
        assert alignment[CaseRole.A] == CaseRole.ERG

    def test_tripartite_alignment_structure(self) -> None:
        """Tripartite alignment is injective: S→ABS, A→ERG, P→ACC."""
        alignment = tripartite_alignment()
        assert alignment[CaseRole.S] == CaseRole.ABS
        assert alignment[CaseRole.A] == CaseRole.ERG
        assert alignment[CaseRole.P] == CaseRole.ACC
        # Injective: all targets distinct
        targets = list(alignment.values())
        assert len(targets) == len(set(targets))

    def test_active_stative_alignment_has_two_contexts(self) -> None:
        """Active-stative alignment returns a dict with 'active' and 'stative'."""
        result = active_stative_alignment()
        assert "active" in result
        assert "stative" in result

    def test_active_stative_active_context(self) -> None:
        """Active context: S_active → ERG, A → ERG, P → ABS."""
        result = active_stative_alignment()
        active = result["active"]
        assert active[CaseRole.S] == CaseRole.ERG
        assert active[CaseRole.A] == CaseRole.ERG
        assert active[CaseRole.P] == CaseRole.ABS

    def test_active_stative_stative_context(self) -> None:
        """Stative context: S_stative → ABS, A → ERG, P → ABS."""
        result = active_stative_alignment()
        stative = result["stative"]
        assert stative[CaseRole.S] == CaseRole.ABS
        assert stative[CaseRole.A] == CaseRole.ERG
        assert stative[CaseRole.P] == CaseRole.ABS

    def test_accusative_ergative_complement(self) -> None:
        """S is marked differently in accusative vs ergative alignment."""
        acc = accusative_alignment()
        erg = ergative_alignment()
        assert acc[CaseRole.S] != erg[CaseRole.S]

    def test_all_alignments_cover_core_roles(self) -> None:
        """All alignment functions cover S, A, P core argument roles."""
        for align_fn in [accusative_alignment, ergative_alignment, tripartite_alignment]:
            alignment = align_fn()
            assert CaseRole.S in alignment
            assert CaseRole.A in alignment
            assert CaseRole.P in alignment


def test_root_package_reexports_standard_enriched_category() -> None:
    """Root ``src`` package exposes the standard enriched factory."""
    from src import EnrichedCategory, standard_enriched_category

    ec = standard_enriched_category()
    assert isinstance(ec, EnrichedCategory)
    assert ec.name
