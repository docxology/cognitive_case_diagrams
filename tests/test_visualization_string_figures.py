"""Tests for the strings/enriched figure domain — src renderer + sub-script.

Covers ``src.visualization.enriched_diagrams.write_magnitude_report`` and the
dedicated sub-script ``scripts/generate_string_figures.run`` (moved out of
``generate_diagrams.py`` per the per-domain sub-script architecture).
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.enriched_cat.enriched import standard_enriched_category  # noqa: E402
from src.visualization.enriched_diagrams import write_magnitude_report  # noqa: E402


class TestWriteMagnitudeReport:
    def test_writes_report_with_computed_magnitude(self, tmp_path):
        cat = standard_enriched_category()
        dest = tmp_path / "enriched_magnitude.txt"
        result = write_magnitude_report(cat, dest)
        assert result == dest
        text = dest.read_text(encoding="utf-8")
        assert f"Enriched Category: {cat.name}" in text
        assert f"Number of objects: {len(cat.roles)}" in text
        assert f"Categorical magnitude: {cat.magnitude():.6f}" in text
        assert f"Weighting vector: {cat.weighting().tolist()}" in text

    def test_accepts_string_path(self, tmp_path):
        cat = standard_enriched_category()
        dest = tmp_path / "magnitude.txt"
        result = write_magnitude_report(cat, str(dest))
        assert Path(result) == dest
        assert dest.exists() and dest.stat().st_size > 0


class TestGenerateStringFiguresScript:
    def test_run_writes_three_figures_and_magnitude_report(self, tmp_path):
        from scripts.generate_string_figures import LAST_FAILURES, run
        produced = run(tmp_path)
        names = {p.name for p in produced}
        assert names == {
            "string_diagram_discocat.png",
            "discourse_string_diagram.png",
            "enriched_hom_matrix.png",
            "enriched_magnitude.txt",
        }
        for p in produced:
            assert p.exists() and p.stat().st_size > 0
        assert LAST_FAILURES == []
