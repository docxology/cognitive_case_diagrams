"""Tests for the string_diagram module.

Validates native DisCoCat/DisCoCirc representations and
real DisCoPy diagram creation functions.
"""

import pytest

from src.diagrams.string_diagram import (
    Wire,
    Box,
    Sentence,
    Discourse,
    N,
    S,
)
from src.case_systems.case_category import CaseRole


class TestAtomicType:
    """Tests for AtomicType."""

    def test_noun_type(self):
        assert N.name == "n"

    def test_sentence_type(self):
        assert S.name == "s"

    def test_repr(self):
        assert repr(N) == "n"


class TestWire:
    """Tests for Wire dataclass."""

    def test_basic_wire(self):
        w = Wire(wire_type=N)
        assert w.wire_type == N
        assert w.entity is None

    def test_entity_wire(self):
        w = Wire(wire_type=N, entity="Alice", case_role=CaseRole.NOM)
        assert w.entity == "Alice"
        assert w.case_role == CaseRole.NOM


class TestBox:
    """Tests for Box dataclass."""

    def test_noun_box(self):
        w = Wire(wire_type=N, entity="Alice")
        b = Box(name="Alice", dom=[], cod=[w])
        assert b.name == "Alice"
        assert b.dom_type == "I"
        assert b.cod_type == "n"

    def test_verb_box(self):
        subj = Wire(wire_type=N, entity="Alice")
        obj = Wire(wire_type=N, entity="Bob")
        sent = Wire(wire_type=S)
        b = Box(name="chases", dom=[subj, obj], cod=[sent])
        assert "n ⊗ n" == b.dom_type
        assert b.cod_type == "s"


class TestSentenceNative:
    """Tests for Sentence (native representation)."""

    def test_transitive(self):
        """Transitive sentence has correct structure."""
        s = Sentence.transitive("Alice", "chases", "Bob")
        assert s.text == "Alice chases Bob"
        assert s.num_boxes == 3  # 2 nouns + 1 verb
        assert s.case_assignments["Alice"] == CaseRole.NOM
        assert s.case_assignments["Bob"] == CaseRole.ACC

    def test_intransitive(self):
        """Intransitive sentence has subject only."""
        s = Sentence.intransitive("Bob", "runs")
        assert s.text == "Bob runs"
        assert s.num_boxes == 2
        assert s.case_assignments["Bob"] == CaseRole.NOM

    def test_codomain_type(self):
        """Sentence codomain includes sentence type."""
        s = Sentence.transitive("Alice", "chases", "Bob")
        assert "s" in s.codomain_type

    def test_add_noun_returns_wire(self):
        """add_noun returns a Wire with correct properties."""
        s = Sentence(text="test")
        w = s.add_noun("Alice", CaseRole.NOM)
        assert w.entity == "Alice"
        assert w.case_role == CaseRole.NOM


class TestDiscourse:
    """Tests for Discourse (DisCoCirc representation)."""

    def test_two_sentence(self):
        """Two-sentence discourse tracks entity persistence."""
        d = Discourse.two_sentence("Alice", "chases", "Bob", "Bob", "runs")
        assert d.num_sentences == 2
        assert "Alice" in d.entities
        assert "Bob" in d.entities

    def test_bob_role_history(self):
        """Bob's role changes from ACC to NOM across discourse."""
        d = Discourse.two_sentence("Alice", "chases", "Bob", "Bob", "runs")
        assert d.role_history["Bob"] == [CaseRole.ACC, CaseRole.NOM]

    def test_role_reversal(self):
        """Three-sentence role reversal discourse."""
        d = Discourse.role_reversal("Alice", "Bob")
        assert d.num_sentences == 3
        assert d.role_history["Alice"] == [CaseRole.NOM, CaseRole.ACC, CaseRole.NOM]

    def test_role_reversal_entities(self):
        """Identifies entities with role changes."""
        d = Discourse.role_reversal("Alice", "Bob")
        reversals = d.role_reversal_entities()
        assert "Alice" in reversals
        assert "Bob" in reversals

    def test_total_boxes(self):
        """Total boxes across discourse."""
        d = Discourse.two_sentence("Alice", "chases", "Bob", "Bob", "runs")
        assert d.total_boxes >= 5

    def test_codomain_type(self):
        """Composite codomain type of discourse."""
        d = Discourse.two_sentence("Alice", "chases", "Bob", "Bob", "runs")
        cod = d.codomain_type
        assert "s" in cod


class TestDiscoPyIntegration:
    """Tests for real DisCoPy diagram creation (requires discopy)."""

    @pytest.fixture(autouse=True)
    def check_discopy(self):
        """Skip tests if discopy is not installed."""
        pytest.importorskip("discopy")

    def test_transitive_diagram(self):
        """Create DisCoPy transitive diagram."""
        from src.diagrams.string_diagram import create_discopy_transitive
        diagram = create_discopy_transitive("Alice", "chases", "Bob")
        # 3 word boxes + 2 Cup boxes = 5 total in DisCoPy
        assert len(diagram.boxes) == 5

    def test_transitive_codomain(self):
        """Transitive diagram reduces to sentence type."""
        from src.diagrams.string_diagram import create_discopy_transitive
        from discopy.rigid import Ty
        diagram = create_discopy_transitive("Alice", "chases", "Bob")
        assert diagram.cod == Ty('s')

    def test_intransitive_diagram(self):
        """Create DisCoPy intransitive diagram."""
        from src.diagrams.string_diagram import create_discopy_intransitive
        from discopy.rigid import Ty
        diagram = create_discopy_intransitive("Bob", "runs")
        # 2 word boxes + 1 Cup = 3 total
        assert len(diagram.boxes) == 3
        assert diagram.cod == Ty('s')

    def test_passive_diagram(self):
        """Create DisCoPy passive voice diagram."""
        from src.diagrams.string_diagram import create_discopy_passive
        from discopy.rigid import Ty
        diagram = create_discopy_passive("Bob", "chased", "Alice")
        # 3 word boxes + 2 Cup boxes = 5 total
        assert len(diagram.boxes) == 5
        assert diagram.cod == Ty('s')

    def test_snake_equation(self):
        """Snake equation: left snake = Id = right snake."""
        from src.diagrams.string_diagram import create_discopy_snake_equation
        from discopy.rigid import Id, Ty
        left, identity, right = create_discopy_snake_equation()
        assert left.normal_form() == Id(Ty('x'))
        assert right.normal_form() == Id(Ty('x'))

    def test_composition(self):
        """Composition produces diagram and normal form."""
        from src.diagrams.string_diagram import create_discopy_composition
        diagram, normal = create_discopy_composition("Alice", "chases", "Bob")
        assert len(diagram.boxes) >= 3
        assert normal is not None

    def test_multilingual(self):
        """Multilingual diagrams created for 6 languages."""
        from src.diagrams.string_diagram import create_discopy_multilingual
        diagrams = create_discopy_multilingual()
        assert len(diagrams) == 6
        assert "English" in diagrams
        assert "Japanese" in diagrams

    def test_multilingual_all_reduce_to_s(self):
        """All multilingual diagrams reduce to sentence type."""
        from src.diagrams.string_diagram import create_discopy_multilingual
        from discopy.rigid import Ty
        diagrams = create_discopy_multilingual()
        for lang, diagram in diagrams.items():
            assert diagram.cod == Ty('s'), f"{lang} doesn't reduce to s"
