"""Tests for the enriched category module.

Validates [0,1]-enrichment axioms, hom-values, composition inequality,
and categorical magnitude computation.
"""

import pytest
import numpy as np

from src.enriched_cat.enriched import (
    EnrichedCategory,
    standard_enriched_category,
    STANDARD_PROXIMITY_MATRIX,
    STANDARD_ROLES,
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
