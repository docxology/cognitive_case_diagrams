"""Syntactic and semantic sentence diagram visualizations.

Renders a publication-quality multi-panel figure showing both syntactic
parse structure (dependency-style trees) and categorical/pregroup type
strings for a curated set of linguistically informative case assignment
scenarios. Uses matplotlib only for reliable headless rendering.

Figure output: syntactic_case_panel.png
"""

from .styles import save_publication_figure
import logging
import textwrap
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from .styles import FIGURE_DPI, mathtext_safe_arrows

logger = logging.getLogger(__name__)

# ── Panel definitions ──────────────────────────────────────────────────────────
# Each entry is a dict with:
#   title      : str   — construction name shown above sub-panel
#   words      : list  — word tokens
#   roles      : list  — case label per word (or None)
#   type_str   : str   — pregroup type formula (LaTeX)
#   subtrees   : list  — (word_idx, parent_idx, label) arcs for the tree
#   desc       : str   — short description shown below type string
# ──────────────────────────────────────────────────────────────────────────────

CASE_PALETTE = {
    "NOM": "#2563EB",
    "ACC": "#DC2626",
    "DAT": "#7C3AED",
    "GEN": "#059669",
    "INS": "#D97706",
    "LOC": "#0891B2",
    "ABL": "#BE185D",
    "ERG": "#9333EA",
    "ABS": "#0D9488",
    "V":   "#374151",
    "ADV": "#6B7280",
    "DET": "#9CA3AF",
    "ADJ": "#F59E0B",
    "PP":  "#10B981",
}

PANELS = [{'title': 'Intransitive (NOM)',
  'words': ['Alice', 'runs'],
  'roles': ['NOM', 'V'],
  'type_str': '$n \\cdot (n^r \\cdot s) \\Rightarrow s$',
  'desc': 'Sole argument S assigned NOM;\nverb type $n^r s$ contracts with subject $n$.',
  'arcs': [(0, 1, 'subj')]},
 {'title': 'Transitive (NOM+ACC)',
  'words': ['Alice', 'chases', 'Bob'],
  'roles': ['NOM', 'V', 'ACC'],
  'type_str': '$n \\cdot (n^r \\cdot s \\cdot n^l) \\cdot n \\Rightarrow s$',
  'desc': 'A=NOM, P=ACC;\nverb $n^r s n^l$ contracts both arguments.',
  'arcs': [(0, 1, 'subj'), (2, 1, 'obj')]},
 {'title': 'Ditransitive (NOM+DAT+ACC)',
  'words': ['Alice', 'gives', 'Bob', 'a book'],
  'roles': ['NOM', 'V', 'DAT', 'ACC'],
  'type_str': '$n \\cdot (n^r \\cdot s \\cdot n^l \\cdot n^l) \\cdot n \\cdot n \\Rightarrow s$',
  'desc': 'Three argument slots: subject NOM,\nrecipient DAT, theme ACC.',
  'arcs': [(0, 1, 'subj'), (2, 1, 'iobj'), (3, 1, 'obj')]},
 {'title': 'Passive Voice (Patient→NOM)',
  'words': ['Bob', 'is chased', 'by Alice'],
  'roles': ['NOM', 'V', 'INS'],
  'type_str': '$n \\cdot (n^r \\cdot s \\cdot n^l) \\cdot n \\Rightarrow s$',
  'desc': 'Assigned passive template; case labels are metadata.\n'
          'The by-phrase is represented as an oblique slot.',
  'arcs': [(0, 1, 'subj'), (2, 1, 'obl')]},
 {'title': 'Ergative Clause (ERG+ABS)',
  'words': ['Actor.ERG', 'Patient.ABS', 'verb'],
  'roles': ['ERG', 'ABS', 'V'],
  'type_str': '$a \\cdot p \\cdot (p^r \\cdot a^r \\cdot s) \\Rightarrow s$',
  'desc': 'Schematic SOV template; a=ERG, p=ABS.\nNo language-specific sentence is asserted.',
  'arcs': [(0, 2, 'A'), (1, 2, 'P')]},
 {'title': 'Benefactive adjunct (schematic)',
  'words': ['Maria', 'cooked', 'dinner', 'for Pablo'],
  'roles': ['NOM', 'V', 'ACC', 'DAT'],
  'type_str': '$n \\cdot (n^r \\cdot s \\cdot n^l) \\cdot n \\cdot (s^r \\cdot s) \\Rightarrow s$',
  'desc': 'The complete for-phrase is assigned sentence-modifier type.\n'
          'DAT is a semantic illustration, not English inflection.',
  'arcs': [(0, 1, 'subj'), (2, 1, 'obj'), (3, 1, 'ben')]},
 {'title': 'Relative Clause (Embedded NOM)',
  'words': ['The man', 'the dog', 'chased', 'ran'],
  'roles': ['NOM', 'NOM', 'V₂', 'V₁'],
  'type_str': 'Relative-clause structure: no formal derivation supplied',
  'desc': 'Head noun has two argument functions.\n'
          'Arcs sketch dependencies; no coreference model is run.',
  'arcs': [(0, 3, 'subj'), (1, 2, 'subj-rc'), (0, 2, 'obj-rc')]},
 {'title': 'Causative + Adj + Adv (Complex)',
  'words': ['The quick fox', 'made', 'the lazy dog', 'jump', 'suddenly'],
  'roles': ['NOM', 'V', 'ACC', 'V₂', 'ADV'],
  'type_str': 'Causative structure: no formal derivation supplied',
  'desc': 'Causative and embedded predicate are annotated.\n'
          'No measured box/cup complexity is claimed.',
  'arcs': [(0, 1, 'cause'), (2, 1, 'causee'), (3, 1, 'comp'), (4, 3, 'adv')]}]


def _draw_tree_panel(
    ax: plt.Axes,
    words: list,
    roles: list,
    arcs: list,
) -> None:
    """Draw a dependency-style tree for one sentence panel.

    Nodes are placed in a row; arcs curve above them.
    """
    n = len(words)
    if n == 0:
        return

    # Evenly space word nodes across x ∈ [0, 1]
    xs = np.linspace(0.08, 0.92, n)
    y_word = 0.22  # word row y

    # Draw arcs first (below nodes)
    for (src, tgt, lbl) in arcs:
        if src >= n or tgt >= n:
            continue
        x1, x2 = xs[src], xs[tgt]
        xm = (x1 + x2) / 2
        # Arc height proportional to distance
        dist = abs(x2 - x1)
        # Draw as bezier via FancyArrowPatch
        ax.annotate(
            "",
            xy=(x2, y_word + 0.04),
            xytext=(x1, y_word + 0.04),
            arrowprops=dict(
                arrowstyle="->",
                color="#374151",
                lw=1.4,
                connectionstyle=f"arc3,rad={-.18 if x2 < x1 else .18}",
            ),
            zorder=2,
        )
        # Arc label
        ax.text(
            xm, y_word + 0.04 + 0.15 * dist, lbl,
            fontsize=16, ha="center", va="bottom", color="#374151",
            fontstyle="italic", zorder=3,
        )

    # Draw word nodes
    for i, (word, role) in enumerate(zip(words, roles)):
        color = CASE_PALETTE.get(role, "#6B7280") if role else "#9CA3AF"
        # Node circle
        circle = plt.Circle(
            (xs[i], y_word), 0.055,
            facecolor=color, edgecolor="white", linewidth=1.5, zorder=4,
        )
        ax.add_patch(circle)
        # Case label inside circle
        ax.text(
            xs[i], y_word, role or "",
            fontsize=16, ha="center", va="center", color="white",
            fontweight="bold", zorder=5,
        )
        # Word label below circle
        ax.text(
            xs[i], y_word - 0.095,
            textwrap.fill(word, 12), fontsize=16, ha="center", va="top",
            color="#111827", fontweight="bold",
        )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.65)
    ax.axis("off")


def render_syntactic_panel(
    output_path: Optional[str] = None,
    panels: Optional[list] = None,
) -> str:
    """Render the multi-panel syntactic + semantic case assignment figure.

    Produces two columns of example panels, each showing:
      - Top row: dependency-style syntactic tree with case annotations
      - Bottom row: categorical pregroup type formula

    Args:
        output_path: Where to save the PNG.
        panels: Override panel definitions (default: PANELS).

    Returns:
        The output path.
    """
    if panels is None:
        panels = PANELS
    n_panels = len(panels)

    # Two columns keep the examples legible on a portrait manuscript page.
    n_cols = 2
    n_rows_of_panels = (n_panels + n_cols - 1) // n_cols   # ceil division
    # Each panel block = 2 matplotlib rows: tree (height 3) + type (height 1.2)
    fig_height = n_rows_of_panels * 4.0
    fig_width = n_cols * 7.0

    fig = plt.figure(figsize=(fig_width, fig_height), facecolor="white")

    for idx, panel in enumerate(panels):
        row_block = idx // n_cols
        col = idx % n_cols

        # Tree subplot: top portion of this panel block
        ax_tree = fig.add_axes((
            col / n_cols + 0.01,
            1.0 - (row_block + 1) / n_rows_of_panels + 0.22 / n_rows_of_panels,
            1 / n_cols - 0.02,
            0.60 / n_rows_of_panels,
        ))
        _draw_tree_panel(
            ax_tree,
            panel["words"],
            panel["roles"],
            panel["arcs"],
        )
        ax_tree.set_title(
            mathtext_safe_arrows(panel["title"]),
            fontsize=16, fontweight="bold", color="#111827",
            pad=4,
        )

        # Type string subplot: bottom portion of this panel block
        ax_type = fig.add_axes((
            col / n_cols + 0.01,
            1.0 - (row_block + 1) / n_rows_of_panels + 0.01 / n_rows_of_panels,
            1 / n_cols - 0.02,
            0.20 / n_rows_of_panels,
        ))
        ax_type.text(
            0.5, 0.70,
            panel["type_str"],
            ha="center", va="center", fontsize=16,
            transform=ax_type.transAxes,
            bbox=dict(
                boxstyle="round,pad=0.35",
                facecolor="#EFF6FF",
                edgecolor="#2563EB",
                linewidth=1.2,
            ),
        )
        ax_type.text(
            0.5, 0.12,
            panel["desc"],
            ha="center", va="center", fontsize=16,
            color="#374151", transform=ax_type.transAxes,
        )
        ax_type.axis("off")

    # Global title
    fig.suptitle(
        "Assigned role labels and selected pregroup types\n"
        "Schematics for simple and complex constructions",
        fontsize=16, fontweight="bold", y=1.005, color="#111827",
    )

    # Legend: case role colours
    legend_elements = [
        mpatches.Patch(color=CASE_PALETTE[k], label=k)
        for k in ["NOM", "ACC", "DAT", "ERG", "ABS", "INS", "V", "ADV"]
    ]
    fig.legend(
        handles=legend_elements,
        loc="lower center",
        ncol=8,
        fontsize=16,
        framealpha=0.9,
        title="Case-role and word-class colours",
        title_fontsize=16,
        bbox_to_anchor=(0.5, -0.085),
    )

    if output_path is None:
        output_path = "syntactic_case_panel.png"

    save_publication_figure(fig,
        output_path,
        dpi=FIGURE_DPI,
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)
    logger.info("Saved syntactic case panel to %s", output_path)
    return output_path
