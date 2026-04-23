---
name: ccd-diagrams
description: DisCoCat/DisCoCirc-style string diagrams, complexity metrics, ditransitive constructions, discourse-level prompt scanning. Use for manuscript §3–§4c (and cross-links to §5b magnitude homology metrics, §9b protocol-level checks where `Discourse` is used).
---

# `src/diagrams/`

## When to use

- Building `Sentence` / `Discourse` diagrams and measuring their structural quantum bounds.
- Calculating `MagnitudeHomologyMetrics` to bound parameter decoherence.
- Scanning discourse histories for non-cartesian topological adversarial hijacking by feeding `Discourse.role_history` slices into `src.security.cognitive_security.CaseFrameValidator.validate_assignment()`.
- Anything that composes case-theoretic types as string diagrams.

## Primary imports

```python
from src.diagrams import (
    AtomicType, Wire, Box, Sentence, Discourse, N, S,
    syntactic_complexity_score, MagnitudeHomologyMetrics, compute_quantum_magnitude_homology,
    compare_diagrams, DiagramMetrics,
    DitransitiveSentence, create_ditransitive,
)
```

## Manuscript

§3–§4c (pregroups through DisCoCirc; §4b complexity; §4c discourse); `complexity_metrics` also supports magnitude-homology metrics tied to §5b in the theory map.

## See also

- [`AGENTS.md`](AGENTS.md) · [`README.md`](README.md)
