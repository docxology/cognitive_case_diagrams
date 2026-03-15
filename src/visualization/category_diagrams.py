"""Category diagram visualizations using matplotlib and networkx.

Renders case categories as directed graphs, alignment comparisons,
and composition triangles for the manuscript figures.
"""

import logging
from pathlib import Path
from typing import Optional

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from ..case_systems.case_category import CaseCategory, CaseRole, Morphism, standard_case_category, minimal_case_category
from .styles import CASE_COLORS, FONT_SIZE_FLOOR, FONT_SIZE_TITLE, FONT_SIZE_LABEL, DEFAULT_FIGSIZE, COMPARISON_FIGSIZE, FIGURE_DPI

logger = logging.getLogger(__name__)


def _get_color(role: CaseRole) -> str:
    """Get the palette color for a case role."""
    return CASE_COLORS.get(role.name, "#4B5563")


def render_case_category(
    category: CaseCategory,
    output_path: Optional[Path] = None,
    title: Optional[str] = None,
) -> matplotlib.figure.Figure:
    """Render a case category as a directed graph.

    Objects (case roles) are nodes in a circular layout.
    Morphisms (grammatical relations) are directed edges.

    Args:
        category: The case category to render.
        output_path: Optional path to save the figure.
        title: Optional title override.

    Returns:
        The matplotlib Figure object.
    """
    fig, ax = plt.subplots(1, 1, figsize=DEFAULT_FIGSIZE)

    G = nx.DiGraph()
    roles = sorted(category.objects, key=lambda r: r.name)
    for role in roles:
        G.add_node(role.name)
    for morph in category.morphisms:
        G.add_edge(morph.source.name, morph.target.name, label=morph.label)

    pos = nx.circular_layout(G)
    colors = [_get_color(r) for r in roles]

    nx.draw_networkx_nodes(
        G, pos, ax=ax, node_size=2000, node_color=colors, alpha=0.9
    )
    nx.draw_networkx_labels(
        G, pos, ax=ax, font_size=FONT_SIZE_LABEL, font_weight="bold",
        font_color="white"
    )
    nx.draw_networkx_edges(
        G, pos, ax=ax, edge_color="#374151", arrows=True,
        arrowsize=20, connectionstyle="arc3,rad=0.1", width=2
    )
    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, ax=ax,
        font_size=FONT_SIZE_FLOOR - 4, font_color="#374151"
    )

    display_title = title or f"Case Category: {category.name}"
    ax.set_title(display_title, fontsize=FONT_SIZE_TITLE, fontweight="bold", pad=20)
    ax.margins(0.2)
    ax.axis("off")
    fig.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
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

        source_colors = [CASE_COLORS.get(s, "#6B7280") for s in sources]
        target_colors = [CASE_COLORS.get(t, "#6B7280") for t in targets]

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
            G, pos, ax=ax, edge_color="#374151", arrows=True,
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
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))

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
        edge_color="#374151", arrows=True, arrowsize=20, width=2
    )
    nx.draw_networkx_edges(
        G, pos, edgelist=composed_edge, ax=ax,
        edge_color="#DC2626", arrows=True, arrowsize=20, width=2.5,
        style="dashed"
    )

    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, ax=ax,
        font_size=FONT_SIZE_FLOOR - 4, font_color="#374151"
    )

    ax.set_title(
        "Morphism Composition: g ∘ f = h",
        fontsize=FONT_SIZE_TITLE, fontweight="bold", pad=20
    )
    ax.axis("off")
    ax.margins(0.3)
    fig.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
        logger.info("Saved composition triangle to %s", output_path)

    return fig
