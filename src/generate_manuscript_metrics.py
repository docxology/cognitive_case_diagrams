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

Coverage totals are read from ``coverage.json`` in the project root when present
(regenerate with ``uv run pytest tests/ --cov=src --cov-report=json``).
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from importlib import metadata
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_TESTS_DIR = _PROJECT_ROOT / "tests"
_DAIF_DIR = _PROJECT_ROOT / "src" / "daif"
_SRC_DIR = _PROJECT_ROOT / "src"
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
            timeout=120,
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


def _count_domain_subpackages(src_dir: Path) -> int:
    """Count first-level packages under ``src/`` (directories with ``__init__.py``)."""
    n = 0
    for p in src_dir.iterdir():
        if p.is_dir() and p.name != "__pycache__" and (p / "__init__.py").is_file():
            n += 1
    return n


def _optional_distribution_version(name: str) -> str:
    """Return installed package version or empty string."""
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return ""


def _read_coverage_totals(project_root: Path) -> dict[str, str]:
    """Parse ``coverage.json`` (pytest-cov / coverage.py JSON report) if present."""
    cov_path = project_root / "coverage.json"
    if not cov_path.is_file():
        return {}
    try:
        data = json.loads(cov_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    totals = data.get("totals") or {}
    if not isinstance(totals, dict) or not totals:
        return {}

    out: dict[str, str] = {}
    pct_disp = totals.get("percent_covered_display")
    if pct_disp is not None:
        s = str(pct_disp).strip().rstrip("%")
        out["coverage_percent"] = s
    pc = totals.get("percent_covered")
    if isinstance(pc, (int, float)):
        out["coverage_percent_raw"] = f"{float(pc):.2f}"

    for key, json_key in (
        ("coverage_lines_covered", "covered_lines"),
        ("coverage_lines_total", "num_statements"),
        ("coverage_branches_covered", "covered_branches"),
        ("coverage_branches_total", "num_branches"),
    ):
        v = totals.get(json_key)
        if v is not None:
            out[key] = str(int(v))

    # One-line fragment for prose (always safe for substitution)
    pct = out.get("coverage_percent") or out.get("coverage_percent_raw", "")
    if pct:
        out["coverage_summary"] = (
            f"{pct}% line-and-branch coverage on ``src/`` (from ``coverage.json``)"
        )
    return out


_ONES = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
)
_TENS = (
    "",
    "",
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety",
)


def _number_to_word(n: int) -> str:
    """Convert non-negative integers to English words for prose (0–999, then decimal string)."""
    if n < 0:
        return str(n)
    if n < 20:
        return _ONES[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        if ones == 0:
            return _TENS[tens]
        return f"{_TENS[tens]}-{_ONES[ones]}"
    if n < 1000:
        hundreds, rest = divmod(n, 100)
        head = f"{_ONES[hundreds]} hundred"
        if rest == 0:
            return head
        return f"{head} {_number_to_word(rest)}"
    return str(n)


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
    src_dir = root / "src"
    figures_dir = root / "output" / "figures"

    total_tests = _count_collected_tests(root)
    total_files = _count_test_files(tests_dir)
    daif_modules = _count_daif_modules(daif_dir)
    daif_symbols = _count_daif_symbols(daif_dir)
    daif_tests = _count_daif_tests(tests_dir)
    daif_test_files = _count_daif_test_files(tests_dir)
    subpackages = _count_domain_subpackages(src_dir)
    # Figure PNG count — counted directly from output/figures/ so the abstract
    # and any other section that cites a figure total stays in lock-step with
    # generate_diagrams.py.
    total_figures = len(list(figures_dir.glob("*.png"))) if figures_dir.exists() else 0

    discopy_v = _optional_distribution_version("discopy")
    numpy_v = _optional_distribution_version("numpy")

    metrics: dict[str, str] = {
        # Numeric strings
        "total_test_count": str(total_tests),
        "total_test_files": str(total_files),
        "daif_modules": str(daif_modules),
        "daif_symbols": str(daif_symbols),
        "daif_tests": str(daif_tests),
        "daif_test_files": str(daif_test_files),
        "domain_subpackages": str(subpackages),
        "total_figures": str(total_figures),
        # English-word variants for prose
        "daif_modules_word": _number_to_word(daif_modules),
        "total_test_files_word": _number_to_word(total_files),
        # Dependency versions (validated from the active environment)
        "discopy_version": discopy_v,
        "numpy_version": numpy_v,
        "discopy_version_pretty": discopy_v if discopy_v else "not resolved (install ``discopy``)",
        "numpy_version_pretty": numpy_v if numpy_v else "not resolved",
    }

    cov = _read_coverage_totals(root)
    if cov:
        metrics.update(cov)
    else:
        metrics["coverage_summary"] = (
            "coverage metrics not on disk—run "
            "``uv run pytest tests/ --cov=src --cov-report=json`` to write ``coverage.json``"
        )
        metrics["coverage_percent"] = ""

    return metrics


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
