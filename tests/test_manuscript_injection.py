"""Tests for src/manuscript_injection.py — no mocks, real file I/O.

Covers the standalone manuscript ``${variable}`` substitution used by
``scripts/inject_variables.py``: chapter rendering, ancillary copying,
manuscript-directory resolution, and unresolved-token counting.
"""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.manuscript_injection import (  # noqa: E402
    count_unresolved_variables,
    render_all_chapters,
    resolve_manuscript_dir,
)


class TestRenderAllChapters:
    def test_substitutes_numbered_chapters_and_copies_ancillaries(self, tmp_path):
        manuscript = tmp_path / "docs" / "manuscript"
        manuscript.mkdir(parents=True)
        (manuscript / "01_intro.md").write_text(
            "We ran ${total_test_count} tests with ${total_figures} figures.\n",
            encoding="utf-8",
        )
        (manuscript / "02_methods.md").write_text(
            "Magnitude: ${categorical_magnitude}\n", encoding="utf-8"
        )
        (manuscript / "preamble.md").write_text("\\documentclass{article}\n", encoding="utf-8")
        (manuscript / "references.bib").write_text("@book{adams2026}\n", encoding="utf-8")

        metrics = {"total_test_count": "900", "total_figures": "30"}
        out = tmp_path / "rendered"
        written = render_all_chapters(manuscript, metrics, out)

        names = {p.name for p in written}
        assert names == {"01_intro.md", "02_methods.md", "preamble.md", "references.bib"}

        intro = (out / "01_intro.md").read_text(encoding="utf-8")
        assert "We ran 900 tests with 30 figures." in intro
        assert "${" not in intro

        methods = (out / "02_methods.md").read_text(encoding="utf-8")
        # safe_substitute leaves unknown tokens intact
        assert "Magnitude: ${categorical_magnitude}" in methods

        # Ancillaries copied verbatim
        assert (out / "preamble.md").read_text(encoding="utf-8") == "\\documentclass{article}\n"
        assert (out / "references.bib").read_text(encoding="utf-8") == "@book{adams2026}\n"

    def test_skips_directories(self, tmp_path):
        manuscript = tmp_path / "manuscript"
        manuscript.mkdir()
        (manuscript / "01_a.md").write_text("x ${k}\n", encoding="utf-8")
        (manuscript / "figures").mkdir()
        (manuscript / "figures" / "f.png").write_bytes(b"png")

        out = tmp_path / "rendered"
        written = render_all_chapters(manuscript, {"k": "v"}, out)

        assert [p.name for p in written] == ["01_a.md"]
        assert (out / "01_a.md").read_text(encoding="utf-8") == "x v\n"
        assert not (out / "figures").exists()

    def test_creates_output_directory(self, tmp_path):
        manuscript = tmp_path / "manuscript"
        manuscript.mkdir()
        (manuscript / "01_a.md").write_text("plain\n", encoding="utf-8")
        out = tmp_path / "nested" / "rendered"

        render_all_chapters(manuscript, {}, out)

        assert out.is_dir()
        assert (out / "01_a.md").exists()


class TestResolveManuscriptDir:
    def test_canonical_docs_manuscript(self, tmp_path):
        canonical = tmp_path / "docs" / "manuscript"
        canonical.mkdir(parents=True)
        (canonical / "01_intro.md").write_text("x", encoding="utf-8")
        assert resolve_manuscript_dir(tmp_path) == canonical

    def test_legacy_fallback(self, tmp_path):
        legacy = tmp_path / "manuscript"
        legacy.mkdir()
        (legacy / "01_intro.md").write_text("x", encoding="utf-8")
        assert resolve_manuscript_dir(tmp_path) == legacy

    def test_defaults_to_canonical_when_neither_has_chapters(self, tmp_path):
        (tmp_path / "docs" / "manuscript").mkdir(parents=True)
        canonical = tmp_path / "docs" / "manuscript"
        assert resolve_manuscript_dir(tmp_path) == canonical


class TestCountUnresolvedVariables:
    def test_counts_unresolved_tokens_across_chapters(self, tmp_path):
        rendered = tmp_path / "rendered"
        rendered.mkdir()
        (rendered / "01_a.md").write_text(
            "keep ${known} drop ${missing_one} and ${missing_one} again\n",
            encoding="utf-8",
        )
        (rendered / "02_b.md").write_text("also ${missing_two}\n", encoding="utf-8")
        # Ancillary (not numbered) files are not scanned
        (rendered / "preamble.md").write_text("${missing_three}\n", encoding="utf-8")

        total = count_unresolved_variables(rendered)
        # 01_a contributes 3 occurrences (missing_one twice, known once), 02_b one
        assert total == 4

    def test_returns_zero_when_all_resolved(self, tmp_path):
        rendered = tmp_path / "rendered"
        rendered.mkdir()
        (rendered / "01_a.md").write_text("all variables resolved\n", encoding="utf-8")
        assert count_unresolved_variables(rendered) == 0

    def test_ignores_non_identifier_braces(self, tmp_path):
        rendered = tmp_path / "rendered"
        rendered.mkdir()
        # LaTeX-like spans without identifier names must not count
        (rendered / "01_a.md").write_text("math ${1+x} and ${} stay\n", encoding="utf-8")
        assert count_unresolved_variables(rendered) == 0
