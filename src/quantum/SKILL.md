---
name: ccd-quantum
description: POVM-based quantum case assignment — CasePOVM, case probabilities, crisp/graded/fluid-S POVM factories, semantic state helpers. Use for §8 and §8b quantum semantics.
---

# `src/quantum/`

## When to use

- Quantum measurement models of case: POVM elements per case role, Born-rule probabilities, or hardware-oriented case assignment sketches.

## Primary imports

```python
from src.quantum import (
    CasePOVM,
    case_probability,
    crisp_case_povm, graded_case_povm, fluid_s_povm,
    semantic_state,
)
```

## Manuscript

§8, §8b.

## See also

- [`AGENTS.md`](AGENTS.md) · [`README.md`](README.md)
