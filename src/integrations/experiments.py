"""Canonical synthetic-experiment results access for the MCP surface.

The numerical lane owns ``src/experiments``; its ``write_results()`` emits the
canonical file ``output/experiments/results.json`` when the parent
orchestration runs the experiments stage. Absence of the file means "not yet
generated" and is reported as such — never synthesized. Schema drift raises
instead of guessing: ``schema_version`` must be ``"1.0"`` and
``provenance.config_sha256`` must be present, because the manuscript injection
binds to exactly those two checks.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

from .registry import MAX_EXPERIMENT_VARIABLES
from .artifacts import ArtifactIndex
from src.experiments.runner import validate_experiment_results

EXPERIMENTS_RELATIVE_PATH = "experiments/results.json"
EXPERIMENTS_RESOURCE_URI = "ccd://experiments/results"
SUPPORTED_SCHEMA_VERSION = "1.0"

_ALLOWED_UNITS = frozenset({"probability", "dimensionless", "nats", "count", "version"})
_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")


class ExperimentsNotGeneratedError(FileNotFoundError):
    """Raised when the canonical experiments results file does not exist yet."""


def experiments_path(artifact_root: Path) -> Path:
    """Return the canonical experiments results path under an artifact root."""
    return Path(artifact_root) / EXPERIMENTS_RELATIVE_PATH


def load_experiments(artifact_root: Path) -> dict:
    """Load and schema-check the canonical experiments results file."""
    path = experiments_path(artifact_root)
    if not path.is_file():
        raise ExperimentsNotGeneratedError(
            "synthetic experiment results not yet generated "
            "(written by the experiments stage)"
        )
    try:
        payload = json.loads(ArtifactIndex(artifact_root).read(EXPERIMENTS_RELATIVE_PATH)[0])
    except json.JSONDecodeError as exc:
        raise ValueError(f"experiment results file is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("experiment results file must contain a JSON object")
    version = payload.get("schema_version")
    if version != SUPPORTED_SCHEMA_VERSION:
        raise ValueError(
            f"unsupported experiment results schema_version {version!r}; "
            f"expected {SUPPORTED_SCHEMA_VERSION!r}"
        )
    provenance = payload.get("provenance")
    if (
        not isinstance(provenance, dict)
        or not isinstance(provenance.get("config_sha256"), str)
        or not provenance["config_sha256"]
    ):
        raise ValueError(
            "experiment results provenance.config_sha256 is required "
            "(manuscript injection binds to it)"
        )
    verdict = validate_experiment_results(payload, artifact_root.parent)
    if not verdict["valid"]:
        raise ValueError("Invalid experiment evidence: " + "; ".join(verdict["errors"]))
    return payload


def _finite_number(value: object, identifier: str, field: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"experiment variable {identifier!r}: {field} must be a number or null")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"experiment variable {identifier!r}: {field} must be finite")
    return number


def summarize_variables(
    artifact_root: Path,
    limit: int = MAX_EXPERIMENT_VARIABLES,
) -> dict:
    """Project the stable ``variables`` registry into a bounded summary."""
    payload = load_experiments(artifact_root)
    variables = payload.get("variables")
    if not isinstance(variables, dict):
        raise ValueError("experiment results variables must be an object")
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= MAX_EXPERIMENT_VARIABLES:
        raise ValueError(f"limit must be a positive integer, got {limit!r}")

    provenance = payload["provenance"]
    identifiers = sorted(variables)
    truncated = len(identifiers) > limit
    projected = []
    for identifier in identifiers[:limit]:
        if not _IDENTIFIER.match(identifier):
            raise ValueError(f"invalid experiment variable identifier {identifier!r}")
        spec = variables[identifier]
        if not isinstance(spec, dict):
            raise ValueError(f"experiment variable {identifier!r} must be an object")
        if spec.get("value") is None or isinstance(spec.get("value"), bool):
            raise ValueError(f"experiment variable {identifier!r}: value must be a finite number")
        value = _finite_number(spec.get("value"), identifier, "value")
        if value is None:
            raise ValueError(f"experiment variable {identifier!r}: value must be a finite number")
        unit = spec.get("unit")
        if unit not in _ALLOWED_UNITS:
            raise ValueError(
                f"experiment variable {identifier!r}: unit {unit!r} not in "
                f"{sorted(_ALLOWED_UNITS)}"
            )
        sample_unit = spec.get("sample_unit")
        interpretation = spec.get("interpretation")
        if not isinstance(sample_unit, str) or not sample_unit:
            raise ValueError(f"experiment variable {identifier!r}: sample_unit is required")
        if not isinstance(interpretation, str) or not interpretation:
            raise ValueError(f"experiment variable {identifier!r}: interpretation is required")
        projected.append(
            {
                "identifier": identifier,
                "value": value,
                "unit": unit,
                "ci_low": _finite_number(spec.get("ci_low"), identifier, "ci_low"),
                "ci_high": _finite_number(spec.get("ci_high"), identifier, "ci_high"),
                "confidence_level": spec["confidence_level"],
                "sample_unit": sample_unit,
                "interpretation": interpretation,
            }
        )
    return {
        "schema_version": payload["schema_version"],
        "config_sha256": provenance["config_sha256"],
        "seed": provenance.get("seed"),
        "numpy_version": provenance.get("numpy_version"),
        "variable_count": len(variables),
        "truncated": truncated,
        "variables": projected,
    }
