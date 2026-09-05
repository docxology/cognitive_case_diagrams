#!/usr/bin/env python3
"""Runnable quality gate: ruff + mypy over src/ and tests/.

The remediation review found mypy *configured* in ``pyproject.toml`` but never
run by anything (real errors sat unreported), and no linter wired up at all.
This gate makes both a single runnable command so they cannot silently rot:

    uv run python scripts/quality_gate.py

Exit codes follow the pipeline convention: 0 = clean, 1 = at least one tool
reported findings. Every finding is printed; nothing is suppressed.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _uv_run(*tool_args: str) -> list[str]:
    """Compose a `uv run --with <tool>` invocation rooted at the project."""
    return ["uv", "run", "--with", *tool_args]


def main() -> int:
    """Run ruff and mypy against the configured targets; return 1 on findings."""
    checks: list[tuple[str, list[str]]] = [
        ("ruff", _uv_run("ruff", "ruff", "check", "src/", "tests/")),
        ("mypy", _uv_run("mypy", "mypy", "src/")),
    ]

    failures: list[str] = []
    for name, cmd in checks:
        print(f"==> {name}: {' '.join(cmd)}", flush=True)
        result = subprocess.run(cmd, cwd=str(_PROJECT_ROOT))
        if result.returncode != 0:
            failures.append(name)

    if failures:
        print(f"quality gate FAILED: {', '.join(failures)}", file=sys.stderr)
        return 1
    print("quality gate: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
