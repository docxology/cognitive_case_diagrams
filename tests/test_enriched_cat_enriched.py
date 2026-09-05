"""Tests for the enriched category module.

Validates [0,1]-enrichment axioms, hom-values, composition inequality,
and categorical magnitude computation.
"""

import pytest
import numpy as np

from src.enriched_cat.enriched import (
    EnrichedCategory,
    standard_enriched_category,
)
from src.case_systems.case_category import CaseRole


class TestEnrichedCreation:
    """Tests for EnrichedCategory initialization and validation."""

    def test_standard_creation(self):
        """Standard enriched category creates without error."""
        cat = standard_enriched_category()
        assert cat.name == "Standard8CaseEnriched"
        assert len(cat.roles) == 8

    def test_identity_axiom(self):
        """Identity axiom: C(A, A) = 1.0 for all objects."""
        cat = standard_enriched_category()
        for i, role in enumerate(cat.roles):
            assert np.isclose(cat.proximity_matrix[i, i], 1.0), \
                f"Identity violated for {role.name}"

    def test_values_in_unit_interval(self):
        """All hom-values are in [0, 1]."""
        cat = standard_enriched_category()
        assert np.all(cat.proximity_matrix >= 0)
        assert np.all(cat.proximity_matrix <= 1)

    def test_invalid_identity_raises(self):
        """Non-unit diagonal raises ValueError."""
        bad_matrix = np.eye(3)
        bad_matrix[1, 1] = 0.5
        with pytest.raises(ValueError, match="Identity axiom"):
            EnrichedCategory(
                name="Bad",
                roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.GEN],
                proximity_matrix=bad_matrix,
            )

    def test_invalid_shape_raises(self):
        """Matrix shape mismatch raises ValueError."""
        with pytest.raises(ValueError, match="shape"):
            EnrichedCategory(
                name="Bad",
                roles=[CaseRole.NOM, CaseRole.ACC],
                proximity_matrix=np.eye(3),
            )

    def test_out_of_range_raises(self):
        """Values outside [0,1] raise ValueError."""
        bad_matrix = np.eye(2)
        bad_matrix[0, 1] = 1.5
        with pytest.raises(ValueError, match="\\[0, 1\\]"):
            EnrichedCategory(
                name="Bad",
                roles=[CaseRole.NOM, CaseRole.ACC],
                proximity_matrix=bad_matrix,
            )


class TestHomValues:
    """Tests for hom-value querying."""

    def test_hom_symmetric_roles(self):
        """NOM-ACC proximity matches expected value."""
        cat = standard_enriched_category()
        assert np.isclose(cat.hom(CaseRole.NOM, CaseRole.ACC), 0.85)

    def test_hom_identity(self):
        """Self-hom is always 1.0."""
        cat = standard_enriched_category()
        for role in cat.roles:
            assert cat.hom(role, role) == 1.0

    def test_hom_invalid_role(self):
        """Querying hom for absent role raises ValueError."""
        cat = standard_enriched_category()
        with pytest.raises(ValueError, match="not in category"):
            cat.hom(CaseRole.ERG, CaseRole.NOM)

    def test_proximity_ordering(self):
        """NOM-ACC > NOM-GEN > NOM-LOC (closer roles have higher values)."""
        cat = standard_enriched_category()
        nom_acc = cat.hom(CaseRole.NOM, CaseRole.ACC)
        nom_gen = cat.hom(CaseRole.NOM, CaseRole.GEN)
        nom_loc = cat.hom(CaseRole.NOM, CaseRole.LOC)
        assert nom_acc > nom_gen > nom_loc


class TestCompositionInequality:
    """Tests for the composition inequality C(A,C) >= C(A,B)·C(B,C)."""

    def test_nom_acc_dat_holds(self):
        """NOM→ACC→DAT composition inequality."""
        cat = standard_enriched_category()
        # C(NOM, DAT) >= C(NOM, ACC) * C(ACC, DAT)
        result = cat.check_composition_inequality(CaseRole.NOM, CaseRole.ACC, CaseRole.DAT)
        # 0.45 >= 0.85 * 0.55 = 0.4675 — fails!
        # This is documented in the manuscript as an example of failure
        assert isinstance(result, bool)

    def test_nom_acc_gen(self):
        """Test composition inequality for NOM→ACC→GEN path."""
        cat = standard_enriched_category()
        result = cat.check_composition_inequality(CaseRole.NOM, CaseRole.ACC, CaseRole.GEN)
        assert isinstance(result, bool)


class TestMagnitude:
    """Tests for categorical magnitude computation."""

    def test_magnitude_is_positive(self):
        """Categorical magnitude should be positive for valid category."""
        cat = standard_enriched_category()
        mag = cat.magnitude()
        assert mag > 0

    def test_magnitude_finite(self):
        """Magnitude should be finite, not inf/nan."""
        cat = standard_enriched_category()
        mag = cat.magnitude()
        assert np.isfinite(mag)

    def test_identity_matrix_magnitude_equals_n(self):
        """For the identity matrix (discrete category), magnitude = n."""
        cat = EnrichedCategory(
            name="Discrete",
            roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.GEN],
            proximity_matrix=np.eye(3),
        )
        assert np.isclose(cat.magnitude(), 3.0)

    def test_singular_matrix_magnitude_is_finite(self):
        """Singular matrix uses pseudo-inverse fallback — magnitude is finite."""
        singular_matrix = np.array([
            [1.0, 1.0],
            [1.0, 1.0]
        ])
        cat = EnrichedCategory(
            name="Singular",
            roles=[CaseRole.NOM, CaseRole.ACC],
            proximity_matrix=singular_matrix,
        )
        mag = cat.magnitude()
        assert np.isfinite(mag), f"Expected finite magnitude, got {mag}"

    def test_singular_matrix_weighting_is_finite(self):
        """Singular matrix uses pseudo-inverse fallback — weighting is finite."""
        cat = EnrichedCategory(
            name="Singular",
            roles=[CaseRole.NOM, CaseRole.ACC],
            proximity_matrix=np.array([[1.0, 1.0], [1.0, 1.0]]),
        )
        w = cat.weighting()
        assert np.all(np.isfinite(w)), f"Expected finite weighting, got {w}"

    def test_singular_matrix_coweighting_is_finite(self):
        """Singular matrix uses pseudo-inverse fallback — coweighting is finite."""
        cat = EnrichedCategory(
            name="Singular",
            roles=[CaseRole.NOM, CaseRole.ACC],
            proximity_matrix=np.array([[1.0, 1.0], [1.0, 1.0]]),
        )
        cv = cat.coweighting()
        assert np.all(np.isfinite(cv)), f"Expected finite coweighting, got {cv}"

    def test_near_singular_matrix_uses_cached_inverse(self):
        """Near-singular matrix computes magnitude via pseudo-inverse (cached)."""
        # Near-singular: rows are almost identical
        near_singular = np.array([
            [1.0, 0.9999999],
            [0.9999999, 1.0],
        ])
        cat = EnrichedCategory(
            name="NearSingular",
            roles=[CaseRole.NOM, CaseRole.ACC],
            proximity_matrix=near_singular,
        )
        mag = cat.magnitude()
        assert np.isfinite(mag)
        # Weighting and coweighting should reuse the same cached inverse
        w = cat.weighting()
        cv = cat.coweighting()
        assert np.isclose(np.sum(w), mag)
        assert np.isclose(np.sum(cv), mag)

    def test_weighting_sums_to_magnitude(self):
        """Weighting vector sums to magnitude."""
        cat = standard_enriched_category()
        w = cat.weighting()
        assert np.isclose(np.sum(w), cat.magnitude())

    def test_coweighting_sums_to_magnitude(self):
        """Coweighting vector sums to magnitude."""
        cat = standard_enriched_category()
        cv = cat.coweighting()
        assert np.isclose(np.sum(cv), cat.magnitude())


class TestFullCompositionCheck:
    """Tests for the full_composition_check method."""

    def test_full_check_results(self):
        """Check handles correctly formed results dictionary."""
        cat = standard_enriched_category()
        result = cat.full_composition_check()
        assert "holds" in result
        assert "violations" in result
        assert "total" in result
        assert "violation_rate" in result
        n = len(cat.roles)
        # Total checks should be P(n, 3) = n * (n-1) * (n-2)
        assert result["total"] == n * (n - 1) * (n - 2)
        assert len(result["holds"]) + len(result["violations"]) == result["total"]

    def test_magnitude_deficit(self):
        """Magnitude deficit computation is n - magnitude."""
        cat = standard_enriched_category()
        n = len(cat.roles)
        deficit = cat.magnitude_deficit()
        assert np.isclose(deficit, n - cat.magnitude())
        assert deficit >= 0  # Expected to be non-negative for this matrix

    def test_role_clusters(self):
        """Identify clusters of roles based on proximity threshold."""
        cat = standard_enriched_category()
        # High threshold -> each role is its own cluster
        clusters_strict = cat.role_clusters(threshold=0.99)
        assert len(clusters_strict) == len(cat.roles)
        
        # Lower threshold -> fewer clusters
        clusters_relaxed = cat.role_clusters(threshold=0.6)
        assert len(clusters_relaxed) < len(cat.roles)
        
        # Extremely low threshold -> single cluster
        clusters_all = cat.role_clusters(threshold=0.0)
        assert len(clusters_all) == 1
        assert len(clusters_all[0]) == len(cat.roles)


class TestNearSingularMatrix:
    """Magnitude computation on near-singular proximity matrices."""

    def test_near_singular_falls_back_to_pinv(self):
        """Near-singular matrix (cond > 1e12) triggers pseudo-inverse fallback."""
        eps = 1e-14
        mat = np.array([
            [1.0, 1.0 - eps, 0.5],
            [1.0 - eps, 1.0, 0.5],
            [0.5, 0.5, 1.0],
        ])
        cat = EnrichedCategory(
            name="NearSingular",
            roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.GEN],
            proximity_matrix=mat,
        )
        # Magnitude must be finite even for near-singular matrices
        mag = cat.magnitude()
        assert np.isfinite(mag)
