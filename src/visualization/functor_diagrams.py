"""Alignment functor diagram visualizations.

Renders side-by-side directed acyclic graphs representing source and
target categories with dashed mapping arrows between them.
"""

import logging
from pathlib import Path
from typing import Optional

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

from ..case_systems.functor import AlignmentFunctor
from .styles import CASE_COLORS, FONT_SIZE_FLOOR, FONT_SIZE_TITLE, FONT_SIZE_LABEL, WIDE_FIGSIZE, FIGURE_DPI

logger = logging.getLogger(__name__)


def render_functor_diagram(
    functor: AlignmentFunctor,
    output_path: Optional[Path] = None,
    title: Optional[str] = None,
) -> matplotlib.figure.Figure:
    """Render an alignment functor as side-by-side category diagrams.

    Source category on the left, target on the right, with dashed
    arrows showing the functor mapping between objects.

    Args:
        functor: The alignment functor to visualize.
        output_path: Optional path to save the figure.
        title: Optional title override.

    Returns:
        The matplotlib Figure object.
    """
    fig, (ax_source, ax_target) = plt.subplots(1, 2, figsize=WIDE_FIGSIZE)

    # Source category
    _render_category_side(ax_source, functor.source, f"Source: {functor.source.name}")

    # Target category
    _render_category_side(ax_target, functor.target, f"Target: {functor.target.name}")

    # Draw functor mapping arrows using figure-level coordinates
    source_roles = sorted(functor.source.objects, key=lambda r: r.name)
    target_roles = sorted(functor.target.objects, key=lambda r: r.name)

    for source_role, target_role in functor.object_map.items():
        if source_role in functor.source.objects and target_role in functor.target.objects:
            try:
                s_idx = source_roles.index(source_role)
                t_idx = target_roles.index(target_role)
            except ValueError:
                continue

            # Use figure-level annotation for cross-axes arrows
            s_y = 1.0 - (s_idx + 0.5) / len(source_roles)
            t_y = 1.0 - (t_idx + 0.5) / len(target_roles)

            fig.add_artist(mpatches.FancyArrowPatch(
                posA=(0.48, s_y * 0.7 + 0.15),
                posB=(0.52, t_y * 0.7 + 0.15),
                transform=fig.transFigure,
                arrowstyle="->,head_width=6,head_length=6",
                color="#9333EA",
                linewidth=2,
                linestyle="dashed",
                mutation_scale=15,
            ))

    display_title = title or f"Alignment Functor: {functor.name}"
    fig.suptitle(
        display_title, fontsize=FONT_SIZE_TITLE,
        fontweight="bold", y=1.02,
    )
    fig.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
        logger.info("Saved functor diagram to %s", output_path)

    return fig


def _render_category_side(ax: plt.Axes, category, title: str) -> None:
    """Render a single category as a directed graph in the given axes."""
    G = nx.DiGraph()
    roles = sorted(category.objects, key=lambda r: r.name)
    for role in roles:
        G.add_node(role.name)
    for morph in category.morphisms:
        G.add_edge(morph.source.name, morph.target.name, label=morph.label)

    pos = nx.circular_layout(G)
    colors = [CASE_COLORS.get(r.name, "#6B7280") for r in roles]

    nx.draw_networkx_nodes(
        G, pos, ax=ax, node_size=1500, node_color=colors, alpha=0.9,
    )
    nx.draw_networkx_labels(
        G, pos, ax=ax, font_size=FONT_SIZE_LABEL - 2,
        font_weight="bold", font_color="white",
    )
    if G.edges:
        nx.draw_networkx_edges(
            G, pos, ax=ax, edge_color="#374151", arrows=True,
            arrowsize=15, width=1.5, connectionstyle="arc3,rad=0.1",
        )

    ax.set_title(title, fontsize=FONT_SIZE_LABEL, fontweight="bold")
    ax.axis("off")
    ax.margins(0.3)
