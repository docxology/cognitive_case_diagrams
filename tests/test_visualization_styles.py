"""Tests for visualization modules: complexity plots and discopy diagrams.

Tests actual figure generation to verify rendering works without errors.
Figures are generated to tmp paths and validated for file existence.
"""

import os
import tempfile


from src.visualization.complexity_plots import (
    render_complexity_comparison,
    render_normal_form_comparison,
    render_syntactic_complexity_radar,
)


class TestComplexityComparison:
    """Tests for complexity comparison bar chart."""

    def test_renders_to_file(self) -> None:
        """Complexity comparison renders to PNG successfully."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            path = f.name
        try:
            result = render_complexity_comparison(
                labels=["Intransitive", "Transitive", "Ditransitive"],
                box_counts=[3, 5, 7],
                word_counts=[2, 3, 4],
                cup_counts=[1, 2, 3],
                sentences=["A runs", "A chases B", "A gives B C"],
                output_path=path,
            )
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_returns_output_path(self) -> None:
        """Render returns the output path."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            path = f.name
        try:
            result = render_complexity_comparison(
                labels=["A"],
                box_counts=[1],
                word_counts=[1],
                cup_counts=[0],
                sentences=["test"],
                output_path=path,
            )
            assert result == path
        finally:
            if os.path.exists(path):
                os.unlink(path)


class TestNormalFormComparison:
    """Tests for normal form comparison chart."""

    def test_renders_to_file(self) -> None:
        """Normal form comparison renders successfully."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            path = f.name
        try:
            result = render_normal_form_comparison(
                labels=["Transitive", "Passive"],
                original_counts=[5, 5],
                normal_form_counts=[5, 5],
                output_path=path,
            )
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0
        finally:
            if os.path.exists(path):
                os.unlink(path)


class TestRadarChart:
    """Tests for complexity radar chart."""

    def test_renders_to_file(self) -> None:
        """Radar chart renders successfully."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            path = f.name
        try:
            result = render_syntactic_complexity_radar(
                labels=["Intransitive", "Transitive", "Ditransitive", "Passive"],
                metrics={
                    "Box Count": [3, 5, 7, 5],
                    "Word Count": [2, 3, 4, 3],
                    "Cup Count": [1, 2, 3, 2],
                },
                output_path=path,
            )
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0
        finally:
            if os.path.exists(path):
                os.unlink(path)


class TestMathtextSafeArrows:
    """Unit tests for styles.mathtext_safe_arrows (Helvetica glyph gaps)."""

    def test_replaces_arrows_and_marks(self) -> None:
        from src.visualization.styles import mathtext_safe_arrows

        s = mathtext_safe_arrows("a→b⇒c✓d✗e∘f")
        assert "rightarrow" in s and "Rightarrow" in s
        assert "checkmark" in s and "times" in s and "circ" in s
        assert "→" not in s and "✓" not in s and "∘" not in s

