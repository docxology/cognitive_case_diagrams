"""Tests for the syntactic sentence diagrams visualization module.

Verifies that the syntactic case assignment panel figure is generated
correctly as a PNG file with the expected structure and content.
All tests use real file I/O and matplotlib rendering — no mocks.
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Ensure the project src is on the path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.visualization.syntactic_sentence_diagrams import (
    PANELS,
    render_syntactic_panel,
)


class TestSyntacticDiagramsPanelData:
    """Tests for the PANELS data structure correctness."""

    def test_panel_count_is_eight(self):
        """The figure must contain exactly 8 panels (4 per row, 2 rows)."""
        assert len(PANELS) == 8, (
            f"Expected 8 panels, got {len(PANELS)}. "
            "Each row of the 2×4 figure must have exactly 4 panels."
        )

    def test_each_panel_has_required_keys(self):
        """Every panel dict must supply title, roles, and type_formula fields."""
        required_keys = {"title", "roles", "type_str"}
        for i, panel in enumerate(PANELS):
            missing = required_keys - set(panel.keys())
            assert not missing, (
                f"Panel {i} is missing required keys: {missing}. "
                "Each panel must declare its construction title, case roles, "
                "and the pregroup type formula string (type_str)."
            )

    def test_panel_titles_are_nonempty_strings(self):
        """Every panel title must be a non-empty string."""
        for i, panel in enumerate(PANELS):
            assert isinstance(panel["title"], str) and panel["title"].strip(), (
                f"Panel {i} has a blank or non-string title: {panel.get('title')!r}"
            )

    def test_panel_roles_is_nonempty_list(self):
        """Every panel must declare at least one case role."""
        for i, panel in enumerate(PANELS):
            roles = panel.get("roles", [])
            assert isinstance(roles, list) and len(roles) >= 1, (
                f"Panel {i} has no case roles defined: {roles!r}"
            )


class TestSyntacticDiagramsRendering:
    """Tests for the render_syntactic_panel() function output."""

    def test_renders_to_file(self, tmp_path):
        """render_syntactic_panel() must create a non-empty PNG at the given path."""
        output_path = tmp_path / "syntactic_case_panel.png"
        render_syntactic_panel(str(output_path))

        assert output_path.exists(), (
            f"Expected PNG not found at {output_path}. "
            "render_syntactic_panel() must save the figure to the provided path."
        )
        assert output_path.stat().st_size > 0, (
            f"PNG at {output_path} is empty (0 bytes). "
            "The figure was not written correctly."
        )

    def test_output_is_valid_png(self, tmp_path):
        """The generated file must begin with the PNG magic bytes (\\x89PNG)."""
        output_path = tmp_path / "syntactic_case_panel.png"
        render_syntactic_panel(str(output_path))

        with open(output_path, "rb") as f:
            header = f.read(8)

        png_magic = b"\x89PNG\r\n\x1a\n"
        assert header == png_magic, (
            f"File at {output_path} does not start with PNG magic bytes. "
            f"Got: {header!r}. The renderer may be saving a corrupt or wrong format."
        )

    def test_file_size_reasonable(self, tmp_path):
        """The PNG must be at least 10 KB — a figure this complex cannot be smaller."""
        output_path = tmp_path / "syntactic_case_panel.png"
        render_syntactic_panel(str(output_path))

        size_bytes = output_path.stat().st_size
        min_size = 10_000  # 10 KB
        assert size_bytes >= min_size, (
            f"PNG is only {size_bytes} bytes, less than the minimum {min_size}. "
            "This suggests the figure content may be empty or degenerate."
        )
