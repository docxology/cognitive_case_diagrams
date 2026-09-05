---
name: ccd-case-systems
description: Linguistic case formally typed as a category — CaseRole, Morphism, AlignmentFunctor, MonoidalFunctor, natural transformations. Use for §2/§2b categorical case, downstream §7c DAIF alignment, and the §9b protocol-level type-violation story.
---

# `src/case_systems/`

## When to use

- Defining, comparing, or mathematically grading case inventories and cross-linguistic functors.
- Evaluating **DAIF Surprisal (N400/P600)** using `CaseCategory.assess_daif_surprisal()`.
- Flagging ill-typed role bindings (`ACC -> NOM`) via `src.security.cognitive_security.CaseFrameValidator.validate_assignment()`.
- Checking tensor preservation `F(A⊗B)` with `MonoidalFunctor.preserves_tensor()` — a specification-level check on the alignment map, not a guarantee about a deployed model.
- Verifying a natural transformation with `NaturalTransformation.naturality_holds()`.

## Primary imports

```python
from src.case_systems import (
    CaseRole, Morphism, CaseCategory,
    standard_case_category, minimal_case_category,
    accusative_alignment, ergative_alignment, tripartite_alignment, active_stative_alignment,
    AlignmentFunctor, MonoidalFunctor, accusative_to_ergative_functor,
    ComponentMorphism, NaturalTransformation, IdentityNaturalTransformation, compose_transformations,
    FluidSFunctor, VolitionContext,
)
```

## Manuscript

§2, §2b — categorical case; foundation for later string diagrams and enrichment.

## See also

- [`AGENTS.md`](AGENTS.md) · [`README.md`](README.md)
