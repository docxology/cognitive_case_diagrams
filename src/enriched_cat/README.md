# enriched_cat/ — §5: Enriched Categories and Magnitude

[0,1]-enriched category theory for distributional semantics. Hom-values represent distributional proximity between case roles.

## Quick Import

Root package also re-exports `EnrichedCategory` and `standard_enriched_category` (`from src import …`).

```python
from src.enriched_cat.enriched import (
    EnrichedCategory, standard_enriched_category,
    STANDARD_ROLES, STANDARD_PROXIMITY_MATRIX,
)
```

## Key API

| Method | Description |
|--------|-------------|
| `ec.hom(A, B)` | Returns `C(A,B) ∈ [0,1]` proximity |
| `ec.magnitude()` | `\|C\| = Σᵢⱼ (Z⁻¹)ᵢⱼ` — effective category size |
| `ec.magnitude_deficit()` | `n - \|C\|` — distributional redundancy |
| `ec.weighting()` | Column sums of Z⁻¹ |
| `ec.coweighting()` | Row sums of Z⁻¹ |
| `ec.role_clusters(threshold)` | BFS clustering by proximity |
| `ec.full_composition_check()` | All-triple composition inequality stats |
| `standard_enriched_category()` | 8-role empirically-motivated category |

See [`AGENTS.md`](AGENTS.md) for full API reference, magnitude interpretation, and the standard proximity matrix; [`SKILL.md`](SKILL.md) for agent routing.
