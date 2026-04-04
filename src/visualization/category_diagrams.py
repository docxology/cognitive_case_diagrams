"""Category diagram visualizations using matplotlib and networkx.

Renders case categories as directed graphs, alignment comparisons,
and composition triangles for the manuscript figures.
"""

import logging
from pathlib import Path
from typing import Optional, Union

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx

from ..case_systems.case_category import CaseCategory, CaseRole, Morphism
from .styles import (
    CASE_COLORS, FONT_SIZE_FLOOR, FONT_SIZE_TITLE, FONT_SIZE_LABEL,
    DEFAULT_FIGSIZE, COMPARISON_FIGSIZE, SQUARE_FIGSIZE, FIGURE_DPI,
    COLOR_EDGE, COLOR_TEXT, COLOR_NEUTRAL,
    mathtext_safe_arrows,
)

logger = logging.getLogger(__name__)

# Default structurally prohibited transitions (drawn only if both roles exist).
DEFAULT_STRUCTURAL_PROHIBITIONS: list[tuple[CaseRole, CaseRole, str]] = [
    (CaseRole.VOC, CaseRole.NOM, mathtext_safe_arrows("vocative→agent")),
    (CaseRole.LOC, CaseRole.ACC, mathtext_safe_arrows("spatial→patient")),
    (CaseRole.ABL, CaseRole.DAT, mathtext_safe_arrows("source→goal")),
]


def _prohibited_edges_to_draw(
    node_names: set[str],
    extra: Optional[list[tuple[CaseRole, CaseRole, str]]] = None,
) -> list[tuple[str, str, str]]:
    """Merge default and extra prohibited edges, deduplicated by (source, target)."""
    out: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()
    for src, tgt, label in DEFAULT_STRUCTURAL_PROHIBITIONS:
        if src.name in node_names and tgt.name in node_names:
            key = (src.name, tgt.name)
            if key not in seen:
                seen.add(key)
                out.append((src.name, tgt.name, label))
    if extra:
        for src, tgt, label in extra:
            if src.name in node_names and tgt.name in node_names:
                key = (src.name, tgt.name)
                if key not in seen:
                    seen.add(key)
                    out.append((src.name, tgt.name, label))
    return out


def _get_color(role: CaseRole) -> str:
    """Get the palette color for a case role."""
    return CASE_COLORS.get(role.name, COLOR_NEUTRAL)


def render_case_category(
    category: CaseCategory,
    output_path: Optional[Path] = None,
    title: Optional[str] = None,
    show_admissibility: bool = True,
    extra_prohibited: Optional[list[tuple[CaseRole, CaseRole, str]]] = None,
    figsize: Optional[tuple[float, float]] = None,
    node_positions: Optional[dict[str, tuple[float, float]]] = None,
    edge_label_prefix: Optional[dict[tuple[str, str], str]] = None,
    licensed_connectionstyle: Union[str, dict[tuple[str, str], str], None] = None,
) -> matplotlib.figure.Figure:
    """Render a case category as a directed graph with admissibility.

    Objects (case roles) are nodes. By default layout is circular; pass
    *node_positions* for a fixed planar layout (keys must cover every node).
    Licensed morphisms shown as solid green directed edges with ✓ and weight.
    Prohibited morphisms shown as dashed red directed edges with ✗.

    Default prohibited transitions (VOC→NOM, LOC→ACC, ABL→DAT) are drawn only
    when both endpoint roles appear in *category*. Additional prohibited pairs
    may be supplied via *extra_prohibited* (same filtering and deduplication).

    Args:
        category: The case category to render.
        output_path: Optional path to save the figure.
        title: Optional title override.
        show_admissibility: If True, overlay admissibility annotations.
        extra_prohibited: Optional (source, target, label) prohibited edges.
        figsize: Optional ``(width, height)`` inches; default ``(12, 10)``.
        node_positions: Optional mapping node name → (x, y) in layout space.
        edge_label_prefix: Optional (source, target) → text prepended to licensed
            edge labels (e.g. morphism symbols ``f:``, ``h=g∘f:``).
        licensed_connectionstyle: Optional NetworkX ``connectionstyle`` string
            for all licensed edges, or per-edge dict; default ``arc3,rad=0.12``.

    Returns:
        The matplotlib Figure object.
    """
    import matplotlib.patches as mpatches

    size = figsize if figsize is not None else (12, 10)
    fig, ax = plt.subplots(1, 1, figsize=size)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    G = nx.DiGraph()
    roles = sorted(category.objects, key=lambda r: r.name)
    for role in roles:
        G.add_node(role.name)

    for morph in category.morphisms:
        G.add_edge(morph.source.name, morph.target.name,
                   label=morph.label, weight=morph.weight)

    node_names = set(G.nodes())
    prohibited_morphisms = _prohibited_edges_to_draw(node_names, extra_prohibited)

    if node_positions is not None:
        missing = node_names - set(node_positions.keys())
        if missing:
            raise ValueError(
                "node_positions must include every graph node; missing: "
                + ", ".join(sorted(missing))
            )
        pos = {n: node_positions[n] for n in G.nodes()}
    else:
        pos = nx.circular_layout(G)
    colors = [_get_color(r) for r in roles]

    # Draw nodes — no text yet (drawn manually below for font safety)
    nx.draw_networkx_nodes(
        G, pos, ax=ax, node_size=2800, node_color=colors, alpha=0.92,
        edgecolors="white", linewidths=2.5,
    )

    # Draw per-node labels explicitly with ax.text to guarantee glyph support.
    # nx.draw_networkx_labels uses the Agg renderer which can produce white
    # boxes for Unicode glyphs; ax.text with fontfamily='DejaVu Sans' is safe.
    for role in roles:
        x, y = pos[role.name]
        ax.text(
            x, y, role.name,
            fontsize=FONT_SIZE_LABEL, fontweight="bold", color="white",
            fontfamily="sans-serif",
            ha="center", va="center", zorder=6,
        )

    # Draw licensed edges (solid, green-tinted), grouped by connectionstyle
    licensed_color = "#22c55e"  # green
    default_cs = "arc3,rad=0.12"
    edge_by_style: dict[str, list[tuple[str, str]]] = {}
    for u, v in G.edges():
        if isinstance(licensed_connectionstyle, dict):
            cs = licensed_connectionstyle.get((u, v), default_cs)
        elif isinstance(licensed_connectionstyle, str):
            cs = licensed_connectionstyle
        else:
            cs = default_cs
        edge_by_style.setdefault(cs, []).append((u, v))
    for cs, edgelist in edge_by_style.items():
        nx.draw_networkx_edges(
            G, pos, ax=ax, edgelist=edgelist,
            edge_color=licensed_color, arrows=True,
            arrowsize=24, arrowstyle="-|>", connectionstyle=cs, width=2.75,
            alpha=0.85,
        )

    # Edge labels with weight and admissibility marker
    if show_admissibility:
        edge_labels = {}
        for u, v, data in G.edges(data=True):
            w = data.get("weight", 1.0)
            lbl = data.get("label", "")
            pfx = edge_label_prefix.get((u, v), "") if edge_label_prefix else ""
            edge_labels[(u, v)] = mathtext_safe_arrows(f"{pfx}✓ {lbl}\n(w={w:.1f})")
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, ax=ax,
            font_size=FONT_SIZE_FLOOR - 4, font_color=licensed_color,
            font_family="sans-serif",
        )

        # Draw prohibited edges
        prohibited_color = "#ef4444"  # red
        for src_name, tgt_name, label in prohibited_morphisms:
            if src_name in pos and tgt_name in pos:
                P = nx.DiGraph()
                P.add_edge(src_name, tgt_name)
                nx.draw_networkx_edges(
                    P, pos, ax=ax, edge_color=prohibited_color,
                    arrows=True, arrowsize=18, arrowstyle="-|>", width=1.6,
                    style="dashed", alpha=0.65,
                    connectionstyle="arc3,rad=0.15",
                )
                sx, sy = pos[src_name]
                tx, ty = pos[tgt_name]
                mx, my = (sx + tx) / 2, (sy + ty) / 2
                ax.annotate(
                    mathtext_safe_arrows(f"✗ {label}"), (mx, my),
                    fontsize=FONT_SIZE_FLOOR - 4,
                    color=prohibited_color, ha="center", va="center",
                    fontweight="bold", fontstyle="italic",
                    fontfamily="sans-serif",
                )

        # Legend
        licensed_patch = mpatches.Patch(
            color=licensed_color,
            label=mathtext_safe_arrows("✓ Licensed (structurally admissible)"),
        )
        prohibited_patch = mpatches.Patch(
            color=prohibited_color,
            label=mathtext_safe_arrows("✗ Prohibited (ill-formed)"),
        )
        ax.legend(
            handles=[licensed_patch, prohibited_patch],
            loc="lower left", fontsize=FONT_SIZE_FLOOR,
            framealpha=0.9,
        )
        ax.text(
            0.98,
            0.02,
            mathtext_safe_arrows(
                "Arrows: source role → target.\n"
                "Dashed edges not in Mor($\\mathcal{C}$)."
            ),
            transform=ax.transAxes,
            fontsize=max(FONT_SIZE_FLOOR - 6, 11),
            va="bottom",
            ha="right",
            color=COLOR_TEXT,
            fontfamily="sans-serif",
            zorder=10,
        )
    else:
        if edge_label_prefix:
            edge_labels = {}
            for u, v, data in G.edges(data=True):
                lbl = data.get("label", "")
                pfx = edge_label_prefix.get((u, v), "")
                edge_labels[(u, v)] = mathtext_safe_arrows(f"{pfx}{lbl}")
        else:
            edge_labels = {
                k: mathtext_safe_arrows(v)
                for k, v in nx.get_edge_attributes(G, "label").items()
            }
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, ax=ax,
            font_size=FONT_SIZE_FLOOR - 4, font_color=COLOR_TEXT,
            font_family="sans-serif",
        )

    # Use mathtext for \\mathcal{C} — Unicode 𝒞 (U+1D49E) is missing from DejaVu Sans.
    display_title = title or ("Case Category " + r"$\mathcal{C}$" + f": {category.name}")
    ax.set_title(display_title, fontsize=FONT_SIZE_TITLE, fontweight="bold", pad=20)
    if node_positions is not None:
        ax.margins(0.32)
    elif figsize is not None:
        ax.margins(0.28)
    else:
        ax.margins(0.25)
    ax.axis("off")
    fig.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight", facecolor="white")
        logger.info("Saved case category figure to %s", output_path)

    return fig


def render_alignment_comparison(
    output_path: Optional[Path] = None,
) -> matplotlib.figure.Figure:
    """Render side-by-side comparison of Accusative, Ergative, and Tripartite systems.

    Shows how core argument roles (S, A, P) are grouped differently
    under each alignment system.

    Args:
        output_path: Optional path to save the figure.

    Returns:
        The matplotlib Figure object.
    """
    fig, axes = plt.subplots(1, 3, figsize=COMPARISON_FIGSIZE)

    alignments = [
        ("Nominative-Accusative", {"S": "NOM", "A": "NOM", "P": "ACC"}),
        ("Ergative-Absolutive", {"S": "ABS", "A": "ERG", "P": "ABS"}),
        ("Tripartite", {"S": "ABS", "A": "ERG", "P": "ACC"}),
    ]

    for ax, (title, mapping) in zip(axes, alignments):
        G = nx.DiGraph()
        # Source nodes (left side)
        sources = ["S", "A", "P"]
        # Target nodes (right side)
        targets = sorted(set(mapping.values()))

        for s in sources:
            G.add_node(s, side="source")
        for t in targets:
            G.add_node(t, side="target")
        for s, t in mapping.items():
            G.add_edge(s, t)

        # Position: sources on left, targets on right
        pos = {}
        for i, s in enumerate(sources):
            pos[s] = (-1, -i)
        for i, t in enumerate(targets):
            pos[t] = (1, -i * (len(sources) - 1) / max(len(targets) - 1, 1))

        source_colors = [CASE_COLORS.get(s, COLOR_NEUTRAL) for s in sources]
        target_colors = [CASE_COLORS.get(t, COLOR_NEUTRAL) for t in targets]

        nx.draw_networkx_nodes(
            G, pos, nodelist=sources, ax=ax,
            node_size=1500, node_color=source_colors, alpha=0.9
        )
        nx.draw_networkx_nodes(
            G, pos, nodelist=targets, ax=ax,
            node_size=1500, node_color=target_colors, alpha=0.9
        )
        nx.draw_networkx_labels(
            G, pos, ax=ax, font_size=FONT_SIZE_LABEL - 2,
            font_weight="bold", font_color="white"
        )
        nx.draw_networkx_edges(
            G, pos, ax=ax, edge_color=COLOR_TEXT, arrows=True,
            arrowsize=15, width=2, style="dashed"
        )

        ax.set_title(title, fontsize=FONT_SIZE_LABEL, fontweight="bold")
        ax.axis("off")
        ax.margins(0.3)

    fig.suptitle(
        "Alignment Typology: Grouping of Core Argument Roles",
        fontsize=FONT_SIZE_TITLE, fontweight="bold", y=1.02
    )
    fig.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
        logger.info("Saved alignment comparison to %s", output_path)

    return fig


def render_composition_triangle(
    output_path: Optional[Path] = None,
) -> matplotlib.figure.Figure:
    """Render a composition diagram: f: A → B, g: B → C, h = g∘f: A → C.

    Shows the fundamental composition operation in the case category.

    Args:
        output_path: Optional path to save the figure.

    Returns:
        The matplotlib Figure object.
    """
    fig, ax = plt.subplots(1, 1, figsize=SQUARE_FIGSIZE)

    G = nx.DiGraph()
    nodes = ["A (NOM)", "B (ACC)", "C (DAT)"]
    G.add_nodes_from(nodes)
    G.add_edge(nodes[0], nodes[1], label="f: acts_on")
    G.add_edge(nodes[1], nodes[2], label="g: received_by")
    G.add_edge(nodes[0], nodes[2], label="h = g∘f")

    pos = {
        nodes[0]: (0, 0),
        nodes[1]: (2, 0),
        nodes[2]: (1, -1.5),
    }
    colors = [CASE_COLORS["NOM"], CASE_COLORS["ACC"], CASE_COLORS["DAT"]]

    nx.draw_networkx_nodes(
        G, pos, ax=ax, node_size=2500, node_color=colors, alpha=0.9
    )
    nx.draw_networkx_labels(
        G, pos, ax=ax, font_size=FONT_SIZE_LABEL - 2,
        font_weight="bold", font_color="white"
    )

    # Draw edges with different styles
    straight_edges = [(nodes[0], nodes[1]), (nodes[1], nodes[2])]
    composed_edge = [(nodes[0], nodes[2])]

    nx.draw_networkx_edges(
        G, pos, edgelist=straight_edges, ax=ax,
        edge_color=COLOR_TEXT, arrows=True, arrowsize=20, width=2
    )
    nx.draw_networkx_edges(
        G, pos, edgelist=composed_edge, ax=ax,
        edge_color=CASE_COLORS["ACC"], arrows=True, arrowsize=20, width=2.5,
        style="dashed"
    )

    edge_labels = {
        k: mathtext_safe_arrows(v)
        for k, v in nx.get_edge_attributes(G, "label").items()
    }
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, ax=ax,
        font_size=FONT_SIZE_FLOOR - 4, font_color=COLOR_TEXT
    )

    ax.set_title(
        r"Morphism Composition: $g \circ f = h$",
        fontsize=FONT_SIZE_TITLE, fontweight="bold", pad=20
    )
    ax.axis("off")
    ax.margins(0.3)
    fig.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
        logger.info("Saved composition triangle to %s", output_path)

    return fig
