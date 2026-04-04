"""Coverage-boosting tests for visualization.syntactic_sentence_diagrams module.

Targets uncovered branches: empty panel handling, out-of-range arc indices,
default output path, and render_syntactic_panel with custom panels.
"""

import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from src.visualization.syntactic_sentence_diagrams import (
    PANELS,
    CASE_PALETTE,
    _draw_tree_panel,
    render_syntactic_panel,
)

logger = logging.getLogger(__name__)


class TestCasePalette:
    """Tests for CASE_PALETTE constant."""

    def test_has_required_keys(self):
        """Test palette has all required case role keys."""
        required = ["NOM", "ACC", "DAT", "ERG", "ABS", "INS", "V", "ADV"]
        for key in required:
            assert key in CASE_PALETTE, f"Missing palette key: {key}"

    def test_values_are_hex_colors(self):
        """Test all palette values are valid hex color strings."""
        for key, val in CASE_PALETTE.items():
            assert val.startswith("#"), f"{key} color not hex: {val}"
            assert len(val) == 7, f"{key} color wrong length: {val}"


class TestPanelDefinitions:
    """Tests for PANELS constant."""

    def test_panels_count(self):
        """Test the expected number of panels."""
        assert len(PANELS) == 8

    def test_panel_structure(self):
        """Test each panel has required keys."""
        for i, p in enumerate(PANELS):
            assert "title" in p, f"Panel {i} missing title"
            assert "words" in p, f"Panel {i} missing words"
            assert "roles" in p, f"Panel {i} missing roles"
            assert "type_str" in p, f"Panel {i} missing type_str"
            assert "arcs" in p, f"Panel {i} missing arcs"
            assert "desc" in p, f"Panel {i} missing desc"

    def test_words_roles_matching(self):
        """Test words and roles have the same length."""
        for i, p in enumerate(PANELS):
            assert len(p["words"]) == len(p["roles"]), (
                f"Panel {i}: words({len(p['words'])}) != roles({len(p['roles'])})"
            )


class TestDrawTreePanel:
    """Tests for _draw_tree_panel function."""

    def test_empty_words(self):
        """Test early return for empty word list."""
        fig, ax = plt.subplots()
        _draw_tree_panel(ax, [], [], [])
        # Should return immediately without adding patches
        assert len(ax.patches) == 0
        plt.close(fig)

    def test_basic_panel(self):
        """Test drawing a basic intransitive panel."""
        fig, ax = plt.subplots()
        _draw_tree_panel(
            ax,
            words=["Alice", "runs"],
            roles=["NOM", "V"],
            arcs=[(0, 1, "subj")],
        )
        # Should have created 2 circle patches
        assert len(ax.patches) == 2
        plt.close(fig)

    def test_out_of_range_arc(self):
        """Test arc with indices >= n is skipped (line 139-140)."""
        fig, ax = plt.subplots()
        _draw_tree_panel(
            ax,
            words=["Alice"],
            roles=["NOM"],
            arcs=[(0, 5, "bad"), (10, 0, "also_bad")],
        )
        # Should have 1 circle patch (only Alice), arcs silently skipped
        assert len(ax.patches) == 1
        plt.close(fig)

    def test_unknown_role_color(self):
        """Test a role not in CASE_PALETTE falls back to gray."""
        fig, ax = plt.subplots()
        _draw_tree_panel(
            ax,
            words=["x"],
            roles=["UNKNOWN_ROLE"],
            arcs=[],
        )
        # Should have 1 patch with fallback color
        assert len(ax.patches) == 1
        plt.close(fig)

    def test_none_role(self):
        """Test a None role falls back to default gray."""
        fig, ax = plt.subplots()
        _draw_tree_panel(
            ax,
            words=["x"],
            roles=[None],
            arcs=[],
        )
        assert len(ax.patches) == 1
        plt.close(fig)


class TestRenderSyntacticPanel:
    """Tests for render_syntactic_panel function."""

    def test_full_default_render(self, tmp_path):
        """Test rendering with default PANELS."""
        out = tmp_path / "panel.png"
        result = render_syntactic_panel(output_path=out)
        assert result == out
        assert out.exists()
        assert out.stat().st_size > 0

    def test_single_panel_override(self, tmp_path):
        """Test rendering with a single custom panel."""
        custom = [{
            "title": "Test Panel",
            "words": ["A", "B"],
            "roles": ["NOM", "V"],
            "type_str": r"$n \cdot (n^r \cdot s) \Rightarrow s$",
            "desc": "Test description.",
            "arcs": [(0, 1, "test")],
        }]
        out = tmp_path / "custom.png"
        result = render_syntactic_panel(output_path=out, panels=custom)
        assert result == out
        assert out.exists()

    def test_default_output_path(self):
        """Test default output path when None is provided (line 296-297)."""
        result = render_syntactic_panel(panels=[{
            "title": "T",
            "words": ["A"],
            "roles": ["NOM"],
            "type_str": "$x$",
            "desc": "d",
            "arcs": [],
        }])
        assert result == Path("syntactic_case_panel.png")
        # Clean up
        Path("syntactic_case_panel.png").unlink(missing_ok=True)

    def test_large_panel_set(self, tmp_path):
        """Test with more than 4 panels (tests ceil division logic)."""
        custom = [
            {
                "title": f"Panel {i}",
                "words": [f"W{i}"],
                "roles": ["NOM"],
                "type_str": "$x$",
                "desc": f"Panel {i}",
                "arcs": [],
            }
            for i in range(6)
        ]
        out = tmp_path / "large.png"
        result = render_syntactic_panel(output_path=out, panels=custom)
        assert out.exists()
