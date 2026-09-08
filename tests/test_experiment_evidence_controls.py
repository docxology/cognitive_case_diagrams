"""Negative controls for complete, internally coherent synthetic evidence."""
from copy import deepcopy

import numpy as np
import pytest

from src.experiments import run_experiments, validate_experiment_results
from src.experiments.stats import ci_block


@pytest.fixture(scope="module")
def evidence():
    return run_experiments({"n_replicates": 4, "quantile": {"brute_force_tau_points": 101}})


def test_repeated_filtering_exposes_transition_effect(evidence):
    differences = evidence["experiments"]["filtering"]["samples"]["paired_loglik_diff"]
    assert np.max(np.abs(differences)) > 1e-4
    first_step = run_experiments({
        "n_replicates": 4, "filtering": {"n_iterations": 1},
        "calibration": {"enabled": False}, "quantile": {"enabled": False},
        "projection": {"enabled": False}, "sensitivity": {"enabled": False},
    })
    np.testing.assert_allclose(
        first_step["experiments"]["filtering"]["samples"]["paired_loglik_diff"],
        0, atol=1e-14,
    )


def test_missing_configured_study_is_rejected_even_with_matching_variables(evidence):
    changed = deepcopy(evidence)
    del changed["experiments"]["filtering"]
    changed["variables"] = {k: v for k, v in changed["variables"].items() if not k.startswith("exp_filter_")}
    verdict = validate_experiment_results(changed)
    assert not verdict["valid"]
    assert not verdict["checks"]["experiment_membership"]


@pytest.mark.parametrize("field,value", [
    ("low", 2.0), ("high", -2.0), ("mean", True),
    ("confidence_level", .8), ("estimator", ""), ("sample_unit", " "),
])
def test_inconsistent_interval_is_rejected(evidence, field, value):
    changed = deepcopy(evidence)
    changed["experiments"]["filtering"]["uncertainty"]["posterior_accuracy"][field] = value
    verdict = validate_experiment_results(changed)
    assert not verdict["valid"]
    assert any("interval" in error for error in verdict["errors"])


def test_unexpected_generator_and_missing_metric_are_rejected(evidence):
    changed = deepcopy(evidence)
    changed["provenance"]["generator"] = "unrelated producer"
    del changed["experiments"]["quantile"]["metrics"]["bruteforce_w1_crossing_residual_max"]
    verdict = validate_experiment_results(changed)
    assert not verdict["valid"]
    assert not verdict["checks"]["generator"]
    assert any("Required study metric missing" in error for error in verdict["errors"])


@pytest.mark.parametrize("estimate,low,high", [(2., 3., 1.), (2., 0., 1.), (-2., 0., 1.)])
def test_interval_writer_rejects_inverted_or_displaced_bounds(estimate, low, high):
    with pytest.raises(ValueError, match="low <= estimate <= high"):
        ci_block(estimate, low, high, .95, "normal", "replicate")


@pytest.mark.parametrize("estimator,sample_unit", [(1, "replicate"), ("normal", []), (" ", "replicate")])
def test_interval_writer_requires_real_descriptions(estimator, sample_unit):
    with pytest.raises(ValueError, match="non-empty strings"):
        ci_block(0., -1., 1., .95, estimator, sample_unit)


def test_ci95_alias_requires_exact_confidence():
    result = run_experiments({
        "n_replicates": 2, "confidence_level": .95 + 1e-13,
        "calibration": {"enabled": False}, "quantile": {"enabled": False},
        "projection": {"enabled": False}, "sensitivity": {"enabled": False},
    })
    assert validate_experiment_results(result)["valid"]
    assert not any("_ci95_" in name for name in result["variables"])
