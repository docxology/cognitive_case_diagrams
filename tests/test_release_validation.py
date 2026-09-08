"""Real-file controls for stale or internally false publication receipts."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.release_validation import (
    QUALITY_JUNIT,
    QUALITY_RECEIPT,
    file_sha256,
    is_quality_input,
    quality_input_fingerprint,
    validate_quality_receipt,
    write_json_atomic,
    write_quality_receipt,
)


@pytest.fixture
def quality_tree(tmp_path: Path) -> Path:
    for name in ("src", "tests", "scripts"):
        (tmp_path / name).mkdir()
        (tmp_path / name / "example.py").write_text("value = 1\n")
    (tmp_path / "pyproject.toml").write_text("[tool.coverage.report]\nfail_under = 90\n")
    (tmp_path / "uv.lock").write_text("version = 1\n")
    (tmp_path / QUALITY_JUNIT).parent.mkdir(parents=True)
    (tmp_path / QUALITY_JUNIT).write_text(
        '<testsuites><testsuite><testcase name="analytic"/></testsuite></testsuites>'
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
    (tmp_path / "coverage.json").write_text(json.dumps(coverage))
    return tmp_path


def passing_checks() -> list[dict]:
    return [
        {"name": name, "exit_code": 0, "command": ["uv", "run", name]}
        for name in ("ruff", "mypy", "coverage")
    ]


def create_receipt(root: Path) -> dict:
    return write_quality_receipt(root, passing_checks(), quality_input_fingerprint(root))


def test_complete_receipt_binds_source_and_real_files(quality_tree: Path) -> None:
    receipt = create_receipt(quality_tree)
    assert validate_quality_receipt(quality_tree) == receipt
    assert receipt["tests"]["passed"] == 1
    assert receipt["coverage"]["percent"] == 95
    assert receipt["inputs"]["file_count"] == 5


@pytest.mark.parametrize(
    "relative",
    ["src/example.py", "tests/example.py", "scripts/example.py", "uv.lock", "pyproject.toml"],
)
def test_any_tested_input_mutation_invalidates_receipt(quality_tree: Path, relative: str) -> None:
    create_receipt(quality_tree)
    target = quality_tree / relative
    target.write_text(target.read_text() + "\n# changed\n")
    with pytest.raises(ValueError, match="stale"):
        validate_quality_receipt(quality_tree)


def test_concurrent_change_cannot_be_certified(quality_tree: Path) -> None:
    before = quality_input_fingerprint(quality_tree)
    (quality_tree / "src/example.py").write_text("value = 2\n")
    with pytest.raises(ValueError, match="changed while"):
        write_quality_receipt(quality_tree, passing_checks(), before)
    assert not (quality_tree / QUALITY_RECEIPT).exists()


@pytest.mark.parametrize(
    "checks",
    [
        [],
        [{"name": "ruff", "exit_code": 0}],
        [{"name": name, "exit_code": int(name == "mypy")} for name in ("ruff", "mypy", "coverage")],
        [{"name": name, "exit_code": False} for name in ("ruff", "mypy", "coverage")],
    ],
)
def test_failed_or_incomplete_gate_rejected(quality_tree: Path, checks: list) -> None:
    with pytest.raises(ValueError):
        write_quality_receipt(quality_tree, checks, quality_input_fingerprint(quality_tree))


@pytest.mark.parametrize(
    "replacement",
    [
        "<testsuites/>",
        "<testsuite><testcase><failure/></testcase></testsuite>",
        "<testsuite><testcase><error/></testcase></testsuite>",
        "<testsuite><testcase><skipped/></testcase></testsuite>",
        "<!DOCTYPE test><testsuite><testcase/></testsuite>",
    ],
)
def test_empty_failed_or_unsafe_test_evidence_rejected(
    quality_tree: Path, replacement: str
) -> None:
    (quality_tree / QUALITY_JUNIT).write_text(replacement)
    with pytest.raises(ValueError):
        create_receipt(quality_tree)


@pytest.mark.parametrize(
    "field,value",
    [
        ("covered_lines", 89),
        ("covered_lines", -1),
        ("covered_lines", True),
        ("covered_lines", 101),
        ("covered_branches", 21),
        ("percent_covered", 100),
        ("percent_covered", float("nan")),
        ("num_statements", 0),
    ],
)
def test_false_coverage_evidence_rejected(quality_tree: Path, field: str, value: object) -> None:
    path = quality_tree / "coverage.json"
    data = json.loads(path.read_text())
    data["totals"][field] = value
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        create_receipt(quality_tree)


def test_low_coverage_rejected_even_with_correct_arithmetic(quality_tree: Path) -> None:
    path = quality_tree / "coverage.json"
    data = json.loads(path.read_text())
    data["totals"].update(covered_lines=80, covered_branches=16, percent_covered=80)
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="below configured"):
        create_receipt(quality_tree)


def test_lowered_floor_and_absent_branches_rejected(quality_tree: Path) -> None:
    (quality_tree / "pyproject.toml").write_text("[tool.coverage.report]\nfail_under = 89\n")
    with pytest.raises(ValueError, match="floor"):
        create_receipt(quality_tree)
    (quality_tree / "pyproject.toml").write_text("[tool.coverage.report]\nfail_under = 90\n")
    path = quality_tree / "coverage.json"
    data = json.loads(path.read_text())
    data["meta"]["branch_coverage"] = False
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="branches"):
        create_receipt(quality_tree)


def test_altered_evidence_rejected(quality_tree: Path) -> None:
    create_receipt(quality_tree)
    path = quality_tree / QUALITY_JUNIT
    path.write_text(path.read_text().replace('name="analytic"', 'name="different"'))
    with pytest.raises(ValueError, match="current coverage/test evidence"):
        validate_quality_receipt(quality_tree)


@pytest.mark.parametrize("field,value", [("schema", "other"), ("status", "failed"), ("checks", [])])
def test_tampered_receipt_rejected(quality_tree: Path, field: str, value: object) -> None:
    data = create_receipt(quality_tree)
    data[field] = value
    write_json_atomic(quality_tree / QUALITY_RECEIPT, data)
    with pytest.raises(ValueError):
        validate_quality_receipt(quality_tree)


def test_symlinks_cannot_enter_quality_fingerprint(quality_tree: Path, tmp_path: Path) -> None:
    linked = quality_tree / "src/linked.py"
    linked.symlink_to(quality_tree / "tests/example.py")
    with pytest.raises(ValueError, match="Linked quality input"):
        quality_input_fingerprint(quality_tree)
    with pytest.raises(ValueError, match="regular file"):
        file_sha256(linked)


def test_atomic_writer_preserves_previous_value_on_nonfinite_input(tmp_path: Path) -> None:
    target = tmp_path / "state.json"
    write_json_atomic(target, {"valid": 1})
    with pytest.raises(ValueError):
        write_json_atomic(target, {"invalid": float("inf")})
    assert json.loads(target.read_text()) == {"valid": 1}
    linked = tmp_path / "linked.json"
    linked.symlink_to(target)
    with pytest.raises(ValueError, match="linked"):
        write_json_atomic(linked, {"valid": 2})


@pytest.mark.parametrize("stamp", [None, "", "yesterday", "2026-09-07T12:00:00"])
def test_timestamp_contract_cannot_be_forged(quality_tree: Path, stamp: object) -> None:
    receipt = create_receipt(quality_tree)
    receipt["recorded_at_utc"] = receipt["generated_at"] = stamp
    write_json_atomic(quality_tree / QUALITY_RECEIPT, receipt)
    with pytest.raises(ValueError, match="timestamp"):
        validate_quality_receipt(quality_tree)


@pytest.mark.parametrize("command", [None, "uv run pytest", [], ["uv", ""]])
def test_command_provenance_is_required(quality_tree: Path, command: object) -> None:
    receipt = create_receipt(quality_tree)
    receipt["checks"][0]["command"] = command
    write_json_atomic(quality_tree / QUALITY_RECEIPT, receipt)
    with pytest.raises(ValueError, match="command"):
        validate_quality_receipt(quality_tree)


def test_flat_consumer_fields_cannot_disagree(quality_tree: Path) -> None:
    receipt = create_receipt(quality_tree)
    receipt["pytest_passed"] = 500
    write_json_atomic(quality_tree / QUALITY_RECEIPT, receipt)
    with pytest.raises(ValueError, match="Manuscript-facing"):
        validate_quality_receipt(quality_tree)


def test_documentation_and_test_data_changes_stale_the_receipt(quality_tree: Path) -> None:
    folder = quality_tree / "docs/manuscript"
    folder.mkdir(parents=True)
    config = folder / "config.yaml"
    config.write_text("paper: example\n")
    create_receipt(quality_tree)
    config.write_text("paper: changed\n")
    with pytest.raises(ValueError, match="stale"):
        validate_quality_receipt(quality_tree)


def test_public_receipt_is_readable_and_atomic(quality_tree: Path) -> None:
    import stat
    create_receipt(quality_tree)
    assert stat.S_IMODE((quality_tree / QUALITY_RECEIPT).stat().st_mode) == 0o644


def test_egg_info_residue_never_enters_fingerprint(quality_tree: Path) -> None:
    """Build residue is excluded from fingerprints and archive membership."""
    before = quality_input_fingerprint(quality_tree)
    residue = quality_tree / "src" / "example.egg-info"
    residue.mkdir()
    (residue / "SOURCES.txt").write_text("example.py\n")
    (residue / "requires.txt").write_text("numpy\n")
    assert quality_input_fingerprint(quality_tree) == before
    assert not is_quality_input("src/example.egg-info/SOURCES.txt")
    assert not is_quality_input("src/example.egg-info/PKG-INFO")
