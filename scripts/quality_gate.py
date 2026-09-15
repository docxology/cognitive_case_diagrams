#!/usr/bin/env python3
"""Runnable quality gate: ruff over src/, tests/, and scripts/; mypy over src/ only; optional coverage.

The remediation review found mypy *configured* in ``pyproject.toml`` but never
run by anything (real errors sat unreported), and no linter wired up at all.
This gate makes both a single runnable command so they cannot silently rot:

    uv run python scripts/quality_gate.py               # ruff + mypy (~2 min)
    uv run python scripts/quality_gate.py --coverage    # + pytest --cov (~8 min)

``--coverage`` runs the full test suite under ``--cov=src`` so the
``[tool.coverage.report] fail_under = 90`` floor is actually enforced by one
command locally and in the repository's Python-version CI matrix.

Exit codes follow the pipeline convention: 0 = clean, 1 = at least one tool
reported findings. Every finding is printed; nothing is suppressed.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
import time

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from src.release_validation import quality_input_fingerprint, write_quality_receipt


def _uv_run(*tool_args: str) -> list[str]:
    """Compose a locked project-tool invocation."""
    return ["uv", "run", "--frozen", *tool_args]


def _parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse the gate invocation; argparse exits 2 on unknown arguments."""
    parser = argparse.ArgumentParser(
        prog="quality_gate.py",
        description="Run ruff and mypy (and optionally coverage) as one fail-closed gate.",
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="also run the test suite under --cov=src and write the quality receipt",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run ruff and mypy (and optionally coverage); return 1 on findings."""
    with_coverage = _parse_args(sys.argv[1:] if argv is None else argv).coverage

    before = quality_input_fingerprint(_PROJECT_ROOT)

    checks: list[tuple[str, list[str]]] = [
        ("ruff", _uv_run("ruff", "check", "src/", "tests/", "scripts/")),
        ("mypy", _uv_run("mypy", "src/")),
    ]
    if with_coverage:
        # fail_under = 90 in pyproject makes pytest exit non-zero below the floor.
        checks.append(
            (
                "coverage",
                [
                    "uv",
                    "run",
                    "--frozen",
                    "pytest",
                    "tests/",
                    "--cov=src",
                    "--cov-report=term-missing",
                    "--cov-report=json:coverage.json",
                    "-q",
                    "--no-header",
                    "--junitxml=output/reports/pytest.xml",
                ],
            )
        )

    failures: list[str] = []
    receipts: list[dict] = []
    for name, cmd in checks:
        print(f"==> {name}: {' '.join(cmd)}", flush=True)
        started = time.monotonic()
        result = subprocess.run(cmd, cwd=str(_PROJECT_ROOT))
        receipts.append(
            {
                "name": name,
                "command": cmd,
                "exit_code": result.returncode,
                "elapsed_seconds": round(time.monotonic() - started, 3),
            }
        )
        if result.returncode != 0:
            failures.append(name)

    if failures:
        print(f"quality gate FAILED: {', '.join(failures)}", file=sys.stderr)
        return 1
    if with_coverage:
        try:
            receipt = write_quality_receipt(_PROJECT_ROOT, receipts, before)
        except (OSError, ValueError, KeyError) as exc:
            print(f"quality receipt FAILED: {exc}", file=sys.stderr)
            return 1
        print(f"Source-bound quality receipt: {receipt['tests']['passed']} passed", flush=True)
    print("quality gate: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
