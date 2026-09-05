"""Comprehensive tests for string_diagram.py DisCoPy integration functions.

Tests the create_discopy_* functions that were previously uncovered.
Uses real DisCoPy operations (zero-mock policy).
"""

import pytest

discopy = pytest.importorskip("discopy", reason="discopy required")
from discopy.rigid import Ty  # noqa: E402

from src.diagrams.string_diagram import (  # noqa: E402
    AtomicType,
    Wire,
    Box,
    Sentence,
    Discourse,
    N,
    S,
    create_discopy_transitive,
    create_discopy_intransitive,
    create_discopy_passive,
    create_discopy_snake_equation,
    create_discopy_composition,
    create_discopy_multilingual,
)
from src.case_systems.case_category import CaseRole  # noqa: E402


# ── AtomicType ────────────────────────────────────────────


class TestAtomicType:
    def test_repr(self):
        t = AtomicType("n")
        assert repr(t) == "n"

    def test_frozen(self):
        t = AtomicType("n")
        with pytest.raises(AttributeError):
            t.name = "s"


# ── Wire ──────────────────────────────────────────────────


class TestWire:
    def test_basic_wire(self):
        w = Wire(wire_type=N)
        assert w.wire_type == N
        assert w.entity is None
        assert w.case_role is None

    def test_wire_with_entity_and_role(self):
        w = Wire(wire_type=N, entity="Alice", case_role=CaseRole.NOM)
        assert "Alice" in repr(w)
        assert "NOM" in repr(w)

    def test_wire_repr_basic(self):
        w = Wire(wire_type=N)
        assert repr(w) == "n"

    def test_wire_repr_entity_only(self):
        w = Wire(wire_type=N, entity="Bob")
        assert "(Bob)" in repr(w)

    def test_wire_repr_role_only(self):
        w = Wire(wire_type=N, case_role=CaseRole.ACC)
        assert "[ACC]" in repr(w)


# ── Box ───────────────────────────────────────────────────


class TestBox:
    def test_empty_box(self):
        b = Box(name="test")
        assert b.dom_type == "I"
        assert b.cod_type == "I"

    def test_box_with_wires(self):
        w_in = Wire(wire_type=N)
        w_out = Wire(wire_type=S)
        b = Box(name="verb", dom=[w_in], cod=[w_out])
        assert "n" in b.dom_type
        assert "s" in b.cod_type

    def test_box_repr(self):
        b = Box(name="chases", dom=[Wire(N)], cod=[Wire(S)])
        assert "chases" in repr(b)
        assert "→" in repr(b)


# ── Sentence ──────────────────────────────────────────────


class TestSentence:
    def test_transitive_factory(self):
        s = Sentence.transitive("Alice", "chases", "Bob")
        assert s.text == "Alice chases Bob"
        assert s.num_boxes == 3  # 2 nouns + 1 verb
        assert s.codomain_type == "s"
        assert "Alice" in s.case_assignments
        assert s.case_assignments["Alice"] == CaseRole.NOM
        assert s.case_assignments["Bob"] == CaseRole.ACC

    def test_intransitive_factory(self):
        s = Sentence.intransitive("Bob", "runs")
        assert s.text == "Bob runs"
        assert s.num_boxes == 2
        assert s.codomain_type == "s"
        assert s.case_assignments["Bob"] == CaseRole.NOM

    def test_add_noun(self):
        s = Sentence(text="test")
        wire = s.add_noun("Cat", CaseRole.DAT)
        assert wire.entity == "Cat"
        assert wire.case_role == CaseRole.DAT
        assert len(s.boxes) == 1

    def test_add_verb_transitive(self):
        s = Sentence(text="test")
        subj = s.add_noun("Alice", CaseRole.NOM)
        obj = s.add_noun("Bob", CaseRole.ACC)
        result = s.add_verb("chases", subj, obj)
        assert result.wire_type == S
        assert len(s.boxes) == 3

    def test_add_verb_intransitive(self):
        s = Sentence(text="test")
        subj = s.add_noun("Bob", CaseRole.NOM)
        result = s.add_verb("runs", subj)
        assert result.wire_type == S

    def test_empty_codomain(self):
        s = Sentence(text="empty")
        assert s.codomain_type == "I"


# ── Discourse ─────────────────────────────────────────────


class TestDiscourse:
    def test_two_sentence_factory(self):
        d = Discourse.two_sentence("Alice", "chases", "Bob", "Bob", "runs")
        assert d.num_sentences == 2
        assert "Alice" in d.entities
        assert "Bob" in d.entities
        assert d.total_boxes == 5  # 3 + 2

    def test_role_reversal_factory(self):
        d = Discourse.role_reversal("Alice", "Bob")
        assert d.num_sentences == 3
        reversals = d.role_reversal_entities()
        # Both Alice and Bob change roles across sentences
        assert "Alice" in reversals
        assert "Bob" in reversals

    def test_codomain_type(self):
        d = Discourse.two_sentence("Alice", "chases", "Bob", "Bob", "runs")
        assert "s" in d.codomain_type

    def test_add_sentence(self):
        d = Discourse()
        s1 = Sentence.transitive("Alice", "chases", "Bob")
        d.add_sentence(s1)
        assert d.num_sentences == 1
        assert "Alice" in d.entity_wires
        assert len(d.role_history["Alice"]) == 1

    def test_entity_persistence(self):
        d = Discourse()
        s1 = Sentence.transitive("Alice", "chases", "Bob")
        s2 = Sentence.intransitive("Bob", "runs")
        d.add_sentence(s1)
        d.add_sentence(s2)
        # Bob appears in both sentences
        assert len(d.role_history["Bob"]) == 2

    def test_no_role_reversal(self):
        d = Discourse()
        s1 = Sentence.transitive("Alice", "chases", "Bob")
        d.add_sentence(s1)
        # Single appearance, no reversal
        assert d.role_reversal_entities() == []


# ── DisCoPy Integration Functions ─────────────────────────


class TestCreateDiscopyTransitive:
    def test_basic_transitive(self):
        d = create_discopy_transitive("Alice", "chases", "Bob")
        assert d.cod == Ty("s")
        assert d.dom == Ty()
        assert len(d.boxes) == 5  # 3 words + 2 cups

    def test_custom_s_type(self):
        d = create_discopy_transitive("Alice", "chases", "Bob", s_type="s_en")
        assert d.cod == Ty("s_en")


class TestCreateDiscopyIntransitive:
    def test_basic_intransitive(self):
        d = create_discopy_intransitive("Bob", "runs")
        assert d.cod == Ty("s")
        assert d.dom == Ty()
        assert len(d.boxes) == 3  # 2 words + 1 cup


class TestCreateDiscopyPassive:
    def test_passive_construction(self):
        d = create_discopy_passive("Bob", "chased", "Alice")
        assert d.cod == Ty("s")
        assert d.dom == Ty()
        # Should have 3 word boxes + 2 cups
        assert len(d.boxes) == 5

    def test_passive_same_codomain_as_active(self):
        active = create_discopy_transitive("Alice", "chases", "Bob")
        passive = create_discopy_passive("Bob", "chased", "Alice")
        assert active.cod == passive.cod


class TestCreateDiscopySnakeEquation:
    def test_snake_equation_components(self):
        left, identity, right = create_discopy_snake_equation()
        x = Ty("x")
        assert left.dom == x
        assert left.cod == x
        assert identity.dom == x
        assert identity.cod == x
        assert right.dom == x
        assert right.cod == x

    def test_snake_equation_identity(self):
        left, identity, right = create_discopy_snake_equation()
        # After normal form, snakes should equal identity
        assert left.normal_form() == identity.normal_form()
        assert right.normal_form() == identity.normal_form()


class TestCreateDiscopyComposition:
    def test_composition_output(self):
        words, contracted = create_discopy_composition("Alice", "chases", "Bob")
        # Pre-contraction has 3 word boxes
        assert len(words.boxes) == 3
        # Contracted has 3 words + 2 cups
        assert len(contracted.boxes) == 5
        # Contracted reduces to sentence type
        assert contracted.cod == Ty("s")

    def test_words_domain_is_empty(self):
        words, _ = create_discopy_composition("A", "V", "B")
        assert words.dom == Ty()


class TestCreateDiscopyMultilingual:
    def test_default_languages(self):
        diagrams = create_discopy_multilingual()
        assert len(diagrams) == 6
        assert "English" in diagrams
        assert "Latin" in diagrams
        assert "Japanese" in diagrams
        for lang, d in diagrams.items():
            assert d.cod == Ty("s"), f"{lang} diagram doesn't reduce to s"

    def test_custom_translations(self):
        custom = {"Test": ("A", "V", "B")}
        diagrams = create_discopy_multilingual(translations=custom)
        assert len(diagrams) == 1
        assert "Test" in diagrams
        assert diagrams["Test"].cod == Ty("s")

    def test_all_diagrams_have_same_codomain(self):
        diagrams = create_discopy_multilingual()
        codomains = {d.cod for d in diagrams.values()}
        assert len(codomains) == 1  # All reduce to same type
