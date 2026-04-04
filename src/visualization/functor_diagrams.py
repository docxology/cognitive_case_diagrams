"""Alignment functor diagram visualizations.

Renders side-by-side publication-quality category diagrams representing
source (Accusative) and target (Ergative) alignment systems, with explicit
fixed-position hierarchical node layouts and clean functor arrows.

Figure 17 of the manuscript: F: C_acc → C_erg
"""

import logging
from pathlib import Path
from typing import Optional

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from ..case_systems.functor import AlignmentFunctor
from .styles import (
    CASE_COLORS, FONT_SIZE_FLOOR, FONT_SIZE_TITLE, FONT_SIZE_LABEL,
    FIGURE_DPI, COLOR_FUNCTOR_ARROW, COLOR_TEXT, COLOR_NEUTRAL,
    COLOR_EDGE,
    mathtext_safe_arrows,
)

logger = logging.getLogger(__name__)

# ─── Fixed node positions (data coords 0–1) for each alignment system ──────
# Source: AccusativeSystem  — NOM groups {S,A};  ACC groups {P}
# Vertical hierarchy: intransitive-S / Agent at top, NOM in middle, then P, ACC at bottom.
_ACC_POSITIONS: dict[str, tuple[float, float]] = {
    "S":   (0.15, 0.90),
    "A":   (0.85, 0.90),
    "NOM": (0.50, 0.60),
    "P":   (0.50, 0.30),
    "ACC": (0.50, 0.02),
}

# Target: ErgativeSystem — ERG groups {A only};  ABS groups {S+P}
# Spread S/P apart at mid-level; ERG right, ABS left-bottom.
_ERG_POSITIONS: dict[str, tuple[float, float]] = {
    "A":   (0.85, 0.90),
    "S":   (0.15, 0.60),
    "P":   (0.85, 0.60),
    "ERG": (0.85, 0.30),
    "ABS": (0.15, 0.02),
}

# Intra-category edges (within each panel)
_ACC_EDGES = [
    ("S",   "NOM", "→NOM"),
    ("A",   "NOM", "→NOM"),
    ("NOM", "ACC", "trans"),
    ("P",   "ACC", "→ACC"),
]
_ERG_EDGES = [
    ("A",   "ERG", "→ERG"),
    ("S",   "ABS", "→ABS"),
    ("P",   "ABS", "→ABS"),
    ("ERG", "ABS", "trans"),
]

_NODE_RADIUS = 0.085


def render_functor_diagram(
    functor: AlignmentFunctor,
    output_path: Optional[Path] = None,
    title: Optional[str] = None,
) -> matplotlib.figure.Figure:
    """Render an alignment functor as two side-by-side category diagrams.

    Source category on the left (Accusative), target on the right (Ergative).
    Node positions are fixed hierarchically; functor arrows are drawn as
    straight dashed lines between the two axes using ConnectionPatch.

    Args:
        functor: The alignment functor to visualize.
        output_path: Optional path to save the figure.
        title: Optional title override.

    Returns:
        The matplotlib Figure object.
    """
    fig = plt.figure(figsize=(20, 10), facecolor="white")

    # Three columns: source panel | functor labels | target panel
    gs = fig.add_gridspec(
        1, 3, width_ratios=[5, 1.4, 5],
        left=0.03, right=0.97, top=0.88, bottom=0.05,
        wspace=0.0,
    )
    ax_src = fig.add_subplot(gs[0])
    ax_mid = fig.add_subplot(gs[1])
    ax_tgt = fig.add_subplot(gs[2])

    for ax in (ax_src, ax_mid, ax_tgt):
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.12, 1.02)
        ax.axis("off")

    # ── Draw each category panel ──────────────────────────────────────────
    _draw_category_panel(
        ax_src,
        positions=_ACC_POSITIONS,
        edges=_ACC_EDGES,
        panel_title="$\\mathcal{C}_{\\mathrm{acc}}$  (Accusative)",
        highlight_groups=[
            (["S", "A", "NOM"], "#DBEAFE", "NOM groups S & A"),
            (["P", "ACC"], "#FEE2E2", "ACC groups P"),
        ],
    )
    _draw_category_panel(
        ax_tgt,
        positions=_ERG_POSITIONS,
        edges=_ERG_EDGES,
        panel_title="$\\mathcal{C}_{\\mathrm{erg}}$  (Ergative)",
        highlight_groups=[
            (["A", "ERG"], "#F3E8FF", "ERG groups A"),
            (["S", "P", "ABS"], "#CCFBF1", "ABS groups S & P"),
        ],
    )

    # ── Draw functor arrows (cross-axes ConnectionPatch) ──────────────────
    # Unique canonical mappings: NOM→ERG, ACC→ABS, S→ABS, A→ERG, P→ABS
    functor_pairs = [
        ("S",   _ACC_POSITIONS["S"],   "S",   _ERG_POSITIONS["S"],   "F(S)=ABS"),
        ("A",   _ACC_POSITIONS["A"],   "A",   _ERG_POSITIONS["A"],   "F(A)=ERG"),
        ("NOM", _ACC_POSITIONS["NOM"], "ERG", _ERG_POSITIONS["ERG"], "F(NOM)=ERG"),
        ("P",   _ACC_POSITIONS["P"],   "ABS", _ERG_POSITIONS["ABS"], "F(P)=ABS"),
        ("ACC", _ACC_POSITIONS["ACC"], "ABS", _ERG_POSITIONS["ABS"], "F(ACC)=ABS"),
    ]

    for src_name, (sx, sy), tgt_name, (tx, ty), label in functor_pairs:
        con = mpatches.ConnectionPatch(
            xyA=(sx, sy), coordsA=ax_src.transData,
            xyB=(tx, ty), coordsB=ax_tgt.transData,
            arrowstyle="->,head_width=10,head_length=10",
            color=COLOR_FUNCTOR_ARROW,
            linewidth=2.2,
            linestyle="dashed",
            mutation_scale=18,
            zorder=12,
        )
        fig.add_artist(con)

    # ── Middle column: functor label and arrows list ──────────────────────
    ax_mid.text(
        0.5, 0.92, "$F$", fontsize=26, ha="center", va="top",
        fontweight="bold", color=COLOR_FUNCTOR_ARROW,
        transform=ax_mid.transAxes,
    )
    ax_mid.text(
        0.5, 0.80, "$\\longrightarrow$", fontsize=22, ha="center", va="top",
        color=COLOR_FUNCTOR_ARROW, transform=ax_mid.transAxes,
    )
    mapping_lines = [
        "S $\\mapsto$ ABS",
        "A $\\mapsto$ ERG",
        "P $\\mapsto$ ABS",
        "NOM $\\mapsto$ ERG",
        "ACC $\\mapsto$ ABS",
    ]
    for i, line in enumerate(mapping_lines):
        ax_mid.text(
            0.5, 0.62 - i * 0.12, line, fontsize=13, ha="center", va="top",
            color=COLOR_FUNCTOR_ARROW, transform=ax_mid.transAxes,
            fontstyle="italic",
        )

    # Neutralization note
    ax_mid.text(
        0.5, 0.00,
        mathtext_safe_arrows("Non-injective:\nS,P → ABS"),
        fontsize=11, ha="center", va="bottom",
        color="#BE185D", transform=ax_mid.transAxes,
        style="italic",
    )

    # ── Figure title and annotation ──────────────────────────────────────
    display_title = title or (
        r"Alignment Functor $F: \mathcal{C}_{\mathrm{acc}} \to \mathcal{C}_{\mathrm{erg}}$"
        "\n"
        r"Accusative $\to$ Ergative: $\{S,A\} \to \mathrm{NOM}$ vs $\{S,P\} \to \mathrm{ABS}$"
    )
    fig.suptitle(
        mathtext_safe_arrows(display_title), fontsize=FONT_SIZE_TITLE,
        fontweight="bold", y=0.97, color=COLOR_TEXT,
    )

    if output_path:
        fig.savefig(
            output_path, dpi=FIGURE_DPI,
            bbox_inches="tight", facecolor="white",
        )
        logger.info("Saved functor diagram to %s", output_path)

    return fig


def _draw_category_panel(
    ax: plt.Axes,
    positions: dict[str, tuple[float, float]],
    edges: list[tuple[str, str, str]],
    panel_title: str,
    highlight_groups: list[tuple[list[str], str, str]],
) -> None:
    """Draw a single category as nodes + edges with background grouping.

    Args:
        ax: Target axes.
        positions: Dict mapping role name to (x, y) in [0,1] data coords.
        edges: List of (source_name, target_name, label).
        panel_title: Title of the panel.
        highlight_groups: List of (node_names, fill_color, group_label).
    """
    r = _NODE_RADIUS

    # ── Background grouping halos ─────────────────────────────────────────
    for group_names, fill_color, group_label in highlight_groups:
        pts = [positions[n] for n in group_names if n in positions]
        if not pts:
            continue
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        cx, cy = np.mean(xs), np.mean(ys)
        halo_r = (
            max(
                max(abs(x - cx) for x in xs),
                max(abs(y - cy) for y in ys),
            ) + r * 1.8
        )
        halo = plt.Circle(
            (cx, cy), halo_r,
            color=fill_color, zorder=0, alpha=0.55,
        )
        ax.add_patch(halo)
        ax.text(
            cx, cy - halo_r - 0.02, group_label,
            ha="center", va="top",
            fontsize=FONT_SIZE_FLOOR - 5,
            color="#374151", style="italic",
        )

    # ── Intra-category edges ──────────────────────────────────────────────
    for src_name, tgt_name, label in edges:
        if src_name not in positions or tgt_name not in positions:
            continue
        sx, sy = positions[src_name]
        tx, ty = positions[tgt_name]

        # Offset endpoints to node boundary
        dx, dy = tx - sx, ty - sy
        dist = max(np.hypot(dx, dy), 1e-9)
        dx_n, dy_n = dx / dist, dy / dist

        start_x = sx + dx_n * r
        start_y = sy + dy_n * r
        end_x = tx - dx_n * r
        end_y = ty - dy_n * r

        ax.annotate(
            "",
            xy=(end_x, end_y), xytext=(start_x, start_y),
            arrowprops=dict(
                arrowstyle="->,head_width=0.5,head_length=0.5",
                color=COLOR_EDGE, lw=1.8,
                connectionstyle="arc3,rad=0.18",
            ),
            zorder=3,
        )

    # ── Nodes ──────────────────────────────────────────────────────────────
    for name, (x, y) in positions.items():
        color = CASE_COLORS.get(name, COLOR_NEUTRAL)
        circle = plt.Circle((x, y), r, color=color, zorder=5)
        ax.add_patch(circle)
        # White ring border
        ring = plt.Circle(
            (x, y), r, fill=False,
            edgecolor="white", linewidth=2.5, zorder=6,
        )
        ax.add_patch(ring)
        ax.text(
            x, y, name, ha="center", va="center",
            fontsize=FONT_SIZE_LABEL, fontweight="bold",
            color="white", zorder=7,
        )

    ax.set_title(
        panel_title, fontsize=FONT_SIZE_LABEL + 2,
        fontweight="bold", pad=10, color=COLOR_TEXT,
    )
    ax.set_aspect("equal")
    ax.set_xlim(-0.15, 1.15)
    ax.set_ylim(-0.25, 1.10)
