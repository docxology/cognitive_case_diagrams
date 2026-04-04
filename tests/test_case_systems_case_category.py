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
        f = next(m for m in cat.morphisms if m.label == "acts_on")
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
