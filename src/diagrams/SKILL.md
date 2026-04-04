---
name: ccd-diagrams
description: DisCoCat/DisCoCirc-style string diagrams, complexity metrics, ditransitive constructions. Use for §3–§4c compositional semantics, §4b complexity, and §4c discourse.
---

# `src/diagrams/`

## When to use

- Building `Sentence` / `Discourse` diagrams, ditransitives, or syntactic complexity scores.
- Anything that composes case-theoretic types as string diagrams (depends on `case_systems` types indirectly via diagram API).

## Primary imports

```python
from src.diagrams import (
    AtomicType, Wire, Box, Sentence, Discourse, N, S,
    syntactic_complexity_score, compare_diagrams, DiagramMetrics,
    DitransitiveSentence, create_ditransitive,
)
```

## Manuscript

§3–§4 (pregroup / string diagrams / DisCoCat), §4b (compact closure and complexity metrics), §4c (discourse / DisCoCirc).

## See also

- [`AGENTS.md`](AGENTS.md) · [`README.md`](README.md)
