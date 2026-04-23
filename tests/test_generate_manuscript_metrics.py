"""Tests for manuscript metrics collection (no mocks; real project layout)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from src.generate_manuscript_metrics import (
    _count_domain_subpackages,
    _count_daif_modules,
    _count_daif_symbols,
    _count_daif_test_files,
    _count_daif_tests,
    _count_test_files,
    _number_to_word,
    _optional_distribution_version,
    _read_coverage_totals,
    collect_metrics,
    write_metrics,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = PROJECT_ROOT / "tests"
DAIF_DIR = PROJECT_ROOT / "src" / "daif"


def test_count_test_files_matches_glob() -> None:
    assert _count_test_files(TESTS_DIR) == len(list(TESTS_DIR.glob("test_*.py")))


def test_daif_counts_nonzero() -> None:
    assert _count_daif_modules(DAIF_DIR) >= 1
    assert _count_daif_symbols(DAIF_DIR) >= 1
    assert _count_daif_test_files(TESTS_DIR) == len(list(TESTS_DIR.glob("test_daif*.py")))
    assert _count_daif_tests(TESTS_DIR) >= 1


def test_number_to_word_small_integers() -> None:
    assert _number_to_word(7) == "seven"
    assert _number_to_word(99) == "ninety-nine"


def test_collect_metrics_expected_keys() -> None:
    m = collect_metrics(PROJECT_ROOT)
    for key in (
        "total_test_count",
        "total_test_files",
        "daif_modules",
        "daif_symbols",
        "daif_tests",
        "daif_test_files",
        "daif_modules_word",
        "total_test_files_word",
        "domain_subpackages",
        "total_figures",
        "coverage_summary",
        "discopy_version",
        "numpy_version",
        "discopy_version_pretty",
        "numpy_version_pretty",
    ):
        assert key in m
    assert int(m["total_test_count"]) >= 100
    assert int(m["total_test_files"]) == _count_test_files(TESTS_DIR)
    assert int(m["domain_subpackages"]) >= 9
    # total_figures should reflect the actual PNG count when output/figures/ exists;
    # if the build hasn't run yet the value may be 0, so use a non-strict lower bound.
    assert int(m["total_figures"]) >= 0
    assert len(m["coverage_summary"]) > 10


def test_write_metrics_roundtrip(tmp_path: Path) -> None:
    m = {"a": "1", "b": "two"}
    out = write_metrics(m, tmp_path / "m.json")
    assert out.exists()
    loaded = json.loads(out.read_text(encoding="utf-8"))
    assert loaded == m


def test_main_dry_run_exit_zero() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "src.generate_manuscript_metrics", "--dry-run"],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0
    assert "total_test_count" in result.stdout


def test_count_daif_symbols_zero_without_all_list(tmp_path: Path) -> None:
    daif = tmp_path / "daif"
    daif.mkdir()
    (daif / "__init__.py").write_text("# no __all__\nx = 1\n", encoding="utf-8")
    assert _count_daif_symbols(daif) == 0


def test_count_daif_symbols_empty_all(tmp_path: Path) -> None:
    daif = tmp_path / "daif"
    daif.mkdir()
    (daif / "__init__.py").write_text('__all__ = []\n', encoding="utf-8")
    assert _count_daif_symbols(daif) == 0


def test_main_writes_metrics_file(tmp_path: Path) -> None:
    out = tmp_path / "metrics.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.generate_manuscript_metrics",
            "--output",
            str(out),
        ],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "total_test_count" in data
    assert "Wrote" in result.stdout


def test_count_collected_tests_fallback(tmp_path: Path) -> None:
    """When pytest is not available, fallback counts def test_ lines."""
    from src.generate_manuscript_metrics import _count_collected_tests

    # Create a fake project with test files but no valid pytest config
    fake_root = tmp_path / "fake_project"
    fake_root.mkdir()
    tests_dir = fake_root / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_example.py").write_text(
        "def test_a():\n    pass\n\ndef test_b():\n    pass\n",
        encoding="utf-8",
    )
    # This will fail pytest --collect-only (no pyproject.toml), triggering fallback
    count = _count_collected_tests(fake_root)
    assert count >= 2


def test_count_daif_symbols_missing_init(tmp_path: Path) -> None:
    """Return 0 when __init__.py does not exist."""
    from src.generate_manuscript_metrics import _count_daif_symbols

    empty = tmp_path / "empty_daif"
    empty.mkdir()
    assert _count_daif_symbols(empty) == 0


def test_number_to_word_boundary_values() -> None:
    """Test edge values: 1, 20, 21, 49, 99, 100, and hundreds."""
    assert _number_to_word(1) == "one"
    assert _number_to_word(20) == "twenty"
    assert _number_to_word(21) == "twenty-one"
    assert _number_to_word(49) == "forty-nine"
    assert _number_to_word(99) == "ninety-nine"
    assert _number_to_word(100) == "one hundred"
    assert _number_to_word(915) == "nine hundred fifteen"
    assert _number_to_word(0) == "zero"


def test_collect_metrics_values_are_strings() -> None:
    """All values returned by collect_metrics should be strings."""
    m = collect_metrics(PROJECT_ROOT)
    for k, v in m.items():
        assert isinstance(v, str), f"Key {k} has non-string value: {type(v)}"


def test_coverage_json_populates_percent_when_present() -> None:
    """When coverage.json exists (from pytest --cov-report=json), percent keys are set."""
    cov = PROJECT_ROOT / "coverage.json"
    if not cov.is_file():
        pytest.skip("coverage.json not present — run pytest with --cov-report=json")
    m = collect_metrics(PROJECT_ROOT)
    assert "coverage_percent" in m
    assert m["coverage_percent"], "coverage_percent should be non-empty when JSON exists"
    assert "%" in m["coverage_summary"] or "coverage" in m["coverage_summary"].lower()


def test_read_coverage_totals_minimal_json(tmp_path: Path) -> None:
    """Parse a minimal coverage.json totals block."""
    payload = {
        "totals": {
            "percent_covered_display": "91.00%",
            "percent_covered": 91.0,
            "covered_lines": 100,
            "num_statements": 110,
            "covered_branches": 40,
            "num_branches": 50,
        }
    }
    (tmp_path / "coverage.json").write_text(json.dumps(payload), encoding="utf-8")
    got = _read_coverage_totals(tmp_path)
    assert got["coverage_percent"] == "91.00"
    assert got["coverage_lines_covered"] == "100"
    assert "91.00%" in got["coverage_summary"]


def test_read_coverage_totals_invalid_json(tmp_path: Path) -> None:
    (tmp_path / "coverage.json").write_text("{not json", encoding="utf-8")
    assert _read_coverage_totals(tmp_path) == {}


def test_read_coverage_totals_empty_totals_object(tmp_path: Path) -> None:
    (tmp_path / "coverage.json").write_text(json.dumps({"totals": {}}), encoding="utf-8")
    assert _read_coverage_totals(tmp_path) == {}


def test_read_coverage_totals_raw_percent_only(tmp_path: Path) -> None:
    """When display string is absent, raw percent still drives coverage_summary."""
    payload = {"totals": {"percent_covered": 88.456}}
    (tmp_path / "coverage.json").write_text(json.dumps(payload), encoding="utf-8")
    got = _read_coverage_totals(tmp_path)
    assert got["coverage_percent_raw"] == "88.46"
    assert "88.46%" in got["coverage_summary"]


def test_optional_distribution_version_missing_package() -> None:
    assert _optional_distribution_version("zzz_nonexistent_pkg_zz") == ""


def test_count_domain_subpackages(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "pkg_a").mkdir()
    (src / "pkg_a" / "__init__.py").write_text("", encoding="utf-8")
    (src / "not_pkg").mkdir()
    (src / "loose.py").write_text("x=1\n", encoding="utf-8")
    assert _count_domain_subpackages(src) == 1


def test_write_metrics_creates_parent_dirs(tmp_path: Path) -> None:
    """write_metrics creates intermediate directories if needed."""
    nested = tmp_path / "a" / "b" / "c" / "metrics.json"
    m = {"x": "1"}
    out = write_metrics(m, nested)
    assert out.exists()
    assert json.loads(out.read_text(encoding="utf-8")) == m
