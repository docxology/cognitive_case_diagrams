"""Typed registry for manuscript ``${variable}`` injection.

Every quantitative claim in the numbered manuscript sources must be injected
from this registry. The registry is the single authority for

- which identifiers exist (``VariableSpec`` entries with unit, display
  format, provenance class, and a human-readable description of what the
  number measures),
- which provenance class produced a value and where it is checked
  (quality receipt, experiments runner output, direct computation from
  public ``src`` APIs, or manuscript ``config.yaml``),
- which values are structurally required before injection may run.

Fail-closed contract (enforced with :mod:`src.project_validation` and the
injection path):

- an ``${identifier}`` token that is not registered fails injection,
- a registered required variable without a finite, format-conformant value
  fails collection,
- a nonfinite numeric value, an unknown unit, or a boolean-valued
  experiment metric fails collection,
- experiments results are accepted only from ``schema_version == "1.0"``
  payloads whose declared provenance is well formed.

Scope boundary — tokens are *not* used for structural mathematical
constants (equation coefficients with a stated scope sentence), section
labels, citation keys, or enumerated qualitative labels that do not vary.
Declared example *inputs* (canonical synthetic configurations) live as
typed constants in :mod:`src.generate_manuscript_metrics`, not in prose.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path

__all__ = [
    "EXPERIMENT_RESULTS_RELATIVE",
    "TOKEN_RE",
    "FORMATS",
    "PROVENANCE_CLASSES",
    "UNITS",
    "EXPERIMENT_UNITS",
    "VariableSpec",
    "EXPERIMENT_VARIABLE_NAMES",
    "variable_specs",
    "spec_by_name",
    "validate_token_name",
    "validate_value_for_spec",
    "validate_metrics",
    "format_float",
    "read_experiment_variables",
    "scan_hard_coded_claims",
]

# Identical to the injection pattern: substitution and registry validation
# must agree on what an identifier is.
TOKEN_RE = re.compile(r"\$\{([_a-zA-Z][_a-zA-Z0-9]*)\}")

# Display formats a collected string value must satisfy.
FORMATS = {
    "integer",      # unsigned decimal integer, e.g. "49"
    "decimal2",     # exactly two fractional digits, e.g. "91.23"
    "sig6",         # %g-style, up to six significant digits, e.g. "1.2e-12"
    "word",         # English number word, e.g. "forty-nine"
    "string",       # any nonempty provenance text (version, name list, ISO date)
}

# Provenance classes; each names where a value is checked.
PROVENANCE_CLASSES = {
    "quality_receipt",  # src.release_validation.validate_quality_receipt fields
    "experiments",      # src.experiments run output (schema 1.0, seeded, synthetic)
    "computed",         # direct call into public src.* APIs on canonical inputs
    "config",           # docs/manuscript/config.yaml or pyproject metadata
    "collection",       # pytest --collect-only / structural file counts
    "environment",      # installed distribution versions of the active env
}

# Registry-wide units for non-experiment variables.
UNITS = {
    "count",          # dimensionless integer count
    "dimensionless",  # unitless real number
    "probability",    # real number in [0, 1]
    "percent",        # percentage of a measured whole
    "identifier",     # canonical name or list of canonical names
    "version",        # software/revision version string
    "date",           # ISO-8601 date
    "timestamp",      # ISO-8601 datetime with offset
    "text",           # provenance text (hash, command line)
}

# Units the experiments contract (ccd-methods lane) may declare.
EXPERIMENT_UNITS = {"probability", "dimensionless", "nats", "count", "version"}

# Experiments runner output; written by parent orchestration through
# src.experiments write_results (ccd-methods lane, schema_version "1.0").
EXPERIMENT_RESULTS_RELATIVE = Path("output/experiments/results.json")


@dataclass(frozen=True)
class VariableSpec:
    """Declaration of one injectable manuscript variable."""

    name: str
    unit: str
    format: str
    provenance: str
    description: str
    source: str
    required: bool = True

    def __post_init__(self) -> None:
        validate_token_name(self.name)
        if self.format not in FORMATS:
            raise ValueError(f"{self.name}: unknown format {self.format!r}")
        if self.provenance not in PROVENANCE_CLASSES:
            raise ValueError(f"{self.name}: unknown provenance {self.provenance!r}")
        allowed_units = EXPERIMENT_UNITS if self.provenance == "experiments" else UNITS
        if self.unit not in allowed_units:
            raise ValueError(f"{self.name}: unit {self.unit!r} invalid for provenance {self.provenance!r}")


def validate_token_name(name: str) -> None:
    """Reject names the injection pattern could not address."""
    if not isinstance(name, str) or not TOKEN_RE.fullmatch("${" + name + "}"):
        raise ValueError(f"Invalid variable identifier: {name!r}")


# ---------------------------------------------------------------------------
# Registry: quality-receipt, collection, environment, and config variables
# ---------------------------------------------------------------------------

_SPECS: tuple[VariableSpec, ...] = (
    # --- Source-bound quality receipt (parent lane, ccd-quality-v1) --------
    VariableSpec(
        name="total_tests_passed",
        unit="count", format="integer", provenance="quality_receipt",
        description="Tests that passed in the receipt-bound suite run",
        source="src.release_validation.validate_quality_receipt -> pytest_passed",
    ),
    VariableSpec(
        name="total_tests_failed",
        unit="count", format="integer", provenance="quality_receipt",
        description="Reported failures in the passing receipt (must be zero)",
        source="src.release_validation.validate_quality_receipt -> pytest_failed",
    ),
    VariableSpec(
        name="total_tests_skipped",
        unit="count", format="integer", provenance="quality_receipt",
        description="Reported skips in the receipt-bound suite run",
        source="src.release_validation.validate_quality_receipt -> pytest_skipped",
    ),
    VariableSpec(
        name="coverage_percent",
        unit="percent", format="decimal2", provenance="quality_receipt",
        description="Combined line-and-branch coverage recomputed from counts",
        source="src.release_validation.validate_quality_receipt -> coverage_percent",
    ),
    VariableSpec(
        name="coverage_lines_covered",
        unit="count", format="integer", provenance="quality_receipt",
        description="Covered statements bound to the receipt's coverage.json hash",
        source="src.release_validation.validate_quality_receipt -> coverage_lines_covered",
    ),
    VariableSpec(
        name="coverage_lines_total",
        unit="count", format="integer", provenance="quality_receipt",
        description="Measured statements bound to the receipt's coverage.json hash",
        source="src.release_validation.validate_quality_receipt -> coverage_lines_total",
    ),
    VariableSpec(
        name="quality_fingerprint_short",
        unit="text", format="string", provenance="quality_receipt",
        description="First 12 hex digits of the source/config/test input fingerprint",
        source="src.release_validation.validate_quality_receipt -> quality_input_fingerprint[:12]",
    ),
    VariableSpec(
        name="quality_receipt_generated_at",
        unit="timestamp", format="string", provenance="quality_receipt",
        description="UTC instant at which the receipt was recorded",
        source="src.release_validation.validate_quality_receipt -> generated_at",
    ),
    # --- Collection counters (collection count, NOT a passing receipt) -----
    VariableSpec(
        name="total_test_count",
        unit="count", format="integer", provenance="collection",
        description="Tests collected by pytest --collect-only (no pass claim)",
        source="src.generate_manuscript_metrics._count_collected_tests",
    ),
    VariableSpec(
        name="total_test_files",
        unit="count", format="integer", provenance="collection",
        description="Top-level test_*.py modules under tests/",
        source="src.generate_manuscript_metrics._count_test_files",
    ),
    VariableSpec(
        name="total_test_files_word",
        unit="count", format="word", provenance="collection",
        description="English word form of total_test_files",
        source="src.generate_manuscript_metrics._number_to_word",
    ),
    VariableSpec(
        name="domain_subpackages",
        unit="count", format="integer", provenance="collection",
        description="First-level packages under src/",
        source="src.generate_manuscript_metrics._count_domain_subpackages",
    ),
    VariableSpec(
        name="daif_modules",
        unit="count", format="integer", provenance="collection",
        description="Python modules in src/daif/ excluding __init__.py",
        source="src.generate_manuscript_metrics._count_daif_modules",
    ),
    VariableSpec(
        name="daif_modules_word",
        unit="count", format="word", provenance="collection",
        description="English word form of daif_modules",
        source="src.generate_manuscript_metrics._number_to_word",
    ),
    VariableSpec(
        name="daif_symbols",
        unit="count", format="integer", provenance="collection",
        description="Public symbols exported in src/daif/__init__.py __all__",
        source="src.generate_manuscript_metrics._count_daif_symbols",
    ),
    VariableSpec(
        name="daif_tests",
        unit="count", format="integer", provenance="collection",
        description="Tests collected in test_daif*.py files",
        source="src.generate_manuscript_metrics._count_daif_tests",
    ),
    VariableSpec(
        name="daif_test_files",
        unit="count", format="integer", provenance="collection",
        description="Number of test_daif*.py files",
        source="src.generate_manuscript_metrics._count_daif_test_files",
    ),
    VariableSpec(
        name="total_figures",
        unit="count", format="integer", provenance="collection",
        description="PNG figures in output/figures/, matching the figure registry",
        source="output/figures/*.png count",
    ),
    # --- Environment versions ----------------------------------------------
    VariableSpec(
        name="discopy_version",
        unit="version", format="string", provenance="environment",
        description="Installed DisCoPy distribution version (empty if absent)",
        source="importlib.metadata.version('discopy')",
        required=False,
    ),
    VariableSpec(
        name="numpy_version",
        unit="version", format="string", provenance="environment",
        description="Installed NumPy distribution version (empty if absent)",
        source="importlib.metadata.version('numpy')",
        required=False,
    ),
    VariableSpec(
        name="discopy_version_pretty",
        unit="version", format="string", provenance="environment",
        description="DisCoPy version safe for prose when the package is absent",
        source="src.generate_manuscript_metrics._optional_distribution_version",
    ),
    VariableSpec(
        name="numpy_version_pretty",
        unit="version", format="string", provenance="environment",
        description="NumPy version safe for prose when the package is absent",
        source="src.generate_manuscript_metrics._optional_distribution_version",
    ),
    # --- Manuscript configuration (docs/manuscript/config.yaml) ------------
    VariableSpec(
        name="paper_version",
        unit="version", format="string", provenance="config",
        description="Working paper version declared in config.yaml",
        source="config.yaml paper.version",
    ),
    VariableSpec(
        name="paper_date",
        unit="date", format="string", provenance="config",
        description="Working revision date declared in config.yaml",
        source="config.yaml paper.date",
    ),
    VariableSpec(
        name="paper_doi",
        unit="identifier", format="string", provenance="config",
        description="Concept DOI for the paper (reserved draft until publication)",
        source="config.yaml publication.doi",
        required=False,
    ),
    VariableSpec(
        name="paper_version_doi",
        unit="identifier", format="string", provenance="config",
        description="Reserved version DOI for this revision (not yet published)",
        source="config.yaml publication.version_doi",
        required=False,
    ),
    VariableSpec(
        name="paper_version_record_url",
        unit="identifier", format="string", provenance="config",
        description="Zenodo record URL of the reserved version draft",
        source="config.yaml publication.version_record",
        required=False,
    ),
    VariableSpec(
        name="paper_prior_version_doi",
        unit="identifier", format="string", provenance="config",
        description="Version DOI of the previously published record (history only)",
        source="config.yaml publication.prior_version_doi",
        required=False,
    ),
    VariableSpec(
        name="publication_status",
        unit="text", format="string", provenance="config",
        description="Declared publication status of this revision",
        source="config.yaml publication.status",
    ),
)

_SPECS = _SPECS + (
    # --- Computed from public src APIs on canonical synthetic inputs -------
    VariableSpec(
        name="enriched_magnitude",
        unit="dimensionless", format="sig6", provenance="computed",
        description="Inverse-sum magnitude of the raw illustrative similarity matrix",
        source="src.enriched_cat.enriched.standard_enriched_category().magnitude()",
    ),
    VariableSpec(
        name="enriched_magnitude_deficit",
        unit="dimensionless", format="sig6", provenance="computed",
        description="Object count minus magnitude for that matrix",
        source="src.enriched_cat.enriched.standard_enriched_category().magnitude_deficit()",
    ),
    VariableSpec(
        name="enriched_object_count",
        unit="count", format="integer", provenance="computed",
        description="Role count of the standard enriched example",
        source="len(standard_enriched_category().roles)",
    ),
    VariableSpec(
        name="enriched_z_condition",
        unit="dimensionless", format="sig6", provenance="computed",
        description="Two-norm condition number of the raw similarity matrix",
        source="numpy.linalg.cond on standard_enriched_category().proximity_matrix",
    ),
    VariableSpec(
        name="enriched_nom_dat_raw",
        unit="dimensionless", format="sig6", provenance="computed",
        description="Raw NOM-to-DAT similarity entry",
        source="standard_enriched_category().proximity_matrix[CaseRole.NOM, CaseRole.DAT]",
    ),
    VariableSpec(
        name="enriched_nom_acc_raw",
        unit="dimensionless", format="sig6", provenance="computed",
        description="Raw NOM-to-ACC similarity entry",
        source="standard_enriched_category().proximity_matrix[CaseRole.NOM, CaseRole.ACC]",
    ),
    VariableSpec(
        name="enriched_acc_dat_raw",
        unit="dimensionless", format="sig6", provenance="computed",
        description="Raw ACC-to-DAT similarity entry",
        source="standard_enriched_category().proximity_matrix[CaseRole.ACC, CaseRole.DAT]",
    ),
    VariableSpec(
        name="enriched_nom_acc_dat_product",
        unit="dimensionless", format="sig6", provenance="computed",
        description="Two-step product that exceeds the direct entry (axiom failure)",
        source="product of the two raw entries above",
    ),
    VariableSpec(
        name="topos_standard_sorts",
        unit="count", format="integer", provenance="computed",
        description="Sorts in the standard typological theory presentation",
        source="src.topos_theory.topos.build_typological_theory(standard_case_category())",
    ),
    VariableSpec(
        name="topos_standard_relations",
        unit="count", format="integer", provenance="computed",
        description="Relation symbols in the standard typological theory presentation",
        source="build_typological_theory(standard_case_category()).relation_symbols",
    ),
    VariableSpec(
        name="topos_minimal_sorts",
        unit="count", format="integer", provenance="computed",
        description="Sorts in the minimal typological theory presentation",
        source="build_typological_theory(minimal_case_category()).sorts",
    ),
    VariableSpec(
        name="topos_minimal_relations",
        unit="count", format="integer", provenance="computed",
        description="Relation symbols in the minimal typological theory presentation",
        source="build_typological_theory(minimal_case_category()).relation_symbols",
    ),
    VariableSpec(
        name="standard_inventory_names",
        unit="identifier", format="string", provenance="computed",
        description="Canonical standard case inventory as a prose name list",
        source="CaseRole members NOM..VOC (src/case_systems/case_category.py)",
    ),
    VariableSpec(
        name="standard_inventory_count",
        unit="count", format="integer", provenance="computed",
        description="Size of the standard case inventory",
        source="len(standard inventory CaseRole members)",
    ),
    VariableSpec(
        name="standard_inventory_count_word",
        unit="count", format="word", provenance="computed",
        description="English word form of standard_inventory_count",
        source="src.generate_manuscript_metrics._number_to_word",
    ),
    VariableSpec(
        name="alignment_extra_label_names",
        unit="identifier", format="string", provenance="computed",
        description="Alignment-only CaseRole members beyond the standard inventory",
        source="CaseRole members ERG, ABS, S, A, P",
    ),
    VariableSpec(
        name="alignment_extra_label_count",
        unit="count", format="integer", provenance="computed",
        description="Count of alignment-only CaseRole members",
        source="len(CaseRole) minus standard inventory size",
    ),
    VariableSpec(
        name="introductory_figure_role_count",
        unit="count", format="integer", provenance="computed",
        description="Roles drawn in the introduction figure (fig:case-minimal)",
        source="len(src.case_systems.case_category.introductory_case_category().roles)",
    ),
    VariableSpec(
        name="daif_bellman_example_reward_first",
        unit="dimensionless", format="sig6", provenance="computed",
        description="First reward entry of the Bellman counterexample input",
        source="CANONICAL_BELLMAN_EXAMPLE in src/generate_manuscript_metrics.py",
    ),
    VariableSpec(
        name="daif_bellman_example_reward_second",
        unit="dimensionless", format="sig6", provenance="computed",
        description="Second reward entry of the Bellman counterexample input",
        source="CANONICAL_BELLMAN_EXAMPLE in src/generate_manuscript_metrics.py",
    ),
    VariableSpec(
        name="syntactic_panel_sketch_count",
        unit="count", format="integer", provenance="computed",
        description="Hand-authored sketches in the appendix construction panel",
        source="len(src.visualization.syntactic_sentence_diagrams.PANELS)",
    ),
    VariableSpec(
        name="syntactic_panel_sketch_count_word",
        unit="count", format="word", provenance="computed",
        description="English word form of syntactic_panel_sketch_count",
        source="src.generate_manuscript_metrics._number_to_word",
    ),
    VariableSpec(
        name="quantum_nom_probability",
        unit="probability", format="sig6", provenance="computed",
        description="Born-rule probability of NOM for the canonical figure state",
        source="case_probability(crisp_case_povm, semantic_state) in src/quantum/figure_data.py",
    ),
    VariableSpec(
        name="quantum_acc_probability",
        unit="probability", format="sig6", provenance="computed",
        description="Born-rule probability of ACC for the canonical figure state",
        source="case_probability(crisp_case_povm, semantic_state) in src/quantum/figure_data.py",
    ),
    VariableSpec(
        name="quantum_dat_probability",
        unit="probability", format="sig6", provenance="computed",
        description="Born-rule probability of DAT for the canonical figure state",
        source="case_probability(crisp_case_povm, semantic_state) in src/quantum/figure_data.py",
    ),
    VariableSpec(
        name="daif_trajectory_evidence_count",
        unit="count", format="integer", provenance="computed",
        description="Likelihood vectors in the belief-trajectory figure data",
        source="len(obs_sequence) in src.cognitive.figure_data.make_daif_belief_trajectory_data",
    ),
    VariableSpec(
        name="daif_assignment_iterations",
        unit="count", format="integer", provenance="computed",
        description="Evidence-repetition iterations per vector in the FE figure data",
        source="n_iterations argument in src.cognitive.figure_data.make_free_energy_convergence_data",
    ),
    VariableSpec(
        name="daif_projection_levels",
        unit="dimensionless", format="string", provenance="computed",
        description="Midpoint quantile levels of the four-level projection example",
        source="quantile_levels of push_forward_return canonical endpoint example",
    ),
    VariableSpec(
        name="ci_level_percent",
        unit="percent", format="sig6", provenance="computed",
        description="Confidence level of the experiment interval convention",
        source="experiments.provenance.experiments_config.confidence_level",
    ),
    VariableSpec(
        name="ci_z_score",
        unit="dimensionless", format="sig6", provenance="computed",
        description="Normal quantile used by the interval convention",
        source="statistics.NormalDist inverse CDF at the configured confidence level",
    ),
    VariableSpec(
        name="daif_projection_values",
        unit="dimensionless", format="string", provenance="computed",
        description="Quantile values at those levels for mass at the endpoints",
        source="quantiles of push_forward_return canonical endpoint example",
    ),
    VariableSpec(
        name="daif_projection_support_min",
        unit="dimensionless", format="sig6", provenance="computed",
        description="Lower endpoint of the projection example support",
        source="canonical endpoint example configuration",
    ),
    VariableSpec(
        name="daif_projection_support_max",
        unit="dimensionless", format="sig6", provenance="computed",
        description="Upper endpoint of the projection example support",
        source="canonical endpoint example configuration",
    ),
    VariableSpec(
        name="daif_bellman_example_transition",
        unit="dimensionless", format="sig6", provenance="computed",
        description="Uniform transition entry of the Bellman counterexample input",
        source="CANONICAL_BELLMAN_EXAMPLE in src/generate_manuscript_metrics.py",
    ),
    VariableSpec(
        name="daif_bellman_example_gamma",
        unit="dimensionless", format="sig6", provenance="computed",
        description="Discount of the Bellman counterexample input",
        source="CANONICAL_BELLMAN_EXAMPLE in src/generate_manuscript_metrics.py",
    ),
    VariableSpec(
        name="daif_bellman_example_score_mean",
        unit="dimensionless", format="sig6", provenance="computed",
        description="Score mean the legacy operator reports for that input",
        source="distributional_bellman_operator(...)[0].mean",
    ),
    VariableSpec(
        name="daif_bellman_example_true_return",
        unit="dimensionless", format="sig6", provenance="computed",
        description="Belief-weighted infinite-horizon return (I-gamma T)^-1 R",
        source="numpy.linalg.solve on the canonical transition and reward",
    ),
)

# ---------------------------------------------------------------------------
# Registry: synthetic experiment results (ccd-methods lane, schema 1.0)
# ---------------------------------------------------------------------------

# Frozen identifier set announced by the numerical lane. New identifiers
# require a registry addition AND a manuscript use; unknown experiment
# identifiers fail collection so unregistered claims cannot render.
_SPECS += tuple(
    VariableSpec(name=f"complexity_weight_{kind}", unit="dimensionless", format="sig6", provenance="computed",
                 description=f"Default weight for {kind} in the synthetic complexity score",
                 source=f"signature(syntactic_complexity_score).parameters[w_{kind}].default")
    for kind in ("words", "cups", "caps", "depth")
)

_SPECS += tuple(
    VariableSpec(name=name, unit="count", format="integer", provenance="computed",
                 description=description, source="experiments.provenance.experiments_config")
    for name, description in (
        ("experiment_seed", "Master seed of the reported synthetic run"),
        ("experiment_replicates", "Independent seeded replicates per experiment"),
        ("experiment_filter_roles", "Roles in the synthetic filtering experiment"),
        ("experiment_filter_iterations", "Configured assimilations in the filtering arm"),
        ("experiment_calibration_levels", "Quantile levels evaluated per calibration law"),
        ("experiment_calibration_observations", "Independent outcomes per calibration law"),
    )
)
_SPECS += (VariableSpec(name="experiment_config_sha256", unit="text", format="string",
                       provenance="computed", description="SHA-256 of the canonical experiment configuration",
                       source="experiments.provenance.config_sha256"),)

from src.experiments.runner import experiment_variable_definitions

_EXPERIMENT_DEFINITIONS = experiment_variable_definitions()
EXPERIMENT_VARIABLE_NAMES = tuple(_EXPERIMENT_DEFINITIONS)
_EXPERIMENT_UNIT_HINTS = {name: definition["unit"] for name, definition in _EXPERIMENT_DEFINITIONS.items()}
_SPECS = _SPECS + tuple(
    VariableSpec(
        name=name, unit=definition["unit"], format="sig6", provenance="experiments",
        description=definition["description"],
        source="src.experiments.runner via output/experiments/results.json",
        required=False,
    )
    for name, definition in _EXPERIMENT_DEFINITIONS.items()
)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def variable_specs() -> dict[str, VariableSpec]:
    """Return the authoritative name -> spec mapping."""
    specs: dict[str, VariableSpec] = {}
    for spec in _SPECS:
        if spec.name in specs:
            raise ValueError(f"Duplicate registry name: {spec.name}")
        specs[spec.name] = spec
    return specs


def spec_by_name(name: str) -> VariableSpec | None:
    """Return the declared spec for ``name`` or None when unregistered."""
    return variable_specs().get(name)


def validate_value_for_spec(spec: VariableSpec, value: str) -> None:
    """Raise when a collected string violates the declared format."""
    if not isinstance(value, str) or not value:
        raise ValueError(f"{spec.name}: value must be a nonempty string, got {value!r}")
    if spec.format == "integer":
        if not re.fullmatch(r"(0|[1-9][0-9]*)", value):
            raise ValueError(f"{spec.name}: {value!r} is not a plain integer")
    elif spec.format == "decimal2":
        try:
            parsed = float(value)
        except ValueError as exc:
            raise ValueError(f"{spec.name}: {value!r} is not numeric") from exc
        if not math.isfinite(parsed) or not re.fullmatch(r"-?\d+\.\d{2}", value):
            raise ValueError(f"{spec.name}: {value!r} is not finite with two decimals")
    elif spec.format == "sig6":
        try:
            parsed = float(value)
        except ValueError as exc:
            raise ValueError(f"{spec.name}: {value!r} is not numeric") from exc
        if not math.isfinite(parsed):
            raise ValueError(f"{spec.name}: {value!r} is not finite")
    elif spec.format == "word":
        if not re.fullmatch(r"[a-z]+(-[a-z]+)*( [a-z]+)*", value):
            raise ValueError(f"{spec.name}: {value!r} is not an English number word")


def format_float(value: float) -> str:
    """Format a finite float with up to six significant digits."""
    if not math.isfinite(value):
        raise ValueError(f"Nonfinite value cannot be injected: {value!r}")
    return f"{value:.6g}"


def validate_metrics(metrics: dict[str, str]) -> dict[str, VariableSpec]:
    """Validate a flat collected mapping against the registry.

    Fails closed on unregistered keys, missing required specs, empty or
    malformed values, and nonfinite numeric content. Returns the spec map
    so callers can reuse the lookup.
    """
    specs = variable_specs()
    unknown = sorted(set(metrics) - set(specs))
    if unknown:
        raise ValueError(f"Unregistered manuscript variables: {unknown}")
    missing = sorted(
        name for name, spec in specs.items() if spec.required and name not in metrics
    )
    if missing:
        raise ValueError(
            "Required manuscript variables missing from collection: "
            f"{missing}. Generate the missing provenance inputs first."
        )
    for name, value in metrics.items():
        validate_value_for_spec(specs[name], value)
    return specs


def read_experiment_variables(root: Path) -> dict[str, str]:
    """Load, validate, and flatten ``variables`` from the runner output.

    The payload contract (ccd-methods lane, schema 1.0) is strict:
    ``schema_version == "1.0"``, provenance with hex ``config_sha256``, int
    ``seed``, string ``numpy_version``, and a flat ``variables`` mapping of
    identifier -> {value: finite number, unit, ci_low, ci_high, confidence_level,
    sample_unit, interpretation}. Boolean-valued or nonfinite entries are
    rejected; identifiers outside the registry are rejected.
    """
    path = root / EXPERIMENT_RESULTS_RELATIVE
    if not path.is_file():
        raise FileNotFoundError(
            f"Experiments results missing: {path}. The synthetic-statistics "
            "section quotes exp_* variables; produce the runner output before "
            "collecting manuscript metrics."
        )
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Experiments results are not valid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError("Experiments results must be a JSON object")
    if payload.get("schema_version") != "1.0":
        raise ValueError(
            f"Unsupported experiments schema_version: {payload.get('schema_version')!r}"
        )
    from src.experiments.runner import validate_experiment_results
    verdict = validate_experiment_results(payload, root)
    if not verdict["valid"]:
        raise ValueError("Invalid experiment evidence: " + "; ".join(verdict["errors"]))
    provenance = payload.get("provenance")
    if not isinstance(provenance, dict):
        raise ValueError("Experiments results lack a provenance object")
    config_sha = provenance.get("config_sha256")
    if (
        not isinstance(config_sha, str)
        or len(config_sha) != 64
        or not re.fullmatch(r"[0-9a-f]{64}", config_sha)
    ):
        raise ValueError("Experiments provenance.config_sha256 must be a hex sha256 string")
    if not isinstance(provenance.get("seed"), int) or isinstance(provenance.get("seed"), bool):
        raise ValueError("Experiments provenance.seed must be an integer")
    if not isinstance(provenance.get("numpy_version"), str):
        raise ValueError("Experiments provenance.numpy_version must be a string")
    variables = payload.get("variables")
    if not isinstance(variables, dict) or not variables:
        raise ValueError("Experiments results lack a nonempty variables object")

    specs = variable_specs()
    collected: dict[str, str] = {}
    for name, entry in variables.items():
        if name not in specs:
            raise ValueError(
                f"Unregistered experiment identifier {name!r}; add it to "
                "src/manuscript_variables.py before quoting it in prose"
            )
        if not isinstance(entry, dict):
            raise ValueError(f"Experiment variable {name} must be an object")
        value = entry.get("value")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"Experiment variable {name} must carry a numeric value")
        if not math.isfinite(float(value)):
            raise ValueError(f"Experiment variable {name} is nonfinite")
        unit = entry.get("unit")
        if unit != specs[name].unit:
            raise ValueError(
                f"Experiment variable {name} declares unit {unit!r}; registry "
                f"expects {specs[name].unit!r}"
            )
        for bound in ("ci_low", "ci_high"):
            bound_value = entry.get(bound)
            if bound_value is not None and (
                isinstance(bound_value, bool)
                or not isinstance(bound_value, (int, float))
                or not math.isfinite(float(bound_value))
            ):
                raise ValueError(f"Experiment variable {name} has a nonfinite {bound}")
        for field in ("sample_unit", "interpretation"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                raise ValueError(f"Experiment variable {name} lacks a {field} string")
        collected[name] = format_float(float(value))
    return collected


VARIABLES_MANIFEST_RELATIVE = Path("output/manuscript_variables.json")


def build_variables_manifest(root: Path, metrics: dict[str, str]) -> dict:
    """Bind every rendered variable to its declaration and current evidence inputs."""
    from src.release_validation import file_sha256, validate_quality_receipt

    root = root.resolve(strict=True)
    specs = validate_metrics(metrics)
    receipt = validate_quality_receipt(root)
    read_experiment_variables(root)
    paths = [
        root / "output/reports/quality_receipt.json",
        root / EXPERIMENT_RESULTS_RELATIVE,
        root / "output/figures/figure_registry.json",
        root / "docs/figure_alt_text.json",
    ]
    paths.extend(p for p in (root / "docs/manuscript").iterdir() if p.is_file())
    return {
        "schema": "ccd-manuscript-variables-v1",
        "quality_input_fingerprint": receipt["quality_input_fingerprint"],
        "inputs": {p.relative_to(root).as_posix(): file_sha256(p) for p in sorted(paths)},
        "variables": {name: {"value": value, "spec": asdict(specs[name])} for name, value in sorted(metrics.items())},
    }


def write_variables_manifest(root: Path, metrics: dict[str, str]) -> Path:
    """Write the source-bound registry export only after successful collection."""
    from src.release_validation import write_json_atomic

    destination = root.resolve(strict=True) / VARIABLES_MANIFEST_RELATIVE
    write_json_atomic(destination, build_variables_manifest(root, metrics))
    return destination


def validate_variables_manifest(root: Path, metrics: dict[str, str]) -> dict:
    """Reject missing or stale variable declarations, values or evidence."""
    from src.release_validation import StaleEvidenceError

    actual = json.loads((root / VARIABLES_MANIFEST_RELATIVE).read_text())
    if actual != build_variables_manifest(root, metrics):
        raise StaleEvidenceError("Manuscript variable manifest is stale")
    return actual


# ---------------------------------------------------------------------------
# Negative control: unbacked quantitative claims
# ---------------------------------------------------------------------------

# Literals are flagged in two regimes. Outside mathematics every numeric
# literal must be injected. Inside mathematics the structural integers
# 0-2 and symbolic indices stay out of scope, but decimal literals and
# integers >= 3 are flagged: a supplied example input such as $p=0.8$ is
# a variable, not a constant. Allowlist entries are (literal pattern,
# context regex, justification) triples; the context regex must match a
# window around the literal, so an allowlisted weight cannot excuse the
# same literal in an unrelated sentence.
PROSE_NUMBER_ALLOWLIST: tuple[tuple[str, str, str], ...] = ()

_SPAN_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"```.*?```", re.S),          # fenced code
    re.compile(r"`[^`]+`"),                  # inline code
    re.compile(r"\[@[^\]]+\]"),              # citation keys
    re.compile(r"\{#[\w:.-]+\}"),            # heading/figure/equation labels
    re.compile(r"\]\([^)]+\)"),              # link targets
    re.compile(r"^\s*\d+[.)]\s+", re.M),     # ordered-list enumeration
)
# Image markdown keeps its caption: the alt text is scanned for unbacked
# quantities, only the target path is dropped. Captions are injection
# surface, not an exemption.
_IMAGE_CAPTION_RE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
_MATH_SPAN_RE = re.compile(r"\$\$.+?\$\$|\$[^$\n]+\$", re.S)
_LITERAL_RE = re.compile(r"\d+(?:\.\d+)?(?:[eE]-?\d+)?")
_WINDOW = 160


def _classify_literal(literal: str) -> str | None:
    """Return ``math`` or ``prose`` for a literal, or None to ignore.

    Inside mathematics, structural integers 0, 1, and 2 are constants of
    the stated definitions and unit/singular objects; decimals and larger
    counts are treated as claims. Outside mathematics every literal is a
    claim.
    """
    if "." in literal or "e" in literal.lower():
        return "math"
    if int(literal) >= 3:
        return "math"
    return None


def _is_allowlisted(literal: str, context: str) -> bool:
    """Match the literal against a justified allowlist entry in context."""
    for pattern, context_pattern, _ in PROSE_NUMBER_ALLOWLIST:
        if re.fullmatch(pattern, literal) and re.search(context_pattern, context):
            return True
    return False


def _strip_spans(text: str) -> str:
    """Remove non-prose spans, keeping mathematics and figure captions."""
    # Tokens first: otherwise an early ``$`` swallows the span between
    # ``${identifier}`` and the next math delimiter.
    text = TOKEN_RE.sub(" ", text)
    text = re.sub(r"\b(?:N400|P600|C51|PCG64)\b", "named_component", text)
    text = _IMAGE_CAPTION_RE.sub(lambda m: f" {m.group(1)} ", text)
    for pattern in _SPAN_PATTERNS:
        text = pattern.sub(" ", text)
    return text


def scan_hard_coded_claims(chapters: dict[str, str]) -> list[str]:
    """Return unbacked numeric literals in prose and mathematics.

    Mathematics is scanned, not exempted: decimals such as ``$p=0.8$`` and
    integers >= 3 inside ``$...$`` are flagged unless injected via
    ``${variable}`` (tokens are removed first, so injected values are
    invisible to this scan). Structural integers 0-2 and allowlisted
    entries with a documented justification pass. Figure captions and
    alt-text style content are scanned wherever callers include them.
    """
    findings: list[str] = []
    for name, text in sorted(chapters.items()):
        prose = _strip_spans(text)
        segments: list[tuple[str, bool]] = []
        cursor = 0
        for span in _MATH_SPAN_RE.finditer(prose):
            segments.append((prose[cursor:span.start()], False))
            segments.append((span.group(0), True))
            cursor = span.end()
        segments.append((prose[cursor:], False))
        for segment, in_math in segments:
            for match in _LITERAL_RE.finditer(segment):
                literal = match.group(0)
                verdict = "math" if in_math else "prose"
                if verdict == "math" and _classify_literal(literal) is None:
                    continue
                window = segment[max(0, match.start() - _WINDOW):
                                 match.end() + _WINDOW]
                if _is_allowlisted(literal, window):
                    continue
                findings.append(
                    f"{name}: unbacked numeric literal {literal!r} in {verdict}"
                )
    return findings
