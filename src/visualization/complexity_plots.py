"""Complexity comparison plots for pregroup grammar diagrams.

Generates publication-quality visualizations comparing syntactic
complexity across different sentence types and structures.
"""

import logging

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .styles import CASE_COLORS, FONT_SIZE_FLOOR

# Local aliases for convenience
COLORS = {
    "primary": CASE_COLORS["NOM"],     # Blue
    "secondary": CASE_COLORS["ACC"],   # Red
    "accent": CASE_COLORS["GEN"],      # Emerald
}
FONT_SIZE = FONT_SIZE_FLOOR

logger = logging.getLogger(__name__)


def render_complexity_comparison(
    labels: list[str],
    box_counts: list[int],
    word_counts: list[int],
    cup_counts: list[int],
    sentences: list[str],
    output_path: str,
) -> str:
    """Render a grouped bar chart comparing diagram complexity metrics.

    Shows box count, word count, and cup count side-by-side for
    multiple sentence types.

    Args:
        labels: Sentence type labels (e.g., "Intransitive", "Transitive").
        box_counts: Total box counts per sentence type.
        word_counts: Word box counts per sentence type.
        cup_counts: Cup contraction counts per sentence type.
        sentences: Text of the sentences to overlay on the plot.
        output_path: Path to save the figure.

    Returns:
        The output path.
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    x = np.arange(len(labels))
    width = 0.25

    bars1 = ax.bar(x - width, box_counts, width, label="Total Boxes",
                   color=COLORS["primary"], alpha=0.85)
    bars2 = ax.bar(x, word_counts, width, label="Word Boxes",
                   color=COLORS["secondary"], alpha=0.85)
    bars3 = ax.bar(x + width, cup_counts, width, label="Cup Contractions",
                   color=COLORS["accent"], alpha=0.85)

    ax.set_xlabel("Sentence Type", fontsize=FONT_SIZE)
    ax.set_ylabel("Count", fontsize=FONT_SIZE)
    ax.set_title("DisCoCat Diagram Complexity Comparison",
                 fontsize=FONT_SIZE + 2, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=FONT_SIZE - 2, rotation=15, ha="right")
    ax.tick_params(axis="y", labelsize=FONT_SIZE - 2)
    ax.legend(fontsize=FONT_SIZE - 2, loc='upper left')
    ax.grid(axis="y", alpha=0.3)

    # Add value labels on bars
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2., height + 0.1,
                    f"{int(height)}", ha="center", va="bottom",
                    fontsize=FONT_SIZE - 4,
                )

    # Overlay sentence text under the bars
    max_height = max(max(box_counts), max(word_counts), max(cup_counts))
    for i, sentence in enumerate(sentences):
        ax.text(
            x[i], max_height + 0.8,
            f'"{sentence}"', ha="center", va="bottom",
            fontsize=FONT_SIZE - 4, rotation=45, color="#333333"
        )
    
    ax.set_ylim(0, max_height + 3.0) # make room for text at top

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved complexity comparison plot to %s", output_path)
    return output_path


def render_normal_form_comparison(
    labels: list[str],
    original_counts: list[int],
    normal_form_counts: list[int],
    output_path: str,
) -> str:
    """Render bar chart comparing original vs. normal form box counts.

    Args:
        labels: Diagram labels.
        original_counts: Box counts before normalization.
        normal_form_counts: Box counts after normalization.
        output_path: Path to save the figure.

    Returns:
        The output path.
    """
    fig, ax = plt.subplots(figsize=(9, 6))

    x = np.arange(len(labels))
    width = 0.35

    ax.bar(x - width / 2, original_counts, width, label="Original",
           color=COLORS["primary"], alpha=0.85)
    ax.bar(x + width / 2, normal_form_counts, width, label="Normal Form",
           color=COLORS["accent"], alpha=0.85)

    ax.set_xlabel("Diagram Type", fontsize=FONT_SIZE)
    ax.set_ylabel("Box Count", fontsize=FONT_SIZE)
    ax.set_title("Original vs. Normal Form Diagram Complexity",
                 fontsize=FONT_SIZE + 2, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=FONT_SIZE - 2, rotation=15, ha="right")
    ax.tick_params(axis="y", labelsize=FONT_SIZE - 2)
    ax.legend(fontsize=FONT_SIZE - 2)
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved normal form comparison plot to %s", output_path)
    return output_path


def render_syntactic_complexity_radar(
    labels: list[str],
    metrics: dict[str, list[float]],
    output_path: str,
) -> str:
    """Render a radar chart of syntactic complexity dimensions.

    Args:
        labels: Sentence type labels on radar axes.
        metrics: Dict mapping metric names to lists of values per axis.
        output_path: Path to save the figure.

    Returns:
        The output path.
    """
    n = len(labels)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]  # close the polygon

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"polar": True})

    colors_list = [COLORS["primary"], COLORS["secondary"], COLORS["accent"]]
    for idx, (metric_name, values) in enumerate(metrics.items()):
        vals = values + values[:1]
        color = colors_list[idx % len(colors_list)]
        ax.plot(angles, vals, "o-", linewidth=2, label=metric_name, color=color)
        ax.fill(angles, vals, alpha=0.15, color=color)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=FONT_SIZE - 2)
    ax.set_title("Syntactic Complexity Profile",
                 fontsize=FONT_SIZE + 2, fontweight="bold", y=1.08)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1),
              fontsize=FONT_SIZE - 2)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved complexity radar chart to %s", output_path)
    return output_path
