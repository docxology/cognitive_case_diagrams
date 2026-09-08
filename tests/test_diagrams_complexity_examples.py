"""Tests for src/diagrams/complexity_examples.py.

Verifies that build_complexity_examples() returns a well-formed list of
DisCoPy diagram examples with the expected structure. All tests use real
discopy computations — no mocks.
"""

import pytest

# Skip entire module if discopy is not installed
discopy = pytest.importorskip("discopy", reason="discopy not installed")


class TestBuildComplexityExamples:
    """Tests for the build_complexity_examples() factory function."""

    @pytest.fixture(scope="class")
    def examples(self):
        """Build examples once per test class to avoid repeated construction."""
        from src.diagrams.complexity_examples import build_complexity_examples
        return build_complexity_examples()

    def test_returns_list(self, examples):
        """Result must be a list (not generator or tuple)."""
        assert isinstance(examples, list), (
            f"Expected list, got {type(examples).__name__}. "
            "build_complexity_examples() must return a list."
        )

    def test_count_is_ten(self, examples):
        """Must return exactly 10 example sentences."""
        assert len(examples) == 10, (
            f"Expected 10 examples, got {len(examples)}. "
            "The canonical complexity series is fixed at 10 constructions."
        )

    def test_each_item_is_two_tuple(self, examples):
        """Every item must be a (label, diagram) pair."""
        for i, item in enumerate(examples):
            assert isinstance(item, tuple) and len(item) == 2, (
                f"Item {i} is not a 2-tuple: {item!r}. "
                "Each example must be (str_label, discopy.Diagram)."
            )

    def test_all_labels_nonempty_strings(self, examples):
        """Every label must be a non-empty string."""
        for i, (label, _) in enumerate(examples):
            assert isinstance(label, str) and label.strip(), (
                f"Example {i} has a blank or non-string label: {label!r}"
            )

    def test_all_labels_unique(self, examples):
        """Labels must be unique to allow indexed lookup."""
        labels = [label for label, _ in examples]
        assert len(labels) == len(set(labels)), (
            f"Duplicate labels found: {[lab for lab in labels if labels.count(lab) > 1]}"
        )

    def test_diagrams_have_sentence_codomain(self, examples):
        """Every diagram must have codomain Ty('s') (sentence type)."""
        from discopy.rigid import Ty
        s = Ty("s")
        for i, (label, diag) in enumerate(examples):
            assert diag.cod == s, (
                f"Example {i} ('{label}') has codomain {diag.cod!r}, expected {s!r}. "
                "Diagram must reduce to sentence type s after Cup contractions."
            )

    def test_complexity_kappa_non_decreasing(self, examples):
        """The categorical complexity κ(D) = box_count + cup_count must be non-decreasing.

        The RelCl example (#10) uses a pre-contracted RC head Box to substitute
        the relative-clause gap (documented in complexity_examples.py).  This
        means its Cup count alone may not exceed example #9, but its total κ
        metric (box_count + cup_count) is still non-decreasing across the series.
        """
        from discopy.rigid import Cup

        kappas = []
        for label, diag in examples:
            cup_count = sum(1 for box in diag.boxes if isinstance(box, Cup))
            box_count = len(diag.boxes)
            kappas.append((cup_count + box_count, label))

        for i in range(len(kappas) - 1):
            assert kappas[i][0] <= kappas[i + 1][0], (
                f"κ drops from example {i} (κ={kappas[i][0]}, '{kappas[i][1]}') "
                f"to example {i+1} (κ={kappas[i+1][0]}, '{kappas[i+1][1]}'). "
                "Examples should be ordered by non-decreasing total complexity κ = boxes + cups."
            )



def test_diagram_depth_matches_reference_rows() -> None:
    """diagram_depth implements the layer-span longest path (11 reference rows)."""
    import discopy.monoidal as monoidal
    from discopy.rigid import Box, Cap, Cup, Id, Ty

    from src.diagrams.complexity_metrics import diagram_depth
    from src.diagrams.string_diagram import (
        create_swap_passive,
        create_word_diagram_ditransitive,
    )

    x = monoidal.Ty("x")
    f = monoidal.Box("f", x, x)
    n = Ty("n")
    b = Box("b", n, n)
    eta, eps = Cap(n.r, n), Cup(n, n.r)
    rows = [
        (Id(n), 0),
        (Id(Ty()), 0),
        (f >> f, 2),
        (f @ f, 1),
        (f @ f >> monoidal.Id(x) @ f, 2),
        ((eps @ Id(n)) << (Id(n) @ eta), 2),
        (b @ b >> Id(n) @ b, 2),
        (eta, 1),
        ((Id(n) @ eta) >> (eps @ Id(n)), 2),
        (create_swap_passive("Alice", "chases", "Bob"), 3),
        (create_word_diagram_ditransitive("Alice", "gives", "Bob", "book"), 3),
    ]
    for index, (diagram, expected) in enumerate(rows):
        assert diagram_depth(diagram) == expected, f"reference row {index} failed"
