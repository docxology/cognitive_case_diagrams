"""Native string diagram visualizations using matplotlib.

Renders DisCoCat and DisCoCirc-style string diagrams without DisCoPy,
using direct matplotlib drawing for maximum control over layout.
"""

import logging
from typing import Optional

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from ..case_systems.case_category import CaseRole
from ..diagrams.string_diagram import Sentence, Discourse
from .styles import (
    CASE_COLORS, FONT_SIZE_FLOOR, FONT_SIZE_TITLE, FONT_SIZE_LABEL,
    DEFAULT_FIGSIZE, WIDE_FIGSIZE, FIGURE_DPI,
    COLOR_EDGE, COLOR_TEXT, COLOR_NEUTRAL, COLOR_WIRE,
    COLOR_ENTITY_WIRE, COLOR_ENTITY_BORDER,
    MARKER_SIZE, LINE_WIDTH_EDGE,
    mathtext_safe_arrows,
)

logger = logging.getLogger(__name__)


def render_discocat_sentence(
    sentence: Sentence,
    output_path: Optional[str] = None,
    title: Optional[str] = None,
) -> matplotlib.figure.Figure:
    """Render a single sentence as a DisCoCat string diagram.

    Args:
        sentence: The sentence to render.
        output_path: Optional path to save.
        title: Optional title override.

    Returns:
        The matplotlib Figure.
    """
    fig, ax = plt.subplots(1, 1, figsize=DEFAULT_FIGSIZE)

    boxes = sentence.boxes
    n_boxes = len(boxes)
    x_positions = np.linspace(0.5, n_boxes - 0.5, n_boxes)

    # Draw boxes
    for i, box in enumerate(boxes):
        x = x_positions[i]
        color = CASE_COLORS.get(
            sentence.case_assignments.get(box.name, CaseRole.NOM).name, COLOR_NEUTRAL
        )

        # Box rectangle
        rect = mpatches.FancyBboxPatch(
            (x - 0.35, 0.3), 0.7, 0.4,
            boxstyle="round,pad=0.05",
            facecolor=color, edgecolor=COLOR_EDGE,
            linewidth=LINE_WIDTH_EDGE, alpha=0.9,
        )
        ax.add_patch(rect)
        ax.text(
            x, 0.5, box.name,
            ha="center", va="center",
            fontsize=FONT_SIZE_LABEL, fontweight="bold",
            color="white",
        )

        # Draw output wires
        for wire in box.cod:
            ax.plot(
                [x, x], [0.7, 1.2],
                color=COLOR_TEXT, linewidth=LINE_WIDTH_EDGE, solid_capstyle="round",
            )
            type_label = wire.wire_type.name
            if wire.case_role:
                type_label += f" [{wire.case_role.name}]"
            ax.text(
                x, 1.25, type_label,
                ha="center", va="bottom",
                fontsize=FONT_SIZE_FLOOR - 4, color=COLOR_TEXT,
            )

    # Draw cup connections for transitive verbs
    verb_boxes = [b for b in boxes if any(w.wire_type.name == "s" for w in b.cod)]
    if verb_boxes:
        verb = verb_boxes[0]
        verb_idx = boxes.index(verb)
        verb_x = x_positions[verb_idx]
        # Draw cups from noun wires to verb
        for dom_wire in verb.dom:
            if dom_wire.entity:
                try:
                    noun_box = next(b for b in boxes if b.name == dom_wire.entity)
                    noun_idx = boxes.index(noun_box)
                    noun_x = x_positions[noun_idx]
                    mid_y = -0.3
                    ax.plot(
                        [noun_x, noun_x, verb_x, verb_x],
                        [0.3, mid_y, mid_y, 0.3],
                        color=COLOR_NEUTRAL, linewidth=1.5,
                        linestyle="--", solid_capstyle="round",
                    )
                except StopIteration:
                    pass

    display_title = mathtext_safe_arrows(title or f'DisCoCat: "{sentence.text}"')
    ax.set_title(display_title, fontsize=FONT_SIZE_TITLE, fontweight="bold", pad=20)
    ax.set_xlim(-0.5, n_boxes)
    ax.set_ylim(-0.8, 1.6)
    ax.axis("off")
    fig.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
        logger.info("Saved DisCoCat sentence to %s", output_path)

    return fig


def render_discourse_diagram(
    discourse: Discourse,
    output_path: Optional[str] = None,
    title: Optional[str] = None,
) -> matplotlib.figure.Figure:
    """Render a multi-sentence discourse as a DisCoCirc diagram.

    Shows entity wires persisting across sentence boundaries with
    dynamic case role reassignment.

    Args:
        discourse: The discourse to render.
        output_path: Optional path to save.
        title: Optional title override.

    Returns:
        The matplotlib Figure.
    """
    fig, ax = plt.subplots(1, 1, figsize=WIDE_FIGSIZE)

    entities = sorted(discourse.entities)
    n_entities = len(entities)
    n_sentences = discourse.num_sentences

    # Entity wire x-positions
    x_entity = {e: i * 2 for i, e in enumerate(entities)}

    # Sentence y-positions (going downward)
    y_sentences = [(n_sentences - i) * 2 for i in range(n_sentences)]

    # Draw persistent entity wires (vertical lines)
    for entity in entities:
        x = x_entity[entity]
        ax.plot(
            [x, x], [0, (n_sentences + 1) * 2],
            color=COLOR_WIRE, linewidth=3, zorder=0,
        )
        ax.text(
            x, (n_sentences + 1) * 2 + 0.3, entity,
            ha="center", va="bottom",
            fontsize=FONT_SIZE_LABEL, fontweight="bold",
            color=COLOR_EDGE,
        )

    # Draw sentence boxes
    for sent_idx, sentence in enumerate(discourse.sentences):
        y = y_sentences[sent_idx]

        # Verb box spanning the involved entities
        involved = [e for e in entities if e in sentence.case_assignments]
        if involved:
            x_min = min(x_entity[e] for e in involved) - 0.5
            x_max = max(x_entity[e] for e in involved) + 0.5

            # Find the verb
            verb_boxes = [b for b in sentence.boxes if any(
                w.wire_type.name == "s" for w in b.cod
            )]
            verb_name = verb_boxes[0].name if verb_boxes else "?"

            rect = mpatches.FancyBboxPatch(
                (x_min, y - 0.4), x_max - x_min, 0.8,
                boxstyle="round,pad=0.1",
                facecolor=COLOR_ENTITY_WIRE, edgecolor=COLOR_ENTITY_BORDER,
                linewidth=LINE_WIDTH_EDGE, alpha=0.85,
            )
            ax.add_patch(rect)
            ax.text(
                (x_min + x_max) / 2, y, verb_name,
                ha="center", va="center",
                fontsize=FONT_SIZE_LABEL, fontweight="bold",
                color="white",
            )

        # Draw case role labels at wire intersections
        for entity, role in sentence.case_assignments.items():
            x = x_entity[entity]
            color = CASE_COLORS.get(role.name, COLOR_NEUTRAL)
            ax.plot(x, y, "o", color=color, markersize=MARKER_SIZE, zorder=5)
            ax.text(
                x, y - 0.6, role.name,
                ha="center", va="top",
                fontsize=FONT_SIZE_FLOOR - 4, fontweight="bold",
                color=color,
            )

    display_title = mathtext_safe_arrows(title or "DisCoCirc Discourse Diagram")
    ax.set_title(display_title, fontsize=FONT_SIZE_TITLE, fontweight="bold", pad=20)
    ax.set_xlim(-1, n_entities * 2)
    ax.set_ylim(-0.5, (n_sentences + 2) * 2)
    ax.axis("off")
    fig.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
        logger.info("Saved discourse diagram to %s", output_path)

    return fig


def render_discocirc_discourse(
    output_path: Optional[str] = None,
) -> matplotlib.figure.Figure:
    """Render the canonical two-sentence discourse diagram.

    'Alice chases Bob. Bob runs.' showing Bob as ACC then NOM.
    """
    discourse = Discourse.two_sentence("Alice", "chases", "Bob", "Bob", "runs")
    return render_discourse_diagram(
        discourse,
        output_path=output_path,
        title='DisCoCirc: "Alice chases Bob. Bob runs."',
    )


def render_three_sentence_discourse(
    output_path: Optional[str] = None,
) -> matplotlib.figure.Figure:
    """Render the three-sentence role reversal discourse.

    Uses ``Discourse.role_reversal`` (chases / fears / smiles). Alice (NOM→ACC→NOM) across three sentences.
    """
    discourse = Discourse.role_reversal("Alice", "Bob")
    return render_discourse_diagram(
        discourse,
        output_path=output_path,
        title="Role Reversal: Alice NOM→ACC→NOM",
    )
