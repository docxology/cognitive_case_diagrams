"""Tests for discopy_diagrams.py rendering functions.

Validates all 9 render functions and the get_diagram_metrics utility
by saving to tmp_path files. Uses real DisCoPy operations — no mocks.
"""

import pytest
from pathlib import Path

try:
    import discopy  # noqa: F401
    DISCOPY_AVAILABLE = True
except ImportError:
    DISCOPY_AVAILABLE = False


@pytest.mark.skipif(not DISCOPY_AVAILABLE, reason="discopy not installed")
class TestRenderDiscopyTransitive:
    """Tests for render_discopy_transitive()."""

    def test_renders_to_file(self, tmp_path: Path) -> None:
        """render_discopy_transitive saves a PNG file."""
        from src.visualization.discopy_diagrams import render_discopy_transitive
        out = tmp_path / "transitive.png"
        render_discopy_transitive(output_path=out)
        assert out.exists()
        assert out.stat().st_size > 0


@pytest.mark.skipif(not DISCOPY_AVAILABLE, reason="discopy not installed")
class TestRenderDiscopyComposition:
    """Tests for render_discopy_composition()."""

    def test_renders_to_file(self, tmp_path: Path) -> None:
        """Composition diagram (diagram = normal_form) saves a PNG."""
        from src.visualization.discopy_diagrams import render_discopy_composition
        out = tmp_path / "composition.png"
        render_discopy_composition("Alice", "chases", "Bob", output_path=out)
        assert out.exists()
        assert out.stat().st_size > 0


@pytest.mark.skipif(not DISCOPY_AVAILABLE, reason="discopy not installed")
class TestRenderDiscopySnake:
    """Tests for render_discopy_snake()."""

    def test_renders_to_file(self, tmp_path: Path) -> None:
        """Snake equation (left = Id = right) saves a PNG."""
        from src.visualization.discopy_diagrams import render_discopy_snake
        out = tmp_path / "snake.png"
        render_discopy_snake(output_path=out)
        assert out.exists()
        assert out.stat().st_size > 0


@pytest.mark.skipif(not DISCOPY_AVAILABLE, reason="discopy not installed")
class TestRenderDiscopyPassive:
    """Tests for render_discopy_passive()."""

    def test_renders_to_file(self, tmp_path: Path) -> None:
        """Passive diagram saves a PNG."""
        from src.visualization.discopy_diagrams import render_discopy_passive
        out = tmp_path / "passive.png"
        render_discopy_passive(output_path=out)
        assert out.exists()
        assert out.stat().st_size > 0


@pytest.mark.skipif(not DISCOPY_AVAILABLE, reason="discopy not installed")
class TestRenderDiscopySentenceProgression:
    """Tests for render_discopy_sentence_progression()."""

    def test_renders_to_file(self, tmp_path: Path) -> None:
        """Three-sentence progression saves a PNG."""
        from src.visualization.discopy_diagrams import render_discopy_sentence_progression
        out = tmp_path / "progression.png"
        render_discopy_sentence_progression(output_path=out)
        assert out.exists()
        assert out.stat().st_size > 0


@pytest.mark.skipif(not DISCOPY_AVAILABLE, reason="discopy not installed")
class TestRenderDiscopyMultilingual:
    """Tests for render_discopy_multilingual()."""

    def test_renders_to_file(self, tmp_path: Path) -> None:
        """Multilingual diagram panel saves a PNG."""
        from src.visualization.discopy_diagrams import render_discopy_multilingual
        out = tmp_path / "multilingual.png"
        render_discopy_multilingual(output_path=out)
        assert out.exists()
        assert out.stat().st_size > 0


@pytest.mark.skipif(not DISCOPY_AVAILABLE, reason="discopy not installed")
class TestRenderDiscopyDitransitive:
    """Tests for render_discopy_ditransitive()."""

    def test_renders_to_file(self, tmp_path: Path) -> None:
        """Ditransitive diagram saves a PNG."""
        from src.visualization.discopy_diagrams import render_discopy_ditransitive
        out = tmp_path / "ditransitive.png"
        render_discopy_ditransitive(output_path=out)
        assert out.exists()
        assert out.stat().st_size > 0


@pytest.mark.skipif(not DISCOPY_AVAILABLE, reason="discopy not installed")
class TestRenderDiscopyDiscircDiscourse:
    """Tests for render_discopy_discocirc_discourse()."""

    def test_renders_to_file(self, tmp_path: Path) -> None:
        """Two-sentence discourse diagram saves a PNG."""
        from src.visualization.discopy_diagrams import render_discopy_discocirc_discourse
        out = tmp_path / "discourse.png"
        render_discopy_discocirc_discourse(output_path=out)
        assert out.exists()
        assert out.stat().st_size > 0


@pytest.mark.skipif(not DISCOPY_AVAILABLE, reason="discopy not installed")
class TestRenderDiscopyThreeSentenceDiscourse:
    """Tests for render_discopy_three_sentence_discourse()."""

    def test_renders_to_file(self, tmp_path: Path) -> None:
        """Three-sentence discourse saves a PNG."""
        from src.visualization.discopy_diagrams import render_discopy_three_sentence_discourse
        out = tmp_path / "three_discourse.png"
        render_discopy_three_sentence_discourse(output_path=out)
        assert out.exists()
        assert out.stat().st_size > 0


@pytest.mark.skipif(not DISCOPY_AVAILABLE, reason="discopy not installed")
class TestGetDiagramMetrics:
    """Tests for get_diagram_metrics() utility."""

    def test_metrics_structure(self) -> None:
        """get_diagram_metrics returns dict with required keys."""
        from src.visualization.discopy_diagrams import get_diagram_metrics
        from src.diagrams.string_diagram import create_discopy_transitive
        diagram = create_discopy_transitive("Alice", "chases", "Bob")
        metrics = get_diagram_metrics(diagram)
        assert "n_boxes" in metrics
        assert "dom_type" in metrics
        assert "cod_type" in metrics
        assert "n_wires" in metrics

    def test_transitive_box_count(self) -> None:
        """Transitive diagram has 5 boxes (3 words + 2 cups)."""
        from src.visualization.discopy_diagrams import get_diagram_metrics
        from src.diagrams.string_diagram import create_discopy_transitive
        diagram = create_discopy_transitive("Alice", "chases", "Bob")
        metrics = get_diagram_metrics(diagram)
        assert metrics["n_boxes"] == 5

    def test_intransitive_box_count(self) -> None:
        """Intransitive diagram has 3 boxes (2 words + 1 cup)."""
        from src.visualization.discopy_diagrams import get_diagram_metrics
        from src.diagrams.string_diagram import create_discopy_intransitive
        diagram = create_discopy_intransitive("Bob", "runs")
        metrics = get_diagram_metrics(diagram)
        assert metrics["n_boxes"] == 3

    def test_cod_type_is_s(self) -> None:
        """Transitive diagram codomain is type 's'."""
        from src.visualization.discopy_diagrams import get_diagram_metrics
        from src.diagrams.string_diagram import create_discopy_transitive
        diagram = create_discopy_transitive("Alice", "chases", "Bob")
        metrics = get_diagram_metrics(diagram)
        assert metrics["cod_type"] == "s"

    def test_n_wires_positive(self) -> None:
        """Wire count is positive for any valid diagram."""
        from src.visualization.discopy_diagrams import get_diagram_metrics
        from src.diagrams.string_diagram import create_discopy_intransitive
        diagram = create_discopy_intransitive("Bob", "runs")
        metrics = get_diagram_metrics(diagram)
        assert metrics["n_wires"] > 0
