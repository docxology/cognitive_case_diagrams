"""Tests for manuscript metrics collection (no mocks; real project layout)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from src.generate_manuscript_metrics import (
    _count_daif_modules,
    _count_daif_symbols,
    _count_daif_test_files,
    _count_daif_tests,
    _count_test_files,
    _number_to_word,
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
    assert _number_to_word(99) == "99"


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
    ):
        assert key in m
    assert int(m["total_test_count"]) >= 100
    assert int(m["total_test_files"]) == _count_test_files(TESTS_DIR)


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
