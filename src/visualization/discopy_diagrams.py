"""Real DisCoPy diagram rendering for categorical string diagrams.

Uses the discopy library for mathematically rigorous compact closed
categorical diagrams. This module requires discopy>=1.0.0.

All functions produce publication-quality figures via discopy's
native drawing backend, then fit lexical borders to measured labels and
export the resulting figure at the project's publication resolution.

IMPORTANT: discopy's draw(ax=...) does NOT render visible content
onto a provided matplotlib axes. Let DisCoPy create its native figure
through draw(show=False), then export that figure.

References:
    de Felice, Toumi & Coecke (2020) — DisCoPy
    Coecke, Sadrzadeh & Clark (2010) — DisCoCat
"""
from __future__ import annotations

import logging
from pathlib import Path
from contextlib import contextmanager
from typing import Any, Iterator, Optional

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

from .styles import FIGURE_DPI, FONT_SIZE_FLOOR, save_publication_figure

from ..diagrams.string_diagram import (
    create_discopy_transitive,
    create_discopy_complex_transitive,
    create_discopy_intransitive,
    create_discopy_passive,
    create_discopy_snake_equation,
    create_discopy_composition,
    create_discopy_multilingual,
)

logger = logging.getLogger(__name__)


def _resolve_path(output_path: Optional[str | Path], default_name: str) -> Path:
    """Resolve output path, using a default filename if None."""
    if output_path is None:
        resolved = Path(default_name)
        logger.debug("No output_path provided, using default: %s", resolved)
        return resolved
    return Path(output_path)

# Standard draw kwargs for consistent, publication-quality output.
# Native font sizes are explicit; lexical borders are fitted after native layout.
DRAW_KWARGS = dict(fontsize=FONT_SIZE_FLOOR, fontsize_types=FONT_SIZE_FLOOR, margins=(0.15, 0.15), nodesize=1.2, draw_types=True)


@contextmanager
def _glyph_safe_rc() -> Iterator[None]:
    """Prefer DejaVu for DisCoPy text so Unicode math symbols survive savefig.
    Also pins ``savefig.dpi`` to ``FIGURE_DPI``: discopy's ``draw(path=...)``
    ignores the ``dpi`` kwarg and falls back to matplotlib's default 100 dpi,
    so every DisCoPy figure would otherwise render below the 300-dpi
    publication standard (§ADR-003).
    """
    with plt.rc_context(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [
                "DejaVu Sans",
                "Helvetica",
                "Arial",
                "Liberation Sans",
                "sans-serif",
            ],
            "savefig.dpi": FIGURE_DPI,
        }
    ):
        yield


def _draw_native(drawing: Any, destination: Path, **params: Any) -> None:
    """Use DisCoPy's native geometry, fitting lexical borders to measured text.

    DisCoPy fixes one-output box widths independently of the lexical label.
    Long labels can cross those borders. Expand the horizontal border after
    native layout without changing any wire, port, type or categorical box.
    """
    drawing.draw(show=False, **params)
    fig = plt.gcf()
    try:
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        for ax in fig.axes:
            labels = [t for t in ax.texts if t.get_horizontalalignment() == "center" and t.get_verticalalignment() == "center"]
            for patch in ax.patches:
                if not patch.get_fill() or not hasattr(patch, "get_path"):
                    continue
                vertices = np.asarray(patch.get_path().vertices)
                if len(vertices) != 5:
                    continue
                left, right = vertices[:, 0].min(), vertices[:, 0].max()
                bottom, top = vertices[:, 1].min(), vertices[:, 1].max()
                for label in labels:
                    x, y = label.get_position()
                    if not (left <= x <= right and bottom <= y <= top):
                        continue
                    extent = label.get_window_extent(renderer).transformed(ax.transData.inverted())
                    padding = (right - left) * 0.12
                    expanded_left = min(left, extent.x0 - padding)
                    expanded_right = max(right, extent.x1 + padding)
                    vertices[:, 0] = [expanded_left if value == left else expanded_right for value in vertices[:, 0]]
        save_publication_figure(fig, destination, dpi=FIGURE_DPI, bbox_inches="tight")
    finally:
        plt.close(fig)


def render_discopy_transitive(
    output_path: Optional[str] = None,
) -> None:
    """Render a DisCoPy complex transitive sentence diagram.

    Args:
        output_path: Path to save. Required.
    """
    resolved = _resolve_path(output_path, "discopy_transitive.png")
    diagram = create_discopy_complex_transitive()
    with _glyph_safe_rc():
        _draw_native(diagram, resolved,
            figsize=(16, 16),
            **{**DRAW_KWARGS, "fontsize": 18},
        )
    logger.info("Saved DisCoPy transitive to %s", resolved)


def render_discopy_composition(
    subject: str = "Alice",
    verb: str = "chases",
    obj: str = "Bob",
    output_path: Optional[str] = None,
) -> None:
    """Render a DisCoPy diagram showing pre-contraction → post-contraction.

    Left panel: uncontracted word tensor n ⊗ (n.r ⊗ s ⊗ n.l) ⊗ n
    Right panel: contracted sentence type s after Cup contractions

    Args:
        subject, verb, obj: Sentence components.
        output_path: Path to save.
    """
    from discopy.drawing import Equation

    resolved = _resolve_path(output_path, "discopy_composition.png")
    words, contracted = create_discopy_composition(subject, verb, obj)
    eq = Equation(words, contracted, symbol="→")
    with _glyph_safe_rc():
        _draw_native(eq, resolved,
            figsize=(16, 6),
            **DRAW_KWARGS,
        )
    logger.info("Saved DisCoPy composition to %s", resolved)


def render_discopy_snake(
    output_path: Optional[str] = None,
) -> None:
    """Render the snake equation (compact closure axiom).

    Shows: left snake = identity = right snake
    """
    from discopy.drawing import Equation

    resolved = _resolve_path(output_path, "discopy_snake.png")
    left, identity, right = create_discopy_snake_equation()
    eq = Equation(left, identity, right)
    with _glyph_safe_rc():
        _draw_native(eq, resolved,
            figsize=(18, 5),
            **DRAW_KWARGS,
        )
    logger.info("Saved DisCoPy snake equations to %s", resolved)


def render_discopy_passive(
    output_path: Optional[str] = None,
) -> None:
    """Render a passive voice diagram.

    'Bob is chased by Alice' with a separately assigned passive lexical type.
    """
    resolved = _resolve_path(output_path, "discopy_passive.png")
    diagram = create_discopy_passive("Bob", "chased", "Alice")
    with _glyph_safe_rc():
        _draw_native(diagram, resolved,
            figsize=(10, 5),
            **DRAW_KWARGS,
        )
    logger.info("Saved DisCoPy passive to %s", resolved)


def render_discopy_sentence_progression(
    output_path: Optional[str] = None,
) -> None:
    """Render a progression of sentence complexities.

    Intransitive → Transitive → Passive side by side.
    """
    from discopy.drawing import Equation

    intrans = create_discopy_intransitive("Bob", "runs")
    trans = create_discopy_transitive("Alice", "chases", "Bob")
    passive = create_discopy_passive("Bob", "chased", "Alice")

    resolved = _resolve_path(output_path, "discopy_sentence_progression.png")
    eq = Equation(intrans, trans, passive, symbol="→")
    with _glyph_safe_rc():
        _draw_native(eq, resolved,
            figsize=(24, 7),
            fontsize=18,
            margins=(0.12, 0.12),
        )
    logger.info("Saved sentence progression to %s", resolved)


def render_discopy_multilingual(
    output_path: Optional[str] = None,
) -> None:
    """Render 'Alice chases Bob' across 6 languages.

    Shows structural isomorphism of the DisCoCat type.
    Uses Equation to display all 6 language diagrams in sequence.
    """
    from discopy.drawing import Equation

    diagrams = create_discopy_multilingual()
    diagram_list = list(diagrams.values())

    # Show first 3 languages on one line
    resolved = _resolve_path(output_path, "discopy_multilingual.png")
    eq = Equation(*diagram_list[:3], symbol="≅")
    with _glyph_safe_rc():
        _draw_native(eq, resolved,
            figsize=(26, 7),
            fontsize=18,
            margins=(0.08, 0.08),
        )
    logger.info("Saved multilingual diagrams to %s", resolved)


def render_discopy_ditransitive(
    output_path: Optional[str] = None,
) -> None:
    """Render a ditransitive sentence diagram.

    'Alice gives Bob a book' with three noun arguments.
    """
    from discopy.rigid import Ty, Box as RBox, Cup, Id

    n = Ty('n')
    s = Ty('s')

    # Ditransitive verb: subject.r @ s @ indirect_obj.l @ direct_obj.l
    alice = RBox('Alice', Ty(), n)
    gives = RBox('gives', Ty(), n.r @ s @ n.l @ n.l)
    bob = RBox('Bob', Ty(), n)
    book = RBox('a book', Ty(), n)

    # Build and contract step by step
    diagram = alice @ gives @ bob @ book
    diagram = diagram >> Cup(n, n.r) @ Id(s @ n.l @ n.l @ n @ n)
    diagram = diagram >> Id(s) @ Id(n.l) @ Cup(n.l, n) @ Id(n)
    diagram = diagram >> Id(s) @ Cup(n.l, n)

    resolved = _resolve_path(output_path, "discopy_ditransitive.png")
    with _glyph_safe_rc():
        _draw_native(diagram, resolved,
            figsize=(12, 6),
            **DRAW_KWARGS,
        )
    logger.info("Saved ditransitive diagram to %s", resolved)


def render_discopy_discocirc_discourse(
    output_path: Optional[str] = None,
) -> None:
    """Render a two-sentence discourse using DisCoPy diagrams.

    'Alice chases Bob. Bob runs.' composed side by side.
    """
    from discopy.drawing import Equation

    trans = create_discopy_transitive("Alice", "chases", "Bob")
    intrans = create_discopy_intransitive("Bob", "runs")

    resolved = _resolve_path(output_path, "discopy_discourse.png")
    eq = Equation(trans, intrans, symbol="⊗")
    with _glyph_safe_rc():
        _draw_native(eq, resolved,
            figsize=(16, 6),
            **DRAW_KWARGS,
        )
    logger.info("Saved DisCoPy discourse to %s", resolved)


def render_discopy_three_sentence_discourse(
    output_path: Optional[str] = None,
) -> None:
    """Render three-sentence role reversal using DisCoPy diagrams.

    Matches manuscript §4c and ``Discourse.role_reversal``:
    Alice chases Bob. Bob fears Alice. Alice smiles (lexical heads on boxes).
    """
    from discopy.drawing import Equation

    s1 = create_discopy_transitive("Alice", "chases", "Bob")
    s2 = create_discopy_transitive("Bob", "fears", "Alice")
    s3 = create_discopy_intransitive("Alice", "smiles")

    resolved = _resolve_path(output_path, "discopy_three_sentence.png")
    eq = Equation(s1, s2, s3, symbol="⊗")
    with _glyph_safe_rc():
        _draw_native(eq, resolved,
            figsize=(26, 7),
            fontsize=18,
            margins=(0.08, 0.08),
        )
    logger.info("Saved three-sentence discourse to %s", resolved)


def get_diagram_metrics(diagram) -> dict:
    """Extract structural metrics from a DisCoPy diagram.

    Args:
        diagram: A discopy.rigid.Diagram.

    Returns:
        Dict with keys: n_boxes, dom_type, cod_type, n_wires.
    """
    return {
        "n_boxes": len(diagram.boxes),
        "dom_type": str(diagram.dom),
        "cod_type": str(diagram.cod),
        "n_wires": len(diagram.dom) + len(diagram.cod),
    }
