"""Plots of supplied synthetic model output; no fabricated uncertainty or EEG data."""
from __future__ import annotations
from .styles import save_publication_figure
import logging
from typing import Optional
import numpy as np
import matplotlib.pyplot as plt
from ..cognitive.belief import CaseDiagramBelief
from ..numerics import finite_vector
from .styles import CASE_COLORS, FIGURE_DPI, COLOR_UNKNOWN

logger = logging.getLogger(__name__)


def _save(fig, path: str) -> str:
    save_publication_figure(fig, path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_belief_trajectory(
    trajectory: list[CaseDiagramBelief],
    word_labels: Optional[list[str]] = None,
    gloss_labels: Optional[list[str]] = None,
    title: str = "Synthetic evidence updates for one latent case role",
    figsize: tuple[int, int] = (12, 9),
    output_path: Optional[str] = None,
) -> str:
    """Plot categorical probabilities, entropy, and change between supplied beliefs.

    Labels identify evidence steps; this function does not parse the labels.
    An empty series returns no artifact for compatibility with interactive callers.
    """
    if not trajectory:
        logger.warning("Empty trajectory: no figure produced")
        return ""
    n = len(trajectory)
    roles = trajectory[0].roles
    if any(b.roles != roles for b in trajectory):
        raise ValueError("Trajectory roles and order must agree")
    labels = word_labels if word_labels is not None else [str(i + 1) for i in range(n)]
    if len(labels) != n or (gloss_labels is not None and len(gloss_labels) != n):
        raise ValueError("Step labels must match trajectory length")
    probs = np.array([b.probabilities for b in trajectory])
    x = np.arange(n)
    fig, axes = plt.subplots(3, 1, figsize=figsize, sharex=True, layout="constrained")
    for j, role in enumerate(roles):
        axes[0].plot(x, probs[:, j], "o-", label=role.name,
                     color=CASE_COLORS.get(role.name, COLOR_UNKNOWN))
    axes[0].set(ylabel="Probability", ylim=(-0.03, 1.03))
    axes[0].legend(ncol=min(4, len(roles)), fontsize=16)
    axes[1].plot(x, [b.entropy() for b in trajectory], "o-", color="#5B21B6")
    axes[1].set_ylabel("Entropy (nats)")
    changes = np.concatenate(([0.0], np.abs(np.diff(probs, axis=0)).sum(axis=1) / 2))
    axes[2].bar(x, changes, color="#0F766E")
    axes[2].set(ylabel="Total variation change", xlabel="Evidence step (first change is undefined; shown as zero)")
    axes[2].set_xticks(x, labels)
    for ax in axes:
        ax.tick_params(labelsize=16)
        ax.xaxis.label.set_size(16)
        ax.yaxis.label.set_size(16)
        ax.grid(axis="y", alpha=0.2)
    fig.suptitle(title, fontsize=16)
    return _save(fig, output_path or "daif_belief_trajectory.png")


def plot_free_energy_convergence(
    fe_trajectory: list[float],
    word_boundaries: Optional[list[int]] = None,
    word_labels: Optional[list[str]] = None,
    kl_trajectory: Optional[list[float]] = None,
    loglik_trajectory: Optional[list[float]] = None,
    title: str = "Synthetic sequential filtering: per-update free energy",
    figsize: tuple[int, int] = (14, 6),
    output_path: Optional[str] = None,
) -> str:
    """Plot supplied FE values and, when supplied, their verified KL/data-fit split.

    This is a sequence of changing objectives, not a fixed-objective convergence
    proof. Missing components are explicitly unavailable; inconsistent ones raise.
    """
    if not fe_trajectory:
        logger.warning("Empty free-energy series: no figure produced")
        return ""
    fe = finite_vector(fe_trajectory, "free energy")
    x = np.arange(1, len(fe) + 1)
    components = kl_trajectory is not None or loglik_trajectory is not None
    if components:
        kl = finite_vector(kl_trajectory, "KL", len(fe))
        fit = -finite_vector(loglik_trajectory, "expected log likelihood", len(fe))
        if not np.allclose(kl + fit, fe, rtol=1e-7, atol=1e-9):
            raise ValueError("Components do not sum to free energy")
    if word_boundaries is not None and (word_labels is None or len(word_labels) != len(word_boundaries)):
        raise ValueError("Boundary labels must match boundaries")
    fig, axes = plt.subplots(1, 2, figsize=figsize, layout="constrained")
    axes[0].plot(x, fe, "o-", color="#1D4ED8", label="Computed F")
    axes[0].set_ylabel("F (nats)")
    if word_boundaries is not None:
        for boundary, label in zip(word_boundaries, word_labels or []):
            axes[0].axvline(boundary, color="gray", alpha=0.3)
            axes[0].annotate(label, (boundary, 0.98), xycoords=("data", "axes fraction"),
                             rotation=90, va="top", fontsize=16)
    if components:
        axes[1].plot(x, kl, "s-", label="KL(posterior || predicted prior)")
        axes[1].plot(x, fit, "^-", label="Negative expected log likelihood")
        axes[1].plot(x, fe, "k--", label="Sum = F")
        axes[1].legend(fontsize=16)
    else:
        axes[1].text(0.5, 0.5, "Decomposition unavailable", transform=axes[1].transAxes, ha="center")
    axes[1].set_ylabel("Components (nats)")
    for ax in axes:
        ax.set_xlabel("Filter update")
        ax.tick_params(labelsize=16)
        ax.xaxis.label.set_size(16)
        ax.yaxis.label.set_size(16)
        ax.grid(alpha=0.2)
    fig.suptitle(title, fontsize=16)
    return _save(fig, output_path or "daif_free_energy_convergence.png")


def plot_erp_predictions(
    role_names: list[str],
    enriched_weights: list[float],
    prediction_errors: list[float],
    n400_amplitudes: Optional[list[float]] = None,
    p600_amplitudes: Optional[list[float]] = None,
    title: str = "Synthetic prediction-error proxies (uncalibrated model units)",
    figsize: tuple[int, int] = (14, 6),
    output_path: Optional[str] = None,
) -> str:
    """Plot supplied DPE and optional N400/P600-inspired proxies by role.

    No EEG measurements, literature amplitude ranges, or fitted waveforms are
    inferred from these numbers. Both amplitude series must be supplied together.
    """
    n = len(role_names)
    weights = finite_vector(enriched_weights, "weights", n)
    errors = finite_vector(prediction_errors, "prediction errors", n)
    components = n400_amplitudes is not None or p600_amplitudes is not None
    if components:
        n400 = finite_vector(n400_amplitudes, "N400 proxies", n)
        p600 = finite_vector(p600_amplitudes, "P600 proxies", n)
    fig, axes = plt.subplots(1, 2, figsize=figsize, layout="constrained")
    colors = [CASE_COLORS.get(role, COLOR_UNKNOWN) for role in role_names]
    for role, w, e, color in zip(role_names, weights, errors, colors):
        axes[0].scatter(w, e, color=color, s=65)
        axes[0].annotate(role, (w, e), xytext=(-4 if w > .85 else 4, 5), textcoords="offset points",
                         ha="right" if w > .85 else "left", fontsize=16)
    axes[0].margins(x=.12, y=.15)
    axes[0].set(xlabel="Hand-selected weight", ylabel="Prediction error (model units)")
    if components:
        x = np.arange(n)
        axes[1].bar(x - .2, n400, .4, label="N400-inspired proxy", color="#2563EB")
        axes[1].bar(x + .2, p600, .4, label="P600-inspired proxy", color="#C2410C")
        axes[1].set_xticks(x, role_names, rotation=35)
        axes[1].legend(fontsize=16)
    else:
        axes[1].text(.5, .5, "Amplitude proxies not supplied", transform=axes[1].transAxes, ha="center")
    axes[1].set_ylabel("Signed proxy amplitude (model units)")
    for ax in axes:
        ax.tick_params(labelsize=16)
        ax.xaxis.label.set_size(16)
        ax.yaxis.label.set_size(16)
        ax.grid(axis="y", alpha=.2)
    fig.suptitle(title, fontsize=16)
    return _save(fig, output_path or "daif_erp_predictions.png")
