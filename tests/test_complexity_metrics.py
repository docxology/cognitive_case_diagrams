"""Tests for diagram complexity metrics module.

Validates box counting, normal form computation, diagram equality,
syntactic complexity scoring, and comparison across diagram types.
All tests use real DisCoPy operations — no mocks.
"""

import pytest

try:
    from discopy.rigid import Ty, Box, Cup, Cap, Id, Diagram
    DISCOPY_AVAILABLE = True
except ImportError:
    DISCOPY_AVAILABLE = False

from src.diagrams.complexity_metrics import (
    count_boxes,
    count_words,
    count_cups,
    count_caps,
    compute_normal_form,
    is_in_normal_form,
    diagrams_equal,
    analyze_diagram,
    syntactic_complexity_score,
    compare_diagrams,
    DiagramMetrics,
)


def _make_transitive() -> "Diagram":
    """Create 'child broke vase' transitive diagram."""
    n, s = Ty("n"), Ty("s")
    child = Box("child", Ty(), n)
    broke = Box("broke", Ty(), n.r @ s @ n.l)
    vase = Box("vase", Ty(), n)
    words = child @ broke @ vase
    cups = Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
    return words >> cups


def _make_intransitive() -> "Diagram":
    """Create 'child runs' intransitive diagram."""
    n, s = Ty("n"), Ty("s")
    child = Box("child", Ty(), n)
    runs = Box("runs", Ty(), n.r @ s)
    words = child @ runs
    cups = Cup(n, n.r) @ Id(s)
    return words >> cups


def _make_snake() -> "Diagram":
    """Create left snake equation diagram: x @ Cap(x.r, x) >> Cup(x, x.r) @ x."""
    x = Ty("x")
    return x @ Cap(x.r, x) >> Cup(x, x.r) @ x


@pytest.mark.skipif(not DISCOPY_AVAILABLE, reason="discopy not installed")
class TestBoxCounting:
    """Tests for box and component counting."""

    def test_count_boxes_transitive(self) -> None:
        """Transitive diagram has 5 boxes (3 words + 2 cups)."""
        d = _make_transitive()
        assert count_boxes(d) == 5

    def test_count_boxes_intransitive(self) -> None:
        """Intransitive diagram has 3 boxes (2 words + 1 cup)."""
        d = _make_intransitive()
        assert count_boxes(d) == 3

    def test_count_words_transitive(self) -> None:
        """Transitive has 3 word boxes."""
        d = _make_transitive()
        assert count_words(d) == 3

    def test_count_words_intransitive(self) -> None:
        """Intransitive has 2 word boxes."""
        d = _make_intransitive()
        assert count_words(d) == 2

    def test_count_cups_transitive(self) -> None:
        """Transitive has 2 cup contractions."""
        d = _make_transitive()
        assert count_cups(d) == 2

    def test_count_cups_intransitive(self) -> None:
        """Intransitive has 1 cup contraction."""
        d = _make_intransitive()
        assert count_cups(d) == 1

    def test_count_caps_snake(self) -> None:
        """Snake equation has 1 cap."""
        d = _make_snake()
        assert count_caps(d) == 1

    def test_count_cups_snake(self) -> None:
        """Snake equation has 1 cup."""
        d = _make_snake()
        assert count_cups(d) == 1


@pytest.mark.skipif(not DISCOPY_AVAILABLE, reason="discopy not installed")
class TestNormalForm:
    """Tests for normal form computation."""

    def test_compute_normal_form(self) -> None:
        """Normal form computation returns a diagram."""
        d = _make_transitive()
        nf = compute_normal_form(d)
        assert isinstance(nf, Diagram)

    def test_snake_normal_form_is_identity(self) -> None:
        """Snake equation normalizes to identity wire."""
        x = Ty("x")
        snake = x @ Cap(x.r, x) >> Cup(x, x.r) @ x
        nf = compute_normal_form(snake)
        assert nf == Id(x)

    def test_is_normal_form_identity(self) -> None:
        """Identity diagram is in normal form."""
        x = Ty("x")
        assert is_in_normal_form(Id(x))

    def test_transitive_preserves_types(self) -> None:
        """Normal form preserves domain and codomain types."""
        d = _make_transitive()
        nf = compute_normal_form(d)
        assert nf.dom == d.dom
        assert nf.cod == d.cod


@pytest.mark.skipif(not DISCOPY_AVAILABLE, reason="discopy not installed")
class TestDiagramEquality:
    """Tests for diagram equality via normal forms."""

    def test_same_diagram_equal(self) -> None:
        """A diagram equals itself."""
        d = _make_transitive()
        assert diagrams_equal(d, d)

    def test_different_diagrams_not_equal(self) -> None:
        """Different sentence structures are not equal."""
        d1 = _make_transitive()
        d2 = _make_intransitive()
        assert not diagrams_equal(d1, d2)


@pytest.mark.skipif(not DISCOPY_AVAILABLE, reason="discopy not installed")
class TestAnalyzeDiagram:
    """Tests for comprehensive diagram analysis."""

    def test_analyze_transitive(self) -> None:
        """Analyze transitive diagram produces valid metrics."""
        d = _make_transitive()
        m = analyze_diagram(d, "transitive")
        assert isinstance(m, DiagramMetrics)
        assert m.name == "transitive"
        assert m.box_count == 5
        assert m.word_count == 3
        assert m.cup_count == 2
        assert m.cod_type == "s"

    def test_analyze_intransitive(self) -> None:
        """Analyze intransitive diagram."""
        d = _make_intransitive()
        m = analyze_diagram(d, "intransitive")
        assert m.box_count == 3
        assert m.word_count == 2
        assert m.cup_count == 1

    def test_syntactic_complexity_transitive(self) -> None:
        """Transitive complexity: 3 + 0.5*2 = 4.0."""
        d = _make_transitive()
        score = syntactic_complexity_score(d)
        assert score == pytest.approx(4.0)

    def test_syntactic_complexity_intransitive(self) -> None:
        """Intransitive complexity: 2 + 0.5*1 = 2.5."""
        d = _make_intransitive()
        score = syntactic_complexity_score(d)
        assert score == pytest.approx(2.5)

    def test_transitive_more_complex_than_intransitive(self) -> None:
        """Transitive should have higher complexity than intransitive."""
        t = syntactic_complexity_score(_make_transitive())
        i = syntactic_complexity_score(_make_intransitive())
        assert t > i


@pytest.mark.skipif(not DISCOPY_AVAILABLE, reason="discopy not installed")
class TestCompareDiagrams:
    """Tests for multi-diagram comparison."""

    def test_compare_two_diagrams(self) -> None:
        """Compare transitive and intransitive produces 2 results."""
        diagrams = [
            ("transitive", _make_transitive()),
            ("intransitive", _make_intransitive()),
        ]
        results = compare_diagrams(diagrams)
        assert len(results) == 2
        assert results[0].box_count > results[1].box_count

    def test_compare_empty_list(self) -> None:
        """Empty comparison returns empty list."""
        results = compare_diagrams([])
        assert results == []
