"""Tests for the case_category module.

Validates role/morphism creation, composition, identity axioms,
alignment functions, and standard/minimal category factories.
"""

import pytest

from src.case_systems.case_category import (
    CaseRole,
    Morphism,
    CaseCategory,
    standard_case_category,
    minimal_case_category,
    introductory_case_category,
    accusative_alignment,
    ergative_alignment,
    tripartite_alignment,
)


class TestCaseRole:
    """Tests for the CaseRole enum."""

    def test_standard_roles_exist(self):
        """Verify all 8 standard case roles are defined."""
        standard = {"NOM", "ACC", "GEN", "DAT", "INS", "LOC", "ABL", "VOC"}
        actual = {r.name for r in CaseRole if r.name in standard}
        assert actual == standard

    def test_alignment_roles_exist(self):
        """Verify alignment-specific roles (ERG, ABS, S, A, P)."""
        alignment = {"ERG", "ABS", "S", "A", "P"}
        actual = {r.name for r in CaseRole if r.name in alignment}
        assert actual == alignment

    def test_role_values_are_descriptive(self):
        """Each role has a human-readable value."""
        assert CaseRole.NOM.value == "Nominative"
        assert CaseRole.ERG.value == "Ergative"
        assert CaseRole.S.value == "Sole"


class TestMorphism:
    """Tests for the Morphism dataclass."""

    def test_creation(self):
        """Morphism stores source, target, label."""
        m = Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on")
        assert m.source == CaseRole.NOM
        assert m.target == CaseRole.ACC
        assert m.label == "acts_on"

    def test_repr(self):
        """Morphism repr shows arrow notation."""
        m = Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on")
        assert "NOM" in repr(m)
        assert "ACC" in repr(m)
        assert "acts_on" in repr(m)

    def test_frozen(self):
        """Morphisms are immutable (frozen dataclass)."""
        m = Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on")
        with pytest.raises(AttributeError):
            m.label = "new_label"


class TestCaseCategory:
    """Tests for the CaseCategory class."""

    def test_add_role(self):
        """Roles can be added to category."""
        cat = CaseCategory(name="Test")
        cat.add_role(CaseRole.NOM)
        assert CaseRole.NOM in cat.objects

    def test_add_morphism_valid(self):
        """Valid morphisms are accepted."""
        cat = CaseCategory(name="Test")
        cat.add_role(CaseRole.NOM)
        cat.add_role(CaseRole.ACC)
        m = Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on")
        cat.add_morphism(m)
        assert m in cat.morphisms

    def test_add_morphism_invalid_source(self):
        """Morphisms with unknown source are rejected."""
        cat = CaseCategory(name="Test")
        cat.add_role(CaseRole.ACC)
        m = Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on")
        with pytest.raises(ValueError, match="Source role"):
            cat.add_morphism(m)

    def test_add_morphism_invalid_target(self):
        """Morphisms with unknown target are rejected."""
        cat = CaseCategory(name="Test")
        cat.add_role(CaseRole.NOM)
        m = Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on")
        with pytest.raises(ValueError, match="Target role"):
            cat.add_morphism(m)

    def test_identity(self):
        """Identity morphism is self-loop."""
        cat = CaseCategory(name="Test")
        cat.add_role(CaseRole.NOM)
        id_m = cat.identity(CaseRole.NOM)
        assert id_m.source == CaseRole.NOM
        assert id_m.target == CaseRole.NOM
        assert id_m.label == "id"

    def test_identity_invalid_role(self):
        """Identity for unknown role raises."""
        cat = CaseCategory(name="Test")
        with pytest.raises(ValueError, match="not in category"):
            cat.identity(CaseRole.NOM)

    def test_compose_valid(self):
        """Composable morphisms compose correctly."""
        cat = CaseCategory(name="Test")
        for r in [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]:
            cat.add_role(r)
        f = Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on")
        g = Morphism(CaseRole.ACC, CaseRole.DAT, "received_by")
        h = cat.compose(f, g)
        assert h.source == CaseRole.NOM
        assert h.target == CaseRole.DAT
        assert h.weight == pytest.approx(1.0)

    def test_compose_multiplies_weights(self) -> None:
        """Enriched composition multiplies morphism weights (§2)."""
        cat = CaseCategory(name="W")
        for r in [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]:
            cat.add_role(r)
        f = Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on", weight=0.9)
        g = Morphism(CaseRole.ACC, CaseRole.DAT, "received_by", weight=0.7)
        h = cat.compose(f, g)
        assert h.weight == pytest.approx(0.63)

    def test_compose_invalid(self):
        """Non-composable morphisms raise."""
        cat = CaseCategory(name="Test")
        for r in [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]:
            cat.add_role(r)
        f = Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on")
        g = Morphism(CaseRole.DAT, CaseRole.NOM, "reverse")
        with pytest.raises(ValueError, match="Cannot compose"):
            cat.compose(f, g)

    def test_get_morphisms_from(self):
        """Filter morphisms originating from a role."""
        cat = standard_case_category()
        from_nom = cat.get_morphisms_from(CaseRole.NOM)
        assert len(from_nom) >= 4  # acts_on, transfers_to, uses, located_at, addresses

    def test_get_morphisms_to(self):
        """Filter morphisms targeting a role."""
        cat = standard_case_category()
        to_acc = cat.get_morphisms_to(CaseRole.ACC)
        assert len(to_acc) >= 1  # acts_on


class TestStandardCategory:
    """Tests for the standard 8-case category factory."""

    def test_has_8_roles(self):
        """Standard category has exactly 8 roles."""
        cat = standard_case_category()
        assert len(cat.objects) == 8

    def test_has_morphisms(self):
        """Standard category has morphisms defined."""
        cat = standard_case_category()
        assert len(cat.morphisms) == 8

    def test_all_standard_roles_present(self):
        """All 8 standard roles are included."""
        cat = standard_case_category()
        expected = {CaseRole.NOM, CaseRole.ACC, CaseRole.GEN, CaseRole.DAT,
                    CaseRole.INS, CaseRole.LOC, CaseRole.ABL, CaseRole.VOC}
        assert cat.objects == expected


class TestMinimalCategory:
    """Tests for the minimal 3-role category."""

    def test_has_3_roles(self):
        """Minimal category has 3 roles."""
        cat = minimal_case_category()
        assert len(cat.objects) == 3

    def test_has_3_morphisms(self):
        """Minimal category has 3 morphisms."""
        cat = minimal_case_category()
        assert len(cat.morphisms) == 3

    def test_composition_closes(self):
        """Composition of acts_on and applied_to exists implicitly."""
        cat = minimal_case_category()
        # (acts_on is intentionally unused here — see comment below)
        g = next(m for m in cat.morphisms if m.label == "applied_to")
        # INS -> ACC (applied_to), but NOM -> ACC (acts_on) is the composed path
        # NOM -> INS (uses), INS -> ACC (applied_to) -> compose
        uses = next(m for m in cat.morphisms if m.label == "uses")
        h = cat.compose(uses, g)
        assert h.source == CaseRole.NOM
        assert h.target == CaseRole.ACC


class TestIntroductoryCategory:
    """Tests for introductory_case_category() (manuscript fig:case-minimal)."""

    def test_four_roles_four_morphisms(self) -> None:
        cat = introductory_case_category()
        assert len(cat.objects) == 4
        assert {CaseRole.NOM, CaseRole.ACC, CaseRole.INS, CaseRole.VOC} == cat.objects
        assert len(cat.morphisms) == 4

    def test_triangle_weights_and_composition_product(self) -> None:
        cat = introductory_case_category()
        uses = next(m for m in cat.morphisms if m.label == "uses")
        applied = next(m for m in cat.morphisms if m.label == "applied_to")
        acts = next(m for m in cat.morphisms if m.label == "acts_on")
        assert uses.weight == pytest.approx(0.9)
        assert applied.weight == pytest.approx(0.7)
        assert acts.weight == pytest.approx(0.63)
        assert uses.weight * applied.weight == pytest.approx(acts.weight)
        composed = cat.compose(uses, applied)
        assert composed.source == CaseRole.NOM
        assert composed.target == CaseRole.ACC
        assert composed.weight == pytest.approx(acts.weight)

    def test_identity_has_unit_weight(self) -> None:
        cat = CaseCategory(name="Id")
        cat.add_role(CaseRole.NOM)
        id_m = cat.identity(CaseRole.NOM)
        assert id_m.weight == pytest.approx(1.0)


class TestAssociativity:
    """Tests for CaseCategory.associativity_holds() including weight checks."""

    def test_associativity_with_unit_weights(self):
        """Associativity holds for unit-weight morphisms."""
        cat = minimal_case_category()
        assert cat.associativity_holds()

    def test_associativity_with_enriched_weights(self):
        """Associativity holds for non-unit weights (multiplicative is associative)."""
        cat = CaseCategory(name="Weighted")
        for r in [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]:
            cat.add_role(r)
        cat.add_morphism(Morphism(CaseRole.NOM, CaseRole.ACC, "f", weight=0.8))
        cat.add_morphism(Morphism(CaseRole.ACC, CaseRole.DAT, "g", weight=0.7))
        cat.add_morphism(Morphism(CaseRole.NOM, CaseRole.DAT, "h", weight=0.6))
        assert cat.associativity_holds()

    def test_empty_category_associativity(self):
        """Vacuously true: no morphisms to check."""
        cat = CaseCategory(name="Empty")
        cat.add_role(CaseRole.NOM)
        assert cat.associativity_holds()


class TestIsWellFormed:
    """Tests for CaseCategory.is_well_formed()."""

    def test_minimal_category_well_formed(self):
        cat = minimal_case_category()
        assert cat.is_well_formed()

    def test_standard_category_well_formed(self):
        cat = standard_case_category()
        assert cat.is_well_formed()

    def test_introductory_well_formed(self):
        cat = introductory_case_category()
        assert cat.is_well_formed()

    def test_empty_objects_well_formed(self):
        """Category with no objects is vacuously well-formed."""
        cat = CaseCategory(name="Empty")
        assert cat.is_well_formed()


class TestAssessDAIFSurprisal:
    """Tests for CaseCategory.assess_daif_surprisal()."""

    def test_n400_amplitude_proportional_to_weight_mismatch(self):
        cat = minimal_case_category()
        observed = Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on", weight=0.6)
        result = cat.assess_daif_surprisal(observed, predicted_weight=0.9)
        assert result["N400_amplitude"] == pytest.approx(0.3)

    def test_p600_zero_when_structurally_licensed(self):
        cat = minimal_case_category()
        observed = Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on", weight=1.0)
        result = cat.assess_daif_surprisal(observed, predicted_weight=1.0)
        assert result["P600_amplitude"] == 0.0

    def test_p600_triggers_on_unlicensed_morphism(self):
        cat = minimal_case_category()
        unlicensed = Morphism(CaseRole.ACC, CaseRole.NOM, "fake", weight=1.0)
        result = cat.assess_daif_surprisal(unlicensed, predicted_weight=1.0)
        assert result["P600_amplitude"] == 1.0

    def test_n400_zero_on_perfect_prediction(self):
        cat = minimal_case_category()
        observed = Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on", weight=0.5)
        result = cat.assess_daif_surprisal(observed, predicted_weight=0.5)
        assert result["N400_amplitude"] == pytest.approx(0.0)


class TestActiveStativeAlignment:
    """Tests for active_stative_alignment()."""

    def test_returns_two_modes(self):
        from src.case_systems.case_category import active_stative_alignment
        result = active_stative_alignment()
        assert "active" in result
        assert "stative" in result

    def test_active_s_maps_to_erg(self):
        from src.case_systems.case_category import active_stative_alignment
        result = active_stative_alignment()
        assert result["active"][CaseRole.S] == CaseRole.ERG

    def test_stative_s_maps_to_abs(self):
        from src.case_systems.case_category import active_stative_alignment
        result = active_stative_alignment()
        assert result["stative"][CaseRole.S] == CaseRole.ABS


class TestAlignments:
    """Tests for alignment mapping functions."""

    def test_accusative_groups_s_and_a(self):
        """Accusative collapses {S, A} to NOM."""
        align = accusative_alignment()
        assert align[CaseRole.S] == CaseRole.NOM
        assert align[CaseRole.A] == CaseRole.NOM
        assert align[CaseRole.P] == CaseRole.ACC

    def test_ergative_groups_s_and_p(self):
        """Ergative collapses {S, P} to ABS."""
        align = ergative_alignment()
        assert align[CaseRole.S] == CaseRole.ABS
        assert align[CaseRole.P] == CaseRole.ABS
        assert align[CaseRole.A] == CaseRole.ERG

    def test_tripartite_is_injective(self):
        """Tripartite mapping is injective (no neutralization)."""
        align = tripartite_alignment()
        values = list(align.values())
        assert len(values) == len(set(values))

    def test_all_alignments_cover_core_roles(self):
        """Every alignment maps S, A, P."""
        for align_fn in [accusative_alignment, ergative_alignment, tripartite_alignment]:
            align = align_fn()
            assert set(align.keys()) == {CaseRole.S, CaseRole.A, CaseRole.P}


class TestAssociativityHoldsToleranceKwarg:
    """Regression tests for the ``weight_tolerance`` kwarg on
    ``CaseCategory.associativity_holds()`` — promotes the previously-hardcoded
    ``_FLOAT_TOLERANCE = 1e-9`` to a per-call knob so callers with noisy
    user-supplied weights can loosen or tighten the equality check without
    forking the code."""

    def test_default_tolerance_passes_on_standard_category(self):
        cat = standard_case_category()
        assert cat.associativity_holds() is True

    def test_explicit_tight_tolerance_still_passes(self):
        cat = standard_case_category()
        # Unit-weight morphisms have exact composition, so even a very tight
        # tolerance must still pass on the standard category.
        assert cat.associativity_holds(weight_tolerance=1e-15) is True

    def test_explicit_loose_tolerance_still_passes(self):
        cat = standard_case_category()
        # Loosening the tolerance cannot turn a pass into a fail.
        assert cat.associativity_holds(weight_tolerance=1e-3) is True

    def test_non_positive_tolerance_raises(self):
        cat = standard_case_category()
        with pytest.raises(ValueError, match="weight_tolerance"):
            cat.associativity_holds(weight_tolerance=0.0)
        with pytest.raises(ValueError, match="weight_tolerance"):
            cat.associativity_holds(weight_tolerance=-1e-9)
