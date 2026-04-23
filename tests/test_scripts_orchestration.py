"""Tests for orchestration scripts — no mocks, real file I/O.

Covers:
  - generate_manuscript_metrics.py: collect_metrics(), write_metrics()
  - inject_variables.py: variable substitution pipeline
  - generate_diagrams.py: _write_figure_registry(), run_domain() dispatch
"""
import json
import re
import sys
from pathlib import Path
from string import Template

import pytest

# Ensure project root is importable
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


# ---------------------------------------------------------------------------
# generate_manuscript_metrics
# ---------------------------------------------------------------------------

class TestCollectMetrics:
    def test_returns_dict_with_required_keys(self):
        from src.generate_manuscript_metrics import collect_metrics
        metrics = collect_metrics(_PROJECT_ROOT)
        required_keys = [
            "total_test_count",
            "total_test_files",
            "daif_modules",
            "daif_symbols",
            "daif_tests",
            "domain_subpackages",
            "daif_modules_word",
            "discopy_version_pretty",
        ]
        for key in required_keys:
            assert key in metrics, f"Missing key: {key}"

    def test_total_test_files_is_positive_integer(self):
        from src.generate_manuscript_metrics import collect_metrics
        metrics = collect_metrics(_PROJECT_ROOT)
        n = int(metrics["total_test_files"])
        assert n > 0

    def test_domain_subpackages_at_least_five(self):
        from src.generate_manuscript_metrics import collect_metrics
        metrics = collect_metrics(_PROJECT_ROOT)
        n = int(metrics["domain_subpackages"])
        assert n >= 5, f"Expected ≥5 domain subpackages, got {n}"

    def test_daif_modules_word_is_word_string(self):
        from src.generate_manuscript_metrics import collect_metrics
        metrics = collect_metrics(_PROJECT_ROOT)
        word = metrics["daif_modules_word"]
        assert isinstance(word, str)
        assert len(word) > 0

    def test_all_values_are_strings(self):
        from src.generate_manuscript_metrics import collect_metrics
        metrics = collect_metrics(_PROJECT_ROOT)
        for k, v in metrics.items():
            assert isinstance(v, str), f"Non-string value for key '{k}': {v!r}"


class TestWriteMetrics:
    def test_write_creates_valid_json(self, tmp_path):
        from src.generate_manuscript_metrics import collect_metrics, write_metrics
        metrics = collect_metrics(_PROJECT_ROOT)
        dest = write_metrics(metrics, tmp_path / "metrics.json")
        assert dest.exists()
        loaded = json.loads(dest.read_text(encoding="utf-8"))
        assert loaded == metrics

    def test_write_creates_parent_directory(self, tmp_path):
        from src.generate_manuscript_metrics import collect_metrics, write_metrics
        metrics = collect_metrics(_PROJECT_ROOT)
        nested = tmp_path / "nested" / "dir" / "metrics.json"
        dest = write_metrics(metrics, nested)
        assert dest.exists()


class TestNumberToWord:
    def test_zero_to_nineteen(self):
        from src.generate_manuscript_metrics import _number_to_word
        assert _number_to_word(0) == "zero"
        assert _number_to_word(1) == "one"
        assert _number_to_word(19) == "nineteen"

    def test_round_tens(self):
        from src.generate_manuscript_metrics import _number_to_word
        assert _number_to_word(20) == "twenty"
        assert _number_to_word(50) == "fifty"

    def test_compound_tens(self):
        from src.generate_manuscript_metrics import _number_to_word
        assert _number_to_word(21) == "twenty-one"
        assert _number_to_word(99) == "ninety-nine"

    def test_hundreds(self):
        from src.generate_manuscript_metrics import _number_to_word
        assert _number_to_word(100) == "one hundred"
        assert _number_to_word(200) == "two hundred"

    def test_hundreds_with_remainder(self):
        from src.generate_manuscript_metrics import _number_to_word
        assert _number_to_word(101) == "one hundred one"
        assert _number_to_word(999) == "nine hundred ninety-nine"

    def test_large_number_returns_decimal_string(self):
        from src.generate_manuscript_metrics import _number_to_word
        result = _number_to_word(1000)
        assert result == "1000"

    def test_negative_number_returns_string(self):
        from src.generate_manuscript_metrics import _number_to_word
        result = _number_to_word(-5)
        assert result == "-5"


# ---------------------------------------------------------------------------
# inject_variables — variable substitution logic (no infrastructure logging)
# ---------------------------------------------------------------------------

_UNRESOLVED_VAR_RE = re.compile(r"\$\{([_a-zA-Z][_a-zA-Z0-9]*)\}")


def _do_substitution(text: str, metrics: dict) -> str:
    return Template(text).safe_substitute(metrics)


class TestVariableSubstitution:
    def test_substitution_replaces_known_key(self):
        text = "We ran ${total_test_count} tests."
        result = _do_substitution(text, {"total_test_count": "900"})
        assert "900" in result
        assert "${total_test_count}" not in result

    def test_substitution_leaves_unknown_key_intact(self):
        text = "Value is ${unknown_key}."
        result = _do_substitution(text, {"other_key": "42"})
        assert "${unknown_key}" in result

    def test_all_metrics_resolvable(self, tmp_path):
        """Manuscript placeholders actually used match keys in collect_metrics."""
        from src.generate_manuscript_metrics import collect_metrics
        metrics = collect_metrics(_PROJECT_ROOT)
        manuscript_dir = _PROJECT_ROOT / "manuscript"
        unresolved: set[str] = set()
        for md in sorted(manuscript_dir.glob("[0-9]*.md")):
            text = md.read_text(encoding="utf-8")
            rendered = _do_substitution(text, metrics)
            still_unresolved = _UNRESOLVED_VAR_RE.findall(rendered)
            unresolved.update(still_unresolved)
        # Report but don't hard-fail — some vars may be intentionally unresolved
        # (e.g., coverage_percent when no coverage.json exists)
        expected_unresolvable = {"coverage_percent", "coverage_summary"}
        truly_unexpected = unresolved - expected_unresolvable
        assert truly_unexpected == set(), (
            f"Unexpected unresolved variables in manuscript: {truly_unexpected}"
        )

    def test_write_and_read_metrics_roundtrip(self, tmp_path):
        from src.generate_manuscript_metrics import collect_metrics, write_metrics
        metrics = collect_metrics(_PROJECT_ROOT)
        out = write_metrics(metrics, tmp_path / "metrics.json")
        reloaded = json.loads(out.read_text(encoding="utf-8"))
        assert reloaded["domain_subpackages"] == metrics["domain_subpackages"]


# ---------------------------------------------------------------------------
# generate_diagrams.py — figure registry and domain dispatch
# ---------------------------------------------------------------------------

class TestFigureRegistry:
    def test_write_registry_creates_json(self, tmp_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "generate_diagrams",
            _PROJECT_ROOT / "scripts" / "generate_diagrams.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        # Create fake figure files
        fake_png = tmp_path / "fig1.png"
        fake_svg = tmp_path / "fig2.svg"
        fake_txt = tmp_path / "notes.txt"
        fake_png.write_text("fake")
        fake_svg.write_text("fake")
        fake_txt.write_text("ignored")

        mod._write_figure_registry([fake_png, fake_svg, fake_txt], tmp_path)
        registry_path = tmp_path / "figure_registry.json"
        assert registry_path.exists()
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        assert len(registry) == 2  # txt excluded
        names = [r["filename"] for r in registry]
        assert "fig1.png" in names
        assert "fig2.svg" in names
        assert all("label" in r for r in registry)
        assert all("generated_by" in r for r in registry)

    def test_registry_label_format(self, tmp_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "generate_diagrams",
            _PROJECT_ROOT / "scripts" / "generate_diagrams.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        p = tmp_path / "my_figure_name.png"
        p.write_text("fake")
        mod._write_figure_registry([p], tmp_path)
        registry = json.loads((tmp_path / "figure_registry.json").read_text())
        assert registry[0]["label"] == "fig:my-figure-name"


class TestGenerateDiagramsModule:
    def test_domains_dict_has_expected_keys(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "generate_diagrams",
            _PROJECT_ROOT / "scripts" / "generate_diagrams.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for key in ["category", "discopy", "cognitive", "quantum", "syntactic"]:
            assert key in mod.DOMAINS

    def test_domain_aliases_resolve_correctly(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "generate_diagrams",
            _PROJECT_ROOT / "scripts" / "generate_diagrams.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        assert mod._DOMAIN_ALIASES.get("daif") == "cognitive"
        assert mod._DOMAIN_ALIASES.get("enriched") == "strings"

    def test_unknown_domain_raises_valueerror(self, tmp_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "generate_diagrams",
            _PROJECT_ROOT / "scripts" / "generate_diagrams.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with pytest.raises(ValueError, match="Unknown domain"):
            mod.run_domain("nonexistent_domain", tmp_path)
