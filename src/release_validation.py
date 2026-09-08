"""Source-bound quality receipts and release integrity primitives.

Receipts describe executed local checks. They are not signed attestations or
independent reviews. Changes to tested code, configuration, or test inputs make
the receipt stale instead of silently retaining a previous passing headline.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import shlex
import tempfile
import xml.etree.ElementTree as ET
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:  # Python 3.10
    import tomli as tomllib  # type: ignore[no-redef]


QUALITY_RECEIPT = Path("output/reports/quality_receipt.json")
QUALITY_JUNIT = Path("output/reports/pytest.xml")


def file_sha256(path: Path) -> str:
    """Hash a regular file without following a final symlink."""
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Expected a regular file: {path.name}")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


QUALITY_CACHE_PARTS = frozenset({"__pycache__", "node_modules", "build", "dist", "target", ".venv"})
_QUALITY_DIRECTORIES = ("src", "scripts", "tests", "docs", "skills")
_QUALITY_SUFFIXES = frozenset({".py", ".md", ".json", ".yaml", ".yml", ".toml", ".bib", ".txt"})
_QUALITY_ROOT_FILES = frozenset({"pyproject.toml", "uv.lock", "README.md", "AGENTS.md", "SKILL.md", "MANIFEST.in", ".github/workflows/ci.yml"})


def is_quality_input(relative: str) -> bool:
    """Shared source/test/data membership policy for disk and archive receipts."""
    path = Path(relative)
    if relative in _QUALITY_ROOT_FILES:
        return True
    return (len(path.parts) > 1 and path.parts[0] in _QUALITY_DIRECTORIES
            and path.suffix in _QUALITY_SUFFIXES
            and not any(part.startswith(".") or part in QUALITY_CACHE_PARTS for part in path.parts))


def quality_input_fingerprint(project_root: Path) -> dict[str, Any]:
    """Identify local source, configuration, documentation and test data inputs."""
    root = project_root.resolve(strict=True)
    files: list[Path] = []
    for directory in _QUALITY_DIRECTORIES:
        folder = root / directory
        if folder.is_symlink() or (directory in ("src", "scripts", "tests") and not folder.is_dir()):
            raise ValueError(f"Missing or linked quality input directory: {directory}")
        if folder.is_dir():
            files.extend(p for p in folder.rglob("*") if p.is_file() and is_quality_input(p.relative_to(root).as_posix()))
    files.extend(root / name for name in _QUALITY_ROOT_FILES if (root / name).exists() or name in ("pyproject.toml", "uv.lock"))
    hashes: dict[str, str] = {}
    for path in sorted(files):
        relative = path.relative_to(root)
        current = root
        for component in relative.parts:
            current = current / component
            if current.is_symlink():
                raise ValueError(f"Linked quality input: {relative}")
        hashes[relative.as_posix()] = file_sha256(path)
    encoded = json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()
    return {"sha256": hashlib.sha256(encoded).hexdigest(), "file_count": len(hashes), "files": hashes}


def write_json_atomic(path: Path, payload: Mapping[str, Any]) -> None:
    """Write complete finite JSON, replacing the destination only after success."""
    text = json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
        raise ValueError("Refusing to replace a linked JSON destination")
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        except BaseException:
            temporary.unlink()
            raise
    try:
        temporary.chmod(0o644)  # These are public project evidence artifacts.
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def _nonnegative_int(value: object, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field} must be a nonnegative integer")
    return value


def _coverage_summary(root: Path) -> dict[str, Any]:
    config = tomllib.loads((root / "pyproject.toml").read_text())
    floor = float(config["tool"]["coverage"]["report"]["fail_under"])
    if not math.isfinite(floor) or not 90 <= floor <= 100:
        raise ValueError("Project combined coverage floor must remain between 90 and 100 percent")
    coverage = json.loads((root / "coverage.json").read_text())
    if coverage.get("meta", {}).get("branch_coverage") is not True:
        raise ValueError("Release coverage must include branches")
    totals = coverage["totals"]
    fields = ("covered_lines", "num_statements", "covered_branches", "num_branches")
    counts = {name: _nonnegative_int(totals[name], name) for name in fields}
    if (
        counts["covered_lines"] > counts["num_statements"]
        or counts["covered_branches"] > counts["num_branches"]
    ):
        raise ValueError("Coverage counts exceed measured inputs")
    denominator = counts["num_statements"] + counts["num_branches"]
    if denominator == 0:
        raise ValueError("Empty coverage is not passing evidence")
    percent = 100 * (counts["covered_lines"] + counts["covered_branches"]) / denominator
    reported = float(totals["percent_covered"])
    if not math.isfinite(reported) or not math.isclose(percent, reported, abs_tol=1e-7):
        raise ValueError("Coverage percentage disagrees with line and branch counts")
    if percent < floor:
        raise ValueError(f"Combined coverage {percent:.2f}% is below configured {floor:.2f}%")
    return {
        **counts,
        "percent": percent,
        "floor": floor,
        "sha256": file_sha256(root / "coverage.json"),
    }


def _test_summary(root: Path) -> dict[str, int | str]:
    path = root / QUALITY_JUNIT
    if path.stat().st_size > 16 * 1024 * 1024:
        raise ValueError("Unexpectedly large test receipt")
    text = path.read_text()
    if "<!DOCTYPE" in text or "<!ENTITY" in text:
        raise ValueError("DTD declarations are forbidden in test receipts")
    document = ET.fromstring(text)
    cases = list(document.iter("testcase"))
    if not cases:
        raise ValueError("An empty test run is not passing evidence")
    failures = sum(case.find("failure") is not None for case in cases)
    errors = sum(case.find("error") is not None for case in cases)
    skipped = sum(case.find("skipped") is not None for case in cases)
    passed = len(cases) - failures - errors - skipped
    if failures or errors or passed <= 0:
        raise ValueError(f"Test receipt has {failures} failures, {errors} errors, {passed} passes")
    return {
        "total": len(cases),
        "passed": passed,
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
        "sha256": file_sha256(path),
    }


def _public_fields(receipt: Mapping[str, Any]) -> dict[str, Any]:
    """Flat manuscript-facing fields, derived rather than separately trusted."""
    tests, coverage = receipt["tests"], receipt["coverage"]
    command = next(check["command"] for check in receipt["checks"] if check["name"] == "coverage")
    return {
        "ok": True,
        "pytest_collected": tests["total"],
        "pytest_passed": tests["passed"],
        "pytest_failed": tests["failures"],
        "pytest_errors": tests["errors"],
        "pytest_skipped": tests["skipped"],
        "coverage_percent": coverage["percent"],
        "coverage_lines_covered": coverage["covered_lines"],
        "coverage_lines_total": coverage["num_statements"],
        "coverage_branches_covered": coverage["covered_branches"],
        "coverage_branches_total": coverage["num_branches"],
        "quality_input_fingerprint": receipt["inputs"]["sha256"],
        "generated_at": receipt["recorded_at_utc"],
        "suite_command": shlex.join(command),
    }


def write_quality_receipt(
    project_root: Path,
    checks: Sequence[Mapping[str, Any]],
    input_fingerprint: Mapping[str, Any],
) -> dict[str, Any]:
    """Record a complete gate only when executed checks and source hashes agree."""
    root = project_root.resolve(strict=True)
    if len(checks) != 3 or {check.get("name") for check in checks} != {"ruff", "mypy", "coverage"}:
        raise ValueError("A quality receipt requires Ruff, mypy and coverage checks")
    if any(type(check.get("exit_code")) is not int or check["exit_code"] != 0 for check in checks):
        raise ValueError("A failed check cannot produce a passing quality receipt")
    current = quality_input_fingerprint(root)
    if current != input_fingerprint:
        raise ValueError("Quality inputs changed while the gate was running")
    receipt = {
        "schema": "ccd-quality-v1",
        "status": "passed",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "inputs": current,
        "checks": list(checks),
        "tests": _test_summary(root),
        "coverage": _coverage_summary(root),
    }
    receipt.update(_public_fields(receipt))
    write_json_atomic(root / QUALITY_RECEIPT, receipt)
    return receipt


def validate_quality_receipt(project_root: Path) -> dict[str, Any]:
    """Reject absent, failed, internally inconsistent, or stale local evidence."""
    root = project_root.resolve(strict=True)
    receipt = json.loads((root / QUALITY_RECEIPT).read_text())
    if not isinstance(receipt, dict):
        raise ValueError("Quality receipt must be a JSON object")
    if receipt.get("schema") != "ccd-quality-v1" or receipt.get("status") != "passed":
        raise ValueError("Unsupported or nonpassing quality receipt")
    try:
        timestamp = datetime.fromisoformat(receipt["recorded_at_utc"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Quality receipt requires an ISO timestamp") from exc
    if timestamp.utcoffset() is None:
        raise ValueError("Quality receipt timestamp must include a timezone")
    if receipt.get("inputs") != quality_input_fingerprint(root):
        raise ValueError("Quality receipt is stale for the current source")
    checks = receipt.get("checks", [])
    if (
        len(checks) != 3
        or {check.get("name") for check in checks} != {"ruff", "mypy", "coverage"}
        or any(
            type(check.get("exit_code")) is not int or check["exit_code"] != 0 for check in checks
        )
    ):
        raise ValueError("Quality receipt does not report three passing checks")
    for check in checks:
        command = check.get("command")
        if not isinstance(command, list) or not command or any(
            not isinstance(token, str) or not token.strip() for token in command
        ):
            raise ValueError("Quality receipt requires executed command tokens")
    if receipt.get("coverage") != _coverage_summary(root) or receipt.get("tests") != _test_summary(
        root
    ):
        raise ValueError("Quality receipt does not match its current coverage/test evidence")
    if any(receipt.get(key) != value for key, value in _public_fields(receipt).items()):
        raise ValueError("Manuscript-facing quality fields disagree with executed checks")
    return receipt
