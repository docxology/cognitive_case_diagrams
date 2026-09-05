---
name: ccd-diagrams
description: DisCoCat/DisCoCirc-style string diagrams, complexity metrics, ditransitive constructions, discourse-level prompt scanning. Use for manuscript §3–§4c (and cross-links to §5b magnitude homology metrics, §9b protocol-level checks where `Discourse` is used).
---

# `src/diagrams/`

## When to use

- Building `Sentence` / `Discourse` diagrams and measuring their structural complexity.
- Computing `MagnitudeHomologyMetrics` — a scalar syntactic complexity, a 1-D hole count, an estimated decoherence rate, and a commutation flag. It is **not** a graded homology object; see [`AGENTS.md`](AGENTS.md).
- Scanning discourse histories for role-reversal patterns by feeding `Discourse.role_history` slices into `src.security.cognitive_security.CaseFrameValidator.validate_assignment()`.
- Anything that composes case-theoretic types as string diagrams.

## Primary imports

```python
from src.diagrams import (
    AtomicType, Wire, Box, Sentence, Discourse, N, S,
    syntactic_complexity_score, compare_diagrams, DiagramMetrics,
    diagram_depth, diagram_width,
    DitransitiveSentence, create_ditransitive,
)
# Magnitude-homology helpers are not re-exported by the package __init__;
# import them from the module directly.
from src.diagrams.complexity_metrics import (
    MagnitudeHomologyMetrics, compute_pqc_decoherence_proxy,
)
```

## Manuscript

§3–§4c (pregroups through DisCoCirc; §4b complexity; §4c discourse); `complexity_metrics` also supports magnitude-homology metrics tied to §5b in the theory map.

## See also

- [`AGENTS.md`](AGENTS.md) · [`README.md`](README.md)
