"""Diagrams subpackage — §3–§4c of the manuscript.

String-diagrammatic representations for compositional semantics:
    - string_diagram: DisCoCat ``Sentence`` and DisCoCirc-style ``Discourse``
    - complexity_metrics: Diagram complexity analysis (box/cup/cap counting; §4b)
    - ditransitive: Three-argument verb diagrams
"""

from .string_diagram import (
    AtomicType, Wire, Box, Sentence, Discourse,
    N, S,
)
from .complexity_metrics import (
    syntactic_complexity_score, compare_diagrams, DiagramMetrics,
)
from .ditransitive import (
    DitransitiveSentence, create_ditransitive,
)

__all__ = [
    "AtomicType", "Wire", "Box", "Sentence", "Discourse", "N", "S",
    "syntactic_complexity_score", "compare_diagrams", "DiagramMetrics",
    "DitransitiveSentence", "create_ditransitive",
]
