"""Publication plots of stored synthetic-study results; no experiment reruns.

Chart contract: filtering uses faceted replicate/mean dot plots; calibration
uses exact-target comparison and replicate-error intervals; sensitivity uses
faceted paired dot intervals for every prespecified arm. Blue marks and neutral
references, distinct marker fills and labels preserve meaning without color.
The manuscript and JSON provide configuration, estimators and sample units.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from .styles import FIGURE_DPI, FONT_SIZE_LABEL, FONT_SIZE_TITLE, save_publication_figure

_BLUE = "#2563EB"
_INK = "#374151"
_GRAY = "#9CA3AF"


def _vector(values: Any) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    if array.ndim != 1 or not array.size or not np.all(np.isfinite(array)):
        raise ValueError("Plot data must be a nonempty finite vector")
    return array


def _interval(mean: float, low: float, high: float) -> np.ndarray:
    values = _vector([mean, low, high])
    if values[1] > values[0] or values[0] > values[2]:
        raise ValueError("Plot interval must contain its reported mean")
    return np.array([[mean - low], [high - mean]])


def _style(ax: Axes, ylabel: str) -> None:
    ax.set_ylabel(ylabel, fontsize=FONT_SIZE_LABEL)
    ax.tick_params(labelsize=FONT_SIZE_LABEL)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#E5E7EB", linewidth=0.7)
    ax.set_axisbelow(True)


def _subtitle(results: Mapping[str, Any], confidence: float) -> str:
    cfg = results["provenance"]["experiments_config"]
    return (
        f"Synthetic inputs · {cfg['n_replicates']} independent replicates · "
        f"{confidence:.0%} pointwise normal intervals"
    )


def plot_filtering(results: Mapping[str, Any], output: Path) -> Path:
    """Show raw replicate variation beside its summary, with separate unit axes."""
    block = results["experiments"]["filtering"]
    specifications = (
        ("posterior_accuracy", "Posterior mass on true role", "Probability"),
        ("free_energy_final", "Final free energy", "Nats"),
        ("paired_loglik_diff", "Transition ablation", "Paired log posterior difference (nats)"),
    )
    first = block["uncertainty"][specifications[0][0]]
    confidence = float(first["confidence_level"])
    fig, axes = plt.subplots(1, len(specifications), figsize=(17, 6), layout="constrained")
    try:
        for ax, (key, title, unit) in zip(axes, specifications):
            values = _vector(block["samples"][key])
            interval = block["uncertainty"][key]
            if len(values) != results["provenance"]["experiments_config"]["n_replicates"]:
                raise ValueError("Filtering samples disagree with the replicate count")
            if not np.isclose(np.mean(values), interval["mean"]):
                raise ValueError("Filtering mean disagrees with the stored replicates")
            # Horizontal offsets separate points; they do not encode another quantity.
            offsets = np.linspace(-0.2, 0.2, len(values))
            ax.scatter(offsets, values, color=_GRAY, alpha=0.7, s=20, linewidths=0)
            ax.errorbar(
                [0.8], [interval["mean"]],
                yerr=_interval(interval["mean"], interval["low"], interval["high"]),
                fmt="o", color=_BLUE, capsize=6, linewidth=2, markersize=8,
            )
            ax.set_xticks([0, 0.8], ["Replicates", "Mean + CI"])
            ax.set_xlim(-0.4, 1.2)
            if key == "posterior_accuracy":
                ax.set_ylim(min(0, interval["low"]), max(1.03, interval["high"] + 0.03))
            if key == "paired_loglik_diff":
                ax.axhline(0, color=_INK, linestyle="--", linewidth=1)
            ax.set_title(title, fontsize=FONT_SIZE_TITLE, pad=14)
            _style(ax, unit)
        fig.suptitle("Synthetic filtering and transition ablation\n" + _subtitle(results, confidence), fontsize=FONT_SIZE_TITLE)
        save_publication_figure(fig, output, dpi=FIGURE_DPI, bbox_inches="tight")
    finally:
        plt.close(fig)
    return output


def plot_calibration(results: Mapping[str, Any], output: Path) -> Path:
    """Compare discrete attainable coverage with observed coverage and error."""
    rows = results["experiments"]["calibration"]["coverage_by_level"]
    levels = _vector([r["level"] for r in rows])
    observed = _vector([r["observed_mean"] for r in rows])
    target = _vector([r["exact_target_mean"] for r in rows])
    errors = _vector([r["paired_error_mean"] for r in rows])
    confidence = float(rows[0]["confidence_level"])
    yerr = np.concatenate([_interval(r["paired_error_mean"], *r["paired_error_ci"]) for r in rows], axis=1)
    if np.any(np.diff(levels) <= 0) or np.any((levels <= 0) | (levels >= 1)):
        raise ValueError("Calibration levels must increase strictly inside (0, 1)")
    if np.any((observed < 0) | (observed > 1) | (target < 0) | (target > 1)):
        raise ValueError("Calibration coverage must be a probability")
    fig, axes = plt.subplots(1, 2, figsize=(15, 6), layout="constrained")
    try:
        axes[0].plot(levels, target, "s--", color=_INK, markerfacecolor="white", label="Exact discrete target F(Q)")
        axes[0].plot(levels, observed, "o", color=_BLUE, label="Observed mean coverage")
        axes[0].plot([0, 1], [0, 1], ":", color=_GRAY, label="Nominal level (reference)")
        axes[0].set_ylim(0, 1.03)
        axes[0].set_title("Attainable and observed coverage", fontsize=FONT_SIZE_TITLE)
        axes[0].legend(fontsize=FONT_SIZE_LABEL, loc="lower right")
        _style(axes[0], "Coverage probability")
        axes[1].errorbar(levels, errors, yerr=yerr, fmt="o", color=_BLUE, capsize=3, linewidth=1.5)
        axes[1].axhline(0, color=_INK, linestyle="--", linewidth=1)
        axes[1].set_title("Error relative to exact target", fontsize=FONT_SIZE_TITLE)
        _style(axes[1], "Mean absolute coverage error")
        for ax in axes:
            ax.set_xlabel("Quantile level", fontsize=FONT_SIZE_LABEL)
        fig.suptitle("Synthetic discrete quantile calibration\n" + _subtitle(results, confidence), fontsize=FONT_SIZE_TITLE)
        save_publication_figure(fig, output, dpi=FIGURE_DPI, bbox_inches="tight")
    finally:
        plt.close(fig)
    return output


def plot_sensitivity(results: Mapping[str, Any], output: Path) -> Path:
    """Show every prespecified paired arm; never infer from a selected maximum."""
    blocks = results["experiments"]["sensitivity"]["arms"]
    specifications = (
        ("gamma", "Score scaling", "Gamma"),
        ("entropy_bins", "Entropy discretization", "Bin count"),
        ("temperature", "Policy temperature", "Temperature"),
    )
    fig, axes = plt.subplots(1, 3, figsize=(17, 6), layout="constrained")
    try:
        confidence = float(blocks["gamma"]["arms"][0]["confidence_level"])
        for ax, (key, title, xlabel) in zip(axes, specifications):
            block = blocks[key]
            rows = block["arms"]
            x = _vector([r["value"] for r in rows])
            y = _vector([r["paired_mean"] for r in rows])
            yerr = np.concatenate([_interval(r["paired_mean"], *r["paired_ci"]) for r in rows], axis=1)
            ax.errorbar(x, y, yerr=yerr, fmt="o", color=_BLUE, capsize=5, linewidth=1.5, markersize=8)
            ax.axhline(0, color=_INK, linestyle="--", linewidth=1)
            ax.set_title(f"{title}\nBaseline: {block['baseline']:g}", fontsize=FONT_SIZE_TITLE)
            ax.set_xlabel(xlabel, fontsize=FONT_SIZE_LABEL)
            if key == "temperature":
                ax.set_xscale("log", base=2)
                ax.set_xlabel(xlabel + " (log scale)", fontsize=FONT_SIZE_LABEL)
                ax.minorticks_off()
            ax.set_xticks(x, [f"{value:g}" for value in x])
            _style(ax, f"Paired mean change ({block['unit']})")
        fig.suptitle("Synthetic parameter sensitivity\n" + _subtitle(results, confidence), fontsize=FONT_SIZE_TITLE)
        save_publication_figure(fig, output, dpi=FIGURE_DPI, bbox_inches="tight")
    finally:
        plt.close(fig)
    return output


def generate_experiment_figures(results: Mapping[str, Any], output_dir: Path) -> list[Path]:
    """Render the declared study panels from one already-validated result object."""
    output_dir.mkdir(parents=True, exist_ok=True)
    return [
        plot_filtering(results, output_dir / "experiment_filtering.png"),
        plot_calibration(results, output_dir / "experiment_calibration.png"),
        plot_sensitivity(results, output_dir / "experiment_sensitivity.png"),
    ]
