# 🤖 AGENTS.md — src/security/

## Overview

The `security` subpackage implements manuscript **§9b** ([`09b_cognitive_security.md`](../../docs/manuscript/09b_cognitive_security.md)): cognitive security as **protocol-level** type checking—prompt injection as a **decidable type violation** when roles are ill-typed in the interaction category.

> **Reference**: §9b — *Prompt Injection Is a Type Violation* (`#sec:cognitive-security`). Claims are conditional on fixed protocols, not automatic guarantees on deployed LLM APIs.

## Module Inventory

Line coverage: `uv run pytest tests/ --cov=src --cov-report=term-missing` (project root).

| Module | Key Exports |
|--------|-------------|
| `cognitive_security.py` | `TypeViolation`, `CaseFrameValidator`, `detect_type_violation()`, `injection_score()`, `topological_robustness()`, `semantic_integrity_check()` |

Public surface: [`__init__.py`](__init__.py) `__all__`.

## `cognitive_security.py`

### Core concept

A **case frame** assigns roles to entities; validity is whether pairs of roles admit a morphism in the finite `CaseCategory`. Injection-style attacks correspond to **ill-typed** role pairs or unknown roles. Enriched categories supply a second line of defense: **composition inequality** checks and **magnitude-based robustness**.

### `TypeViolation` (dataclass)

Fields: `source: CaseRole`, `target: CaseRole`, `violation_type: str`, `severity: float` ∈ [0,1], `description: str`.

### `detect_type_violation(category, source, target) -> Optional[TypeViolation]`

Returns `None` if `source == target` or if some morphism `source → target` exists in `category.morphisms`; otherwise a `TypeViolation` with `violation_type="missing_morphism"`.

```python
from src.case_systems.case_category import CaseRole, standard_case_category
from src.security import detect_type_violation

cat = standard_case_category()
v = detect_type_violation(cat, CaseRole.VOC, CaseRole.INS)  # or None if typed
```

### `injection_score(violations: list) -> float`

Mean severity capped at 1.0; empty list → `0.0`.

### `CaseFrameValidator`

Constructor: `CaseFrameValidator(category: CaseCategory | None = None, enriched: EnrichedCategory | None = None)`.

| Method | Returns | Description |
|--------|---------|-------------|
| `validate_assignment(assignments: dict)` | `list[TypeViolation]` | `assignments` maps entity name → `CaseRole`; flags unknown roles and pairs with no valid morphism in either direction |

### `topological_robustness(enriched: EnrichedCategory) -> float`

`magnitude() / n` for `n = len(enriched.roles)`; measures distinctness of relational structure.

### `semantic_integrity_check(enriched: EnrichedCategory) -> list`

Returns triples `(A, B, C)` of roles where the [0,1] composition inequality fails (see `enriched` implementation for the precise predicate).

## Security model

| Attack vector | Formalization | Code hook |
|---------------|---------------|-----------|
| Ill-typed role pair | No morphism `r1 → r2` or `r2 → r1` | `CaseFrameValidator.validate_assignment` |
| Unknown role | Role not in `category.objects` | same |
| Distributional inconsistency | Composition inequality break | `semantic_integrity_check` |
| Low structural distinctness | Small `\|C\|/n` | `topological_robustness` |

## Common patterns

```python
from src.case_systems.case_category import CaseRole, standard_case_category
from src.enriched_cat import standard_enriched_category
from src.security import (
    CaseFrameValidator,
    detect_type_violation,
    injection_score,
    semantic_integrity_check,
    topological_robustness,
)

cat = standard_case_category()
ec = standard_enriched_category()

validator = CaseFrameValidator(category=cat, enriched=ec)
violations = validator.validate_assignment({"subj": CaseRole.NOM, "obj": CaseRole.ACC})
score = injection_score(violations)

v = detect_type_violation(cat, CaseRole.NOM, CaseRole.ACC)
triples = semantic_integrity_check(ec)
R = topological_robustness(ec)
```

## See also

- [`README.md`](README.md) · [`SKILL.md`](SKILL.md)
