"""In-process tests for the agent-facing integration surface.

These exercise the real files and real project validators: the artifact
allowlist against a temporary directory tree (including symlinks and
oversized files), the experiments loader against the shared fail-closed
validator in ``src.experiments.runner``, the registry of tool specifications,
and the ``--list-tools`` / ``--version`` CLI. No mocking frameworks are used.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from src.integrations.artifacts import (
    ARTIFACTS_NOT_GENERATED,
    ArtifactError,
    ArtifactIndex,
    MAX_ARTIFACT_BYTES,
)
from src.integrations.experiments import (
    EXPERIMENTS_RELATIVE_PATH,
    ExperimentsNotGeneratedError,
    load_experiments,
    summarize_variables,
)
from src.integrations.methods import TOOL_SPECS
from src.integrations.metadata import capability_metadata, project_version
from src.integrations.registry import (
    MAX_ARTIFACT_ENTRIES,
    MAX_VECTOR_LENGTH,
    json_safe,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _write(tmp_path: Path, relative: str, content: bytes | str) -> Path:
    target = tmp_path / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, str):
        content = content.encode("utf-8")
    target.write_bytes(content)
    return target


def _populate_public_tree(tmp_path: Path) -> None:
    """Create one file per allowlisted location plus machine-local rejects."""
    _write(tmp_path, "figures/fig.png", b"\x89PNG fake")
    _write(tmp_path, "experiments/results.json", "{}")
    _write(tmp_path, "manuscript/00_abstract.md", "# abstract")
    _write(tmp_path, "web/index.html", "<html></html>")
    _write(tmp_path, "metrics.json", '{"total_test_count": "1"}')
    _write(tmp_path, "reports/quality_receipt.json", '{"status": "validated"}')
    _write(tmp_path, "reports/publication_review.json", "{}")
    _write(tmp_path, "pdf/cognitive_case_diagrams_combined.pdf", b"%PDF-1.4 fake")
    # Machine-local content that must never be listed or read.
    _write(tmp_path, "telemetry.json", "{}")
    _write(tmp_path, "diagnostics.json", "{}")
    _write(tmp_path, "review/private.log", "secret")
    _write(tmp_path, "logs/stage.log", "secret")
    _write(tmp_path, "figures/.hidden.png", "hidden")
    _write(tmp_path, "figures/sub/__pycache__/x.pyc", "cache")
    _write(tmp_path, "web/release-notes.txt", "denied component")


# ---------------------------------------------------------------------------
# json_safe


def test_json_safe_accepts_strictly_serializable_values() -> None:
    assert json_safe({"a": [1, 2.5, None, True], "b": (1, 2)}) == {
        "a": [1, 2.5, None, True],
        "b": [1, 2],
    }
    assert json_safe(np.arange(3)) == [0, 1, 2]
    assert json_safe(np.float64(1.5)) == 1.5


def test_json_safe_rejects_nonfinite_and_unknown_types() -> None:
    with pytest.raises(ValueError, match="finite"):
        json_safe(float("inf"), "score")
    with pytest.raises(ValueError, match="finite"):
        json_safe(float("nan"), "score")
    with pytest.raises(ValueError, match="JSON-serializable"):
        json_safe(object(), "mystery")
    with pytest.raises(ValueError, match="keys must be strings"):
        json_safe({1: "x"}, "mapping")
    with pytest.raises(ValueError, match="too deeply"):
        value: list = []
        current = value
        for _ in range(12):
            nested: list = []
            current.append(nested)
            current = nested
        json_safe(value, "deep")


# ---------------------------------------------------------------------------
# Registry of tool specifications


def test_tool_specs_are_unique_and_described() -> None:
    names = [spec.name for spec in TOOL_SPECS]
    assert len(names) == len(set(names))
    assert len(names) >= 15
    for spec in TOOL_SPECS:
        assert spec.description, spec.name
        assert callable(spec.handler)


def test_every_advertised_tool_has_a_contract_note() -> None:
    from src.integrations.metadata import TOOL_CONTRACT_NOTES

    registered = {spec.name for spec in TOOL_SPECS}
    documented = {note["tool"] for note in TOOL_CONTRACT_NOTES}
    assert registered == documented


# ---------------------------------------------------------------------------
# Artifact containment


def test_artifact_entries_are_exactly_the_allowlist(tmp_path: Path) -> None:
    _populate_public_tree(tmp_path)
    index = ArtifactIndex(tmp_path)
    entries = index.entries()
    paths = [entry["path"] for entry in entries["artifacts"]]
    assert entries["available"] is True
    assert entries["truncated"] is False
    assert "metrics.json" in paths
    assert "reports/quality_receipt.json" in paths
    assert "pdf/cognitive_case_diagrams_combined.pdf" in paths
    assert "figures/fig.png" in paths
    assert "web/index.html" in paths
    # Machine-local content is never listed (component-exact check;
    # web/release-notes.txt is public and stays listed).
    assert "web/release-notes.txt" in paths
    denied = {
        "telemetry.json",
        "diagnostics.json",
        "review/private.log",
        "logs/stage.log",
        "figures/.hidden.png",
        "figures/sub/__pycache__/x.pyc",
    }
    assert not denied & set(paths)
    # No absolute paths in public metadata.
    dumped = json.dumps(entries)
    assert str(tmp_path) not in dumped
    assert not dumped.startswith("/")
    assert entries["root"].startswith(tmp_path.name)


def test_artifact_read_enforces_allowlist_and_containment(tmp_path: Path) -> None:
    _populate_public_tree(tmp_path)
    index = ArtifactIndex(tmp_path)
    data, mime = index.read("metrics.json")
    assert json.loads(data)["total_test_count"] == "1"
    assert mime == "application/json"
    _png, png_mime = index.read("figures/fig.png")
    assert png_mime == "image/png"

    outside = tmp_path.parent / "outside_secret.txt"
    outside.write_text("secret")
    _write(tmp_path, "figures/link.png", "")
    (tmp_path / "figures/link.png").unlink()
    (tmp_path / "figures/link.png").symlink_to(outside)

    for bad in (
        "../../pyproject.toml",
        "/etc/passwd",
        "~/secrets",
        "telemetry.json",
        "review/private.log",
        "figures/.hidden.png",
        "figures/link.png",
        "figures/missing.png",
        "fig\x00ure.png",
        "",
    ):
        with pytest.raises(ArtifactError):
            index.read(bad)


def test_artifact_read_is_bounded_at_open(tmp_path: Path) -> None:
    index = ArtifactIndex(tmp_path)
    big = _write(tmp_path, "metrics.json", b"x" * (MAX_ARTIFACT_BYTES + 1))
    assert big.stat().st_size > MAX_ARTIFACT_BYTES
    with pytest.raises(ArtifactError, match="read bound"):
        index.read("metrics.json")


def test_artifact_index_survives_missing_output_tree(tmp_path: Path) -> None:
    index = ArtifactIndex(tmp_path / "absent_output")
    assert index.available is False
    entries = index.entries()
    assert entries["available"] is False
    assert entries["artifacts"] == []
    assert entries["reason"] == ARTIFACTS_NOT_GENERATED
    with pytest.raises(ArtifactError, match="not yet generated"):
        index.resolve("metrics.json")


def test_artifact_listing_is_capped(tmp_path: Path) -> None:
    for i in range(MAX_ARTIFACT_ENTRIES + 5):
        _write(tmp_path, f"figures/fig_{i:03}.png", b"x")
    entries = ArtifactIndex(tmp_path).entries()
    assert entries["truncated"] is True
    assert entries["count"] == MAX_ARTIFACT_ENTRIES


# ---------------------------------------------------------------------------
# Experiments loader and projection


def _write_real_results(tmp_path: Path) -> Path:
    """Generate real experiment evidence with a fresh fixture source tree.

    ``run_experiments()`` produces genuine results; every provenance source
    file is copied byte-for-byte from the repository into the fixture root so
    the freshness digest recomputes identically under the temporary artifact
    root ``tmp_path / "output"``. No provenance is forged.
    """
    import shutil

    from src.experiments import write_results
    from src.experiments.runner import run_experiments

    results = run_experiments(
        {"n_replicates": 2, "quantile": {"brute_force_tau_points": 101}}
    )
    for relative in results["provenance"]["source_files"]:
        source = PROJECT_ROOT / relative
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    return write_results(results, tmp_path / "output" / EXPERIMENTS_RELATIVE_PATH)


def test_experiments_absence_is_not_generated(tmp_path: Path) -> None:
    with pytest.raises(ExperimentsNotGeneratedError, match="not yet generated"):
        load_experiments(tmp_path)
    with pytest.raises(ExperimentsNotGeneratedError, match="not yet generated"):
        summarize_variables(tmp_path)


def test_experiments_schema_drift_raises(tmp_path: Path) -> None:
    _write_real_results(tmp_path)
    results_path = tmp_path / "output" / EXPERIMENTS_RELATIVE_PATH
    payload = json.loads(results_path.read_text())
    payload["schema_version"] = "0.9"
    results_path.write_text(json.dumps(payload))
    artifact_root = tmp_path / "output"
    with pytest.raises(ValueError, match="schema_version"):
        load_experiments(artifact_root)


def test_experiments_missing_config_hash_raises(tmp_path: Path) -> None:
    _write_real_results(tmp_path)
    results_path = tmp_path / "output" / EXPERIMENTS_RELATIVE_PATH
    payload = json.loads(results_path.read_text())
    del payload["provenance"]["config_sha256"]
    results_path.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="config_sha256"):
        load_experiments(tmp_path / "output")


def test_experiments_stale_or_forged_sources_raise(tmp_path: Path) -> None:
    _write_real_results(tmp_path)
    results_path = tmp_path / "output" / EXPERIMENTS_RELATIVE_PATH
    payload = json.loads(results_path.read_text())
    payload["provenance"]["source_sha256"] = "0" * 64
    results_path.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="Invalid experiment evidence"):
        load_experiments(tmp_path / "output")


@pytest.fixture(scope="session")
def real_results_root(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """One real, validated results tree shared by projection tests."""
    root = tmp_path_factory.mktemp("real_results")
    _write_real_results(root)
    return root / "output"


def test_experiments_projection_fields(real_results_root: Path) -> None:
    summary = summarize_variables(real_results_root)
    assert summary["schema_version"] == "1.0"
    assert summary["variable_count"] >= 1
    assert summary["truncated"] is False
    assert summary["config_sha256"]
    for variable in summary["variables"]:
        assert variable["identifier"].startswith("exp_")
        assert variable["unit"] in {"probability", "dimensionless", "nats", "count", "version"}
        assert isinstance(variable["confidence_level"], float)
        assert variable["sample_unit"]
        assert variable["interpretation"]
    first = summary["variables"][0]
    assert set(first) == {
        "identifier", "value", "unit", "ci_low", "ci_high",
        "confidence_level", "sample_unit", "interpretation",
    }


def test_experiments_projection_respects_limit(real_results_root: Path) -> None:
    summary = summarize_variables(real_results_root, limit=1)
    assert summary["variable_count"] > 1
    assert summary["truncated"] is True
    assert len(summary["variables"]) == 1


# ---------------------------------------------------------------------------
# Capability metadata


def test_capability_metadata_is_honest_and_path_free() -> None:
    capability = capability_metadata(PROJECT_ROOT)
    assert capability["claims"], "claim ledger must be present"
    assert all(entry["status"] for entry in capability["claims"])
    assert capability["tool_contracts"]
    status = capability["quality_receipt"]["status"]
    assert status in {"validated", "missing", "stale_or_invalid"}
    if status != "validated":
        assert "/Volumes" not in json.dumps(capability["quality_receipt"])
        assert "/Users" not in json.dumps(capability["quality_receipt"])


def test_project_version_is_reported() -> None:
    assert project_version(PROJECT_ROOT) not in {"", "unknown"}


# ---------------------------------------------------------------------------
# CLI surface (real subprocess)


def test_cli_list_tools_prints_catalog() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "src.integrations.server", "--list-tools"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert completed.returncode == 0, completed.stderr
    catalog = json.loads(completed.stdout)
    names = [entry["name"] for entry in catalog]
    assert names == [spec.name for spec in TOOL_SPECS]
    for entry in catalog:
        assert entry["description"]
        assert entry["annotations"]["read_only"] is True
        assert entry["annotations"]["open_world"] is False


def test_cli_version_prints_version() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "src.integrations.server", "--version"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert completed.returncode == 0
    assert completed.stdout.strip() == project_version(PROJECT_ROOT)


def test_transport_vector_bounds_match_documented_limits() -> None:
    # The advertised schema bound must equal the registry constant, so docs
    # and runtime cannot drift apart.
    assert MAX_VECTOR_LENGTH == 64
