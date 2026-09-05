"""Active inference visualization for cognitive case diagrams.

Renders belief distributions, free energy landscapes, and prediction errors
over time or trials. Scalar §7 figures use ``plot_alignment_frame_belief_dynamics``
for evidence-step trajectories; ``plot_belief_distribution`` remains a single-snapshot
bar chart for diagnostics.
"""

from __future__ import annotations

import logging
from typing import Optional, Sequence

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

from ..cognitive.belief import CaseDiagramBelief
from ..cognitive.free_energy import variational_free_energy
from .styles import (
    CASE_COLORS, FONT_SIZE_FLOOR, FONT_SIZE_TITLE, FONT_SIZE_LABEL,
    FONT_SIZE_ANNOTATION, DEFAULT_FIGSIZE, FIGURE_DPI, COLOR_UNKNOWN,
    GRID_ALPHA,
)

logger = logging.getLogger(__name__)


def plot_alignment_frame_belief_dynamics(
    prior: CaseDiagramBelief,
    trajectory: Sequence[CaseDiagramBelief],
    observation_sequence: Sequence[np.ndarray],
    *,
    frame_labels: Optional[tuple[str, str]] = None,
    evidence_labels: Optional[Sequence[str]] = None,
    figsize: tuple[int, int] = (14, 11),
    title: str = (
        "Alignment-Frame Belief: Sequential Evidence and Variational Free Energy"
    ),
    output_path: Optional[str] = None,
) -> str:
    """Plot 3-panel scalar belief dynamics over competing alignment frames.

    After each Bayesian update, variational free energy is
    ``E_q[log q - log p(o|s) - log p(s)]`` for that step's likelihood.
    Per-step ``F[q]`` need not decrease; the bottom panel plots both the
    raw curve and ``min_{τ≤t} F[q_τ]`` (running minimum; non-increasing envelope).
    """
    obs_list = [np.asarray(o, dtype=np.float64) for o in observation_sequence]
    traj_list = list(trajectory)
    if not traj_list or not obs_list:
        logger.warning("Empty trajectory or observations; skipping dynamics plot")
        return ""
    if len(traj_list) != len(obs_list):
        raise ValueError(
            f"trajectory ({len(traj_list)}) and observation_sequence "
            f"({len(obs_list)}) must match"
        )
    n_steps = len(traj_list)
    role_names = [r.name for r in prior.roles]
    if [r.name for r in traj_list[0].roles] != role_names:
        raise ValueError("All beliefs in trajectory must share prior.roles")

    if frame_labels is None:
        frame_labels = (
            "Accusative frame (NOM–ACC)",
            "Ergative frame (ERG–ABS)",
        )
    if evidence_labels is None:
        evidence_labels = [f"{i + 1}" for i in range(n_steps)]
    elif len(evidence_labels) != n_steps:
        raise ValueError(
            f"evidence_labels ({len(evidence_labels)}) must equal "
            f"len(trajectory) ({n_steps})"
        )

    log_prior = np.log(np.maximum(prior.probabilities, 1e-12))
    fe_after_update: list[float] = []
    for i, belief in enumerate(traj_list):
        q = belief.probabilities
        log_lik = np.log(np.maximum(obs_list[i], 1e-12))
        fe_after_update.append(variational_free_energy(q, log_lik, log_prior))

    prob_rows = np.vstack([prior.probabilities] + [b.probabilities for b in traj_list])
    entropies = [b.entropy() for b in traj_list]
    x_prior = np.arange(0, prob_rows.shape[0])

    fig = plt.figure(figsize=figsize, dpi=FIGURE_DPI)
    gs = gridspec.GridSpec(3, 1, height_ratios=[1.15, 0.75, 0.85], hspace=0.36)

    colors = [CASE_COLORS.get(role_names[i], COLOR_UNKNOWN) for i in range(len(role_names))]
    legend_names = list(frame_labels)

    ax1 = fig.add_subplot(gs[0])
    ax1.stackplot(
        x_prior,
        prob_rows.T,
        labels=legend_names,
        colors=colors,
        alpha=0.88,
    )
    ax1.set_ylabel("P(alignment frame)", fontsize=FONT_SIZE_LABEL)
    ax1.set_title(
        "Posterior over alignment frames",
        fontsize=FONT_SIZE_LABEL,
        fontweight="bold",
    )
    ax1.set_xlim(float(x_prior[0]), float(x_prior[-1]))
    ax1.set_ylim(0.0, 1.0)
    ax1.legend(
        loc="upper right",
        fontsize=FONT_SIZE_FLOOR - 2,
        ncol=min(len(role_names), 2),
        framealpha=0.92,
    )
    ax1.grid(True, alpha=GRID_ALPHA)
    ax1.tick_params(labelsize=FONT_SIZE_FLOOR)
    xtick_labels = ["Prior"] + list(evidence_labels)
    ax1.set_xticks(x_prior)
    ax1.set_xticklabels(xtick_labels, fontsize=FONT_SIZE_FLOOR, fontstyle="italic")

    x_steps = np.arange(1, n_steps + 1).tolist()
    ax2 = fig.add_subplot(gs[1])
    ax2.plot(
        x_steps,
        entropies,
        "o-",
        color="#2563EB",
        linewidth=2.5,
        markersize=9,
        markerfacecolor="white",
        markeredgewidth=2.2,
    )
    ax2.fill_between(x_steps, entropies, alpha=0.12, color="#2563EB")
    ax2.set_ylabel("H(q) nats", fontsize=FONT_SIZE_LABEL)
    ax2.set_title("Entropy during belief updating", fontsize=FONT_SIZE_LABEL, fontweight="bold")
    ax2.grid(True, alpha=GRID_ALPHA)
    ax2.set_xticks(x_steps)
    ax2.set_xticklabels(list(evidence_labels), fontsize=FONT_SIZE_FLOOR, fontstyle="italic")
    if len(entropies) > 1:
        drops = [entropies[i] - entropies[i + 1] for i in range(len(entropies) - 1)]
        steepest = int(np.argmax(drops))
        y_annot = max(entropies[0] * 0.82, float(np.min(entropies)) + 0.02)
        ax2.annotate(
            f"−{drops[steepest]:.2f} nats\n({evidence_labels[steepest + 1]})",
            xy=(x_steps[steepest + 1], entropies[steepest + 1]),
            xytext=(x_steps[steepest + 1] + 0.35, y_annot),
            fontsize=FONT_SIZE_ANNOTATION,
            arrowprops=dict(arrowstyle="->", color="#DC2626", lw=2),
            color="#DC2626",
            fontweight="bold",
        )

    ax3 = fig.add_subplot(gs[2])
    fe_arr = np.asarray(fe_after_update, dtype=np.float64)
    fe_running = np.minimum.accumulate(fe_arr)
    ax3.plot(
        x_steps,
        fe_arr,
        "o-",
        color="#A78BFA",
        linewidth=1.8,
        markersize=6,
        markerfacecolor="white",
        markeredgewidth=1.5,
        alpha=0.88,
        label=r"$F[q]$ (per-step)",
    )
    ax3.plot(
        x_steps,
        fe_running,
        "s-",
        color="#5B21B6",
        linewidth=2.8,
        markersize=8,
        markerfacecolor="white",
        markeredgewidth=2,
        label=r"$\min_{\tau\leq t} F[q_\tau]$ (envelope)",
    )
    ax3.fill_between(x_steps, fe_running, alpha=0.14, color="#5B21B6")
    y_min = float(np.min(fe_running))
    y_max = float(np.max(np.maximum(fe_arr, fe_running)))
    pad = max((y_max - y_min) * 0.12, 0.05)
    ax3.set_ylim(bottom=y_min - pad, top=y_max + pad)
    y_text = ax3.get_ylim()[1]
    for xv, wl in zip(x_steps, evidence_labels):
        ax3.axvline(x=xv, color="#6B7280", linestyle="--", linewidth=1.1, alpha=0.55)
        ax3.text(
            xv,
            y_text * 0.94,
            f"  {wl}",
            fontsize=FONT_SIZE_ANNOTATION - 2,
            color="#374151",
            fontstyle="italic",
            rotation=90,
            va="top",
        )
    ax3.set_xlabel("Evidence step", fontsize=FONT_SIZE_LABEL)
    ax3.set_ylabel(r"Variational free energy $F[q]$", fontsize=FONT_SIZE_LABEL)
    ax3.set_title(
        "Free energy (per-step and running minimum)",
        fontsize=FONT_SIZE_LABEL,
        fontweight="bold",
    )
    ax3.grid(True, alpha=GRID_ALPHA)
    ax3.legend(fontsize=FONT_SIZE_FLOOR - 2, framealpha=0.9, loc="upper right")
    ax3.set_xticks(x_steps)
    ax3.set_xticklabels([str(int(s)) for s in x_steps])

    fig.suptitle(title, fontsize=FONT_SIZE_TITLE, fontweight="bold", y=0.98)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.92, bottom=0.06)

    if output_path is None:
        output_path = "active_inference_belief.png"
    fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved alignment-frame belief dynamics to %s", output_path)
    return output_path


def plot_belief_distribution(
    belief: CaseDiagramBelief,
    title: str = "Case Role Belief Distribution",
    output_path: Optional[str] = None,
) -> str:
    """Plot the categorical distribution of beliefs over case roles."""
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE, dpi=FIGURE_DPI)

    roles = [r.name for r in belief.roles]
    probs = belief.probabilities
    colors = [CASE_COLORS.get(r, COLOR_UNKNOWN) for r in roles]
    bars = ax.bar(roles, probs, color=colors, alpha=0.8, edgecolor="black", linewidth=1.5)

    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Probability", fontsize=FONT_SIZE_LABEL)
    ax.set_title(title, fontsize=FONT_SIZE_TITLE)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.2f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=FONT_SIZE_FLOOR,
        )

    plt.tight_layout()
    if output_path is None:
        output_path = f"belief_dist_{belief.name}.png" if belief.name else "belief_distribution.png"
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved belief distribution plot to %s", output_path)
    return output_path
