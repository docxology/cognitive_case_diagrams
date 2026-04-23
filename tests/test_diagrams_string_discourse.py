"""Tests for Sentence, Discourse, AtomicType, Wire, Box — no discopy required."""
from src.diagrams.string_diagram import (
    AtomicType,
    Box,
    Discourse,
    N,
    S,
    Sentence,
    Wire,
)
from src.case_systems.case_category import CaseRole


class TestAtomicTypeAndWire:
    def test_atomic_type_repr(self):
        t = AtomicType("n")
        assert repr(t) == "n"

    def test_wire_repr_minimal(self):
        w = Wire(wire_type=N)
        assert "n" in repr(w)

    def test_wire_repr_with_entity_and_role(self):
        w = Wire(wire_type=N, entity="Alice", case_role=CaseRole.NOM)
        r = repr(w)
        assert "Alice" in r
        assert "NOM" in r

    def test_wire_no_entity_no_role(self):
        w = Wire(wire_type=S)
        assert "s" in repr(w)


class TestBox:
    def test_box_repr(self):
        subj = Wire(wire_type=N, entity="Alice", case_role=CaseRole.NOM)
        obj = Wire(wire_type=N, entity="Bob", case_role=CaseRole.ACC)
        sent_wire = Wire(wire_type=S)
        b = Box(name="chases", dom=[subj, obj], cod=[sent_wire])
        r = repr(b)
        assert "chases" in r

    def test_empty_dom_gives_I(self):
        b = Box(name="Alice", dom=[], cod=[Wire(wire_type=N)])
        assert b.dom_type == "I"

    def test_empty_cod_gives_I(self):
        b = Box(name="empty", dom=[], cod=[])
        assert b.cod_type == "I"

    def test_multi_wire_dom_type(self):
        w1 = Wire(wire_type=N)
        w2 = Wire(wire_type=N)
        b = Box(name="verb", dom=[w1, w2], cod=[Wire(wire_type=S)])
        assert "⊗" in b.dom_type


class TestSentence:
    def test_transitive_creates_correct_structure(self):
        s = Sentence.transitive("Alice", "chases", "Bob")
        assert s.text == "Alice chases Bob"
        assert "Alice" in s.case_assignments
        assert s.case_assignments["Alice"] == CaseRole.NOM
        assert s.case_assignments["Bob"] == CaseRole.ACC

    def test_intransitive_creates_correct_structure(self):
        s = Sentence.intransitive("Bob", "runs")
        assert "Bob" in s.case_assignments
        assert s.case_assignments["Bob"] == CaseRole.NOM

    def test_num_boxes_transitive(self):
        s = Sentence.transitive("Alice", "chases", "Bob")
        # 2 noun boxes + 1 verb box
        assert s.num_boxes == 3

    def test_num_boxes_intransitive(self):
        s = Sentence.intransitive("Bob", "runs")
        # 1 noun box + 1 verb box
        assert s.num_boxes == 2

    def test_codomain_type_is_s(self):
        s = Sentence.transitive("Alice", "chases", "Bob")
        assert s.codomain_type == "s"


class TestDiscourse:
    def test_add_sentence_tracks_entities(self):
        d = Discourse()
        d.add_sentence(Sentence.transitive("Alice", "chases", "Bob"))
        assert "Alice" in d.entities
        assert "Bob" in d.entities

    def test_num_sentences(self):
        d = Discourse.two_sentence("Alice", "chases", "Bob", "Bob", "runs")
        assert d.num_sentences == 2

    def test_total_boxes(self):
        d = Discourse.two_sentence("Alice", "chases", "Bob", "Bob", "runs")
        # sentence 1: 3 boxes, sentence 2: 2 boxes
        assert d.total_boxes == 5

    def test_codomain_type_contains_s(self):
        d = Discourse.two_sentence("Alice", "chases", "Bob", "Bob", "runs")
        assert "s" in d.codomain_type

    def test_role_reversal_entities_detected(self):
        d = Discourse.role_reversal("Alice", "Bob")
        reversals = d.role_reversal_entities()
        # Alice: NOM, ACC, NOM — role varies → in reversals
        # Bob: ACC, NOM — role varies → in reversals
        assert "Alice" in reversals or "Bob" in reversals

    def test_role_reversal_discourse_has_three_sentences(self):
        d = Discourse.role_reversal("Alice", "Bob")
        assert d.num_sentences == 3

    def test_no_role_reversal_in_uniform_discourse(self):
        d = Discourse()
        d.add_sentence(Sentence.transitive("Alice", "chases", "Bob"))
        d.add_sentence(Sentence.transitive("Alice", "finds", "Bob"))
        # Alice is NOM both times; Bob is ACC both times — no reversal
        reversals = d.role_reversal_entities()
        assert "Alice" not in reversals
        assert "Bob" not in reversals


