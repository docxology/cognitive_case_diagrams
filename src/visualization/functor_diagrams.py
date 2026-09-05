"""Alignment functor diagram visualizations.

Renders side-by-side publication-quality category diagrams representing
source (Accusative) and target (Ergative) alignment systems, with explicit
fixed-position hierarchical node layouts and clean functor arrows.

Figure 17 of the manuscript: F: C_acc → C_erg

Layout uses **one shared matplotlib Axes** with two disjoint x-ranges (left and
right panels). Functor arrows are ``FancyArrowPatch`` curves in the same data
coordinate system, so endpoints stay on node circles under ``set_aspect("equal")``
and tight bounding-box export.
"""
from __future__ import annotations

import logging
from collections import defaultdict
from typing import Optional

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from ..case_systems.case_category import CaseRole
from ..case_systems.functor import AlignmentFunctor
from .styles import (
    CASE_COLORS, FONT_SIZE_FLOOR, FONT_SIZE_TITLE, FONT_SIZE_LABEL,
    FIGURE_DPI, COLOR_FUNCTOR_ARROW, COLOR_TEXT, COLOR_NEUTRAL,
    COLOR_EDGE,
    mathtext_safe_arrows,
)

logger = logging.getLogger(__name__)

# ─── World x-ranges (single shared Axes): left panel | gap | right panel ───
# Template coords 0–1 are placed inside each panel; gap holds functor notation.
_PANEL_LEFT_X0 = 0.0
_PANEL_LEFT_X1 = 1.0
_PANEL_RIGHT_X0 = 1.58
_PANEL_RIGHT_X1 = 2.58
_FUNCTOR_COLUMN_X = (_PANEL_LEFT_X1 + _PANEL_RIGHT_X0) / 2.0

# ─── Fixed node positions (template 0–1 within each panel) ────────────────
# Source: AccusativeSystem  — NOM groups {S,A};  ACC groups {P}
# Semantic roles aligned at y=0.85 across both panels.
_ACC_POSITIONS: dict[str, tuple[float, float]] = {
    "A":   (0.20, 0.85),
    "S":   (0.50, 0.85),
    "P":   (0.80, 0.85),
    "NOM": (0.35, 0.20),
    "ACC": (0.80, 0.20),
}

# Target: ErgativeSystem — ERG groups {A only};  ABS groups {S+P}
_ERG_POSITIONS: dict[str, tuple[float, float]] = {
    "A":   (0.20, 0.85),
    "S":   (0.50, 0.85),
    "P":   (0.80, 0.85),
    "ERG": (0.20, 0.20),
    "ABS": (0.65, 0.20),
}

# Intra-category edges (within each panel)
_ACC_EDGES = [
    ("A",   "NOM", "→NOM"),
    ("S",   "NOM", "→NOM"),
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
# Separate multiple functor arrows that share a target node (data coordinates).
_STAGGER_FUNCTOR_TARGET_X = 0.042


def _template_to_world(
    template: dict[str, tuple[float, float]],
    panel_x0: float,
) -> dict[str, tuple[float, float]]:
    """Map 0–1 template positions to world x by shifting panel origin."""
    return {name: (panel_x0 + xy[0], xy[1]) for name, xy in template.items()}


def _trim_segment_endpoints(
    sx: float, sy: float, tx: float, ty: float, r: float
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Return start/end on the segment inset by ``r`` from each endpoint."""
    dx, dy = tx - sx, ty - sy
    dist = max(float(np.hypot(dx, dy)), 1e-9)
    dx_n, dy_n = dx / dist, dy / dist
    start = (sx + dx_n * r, sy + dy_n * r)
    end = (tx - dx_n * r, ty - dy_n * r)
    return start, end


def _stagger_offsets_x(n: int, step: float = _STAGGER_FUNCTOR_TARGET_X) -> list[float]:
    """Symmetric horizontal offsets for ``n`` coincident targets."""
    if n <= 1:
        return [0.0]
    mid = (n - 1) / 2.0
    return [(i - mid) * step for i in range(n)]


def _target_stagger_by_pair(
    functor: AlignmentFunctor,
) -> dict[tuple[str, str], float]:
    """Map (target_role_name, source_role_name) -> x-offset at target."""
    by_tgt: dict[str, list[CaseRole]] = defaultdict(list)
    for src, tgt in functor.object_map.items():
        by_tgt[tgt.name].append(src)
    out: dict[tuple[str, str], float] = {}
    for tgt_name, srcs in by_tgt.items():
        srcs_sorted = sorted(srcs, key=lambda s: s.name)
        offsets = _stagger_offsets_x(len(srcs_sorted))
        for src, off in zip(srcs_sorted, offsets):
            out[(tgt_name, src.name)] = off
    return out


def render_functor_diagram(
    functor: AlignmentFunctor,
    output_path: Optional[str] = None,
    title: Optional[str] = None,
) -> matplotlib.figure.Figure:
    """Render an alignment functor as two side-by-side category diagrams.

    Source category on the left (Accusative), target on the right (Ergative).
    Both panels share one Axes with disjoint x-ranges; purple functor arrows
    follow ``functor.object_map`` as dashed ``FancyArrowPatch`` curves (endpoints
    trimmed to node circles; coincident targets are staggered).

    Args:
        functor: The alignment functor to visualize (object map drives arrows).
        output_path: Optional path to save the figure.
        title: Optional title override.

    Returns:
        The matplotlib Figure object.
    """
    fig = plt.figure(figsize=(20, 10), facecolor="white")
    ax = fig.add_axes((0.04, 0.10, 0.92, 0.78))

    left_pos = _template_to_world(_ACC_POSITIONS, _PANEL_LEFT_X0)
    right_pos = _template_to_world(_ERG_POSITIONS, _PANEL_RIGHT_X0)

    ax.set_xlim(-0.12, _PANEL_RIGHT_X1 + 0.12)
    ax.set_ylim(-0.22, 1.14)
    ax.axis("off")

    # Subtle panel backgrounds (caption: blue vs amber panels)
    ax.axvspan(
        _PANEL_LEFT_X0 - 0.04, _PANEL_LEFT_X1 + 0.04,
        facecolor="#EFF6FF", zorder=0, alpha=0.65, linewidth=0,
    )
    ax.axvspan(
        _PANEL_RIGHT_X0 - 0.04, _PANEL_RIGHT_X1 + 0.04,
        facecolor="#FFFBEB", zorder=0, alpha=0.7, linewidth=0,
    )

    _draw_category_panel(
        ax,
        positions=left_pos,
        edges=_ACC_EDGES,
        panel_title="$\\mathcal{C}_{\\mathrm{acc}}$  (Accusative)",
        highlight_groups=[
            (["S", "A", "NOM"], "#DBEAFE", "NOM groups S & A"),
            (["P", "ACC"], "#FEE2E2", "ACC groups P"),
        ],
    )
    _draw_category_panel(
        ax,
        positions=right_pos,
        edges=_ERG_EDGES,
        panel_title="$\\mathcal{C}_{\\mathrm{erg}}$  (Ergative)",
        highlight_groups=[
            (["A", "ERG"], "#F3E8FF", "ERG groups A"),
            (["S", "P", "ABS"], "#CCFBF1", "ABS groups S & P"),
        ],
    )

    # Functor arrows (single coordinate system — no cross-subplot transform drift)
    stagger = _target_stagger_by_pair(functor)
    for src_role, tgt_role in sorted(
        functor.object_map.items(),
        key=lambda kv: (kv[1].name, kv[0].name),
    ):
        src_name = src_role.name
        tgt_name = tgt_role.name
        if src_name not in left_pos or tgt_name not in right_pos:
            logger.warning(
                "Skipping functor arrow %s→%s: missing layout position",
                src_name,
                tgt_name,
            )
            continue
        cx, cy = right_pos[tgt_name]
        off_x = stagger.get((tgt_name, src_name), 0.0)
        tx, ty = cx + off_x, cy
        sx, sy = left_pos[src_name]
        xy_a, xy_b = _trim_segment_endpoints(sx, sy, tx, ty, _NODE_RADIUS)
        vert_span = abs(sy - ty)
        rad = 0.11 if vert_span > 0.45 else 0.045
        arrow = mpatches.FancyArrowPatch(
            xy_a,
            xy_b,
            arrowstyle="->",
            connectionstyle=f"arc3,rad={rad}",
            color=COLOR_FUNCTOR_ARROW,
            linewidth=2.2,
            linestyle="--",
            mutation_scale=18,
            zorder=12,
            shrinkA=0,
            shrinkB=0,
        )
        ax.add_patch(arrow)

    # Functor column (data coords, centered in gap)
    xc = _FUNCTOR_COLUMN_X
    ax.text(
        xc, 0.94, "$F$", fontsize=26, ha="center", va="top",
        fontweight="bold", color=COLOR_FUNCTOR_ARROW,
    )
    ax.text(
        xc, 0.84, "$\\longrightarrow$", fontsize=22, ha="center", va="top",
        color=COLOR_FUNCTOR_ARROW,
    )
    mapping_lines = [
        f"{src.name} $\\mapsto$ {tgt.name}"
        for src, tgt in sorted(
            functor.object_map.items(), key=lambda kv: kv[0].name
        )
    ]
    for i, line in enumerate(mapping_lines):
        ax.text(
            xc, 0.72 - i * 0.095, line, fontsize=13, ha="center", va="top",
            color=COLOR_FUNCTOR_ARROW, fontstyle="italic",
        )

    ax.text(
        xc, -0.06,
        mathtext_safe_arrows("Non-injective:\nS,P → ABS"),
        fontsize=11, ha="center", va="top",
        color="#BE185D", style="italic",
    )

    ax.set_aspect("equal")

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
        ax: Target axes (shared across both panels).
        positions: Dict mapping role name to (x, y) in world data coords.
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
        cx, cy = float(np.mean(xs)), float(np.mean(ys))
        halo_r = (
            max(
                max(abs(x - cx) for x in xs),
                max(abs(y - cy) for y in ys),
            ) + r * 1.8
        )
        halo = plt.Circle(
            (cx, cy), halo_r,
            color=fill_color, zorder=1, alpha=0.55,
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

    xs_p = [positions[k][0] for k in positions]
    cx_title = float(np.mean(xs_p)) if xs_p else 0.5
    ax.text(
        cx_title, 1.08, panel_title,
        fontsize=FONT_SIZE_LABEL + 2,
        fontweight="bold", ha="center", va="bottom", color=COLOR_TEXT,
    )
