"""Fluid-S alignment visualization.

Renders the volition–agentivity landscape as a 2D decision surface
with functor boundary, overlaid Bats verb exemplars, and ERG/ABS regions.

Figure 2 of the manuscript.
"""
from __future__ import annotations

import logging
from typing import Optional
import numpy as np
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap

from ..case_systems.fluid_s import FluidSFunctor, VolitionContext
from .styles import (
    CASE_COLORS, FONT_SIZE_FLOOR, FONT_SIZE_TITLE, FONT_SIZE_LABEL,
    FIGURE_DPI,
    FLUID_S_AGENT_THRESHOLD,
)

logger = logging.getLogger(__name__)

# Bats verb exemplars: (verb, volition_probability, proto_agentivity)
BATS_VERBS = [
    ("sneeze", 0.10, 0.15),
    ("fall (acc.)", 0.15, 0.20),
    ("sleep", 0.25, 0.30),
    ("shiver", 0.30, 0.25),
    ("trip", 0.20, 0.35),
    ("walk", 0.55, 0.60),
    ("fall (vol.)", 0.75, 0.55),
    ("run", 0.80, 0.75),
    ("jump", 0.90, 0.85),
    ("fight", 0.95, 0.90),
]


def _sigmoid(x: np.ndarray, k: float = 10.0, x0: float = 0.5) -> np.ndarray:
    """Logistic sigmoid for smooth decision boundary."""
    return 1.0 / (1.0 + np.exp(-k * (x - x0)))


def plot_fluid_s_volition_landscape(
    functors: list[FluidSFunctor] | None = None,
    probabilities: list[float] | None = None,
    verb_names: list[str] | None = None,
    title: str = "Fluid-S Volition Landscape: Context-Dependent Case Assignment",
    output_path: Optional[str] = None,
) -> str:
    """Plot the 2D volition-agentivity landscape with functor decision boundary.

    Renders a heatmap where:
      - x-axis = volitional control theta in [0,1]
      - y-axis = proto-agentivity (Dowty 1991) in [0,1]
      - color = P(ERG | theta, agentivity)
    Overlays Bats verb exemplars at their coordinates and draws the
    F_theta functor decision boundary curve.

    Note: ``functors``, ``probabilities``, and ``verb_names`` are accepted
    for backward compatibility but not used. The plot uses the canonical
    ``BATS_VERBS`` exemplar data defined in this module.

    Args:
        functors: Unused (kept for API compatibility).
        probabilities: Unused (kept for API compatibility).
        verb_names: Unused (kept for API compatibility).
        title: Title of the plot.
        output_path: Path to save the figure.

    Returns:
        The output path where the figure was saved.
    """
    fig, ax = plt.subplots(figsize=(10, 8), dpi=FIGURE_DPI)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # --- 2D decision surface ---
    theta = np.linspace(0, 1, 200)
    agentivity = np.linspace(0, 1, 200)
    T, A = np.meshgrid(theta, agentivity)

    # P(ERG | θ, agentivity) = σ(w₁θ + w₂A - threshold)
    # Combined probability: higher volition + higher agentivity → ERG
    combined = 0.6 * T + 0.4 * A
    P_erg = _sigmoid(combined, k=12.0, x0=FLUID_S_AGENT_THRESHOLD)

    # Custom colormap: ABS (cool blue, lighter) → ERG (warm red-orange, deeper)
    # Slightly desaturated so labels remain legible on white background
    abs_color = "#4f8ef7"   # medium blue
    erg_color = "#e53935"   # deep red
    cmap = LinearSegmentedColormap.from_list(
        "abs_erg", [abs_color, "#ffb300", erg_color], N=256
    )

    im = ax.pcolormesh(T, A, P_erg, cmap=cmap, shading='gouraud', alpha=0.80)
    cbar = fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label("P(ERG | θ, agentivity)", fontsize=FONT_SIZE_LABEL, color="#111111")
    cbar.ax.tick_params(labelsize=FONT_SIZE_FLOOR, colors="#111111")
    cbar.ax.yaxis.set_tick_params(color="#111111")
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color="#111111")

    # --- Decision boundary contour ---
    # Use dark charcoal on white background for visibility
    contour = ax.contour(
        T, A, P_erg, levels=[0.5], colors=["#212121"],
        linewidths=2.5, linestyles="--",
    )
    ax.clabel(contour, fmt="F_θ boundary", fontsize=FONT_SIZE_FLOOR,
              inline=True, inline_spacing=10, colors=["#212121"])

    # --- Bats verb exemplars ---
    for verb, vol, agent in BATS_VERBS:
        is_erg = (0.6 * vol + 0.4 * agent) >= FLUID_S_AGENT_THRESHOLD
        marker = "^" if is_erg else "v"
        # White edge so markers stand out against the coloured heatmap
        edge_color = "white"
        face_color = erg_color if is_erg else abs_color
        ax.scatter(
            vol, agent, s=150, marker=marker,
            facecolors=face_color, edgecolors=edge_color,
            linewidths=2.0, zorder=5,
        )
        # Labels: dark text with a white halo for legibility on coloured surface
        offset_x = 0.02 if vol < 0.5 else -0.02
        ha = "left" if vol < 0.5 else "right"
        ax.annotate(
            verb, (vol, agent),
            xytext=(offset_x, 0.03), textcoords="offset fontsize",
            fontsize=FONT_SIZE_FLOOR - 1, color="#1a1a1a",
            fontweight="bold", ha=ha, va="bottom",
            path_effects=[
                pe.withStroke(linewidth=3, foreground="white")
            ],
        )

    # --- Region annotations ---
    ax.text(
        0.13, 0.87, "ABS\n(Patient-like)",
        fontsize=FONT_SIZE_LABEL, color="#ffffff", fontweight="bold",
        ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.4", facecolor=abs_color, alpha=0.85, edgecolor="white"),
    )
    ax.text(
        0.87, 0.87, "ERG\n(Agent-like)",
        fontsize=FONT_SIZE_LABEL, color="#ffffff", fontweight="bold",
        ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.4", facecolor=erg_color, alpha=0.85, edgecolor="white"),
    )

    # --- Functor notation ---
    ax.text(
        0.5, 0.02, r"$F_{\theta}: \mathcal{U} \to \mathcal{L}$  |  "
                    r"$F_{+\mathrm{vol}}(S) = \mathrm{ERG}$, "
                    r"$F_{-\mathrm{vol}}(S) = \mathrm{ABS}$",
        fontsize=FONT_SIZE_FLOOR, color="#111111", fontweight="bold",
        ha="center", va="bottom", transform=ax.transAxes,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.85, edgecolor="#aaaaaa"),
    )

    # --- Legend ---
    erg_patch = mpatches.Patch(color=erg_color, label="ERG (Agent/Volitional)")
    abs_patch = mpatches.Patch(color=abs_color, label="ABS (Patient/Non-volitional)")
    boundary_line = plt.Line2D([0], [0], color="#212121", linestyle="--",
                                linewidth=2, label="$F_\\theta$ boundary (P=0.5)")
    ax.legend(
        handles=[erg_patch, abs_patch, boundary_line],
        loc="upper left", fontsize=FONT_SIZE_FLOOR,
        framealpha=0.92, facecolor="white", edgecolor="#cccccc",
        labelcolor="#111111",
    )

    ax.set_xlabel("Volitional Control θ", fontsize=FONT_SIZE_LABEL, color="#111111")
    ax.set_ylabel("Proto-Agentivity (Dowty 1991)", fontsize=FONT_SIZE_LABEL, color="#111111")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(title, fontsize=FONT_SIZE_TITLE, fontweight="bold", pad=15, color="#111111")
    ax.tick_params(labelsize=FONT_SIZE_FLOOR, colors="#111111")
    ax.spines[:].set_edgecolor("#aaaaaa")

    fig.tight_layout()

    if output_path is None:
        output_path = "fluid_s_volition_landscape.png"
    fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    logger.info("Saved Fluid-S volition landscape to %s", output_path)

    return output_path
