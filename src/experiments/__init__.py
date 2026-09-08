"""Bounded synthetic statistical experiments for the numerical lane.

Public entry point::

    from src.experiments import run_experiments

    results = run_experiments()          # default ExperimentConfig
    results = run_experiments({"seed": 1, "n_replicates": 64})

The returned dict is JSON-serializable, deterministic for a fixed config,
and self-describing: ``schema_version``, ``provenance`` (config hash, seed,
source digests), ``experiments`` (per-study blocks), and ``variables`` (the
flat ``exp_*`` registry consumed by manuscript injection and MCP).

All studies are synthetic and seeded; no empirical datasets, human effects,
or p-values are produced anywhere in this package. Consumers of a results
artifact should call :func:`validate_experiment_results` before trusting it.
See this package's README.md, AGENTS.md, and SKILL.md for the study designs
and uncertainty conventions.
"""
from .config import (
    DEFAULT_CONFIG,
    CalibrationConfig,
    ConfigError,
    ExperimentConfig,
    FilteringConfig,
    ProjectionConfig,
    QuantileConfig,
    SanityConfig,
    SensitivityConfig,
    canonical_config_json,
    config_sha256,
    load_config,
    save_config,
)
from .rng import STREAM_IDS, master_rng, replicate_rng
from .runner import (
    DEFAULT_RESULTS_PATH,
    RESULTS_SCHEMA_VERSION,
    assert_finite_json,
    run_experiments,
    validate_experiment_results,
)
from .serialization import results_to_json, write_results
from .stats import Z95, ci_block, mean_ci, normal_z, paired_mean_ci, wilson_score_interval

__all__ = [
    # entry point
    "run_experiments",
    "validate_experiment_results",
    "RESULTS_SCHEMA_VERSION",
    "DEFAULT_RESULTS_PATH",
    "assert_finite_json",
    # config
    "ExperimentConfig",
    "FilteringConfig",
    "CalibrationConfig",
    "QuantileConfig",
    "ProjectionConfig",
    "SensitivityConfig",
    "SanityConfig",
    "ConfigError",
    "DEFAULT_CONFIG",
    "canonical_config_json",
    "config_sha256",
    "load_config",
    "save_config",
    # serialization
    "results_to_json",
    "write_results",
    # rng
    "STREAM_IDS",
    "master_rng",
    "replicate_rng",
    # statistics
    "Z95",
    "normal_z",
    "ci_block",
    "mean_ci",
    "paired_mean_ci",
    "wilson_score_interval",
]
