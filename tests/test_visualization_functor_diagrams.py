"""Tests for src.visualization.functor_diagrams module.

Validates render_functor_diagram produces valid matplotlib figures
with a single-axes dual-panel layout and functor arrows.
"""

import logging

import matplotlib
import matplotlib.patches as mpatches
import pytest

from src.case_systems.functor import accusative_to_ergative_functor
from src.visualization.functor_diagrams import render_functor_diagram

logger = logging.getLogger(__name__)


class TestRenderFunctorDiagram:
    """Tests for render_functor_diagram()."""

    def test_returns_figure(self):
        """render_functor_diagram returns a matplotlib Figure."""
        functor = accusative_to_ergative_functor()
        fig = render_functor_diagram(functor)
        assert isinstance(fig, matplotlib.figure.Figure)
        logger.info("render_functor_diagram returned valid Figure")

    def test_single_axes_shared_coordinate_system(self):
        """Single axes holds both panels so functor arrows share one transform."""
        functor = accusative_to_ergative_functor()
        fig = render_functor_diagram(functor)
        assert len(fig.get_axes()) == 1

    def test_functor_fancy_arrow_patch_count_matches_object_map(self):
        """One FancyArrowPatch per object_map entry for canonical Acc→Erg functor."""
        functor = accusative_to_ergative_functor()
        fig = render_functor_diagram(functor)
        ax = fig.axes[0]
        n_arrows = sum(
            1 for p in ax.patches if isinstance(p, mpatches.FancyArrowPatch)
        )
        assert n_arrows == len(functor.object_map)

    def test_custom_title(self):
        """Custom title is applied to the suptitle."""
        functor = accusative_to_ergative_functor()
        title = "Test Functor Title"
        fig = render_functor_diagram(functor, title=title)
        assert title in fig._suptitle.get_text()

    def test_save_to_file(self, tmp_path):
        """Saves output to the specified path."""
        functor = accusative_to_ergative_functor()
        out = tmp_path / "functor.png"
        fig = render_functor_diagram(functor, output_path=out)
        assert out.exists()
        assert out.stat().st_size > 0
        logger.info("Saved functor diagram to %s (%d bytes)", out, out.stat().st_size)
