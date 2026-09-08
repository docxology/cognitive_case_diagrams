"""End-to-end tests for the experiments runner, serialization, and validator.

The module fixture runs the bounded study suite twice at a small config and
pins the intended public contract: determinism, frozen schema, statistical
controls with real numerical bounds, source-freshness validation, and the
level-honest ``*_ci95_*`` sidecar rule.

Notes on interval semantics pinned here:

- Normal-approximation intervals on a nonnegative statistic may have a
  negative lower bound at small replicate counts; the tests require finite
  bounds, correct ordering, and that the interval CONTAINS the estimate.
  No clipping is applied to normal intervals.
- Normal-approximation mean intervals are APPROXIMATE at finite n; the
  estimator strings reported in the results say so.
"""
from __future__ import annotations

import copy
import json
import re
import shutil
from pathlib import Path

import pytest

from src.experiments import (
    ConfigError,
    results_to_json,
    run_experiments,
    validate_experiment_results,
    write_results,
)

SMALL_CONFIG = {
    "seed": 12345,
    "n_replicates": 6,
    "calibration": {"n_observations": 40},
    "quantile": {"brute_force_tau_points": 5001},
}

# Source trees bound into the provenance digest (relative to the repo root).
_SOURCE_DIRS = (
    "src/experiments", "src/case_systems", "src/cognitive", "src/daif",
    "src/enriched_cat", "src/quantum", "src/security", "src/topos_theory",
    "src/diagrams",
)
_SOURCE_FILES = ("src/numerics.py",)


def _copy_source_tree(destination: Path) -> None:
    """Copy the digest-bound source files into a temporary project tree."""
    repo = Path(__file__).resolve().parents[1]
    for rel_dir in _SOURCE_DIRS:
        shutil.copytree(repo / rel_dir, destination / rel_dir)
    for rel_file in _SOURCE_FILES:
        target = destination / rel_file
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(repo / rel_file, target)


@pytest.fixture(scope="module")
def small_results():
    return run_experiments(SMALL_CONFIG)


@pytest.fixture(scope="module")
def small_text(small_results):
    return results_to_json(small_results)


# --------------------------------------------------------------------------
# Schema, determinism, provenance
# --------------------------------------------------------------------------
def test_top_level_schema(small_results):
    assert set(small_results) == {
        "schema_version", "provenance", "experiments", "variables"}
    assert small_results["schema_version"] == "1.0"
    provenance = small_results["provenance"]
    assert provenance["seed"] == SMALL_CONFIG["seed"]
    assert provenance["config_sha256"]
    assert provenance["numpy_version"]
    assert set(provenance["source_files"])
    assert len(provenance["source_sha256"]) == 64
    assert all(not p.startswith("/") for p in provenance["source_files"])
    assert "src/experiments/runner.py" in provenance["source_files"]


def test_runs_are_deterministic(small_text):
    assert results_to_json(run_experiments(SMALL_CONFIG)) == small_text


def test_seed_changes_numbers(small_results):
    other = run_experiments({**SMALL_CONFIG, "seed": 999})
    filter_metrics = small_results["experiments"]["filtering"]["metrics"]
    other_metrics = other["experiments"]["filtering"]["metrics"]
    assert (other_metrics["posterior_accuracy_mean"]
            != filter_metrics["posterior_accuracy_mean"])


def test_invalid_config_via_run_experiments_raises():
    with pytest.raises(ConfigError):
        run_experiments({"n_replicates": 1})
    with pytest.raises(ConfigError):
        run_experiments({"unknown_key": True})
    with pytest.raises(ConfigError):
        run_experiments(42)  # type: ignore[arg-type]


def test_disabled_sections_produce_no_blocks():
    config = {key: {"enabled": False}
              for key in ("filtering", "calibration", "quantile",
                          "projection", "sensitivity", "sanity")}
    results = run_experiments({**config, "n_replicates": 4})
    assert results["experiments"] == {}
    assert results["variables"] == {}


def test_all_expected_blocks_present(small_results):
    assert set(small_results["experiments"]) == {
        "filtering", "calibration", "quantile", "projection",
        "quantum_projection", "sensitivity", "sanity"}


# --------------------------------------------------------------------------
# Statistical controls with real numerical bounds
# --------------------------------------------------------------------------
def test_filter_matches_exact_repeated_bayes(small_results):
    metrics = small_results["experiments"]["filtering"]["metrics"]
    assert metrics["closed_form_residual_max"] <= 1e-10
    assert 0.0 <= metrics["posterior_accuracy_mean"] <= 1.0
    assert -10.0 < metrics["paired_loglik_diff_mean"] < 10.0
    assert metrics["free_energy_final_mean"] > 0.0


def test_filter_supports_two_roles():
    results = run_experiments({**SMALL_CONFIG, "filtering": {"n_roles": 2},
                               "n_replicates": 4})
    metrics = results["experiments"]["filtering"]["metrics"]
    assert metrics["closed_form_residual_max"] <= 1e-10
    assert -10.0 < metrics["paired_loglik_diff_mean"] < 10.0


def test_calibration_hits_exact_discrete_law_target(small_results):
    block = small_results["experiments"]["calibration"]
    metrics = block["metrics"]
    # Exact-target error must be small binomial noise, not the atom gap.
    assert 0.0 <= metrics["coverage_error_mean"] < 0.15
    # The deterministic atom gap is nonnegative and bounded by one.
    assert 0.0 <= metrics["atom_gap_mean"] < 1.0
    assert 0.0 <= metrics["atom_gap_max"] < 1.0
    assert metrics["level_target_gap_max"] < 0.15
    levels = block["coverage_by_level"]
    assert len(levels) == 19
    required = {"level", "observed_mean", "exact_target_mean",
                "paired_error_mean", "paired_error_ci", "confidence_level"}
    for entry in levels:
        assert required <= set(entry)
        assert 0.05 <= entry["level"] <= 0.95
        assert 0.0 <= entry["paired_error_mean"]
        lo, hi = entry["paired_error_ci"]
        # Normal intervals on a nonnegative statistic may dip below zero at
        # small replicate counts: require finite bounds, correct ordering,
        # and that the interval contains the estimate. No clipping.
        assert all(bound == bound and abs(bound) != float("inf")
                   for bound in (lo, hi))
        assert lo <= entry["paired_error_mean"] <= hi


def test_quantile_exactness_controls(small_results):
    metrics = small_results["experiments"]["quantile"]["metrics"]
    assert metrics["wasserstein_selfdistance_max"] == 0.0
    assert metrics["wasserstein_point_mass_residual_max"] <= 1e-12
    assert metrics["wasserstein_shift_residual_max"] <= 1e-12
    # Offset pair: |Delta q| does not change sign, trapezoid is exact.
    assert metrics["bruteforce_w1_residual_max"] <= 1e-9
    # Crossing pair: trapezoid carries an O(h) bound on the kink interval.
    assert 0.0 <= metrics["bruteforce_w1_crossing_residual_max"] <= 1e-3
    assert metrics["wasserstein_triangle_violation_max"] <= 1e-12


def test_huber_update_matches_finite_difference_gradient(small_results):
    """Pins the quantile_td_update == gradient-step identity via FD.

    The objective is the asymmetric Huber LOSS (quadratic inside kappa,
    linear outside); its central-difference derivative must match the
    implementation's per-coordinate update to rounding.
    """
    metrics = small_results["experiments"]["quantile"]["metrics"]
    assert metrics["huber_fd_residual_max"] <= 1e-6
    assert metrics["huber_fd_residual_mean"] <= 1e-6


def test_projection_exactness_and_mass(small_results):
    metrics = small_results["experiments"]["projection"]["metrics"]
    assert metrics["mass_residual_max"] <= 1e-12
    assert metrics["mean_exactness_residual_max"] <= 1e-12
    assert metrics["refinement_paired_diff_mean"] <= 1e-12
    arms = small_results["experiments"]["projection"]["samples"]
    assert set(arms["mean_exactness_by_atom_count"]) == {"11", "51", "201"}


def test_quantum_probability_projection(small_results):
    metrics = small_results["experiments"]["quantum_projection"]["metrics"]
    assert metrics["completeness_residual_max"] <= 1e-12
    assert metrics["probability_range_violation_max"] <= 1e-12
    assert metrics["fluid_s_analytic_residual_max"] <= 1e-12


def test_sensitivity_arms_contract(small_results):
    block = small_results["experiments"]["sensitivity"]
    assert block["uncertainty"] == {}
    for sweep in ("gamma", "entropy_bins", "temperature"):
        arm = block["arms"][sweep]
        assert {"unit", "quantity", "baseline", "arms"} <= set(arm)
        # The baseline arm differs from itself exactly; the paired interval
        # is degenerate at zero.
        assert arm["arms"][0]["paired_ci"][0] == pytest.approx(0.0, abs=1e-12)
        assert arm["arms"][0]["paired_ci"][1] == pytest.approx(0.0, abs=1e-12)
        for entry in arm["arms"]:
            lo, hi = entry["paired_ci"]
            assert lo <= hi
    # Selected maxima are descriptive only: no interval fields anywhere.
    metrics = block["metrics"]
    assert set(metrics) == {
        "gamma_max_abs_effect", "gamma_sweep_value",
        "entropy_bins_max_abs_effect", "entropy_bins_sweep_value",
        "temperature_max_abs_effect", "temperature_sweep_value"}


def test_sanity_controls_all_pass(small_results):
    controls = small_results["experiments"]["sanity"]["controls"]
    assert controls["analytic_identities_failed"] == []
    assert controls["invalid_input_failed"] == []


# --------------------------------------------------------------------------
# Variables registry
# --------------------------------------------------------------------------
def test_variables_registry_contract(small_results):
    variables = small_results["variables"]
    assert variables
    pattern = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
    for name, entry in variables.items():
        assert pattern.match(name), name
        assert set(entry) == {"value", "unit", "ci_low", "ci_high",
                              "confidence_level", "sample_unit",
                              "interpretation"}
        assert isinstance(entry["value"], float)
        assert entry["unit"] in {"probability", "dimensionless", "nats",
                                 "count", "version"}
        assert entry["interpretation"]
        assert entry["sample_unit"]
        if entry["ci_low"] is None:
            assert entry["ci_high"] is None
        else:
            assert entry["ci_low"] <= entry["ci_high"]
    expected_roots = ("exp_filter_", "exp_calibration_", "exp_quantile_",
                      "exp_projection_", "exp_quantum_", "exp_sensitivity_",
                      "exp_sanity_")
    for name in variables:
        assert name.startswith(expected_roots), name


def test_sensitivity_variables_carry_no_intervals(small_results):
    variables = small_results["variables"]
    for name in ("exp_sensitivity_gamma_max_abs_effect",
                 "exp_sensitivity_entropy_bins_max_abs_effect",
                 "exp_sensitivity_temperature_max_abs_effect"):
        assert variables[name]["ci_low"] is None
        assert variables[name]["ci_high"] is None


def test_ci95_sidecars_only_at_exact_95(small_results):
    variables = small_results["variables"]
    sided = [n for n in variables if n.endswith(("_ci95_low", "_ci95_high"))]
    assert sided, "default config is at 0.95, so sidecars must exist"
    assert small_results["experiments"]["filtering"]["uncertainty"][
        "posterior_accuracy"]["confidence_level"] == 0.95

    other = run_experiments({**SMALL_CONFIG, "confidence_level": 0.9})
    other_vars = other["variables"]
    assert not [n for n in other_vars if n.endswith(("_ci95_low", "_ci95_high"))]
    entry = other_vars["exp_filter_posterior_accuracy_mean"]
    assert entry["ci_low"] is not None and entry["ci_high"] is not None
    assert entry["confidence_level"] == pytest.approx(0.9)


# --------------------------------------------------------------------------
# Serialization
# --------------------------------------------------------------------------
def test_write_results_round_trip(tmp_path, small_results, small_text):
    path = write_results(small_results, tmp_path / "out" / "results.json")
    assert path.exists()
    assert path.read_text(encoding="utf-8") == small_text
    assert json.loads(path.read_text(encoding="utf-8")) == small_results


def test_write_results_rejects_nonfinite(tmp_path, small_results):
    poisoned = copy.deepcopy(small_results)
    poisoned["experiments"]["sanity"]["metrics"]["n_analytic_identities"] = float("nan")
    # assert_finite_json guards before serialization and raises RuntimeError;
    # allow_nan=False in the encoder is the second line of defense.
    with pytest.raises(RuntimeError, match="non-finite"):
        write_results(poisoned, tmp_path / "nan.json")
    assert not (tmp_path / "nan.json").exists()


def test_default_write_path_is_canonical(tmp_path, small_results, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = write_results(small_results)
    # The canonical default path is relative to the working directory;
    # compare resolved locations (tmp_path may itself be a symlink).
    assert path == Path("output") / "experiments" / "results.json"
    assert path.resolve() == (tmp_path / path).resolve()
    assert path.exists()


# --------------------------------------------------------------------------
# Shared validator
# --------------------------------------------------------------------------
def test_validator_accepts_fresh_run(small_results):
    report = validate_experiment_results(small_results)
    assert report["valid"], report["errors"]
    assert report["errors"] == []
    assert all(report["checks"].values())


def test_validator_rejects_tampered_results(small_results):
    base = copy.deepcopy(small_results)

    wrong_schema = copy.deepcopy(base)
    wrong_schema["schema_version"] = "0.9"
    report = validate_experiment_results(wrong_schema)
    assert not report["valid"]
    assert any("schema_version" in e for e in report["errors"])

    stale = copy.deepcopy(base)
    first = sorted(stale["provenance"]["source_files"])[0]
    stale["provenance"]["source_files"][first] = "0" * 64
    report = validate_experiment_results(stale)
    assert not report["valid"]
    assert any("stale source bytes" in e for e in report["errors"])

    membership = copy.deepcopy(base)
    membership["provenance"]["source_files"].pop(first)
    report = validate_experiment_results(membership)
    assert not report["valid"]
    assert any("membership" in e for e in report["errors"])

    hash_mismatch = copy.deepcopy(base)
    hash_mismatch["provenance"]["config_sha256"] = "f" * 64
    report = validate_experiment_results(hash_mismatch)
    assert not report["valid"]
    assert any("config_sha256 mismatch" in e for e in report["errors"])

    seed_mismatch = copy.deepcopy(base)
    seed_mismatch["provenance"]["seed"] = base["provenance"]["seed"] + 1
    report = validate_experiment_results(seed_mismatch)
    assert not report["valid"]
    assert any("seed" in e for e in report["errors"])

    numpy_mismatch = copy.deepcopy(base)
    numpy_mismatch["provenance"]["numpy_version"] = "0.0-not-real"
    report = validate_experiment_results(numpy_mismatch)
    assert not report["valid"]
    assert any("NumPy" in e for e in report["errors"])

    bad_unit = copy.deepcopy(base)
    name = sorted(bad_unit["variables"])[0]
    bad_unit["variables"][name]["unit"] = "microvolts"
    report = validate_experiment_results(bad_unit)
    assert not report["valid"]
    assert any("unit" in e for e in report["errors"])

    bad_identifier = copy.deepcopy(base)
    key = sorted(bad_unit["variables"])[0]
    bad_identifier["variables"][key + "-dotted.name"] = bad_identifier["variables"][key]
    report = validate_experiment_results(bad_identifier)
    assert not report["valid"]

    sanity_broken = copy.deepcopy(base)
    sanity_broken["experiments"]["sanity"]["metrics"]["analytic_identities_pass"] = 0.0
    report = validate_experiment_results(sanity_broken)
    assert not report["valid"]
    assert any("analytic identity" in e for e in report["errors"])

    interval_crossed = copy.deepcopy(base)
    target = "exp_filter_posterior_accuracy_mean"
    interval_crossed["variables"][target]["ci_low"] = 1.0
    interval_crossed["variables"][target]["ci_high"] = 0.0
    report = validate_experiment_results(interval_crossed)
    assert not report["valid"]
    assert any("low <= high" in e for e in report["errors"])


def test_validator_rejects_malformed_inputs():
    garbage_samples: list[object] = [None, [], "results", 42]
    for garbage in garbage_samples:
        report = validate_experiment_results(garbage)
        assert not report["valid"]
        assert report["errors"]


def test_validator_freshness_on_copied_then_mutated_tree(
    tmp_path, small_results,
):
    """A faithful copy validates; mutating one bound file invalidates.

    The temporary tree must contain the FULL source membership so the
    fingerprint is non-empty; an empty or symlinked set is rejected outright
    by the tightened wrapper.
    """
    tree = tmp_path / "project"
    _copy_source_tree(tree)
    fresh = validate_experiment_results(small_results, project_root=tree)
    assert fresh["valid"], fresh["errors"]

    bound_file = tree / "src" / "experiments" / "rng.py"
    bound_file.write_text(bound_file.read_text(encoding="utf-8") + "\n# mutated\n",
                          encoding="utf-8")
    stale_report = validate_experiment_results(small_results, project_root=tree)
    assert not stale_report["valid"]
    assert any("stale source bytes" in e for e in stale_report["errors"])


def test_validator_rejects_empty_source_tree(tmp_path, small_results):
    (tmp_path / "src" / "experiments").mkdir(parents=True)
    report = validate_experiment_results(small_results, project_root=tmp_path)
    assert not report["valid"]
    assert any("source" in e for e in report["errors"])
