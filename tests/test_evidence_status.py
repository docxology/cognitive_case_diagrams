"""Evidence-status CLI: real subprocess probes over temporary evidence trees.

Every stage state (missing, stale, invalid, validated) is produced by
creating, mutating, or forging real files in temporary project trees; no
mocking, and every run goes through a real interpreter subprocess.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import yaml

pytest_plugins = ("fixtures_manuscript",)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

STAGES = ("quality", "experiments", "manuscript", "metadata", "visual_review", "release")


def run_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "src.evidence_status", *arguments],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )


def status_of(tree: Path) -> tuple[int, dict]:
    completed = run_cli("--project-root", str(tree))
    report = json.loads(completed.stdout)
    assert str(tree) not in completed.stdout, "absolute project path leaked into the report"
    assert completed.returncode == report["exit_code"]
    return completed.returncode, report


def _snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _gate_checks() -> list[dict]:
    return [
        {"name": name, "exit_code": 0, "command": ["uv", "run", name]}
        for name in ("ruff", "mypy", "coverage")
    ]


def _integrated_tree(gate_tree: Path) -> Path:
    """Extend the canonical gate tree to a fully released end state."""
    from src.manuscript_injection import render_all_chapters
    from src.manuscript_variables import write_variables_manifest
    from src.publication_review import BROWSER_CHECKS, record_publication_review
    from src.release_bundle import build_release_archive
    from src.release_metadata import validate_release_metadata, write_release_metadata
    from src.release_validation import (
        quality_input_fingerprint,
        write_json_atomic,
        write_quality_receipt,
    )

    (gate_tree / "pyproject.toml").write_text(
        '[project]\nname = "cognitive_case_diagrams"\nversion = "2.4.0"\n'
        'license = "Apache-2.0"\n'
        '[project.urls]\nRepository = "https://github.com/docxology/cognitive_case_diagrams"\n'
        "\n[tool.coverage.report]\nfail_under = 90\n"
    )
    config = {
        "paper": {"title": "Fixture", "version": "2.4.0", "date": "2026-09-07"},
        "publication": {
            "doi": "10.5281/zenodo.19695259",
            "version_doi": "10.5281/zenodo.22653315",
            "version_record": "https://zenodo.org/records/22653315",
            "prior_version_doi": "10.5281/zenodo.19695260",
            "status": "release manuscript",
            "year": "2026",
        },
        "authors": [{"name": "Daniel Ari Friedman"}],
        "keywords": ["fixture"],
    }
    config["metadata"] = {"license": "CC-BY-4.0"}
    (gate_tree / "docs" / "manuscript" / "config.yaml").write_text(
        yaml.safe_dump(config, sort_keys=False)
    )
    (gate_tree / "docs" / "manuscript" / "00_abstract.md").write_text(
        "# Abstract\n\nSynthetic fixture abstract without injected variables.\n"
    )
    write_quality_receipt(gate_tree, _gate_checks(), quality_input_fingerprint(gate_tree))
    fingerprint = quality_input_fingerprint(gate_tree)["sha256"]
    registry_path = gate_tree / "output" / "figures" / "figure_registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    for entry in registry:
        entry["generator_input_fingerprint"] = fingerprint
    registry_path.write_text(json.dumps(registry, indent=2) + "\n")
    metrics = json.loads((gate_tree / "output" / "metrics.json").read_text(encoding="utf-8"))
    render_all_chapters(gate_tree / "docs" / "manuscript", metrics, gate_tree / "output" / "manuscript")
    write_variables_manifest(gate_tree, metrics)
    write_release_metadata(gate_tree)
    pdf = gate_tree / "output" / "pdf" / "cognitive_case_diagrams_combined.pdf"
    pdf.parent.mkdir(parents=True, exist_ok=True)
    _write_real_pdf(pdf)
    web = gate_tree / "output" / "web" / "index.html"
    web.parent.mkdir(parents=True, exist_ok=True)
    web.write_text("<p>Fixture</p>\n")
    record_publication_review(
        gate_tree,
        pdf_page_count=2,
        inspected_pdf_pages=[1, 2],
        inspected_figures=["a.png"],
        browser_checks={name: True for name in BROWSER_CHECKS},
        pdf_metadata_checked=True,
        reviewer="Fixture Reviewer",
        method="fixture observation",
        limitations="Fixture limitation",
    )
    destination = (
        gate_tree / "output" / "releases" / "v2.4.0"
        / "cognitive_case_diagrams-2.4.0-reproducibility.zip"
    )
    manifest = build_release_archive(
        gate_tree, destination, version="2.4.0", publication_date="2026-09-07"
    )
    write_json_atomic(
        destination.parent / "zenodo-publication.json",
        validate_release_metadata(gate_tree)["publication"],
    )
    write_json_atomic(
        destination.parent / "release-validation.json",
        {
            "schema": "ccd-release-v1",
            "status": "passed",
            "source": quality_input_fingerprint(gate_tree)["sha256"],
            "tests_passed": 2,
            "coverage_percent": 95.0,
            "archive_sha256": manifest["archive_sha256"],
            "version": "2.4.0",
        },
    )
    return gate_tree


def test_empty_tree_reports_missing_and_undeclared_release(tmp_path: Path) -> None:
    code, report = status_of(tmp_path)
    assert code == 1
    assert report["schema"] == "ccd-evidence-status-v1"
    assert report["overall"] == "incomplete"
    assert report["version"] == "unknown"
    assert set(report["evidence"]) == set(STAGES)
    for name, entry in report["evidence"].items():
        expected = "invalid" if name == "release" else "missing"
        assert entry["state"] == expected
    assert "/private/" not in json.dumps(report)


def test_usage_error_exits_two() -> None:
    completed = run_cli("--no-such-flag")
    assert completed.returncode == 2


def test_missing_project_root_reports_error_envelope(tmp_path: Path) -> None:
    completed = run_cli("--project-root", str(tmp_path / "absent"))
    assert completed.returncode == 1
    envelope = json.loads(completed.stderr)
    assert envelope["schema"] == "ccd-evidence-status-v1"
    assert envelope["overall"] == "error"


def test_gate_tree_separates_validated_and_pending_stages(gate_tree: Path) -> None:
    code, report = status_of(gate_tree)
    assert code == 1
    states = {name: entry["state"] for name, entry in report["evidence"].items()}
    assert states == {
        "quality": "validated",
        "experiments": "validated",
        "manuscript": "validated",
        "metadata": "missing",
        "visual_review": "missing",
        "release": "invalid",
    }
    quality = report["evidence"]["quality"]
    assert quality["detail"] == "quality gate passed: 2 tests, 95.0% line-and-branch coverage"
    assert report["evidence"]["experiments"]["errors"] == []


def test_source_change_marks_quality_and_manuscript_stale_only(gate_tree: Path) -> None:
    (gate_tree / "src" / "example.py").write_text("value = 2\n")
    _, report = status_of(gate_tree)
    evidence = report["evidence"]
    assert evidence["quality"]["state"] == "stale"
    assert "stale for the current source" in evidence["quality"]["detail"]
    assert evidence["manuscript"]["state"] == "stale"
    assert evidence["experiments"]["state"] == "validated"


def test_experiments_binding_mutation_is_stale(gate_tree: Path) -> None:
    bound = sorted((gate_tree / "src" / "experiments").glob("*.py"))
    assert bound, "fixture did not copy bound experiment sources"
    target = bound[0]
    target.write_text(target.read_text(encoding="utf-8") + "\n# mutation\n")
    _, report = status_of(gate_tree)
    experiments = report["evidence"]["experiments"]
    assert experiments["state"] == "stale"
    assert any("stale source bytes" in error for error in experiments["errors"])


def test_forged_quality_receipt_is_invalid_not_stale(gate_tree: Path) -> None:
    receipt_path = gate_tree / "output" / "reports" / "quality_receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["pytest_passed"] = receipt["pytest_passed"] + 1
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    _, report = status_of(gate_tree)
    assert report["evidence"]["quality"]["state"] == "invalid"


def test_corrupted_experiment_results_are_invalid(gate_tree: Path) -> None:
    results = gate_tree / "output" / "experiments" / "results.json"
    results.write_text("{not json")
    _, report = status_of(gate_tree)
    assert report["evidence"]["experiments"]["state"] == "invalid"


def test_metadata_stage_states(tmp_path: Path) -> None:
    from src.release_metadata import write_release_metadata

    tree = tmp_path / "metadata-tree"
    tree.mkdir()
    (tree / "docs" / "manuscript").mkdir(parents=True)
    (tree / "output" / "manuscript").mkdir(parents=True)
    (tree / "output" / "manuscript" / "00_abstract.md").write_text(
        "# Abstract\n\nSynthetic fixture abstract without injected variables.\n"
    )
    config = {
        "paper": {"title": "Fixture", "version": "2.4.0", "date": "2026-09-07"},
        "publication": {
            "doi": "10.5281/zenodo.19695259",
            "version_doi": "10.5281/zenodo.22653315",
        },
        "authors": [{"name": "Daniel Ari Friedman"}],
        "keywords": ["fixture"],
        "metadata": {"license": "CC-BY-4.0"},
    }
    (tree / "docs" / "manuscript" / "config.yaml").write_text(yaml.safe_dump(config))
    (tree / "pyproject.toml").write_text(
        '[project]\nname = "cognitive_case_diagrams"\nversion = "2.4.0"\n'
        'license = "Apache-2.0"\n'
        '[project.urls]\nRepository = "https://github.com/docxology/cognitive_case_diagrams"\n'
    )
    write_release_metadata(tree)
    _, report = status_of(tree)
    assert report["evidence"]["metadata"]["state"] == "validated"
    citation = tree / "CITATION.cff"
    citation.write_text(citation.read_text(encoding="utf-8").replace("Fixture", "Renamed", 1))
    _, report = status_of(tree)
    assert report["evidence"]["metadata"]["state"] == "stale"
    citation.write_text("a: [unclosed\n")
    _, report = status_of(tree)
    assert report["evidence"]["metadata"]["state"] == "invalid"
    citation.unlink()
    (tree / ".zenodo.json").unlink()
    _, report = status_of(tree)
def test_visual_review_stage_states(gate_tree: Path) -> None:
    from src.publication_review import BROWSER_CHECKS

    pdf = gate_tree / "output" / "pdf" / "cognitive_case_diagrams_combined.pdf"
    pdf.parent.mkdir(parents=True, exist_ok=True)
    _write_real_pdf(pdf)
    web = gate_tree / "output" / "web" / "index.html"
    web.parent.mkdir(parents=True, exist_ok=True)
    web.write_text("<p>Fixture</p>\n")
    _, report = status_of(gate_tree)
    assert report["evidence"]["visual_review"]["state"] == "missing"
    record = gate_tree / "output" / "reports" / "publication_review.json"
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text(json.dumps({"schema": "ccd-publication-review-v0"}))
    _, report = status_of(gate_tree)
    assert report["evidence"]["visual_review"]["state"] == "invalid"
    record.write_text(json.dumps({"schema": "ccd-publication-review-v1"}))
    _, report = status_of(gate_tree)
    assert report["evidence"]["visual_review"]["state"] == "invalid"
    record.write_text(
        json.dumps(
            {
                "schema": "ccd-publication-review-v1",
                "inputs": {"quality_source": "0" * 64, "files": {}, "sha256": "1" * 64},
                "observations": {
                    "pdf_page_count": 2,
                    "inspected_pdf_pages": [1, 2],
                    "inspected_figures": ["a.png"],
                    "browser_checks": {name: True for name in BROWSER_CHECKS},
                    "pdf_metadata_checked": True,
                    "reviewer": "Fixture Reviewer",
                    "method": "fixture observation",
                    "limitations": "Fixture limitation",
                },
            }
        )
        + "\n"
    )
    _, report = status_of(gate_tree)
    assert report["evidence"]["visual_review"]["state"] == "stale"


def test_release_stage_undeclared_version_and_missing_archive(gate_tree: Path) -> None:
    _, report = status_of(gate_tree)
    assert report["evidence"]["release"]["state"] == "invalid"
    (gate_tree / "pyproject.toml").write_text(
        '[project]\nversion = "2.4.0"\n\n[tool.coverage.report]\nfail_under = 90\n'
    )
    _, report = status_of(gate_tree)
    assert report["evidence"]["release"]["state"] == "missing"


def test_integrated_tree_validates_end_to_end(gate_tree: Path) -> None:
    tree = _integrated_tree(gate_tree)
    code, report = status_of(tree)
    assert code == 0
    assert report["overall"] == "validated"
    assert report["version"] == "2.4.0"
    assert all(entry["state"] == "validated" for entry in report["evidence"].values())
    release = report["evidence"]["release"]
    assert set(release) >= {"state", "artifact", "detail", "archive_sha256"}
    assert len(release["archive_sha256"]) == 64


def test_release_record_corruption_and_absence(gate_tree: Path) -> None:
    tree = _integrated_tree(gate_tree)
    releases = tree / "output" / "releases" / "v2.4.0"
    validation = releases / "release-validation.json"
    record = json.loads(validation.read_text(encoding="utf-8"))
    record["archive_sha256"] = "0" * 64
    validation.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    _, report = status_of(tree)
    assert report["evidence"]["release"]["state"] == "invalid"
    (releases / "zenodo-publication.json").write_text('{"schema": "tampered"}\n')
    _, report = status_of(tree)
    assert report["evidence"]["release"]["state"] == "invalid"
    validation.unlink()
    _, report = status_of(tree)
    assert report["evidence"]["release"]["state"] == "missing"


def test_release_binding_is_stale_after_source_change(gate_tree: Path) -> None:
    tree = _integrated_tree(gate_tree)
    (tree / "src" / "example.py").write_text("value = 3\n")
    _, report = status_of(tree)
    assert report["evidence"]["release"]["state"] == "stale"
    assert report["evidence"]["quality"]["state"] == "stale"


def test_forged_archive_member_is_rejected(gate_tree: Path, tmp_path: Path) -> None:
    from src.release_validation import quality_input_fingerprint, write_quality_receipt

    tree = _integrated_tree(gate_tree)
    archive = (
        tree / "output" / "releases" / "v2.4.0"
        / "cognitive_case_diagrams-2.4.0-reproducibility.zip"
    )
    foreign = tmp_path / "foreign"
    shutil.copytree(tree, foreign)
    (foreign / "src" / "example.py").write_text("value = 999\n")
    foreign_receipt = write_quality_receipt(foreign, _gate_checks(), quality_input_fingerprint(foreign))
    with zipfile.ZipFile(archive) as bundle:
        entries = {name: bundle.read(name) for name in bundle.namelist()}
    entries["output/reports/quality_receipt.json"] = (
        json.dumps(foreign_receipt, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    manifest = json.loads(entries["RELEASE_MANIFEST.json"])
    payload = entries["output/reports/quality_receipt.json"]
    manifest["files"]["output/reports/quality_receipt.json"] = {
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
    }
    entries["RELEASE_MANIFEST.json"] = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 7, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, entries[name])
    _, report = status_of(tree)
    assert report["evidence"]["release"]["state"] == "stale"


def test_status_generates_nothing(gate_tree: Path) -> None:
    before = _snapshot(gate_tree)
    status_of(gate_tree)
    assert _snapshot(gate_tree) == before


def test_console_script_entry_point(gate_tree: Path) -> None:
    executable = shutil.which("ccd-evidence-status")
    assert executable, "ccd-evidence-status console script not installed in the test environment"
    completed = subprocess.run(
        [executable, "--project-root", str(gate_tree)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    report = json.loads(completed.stdout)
    assert completed.returncode == 1
    assert report["overall"] == "incomplete"


def test_clean_scrubs_only_the_project_root_prefix(tmp_path: Path) -> None:
    """Root prefixes are scrubbed; unrelated absolute paths stay verbatim."""
    from src.evidence_status import _clean

    nested = tmp_path / "project"
    detail = _clean(f"evidence at {nested}/output/reports/x.json", nested)
    assert detail == "evidence at <project>/output/reports/x.json"
    elsewhere = tmp_path / "elsewhere"
    assert _clean(f"refused {elsewhere}", nested) == f"refused {elsewhere}"


def test_report_is_byte_deterministic(gate_tree: Path, tmp_path: Path) -> None:
    """Two runs on unchanged trees emit byte-identical documents."""
    first = run_cli("--project-root", str(gate_tree))
    second = run_cli("--project-root", str(gate_tree))
    assert first.stdout == second.stdout
    empty_first = run_cli("--project-root", str(tmp_path))
    empty_second = run_cli("--project-root", str(tmp_path))
    assert empty_first.stdout == empty_second.stdout
    assert empty_first.returncode == 1


def _write_real_pdf(path: Path) -> None:
    """A real two-page PDF: the receipt validator derives counts from bytes."""
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.pyplot as plt

    path.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(path) as pdf:
        for _ in range(2):
            figure = plt.figure()
            pdf.savefig(figure)
            plt.close(figure)
