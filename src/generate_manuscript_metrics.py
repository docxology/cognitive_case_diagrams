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
import os
import subprocess
import sys
from functools import lru_cache
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


@lru_cache(maxsize=8)
def _count_collected_tests_cached(project_root_str: str) -> int:
    """Memoised backing store for :func:`_count_collected_tests`.

    Collection spawns a full nested pytest run (minutes on this suite). The
    count cannot change within a single process, so callers that build metrics
    repeatedly — the test module does so four times — pay for it once.
    """
    return _count_collected_tests_uncached(Path(project_root_str))


def _count_collected_tests(project_root: Path) -> int:
    """Run ``pytest --collect-only -q`` and count collected test items."""
    return _count_collected_tests_cached(str(project_root))


def _count_collected_tests_uncached(project_root: Path) -> int:
    """Run ``pytest --collect-only -q`` and count collected test items.

    Raises rather than guessing. A regex scan of ``def test_`` cannot see
    parametrization and undercounts this suite by 8, so a silent fallback would
    publish a wrong number into the manuscript abstract with no error. If pytest
    is not importable in this interpreter, that is a broken environment and the
    metrics run must fail loudly.
    """
    # Collection imports matplotlib and discopy across 64 modules; on slower or
    # network/external storage this takes minutes, so the ceiling is generous and
    # overridable rather than a value that turns a slow disk into a wrong number.
    timeout_s = float(os.environ.get("CCD_COLLECT_TIMEOUT", "900"))
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(project_root / "tests"), "--collect-only", "-q"],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=timeout_s,
        )
    except (subprocess.SubprocessError, OSError) as exc:
        raise RuntimeError(
            f"pytest --collect-only could not be executed with {sys.executable}: {exc}"
        ) from exc

    # rc 0 = tests collected, rc 5 = no tests collected; anything else is a failure.
    if result.returncode not in (0, 5):
        raise RuntimeError(
            f"pytest --collect-only failed (rc={result.returncode}) with "
            f"{sys.executable}: {result.stderr.strip() or result.stdout.strip()}"
        )

    # Last meaningful line is like "727 tests collected in 0.32s"
    for line in reversed(result.stdout.strip().splitlines()):
        if "collected" in line:
            for part in line.split():
                if part.isdigit():
                    return int(part)

    raise RuntimeError(
        "pytest --collect-only produced no 'collected' line; cannot determine the "
        f"test count. stdout: {result.stdout.strip()[:400]!r}"
    )


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
    """Count collected test items in ``test_daif*.py`` files.

    Uses the same real ``pytest --collect-only`` collection as
    ``${total_test_count}`` (an AST ``def test_`` scan cannot see
    parametrization, so it undercounts; two different counters for the same
    quantity is how ``${daif_tests}`` drifted from ``${total_test_count}``).
    """
    daif_files = tuple(str(p) for p in sorted(tests_dir.glob("test_daif*.py")))
    if not daif_files:
        return 0
    return _count_collected_tests_in_paths(daif_files, cwd=str(_PROJECT_ROOT))


@lru_cache(maxsize=8)
def _count_collected_tests_in_paths_cached(paths_joined: str, cwd: str) -> int:
    """Memoised collector for an explicit list of test files."""
    return _count_collected_tests_in_paths_uncached(
        tuple(paths_joined.split("\x1f")), cwd,
    )


def _count_collected_tests_in_paths(paths: tuple[str, ...], cwd: str) -> int:
    """Collect the given test files and return the collected-item count."""
    return _count_collected_tests_in_paths_cached("\x1f".join(paths), cwd)


def _count_collected_tests_in_paths_uncached(paths: tuple[str, ...], cwd: str) -> int:
    """Run ``pytest --collect-only -q`` on ``paths`` and count collected items.

    Raises rather than guessing — same policy as
    :func:`_count_collected_tests_uncached`.
    """
    timeout_s = float(os.environ.get("CCD_COLLECT_TIMEOUT", "900"))
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", *paths, "--collect-only", "-q"],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=timeout_s,
        )
    except (subprocess.SubprocessError, OSError) as exc:
        raise RuntimeError(
            f"pytest --collect-only could not be executed with {sys.executable}: {exc}"
        ) from exc
    if result.returncode not in (0, 5):
        raise RuntimeError(
            f"pytest --collect-only failed (rc={result.returncode}) with "
            f"{sys.executable}: {result.stderr.strip() or result.stdout.strip()}"
        )
    # Summary line: "54 tests collected in 15.51s"
    for line in reversed(result.stdout.strip().splitlines()):
        if "collected" in line:
            for part in line.split():
                if part.isdigit():
                    return int(part)
    raise RuntimeError(
        "pytest --collect-only produced no 'collected' line; cannot determine "
        f"the test count for {len(paths)} file(s). stdout: {result.stdout.strip()[:400]!r}"
    )


def _count_daif_test_files(tests_dir: Path) -> int:
    """Count ``test_daif*.py`` files."""
    return len(list(tests_dir.glob("test_daif*.py")))


def _enriched_metrics() -> dict[str, str]:
    """Compute the §5b enriched-category quantities the manuscript quotes.

    These were typed into ``docs/manuscript/05b_magnitude_homology.md`` as
    literals (2.50 / 5.50 / "condition number ~ 9.5"). The first two matched the
    code to 2 dp; the third did not match any norm — ``numpy.linalg.cond`` on the
    standard Z is ~92, not 9.5. Emitting all three here makes the printed values
    whatever the code computes, so they cannot drift again.

    Returns an empty dict if the domain package cannot be imported, so a failure
    here degrades one section rather than aborting the whole metrics run.
    """
    try:
        import numpy as np

        from src.enriched_cat.enriched import standard_enriched_category

        cat = standard_enriched_category()
        z = np.asarray(cat.proximity_matrix, dtype=float)
        return {
            "enriched_magnitude": f"{cat.magnitude():.2f}",
            "enriched_magnitude_deficit": f"{cat.magnitude_deficit():.2f}",
            "enriched_object_count": str(len(cat.roles)),
            # 2-norm condition number, the numpy default.
            "enriched_z_condition": f"{np.linalg.cond(z):.0f}",
        }
    except Exception as exc:  # pragma: no cover - degraded-import path
        print(
            f"warning: enriched metrics unavailable ({exc}); "
            "${enriched_*} variables will not resolve",
            file=sys.stderr,
        )
        return {}


def _topos_metrics() -> dict[str, str]:
    """Compute the §6 signature sizes the manuscript quotes.

    The prose claimed "approximately 15 function symbols" for the standard
    8-case theory and 5 for the minimal one; the builder emits one relation per
    morphism, giving 8 and 3. The API calls them ``relation_symbols``.
    """
    try:
        from src.case_systems.case_category import (
            minimal_case_category,
            standard_case_category,
        )
        from src.topos_theory.topos import build_typological_theory

        std = build_typological_theory(standard_case_category())
        mini = build_typological_theory(minimal_case_category())
        return {
            "topos_standard_sorts": str(len(std.sorts)),
            "topos_standard_relations": str(len(std.relation_symbols)),
            "topos_minimal_sorts": str(len(mini.sorts)),
            "topos_minimal_relations": str(len(mini.relation_symbols)),
        }
    except Exception as exc:  # pragma: no cover - degraded-import path
        print(
            f"warning: topos metrics unavailable ({exc}); "
            "${topos_*} variables will not resolve",
            file=sys.stderr,
        )
        return {}


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
            f"{pct}% line-and-branch coverage on ``src/`` (measured; see "
            "``output/metrics.json`` and ``tests/AGENTS.md`` for provenance)"
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


def _read_publication_metadata(root: Path) -> dict[str, str]:
    """Parse DOI / version / repo URL from ``docs/manuscript/config.yaml``.

    Falls back to empty strings when the file or a key is missing — the
    manuscript's ``${paper_*}`` variables render the empty string rather than
    a stale hand-typed literal. Never raises: a missing key is a provenance
    gap the author fixes in config.yaml, not a metrics-run failure.
    """
    cfg_path = root / "docs" / "manuscript" / "config.yaml"
    out = {"version": "", "doi": "", "repo_url": ""}
    if not cfg_path.is_file():
        return out
    try:
        import yaml

        cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return out
    paper = cfg.get("paper") or {}
    publication = cfg.get("publication") or {}
    doi = str(publication.get("doi") or paper.get("doi") or "").strip()
    # Canonical short form: 10.5281/zenodo.19695260 (strip resolver prefix).
    if doi.startswith("https://doi.org/"):
        doi = doi[len("https://doi.org/"):]
    out["doi"] = doi
    out["version"] = str(paper.get("version") or "").strip()

    # Repo URL: pyproject [project.urls] is the authoritative source (it was
    # already corrected to the real remote during remediation).
    try:
        import tomllib

        pyproject = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
        out["repo_url"] = str(
            (pyproject.get("project", {}).get("urls", {}) or {}).get("Repository", "")
        ).strip()
    except (OSError, ValueError, TypeError):
        pass
    return out


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

    # Publication metadata: parsed from docs/manuscript/config.yaml so the
    # DOI/version/URL in prose resolve from the canonical source instead of
    # hand-maintained literals that can drift.
    pub = _read_publication_metadata(root)

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
        # Publication metadata (from config.yaml / pyproject; empty if unresolved)
        "paper_version": pub["version"],
        "paper_doi": pub["doi"],
        "paper_repo_url": pub["repo_url"],
    }

    cov = _read_coverage_totals(root)
    if cov:
        metrics.update(cov)
    else:
        # Fail loudly instead of injecting a build instruction where the
        # coverage number belongs in the published abstract.
        raise RuntimeError(
            "coverage.json not found in project root — the manuscript abstract "
            "quotes ${coverage_percent} / ${coverage_summary} and must not render "
            "a build instruction in its place. Generate it first with:\n"
            "  uv run pytest tests/ --cov=src --cov-report=json:coverage.json"
        )

    # Domain-computed quantities the manuscript quotes in §5b and §6.
    metrics.update(_enriched_metrics())
    metrics.update(_topos_metrics())

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
