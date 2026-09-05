# Module: `security` — Prompt Injection Is a Type Violation (§9b)

> **Package**: `src.security`
> **Manuscript**: §9b [`09b_cognitive_security.md`](../../docs/manuscript/09b_cognitive_security.md) (`#sec:cognitive-security`)
> **Dependencies**: `case_systems`, `enriched_cat`
> **Test files**: `tests/test_security*.py`

---

## Purpose

The `security` package formalizes **prompt injection as decidable categorical type violation** under a fixed interaction protocol. The core insight (§9b): case frames impose categorical type constraints on linguistic input, and an adversarial prompt injection attempts to insert an ill-typed case assignment that violates the categorical composition rules. Detection is decidable because type-checking in a finite category is decidable. This is a **specification-level** story aligned with [`09b_cognitive_security.md`](../../docs/manuscript/09b_cognitive_security.md), not an automatic guarantee on deployed LLM APIs.

Key capabilities:

1. **Type violation detection**: identify morphisms not licensed by the case category
2. **Injection scoring**: quantify severity of case-frame injection attempts
3. **Topological robustness**: magnitude-based robustness summary $\lvert\mathcal{C}\rvert / n$
4. **Semantic integrity**: enriched composition inequality as an integrity invariant

---

## Architecture

```text
security/
├── __init__.py               # 6 exported symbols
└── cognitive_security.py     # CaseFrameValidator, TypeViolation, detection functions
```

### Dependency Position

```text
case_systems → security
enriched_cat →↗
                ↓
           visualization.security_plots
```

---

## Module Reference

### `cognitive_security.py` — Complete API

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `TypeViolation` | `@dataclass` | Record: `source`, `target`, `violation_type`, `severity ∈ [0,1]`, `description` |
| `CaseFrameValidator` | class | Validates case frames against categorical constraints |
| `detect_type_violation()` | function | Identifies ill-typed case assignments |
| `injection_score()` | function | Quantifies severity of case-frame injection |
| `topological_robustness()` | function | Normalized magnitude $\lvert\mathcal{C}\rvert / n$ as a robustness summary |
| `semantic_integrity_check()` | function | Returns the enriched triples violating the composition inequality |

### `TypeViolation`

Records a detected violation with:

- `source`: the source `CaseRole` of the violating morphism
- `target`: the target `CaseRole`
- `violation_type`: one of `"missing_morphism"`, `"composition_violation"`, `"identity_violation"`
- `severity`: float in $[0,1]$ where 1.0 = critical
- `description`: human-readable explanation

### `CaseFrameValidator`

```python
class CaseFrameValidator:
    def __init__(self, category=None, enriched=None):
        """Initialize with case category (defaults to standard 8-case)
        and optional enriched category for weight-based checks."""
```

On initialization, builds the set of valid `(source, target)` morphism pairs from the category. Validation then checks whether a proposed case frame assignment contains only licensed pairs.

### Detection & Scoring Functions

**`detect_type_violation(category, source, target)`**: Returns a `TypeViolation` if the `(source, target)` pair has no licensed morphism in `category`, or `None` if the assignment is well-typed (identity morphisms `source == target` are always well-typed).

**`injection_score(violations)`**: Computes an aggregate severity score from a list of `TypeViolation` objects. Higher scores indicate more severe injection attempts.

**`topological_robustness(enriched)`**: Returns the normalized categorical magnitude $R = \lvert\mathcal{C}\rvert / n$, where $n$ is the number of roles. Higher magnitude means more distinct relational structure, and so more "surface area" for detecting type violations. $R$ is bounded in $(0, 1]$ **only** for hom-matrices that satisfy the composition inequality $\mathcal{C}(A,C) \geq \mathcal{C}(A,B)\cdot\mathcal{C}(B,C)$; `EnrichedCategory._validate()` does not enforce that axiom, so a user-supplied proximity matrix can return $R > 1$ (the function logs a warning when it does). This is a summary statistic, not a proved perturbation bound.

**`semantic_integrity_check(enriched)`**: Checks $\mathcal{C}(A,C) \geq \mathcal{C}(A,B)\cdot\mathcal{C}(B,C)$ over all distinct triples of the enriched category and returns the `list[tuple[CaseRole, CaseRole, CaseRole]]` of triples that violate it — empty when the category is coherent. It takes no case-frame argument.

---

## Usage Examples

```python
from src.case_systems import CaseRole, standard_case_category
from src.enriched_cat import standard_enriched_category
from src.security import (
    CaseFrameValidator, TypeViolation,
    detect_type_violation, injection_score,
    topological_robustness, semantic_integrity_check,
)

# 1. Create a validator
cat = standard_case_category()
enriched = standard_enriched_category()
validator = CaseFrameValidator(category=cat, enriched=enriched)

# 2. Check a well-typed assignment — note the (category, source, target) argument order
violation = detect_type_violation(cat, CaseRole.NOM, CaseRole.ACC)
print(f"NOM→ACC: {violation}")  # None (well-typed)

# 3. Check an ill-typed assignment (prompt injection attempt)
violation = detect_type_violation(cat, CaseRole.VOC, CaseRole.NOM)
print(f"VOC→NOM: {violation}")  # TypeViolation detected

# 4. Compute robustness
robustness = topological_robustness(enriched)
print(f"Topological robustness: {robustness:.4f}")

# 5. Semantic integrity — returns the list of composition-inequality violations
violating_triples = semantic_integrity_check(enriched)
print(f"Composition-inequality violations: {len(violating_triples)}")
```

---

## Manuscript Equations Implemented

| Equation | Function | Description |
| -------- | -------- | ----------- |
| Type violation decidability | `detect_type_violation()` | Finite category → decidable type checking |
| Injection severity | `injection_score()` | Weighted aggregate of violation severity |
| Normalized magnitude | `topological_robustness()` | $R = \lvert\mathcal{C}\rvert / n$ — in $(0,1]$ only when the composition inequality holds |
| Composition inequality integrity | `semantic_integrity_check()` | $\mathcal{C}(A,C) \geq \mathcal{C}(A,B) \cdot \mathcal{C}(B,C)$ |

---

## Related Documentation

- **Upstream**: [`case_systems`](case_systems.md), [`enriched_cat`](enriched_cat.md)
- **Theory map**: [theory_implementation_map.md](../theory_implementation_map.md) (§9b security row)
- **Visualization**: [`visualization`](visualization.md) — `security_plots.py`
- **Figures**: [manuscript_figure_index.md](../manuscript_figure_index.md) — Figure 19 (`security_type_violations.png`, via `plot_case_interaction_graph()`) and Figure 19b (`monoidal_functor_security.png`, via `plot_monoidal_functor_security()`)
- **Literature**: [literature_guide.md](../literature_guide.md) — Adversarial Robustness section
- **Glossary**: [glossary.md](../glossary.md) — prompt injection, type violation, robustness

---

*Last updated: 2026-04-22. Source of truth: `src/security/__init__.py`.*
