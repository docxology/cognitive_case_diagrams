"""Manuscript metrics generator for cognitive_case_diagrams.

Introspects the project's test suite and source modules to produce a
``metrics.json`` that the injection script uses to replace ``${variable}``
placeholders in manuscript files.

Public API:
    collect_metrics  -- gather all metrics from the project
    write_metrics    -- serialise to JSON

Usage (standalone):
    python -m src.generate_manuscript_metrics          # writes output/metrics.json
    python -m src.generate_manuscript_metrics --dry-run # prints to stdout
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_TESTS_DIR = _PROJECT_ROOT / "tests"
_DAIF_DIR = _PROJECT_ROOT / "src" / "daif"
_OUTPUT_DIR = _PROJECT_ROOT / "output"


# ---------------------------------------------------------------------------
# Collectors
# ---------------------------------------------------------------------------

def _count_test_files(tests_dir: Path) -> int:
    """Count ``test_*.py`` files in the tests/ directory."""
    return len(list(tests_dir.glob("test_*.py")))


def _count_collected_tests(project_root: Path) -> int:
    """Run ``pytest --collect-only -q`` and count collected test items.

    Falls back to a regex-based scan if pytest is unavailable.
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(project_root / "tests"), "--collect-only", "-q"],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=60,
        )
        # Last meaningful line is like "727 tests collected in 0.32s"
        for line in reversed(result.stdout.strip().splitlines()):
            if "collected" in line:
                parts = line.split()
                for part in parts:
                    if part.isdigit():
                        return int(part)
    except (subprocess.SubprocessError, OSError, ValueError):
        pass

    # Fallback: count ``def test_`` in all test files
    count = 0
    for tf in (project_root / "tests").glob("test_*.py"):
        content = tf.read_text(encoding="utf-8", errors="replace")
        count += content.count("\ndef test_")
        count += content.count("\n    def test_")  # methods in classes
    return count


def _count_daif_modules(daif_dir: Path) -> int:
    """Count Python source modules (excluding __init__.py) in src/daif/."""
    return len([
        f for f in daif_dir.glob("*.py")
        if f.name != "__init__.py"
    ])


def _count_daif_symbols(daif_dir: Path) -> int:
    """Count public symbols exported via ``__all__`` in src/daif/__init__.py."""
    init = daif_dir / "__init__.py"
    if not init.exists():
        return 0
    tree = ast.parse(init.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    if isinstance(node.value, ast.List):
                        return len(node.value.elts)
    return 0


def _count_daif_tests(tests_dir: Path) -> int:
    """Count test items in ``test_daif*.py`` files via AST scanning."""
    count = 0
    for tf in sorted(tests_dir.glob("test_daif*.py")):
        tree = ast.parse(tf.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name.startswith("test_"):
                    count += 1
    return count


def _count_daif_test_files(tests_dir: Path) -> int:
    """Count ``test_daif*.py`` files."""
    return len(list(tests_dir.glob("test_daif*.py")))


def _number_to_word(n: int) -> str:
    """Convert small integers to English words for prose use."""
    words = {
        1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
        6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
        11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
        15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen",
        19: "nineteen", 20: "twenty",
    }
    return words.get(n, str(n))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def collect_metrics(
    project_root: Path | None = None,
) -> dict[str, str]:
    """Collect all manuscript metrics from the project structure.

    Returns:
        Flat dict of variable name → string value, ready for
        ``string.Template.safe_substitute()``.
    """
    root = project_root or _PROJECT_ROOT
    tests_dir = root / "tests"
    daif_dir = root / "src" / "daif"

    total_tests = _count_collected_tests(root)
    total_files = _count_test_files(tests_dir)
    daif_modules = _count_daif_modules(daif_dir)
    daif_symbols = _count_daif_symbols(daif_dir)
    daif_tests = _count_daif_tests(tests_dir)
    daif_test_files = _count_daif_test_files(tests_dir)

    return {
        # Numeric strings
        "total_test_count": str(total_tests),
        "total_test_files": str(total_files),
        "daif_modules": str(daif_modules),
        "daif_symbols": str(daif_symbols),
        "daif_tests": str(daif_tests),
        "daif_test_files": str(daif_test_files),
        # English-word variants for prose
        "daif_modules_word": _number_to_word(daif_modules),
        "total_test_files_word": _number_to_word(total_files),
    }


def write_metrics(
    metrics: dict[str, str],
    output_path: Path | None = None,
) -> Path:
    """Serialise metrics to a JSON file.

    Args:
        metrics: Dict from :func:`collect_metrics`.
        output_path: Destination path.  Defaults to ``output/metrics.json``.

    Returns:
        Path of the written file.
    """
    dest = output_path or (_OUTPUT_DIR / "metrics.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    return dest


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> int:
    """CLI: collect metrics and write (or print in dry-run mode)."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate manuscript metrics")
    parser.add_argument("--dry-run", action="store_true", help="Print metrics to stdout only")
    parser.add_argument("--output", type=Path, default=None, help="Output path for metrics.json")
    args = parser.parse_args()

    metrics = collect_metrics()

    if args.dry_run:
        print(json.dumps(metrics, indent=2))
    else:
        dest = write_metrics(metrics, args.output)
        print(f"Wrote {len(metrics)} metrics to {dest}")

    # Summary
    for k, v in sorted(metrics.items()):
        print(f"  {k} = {v}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
