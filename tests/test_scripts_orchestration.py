"""Tests for orchestration scripts — no mocks, real file I/O.

Covers:
  - generate_manuscript_metrics.py: collect_metrics(), write_metrics()
  - inject_variables.py: strict variable substitution
  - generate_diagrams.py: _write_figure_registry(), run_domain() dispatch

Metrics classes run against the real tmp gate tree from
``tests/fixtures_manuscript.py`` so the gate itself never depends on a
live-root receipt (which would be circular evidence).
"""

import json
import re
import sys
from pathlib import Path

import pytest

# Ensure project root is importable
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

pytest_plugins = ("fixtures_manuscript",)

_UNRESOLVED_VAR_RE = re.compile(r"\$\{([_a-zA-Z][_a-zA-Z0-9]*)\}")


# ---------------------------------------------------------------------------
# generate_manuscript_metrics
# ---------------------------------------------------------------------------


class TestCollectMetrics:
    def test_returns_registry_complete_mapping(self, gate_tree):
        from src.generate_manuscript_metrics import collect_metrics
        from src.manuscript_variables import variable_specs

        metrics = collect_metrics(gate_tree)
        # Every registry-required spec is present and nothing unregistered.
        assert set(metrics) <= set(variable_specs())
        for name, spec in variable_specs().items():
            if spec.required:
                assert name in metrics, f"Missing required key: {name}"

    def test_collection_count_matches_fixture_tests(self, gate_tree):
        from src.generate_manuscript_metrics import collect_metrics

        metrics = collect_metrics(gate_tree)
        assert metrics["total_test_count"] == "2"
        assert metrics["total_test_files"] == "2"

    def test_receipt_backed_fields_bind_evidence(self, gate_tree):
        from src.generate_manuscript_metrics import collect_metrics

        metrics = collect_metrics(gate_tree)
        assert metrics["total_tests_passed"] == "2"
        assert metrics["total_tests_failed"] == "0"
        assert metrics["coverage_percent"] == "95.00"
        assert metrics["coverage_lines_total"] == "100"
        assert 0 < len(metrics["quality_fingerprint_short"]) <= 12

    def test_experiment_fields_come_from_runner_output(self, gate_tree):
        from src.generate_manuscript_metrics import collect_metrics
        from src.experiments.runner import experiment_variable_definitions

        metrics = collect_metrics(gate_tree)
        for name in experiment_variable_definitions():
            assert name in metrics, f"Missing experiment variable: {name}"
        assert metrics["experiment_seed"].isdigit()

    def test_all_values_are_strings(self, gate_tree):
        from src.generate_manuscript_metrics import collect_metrics

        for key, value in collect_metrics(gate_tree).items():
            assert isinstance(value, str), f"Non-string value for key '{key}'"


class TestWriteMetrics:
    def test_write_creates_valid_json(self, tmp_path):
        from src.generate_manuscript_metrics import write_metrics

        metrics = {"a": "1", "b": "two"}
        dest = write_metrics(metrics, tmp_path / "metrics.json")
        assert dest.exists()
        loaded = json.loads(dest.read_text(encoding="utf-8"))
        assert loaded == metrics

    def test_write_creates_parent_directory(self, tmp_path):
        from src.generate_manuscript_metrics import write_metrics

        nested = tmp_path / "nested" / "dir" / "metrics.json"
        dest = write_metrics({"a": "1"}, nested)
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
# inject_variables — strict variable substitution
# ---------------------------------------------------------------------------


class TestVariableSubstitution:
    def test_substitution_replaces_known_key(self):
        from src.manuscript_injection import substitute_variables

        text = "We ran ${total_test_count} tests."
        result = substitute_variables(text, {"total_test_count": "900"})
        assert "900" in result
        assert "${total_test_count}" not in result

    def test_substitution_rejects_unknown_key(self):
        from src.manuscript_injection import substitute_variables

        with pytest.raises(ValueError, match="unknown_key"):
            substitute_variables("Value is ${unknown_key}.", {"other_key": "42"})

    def test_all_manuscript_tokens_resolve_from_registry_metrics(self, gate_tree):
        """Every placeholder in the canonical chapters resolves strictly."""
        from src.generate_manuscript_metrics import collect_metrics
        from src.manuscript_injection import substitute_variables

        metrics = collect_metrics(gate_tree)
        manuscript_dir = gate_tree / "docs" / "manuscript"
        chapters = sorted(manuscript_dir.glob("[0-9]*.md"))
        assert len(chapters) >= 1
        for md in chapters:
            substitute_variables(md.read_text(encoding="utf-8"), metrics)

    def test_live_chapter_tokens_are_registry_declared(self):
        """The authored sources never reference an undeclared identifier."""
        from src.manuscript_variables import TOKEN_RE, variable_specs

        manuscript_dir = _PROJECT_ROOT / "docs" / "manuscript"
        chapters = sorted(manuscript_dir.glob("[0-9]*.md"))
        assert len(chapters) >= 20, (
            f"expected the numbered manuscript sections, found {len(chapters)} "
            f"in {manuscript_dir}"
        )
        specs = variable_specs()
        unresolved: set[str] = set()
        for md in chapters:
            unresolved.update(TOKEN_RE.findall(md.read_text(encoding="utf-8")))
        unknown = unresolved - set(specs)
        assert unknown == set(), (
            f"Chapters reference unregistered variables: {sorted(unknown)}"
        )

    def test_write_and_read_metrics_roundtrip(self, tmp_path):
        from src.generate_manuscript_metrics import write_metrics

        out = write_metrics({"domain_subpackages": "9"}, tmp_path / "metrics.json")
        reloaded = json.loads(out.read_text(encoding="utf-8"))
        assert reloaded["domain_subpackages"] == "9"


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
        # Every domain must delegate to a sub-script module (no inline handlers)
        assert all(mod.DOMAINS.values())

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

    def test_run_domain_strings_delegates_to_subscript(self, tmp_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "generate_diagrams",
            _PROJECT_ROOT / "scripts" / "generate_diagrams.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        paths, failures = mod.run_domain("strings", tmp_path)
        names = {p.name for p in paths}
        assert {
            "string_diagram_discocat.png",
            "discourse_string_diagram.png",
            "enriched_hom_matrix.png",
            "enriched_magnitude.txt",
        } <= names
        assert failures == []
