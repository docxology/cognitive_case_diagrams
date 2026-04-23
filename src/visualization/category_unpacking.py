"""Multi-panel category-theory *unpacking* figures.

These figures complement the raw DisCoPy string-diagram outputs with
pedagogical, step-by-step decompositions of the key category-theoretic
constructions used throughout the manuscript:

* :func:`render_pregroup_reduction_unpacking` — four panels walking the
  DisCoCat reduction of a transitive sentence from raw word types through
  parallel tensor, cup contractions, and finally the sentence-type
  normal form. Used alongside Fig. ``fig:discopy-transitive`` in §3.

* :func:`render_discocirc_entity_persistence` — three panels plus a
  role-history ribbon, tracking the same entity across the three-sentence
  discourse ``Alice chases Bob. Bob fears Alice. Alice smiles.``.
  Used alongside Fig. ``fig:three-sentence-discourse`` in §4c.

* :func:`render_snake_equation_unpacking` — three panels stating the
  compact-closure axiom $(\\varepsilon_n \\otimes 1_n) \\circ (1_n \\otimes \\eta_n) = 1_n$
  with explicit η and ε labels.  Used alongside Fig. ``fig:discopy-snake`` in §4b.

All three functions are pure matplotlib (no DisCoPy dependency) so they
render identically in every environment, and they give us full control
over per-case wire colouring, annotations, and typography.
"""
from __future__ import annotations

import logging
from typing import Optional

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path as MplPath

from .styles import (
    CASE_COLORS,
    FONT_SIZE_TITLE,
    FONT_SIZE_LABEL,
    FONT_SIZE_ANNOTATION,
    FONT_SIZE_FLOOR,
    FIGURE_DPI,
    COLOR_EDGE,
    COLOR_TEXT,
    COLOR_WIRE,
    COLOR_ENTITY_WIRE,
    LINE_WIDTH_EDGE,
)

logger = logging.getLogger(__name__)


# ─── helpers ─────────────────────────────────────────────────────────────────

def _clean_ax(ax, xlim=(0, 1), ylim=(0, 1), *, aspect="equal") -> None:
    """Strip axes to a clean drawing canvas.

    Pass ``aspect="auto"`` for ribbons / elongated panels where a strict
    1:1 aspect would compress the content.
    """
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if aspect is not None:
        ax.set_aspect(aspect)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def _word_box(ax, x, y, width, height, label, facecolor, *, text_color="white") -> None:
    rect = mpatches.FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width, height,
        boxstyle="round,pad=0.02",
        facecolor=facecolor,
        edgecolor=COLOR_EDGE,
        linewidth=LINE_WIDTH_EDGE,
        alpha=0.95,
    )
    ax.add_patch(rect)
    ax.text(
        x, y, label,
        ha="center", va="center",
        fontsize=FONT_SIZE_LABEL, fontweight="bold",
        color=text_color,
    )


def _wire(ax, x0, y0, x1, y1, color=None, lw=2.2, linestyle="-") -> None:
    ax.plot(
        [x0, x1], [y0, y1],
        color=color or COLOR_TEXT,
        linewidth=lw,
        linestyle=linestyle,
        solid_capstyle="round",
    )


def _cup(ax, x_left, x_right, y_top, depth=0.08, *, color=None, lw=2.2) -> None:
    """Draw a downward cup (ε) connecting two wires."""
    ctrl_y = y_top - depth
    path_data = [
        (MplPath.MOVETO, (x_left, y_top)),
        (MplPath.CURVE4, (x_left, ctrl_y)),
        (MplPath.CURVE4, (x_right, ctrl_y)),
        (MplPath.CURVE4, (x_right, y_top)),
    ]
    codes, verts = zip(*path_data)
    patch = mpatches.PathPatch(
        MplPath(verts, codes),
        edgecolor=color or COLOR_TEXT,
        facecolor="none",
        linewidth=lw,
    )
    ax.add_patch(patch)


def _cap(ax, x_left, x_right, y_bot, height=0.08, *, color=None, lw=2.2) -> None:
    """Draw an upward cap (η) connecting two wires."""
    ctrl_y = y_bot + height
    path_data = [
        (MplPath.MOVETO, (x_left, y_bot)),
        (MplPath.CURVE4, (x_left, ctrl_y)),
        (MplPath.CURVE4, (x_right, ctrl_y)),
        (MplPath.CURVE4, (x_right, y_bot)),
    ]
    codes, verts = zip(*path_data)
    patch = mpatches.PathPatch(
        MplPath(verts, codes),
        edgecolor=color or COLOR_TEXT,
        facecolor="none",
        linewidth=lw,
    )
    ax.add_patch(patch)


# ─── figure 1: pregroup reduction unpacking ─────────────────────────────────

def render_pregroup_reduction_unpacking(
    output_path: Optional[str] = None,
    *,
    subject: str = "Alice",
    verb: str = "chases",
    obj: str = "Bob",
) -> str:
    """Four-panel walkthrough of a transitive-sentence pregroup reduction.

    The panels show, left-to-right:

    1. *Raw pregroup types.* Each word is stood up as a typed box with
       its full type signature dangling below (``n`` for nouns,
       ``n^r ⊗ s ⊗ n^l`` for the verb).
    2. *Parallel composition.* The same three boxes tensored
       ``Alice ⊗ chases ⊗ Bob`` with all five wires dangling.
    3. *Cup contractions.* Two cups ε_n are applied, one between
       Alice's ``n`` and the verb's ``n^r`` (left argument), one between
       the verb's ``n^l`` and Bob's ``n`` (right argument).
    4. *Normal form.* Only the ``s`` wire remains — the sentence type.

    Args:
        output_path: PNG path to save; defaults to
            ``pregroup_reduction_unpacking.png``.
        subject, verb, obj: Lexical content. Defaults match the
            canonical example used in §3 and §4.

    Returns:
        The resolved output path as a string.
    """
    fig, axes = plt.subplots(1, 4, figsize=(20, 6), dpi=FIGURE_DPI)

    nom = CASE_COLORS["NOM"]
    acc = CASE_COLORS["ACC"]
    sent = CASE_COLORS["S"]

    # panel 1 — raw types
    ax = axes[0]
    _clean_ax(ax)
    _word_box(ax, 0.20, 0.72, 0.22, 0.18, subject, nom)
    _word_box(ax, 0.50, 0.72, 0.22, 0.18, verb,    sent)
    _word_box(ax, 0.80, 0.72, 0.22, 0.18, obj,     acc)

    # dangling wires
    _wire(ax, 0.20, 0.63, 0.20, 0.48, color=nom)
    _wire(ax, 0.42, 0.63, 0.42, 0.48, color=sent)
    _wire(ax, 0.50, 0.63, 0.50, 0.48, color=sent)
    _wire(ax, 0.58, 0.63, 0.58, 0.48, color=sent)
    _wire(ax, 0.80, 0.63, 0.80, 0.48, color=acc)
    # type labels below each wire, well-separated
    ax.text(0.20, 0.40, r"$n$", ha="center", fontsize=FONT_SIZE_LABEL, color=nom,  fontweight="bold")
    ax.text(0.42, 0.40, r"$n^r$", ha="center", fontsize=FONT_SIZE_ANNOTATION, color=sent, fontweight="bold")
    ax.text(0.50, 0.40, r"$s$",   ha="center", fontsize=FONT_SIZE_ANNOTATION, color=sent, fontweight="bold")
    ax.text(0.58, 0.40, r"$n^l$", ha="center", fontsize=FONT_SIZE_ANNOTATION, color=sent, fontweight="bold")
    ax.text(0.80, 0.40, r"$n$", ha="center", fontsize=FONT_SIZE_LABEL, color=acc, fontweight="bold")
    ax.text(0.50, 0.28, r"type$(\mathrm{chases}) = n^r \otimes s \otimes n^l$",
            ha="center", fontsize=FONT_SIZE_ANNOTATION, color=COLOR_TEXT, fontstyle="italic")
    ax.set_title("1. Raw pregroup types", fontsize=FONT_SIZE_LABEL, fontweight="bold")
    ax.text(0.50, 0.10,
            "Three word boxes: each with its pregroup type signature",
            ha="center", fontsize=FONT_SIZE_ANNOTATION, color=COLOR_TEXT, fontstyle="italic")

    # panel 2 — parallel tensor
    ax = axes[1]
    _clean_ax(ax)
    _word_box(ax, 0.15, 0.78, 0.20, 0.16, subject, nom)
    _word_box(ax, 0.50, 0.78, 0.30, 0.16, verb,    sent)
    _word_box(ax, 0.85, 0.78, 0.20, 0.16, obj,     acc)
    # five wires
    for xi, color, label in [
        (0.15, nom,  r"$n$"),
        (0.38, sent, r"$n^r$"),
        (0.50, sent, r"$s$"),
        (0.62, sent, r"$n^l$"),
        (0.85, acc,  r"$n$"),
    ]:
        _wire(ax, xi, 0.70, xi, 0.22, color=color, lw=2.0)
        ax.text(xi, 0.16, label, ha="center", fontsize=FONT_SIZE_ANNOTATION, color=color, fontweight="bold")
    ax.set_title("2. Parallel composition (tensor $\\otimes$)", fontsize=FONT_SIZE_LABEL, fontweight="bold")

    # panel 3 — cup contractions
    ax = axes[2]
    _clean_ax(ax)
    _word_box(ax, 0.15, 0.80, 0.20, 0.14, subject, nom)
    _word_box(ax, 0.50, 0.80, 0.30, 0.14, verb,    sent)
    _word_box(ax, 0.85, 0.80, 0.20, 0.14, obj,     acc)
    for xi, color in [(0.15, nom), (0.38, sent), (0.50, sent), (0.62, sent), (0.85, acc)]:
        _wire(ax, xi, 0.73, xi, 0.45, color=color, lw=2.0)
    # left cup: n (Alice) — n^r (verb)
    _cup(ax, 0.15, 0.38, 0.45, depth=0.08, color=nom, lw=2.4)
    # right cup: n^l (verb) — n (Bob)
    _cup(ax, 0.62, 0.85, 0.45, depth=0.08, color=acc, lw=2.4)
    # central s wire survives
    _wire(ax, 0.50, 0.45, 0.50, 0.18, color=sent, lw=2.4)
    ax.text(0.265, 0.33, r"$\varepsilon_n$", ha="center", fontsize=FONT_SIZE_LABEL, color=nom, fontweight="bold")
    ax.text(0.735, 0.33, r"$\varepsilon_n$", ha="center", fontsize=FONT_SIZE_LABEL, color=acc, fontweight="bold")
    ax.text(0.50, 0.13, r"$s$", ha="center", fontsize=FONT_SIZE_LABEL, color=sent, fontweight="bold")
    ax.set_title("3. Cup contractions $\\varepsilon_n$", fontsize=FONT_SIZE_LABEL, fontweight="bold")

    # panel 4 — normal form
    ax = axes[3]
    _clean_ax(ax)
    _word_box(ax, 0.50, 0.80, 0.50, 0.14, f"{subject} {verb} {obj}", sent)
    _wire(ax, 0.50, 0.73, 0.50, 0.22, color=sent, lw=3.0)
    ax.text(0.50, 0.16, r"$s$", ha="center", fontsize=FONT_SIZE_TITLE, color=sent, fontweight="bold")
    ax.set_title("4. Normal form", fontsize=FONT_SIZE_LABEL, fontweight="bold")
    ax.text(0.50, 0.06,
            "Only the $s$ wire survives — the sentence type",
            ha="center", fontsize=FONT_SIZE_ANNOTATION, color=COLOR_TEXT, fontstyle="italic")

    fig.suptitle(
        f"Pregroup reduction of “{subject} {verb} {obj}”: "
        "raw types $\\to$ tensor $\\to$ cups $\\to$ normal form",
        fontsize=FONT_SIZE_TITLE, fontweight="bold", y=1.02,
    )
    fig.tight_layout()

    if output_path is None:
        output_path = "pregroup_reduction_unpacking.png"
    fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved pregroup reduction unpacking to %s", output_path)
    return str(output_path)


# ─── figure 2: DisCoCirc entity persistence ─────────────────────────────────

def render_discocirc_entity_persistence(
    output_path: Optional[str] = None,
) -> str:
    """Three-panel DisCoCirc unpacking with entity-persistence ribbon.

    Shows the canonical discourse
    ``Alice chases Bob. Bob fears Alice. Alice smiles.`` with:

    * Three sentence panels (DisCoCat string diagrams) side by side.
    * A bottom *role-history ribbon* explicitly labelling the case-role
      trajectory of Alice (NOM $\\to$ ACC $\\to$ NOM) and Bob (ACC $\\to$ NOM).
    * Coloured identity threads linking each entity's instances across
      sentences — the diagrammatic signature of DisCoCirc's Frobenius-spider
      entity wires.

    Args:
        output_path: PNG path to save; defaults to
            ``discocirc_entity_persistence.png``.

    Returns:
        The resolved output path as a string.
    """
    fig = plt.figure(figsize=(20, 8), dpi=FIGURE_DPI, constrained_layout=True)
    gs = fig.add_gridspec(2, 3, height_ratios=[3, 1], hspace=0.25, wspace=0.15)
    sent_axes = [fig.add_subplot(gs[0, i]) for i in range(3)]
    ribbon_ax = fig.add_subplot(gs[1, :])

    nom = CASE_COLORS["NOM"]
    acc = CASE_COLORS["ACC"]
    sent = CASE_COLORS["S"]
    alice_color = "#6366F1"   # indigo — Alice entity thread
    bob_color   = "#F59E0B"   # amber  — Bob   entity thread

    # panel 1 — Alice(NOM) chases Bob(ACC)
    ax = sent_axes[0]
    _clean_ax(ax)
    _word_box(ax, 0.22, 0.80, 0.24, 0.14, "Alice",  alice_color)
    _word_box(ax, 0.55, 0.80, 0.28, 0.14, "chases", sent)
    _word_box(ax, 0.82, 0.80, 0.24, 0.14, "Bob",    bob_color)
    for xi, color in [(0.22, alice_color), (0.45, sent), (0.55, sent), (0.65, sent), (0.82, bob_color)]:
        _wire(ax, xi, 0.73, xi, 0.40, color=color, lw=2.0)
    _cup(ax, 0.22, 0.45, 0.40, depth=0.08, color=alice_color, lw=2.3)
    _cup(ax, 0.65, 0.82, 0.40, depth=0.08, color=bob_color,   lw=2.3)
    _wire(ax, 0.55, 0.40, 0.55, 0.14, color=sent, lw=2.6)
    ax.text(0.22, 0.34, "NOM", ha="center", fontsize=FONT_SIZE_ANNOTATION, color=nom, fontweight="bold")
    ax.text(0.82, 0.34, "ACC", ha="center", fontsize=FONT_SIZE_ANNOTATION, color=acc, fontweight="bold")
    ax.text(0.55, 0.08, r"$s_1$", ha="center", fontsize=FONT_SIZE_LABEL, color=sent, fontweight="bold")
    ax.set_title("1. Alice chases Bob", fontsize=FONT_SIZE_LABEL, fontweight="bold")

    # panel 2 — Bob(NOM) fears Alice(ACC)
    ax = sent_axes[1]
    _clean_ax(ax)
    _word_box(ax, 0.22, 0.80, 0.24, 0.14, "Bob",   bob_color)
    _word_box(ax, 0.55, 0.80, 0.28, 0.14, "fears", sent)
    _word_box(ax, 0.82, 0.80, 0.24, 0.14, "Alice", alice_color)
    for xi, color in [(0.22, bob_color), (0.45, sent), (0.55, sent), (0.65, sent), (0.82, alice_color)]:
        _wire(ax, xi, 0.73, xi, 0.40, color=color, lw=2.0)
    _cup(ax, 0.22, 0.45, 0.40, depth=0.08, color=bob_color,   lw=2.3)
    _cup(ax, 0.65, 0.82, 0.40, depth=0.08, color=alice_color, lw=2.3)
    _wire(ax, 0.55, 0.40, 0.55, 0.14, color=sent, lw=2.6)
    ax.text(0.22, 0.34, "NOM", ha="center", fontsize=FONT_SIZE_ANNOTATION, color=nom, fontweight="bold")
    ax.text(0.82, 0.34, "ACC", ha="center", fontsize=FONT_SIZE_ANNOTATION, color=acc, fontweight="bold")
    ax.text(0.55, 0.08, r"$s_2$", ha="center", fontsize=FONT_SIZE_LABEL, color=sent, fontweight="bold")
    ax.set_title("2. Bob fears Alice  (roles swap)", fontsize=FONT_SIZE_LABEL, fontweight="bold")

    # panel 3 — Alice(NOM) smiles
    ax = sent_axes[2]
    _clean_ax(ax)
    _word_box(ax, 0.30, 0.80, 0.24, 0.14, "Alice",  alice_color)
    _word_box(ax, 0.65, 0.80, 0.24, 0.14, "smiles", sent)
    for xi, color in [(0.30, alice_color), (0.58, sent), (0.65, sent)]:
        _wire(ax, xi, 0.73, xi, 0.40, color=color, lw=2.0)
    _cup(ax, 0.30, 0.58, 0.40, depth=0.08, color=alice_color, lw=2.3)
    _wire(ax, 0.65, 0.40, 0.65, 0.14, color=sent, lw=2.6)
    ax.text(0.30, 0.34, "NOM", ha="center", fontsize=FONT_SIZE_ANNOTATION, color=nom, fontweight="bold")
    ax.text(0.65, 0.08, r"$s_3$", ha="center", fontsize=FONT_SIZE_LABEL, color=sent, fontweight="bold")
    ax.set_title("3. Alice smiles", fontsize=FONT_SIZE_LABEL, fontweight="bold")

    # role-history ribbon at the bottom — non-equal aspect so it breathes
    _clean_ax(ribbon_ax, xlim=(0, 1), ylim=(0, 1), aspect="auto")
    ribbon_ax.set_title("Role-history ribbon (entity persistence via Frobenius spiders)",
                        fontsize=FONT_SIZE_LABEL, fontweight="bold", loc="left")
    # Alice track
    alice_y = 0.65
    ribbon_ax.text(0.02, alice_y, "Alice", fontsize=FONT_SIZE_LABEL, color=alice_color, fontweight="bold", va="center")
    for i, (x, role) in enumerate([(0.22, "NOM"), (0.52, "ACC"), (0.82, "NOM")]):
        color_ = CASE_COLORS[role]
        circle = mpatches.Circle((x, alice_y), 0.035, facecolor=color_, edgecolor=alice_color, linewidth=2, zorder=5)
        ribbon_ax.add_patch(circle)
        ribbon_ax.text(x, alice_y - 0.17, role, ha="center", fontsize=FONT_SIZE_ANNOTATION, color=color_, fontweight="bold")
    ribbon_ax.annotate("", xy=(0.485, alice_y), xytext=(0.255, alice_y),
                       arrowprops=dict(arrowstyle="->", color=alice_color, lw=2.2))
    ribbon_ax.annotate("", xy=(0.785, alice_y), xytext=(0.555, alice_y),
                       arrowprops=dict(arrowstyle="->", color=alice_color, lw=2.2))
    # Bob track
    bob_y = 0.20
    ribbon_ax.text(0.02, bob_y, "Bob", fontsize=FONT_SIZE_LABEL, color=bob_color, fontweight="bold", va="center")
    for i, (x, role) in enumerate([(0.22, "ACC"), (0.52, "NOM")]):
        color_ = CASE_COLORS[role]
        circle = mpatches.Circle((x, bob_y), 0.035, facecolor=color_, edgecolor=bob_color, linewidth=2, zorder=5)
        ribbon_ax.add_patch(circle)
        ribbon_ax.text(x, bob_y - 0.17, role, ha="center", fontsize=FONT_SIZE_ANNOTATION, color=color_, fontweight="bold")
    ribbon_ax.annotate("", xy=(0.485, bob_y), xytext=(0.255, bob_y),
                       arrowprops=dict(arrowstyle="->", color=bob_color, lw=2.2))
    ribbon_ax.text(0.82, bob_y, "(absent)", ha="center", fontsize=FONT_SIZE_ANNOTATION, color=COLOR_TEXT, fontstyle="italic", va="center")

    fig.suptitle(
        "DisCoCirc entity persistence: case roles of the *same* entity across three sentences",
        fontsize=FONT_SIZE_TITLE, fontweight="bold",
    )

    if output_path is None:
        output_path = "discocirc_entity_persistence.png"
    fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved DisCoCirc entity persistence to %s", output_path)
    return str(output_path)


# ─── figure 3: snake equation unpacking ─────────────────────────────────────

def render_snake_equation_unpacking(
    output_path: Optional[str] = None,
) -> str:
    """Three-panel visual derivation of the compact-closure snake equation.

    Panels (left to right):

    1. *LHS zigzag* — the composite $(\\varepsilon_n \\otimes 1_n) \\circ (1_n \\otimes \\eta_n)$
       drawn with labelled cup (ε) and cap (η).
    2. *Equality* — the identity wire $1_n$ with an explicit ``=`` bridging
       the two panels.
    3. *Axiom recap* — the defining compact-closure equations
       ``(ε_n ⊗ 1) ∘ (1 ⊗ η_n) = 1_n`` and
       ``(1 ⊗ ε_n) ∘ (η_n ⊗ 1) = 1_n`` written out for reference.

    Args:
        output_path: PNG path to save; defaults to
            ``snake_equation_unpacking.png``.

    Returns:
        The resolved output path as a string.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=FIGURE_DPI,
                             gridspec_kw={"width_ratios": [1.1, 1.0, 1.3]})

    wire_color = CASE_COLORS["S"]

    # panel 1 — zigzag LHS
    ax = axes[0]
    _clean_ax(ax)
    # upper wire (vertical identity on top)
    _wire(ax, 0.25, 0.92, 0.25, 0.58, color=wire_color, lw=2.6)
    # cap η at middle
    _cap(ax, 0.25, 0.55, 0.58, height=0.12, color=wire_color, lw=2.6)
    # cup ε beneath cap
    _cup(ax, 0.55, 0.85, 0.42, depth=0.12, color=wire_color, lw=2.6)
    # lower wire continuation
    _wire(ax, 0.85, 0.42, 0.85, 0.08, color=wire_color, lw=2.6)
    # top / bottom type labels
    ax.text(0.25, 0.97, r"$n$", ha="center", fontsize=FONT_SIZE_LABEL, color=wire_color, fontweight="bold")
    ax.text(0.85, 0.03, r"$n$", ha="center", fontsize=FONT_SIZE_LABEL, color=wire_color, fontweight="bold")
    # cap/cup annotations
    ax.text(0.40, 0.73, r"$\eta_n$", ha="center", fontsize=FONT_SIZE_LABEL, color=wire_color, fontweight="bold")
    ax.text(0.70, 0.27, r"$\varepsilon_n$", ha="center", fontsize=FONT_SIZE_LABEL, color=wire_color, fontweight="bold")
    # internal type labels on the bent wires
    ax.text(0.42, 0.50, r"$n^r$", ha="center", fontsize=FONT_SIZE_ANNOTATION, color=COLOR_TEXT)
    ax.set_title(
        r"1. LHS zigzag $(\varepsilon_n \otimes 1_n)\circ(1_n \otimes \eta_n)$",
        fontsize=FONT_SIZE_LABEL - 1, fontweight="bold",
    )

    # panel 2 — identity RHS with explicit '='
    ax = axes[1]
    _clean_ax(ax)
    ax.text(0.12, 0.50, "$=$", ha="center", va="center",
            fontsize=FONT_SIZE_TITLE * 2, color=COLOR_EDGE, fontweight="bold")
    _wire(ax, 0.55, 0.92, 0.55, 0.08, color=wire_color, lw=3.0)
    ax.text(0.55, 0.97, r"$n$", ha="center", fontsize=FONT_SIZE_LABEL, color=wire_color, fontweight="bold")
    ax.text(0.55, 0.03, r"$n$", ha="center", fontsize=FONT_SIZE_LABEL, color=wire_color, fontweight="bold")
    ax.text(0.55, 0.50, r"$1_n$", ha="left", fontsize=FONT_SIZE_LABEL, color=wire_color, fontweight="bold")
    ax.set_title("2. Identity $1_n$", fontsize=FONT_SIZE_LABEL, fontweight="bold")

    # panel 3 — axiom recap
    ax = axes[2]
    _clean_ax(ax)
    ax.text(0.50, 0.85, "Compact-closure axiom",
            ha="center", fontsize=FONT_SIZE_LABEL, color=COLOR_EDGE, fontweight="bold")
    ax.text(0.50, 0.60,
            r"$(\varepsilon_n \otimes 1_n) \circ (1_n \otimes \eta_n) \;=\; 1_n$",
            ha="center", fontsize=FONT_SIZE_LABEL, color=wire_color)
    ax.text(0.50, 0.42,
            r"$(1_n \otimes \varepsilon_n) \circ (\eta_n \otimes 1_n) \;=\; 1_n$",
            ha="center", fontsize=FONT_SIZE_LABEL, color=wire_color)
    ax.text(0.50, 0.18,
            "Both zigzags straighten.\n"
            r"$\eta_n: 1 \to n \otimes n^r$ (cap)"
            "\n"
            r"$\varepsilon_n: n^r \otimes n \to 1$ (cup)",
            ha="center", fontsize=FONT_SIZE_ANNOTATION, color=COLOR_TEXT, fontstyle="italic",
            linespacing=1.5)
    ax.set_title("3. Axiom recap", fontsize=FONT_SIZE_LABEL, fontweight="bold")

    fig.suptitle(
        "Snake equation unpacking — why cup-cap pairs cancel to the identity wire",
        fontsize=FONT_SIZE_TITLE, fontweight="bold", y=1.02,
    )
    fig.tight_layout()

    if output_path is None:
        output_path = "snake_equation_unpacking.png"
    fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved snake equation unpacking to %s", output_path)
    return str(output_path)


__all__ = [
    "render_pregroup_reduction_unpacking",
    "render_discocirc_entity_persistence",
    "render_snake_equation_unpacking",
]
