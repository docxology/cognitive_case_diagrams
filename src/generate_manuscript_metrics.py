"""Manuscript metrics generator for cognitive_case_diagrams.

Collects every quantity the numbered manuscript quotes and validates the
result against the typed registry in :mod:`src.manuscript_variables` before
returning it. Collection is fail-closed: a missing quality receipt, missing
experiments output, an unregistered identifier, or a nonfinite value aborts
the run instead of rendering a placeholder or a stale claim.

Public API:
    collect_metrics  -- gather, validate, and return all manuscript variables
    write_metrics    -- serialise the flat mapping to JSON

Usage (standalone):
    python -m src.generate_manuscript_metrics          # writes output/metrics.json
    python -m src.generate_manuscript_metrics --dry-run # prints to stdout

Provenance classes (see the registry): ``quality_receipt`` values come from
``src.release_validation.validate_quality_receipt`` (never from a bare
``coverage.json``); ``experiments`` values come from the schema-1.0 runner
output at ``output/experiments/results.json``; ``computed`` values
are direct calls into public ``src`` APIs on canonical synthetic inputs
declared here; ``collection``, ``environment``, and ``config`` values count
or read the declared sources.
"""

from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
from pathlib import Path
from functools import lru_cache
from dataclasses import dataclass
from importlib import metadata

import numpy as np

from src.manuscript_variables import (
    format_float,
    read_experiment_variables,
    validate_metrics,
)

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

    Early revisions typed these literals into
    ``docs/manuscript/05b_magnitude_homology.md`` by hand and one of them
    did not match any computed norm. Emitting every quoted quantity here
    makes the printed values whatever the code computes, so they cannot
    drift again. The raw entry values back the axiom-failure counterexample
    in §5 (direct entry versus two-step product).

    Raises if the domain computation fails; incomplete scientific metrics
    must not be silently published.
    """
    from src.case_systems.case_category import CaseRole
    from src.enriched_cat.enriched import standard_enriched_category

    cat = standard_enriched_category()
    z = np.asarray(cat.proximity_matrix, dtype=float)
    roles = list(cat.roles)
    nom, acc, dat = roles.index(CaseRole.NOM), roles.index(CaseRole.ACC), roles.index(CaseRole.DAT)
    direct = float(z[nom, dat])
    product = float(z[nom, acc]) * float(z[acc, dat])
    return {
        "enriched_magnitude": format_float(cat.magnitude()),
        "enriched_magnitude_deficit": format_float(cat.magnitude_deficit()),
        "enriched_object_count": str(len(cat.roles)),
        # 2-norm condition number, the numpy default.
        "enriched_z_condition": format_float(np.linalg.cond(z)),
        "enriched_nom_dat_raw": format_float(direct),
        "enriched_nom_acc_raw": format_float(float(z[nom, acc])),
        "enriched_acc_dat_raw": format_float(float(z[acc, dat])),
        "enriched_nom_acc_dat_product": format_float(product),
    }

def _topos_metrics() -> dict[str, str]:
    """Compute the §6 signature sizes the manuscript quotes.

    The prose claimed "approximately 15 function symbols" for the standard
    8-case theory and 5 for the minimal one; the builder emits one relation per
    morphism, giving 8 and 3. The API calls them ``relation_symbols``.
    """
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



# Canonical synthetic configuration for the §7c Bellman counterexample.
# Every number the manuscript quotes about this example is computed from
# this dataclass; changing the example means editing it here.
@dataclass(frozen=True)
class _BellmanExample:
    """Uniform-drift counterexample inputs (all dimensionless scores)."""

    transition_entry: float = 0.5
    reward_first: float = 1.0
    reward_second: float = 0.0
    gamma: float = 0.9


CANONICAL_BELLMAN_EXAMPLE = _BellmanExample()

# Canonical synthetic support endpoints for the §7c projection example.
_PROJECTION_SUPPORT_MIN = 0.0
_PROJECTION_SUPPORT_MAX = 10.0
_PROJECTION_LEVELS = 4


def _bellman_example_metrics() -> dict[str, str]:
    """Compute the §7c score-versus-return counterexample from real code.

    The legacy ``distributional_bellman_operator`` propagates beliefs; the
    true infinite-horizon return of the same finite Markov reward process
    solves ``(I - gamma T) v = R``. Publishing both numbers side by side
    requires no narrative — they simply disagree.
    """
    from src.case_systems.case_category import CaseRole
    from src.cognitive.belief import CaseDiagramBelief
    from src.daif.core import distributional_bellman_operator

    ex = CANONICAL_BELLMAN_EXAMPLE
    n = 2
    t = np.full((n, n), ex.transition_entry)
    r = np.array([ex.reward_first, ex.reward_second])
    belief = CaseDiagramBelief(
        roles=[CaseRole.NOM, CaseRole.ACC],
        probabilities=np.full(n, 1.0 / n),
        name="bellman_counterexample",
    )
    steps = distributional_bellman_operator(
        belief, t, r, gamma=ex.gamma, n_steps=2, n_quantiles=2,
    )
    score_mean = float(steps[0].mean)
    identity = np.eye(n)
    values = np.linalg.solve(identity - ex.gamma * t, r)
    true_return = float(belief.probabilities @ values)
    return {
        "daif_bellman_example_transition": format_float(ex.transition_entry),
        "daif_bellman_example_gamma": format_float(ex.gamma),
        "daif_bellman_example_reward_first": format_float(ex.reward_first),
        "daif_bellman_example_reward_second": format_float(ex.reward_second),
        "daif_bellman_example_score_mean": format_float(score_mean),
        "daif_bellman_example_true_return": format_float(true_return),
    }


def _projection_example_metrics() -> dict[str, str]:
    """Compute the §7c endpoint-mass projection example from real code.

    A two-state uniform-drift example with zero discount places all mass on
    the support endpoints; the stored four midpoint levels then read the
    endpoints back through the generalized inverse.
    """
    from src.case_systems.case_category import CaseRole
    from src.cognitive.belief import CaseDiagramBelief
    from src.daif.core import push_forward_return

    n = 2
    t = np.full((n, n), 0.5)
    r = np.array([_PROJECTION_SUPPORT_MIN, _PROJECTION_SUPPORT_MAX])
    belief = CaseDiagramBelief(
        roles=[CaseRole.NOM, CaseRole.ACC],
        probabilities=np.full(n, 0.5),
        name="projection_example",
    )
    law = push_forward_return(
        belief, t, r, gamma=0.0, n_quantiles=_PROJECTION_LEVELS,
    )
    levels = ", ".join(format_float(v) for v in law.quantile_levels)
    values = ", ".join(format_float(v) for v in law.quantiles)
    return {
        "daif_projection_levels": levels,
        "daif_projection_values": values,
        "daif_projection_support_min": format_float(_PROJECTION_SUPPORT_MIN),
        "daif_projection_support_max": format_float(_PROJECTION_SUPPORT_MAX),
    }


def _quantum_example_metrics() -> dict[str, str]:
    """Compute the §8b Born-rule probabilities shown by the canonical figure."""
    from src.quantum.figure_data import make_quantum_povm_example
    from src.quantum.quantum_case import case_probability

    example = make_quantum_povm_example()
    probabilities = [case_probability(example["povm"].elements[role], example["state"]) for role in example["roles"]]
    by_role = {
        role.name: format_float(float(p))
        for role, p in zip(example["roles"], probabilities)
    }
    return {
        "quantum_nom_probability": by_role["NOM"],
        "quantum_acc_probability": by_role["ACC"],
        "quantum_dat_probability": by_role["DAT"],
    }


def _figure_parameter_metrics() -> dict[str, str]:
    """Compute figure-parameter counts quoted in captions and prose.

    These are the canonical inputs the generators actually consume, so a
    generator change that alters a figure also changes its caption.
    """
    from src.case_systems.case_category import (
        CaseRole,
        introductory_case_category,
    )
    from src.cognitive.figure_data import (
        make_daif_belief_trajectory_data,
        make_free_energy_convergence_data,
    )
    from src.visualization.syntactic_sentence_diagrams import PANELS

    standard = [
        CaseRole.NOM, CaseRole.ACC, CaseRole.GEN, CaseRole.DAT,
        CaseRole.INS, CaseRole.LOC, CaseRole.ABL, CaseRole.VOC,
    ]
    extra = [role for role in CaseRole if role not in standard]
    trajectory = make_daif_belief_trajectory_data()
    fe_data = make_free_energy_convergence_data()
    per_vector_iterations = len(fe_data["all_fe"]) // len(fe_data["word_boundaries"])
    standard_names = ", ".join(
        [role.name for role in standard[:-1]] + [standard[-1].name]
    )
    extra_names = ", ".join(
        [role.name for role in extra[:-1]] + [f"and {extra[-1].name}"]
    )
    panel_count = len(PANELS)
    return {
        "standard_inventory_names": standard_names,
        "standard_inventory_count": str(len(standard)),
        "standard_inventory_count_word": _number_to_word(len(standard)),
        "alignment_extra_label_names": extra_names,
        "alignment_extra_label_count": str(len(extra)),
        "introductory_figure_role_count": str(len(introductory_case_category().objects)),
        "syntactic_panel_sketch_count": str(panel_count),
        "syntactic_panel_sketch_count_word": _number_to_word(panel_count),
        "daif_trajectory_evidence_count": str(len(trajectory["word_labels"])),
        "daif_assignment_iterations": str(per_vector_iterations),
    }


def _complexity_weight_metrics() -> dict[str, str]:
    from inspect import signature
    from src.diagrams.complexity_metrics import syntactic_complexity_score
    parameters = signature(syntactic_complexity_score).parameters
    return {f"complexity_weight_{kind}": format_float(float(parameters[f"w_{kind}"].default))
            for kind in ("words", "cups", "caps", "depth")}


def _receipt_metrics(project_root: Path) -> dict[str, str]:
    """Read the source-bound quality receipt (never a bare coverage.json)."""
    from src.release_validation import validate_quality_receipt

    receipt = validate_quality_receipt(project_root)
    percent = float(receipt["coverage_percent"])
    return {
        "total_tests_passed": str(int(receipt["pytest_passed"])),
        "total_tests_failed": str(int(receipt["pytest_failed"])),
        "total_tests_skipped": str(int(receipt["pytest_skipped"])),
        "coverage_percent": f"{percent:.2f}",
        "coverage_lines_covered": str(int(receipt["coverage_lines_covered"])),
        "coverage_lines_total": str(int(receipt["coverage_lines_total"])),
        "quality_fingerprint_short": str(receipt["quality_input_fingerprint"])[:12],
        "quality_receipt_generated_at": str(receipt["generated_at"]),
    }


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
    """Parse publication metadata from ``docs/manuscript/config.yaml``.

    Covers the concept DOI, reserved (unpublished) version DOI and record
    URL, the historical prior-version DOI, working version and date, and
    the declared publication status. DOI strings are canonicalised to the
    short ``10.x/yyyy`` form. Falls back to empty strings when a key is
    genuinely optional; ``required`` registry entries fail validation when
    a mandatory key is missing. Repo URL comes from pyproject
    ``[project.urls]``.
    """
    cfg_path = root / "docs" / "manuscript" / "config.yaml"
    out = {
        "version": "", "date": "", "doi": "", "version_doi": "",
        "version_record": "", "prior_version_doi": "", "status": "",
        "repo_url": "",
    }
    if not cfg_path.is_file():
        return out
    try:
        import yaml

        cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return out
    paper = cfg.get("paper") or {}
    publication = cfg.get("publication") or {}

    def _short_doi(value: object) -> str:
        doi = str(value or "").strip()
        prefix = "https://doi.org/"
        return doi[len(prefix):] if doi.startswith(prefix) else doi

    out["doi"] = _short_doi(publication.get("doi") or paper.get("doi"))
    out["version_doi"] = _short_doi(publication.get("version_doi"))
    out["version_record"] = str(publication.get("version_record") or "").strip()
    out["prior_version_doi"] = _short_doi(publication.get("prior_version_doi"))
    out["version"] = str(paper.get("version") or "").strip()
    out["date"] = str(paper.get("date") or "").strip()

    out["status"] = str(publication.get("status") or "").strip()

    try:
        try:
            import tomllib
        except ImportError:  # Python 3.10
            import tomli as tomllib  # type: ignore[no-redef]

        pyproject = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
        out["repo_url"] = str(
            (pyproject.get("project", {}).get("urls", {}) or {}).get("Repository", "")
        ).strip()
    except (OSError, ValueError, TypeError):
        pass
    # Validation seam: malformed DOI/record values must fail collection so
    # they can never reach hydrated manuscript prose (CH18/AC1). Empty
    # optional values pass; role collisions (concept/version/prior) also
    # fail here.
    from src.release_metadata import validate_publication_identifiers

    validate_publication_identifiers(out)
    return out


def collect_metrics(
    project_root: Path | None = None,
) -> dict[str, str]:
    """Collect all manuscript variables and validate against the registry.

    Returns:
        Flat dict of variable name → string value. Every key is a
        registered ``VariableSpec``; every required spec has a finite,
        input so a partial run can never hydrate the manuscript.
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
        # Collection counters (collection is not a passing receipt)
        "total_test_count": str(total_tests),
        "total_test_files": str(total_files),
        "daif_modules": str(daif_modules),
        "daif_symbols": str(daif_symbols),
        "daif_tests": str(daif_tests),
        "daif_test_files": str(daif_test_files),
        "domain_subpackages": str(subpackages),
        "total_figures": str(total_figures),
        "daif_modules_word": _number_to_word(daif_modules),
        "total_test_files_word": _number_to_word(total_files),
        # Dependency versions (validated from the active environment)
        "discopy_version": discopy_v,
        "numpy_version": numpy_v,
        "discopy_version_pretty": discopy_v if discopy_v else "not resolved (install ``discopy``)",
        "numpy_version_pretty": numpy_v if numpy_v else "not resolved",
    }

    # Publication metadata (config.yaml / pyproject).
    pub = _read_publication_metadata(root)
    metrics.update({
        "paper_version": pub["version"],
        "paper_date": pub["date"],
        "paper_doi": pub["doi"],
        "paper_version_doi": pub["version_doi"],
        "paper_version_record_url": pub["version_record"],
        "paper_prior_version_doi": pub["prior_version_doi"],
        "publication_status": pub["status"],
    })

    # Source-bound quality receipt: coverage and passing-test claims bind to
    # a fingerprinted receipt, never to a bare coverage.json.
    metrics.update(_receipt_metrics(root))

    # Synthetic experiments (schema 1.0, seeded, ccd-methods lane).
    metrics.update(read_experiment_variables(root))
    from src.experiments.stats import normal_z
    experiment_config = json.loads((root / "output/experiments/results.json").read_text())["provenance"]["experiments_config"]
    confidence = float(experiment_config["confidence_level"])
    metrics["ci_level_percent"] = format_float(100 * confidence)
    metrics["ci_z_score"] = format_float(normal_z(confidence))
    metrics.update({
        "experiment_seed": str(experiment_config["seed"]),
        "experiment_replicates": str(experiment_config["n_replicates"]),
        "experiment_filter_roles": str(experiment_config["filtering"]["n_roles"]),
        "experiment_filter_iterations": str(experiment_config["filtering"]["n_iterations"]),
        "experiment_calibration_levels": str(experiment_config["calibration"]["n_levels"]),
        "experiment_calibration_observations": str(experiment_config["calibration"]["n_observations"]),
        "experiment_config_sha256": json.loads((root / "output/experiments/results.json").read_text())["provenance"]["config_sha256"],
    })

    # Domain-computed quantities quoted in §5, §5b, §6, §7c, §8b, and
    # figure captions.
    metrics.update(_enriched_metrics())
    metrics.update(_topos_metrics())
    metrics.update(_bellman_example_metrics())
    metrics.update(_projection_example_metrics())
    metrics.update(_quantum_example_metrics())
    metrics.update(_figure_parameter_metrics())
    metrics.update(_complexity_weight_metrics())

    # Fail closed before any prose can render: unregistered identifiers,
    # missing required values, and format violations abort here.
    validate_metrics(metrics)
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
    parser.add_argument("--project-root", type=Path, default=_PROJECT_ROOT, help="Project whose evidence is collected")
    args = parser.parse_args()

    metrics = collect_metrics(args.project_root)

    if args.dry_run:
        print(json.dumps(metrics, indent=2))
    else:
        dest = write_metrics(metrics, args.output or args.project_root / "output/metrics.json")
        print(f"Wrote {len(metrics)} metrics to {dest}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
