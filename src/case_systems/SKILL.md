---
name: ccd-case-systems
description: Linguistic case as a category — CaseRole, Morphism, CaseCategory, alignment functors, natural transformations, Fluid-S. Use for §2 manuscript code and anything that must not depend on other src subpackages.
---

# `src/case_systems/`

## When to use

- Defining or comparing case inventories, morphisms, or cross-linguistic alignment functors.
- Verifying a natural transformation with `NaturalTransformation.naturality_holds()` (complete components required).
- Fluid-S / volition-scoped alignment without pulling in diagrams or cognitive modules.

## Primary imports

```python
from src.case_systems import (
    CaseRole, Morphism, CaseCategory,
    standard_case_category, minimal_case_category, introductory_case_category,
    accusative_alignment, ergative_alignment, tripartite_alignment, active_stative_alignment,
    AlignmentFunctor, accusative_to_ergative_functor, tripartite_functor,
    ComponentMorphism, NaturalTransformation, IdentityNaturalTransformation, compose_transformations,
    FluidSFunctor, VolitionContext,
)
```

## Manuscript

§2, §2b — categorical case; foundation for later string diagrams and enrichment.

## See also

- [`AGENTS.md`](AGENTS.md) · [`README.md`](README.md)
