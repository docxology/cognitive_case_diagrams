"""Tests for src.visualization.complexity_plots module.

Validates render_complexity_comparison, render_normal_form_comparison,
and render_syntactic_complexity_radar produce valid output files.
"""

import logging
import os

import pytest

from src.visualization.complexity_plots import (
    render_complexity_comparison,
    render_normal_form_comparison,
    render_syntactic_complexity_radar,
)

logger = logging.getLogger(__name__)


class TestRenderComplexityComparison:
    """Tests for render_complexity_comparison()."""

    def test_returns_path(self, tmp_path):
        """render_complexity_comparison returns a file path string."""
        out = str(tmp_path / "complexity.png")
        result = render_complexity_comparison(
            labels=["Intransitive", "Transitive", "Ditransitive"],
            box_counts=[3, 5, 7],
            word_counts=[2, 3, 4],
            cup_counts=[1, 2, 3],
            sentences=["Alice runs", "Alice sees Bob", "Alice gives Bob cake"],
            output_path=out,
        )
        assert isinstance(result, str)
        assert os.path.exists(result)
        logger.info("render_complexity_comparison saved to %s", result)

    def test_creates_file(self, tmp_path):
        """Output file is created and non-empty."""
        out = str(tmp_path / "complexity.png")
        render_complexity_comparison(
            labels=["A", "B"],
            box_counts=[3, 5],
            word_counts=[2, 3],
            cup_counts=[1, 2],
            sentences=["s1", "s2"],
            output_path=out,
        )
        assert os.path.getsize(out) > 0


class TestRenderNormalFormComparison:
    """Tests for render_normal_form_comparison()."""

    def test_returns_path(self, tmp_path):
        """render_normal_form_comparison returns a file path string."""
        out = str(tmp_path / "normal_form.png")
        result = render_normal_form_comparison(
            labels=["Transitive", "Passive"],
            original_counts=[5, 7],
            normal_form_counts=[3, 4],
            output_path=out,
        )
        assert isinstance(result, str)
        assert os.path.exists(result)

    def test_creates_file(self, tmp_path):
        """Output file is created and non-empty."""
        out = str(tmp_path / "normal_form.png")
        render_normal_form_comparison(
            labels=["A"],
            original_counts=[5],
            normal_form_counts=[3],
            output_path=out,
        )
        assert os.path.getsize(out) > 0


class TestRenderSyntacticComplexityRadar:
    """Tests for render_syntactic_complexity_radar()."""

    def test_returns_path(self, tmp_path):
        """render_syntactic_complexity_radar returns a file path string."""
        out = str(tmp_path / "radar.png")
        result = render_syntactic_complexity_radar(
            labels=["Boxes", "Cups", "Depth", "Width"],
            metrics={
                "Transitive": [5, 2, 3, 4],
                "Ditransitive": [7, 3, 4, 5],
            },
            output_path=out,
        )
        assert isinstance(result, str)
        assert os.path.exists(result)

    def test_creates_file(self, tmp_path):
        """Output file is created and non-empty."""
        out = str(tmp_path / "radar.png")
        render_syntactic_complexity_radar(
            labels=["A", "B", "C"],
            metrics={"Test": [1, 2, 3]},
            output_path=out,
        )
        assert os.path.getsize(out) > 0
        logger.info("Radar chart created at %s", out)
