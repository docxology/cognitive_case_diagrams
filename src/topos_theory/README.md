# topos_theory/ — §6: Topos-Theoretic Bridges

Geometric theories, classifying toposes, and Morita equivalence for inter-theoretic translation between case systems.

**`check_morita_equivalence` tests necessary conditions only.** A `True` means
"not ruled out", never "equivalent" — see [`AGENTS.md`](AGENTS.md).

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
| `GeometricTheory` | Case system as a geometric theory: `sorts`, `relation_symbols`, `axioms` — built via `add_sort` / `add_relation` / `add_axiom` |
| `Axiom` | `name`, `antecedent`, `consequent`, `sort_variables` |
| `ClassifyingTopos` | Universal model `E_T`; `invariants` holds `signature_shape`, `arity_spectrum`, `axiom_count`, `theory_type` |
| `TheoryType` | Enum: `TYPOLOGICAL`, `TYPE_LOGICAL`, `DISTRIBUTIONAL`, `ENRICHED` |
| `check_morita_equivalence(topos1, topos2)` | Takes two `ClassifyingTopos`; returns `(not_ruled_out: bool, mismatches: list[str])` |
| `build_typological_theory(category, alignment_name="typological")` | Formalizes a `CaseCategory` as a geometric theory |
| `build_enriched_theory(enriched_cat)` | Formalizes an `EnrichedCategory` as a geometric theory |
| `bridge_transfer(source_topos, target_topos, property_name)` | Returns a transfer-result dict (never raises on mismatch) |

## Morita Equivalence

```python
from src.case_systems.case_category import standard_case_category, minimal_case_category

acc = ClassifyingTopos(theory=build_typological_theory(standard_case_category(), "accusative"))
mini = ClassifyingTopos(theory=build_typological_theory(minimal_case_category(), "minimal"))
not_ruled_out, mismatches = check_morita_equivalence(acc, mini)
# not_ruled_out → bool ("not ruled out", not "equivalent"); mismatches → list[str]
```

See [`AGENTS.md`](AGENTS.md) for theory of Morita equivalence, Caramello's bridges, and the Language of Thought connection; [`SKILL.md`](SKILL.md) for agent routing.
