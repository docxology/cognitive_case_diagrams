"""Tests for src.visualization.category_diagrams module.

Validates render_case_category, render_alignment_comparison,
and render_composition_triangle produce valid matplotlib figures
with correct structural properties.
"""

import logging
import tempfile
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pytest

from src.case_systems.case_category import (
    CaseCategory, CaseRole, Morphism,
    standard_case_category, minimal_case_category,
    introductory_case_category,
)
from src.visualization.category_diagrams import (
    _prohibited_edges_to_draw,
    render_case_category,
    render_alignment_comparison,
    render_composition_triangle,
)
from src.visualization.styles import mathtext_safe_arrows

logger = logging.getLogger(__name__)


class TestRenderCaseCategory:
    """Tests for render_case_category()."""

    def test_returns_figure(self):
        """render_case_category returns a matplotlib Figure."""
        cat = standard_case_category()
        fig = render_case_category(cat)
        assert isinstance(fig, matplotlib.figure.Figure)
        logger.info("render_case_category returned valid Figure")

    def test_minimal_category(self):
        """Renders correctly with a minimal 3-role category."""
        cat = minimal_case_category()
        fig = render_case_category(cat)
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_with_title_override(self):
        """Custom title is applied to the figure."""
        cat = standard_case_category()
        title = "Test Custom Title"
        fig = render_case_category(cat, title=title)
        axes = fig.get_axes()
        assert any(title in ax.get_title() for ax in axes)

    def test_admissibility_off(self):
        """Renders without admissibility annotations."""
        cat = standard_case_category()
        fig = render_case_category(cat, show_admissibility=False)
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_save_to_file(self, tmp_path):
        """Saves output to the specified path."""
        cat = standard_case_category()
        out = tmp_path / "test_category.png"
        fig = render_case_category(cat, output_path=out)
        assert out.exists()
        assert out.stat().st_size > 0
        logger.info("Saved category diagram to %s (%d bytes)", out, out.stat().st_size)

    def test_has_axes(self):
        """Figure contains at least one axes."""
        cat = standard_case_category()
        fig = render_case_category(cat)
        assert len(fig.get_axes()) >= 1

    def test_scatter_node_count_matches_category_objects(self):
        """NetworkX node draw produces one scatter point per case role (structural check)."""
        for cat in (minimal_case_category(), standard_case_category()):
            fig = render_case_category(cat)
            ax = fig.axes[0]
            collections = [
                c for c in ax.collections
                if hasattr(c, "get_offsets") and c.get_offsets().size > 0
            ]
            assert len(collections) >= 1
            n_drawn = int(collections[0].get_offsets().shape[0])
            assert n_drawn == len(cat.objects)
            plt.close(fig)

    def test_extra_prohibited_renders(self, tmp_path):
        """Optional prohibited edges render when endpoints exist in the graph."""
        cat = minimal_case_category()
        out = tmp_path / "extra_prohibited.png"
        fig = render_case_category(
            cat,
            output_path=out,
            extra_prohibited=[
                (CaseRole.ACC, CaseRole.NOM, mathtext_safe_arrows("patient→agent")),
            ],
        )
        assert isinstance(fig, matplotlib.figure.Figure)
        assert out.exists()

    def test_prohibited_dedupes_source_target(self):
        """Same (source, target) from default and extra appears once."""
        nodes = {"VOC", "NOM", "ACC"}
        dup_extra = [
            (CaseRole.VOC, CaseRole.NOM, "dup"),
        ]
        edges = _prohibited_edges_to_draw(nodes, dup_extra)
        voc_nom = [e for e in edges if e[0] == "VOC" and e[1] == "NOM"]
        assert len(voc_nom) == 1

    def test_node_positions_must_cover_all_nodes(self):
        """Incomplete node_positions raises ValueError listing missing nodes."""
        cat = minimal_case_category()
        with pytest.raises(ValueError, match="missing"):
            render_case_category(
                cat,
                node_positions={"NOM": (0.0, 0.0), "ACC": (1.0, 0.0)},
            )

    def test_custom_positions_prefix_and_connectionstyle_save_png(self, tmp_path):
        """Intro-style kwargs produce a non-empty PNG (fig:case-minimal pipeline)."""
        cat = introductory_case_category()
        positions = {
            "NOM": (0.0, 1.0),
            "INS": (0.92, -0.52),
            "ACC": (-0.92, -0.52),
            "VOC": (-0.98, 0.48),
        }
        prefix = {
            ("NOM", "INS"): "f: ",
            ("INS", "ACC"): "g: ",
            ("NOM", "ACC"): "h=g\u2218f: ",
        }
        conn = {
            ("NOM", "INS"): "arc3,rad=0.05",
            ("INS", "ACC"): "arc3,rad=0.05",
            ("NOM", "ACC"): "arc3,rad=-0.28",
            ("NOM", "VOC"): "arc3,rad=0.12",
        }
        out = tmp_path / "case_minimal_style.png"
        fig = render_case_category(
            cat,
            output_path=out,
            node_positions=positions,
            edge_label_prefix=prefix,
            licensed_connectionstyle=conn,
            extra_prohibited=[
                (CaseRole.ACC, CaseRole.NOM, mathtext_safe_arrows("patient→agent")),
            ],
        )
        assert isinstance(fig, matplotlib.figure.Figure)
        assert out.exists()
        assert out.stat().st_size > 8000


class TestRenderAlignmentComparison:
    """Tests for render_alignment_comparison()."""

    def test_returns_figure(self):
        """render_alignment_comparison returns a Figure."""
        fig = render_alignment_comparison()
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_three_subplots(self):
        """Creates 3 subplots (accusative, ergative, tripartite)."""
        fig = render_alignment_comparison()
        axes = fig.get_axes()
        assert len(axes) == 3
        logger.info("Alignment comparison has %d subplots", len(axes))

    def test_save_to_file(self, tmp_path):
        """Saves output to the specified path."""
        out = tmp_path / "alignment.png"
        fig = render_alignment_comparison(output_path=out)
        assert out.exists()


class TestRenderCompositionTriangle:
    """Tests for render_composition_triangle()."""

    def test_returns_figure(self):
        """render_composition_triangle returns a Figure."""
        fig = render_composition_triangle()
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_has_title(self):
        """Figure has a title containing 'Composition'."""
        fig = render_composition_triangle()
        axes = fig.get_axes()
        assert any("Composition" in ax.get_title() for ax in axes)

    def test_save_to_file(self, tmp_path):
        """Saves output to the specified path."""
        out = tmp_path / "composition.png"
        fig = render_composition_triangle(output_path=out)
        assert out.exists()
