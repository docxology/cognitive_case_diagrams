"""Cognitive security visualization.

Bar chart of ``TypeViolation`` severities with colour bands (high / medium / low).
"""
from __future__ import annotations

import logging
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from ..security.cognitive_security import TypeViolation
from .styles import (
    FONT_SIZE_FLOOR, FONT_SIZE_TITLE, FONT_SIZE_LABEL,
    DEFAULT_FIGSIZE, FIGURE_DPI,
    COLOR_SEVERITY_HIGH, COLOR_SEVERITY_MED, COLOR_SEVERITY_LOW,
    SEVERITY_HIGH_THRESHOLD, SEVERITY_MED_THRESHOLD,
    BAR_WIDTH_WIDE, BAR_ALPHA,
    mathtext_safe_arrows,
)

logger = logging.getLogger(__name__)


def plot_type_violations(
    violations: list[TypeViolation],
    title: str = "Case Frame Type Violations",
    output_path: Optional[str] = None,
) -> str:
    """Plot severity and confidence of detected type violations.

    Args:
        violations: List of TypeViolation objects.
        title: Title of the plot.
        output_path: Path to save the figure.

    Returns:
        The output path where the figure was saved.
    """
    if not violations:
        logger.warning("No violations to plot.")
        return ""

    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE, dpi=FIGURE_DPI)

    sorted_violations = sorted(violations, key=lambda v: v.severity, reverse=True)

    labels = [
        mathtext_safe_arrows(
            f"{v.source.name} → {v.target.name}\n({v.violation_type})"
        )
        for v in sorted_violations
    ]
    severities = [v.severity for v in sorted_violations]

    x = np.arange(len(labels))
    width = BAR_WIDTH_WIDE

    colors = [
        COLOR_SEVERITY_HIGH if s >= SEVERITY_HIGH_THRESHOLD
        else COLOR_SEVERITY_MED if s >= SEVERITY_MED_THRESHOLD
        else COLOR_SEVERITY_LOW
        for s in severities
    ]

    ax.bar(x, severities, width, color=colors, alpha=BAR_ALPHA, edgecolor="black")

    ax.set_ylabel("Severity Score", fontsize=FONT_SIZE_LABEL)
    ax.set_ylim(0, 1.05)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=FONT_SIZE_FLOOR, rotation=15)
    ax.set_title(title, fontsize=FONT_SIZE_TITLE)

    legend_handles = [
        Patch(
            facecolor=COLOR_SEVERITY_HIGH,
            edgecolor="black",
            alpha=BAR_ALPHA,
            label=f"high (≥ {SEVERITY_HIGH_THRESHOLD:g})",
        ),
        Patch(
            facecolor=COLOR_SEVERITY_MED,
            edgecolor="black",
            alpha=BAR_ALPHA,
            label=f"medium ({SEVERITY_MED_THRESHOLD:g}–{SEVERITY_HIGH_THRESHOLD:g})",
        ),
        Patch(
            facecolor=COLOR_SEVERITY_LOW,
            edgecolor="black",
            alpha=BAR_ALPHA,
            label=f"low (< {SEVERITY_MED_THRESHOLD:g})",
        ),
    ]
    ax.legend(
        handles=legend_handles,
        title="Severity band",
        loc="upper right",
        fontsize=FONT_SIZE_FLOOR - 2,
        title_fontsize=FONT_SIZE_FLOOR - 2,
        framealpha=0.92,
    )

    plt.tight_layout()

    if output_path is None:
        output_path = "type_violations.png"
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved type violation plot to %s", output_path)

    return output_path


def plot_case_interaction_graph(
    output_path: Optional[str] = None,
) -> str:
    """Render a two-panel case interaction graph for §9b.

    Panel 1 (top): legitimate NOM→INS→ACC→DAT trace (commutes, ✓).
    Panel 2 (bottom): same trace plus the illicit ACC→INS arc (φ, ✗).

    Args:
        output_path: Path to save the PNG.

    Returns:
        The output path.
    """
    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(10, 7), dpi=FIGURE_DPI)
    fig.patch.set_facecolor("white")

    nodes = ["User\n(NOM)", "Model\n(INS)", "Webpage\n(ACC)", "Output\n(DAT)"]
    edge_labels = ["$f_{\\mathrm{request}}$", "$g_{\\mathrm{summarize}}$", "$h_{\\mathrm{deliver}}$"]
    xs = [0.1, 0.37, 0.63, 0.9]
    y_mid = 0.5

    def _draw_nodes(ax: plt.Axes, highlight_idx: Optional[int] = None) -> None:
        for i, (x, label) in enumerate(zip(xs, nodes)):
            color = COLOR_SEVERITY_HIGH if i == highlight_idx else "#4f8ef7"
            ax.scatter(x, y_mid, s=800, color=color, zorder=5,
                       edgecolors="#222", lw=1.8)
            ax.text(x, y_mid - 0.18, label, ha="center", va="top",
                    fontsize=FONT_SIZE_FLOOR, fontweight="bold", color="#1a1a1a")

    def _draw_main_edges(ax: plt.Axes) -> None:
        for i, lbl in enumerate(edge_labels):
            x0, x1 = xs[i], xs[i + 1]
            ax.annotate("", xy=(x1 - 0.03, y_mid), xytext=(x0 + 0.03, y_mid),
                        arrowprops=dict(arrowstyle="->", color="#222222", lw=1.8))
            ax.text((x0 + x1) / 2, y_mid + 0.12, lbl,
                    ha="center", va="bottom", fontsize=FONT_SIZE_FLOOR - 1,
                    color="#333333")

    # ── Panel 1: legitimate trace ─────────────────────────────────────────────
    for ax in (ax_top, ax_bot):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_facecolor("white")
        ax.axis("off")

    _draw_main_edges(ax_top)
    _draw_nodes(ax_top)
    ax_top.text(0.97, 0.92, "✓", fontsize=22, color="#16a34a", ha="right", va="top",
                fontweight="bold")
    ax_top.set_title("Legitimate Interaction — diagram commutes",
                     fontsize=FONT_SIZE_LABEL, pad=8, color="#16a34a")

    # ── Panel 2: injection attempt ────────────────────────────────────────────
    _draw_main_edges(ax_bot)
    _draw_nodes(ax_bot, highlight_idx=2)  # highlight ACC node in red

    # Illicit arc: Webpage(ACC) → Model(INS), dashed red arc above
    ax_bot.annotate(
        "",
        xy=(xs[1] + 0.03, y_mid + 0.04),
        xytext=(xs[2] - 0.03, y_mid + 0.04),
        arrowprops=dict(
            arrowstyle="->", color=COLOR_SEVERITY_HIGH, lw=2.2,
            linestyle="dashed",
            connectionstyle="arc3,rad=-0.45",
        ),
    )
    ax_bot.text(
        (xs[1] + xs[2]) / 2, y_mid + 0.42,
        mathtext_safe_arrows("φ: ACC→INS  (illicit promotion)"),
        ha="center", va="bottom", fontsize=FONT_SIZE_FLOOR - 1,
        color=COLOR_SEVERITY_HIGH, fontstyle="italic",
    )
    ax_bot.text(0.97, 0.92, "✗", fontsize=22, color=COLOR_SEVERITY_HIGH,
                ha="right", va="top", fontweight="bold")
    ax_bot.text(
        0.5, 0.04,
        mathtext_safe_arrows("ACC→NOM: type violation — diagram does not commute"),
        ha="center", va="bottom", fontsize=FONT_SIZE_FLOOR - 1,
        color=COLOR_SEVERITY_HIGH, fontweight="bold",
        bbox=dict(boxstyle="round", facecolor="#fff3f3",
                  edgecolor=COLOR_SEVERITY_HIGH, alpha=0.9),
    )
    ax_bot.set_title("Prompt Injection — fails type check",
                     fontsize=FONT_SIZE_LABEL, pad=8, color=COLOR_SEVERITY_HIGH)

    fig.tight_layout(pad=1.5)

    if output_path is None:
        output_path = "security_type_violations.png"
    fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    logger.info("Saved case interaction graph to %s", output_path)
    return output_path


def plot_monoidal_functor_security(
    functor,
    title: str = "MonoidalFunctor tensor check (§9b)",
    output_path: Optional[str] = None,
) -> str:
    """Render a dual-panel figure for the §9b protocol narrative (specification-level).

    Panel 1 (left): Bipartite object-map graph F: source roles → target roles.
        The adversarial ACC→NOM promotion edge is highlighted in red (blocked).
    Panel 2 (right): Tensor-preservation truth table: F(A⊗B) ≅ F(A)⊗F(B)?
        Green = preserved; Red = tensor check fails (illicit role merge; §9b story).

    While this figure is built, ``functor.preserves_tensor`` may emit INFO/WARNING lines
    from ``src.case_systems.functor`` (e.g. tensor preservation failures). That output is
    expected diagnostic narrative for the plot, not a pipeline fault.

    Args:
        functor: MonoidalFunctor instance exposing .object_map and .preserves_tensor().
        title: Suptitle of the figure.
        output_path: Path to save the PNG.

    Returns:
        The output path.
    """
    from ..case_systems.case_category import CaseRole

    source_roles = list(functor.object_map.keys())
    target_roles = list(dict.fromkeys(functor.object_map.values()))

    fig, (ax_map, ax_tensor) = plt.subplots(1, 2, figsize=(16, 7), dpi=FIGURE_DPI)
    fig.patch.set_facecolor("white")

    # ── Panel 1: Bipartite object-map ──────────────────────────────────────────
    ax_map.set_xlim(0, 1)
    ax_map.set_ylim(0, 1)
    ax_map.set_facecolor("white")
    ax_map.set_aspect("equal")
    ax_map.axis("off")

    n_src = len(source_roles)
    n_tgt = len(target_roles)
    # Reserve the bottom ~18% of the axes for the §9b narrative annotation
    # so the last-row node labels don't collide with it.
    src_ys = np.linspace(0.22, 0.92, n_src)
    tgt_ys = np.linspace(0.22, 0.92, n_tgt)
    tgt_pos = {r: (0.75, tgt_ys[i]) for i, r in enumerate(target_roles)}
    src_pos = {r: (0.25, src_ys[i]) for i, r in enumerate(source_roles)}

    # Draw edges
    for src_role, tgt_role in functor.object_map.items():
        is_blocked = (src_role == CaseRole.ACC and tgt_role == CaseRole.NOM)
        color = COLOR_SEVERITY_HIGH if is_blocked else "#555555"
        lw = 2.5 if is_blocked else 1.2
        ls = "--" if is_blocked else "-"
        x0, y0 = src_pos[src_role]
        x1, y1 = tgt_pos[tgt_role]
        ax_map.annotate(
            "",
            xy=(x1, y1), xytext=(x0, y0),
            arrowprops=dict(
                arrowstyle="->", color=color, lw=lw, linestyle=ls,
                connectionstyle="arc3,rad=0.08",
            ),
        )

    # Draw source nodes
    for role, (x, y) in src_pos.items():
        ax_map.scatter(x, y, s=400, color="#4f8ef7", zorder=5, edgecolors="#222", lw=1.5)
        ax_map.text(x - 0.06, y, role.name, fontsize=FONT_SIZE_FLOOR,
                    ha="right", va="center", fontweight="bold", color="#1a1a1a")

    # Draw target nodes
    for role, (x, y) in tgt_pos.items():
        ax_map.scatter(x, y, s=400, color="#e53935", zorder=5, edgecolors="#222", lw=1.5)
        ax_map.text(x + 0.06, y, role.name, fontsize=FONT_SIZE_FLOOR,
                    ha="left", va="center", fontweight="bold", color="#1a1a1a")

    ax_map.text(0.25, 0.98, "Source", fontsize=FONT_SIZE_LABEL, ha="center",
                va="top", fontweight="bold", color="#4f8ef7")
    ax_map.text(0.75, 0.98, "Target", fontsize=FONT_SIZE_LABEL, ha="center",
                va="top", fontweight="bold", color="#e53935")
    ax_map.set_title(
        mathtext_safe_arrows("Object Map  F: C → D"),
        fontsize=FONT_SIZE_LABEL,
        pad=10,
    )

    # §9b narrative annotation (protocol-level type violation); kept on a
    # single line and seated in the reserved 0–18 % band so it does not
    # collide with the lowest source/target node labels.
    ax_map.text(0.5, 0.06,
                mathtext_safe_arrows(
                    "ACC → NOM: type violation  —  non-cartesian merge (§9b)"
                ),
                fontsize=FONT_SIZE_FLOOR - 2, ha="center", va="center",
                color=COLOR_SEVERITY_HIGH, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#fff3f3",
                          edgecolor=COLOR_SEVERITY_HIGH, alpha=0.95))

    # ── Panel 2: Tensor-preservation truth table ───────────────────────────────
    core_roles = [r for r in CaseRole if r in functor.object_map]
    n = len(core_roles)
    table = np.zeros((n, n))
    annotations = []
    for i, ra in enumerate(core_roles):
        row_ann = []
        for j, rb in enumerate(core_roles):
            try:
                ok = functor.preserves_tensor(ra, rb)
            except (KeyError, ValueError):
                ok = True
            table[i, j] = 1.0 if ok else 0.0
            row_ann.append(mathtext_safe_arrows("✓" if ok else "✗"))
        annotations.append(row_ann)

    # Colorblind-safe: amber = fails, blue = preserved (avoids red/green)
    cmap_tt = plt.matplotlib.colors.ListedColormap(["#D97706", "#2563EB"])
    ax_tensor.imshow(table, cmap=cmap_tt, vmin=0, vmax=1, aspect="auto")

    role_names = [r.name for r in core_roles]
    ax_tensor.set_xticks(range(n))
    ax_tensor.set_yticks(range(n))
    ax_tensor.set_xticklabels(role_names, fontsize=FONT_SIZE_FLOOR, rotation=30, ha="right")
    ax_tensor.set_yticklabels(role_names, fontsize=FONT_SIZE_FLOOR)
    ax_tensor.set_xlabel("Role B", fontsize=FONT_SIZE_LABEL)
    ax_tensor.set_ylabel("Role A", fontsize=FONT_SIZE_LABEL)
    ax_tensor.set_title(
        r"Tensor Preservation: $F(A \otimes B) \cong F(A) \otimes F(B)$?",
        fontsize=FONT_SIZE_LABEL, pad=10,
    )

    for i in range(n):
        for j in range(n):
            color = "white"
            ax_tensor.text(j, i, annotations[i][j], ha="center", va="center",
                           fontsize=FONT_SIZE_LABEL, fontweight="bold", color=color)

    legend_handles = [
        Patch(facecolor="#2563EB", label="Preserved (safe)"),
        Patch(facecolor="#D97706", label="Tensor check fails (§9b)"),
    ]
    ax_tensor.legend(handles=legend_handles, loc="lower right",
                     fontsize=FONT_SIZE_FLOOR - 1, framealpha=0.95)

    fig.suptitle(title, fontsize=FONT_SIZE_TITLE + 1, fontweight="bold", y=1.01)
    fig.tight_layout()

    if output_path is None:
        output_path = "monoidal_functor_security.png"
    fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    logger.info("Saved MonoidalFunctor security plot to %s", output_path)
    return output_path
