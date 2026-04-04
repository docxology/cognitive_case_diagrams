"""Real DisCoPy diagram rendering for categorical string diagrams.

Uses the discopy library for mathematically rigorous compact closed
categorical diagrams. This module requires discopy>=1.0.0.

All functions produce publication-quality figures via discopy's
native drawing backend, using draw(path=...) which is the only
reliable rendering path for discopy diagrams.

IMPORTANT: discopy's draw(ax=...) does NOT render visible content
onto a provided matplotlib axes. Always use draw(path=...) or
Equation().draw(path=...) for visible output.

References:
    de Felice, Toumi & Coecke (2020) — DisCoPy
    Coecke, Sadrzadeh & Clark (2010) — DisCoCat
"""

import logging
from pathlib import Path
from contextlib import contextmanager
from typing import Iterator, Optional

import matplotlib.pyplot as plt

from ..diagrams.string_diagram import (
    create_discopy_transitive,
    create_discopy_intransitive,
    create_discopy_passive,
    create_discopy_snake_equation,
    create_discopy_composition,
    create_discopy_multilingual,
)

logger = logging.getLogger(__name__)

# Standard draw kwargs for consistent, publication-quality output.
# fontsize=18 satisfies the 16pt floor with margin for rendering variance.
DRAW_KWARGS = dict(fontsize=18, margins=(0.12, 0.12))


@contextmanager
def _glyph_safe_rc() -> Iterator[None]:
    """Prefer DejaVu for DisCoPy text so Unicode math symbols survive savefig."""
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
        }
    ):
        yield


def render_discopy_transitive(
    subject: str = "Alice",
    verb: str = "chases",
    obj: str = "Bob",
    output_path: Optional[Path] = None,
) -> None:
    """Render a DisCoPy transitive sentence diagram.

    Args:
        subject: Subject noun.
        verb: Transitive verb.
        obj: Object noun.
        output_path: Path to save. Required.
    """
    diagram = create_discopy_transitive(subject, verb, obj)
    with _glyph_safe_rc():
        diagram.draw(
            path=str(output_path),
            figsize=(10, 5),
            **DRAW_KWARGS,
        )
    logger.info("Saved DisCoPy transitive to %s", output_path)


def render_discopy_composition(
    subject: str = "Alice",
    verb: str = "chases",
    obj: str = "Bob",
    output_path: Optional[Path] = None,
) -> None:
    """Render a DisCoPy diagram showing pre-contraction → post-contraction.

    Left panel: uncontracted word tensor n ⊗ (n.r ⊗ s ⊗ n.l) ⊗ n
    Right panel: contracted sentence type s after Cup contractions

    Args:
        subject, verb, obj: Sentence components.
        output_path: Path to save.
    """
    from discopy.drawing import Equation

    words, contracted = create_discopy_composition(subject, verb, obj)
    eq = Equation(words, contracted, symbol="→")
    with _glyph_safe_rc():
        eq.draw(
            path=str(output_path),
            figsize=(16, 6),
            **DRAW_KWARGS,
        )
    logger.info("Saved DisCoPy composition to %s", output_path)


def render_discopy_snake(
    output_path: Optional[Path] = None,
) -> None:
    """Render the snake equation (compact closure axiom).

    Shows: left snake = identity = right snake
    """
    from discopy.drawing import Equation

    left, identity, right = create_discopy_snake_equation()
    eq = Equation(left, identity, right)
    with _glyph_safe_rc():
        eq.draw(
            path=str(output_path),
            figsize=(18, 5),
            **DRAW_KWARGS,
        )
    logger.info("Saved DisCoPy snake equations to %s", output_path)


def render_discopy_passive(
    output_path: Optional[Path] = None,
) -> None:
    """Render a passive voice diagram.

    'Bob is chased by Alice' — passivization as type permutation.
    """
    diagram = create_discopy_passive("Bob", "chased", "Alice")
    with _glyph_safe_rc():
        diagram.draw(
            path=str(output_path),
            figsize=(10, 5),
            **DRAW_KWARGS,
        )
    logger.info("Saved DisCoPy passive to %s", output_path)


def render_discopy_sentence_progression(
    output_path: Optional[Path] = None,
) -> None:
    """Render a progression of sentence complexities.

    Intransitive → Transitive → Passive side by side.
    """
    from discopy.drawing import Equation

    intrans = create_discopy_intransitive("Bob", "runs")
    trans = create_discopy_transitive("Alice", "chases", "Bob")
    passive = create_discopy_passive("Bob", "chased", "Alice")

    eq = Equation(intrans, trans, passive, symbol="→")
    with _glyph_safe_rc():
        eq.draw(
            path=str(output_path),
            figsize=(24, 7),
            fontsize=18,
            margins=(0.12, 0.12),
        )
    logger.info("Saved sentence progression to %s", output_path)


def render_discopy_multilingual(
    output_path: Optional[Path] = None,
) -> None:
    """Render 'Alice chases Bob' across 6 languages.

    Shows structural isomorphism of the DisCoCat type.
    Uses Equation to display all 6 language diagrams in sequence.
    """
    from discopy.drawing import Equation

    diagrams = create_discopy_multilingual()
    diagram_list = list(diagrams.values())

    # Show first 3 languages on one line
    eq = Equation(*diagram_list[:3], symbol="≅")
    with _glyph_safe_rc():
        eq.draw(
            path=str(output_path),
            figsize=(26, 7),
            fontsize=18,
            margins=(0.08, 0.08),
        )
    logger.info("Saved multilingual diagrams to %s", output_path)


def render_discopy_ditransitive(
    output_path: Optional[Path] = None,
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

    with _glyph_safe_rc():
        diagram.draw(
            path=str(output_path),
            figsize=(12, 6),
            **DRAW_KWARGS,
        )
    logger.info("Saved ditransitive diagram to %s", output_path)


def render_discopy_discocirc_discourse(
    output_path: Optional[Path] = None,
) -> None:
    """Render a two-sentence discourse using DisCoPy diagrams.

    'Alice chases Bob. Bob runs.' composed side by side.
    """
    from discopy.drawing import Equation

    trans = create_discopy_transitive("Alice", "chases", "Bob")
    intrans = create_discopy_intransitive("Bob", "runs")

    eq = Equation(trans, intrans, symbol="⊗")
    with _glyph_safe_rc():
        eq.draw(
            path=str(output_path),
            figsize=(16, 6),
            **DRAW_KWARGS,
        )
    logger.info("Saved DisCoPy discourse to %s", output_path)


def render_discopy_three_sentence_discourse(
    output_path: Optional[Path] = None,
) -> None:
    """Render three-sentence role reversal using DisCoPy diagrams.

    Alice chases Bob. Bob catches Alice. Alice escapes.
    """
    from discopy.drawing import Equation

    s1 = create_discopy_transitive("Alice", "chases", "Bob")
    s2 = create_discopy_transitive("Bob", "catches", "Alice")
    s3 = create_discopy_intransitive("Alice", "escapes")

    eq = Equation(s1, s2, s3, symbol="⊗")
    with _glyph_safe_rc():
        eq.draw(
            path=str(output_path),
            figsize=(26, 7),
            fontsize=18,
            margins=(0.08, 0.08),
        )
    logger.info("Saved three-sentence discourse to %s", output_path)


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
