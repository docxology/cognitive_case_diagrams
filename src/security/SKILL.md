---
name: ccd-security
description: Cognitive security — type violations, CaseFrameValidator, injection scoring, topological robustness, semantic integrity. Use for §9b adversarial and type-checking narratives.
---

# `src/security/`

## When to use

- Validating frames against an enriched case category, scoring adversarial injections, or reporting robustness / integrity diagnostics.

## Primary imports

```python
from src.security import (
    TypeViolation,
    CaseFrameValidator,
    detect_type_violation,
    injection_score,
    topological_robustness,
    semantic_integrity_check,
)
```

## Manuscript

§9b.

## See also

- [`AGENTS.md`](AGENTS.md) · [`README.md`](README.md)
