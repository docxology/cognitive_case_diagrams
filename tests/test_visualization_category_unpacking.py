"""Tests for src/visualization/category_unpacking.py.

All tests render real matplotlib figures to temp files and verify the
output is non-empty and the return path matches the requested location.
Zero mocks.
"""
from __future__ import annotations

import pathlib


from src.visualization.category_unpacking import (
    render_pregroup_reduction_unpacking,
    render_discocirc_entity_persistence,
    render_snake_equation_unpacking,
)


class TestPregroupReductionUnpacking:
    def test_default_sentence_renders(self, tmp_path):
        out = tmp_path / "pregroup.png"
        result = render_pregroup_reduction_unpacking(output_path=str(out))
        assert result == str(out)
        assert out.exists() and out.stat().st_size > 0

    def test_custom_sentence_renders(self, tmp_path):
        out = tmp_path / "custom.png"
        result = render_pregroup_reduction_unpacking(
            output_path=str(out),
            subject="Cat", verb="sees", obj="dog",
        )
        assert result == str(out)
        assert out.exists() and out.stat().st_size > 0

    def test_default_path_when_none(self, tmp_path, monkeypatch):
        # Switch CWD so the default filename lands in tmp_path.
        monkeypatch.chdir(tmp_path)
        result = render_pregroup_reduction_unpacking(output_path=None)
        assert pathlib.Path(result).exists()


class TestDisCoCircEntityPersistence:
    def test_default_renders(self, tmp_path):
        out = tmp_path / "discocirc.png"
        result = render_discocirc_entity_persistence(output_path=str(out))
        assert result == str(out)
        assert out.exists() and out.stat().st_size > 0

    def test_default_path_when_none(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        result = render_discocirc_entity_persistence(output_path=None)
        assert pathlib.Path(result).exists()


class TestSnakeEquationUnpacking:
    def test_default_renders(self, tmp_path):
        out = tmp_path / "snake.png"
        result = render_snake_equation_unpacking(output_path=str(out))
        assert result == str(out)
        assert out.exists() and out.stat().st_size > 0

    def test_default_path_when_none(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        result = render_snake_equation_unpacking(output_path=None)
        assert pathlib.Path(result).exists()


class TestPublicAPI:
    def test_all_three_exported_from_package_init(self):
        from src import visualization
        assert hasattr(visualization, "render_pregroup_reduction_unpacking")
        assert hasattr(visualization, "render_discocirc_entity_persistence")
        assert hasattr(visualization, "render_snake_equation_unpacking")

    def test_generator_script_entry_point(self, tmp_path):
        """scripts/generate_category_unpacking_figures.run writes three PNGs."""
        from scripts.generate_category_unpacking_figures import run
        produced = run(tmp_path)
        assert len(produced) == 3
        for p in produced:
            assert p.exists() and p.stat().st_size > 0
