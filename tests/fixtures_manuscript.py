"""Real-file fixtures shared by manuscript gate tests.

Builds a complete, internally consistent tmp project: a real seeded
experiments run, a real quality receipt over the copied tree, a rendered
chapter set, and a written variables manifest. No mocks; every file is
byte-for-byte what the production writers produce.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.release_validation import (  # noqa: E402
    QUALITY_JUNIT,
    quality_input_fingerprint,
    write_quality_receipt,
)

_CHAPTER = (
    "# Test {#sec:test}\n"
    "\n"
    "The suite collects ${total_test_count} tests. [@ref; @sec:test].\n"
    "\n"
    "![A real fixture](output/figures/a.png){#fig:a}\n"
)

_CONFIG_YAML = (
    "paper:\n"
    '  title: "Fixture"\n'
    '  version: "2.4.0"\n'
    '  date: "2026-09-07"\n'
    "publication:\n"
    '  doi: "10.5281/zenodo.19695259"\n'
    '  version_doi: "10.5281/zenodo.22653315"\n'
    '  version_record: "https://zenodo.org/records/22653315"\n'
    '  prior_version_doi: "10.5281/zenodo.19695260"\n'
    '  status: "release manuscript"\n'
    '  year: "2026"\n'
)

_BIB = "@book{ref, title={A}, year={2026}}\n"


def _write_receipt_tree(root: Path) -> None:
    """Minimal fingerprinted tree plus coverage and JUnit evidence."""
    for name in ("src", "scripts"):
        # src/ may already hold runner source copies; never clobber them.
        (root / name).mkdir(exist_ok=True)
        (root / name / "example.py").write_text("value = 1\n")
    tests = root / "tests"
    tests.mkdir(exist_ok=True)
    (tests / "test_alpha.py").write_text(
        "def test_alpha() -> None:\n    assert True\n"
    )
    (tests / "test_beta.py").write_text(
        "def test_beta() -> None:\n    assert 1 + 1 == 2\n"
    )
    (root / "pyproject.toml").write_text("[tool.coverage.report]\nfail_under = 90\n")
    (root / "uv.lock").write_text("version = 1\n")
    (root / QUALITY_JUNIT).parent.mkdir(parents=True, exist_ok=True)
    (root / QUALITY_JUNIT).write_text(
        '<testsuites><testsuite><testcase name="analytic"/>'
        '<testcase name="contract"/></testsuite></testsuites>'
    )
    coverage = {
        "meta": {"branch_coverage": True},
        "totals": {
            "covered_lines": 95,
            "num_statements": 100,
            "covered_branches": 19,
            "num_branches": 20,
            "percent_covered": 95.0,
        },
    }
    (root / "coverage.json").write_text(json.dumps(coverage))


def _create_receipt(root: Path) -> dict:
    checks = [
        {"name": name, "exit_code": 0, "command": ["uv", "run", name]}
        for name in ("ruff", "mypy", "coverage")
    ]
    return write_quality_receipt(root, checks, quality_input_fingerprint(root))


def _write_experiment_results(root: Path) -> dict:
    """Run the real seeded runner small and copy its source files across."""
    from src.experiments.config import ExperimentConfig
    from src.experiments.runner import run_experiments

    results = run_experiments(ExperimentConfig(n_replicates=2))
    destination = root / "output" / "experiments" / "results.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(results, indent=2, sort_keys=True))
    for relative in results["provenance"]["source_files"]:
        source = PROJECT_ROOT / relative
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    return results


def build_canonical_gate_tree(target: Path) -> Path:
    """Assemble a fully valid project tree that passes validate_project."""
    source = target / "docs" / "manuscript"
    source.mkdir(parents=True)
    (source / "01_a.md").write_text(_CHAPTER)
    (source / "references.bib").write_text(_BIB)
    (source / "config.yaml").write_text(_CONFIG_YAML)
    (source / "preamble.md").write_text("")
    (target / "docs" / "figure_alt_text.json").write_text(
        json.dumps({"a.png": "White square fixture."})
    )

    _write_experiment_results(target)
    _write_receipt_tree(target)
    _create_receipt(target)

    figures = target / "output" / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    from PIL import Image

    image = figures / "a.png"
    Image.new("RGB", (8, 8), color="white").save(image)
    registry = [
        {
            "filename": "a.png",
            "label": "fig:a",
            "path": "output/figures/a.png",
            "alt_text": "White square fixture.",
            "sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
            "generator_input_fingerprint": quality_input_fingerprint(target)["sha256"],
        }
    ]
    (figures / "figure_registry.json").write_text(json.dumps(registry, indent=2))

    from src.generate_manuscript_metrics import collect_metrics, write_metrics
    from src.manuscript_injection import render_all_chapters
    from src.manuscript_variables import write_variables_manifest

    metrics = collect_metrics(target)
    write_metrics(metrics, target / "output" / "metrics.json")
    render_all_chapters(source, metrics, target / "output" / "manuscript")
    write_variables_manifest(target, metrics)
    return target


@pytest.fixture(scope="session")
def canonical_gate_tree(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """One canonical valid tree per session; tests mutate copies."""
    return build_canonical_gate_tree(tmp_path_factory.mktemp("gate-canonical"))


@pytest.fixture
def gate_tree(canonical_gate_tree: Path, tmp_path: Path) -> Path:
    """A fresh writable copy of the canonical tree for each test."""
    copy = tmp_path / "project"
    shutil.copytree(canonical_gate_tree, copy)
    return copy
