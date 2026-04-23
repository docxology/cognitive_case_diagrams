# security/ — §9b: Prompt Injection Is a Type Violation

Prompt injection and frame manipulation as decidable type violations against a finite case category (and optional enriched structure). Framed as a **protocol-level** analysis in [`09b_cognitive_security.md`](../../manuscript/09b_cognitive_security.md), not a guarantee on production LLM APIs.

## Quick Import

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

## Key APIs

| Symbol | Role |
|--------|------|
| `TypeViolation` | Dataclass: `source`, `target`, `violation_type`, `severity`, `description` |
| `detect_type_violation(category, source, target)` | Returns `TypeViolation` or `None` if a morphism `source → target` is missing |
| `injection_score(violations)` | Aggregate severity in `[0, 1]` from a list of `TypeViolation` |
| `CaseFrameValidator` | `validate_assignment(assignments: dict)` → list of violations; optional `enriched` for future weight checks |
| `topological_robustness(enriched)` | `|C|/n` magnitude-based robustness in `(0, 1]` |
| `semantic_integrity_check(enriched)` | Lists `(A,B,C)` triples breaking the composition inequality |

## Example

```python
from src.case_systems.case_category import CaseRole, standard_case_category
from src.security import CaseFrameValidator, detect_type_violation, injection_score

cat = standard_case_category()
v = detect_type_violation(cat, CaseRole.VOC, CaseRole.INS)

validator = CaseFrameValidator(category=cat)
violations = validator.validate_assignment({"np1": CaseRole.NOM, "np2": CaseRole.ACC})
score = injection_score(violations)
```

See [`AGENTS.md`](AGENTS.md) for the full security model. [`SKILL.md`](SKILL.md) for agent context.
