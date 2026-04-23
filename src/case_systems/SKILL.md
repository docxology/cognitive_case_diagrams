---
name: ccd-case-systems
description: Linguistic case formally typed as an analytic category — CaseRole, Morphism, AlignmentFunctor, MonoidalFunctor, Natural Transformations. Crucial for §2 core topology, downstream §7c DAIF alignment, and §9b adversarial injection formal verification.
---

# `src/case_systems/`

## When to use

- Defining, comparing, or mathematically grading case inventories and cross-linguistic functors.
- Evaluating **DAIF Surprisal (N400/P600)** using `CaseCategory.assess_daif_surprisal()`.
- Validating adversarial NLP topological bindings (`ACC -> NOM`) via `src.security.cognitive_security.CaseFrameValidator.validate_assignment()`.
- Checking Fibrational F(A⊗B) tensor preservation with `MonoidalFunctor` against multi-turn chain-of-thought hijacking.
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
