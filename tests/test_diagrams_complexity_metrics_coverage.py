"""Comprehensive tests for complexity_metrics module.

Tests all functions in src/diagrams/complexity_metrics.py to bring
coverage above 90%. Uses real DisCoPy diagrams (zero-mock policy).
"""

import pytest

discopy = pytest.importorskip("discopy", reason="discopy required")
from discopy.rigid import Ty, Box, Cup, Cap, Id  # noqa: E402

from src.diagrams.complexity_metrics import (  # noqa: E402
    DiagramMetrics,
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
)


# ── Fixtures ──────────────────────────────────────────────


@pytest.fixture
def n():
    return Ty("n")


@pytest.fixture
def s():
    return Ty("s")


@pytest.fixture
def transitive_diagram(n, s):
    """Alice chases Bob — standard transitive sentence."""
    alice = Box("Alice", Ty(), n)
    chases = Box("chases", Ty(), n.r @ s @ n.l)
    bob = Box("Bob", Ty(), n)
    words = alice @ chases @ bob
    return words >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)


@pytest.fixture
def intransitive_diagram(n, s):
    """Bob runs — intransitive sentence."""
    bob = Box("Bob", Ty(), n)
    runs = Box("runs", Ty(), n.r @ s)
    return bob @ runs >> Cup(n, n.r) @ Id(s)


@pytest.fixture
def identity_diagram(n):
    """Identity diagram on n."""
    return Id(n)


# ── DiagramMetrics dataclass ─────────────────────────────


class TestDiagramMetrics:
    def test_default_construction(self):
        m = DiagramMetrics(name="test")
        assert m.name == "test"
        assert m.box_count == 0
        assert m.word_count == 0
        assert m.cup_count == 0
        assert m.cap_count == 0
        assert m.is_normal_form is False
        assert m.normal_form_box_count == 0
        assert m.dom_type == ""
        assert m.cod_type == ""

    def test_custom_construction(self):
        m = DiagramMetrics(
            name="custom",
            box_count=5,
            word_count=3,
            cup_count=2,
            cap_count=0,
            is_normal_form=True,
            normal_form_box_count=5,
            dom_type="Ty()",
            cod_type="Ty(s)",
        )
        assert m.box_count == 5
        assert m.is_normal_form is True


# ── Counting functions ────────────────────────────────────


class TestCountBoxes:
    def test_transitive_count(self, transitive_diagram):
        # 3 Word boxes + 2 Cup = 5 total
        assert count_boxes(transitive_diagram) == 5

    def test_intransitive_count(self, intransitive_diagram):
        # 2 Word boxes + 1 Cup = 3 total
        assert count_boxes(intransitive_diagram) == 3

    def test_identity_count(self, identity_diagram):
        assert count_boxes(identity_diagram) == 0


class TestCountWords:
    def test_transitive_words(self, transitive_diagram):
        # 3 Word boxes (Alice, chases, Bob) excluding cups
        assert count_words(transitive_diagram) == 3

    def test_intransitive_words(self, intransitive_diagram):
        assert count_words(intransitive_diagram) == 2

    def test_identity_words(self, identity_diagram):
        assert count_words(identity_diagram) == 0


class TestCountCups:
    def test_transitive_cups(self, transitive_diagram):
        assert count_cups(transitive_diagram) == 2

    def test_intransitive_cups(self, intransitive_diagram):
        assert count_cups(intransitive_diagram) == 1

    def test_identity_cups(self, identity_diagram):
        assert count_cups(identity_diagram) == 0


class TestCountCaps:
    def test_transitive_no_caps(self, transitive_diagram):
        assert count_caps(transitive_diagram) == 0

    def test_cap_diagram(self, n):
        cap_diag = Cap(n, n.l)
        assert count_caps(cap_diag) == 1


# ── Normal form functions ─────────────────────────────────


class TestNormalForm:
    def test_compute_normal_form(self, transitive_diagram):
        nf = compute_normal_form(transitive_diagram)
        assert nf is not None
        assert nf.cod == transitive_diagram.cod

    def test_is_in_normal_form_identity(self, identity_diagram):
        assert is_in_normal_form(identity_diagram) is True

    def test_normal_form_preserves_codomain(self, transitive_diagram):
        nf = compute_normal_form(transitive_diagram)
        assert nf.cod == transitive_diagram.cod


# ── Diagram equality ─────────────────────────────────────


class TestDiagramsEqual:
    def test_identical_diagrams_equal(self, n, s):
        """Two identically constructed diagrams should be equal."""
        d1 = Box("A", Ty(), n) @ Box("V", Ty(), n.r @ s @ n.l) @ Box("B", Ty(), n)
        d1 = d1 >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
        d2 = Box("A", Ty(), n) @ Box("V", Ty(), n.r @ s @ n.l) @ Box("B", Ty(), n)
        d2 = d2 >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
        assert diagrams_equal(d1, d2) is True

    def test_different_diagrams_not_equal(self, n, s):
        d1 = Box("Alice", Ty(), n) @ Box("chases", Ty(), n.r @ s @ n.l) @ Box("Bob", Ty(), n)
        d1 = d1 >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
        d2 = Box("Bob", Ty(), n) @ Box("runs", Ty(), n.r @ s)
        d2 = d2 >> Cup(n, n.r) @ Id(s)
        assert diagrams_equal(d1, d2) is False

    def test_self_equality(self, transitive_diagram):
        assert diagrams_equal(transitive_diagram, transitive_diagram) is True


# ── Analyze diagram ──────────────────────────────────────


class TestAnalyzeDiagram:
    def test_analyze_transitive(self, transitive_diagram):
        metrics = analyze_diagram(transitive_diagram, name="Alice chases Bob")
        assert metrics.name == "Alice chases Bob"
        assert metrics.box_count == 5
        assert metrics.word_count == 3
        assert metrics.cup_count == 2
        assert metrics.cap_count == 0
        assert metrics.normal_form_box_count >= 0
        assert isinstance(metrics.dom_type, str)
        assert isinstance(metrics.cod_type, str)

    def test_analyze_intransitive(self, intransitive_diagram):
        metrics = analyze_diagram(intransitive_diagram, name="Bob runs")
        assert metrics.box_count == 3
        assert metrics.word_count == 2
        assert metrics.cup_count == 1

    def test_analyze_identity(self, identity_diagram):
        metrics = analyze_diagram(identity_diagram, name="identity")
        assert metrics.box_count == 0
        assert metrics.is_normal_form is True

    def test_analyze_empty_name(self, transitive_diagram):
        metrics = analyze_diagram(transitive_diagram)
        assert metrics.name == ""


# ── Syntactic complexity score ────────────────────────────


class TestSyntacticComplexityScore:
    def test_transitive_complexity(self, transitive_diagram):
        score = syntactic_complexity_score(transitive_diagram)
        # 3 words + 0.5*2 cups + 0.25*0 caps = 4.0
        assert score == pytest.approx(4.0)

    def test_intransitive_complexity(self, intransitive_diagram):
        score = syntactic_complexity_score(intransitive_diagram)
        # 2 words + 0.5*1 cup + 0.25*0 caps = 2.5
        assert score == pytest.approx(2.5)

    def test_identity_complexity(self, identity_diagram):
        score = syntactic_complexity_score(identity_diagram)
        assert score == pytest.approx(0.0)

    def test_transitive_more_complex_than_intransitive(
        self, transitive_diagram, intransitive_diagram
    ):
        t_score = syntactic_complexity_score(transitive_diagram)
        i_score = syntactic_complexity_score(intransitive_diagram)
        assert t_score > i_score


# ── Compare diagrams ──────────────────────────────────────


class TestCompareDiagrams:
    def test_compare_multiple(self, transitive_diagram, intransitive_diagram):
        results = compare_diagrams([
            ("transitive", transitive_diagram),
            ("intransitive", intransitive_diagram),
        ])
        assert len(results) == 2
        assert results[0].name == "transitive"
        assert results[1].name == "intransitive"
        assert results[0].box_count > results[1].box_count

    def test_compare_empty(self):
        results = compare_diagrams([])
        assert results == []

    def test_compare_single(self, transitive_diagram):
        results = compare_diagrams([("single", transitive_diagram)])
        assert len(results) == 1
        assert results[0].name == "single"
