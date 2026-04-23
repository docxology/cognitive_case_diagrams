"""Tests for topos-theoretic bridges module.

Validates geometric theory construction, classifying topos invariants,
Morita equivalence checking, and inter-theoretic transfer.
All tests use real computations — no mocks.
"""

import pytest

from src.case_systems.case_category import (
    CaseRole, CaseCategory,
    standard_case_category,
    minimal_case_category,
)
from src.enriched_cat.enriched import (
    EnrichedCategory,
    standard_enriched_category,
)
from src.topos_theory.topos import (
    Axiom,
    GeometricTheory,
    ClassifyingTopos,
    TheoryType,
    check_morita_equivalence,
    build_typological_theory,
    build_enriched_theory,
    bridge_transfer,
)


class TestAxiom:
    """Tests for Axiom dataclass."""

    def test_creation(self) -> None:
        """Test axiom creation."""
        ax = Axiom(name="test", antecedent="P(x)", consequent="Q(x)")
        assert ax.name == "test"
        assert ax.antecedent == "P(x)"
        assert ax.consequent == "Q(x)"

    def test_str_representation(self) -> None:
        """Test axiom string formatting as sequent."""
        ax = Axiom(
            name="test",
            antecedent="P(x)",
            consequent="Q(x)",
            sort_variables=["x"],
        )
        s = str(ax)
        assert "⊢" in s
        assert "P(x)" in s
        assert "Q(x)" in s

    def test_empty_sort_variables(self) -> None:
        """Test axiom with no sort variables."""
        ax = Axiom(name="test", antecedent="T", consequent="T")
        s = str(ax)
        assert "∅" in s


class TestGeometricTheory:
    """Tests for geometric theory construction."""

    def test_creation(self) -> None:
        """Test empty theory creation."""
        t = GeometricTheory(
            name="T_test",
            theory_type=TheoryType.TYPOLOGICAL,
        )
        assert t.name == "T_test"
        assert len(t.sorts) == 0
        assert len(t.axioms) == 0

    def test_add_sort(self) -> None:
        """Test adding sorts."""
        t = GeometricTheory(name="T", theory_type=TheoryType.TYPOLOGICAL)
        t.add_sort("NOM")
        t.add_sort("ACC")
        assert len(t.sorts) == 2
        assert "NOM" in t.sorts

    def test_add_sort_idempotent(self) -> None:
        """Adding same sort twice doesn't duplicate."""
        t = GeometricTheory(name="T", theory_type=TheoryType.TYPOLOGICAL)
        t.add_sort("NOM")
        t.add_sort("NOM")
        assert len(t.sorts) == 1

    def test_add_relation(self) -> None:
        """Test adding a relation symbol."""
        t = GeometricTheory(name="T", theory_type=TheoryType.TYPOLOGICAL)
        t.add_sort("NOM")
        t.add_sort("ACC")
        t.add_relation("acts_on", ("NOM", "ACC"))
        assert "acts_on" in t.relation_symbols
        assert t.relation_symbols["acts_on"] == ("NOM", "ACC")

    def test_add_relation_invalid_sort(self) -> None:
        """Adding relation with undefined sort raises ValueError."""
        t = GeometricTheory(name="T", theory_type=TheoryType.TYPOLOGICAL)
        t.add_sort("NOM")
        with pytest.raises(ValueError):
            t.add_relation("acts_on", ("NOM", "ACC"))

    def test_add_axiom(self) -> None:
        """Test adding axioms."""
        t = GeometricTheory(name="T", theory_type=TheoryType.TYPOLOGICAL)
        ax = Axiom(name="id", antecedent="x", consequent="id_x")
        t.add_axiom(ax)
        assert len(t.axioms) == 1

    def test_signature_invariant(self) -> None:
        """Test signature invariant computation."""
        t = GeometricTheory(name="T", theory_type=TheoryType.TYPOLOGICAL)
        t.add_sort("NOM")
        t.add_sort("ACC")
        t.add_relation("acts_on", ("NOM", "ACC"))
        t.add_axiom(Axiom(name="id", antecedent="T", consequent="T"))
        assert t.signature_invariant() == (2, 1, 1)

    def test_arity_spectrum(self) -> None:
        """Test arity spectrum computation."""
        t = GeometricTheory(name="T", theory_type=TheoryType.TYPOLOGICAL)
        t.add_sort("A")
        t.add_sort("B")
        t.add_sort("C")
        t.add_relation("r1", ("A", "B"))
        t.add_relation("r2", ("A", "B", "C"))
        assert t.arity_spectrum() == [2, 3]


class TestClassifyingTopos:
    """Tests for classifying topos construction."""

    def test_creation_computes_invariants(self) -> None:
        """Creating a ClassifyingTopos computes invariants automatically."""
        t = GeometricTheory(name="T", theory_type=TheoryType.TYPOLOGICAL)
        t.add_sort("NOM")
        topos = ClassifyingTopos(theory=t)
        assert "signature_shape" in topos.invariants
        assert "arity_spectrum" in topos.invariants

    def test_invariants_match_theory(self) -> None:
        """Invariants reflect the underlying theory."""
        t = GeometricTheory(name="T", theory_type=TheoryType.TYPOLOGICAL)
        t.add_sort("NOM")
        t.add_sort("ACC")
        t.add_relation("R", ("NOM", "ACC"))
        topos = ClassifyingTopos(theory=t)
        assert topos.invariants["signature_shape"] == (2, 1, 0)


class TestMoritaEquivalence:
    """Tests for Morita equivalence checking."""

    def test_identical_theories_equivalent(self) -> None:
        """A theory is Morita-equivalent to itself."""
        t = GeometricTheory(name="T1", theory_type=TheoryType.TYPOLOGICAL)
        t.add_sort("NOM")
        t.add_sort("ACC")
        t.add_relation("R", ("NOM", "ACC"))
        t.add_axiom(Axiom(name="id", antecedent="T", consequent="T"))

        topos1 = ClassifyingTopos(theory=t)
        topos2 = ClassifyingTopos(theory=t)
        equiv, mismatches = check_morita_equivalence(topos1, topos2)
        assert equiv is True
        assert len(mismatches) == 0

    def test_different_arity_not_equivalent(self) -> None:
        """Theories with different arity spectra are not equivalent."""
        t1 = GeometricTheory(name="T1", theory_type=TheoryType.TYPOLOGICAL)
        t1.add_sort("A")
        t1.add_sort("B")
        t1.add_relation("R1", ("A", "B"))

        t2 = GeometricTheory(name="T2", theory_type=TheoryType.DISTRIBUTIONAL)
        t2.add_sort("X")
        t2.add_sort("Y")
        t2.add_sort("Z")
        t2.add_relation("R2", ("X", "Y", "Z"))

        topos1 = ClassifyingTopos(theory=t1)
        topos2 = ClassifyingTopos(theory=t2)
        equiv, mismatches = check_morita_equivalence(topos1, topos2)
        assert equiv is False
        assert len(mismatches) > 0


class TestBuildTheories:
    """Tests for theory builders from categories."""

    def test_build_typological_from_standard(self) -> None:
        """Build geometric theory from standard case category."""
        cat = standard_case_category()
        theory = build_typological_theory(cat, "standard")
        assert theory.theory_type == TheoryType.TYPOLOGICAL
        assert len(theory.sorts) == 8  # 8 standard roles
        assert len(theory.axioms) >= 2  # identity + composition

    def test_build_typological_from_minimal(self) -> None:
        """Build geometric theory from minimal case category."""
        cat = minimal_case_category()
        theory = build_typological_theory(cat, "minimal")
        assert theory.theory_type == TheoryType.TYPOLOGICAL
        assert len(theory.sorts) == 3

    def test_build_enriched_theory(self) -> None:
        """Build geometric theory from enriched category."""
        ec = standard_enriched_category()
        theory = build_enriched_theory(ec)
        assert theory.theory_type == TheoryType.ENRICHED
        assert len(theory.sorts) == 8  # 8 case roles
        assert len(theory.axioms) >= 2

    def test_standard_and_minimal_morita_check(self) -> None:
        """Check Morita equivalence between standard and minimal theories."""
        std_cat = standard_case_category()
        min_cat = minimal_case_category()
        t1 = build_typological_theory(std_cat, "std")
        t2 = build_typological_theory(min_cat, "min")
        topos1 = ClassifyingTopos(theory=t1)
        topos2 = ClassifyingTopos(theory=t2)
        equiv, _ = check_morita_equivalence(topos1, topos2)
        # Different sort counts, so not equivalent
        assert equiv is False


class TestClassifyingToposMinimalTheory:
    """Extended tests: minimal 2-object theory, Morita equality, add_axiom edge cases."""

    def test_two_object_minimal_theory_topos(self):
        """ClassifyingTopos on a pure NOM/ACC theory computes valid invariants."""
        t = GeometricTheory(name="T_minimal", theory_type=TheoryType.TYPOLOGICAL)
        t.add_sort("NOM")
        t.add_sort("ACC")
        t.add_relation("acts_on", ("NOM", "ACC"))
        t.add_axiom(Axiom(name="id", antecedent="T", consequent="T"))
        topos = ClassifyingTopos(theory=t)
        assert topos.invariants["signature_shape"] == (2, 1, 1)
        assert topos.invariants["arity_spectrum"] == [2]

    def test_two_identical_two_object_theories_morita_equivalent(self):
        """Two structurally identical minimal theories are Morita-equivalent."""
        def _make_nom_acc():
            t = GeometricTheory(name="T", theory_type=TheoryType.TYPOLOGICAL)
            t.add_sort("NOM")
            t.add_sort("ACC")
            t.add_relation("acts_on", ("NOM", "ACC"))
            t.add_axiom(Axiom(name="id", antecedent="T", consequent="T"))
            return t
        topos1 = ClassifyingTopos(theory=_make_nom_acc())
        topos2 = ClassifyingTopos(theory=_make_nom_acc())
        equiv, mismatches = check_morita_equivalence(topos1, topos2)
        assert equiv is True
        assert mismatches == []

    def test_add_axiom_with_empty_string_antecedent(self):
        """add_axiom accepts an empty-string antecedent (represents vacuous truth)."""
        t = GeometricTheory(name="T", theory_type=TheoryType.TYPOLOGICAL)
        ax = Axiom(name="vacuous", antecedent="", consequent="True")
        t.add_axiom(ax)
        assert len(t.axioms) == 1
        assert t.axioms[0].antecedent == ""

    def test_add_axiom_with_unicode_formula(self):
        """add_axiom handles Unicode mathematical notation in antecedent."""
        t = GeometricTheory(name="T", theory_type=TheoryType.TYPOLOGICAL)
        ax = Axiom(
            name="categorical_identity",
            antecedent="∀x. id(x) ⊢ id(x)",
            consequent="T",
            sort_variables=["x"],
        )
        t.add_axiom(ax)
        assert "∀x" in str(t.axioms[0])


class TestBridgeTransfer:
    """Tests for inter-theoretic bridge transfer."""

    def test_transfer_between_equivalent_theories(self) -> None:
        """Bridge transfer succeeds for equivalent theories."""
        t = GeometricTheory(name="T", theory_type=TheoryType.TYPOLOGICAL)
        t.add_sort("A")
        t.add_axiom(Axiom(name="ax", antecedent="T", consequent="T"))
        topos1 = ClassifyingTopos(theory=t)
        topos2 = ClassifyingTopos(theory=t)

        result = bridge_transfer(topos1, topos2, "composition_associativity")
        assert result["transfer_possible"] is True
        assert result["property"] == "composition_associativity"

    def test_transfer_blocked_for_non_equivalent(self) -> None:
        """Bridge transfer blocked for non-equivalent theories."""
        t1 = GeometricTheory(name="T1", theory_type=TheoryType.TYPOLOGICAL)
        t1.add_sort("A")
        t1.add_sort("B")
        t1.add_relation("R", ("A", "B"))

        t2 = GeometricTheory(name="T2", theory_type=TheoryType.ENRICHED)
        t2.add_sort("X")
        t2.add_sort("Y")
        t2.add_sort("Z")
        t2.add_relation("S", ("X", "Y", "Z"))

        topos1 = ClassifyingTopos(theory=t1)
        topos2 = ClassifyingTopos(theory=t2)

        result = bridge_transfer(topos1, topos2, "identity_axiom")
        assert result["transfer_possible"] is False

    def test_transfer_result_has_required_keys(self) -> None:
        """Bridge transfer result dictionary has all required keys."""
        t = GeometricTheory(name="T", theory_type=TheoryType.TYPOLOGICAL)
        t.add_sort("A")
        topos = ClassifyingTopos(theory=t)
        result = bridge_transfer(topos, topos, "test_property")
        for key in ["property", "source_theory", "target_theory",
                     "morita_equivalent", "transfer_possible", "mismatches"]:
            assert key in result

    def test_transfer_blocked_on_mismatched_arity_spectrum(self) -> None:
        """Two theories with the *same* sort count but different relation
        arities must have different arity spectra, hence non-equivalent
        classifying-topos invariants, hence the guarded ``bridge_transfer``
        must report ``transfer_possible is False`` and cite the arity
        spectrum in its ``mismatches`` list (soundness guard for §6)."""
        t1 = GeometricTheory(name="T1", theory_type=TheoryType.TYPOLOGICAL)
        t1.add_sort("A"); t1.add_sort("B"); t1.add_sort("C")
        t1.add_relation("R", ("A", "B"))  # binary

        t2 = GeometricTheory(name="T2", theory_type=TheoryType.ENRICHED)
        t2.add_sort("A"); t2.add_sort("B"); t2.add_sort("C")
        t2.add_relation("S", ("A", "B", "C"))  # ternary

        topos1 = ClassifyingTopos(theory=t1)
        topos2 = ClassifyingTopos(theory=t2)

        # Sanity: identical sort counts, mismatched arity spectra.
        assert len(t1.sorts) == len(t2.sorts)
        assert t1.arity_spectrum() != t2.arity_spectrum()

        result = bridge_transfer(topos1, topos2, "composition_associativity")
        assert result["transfer_possible"] is False
        assert result["morita_equivalent"] is False
        # At least one mismatch message must mention the arity spectrum.
        assert any(
            "arity" in msg.lower() for msg in result["mismatches"]
        ), f"Expected arity-spectrum mismatch in {result['mismatches']!r}"
