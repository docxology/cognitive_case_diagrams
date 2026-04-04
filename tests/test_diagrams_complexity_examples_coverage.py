"""Comprehensive tests for complexity_examples module.

Tests build_complexity_examples() to bring coverage above 0%.
Uses real DisCoPy operations (zero-mock policy).
"""

import pytest

discopy = pytest.importorskip("discopy", reason="discopy required")
from discopy.rigid import Ty  # noqa: E402

from src.diagrams.complexity_examples import build_complexity_examples  # noqa: E402


class TestBuildComplexityExamples:
    """Tests for the build_complexity_examples() factory function."""

    @pytest.fixture(scope="class")
    def examples(self):
        """Build examples once per test class."""
        return build_complexity_examples()

    def test_returns_list(self, examples):
        assert isinstance(examples, list)

    def test_non_empty(self, examples):
        assert len(examples) > 0

    def test_has_ten_examples(self, examples):
        """Should have exactly 10 canonical examples."""
        assert len(examples) == 10

    def test_tuple_structure(self, examples):
        """Each example should be a (label, diagram) tuple."""
        for ex in examples:
            assert isinstance(ex, tuple)
            assert len(ex) == 2

    def test_all_labels_are_strings(self, examples):
        for label, _ in examples:
            assert isinstance(label, str)
            assert len(label) > 0

    def test_all_diagrams_reduce_to_sentence_type(self, examples):
        """Every diagram should have codomain equal to Ty('s')."""
        s = Ty("s")
        for label, diagram in examples:
            assert diagram.cod == s, (
                f"Example '{label}' has cod={diagram.cod}, expected {s}"
            )

    def test_all_diagrams_have_empty_domain(self, examples):
        """Every diagram should have Ty() as domain."""
        for label, diagram in examples:
            assert diagram.dom == Ty(), (
                f"Example '{label}' has dom={diagram.dom}, expected Ty()"
            )

    def test_examples_ordered_by_box_count(self, examples):
        """Examples should be ordered by increasing box count."""
        box_counts = [len(diagram.boxes) for _, diagram in examples]
        for i in range(1, len(box_counts)):
            assert box_counts[i] >= box_counts[i - 1], (
                f"Example {i} ({box_counts[i]} boxes) is simpler than "
                f"example {i-1} ({box_counts[i-1]} boxes)"
            )

    def test_unique_labels(self, examples):
        """All labels should be unique."""
        labels = [label for label, _ in examples]
        assert len(labels) == len(set(labels))

    def test_box_counts_vary(self, examples):
        """Not all examples should have the same number of boxes."""
        box_counts = {len(diagram.boxes) for _, diagram in examples}
        assert len(box_counts) > 1

    def test_includes_intransitive(self, examples):
        """Should include an intransitive example."""
        labels_lower = [label.lower() for label, _ in examples]
        assert any("intransitive" in l for l in labels_lower)

    def test_includes_transitive(self, examples):
        """Should include a transitive example."""
        labels_lower = [label.lower() for label, _ in examples]
        assert any("transitive" in l for l in labels_lower)

    def test_first_example_simplest(self, examples):
        """First example should have the fewest boxes."""
        first_count = len(examples[0][1].boxes)
        for _, diagram in examples[1:]:
            assert len(diagram.boxes) >= first_count

    def test_last_example_most_complex(self, examples):
        """Last example should have the most boxes."""
        last_count = len(examples[-1][1].boxes)
        for _, diagram in examples[:-1]:
            assert len(diagram.boxes) <= last_count
