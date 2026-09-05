---
name: ccd-topos-theory
description: Geometric theories, classifying toposes, Morita necessary-condition screens, theory builders. Use for §6 topos-theoretic semantics and bridges between syntactic/semantic theories.
---

# `src/topos_theory/`

## When to use

- Encoding geometric theories, classifying toposes, or comparing theories via Morita equivalence helpers.
- Connecting typological or enriched setups to topos-level structure.

`check_morita_equivalence(topos1, topos2)` takes two `ClassifyingTopos` values and
returns `(not_ruled_out, mismatches)`. It screens **necessary conditions only** —
a `True` never establishes equivalence.

## Primary imports

```python
from src.topos_theory import (
    TheoryType, Axiom, GeometricTheory, ClassifyingTopos,
    check_morita_equivalence,
    build_typological_theory, build_enriched_theory,
)
```

## Manuscript

§6.

## See also

- [`AGENTS.md`](AGENTS.md) · [`README.md`](README.md)
