"""Diagrams subpackage — §3, §4, §4b of the manuscript.

String-diagrammatic representations for compositional semantics:
    - string_diagram: DisCoCat/DisCoCirc Sentence and Discourse representations
    - complexity_metrics: Diagram complexity analysis (box/cup/cap counting)
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
