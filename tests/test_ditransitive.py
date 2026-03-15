"""Tests for the ditransitive sentence module.

Validates DitransitiveSentence creation, case assignments,
and DisCoPy diagram generation for three-argument verbs.
All tests use real computations — no mocks.
"""

import pytest

from src.case_systems.case_category import CaseRole
from src.diagrams.ditransitive import (
    DitransitiveSentence,
    create_ditransitive,
)


class TestDitransitiveSentence:
    """Tests for DitransitiveSentence class."""

    def test_creation(self) -> None:
        """Basic ditransitive sentence creation."""
        sent = DitransitiveSentence(
            subject="Alice",
            verb="gave",
            direct_object="book",
            indirect_object="Bob",
        )
        assert "Alice" in sent.text
        assert "gave" in sent.text

    def test_case_assignments(self) -> None:
        """Three case roles assigned correctly."""
        sent = create_ditransitive("Alice", "gave", "Bob", "book")
        cases = sent.case_assignments
        assert cases["Alice"] == CaseRole.NOM
        assert cases["Bob"] == CaseRole.DAT
        assert cases["book"] == CaseRole.ACC

    def test_num_arguments(self) -> None:
        """Ditransitive always has 3 arguments."""
        sent = create_ditransitive("Alice", "gave", "Bob", "book")
        assert sent.num_arguments == 3

    def test_codomain_type(self) -> None:
        """Sentence codomain type is 'I' (identity — monoidal unit)."""
        sent = create_ditransitive("Alice", "gave", "Bob", "book")
        # The native representation uses manual box/wire construction,
        # so codomain_type returns the monoidal unit 'I'
        assert sent.codomain_type == "I"

    def test_factory_function(self) -> None:
        """Factory function creates valid sentence."""
        sent = create_ditransitive("Alice", "showed", "Bob", "picture")
        assert sent.subject == "Alice"
        assert sent.verb == "showed"
        assert sent.indirect_object == "Bob"
        assert sent.direct_object == "picture"

    def test_different_verbs(self) -> None:
        """Various ditransitive verbs work correctly."""
        verbs = ["gave", "sent", "showed", "told", "offered"]
        for verb in verbs:
            sent = create_ditransitive("Alice", verb, "Bob", "thing")
            assert sent.verb == verb
            assert sent.num_arguments == 3

    def test_num_boxes(self) -> None:
        """Ditransitive sentence has at least 4 boxes (3 nouns + 1 verb)."""
        sent = create_ditransitive("Alice", "gave", "Bob", "book")
        assert sent.num_boxes >= 4


class TestDiscopyDitransitive:
    """Tests for DisCoPy ditransitive diagram generation."""

    def test_discopy_import(self) -> None:
        """DisCoPy ditransitive creation works if discopy available."""
        try:
            from src.diagrams.ditransitive import create_discopy_ditransitive
            diagram = create_discopy_ditransitive("Alice", "gave", "Bob", "book")
            # Diagram should reduce to sentence type 's'
            from discopy.rigid import Ty
            assert diagram.cod == Ty('s')
        except ImportError:
            pytest.skip("discopy not installed")

    def test_discopy_box_count(self) -> None:
        """DisCoPy ditransitive has 4 boxes + 3 cups."""
        try:
            from src.diagrams.ditransitive import create_discopy_ditransitive
            from discopy.rigid import Cup
            diagram = create_discopy_ditransitive("Alice", "gave", "Bob", "book")
            cups = [b for b in diagram.boxes if isinstance(b, Cup)]
            assert len(cups) == 3  # 3 argument contractions
        except ImportError:
            pytest.skip("discopy not installed")

    def test_complexity_comparison(self) -> None:
        """Ditransitive is more complex than transitive."""
        try:
            from src.diagrams.ditransitive import create_discopy_ditransitive
            from src.diagrams.complexity_metrics import analyze_diagram
            from discopy.rigid import Ty, Box, Cup, Id

            # Transitive
            n = Ty('n')
            s = Ty('s')
            trans = (
                Box("Alice", Ty(), n) @ Box("chases", Ty(), n.r @ s @ n.l)
                @ Box("Bob", Ty(), n)
                >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
            )
            trans_c = analyze_diagram(trans)

            # Ditransitive
            ditrans = create_discopy_ditransitive("Alice", "gave", "Bob", "book")
            ditrans_c = analyze_diagram(ditrans)

            # Ditransitive should be more complex
            assert ditrans_c.box_count > trans_c.box_count
        except ImportError:
            pytest.skip("discopy not installed")
