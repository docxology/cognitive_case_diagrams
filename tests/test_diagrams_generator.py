"""Tests for the visualization and diagram generation pipeline.

Validates that all rendering functions produce matplotlib figures
without errors and that the orchestration script generates the
9 canonical output files.
"""

import pytest
import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

from src.case_systems.case_category import standard_case_category, minimal_case_category
from src.enriched_cat.enriched import standard_enriched_category
from src.case_systems.functor import accusative_to_ergative_functor, tripartite_functor
from src.diagrams.string_diagram import Sentence, Discourse
from src.visualization.category_diagrams import (
    render_case_category,
    render_alignment_comparison,
    render_composition_triangle,
)
from src.visualization.enriched_diagrams import render_enriched_heatmap
from src.visualization.functor_diagrams import render_functor_diagram
from src.visualization.string_diagrams import (
    render_discocat_sentence,
    render_discourse_diagram,
    render_discocirc_discourse,
    render_three_sentence_discourse,
)


class TestCategoryDiagrams:
    """Tests for category diagram rendering."""

    def test_standard_category(self):
        """Render standard 8-case category."""
        cat = standard_case_category()
        fig = render_case_category(cat)
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_minimal_category(self):
        """Render minimal 3-role category."""
        cat = minimal_case_category()
        fig = render_case_category(cat)
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_save_standard(self):
        """Save standard category to file."""
        cat = standard_case_category()
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "standard.png"
            render_case_category(cat, output_path=path)
            assert path.exists()
            assert path.stat().st_size > 0

    def test_alignment_comparison(self):
        """Render alignment comparison figure."""
        fig = render_alignment_comparison()
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_save_alignment(self):
        """Save alignment comparison to file."""
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "alignment.png"
            render_alignment_comparison(output_path=path)
            assert path.exists()

    def test_composition_triangle(self):
        """Render composition triangle."""
        fig = render_composition_triangle()
        assert isinstance(fig, matplotlib.figure.Figure)


class TestEnrichedDiagrams:
    """Tests for enriched category heatmap rendering."""

    def test_heatmap(self):
        """Render enriched heatmap."""
        cat = standard_enriched_category()
        fig = render_enriched_heatmap(cat)
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_save_heatmap(self):
        """Save heatmap to file."""
        cat = standard_enriched_category()
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "heatmap.png"
            render_enriched_heatmap(cat, output_path=path)
            assert path.exists()
            assert path.stat().st_size > 0


class TestFunctorDiagrams:
    """Tests for functor diagram rendering."""

    def test_acc_to_erg(self):
        """Render accusative-to-ergative functor."""
        functor = accusative_to_ergative_functor()
        fig = render_functor_diagram(functor)
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_tripartite(self):
        """Render tripartite functor."""
        functor = tripartite_functor()
        fig = render_functor_diagram(functor)
        assert isinstance(fig, matplotlib.figure.Figure)


class TestStringDiagrams:
    """Tests for string diagram rendering."""

    def test_discocat_transitive(self):
        """Render DisCoCat transitive sentence."""
        sent = Sentence.transitive("Alice", "chases", "Bob")
        fig = render_discocat_sentence(sent)
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_discocat_intransitive(self):
        """Render DisCoCat intransitive sentence."""
        sent = Sentence.intransitive("Bob", "runs")
        fig = render_discocat_sentence(sent)
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_discourse_two_sentence(self):
        """Render two-sentence discourse."""
        disc = Discourse.two_sentence("Alice", "chases", "Bob", "Bob", "runs")
        fig = render_discourse_diagram(disc)
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_discocirc_discourse(self):
        """Render canonical DisCoCirc discourse."""
        fig = render_discocirc_discourse()
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_three_sentence_discourse(self):
        """Render three-sentence role reversal."""
        fig = render_three_sentence_discourse()
        assert isinstance(fig, matplotlib.figure.Figure)


class TestDiscoPyDiagrams:
    """Tests for DisCoPy diagram rendering (requires discopy).

    DisCoPy render functions use draw(path=...) to save directly to file,
    so tests verify file creation and non-zero size.
    """

    @pytest.fixture(autouse=True)
    def check_discopy(self):
        pytest.importorskip("discopy")

    def test_discopy_transitive(self):
        from src.visualization.discopy_diagrams import render_discopy_transitive
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "transitive.png"
            render_discopy_transitive(output_path=path)
            assert path.exists()
            assert path.stat().st_size > 1000  # Real diagram, not blank

    def test_discopy_composition(self):
        from src.visualization.discopy_diagrams import render_discopy_composition
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "composition.png"
            render_discopy_composition(output_path=path)
            assert path.exists()
            assert path.stat().st_size > 1000

    def test_discopy_snake(self):
        from src.visualization.discopy_diagrams import render_discopy_snake
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "snake.png"
            render_discopy_snake(output_path=path)
            assert path.exists()
            assert path.stat().st_size > 1000

    def test_discopy_passive(self):
        from src.visualization.discopy_diagrams import render_discopy_passive
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "passive.png"
            render_discopy_passive(output_path=path)
            assert path.exists()
            assert path.stat().st_size > 1000

    def test_discopy_sentence_progression(self):
        from src.visualization.discopy_diagrams import render_discopy_sentence_progression
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "progression.png"
            render_discopy_sentence_progression(output_path=path)
            assert path.exists()
            assert path.stat().st_size > 1000

    def test_discopy_multilingual(self):
        from src.visualization.discopy_diagrams import render_discopy_multilingual
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "multilingual.png"
            render_discopy_multilingual(output_path=path)
            assert path.exists()
            assert path.stat().st_size > 1000

    def test_discopy_ditransitive(self):
        from src.visualization.discopy_diagrams import render_discopy_ditransitive
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "ditransitive.png"
            render_discopy_ditransitive(output_path=path)
            assert path.exists()
            assert path.stat().st_size > 1000

    def test_discopy_discourse(self):
        from src.visualization.discopy_diagrams import render_discopy_discocirc_discourse
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "discourse.png"
            render_discopy_discocirc_discourse(output_path=path)
            assert path.exists()
            assert path.stat().st_size > 1000

    def test_discopy_three_sentence(self):
        from src.visualization.discopy_diagrams import render_discopy_three_sentence_discourse
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "three_sent.png"
            render_discopy_three_sentence_discourse(output_path=path)
            assert path.exists()
            assert path.stat().st_size > 1000

    def test_get_diagram_metrics(self):
        from src.diagrams.string_diagram import create_discopy_transitive
        from src.visualization.discopy_diagrams import get_diagram_metrics
        diagram = create_discopy_transitive("Alice", "chases", "Bob")
        metrics = get_diagram_metrics(diagram)
        # 3 word boxes + 2 cup boxes = 5 in DisCoPy
        assert metrics["n_boxes"] == 5
        assert "s" in metrics["cod_type"]
