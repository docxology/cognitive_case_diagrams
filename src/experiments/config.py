"""Typed, validated configuration for the synthetic experiments.

The configuration is the single source of randomness, sample-size, and
confidence-level decisions for ``run_experiments``. Every field is validated
eagerly: ``from_dict`` never returns a partially valid config, unknown or
misspelled keys are rejected so silent defaults cannot mask an intended
setting, and every numeric field carries a resource cap so a public caller
cannot request an unbounded run.

All canonical inputs are synthetic. No empirical dataset, human measurement,
or p-value enters through this module.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from typing import Any

__all__ = [
    "ConfigError",
    "ExperimentConfig",
    "DEFAULT_CONFIG",
    "canonical_config_json",
    "config_sha256",
    "load_config",
    "save_config",
]

# Resource caps: the public API is bounded; these bounds keep any admitted
# configuration inside a well-defined compute envelope.
_MAX_REPLICATES = 100_000
from src.case_systems.case_category import CaseRole

_MAX_ROLES = len(CaseRole)
_MAX_LEVELS = 200
_MAX_OBSERVATIONS = 1_000_000
_MAX_QUANTILES = 4096
_MAX_TARGETS = 4096
_MAX_TAU_POINTS = 2_000_001
_MAX_ATOMS = 100_001
_MAX_LIST_ENTRIES = 64
_MAX_BIN_ENTRIES = 64


class ConfigError(ValueError):
    """Raised when an experiment configuration is invalid."""


def _require_bool(section: str, key: str, value: Any) -> bool:
    if not isinstance(value, bool):
        raise ConfigError(f"{section}.{key} must be a boolean, got {value!r}")
    return value


def _require_int(section: str, key: str, value: Any, minimum: int,
                 maximum: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ConfigError(f"{section}.{key} must be an integer >= {minimum}, got {value!r}")
    if value < minimum:
        raise ConfigError(f"{section}.{key} must be >= {minimum}, got {value}")
    if maximum is not None and value > maximum:
        raise ConfigError(f"{section}.{key} must be <= {maximum}, got {value}")
    return int(value)


def _require_float(section: str, key: str, value: Any, low: float, high: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ConfigError(f"{section}.{key} must be a number in [{low}, {high}], got {value!r}")
    value = float(value)
    if not math_isfinite(value):
        raise ConfigError(f"{section}.{key} must be finite, got {value!r}")
    if not low <= value <= high:
        raise ConfigError(f"{section}.{key} must be in [{low}, {high}], got {value}")
    return value


def math_isfinite(value: float) -> bool:
    """Finite check without a numpy dependency in the config layer."""
    return value == value and value not in (float("inf"), float("-inf"))


def _require_choice(section: str, key: str, value: Any, allowed: tuple[Any, ...]) -> Any:
    if isinstance(value, bool) or value not in allowed:
        raise ConfigError(f"{section}.{key} must be one of {allowed}, got {value!r}")
    return value


def _require_int_list(section: str, key: str, value: Any, minimum: int,
                      maximum: int | None = None, unique: bool = True,
                      max_entries: int = _MAX_LIST_ENTRIES) -> list[int]:
    if not isinstance(value, list) or not value:
        raise ConfigError(f"{section}.{key} must be a non-empty list of integers, got {value!r}")
    if len(value) > max_entries:
        raise ConfigError(f"{section}.{key} must have at most {max_entries} entries")
    out: list[int] = []
    for item in value:
        if isinstance(item, bool) or not isinstance(item, int):
            raise ConfigError(f"{section}.{key} entries must be integers, got {item!r}")
        if item < minimum:
            raise ConfigError(f"{section}.{key} entries must be >= {minimum}, got {item}")
        if maximum is not None and item > maximum:
            raise ConfigError(f"{section}.{key} entries must be <= {maximum}, got {item}")
        out.append(int(item))
    if unique and len(set(out)) != len(out):
        raise ConfigError(f"{section}.{key} entries must be unique, got {value!r}")
    return out


def _require_float_list(section: str, key: str, value: Any, low: float, high: float,
                        unique: bool = True,
                        max_entries: int = _MAX_LIST_ENTRIES) -> list[float]:
    if not isinstance(value, list) or not value:
        raise ConfigError(f"{section}.{key} must be a non-empty list of numbers, got {value!r}")
    if len(value) > max_entries:
        raise ConfigError(f"{section}.{key} must have at most {max_entries} entries")
    out = [_require_float(section, f"{key}[{i}]", item, low, high) for i, item in enumerate(value)]
    if unique and len(set(out)) != len(out):
        raise ConfigError(f"{section}.{key} entries must be unique, got {value!r}")
    return out


def _reject_unknown(section: str, data: dict[str, Any], known: tuple[str, ...]) -> None:
    unknown = sorted(set(data) - set(known))
    if unknown:
        raise ConfigError(f"Unknown keys in {section}: {unknown}; known keys are {sorted(known)}")


@dataclass
class FilteringConfig:
    """Multi-replicate Bayesian filtering validation settings."""

    enabled: bool = True
    n_roles: int = 3
    evidence_strength: float = 0.8     # mixture weight on the true-role indicator
    n_iterations: int = 3              # repeated updates expose transition effects
    closed_form_iterations: int = 5    # length of the closed-form repeated-Bayes check

    def validate(self) -> None:
        _require_bool("filtering", "enabled", self.enabled)
        _require_int("filtering", "n_roles", self.n_roles, 2, _MAX_ROLES)
        _require_float("filtering", "evidence_strength", self.evidence_strength, 0.0, 1.0)
        _require_int("filtering", "n_iterations", self.n_iterations, 1, _MAX_QUANTILES)
        _require_int("filtering", "closed_form_iterations", self.closed_form_iterations,
                     1, _MAX_QUANTILES)


@dataclass
class CalibrationConfig:
    """Quantile-coverage calibration validation settings.

    The confidence level for every reported interval lives at the top level
    of :class:`ExperimentConfig` so a single declared value drives all
    intervals consistently.
    """

    enabled: bool = True
    n_levels: int = 19             # quantile levels per replicate model
    n_observations: int = 200      # synthetic outcomes per replicate

    def validate(self) -> None:
        _require_bool("calibration", "enabled", self.enabled)
        _require_int("calibration", "n_levels", self.n_levels, 2, _MAX_LEVELS)
        _require_int("calibration", "n_observations", self.n_observations,
                     1, _MAX_OBSERVATIONS)


@dataclass
class QuantileConfig:
    """Quantile-update and Wasserstein validation settings."""

    enabled: bool = True
    n_quantiles: int = 8
    n_targets: int = 6
    learning_rate: float = 0.1
    kappa: float = 0.5
    wasserstein_p: int = 1
    brute_force_tau_points: int = 20001

    def validate(self) -> None:
        _require_bool("quantile", "enabled", self.enabled)
        _require_int("quantile", "n_quantiles", self.n_quantiles, 2, _MAX_QUANTILES)
        _require_int("quantile", "n_targets", self.n_targets, 1, _MAX_TARGETS)
        _require_float("quantile", "learning_rate", self.learning_rate, 0.0, 1.0)
        if self.learning_rate <= 0.0:
            raise ConfigError("quantile.learning_rate must be strictly inside (0, 1]")
        _require_float("quantile", "kappa", self.kappa, 0.0, float("inf"))
        if self.kappa <= 0.0:
            raise ConfigError("quantile.kappa must be strictly positive")
        _require_choice("quantile", "wasserstein_p", self.wasserstein_p, (1, 2))
        _require_int("quantile", "brute_force_tau_points", self.brute_force_tau_points,
                     101, _MAX_TAU_POINTS)


@dataclass
class ProjectionConfig:
    """C51-style categorical projection validation settings."""

    enabled: bool = True
    atom_counts: list[int] = field(default_factory=lambda: [11, 51, 201])
    v_min: float = -1.0
    v_max: float = 1.0

    def validate(self) -> None:
        _require_bool("projection", "enabled", self.enabled)
        _require_int_list("projection", "atom_counts", self.atom_counts,
                          2, _MAX_ATOMS, max_entries=8)
        _require_float("projection", "v_min", self.v_min, float("-inf"), float("inf"))
        _require_float("projection", "v_max", self.v_max, float("-inf"), float("inf"))
        if self.v_min >= self.v_max:
            raise ConfigError("projection.v_min must be < projection.v_max")


@dataclass
class SensitivityConfig:
    """One-at-a-time parameter sweeps with common random numbers."""

    enabled: bool = True
    gammas: list[float] = field(default_factory=lambda: [0.0, 0.25, 0.5, 0.75, 1.0])
    entropy_bins: list[int] = field(default_factory=lambda: [10, 50, 200])
    temperatures: list[float] = field(default_factory=lambda: [0.25, 0.5, 1.0, 2.0, 4.0])

    def validate(self) -> None:
        _require_bool("sensitivity", "enabled", self.enabled)
        _require_float_list("sensitivity", "gammas", self.gammas, 0.0, 1.0)
        _require_int_list("sensitivity", "entropy_bins", self.entropy_bins,
                          2, 2001, max_entries=_MAX_BIN_ENTRIES)
        _require_float_list("sensitivity", "temperatures", self.temperatures,
                            0.0, float("inf"))
        if any(t <= 0.0 for t in self.temperatures):
            raise ConfigError("sensitivity.temperatures entries must be strictly positive")


@dataclass
class SanityConfig:
    """Analytic identity controls and invalid-input rejection controls."""

    enabled: bool = True

    def validate(self) -> None:
        _require_bool("sanity", "enabled", self.enabled)


@dataclass
class ExperimentConfig:
    """Central typed configuration for ``run_experiments``.

    ``n_replicates`` is the sample size of every seeded multi-replicate study
    and the sample unit of all reported mean intervals.
    ``confidence_level`` drives every interval in the results via
    ``statistics.NormalDist().inv_cdf((1 + level) / 2)``; the flat
    ``*_ci95_*`` sidecar identifiers are emitted only when the level is
    exactly 0.95, so a named alias never misstates its coverage.
    """

    seed: int = 20260907
    n_replicates: int = 256
    confidence_level: float = 0.95
    filtering: FilteringConfig = field(default_factory=FilteringConfig)
    calibration: CalibrationConfig = field(default_factory=CalibrationConfig)
    quantile: QuantileConfig = field(default_factory=QuantileConfig)
    projection: ProjectionConfig = field(default_factory=ProjectionConfig)
    sensitivity: SensitivityConfig = field(default_factory=SensitivityConfig)
    sanity: SanityConfig = field(default_factory=SanityConfig)

    def validate(self) -> None:
        if isinstance(self.seed, bool) or not isinstance(self.seed, int):
            raise ConfigError(f"seed must be an integer, got {self.seed!r}")
        if not 0 <= self.seed < 2**64:
            raise ConfigError(f"seed must be in [0, 2^64), got {self.seed}")
        _require_int("config", "n_replicates", self.n_replicates, 2, _MAX_REPLICATES)
        if not isinstance(self.confidence_level, (int, float)) \
                or isinstance(self.confidence_level, bool):
            raise ConfigError(
                f"confidence_level must be a number, got {self.confidence_level!r}")
        level = float(self.confidence_level)
        if not math_isfinite(level) or not 0.0 < level < 1.0:
            raise ConfigError(
                f"confidence_level must be strictly inside (0, 1), got {level}")
        for name, cls in (("filtering", FilteringConfig), ("calibration", CalibrationConfig),
                          ("quantile", QuantileConfig), ("projection", ProjectionConfig),
                          ("sensitivity", SensitivityConfig), ("sanity", SanityConfig)):
            section = getattr(self, name)
            if not isinstance(section, cls):
                raise ConfigError(f"{name} must be a {cls.__name__}")
            section.validate()

    # ---------- conversion ----------
    def to_dict(self) -> dict[str, Any]:
        """Return the canonical plain-dict form (JSON-serializable)."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Any) -> "ExperimentConfig":
        """Build a validated config from a plain dict.

        Raises:
            ConfigError: On unknown keys, wrong types, or out-of-range values.
        """
        if not isinstance(data, dict):
            raise ConfigError(f"config must be a mapping, got {type(data).__name__}")
        known = {f.name for f in fields(cls)}
        _reject_unknown("config", data, tuple(known))
        payload = dict(data)
        for section_name in ("filtering", "calibration", "quantile",
                             "projection", "sensitivity", "sanity"):
            section_cls = {
                "filtering": FilteringConfig, "calibration": CalibrationConfig,
                "quantile": QuantileConfig, "projection": ProjectionConfig,
                "sensitivity": SensitivityConfig, "sanity": SanityConfig,
            }[section_name]
            raw = payload.get(section_name, {})
            if not isinstance(raw, dict):
                raise ConfigError(f"{section_name} must be a mapping, got {type(raw).__name__}")
            _reject_unknown(section_name, raw, tuple(f.name for f in fields(section_cls)))
            payload[section_name] = section_cls(**raw)
        config = cls(**payload)
        config.validate()
        return config

    def enabled_sections(self) -> list[str]:
        """Names of the study blocks that will run, in execution order."""
        order = ("filtering", "calibration", "quantile", "projection",
                 "sensitivity", "sanity")
        sections = {"filtering": self.filtering, "calibration": self.calibration,
                    "quantile": self.quantile, "projection": self.projection,
                    "sensitivity": self.sensitivity, "sanity": self.sanity}
        return [name for name in order if getattr(sections[name], "enabled")]


DEFAULT_CONFIG = ExperimentConfig()


def canonical_config_json(config: ExperimentConfig) -> str:
    """Return the deterministic JSON text used for the provenance hash."""
    return json.dumps(config.to_dict(), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False)


def config_sha256(config: ExperimentConfig) -> str:
    """Return the SHA-256 of the canonical config JSON (provenance key)."""
    import hashlib

    return hashlib.sha256(canonical_config_json(config).encode("utf-8")).hexdigest()


def save_config(config: ExperimentConfig, path: str | Path) -> Path:
    """Serialize a config to JSON. Returns the written path."""
    config.validate()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config.to_dict(), indent=2, sort_keys=True,
                               ensure_ascii=True, allow_nan=False) + "\n", encoding="utf-8")
    return path


def load_config(path: str | Path) -> ExperimentConfig:
    """Load and validate a config from JSON.

    Raises:
        ConfigError: If the file is missing, unparseable, or invalid.
    """
    path = Path(path)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigError(f"config file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(f"config file {path} is not valid JSON: {exc}") from exc
    return ExperimentConfig.from_dict(raw)
