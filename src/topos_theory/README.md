# topos_theory/ — §6: Topos Theory

Geometric theories, classifying toposes, and Morita equivalence for inter-theoretic translation between case systems.

## Quick Import

```python
from src.topos_theory import (
    GeometricTheory,
    ClassifyingTopos,
    TheoryType,
    check_morita_equivalence,
    build_typological_theory,
    build_enriched_theory,
)
# Lower-level helpers (e.g. bridge_transfer) live in topos.py:
from src.topos_theory.topos import bridge_transfer
```

## Key APIs

| Function/Class | Description |
|---------------|-------------|
| `GeometricTheory` | Case system as geometric theory with axioms and signature |
| `ClassifyingTopos` | Universal model `Set[T^op]` with computed invariants |
| `TheoryType` | Enum: `TYPOLOGICAL`, `ALIGNMENT`, `ENRICHED`, `FLUID_S` |
| `check_morita_equivalence(T1, T2)` | Returns `{equivalent, reason, shared_invariants}` |
| `build_typological_theory(type, functors)` | Factory for alignment theories |
| `bridge_transfer(source, target, knowledge)` | Cross-theory knowledge transfer |

## Morita Equivalence

```python
acc = build_typological_theory("accusative", ["acts_on", "receives"])
erg = build_typological_theory("ergative", ["is_agent_of", "is_patient_of"])
result = check_morita_equivalence(acc, erg)
# result["equivalent"] → bool
```

See [`AGENTS.md`](AGENTS.md) for theory of Morita equivalence, Caramello's bridges, and the Language of Thought connection; [`SKILL.md`](SKILL.md) for agent routing.
