"""Real PNG rendering and rejection of inconsistent stored experiment summaries."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pytest

from src.visualization.experiment_plots import (
    _interval,
    _vector,
    generate_experiment_figures,
    plot_calibration,
    plot_filtering,
)


@pytest.fixture
def results() -> dict:
    samples = [0.2, 0.4, 0.6, 0.8]
    interval = {"mean": 0.5, "low": 0.25, "high": 0.75, "confidence_level": 0.95}
    keys = ("posterior_accuracy", "free_energy_final", "paired_loglik_diff")
    arms = [
        {"value": 1, "paired_mean": 0, "paired_ci": [0, 0], "confidence_level": 0.95},
        {"value": 2, "paired_mean": 0.3, "paired_ci": [0.1, 0.5], "confidence_level": 0.95},
    ]
    return {
        "provenance": {"experiments_config": {"n_replicates": len(samples)}},
        "experiments": {
            "filtering": {
                "samples": {key: samples.copy() for key in keys},
                "uncertainty": {key: interval.copy() for key in keys},
            },
            "calibration": {"coverage_by_level": [
                {"level": 0.25, "observed_mean": 0.5, "exact_target_mean": 0.5,
                 "paired_error_mean": 0.1, "paired_error_ci": [0.05, 0.15], "confidence_level": 0.95},
                {"level": 0.75, "observed_mean": 0.9, "exact_target_mean": 0.9,
                 "paired_error_mean": 0.02, "paired_error_ci": [0.01, 0.03], "confidence_level": 0.95},
            ]},
            "sensitivity": {"arms": {
                key: {"arms": deepcopy(arms), "baseline": 1, "unit": unit}
                for key, unit in (("gamma", "dimensionless"), ("entropy_bins", "nats"), ("temperature", "nats"))
            }},
        },
    }


def test_render_all_stored_panels(results: dict, tmp_path: Path) -> None:
    paths = generate_experiment_figures(results, tmp_path)
    assert {p.name for p in paths} == {
        "experiment_filtering.png", "experiment_calibration.png", "experiment_sensitivity.png"
    }
    for path in paths:
        with Image.open(path) as image:
            assert image.width > 1000 and image.height > 500
            assert np.asarray(image.convert("RGB")).std() > 10
    assert not plt.get_fignums()


@pytest.mark.parametrize("values", [[], [[1, 2]], [float("nan")], [float("inf")]])
def test_nonfinite_or_nonvector_data_rejected(values: list) -> None:
    with pytest.raises(ValueError, match="finite vector"):
        _vector(values)


@pytest.mark.parametrize("values", [(1, 2, 3), (2, 0, 1)])
def test_interval_must_contain_estimate(values: tuple) -> None:
    with pytest.raises(ValueError, match="contain"):
        _interval(*values)


@pytest.mark.parametrize("mutation", ["count", "mean"])
def test_summary_cannot_disagree_with_replicates(results: dict, tmp_path: Path, mutation: str) -> None:
    if mutation == "count":
        results["provenance"]["experiments_config"]["n_replicates"] += 1
    else:
        results["experiments"]["filtering"]["uncertainty"]["posterior_accuracy"]["mean"] = 0.6
    with pytest.raises(ValueError, match="disagree"):
        plot_filtering(results, tmp_path / "bad.png")
    assert not (tmp_path / "bad.png").exists()
    assert not plt.get_fignums()


@pytest.mark.parametrize("mutation", ["levels", "range"])
def test_invalid_calibration_coordinates_rejected(results: dict, tmp_path: Path, mutation: str) -> None:
    rows = results["experiments"]["calibration"]["coverage_by_level"]
    if mutation == "levels":
        rows[1]["level"] = rows[0]["level"]
    else:
        rows[0]["observed_mean"] = 1.1
    with pytest.raises(ValueError):
        plot_calibration(results, tmp_path / "bad.png")
    assert not (tmp_path / "bad.png").exists()
