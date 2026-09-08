"""Strict injection tests: whole-file substitution with fail-closed rejects."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

pytest_plugins = ("fixtures_manuscript",)

from src.manuscript_injection import (  # noqa: E402
    count_unresolved_variables,
    render_all_chapters,
    resolve_manuscript_dir,
    substitute_variables,
)


class TestRenderAllChapters:
    def test_substitutes_numbered_chapters_and_copies_ancillaries(self, tmp_path):
        manuscript = tmp_path / "docs" / "manuscript"
        manuscript.mkdir(parents=True)
        (manuscript / "01_a.md").write_text(
            "value ${count} and $x+y$ inline", encoding="utf-8"
        )
        (manuscript / "references.bib").write_text("@book{adams2026}\n")
        out = tmp_path / "out"
        written = render_all_chapters(manuscript, {"count": "3"}, out)
        assert (out / "01_a.md").read_text(encoding="utf-8") == (
            "value 3 and $x+y$ inline"
        )
        assert (out / "references.bib").read_text(encoding="utf-8") == (
            "@book{adams2026}\n"
        )
        assert sorted(p.name for p in written) == ["01_a.md", "references.bib"]

    def test_skips_directories(self, tmp_path):
        manuscript = tmp_path / "manuscript"
        (manuscript / "figures").mkdir(parents=True)
        (manuscript / "figures" / "nested.md").write_text("ignored")
        (manuscript / "01_a.md").write_text("${count}", encoding="utf-8")
        out = tmp_path / "out"
        render_all_chapters(manuscript, {"count": "1"}, out)
        assert not (out / "figures").exists()

    def test_creates_output_directory(self, tmp_path):
        manuscript = tmp_path / "manuscript"
        manuscript.mkdir(parents=True)
        (manuscript / "01_a.md").write_text("${count}", encoding="utf-8")
        out = tmp_path / "out" / "deep"
        written = render_all_chapters(manuscript, {"count": "1"}, out)
        assert (out / "01_a.md").exists()
        assert len(written) == 1

    def test_no_chapters_is_rejected(self, tmp_path):
        empty = tmp_path / "manuscript"
        empty.mkdir(parents=True)
        with pytest.raises(ValueError, match="No numbered manuscript chapters"):
            render_all_chapters(empty, {"count": "1"}, tmp_path / "out")

    def test_unknown_token_aborts_before_any_write(self, tmp_path):
        manuscript = tmp_path / "manuscript"
        manuscript.mkdir(parents=True)
        (manuscript / "01_a.md").write_text("${known}", encoding="utf-8")
        (manuscript / "02_b.md").write_text("${unknown}", encoding="utf-8")
        out = tmp_path / "out"
        with pytest.raises(ValueError, match="unknown"):
            render_all_chapters(manuscript, {"known": "1"}, out)
        assert not out.exists()


class TestResolveManuscriptDir:
    def test_canonical_docs_manuscript(self, tmp_path):
        canonical = tmp_path / "docs" / "manuscript"
        canonical.mkdir(parents=True)
        (canonical / "01_a.md").write_text("x")
        assert resolve_manuscript_dir(tmp_path) == canonical

    def test_legacy_fallback(self, tmp_path):
        legacy = tmp_path / "manuscript"
        legacy.mkdir(parents=True)
        (legacy / "01_a.md").write_text("x")
        assert resolve_manuscript_dir(tmp_path) == legacy

    def test_defaults_to_canonical_when_neither_has_chapters(self, tmp_path):
        (tmp_path / "docs" / "manuscript").mkdir(parents=True)
        canonical = tmp_path / "docs" / "manuscript"
        assert resolve_manuscript_dir(tmp_path) == canonical


class TestCountUnresolvedVariables:
    def test_counts_unresolved_tokens_across_chapters(self, tmp_path):
        rendered = tmp_path / "rendered"
        rendered.mkdir()
        (rendered / "01_a.md").write_text("${b} then ${a} then ${b}")
        (rendered / "02_b.md").write_text("no tokens here")
        assert count_unresolved_variables(rendered) == 3

    def test_returns_zero_when_fully_resolved(self, tmp_path):
        rendered = tmp_path / "rendered"
        rendered.mkdir()
        (rendered / "01_a.md").write_text("all resolved")
        assert count_unresolved_variables(rendered) == 0


def test_substitute_variables_replaces_exactly() -> None:
    text = "We ran ${total_test_count} tests; math $x+y$ survives."
    assert substitute_variables(text, {"total_test_count": "900"}) == (
        "We ran 900 tests; math $x+y$ survives."
    )


def test_substitute_variables_rejects_missing_sorted() -> None:
    with pytest.raises(ValueError) as excinfo:
        substitute_variables("${b} ${a}", {})
    assert "['a', 'b']" in str(excinfo.value)


def test_substitute_variables_rejects_nested_token() -> None:
    with pytest.raises(ValueError, match="nested|unresolved"):
        substitute_variables("${outer}", {"outer": "${inner}"})


def test_substitute_variables_rejects_dollar_adjacent_lookup() -> None:
    # A literal $ followed by a braced word must not be treated as a token.
    assert substitute_variables("cost $ {not_a_token}", {}) == (
        "cost $ {not_a_token}"
    )


def test_render_uses_strict_substitution(gate_tree):
    metrics = {}
    import json

    metrics = json.loads((gate_tree / "output" / "metrics.json").read_text())
    out = gate_tree / "output" / "manuscript"
    before = (out / "01_a.md").read_text(encoding="utf-8")
    written = render_all_chapters(
        resolve_manuscript_dir(gate_tree), metrics, out
    )
    assert (out / "01_a.md").read_text(encoding="utf-8") == before
    assert any(p.name == "01_a.md" for p in written)
