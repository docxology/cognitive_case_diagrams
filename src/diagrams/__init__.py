"""Diagrams subpackage — §3–§4c of the manuscript.

String-diagrammatic representations for compositional semantics:
    - string_diagram: DisCoCat ``Sentence`` and DisCoCirc-style ``Discourse``
    - complexity_metrics: Diagram complexity analysis (box/cup/cap counting; §4b)
    - ditransitive: Three-argument verb diagrams

DisCoPy is an *optional* runtime dependency.  The pure-Python ``Sentence`` /
``Discourse`` / ``Discourse`` machinery works without it, but the normal-form
validator, complexity-metric helpers, and the ``create_discopy_*`` factories in
``string_diagram`` require ``discopy >= 1.2``.  When DisCoPy is missing the
package emits an ``ImportWarning`` so downstream users notice the silent
feature loss instead of discovering it via a ``RuntimeError`` deep inside a
test.
"""

import warnings as _warnings

try:  # pragma: no cover - exercised by environments without discopy
    import discopy as _discopy  # noqa: F401
except ImportError:  # pragma: no cover
    _warnings.warn(
        "DisCoPy is not installed; string-diagram normal-form validation, "
        "complexity-metric helpers, and `create_discopy_*` factories will be "
        "disabled. Install with `pip install discopy>=1.2` to enable them.",
        ImportWarning,
        stacklevel=2,
    )

from .string_diagram import (
    AtomicType, Wire, Box, Sentence, Discourse,
    N, S,
)
from .complexity_metrics import (
    syntactic_complexity_score, compare_diagrams, DiagramMetrics,
    diagram_depth, diagram_width,
)
from .ditransitive import (
    DitransitiveSentence, create_ditransitive,
)

__all__ = [
    "AtomicType", "Wire", "Box", "Sentence", "Discourse", "N", "S",
    "syntactic_complexity_score", "compare_diagrams", "DiagramMetrics",
    "diagram_depth", "diagram_width",
    "DitransitiveSentence", "create_ditransitive",
]
