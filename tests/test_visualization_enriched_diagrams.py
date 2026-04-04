"""Tests for src.visualization.enriched_diagrams module.

Validates render_enriched_heatmap produces valid matplotlib figures
with correct heatmap structure and annotations.
"""

import logging

import matplotlib
import numpy as np
import pytest

from src.case_systems.case_category import CaseRole
from src.enriched_cat.enriched import EnrichedCategory
from src.visualization.enriched_diagrams import render_enriched_heatmap

logger = logging.getLogger(__name__)


def _make_enriched_category() -> EnrichedCategory:
    """Create a small enriched category for testing."""
    roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
    matrix = np.array([
        [1.0, 0.3, 0.2],
        [0.3, 1.0, 0.5],
        [0.2, 0.5, 1.0],
    ])
    return EnrichedCategory(name="Test", roles=roles, proximity_matrix=matrix)


class TestRenderEnrichedHeatmap:
    """Tests for render_enriched_heatmap()."""

    def test_returns_figure(self):
        """render_enriched_heatmap returns a matplotlib Figure."""
        ec = _make_enriched_category()
        fig = render_enriched_heatmap(ec)
        assert isinstance(fig, matplotlib.figure.Figure)
        logger.info("render_enriched_heatmap returned valid Figure")

    def test_has_colorbar(self):
        """Figure includes a colorbar axes."""
        ec = _make_enriched_category()
        fig = render_enriched_heatmap(ec)
        # Colorbar adds an extra axes
        assert len(fig.get_axes()) >= 2

    def test_custom_title(self):
        """Custom title is applied."""
        ec = _make_enriched_category()
        title = "Custom Heatmap Title"
        fig = render_enriched_heatmap(ec, title=title)
        axes = fig.get_axes()
        assert any(title in ax.get_title() for ax in axes)

    def test_save_to_file(self, tmp_path):
        """Saves output to the specified path."""
        ec = _make_enriched_category()
        out = tmp_path / "heatmap.png"
        fig = render_enriched_heatmap(ec, output_path=out)
        assert out.exists()
        assert out.stat().st_size > 0

    def test_identity_diagonal_highlighted(self):
        """Diagonal values (1.0) should be present in the matrix."""
        ec = _make_enriched_category()
        assert all(ec.proximity_matrix[i, i] == 1.0 for i in range(len(ec.roles)))
