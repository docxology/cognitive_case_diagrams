# Module: `enriched_cat` — Enriched Categories & Magnitude (§5–5b)

> **Package**: `src.enriched_cat`
> **Manuscript**: §5 *Enriched Categories* and §5b *Magnitude Homology*
> **Dependencies**: `case_systems`
> **Test files**: `tests/test_enriched_cat*.py`

---

## Purpose

The `enriched_cat` package elevates case categories from discrete (morphism-exists-or-not) to **continuous** by replacing boolean hom-sets with hom-values in $[0,1]$. This is mathematically precise: a $[0,1]$-enriched category replaces the ordinary category's $\text{Hom}(A,B) \in \{0,1\}$ with $\mathcal{C}(A,B) \in [0,1]$ representing distributional proximity between case roles.

Key contributions:

1. **Hom-values** encode distributional relatedness (e.g., NOM↔ACC = 0.85)
2. **Composition inequality**: $\mathcal{C}(A,C) \geq \mathcal{C}(A,B) \cdot \mathcal{C}(B,C)$ — the enriched analogue of composition
3. **Categorical magnitude** $|\mathcal{C}| = \sum_{i,j} (Z^{-1})_{ij}$ — an information-theoretic invariant quantifying the "effective size" of the case system
4. **Weighting/coweighting vectors** — distributional importance of each role
5. **Magnitude deficit** $n - |\mathcal{C}|$ — quantifies distributional redundancy

---

## Architecture

```text
enriched_cat/
├── __init__.py     # 4 exported symbols
└── enriched.py     # EnrichedCategory class + standard factory
```

This is a compact, focused module. All functionality is in a single file.

### Dependency Position

```text
case_systems → enriched_cat → topos_theory
                    ↓
               cognitive.reanalysis
                    ↓
               security
```

---

## Module Reference

### `enriched.py` — Full API

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `STANDARD_ROLES` | `list[CaseRole]` | Canonical ordering: NOM, ACC, GEN, DAT, INS, LOC, ABL, VOC |
| `STANDARD_PROXIMITY_MATRIX` | `np.ndarray` (8×8) | Empirically motivated proximity matrix |
| `EnrichedCategory` | `@dataclass` | Core class: `name`, `roles`, `proximity_matrix` |
| `standard_enriched_category()` | factory | Creates the standard 8-case enriched category |

### `EnrichedCategory` Methods

| Method | Returns | Description |
| ------ | ------- | ----------- |
| `hom(source, target)` | `float` | Distributional proximity $\mathcal{C}(A,B) \in [0,1]$ |
| `check_composition_inequality(a, b, c)` | `bool` | $\mathcal{C}(A,C) \geq \mathcal{C}(A,B) \cdot \mathcal{C}(B,C)$ |
| `magnitude()` | `float` | $\|\mathcal{C}\| = \sum_{i,j} (Z^{-1})_{ij}$ |
| `weighting()` | `np.ndarray` | Row sums of $Z^{-1}$ — the solution $w$ of $Zw = \mathbf{1}$ |
| `coweighting()` | `np.ndarray` | Column sums of $Z^{-1}$ — the solution $v$ of $vZ = \mathbf{1}$ |
| `magnitude_deficit()` | `float` | $n - \|\mathcal{C}\|$ |
| `full_composition_check()` | `dict` | Tests all triples; returns `holds`, `violations`, `total`, `violation_rate` |
| `role_clusters(threshold)` | `list[set]` | BFS clustering of roles with $\mathcal{C}(A,B) \geq \theta$ |

### Axiom Validation (`__post_init__`)

On construction, `EnrichedCategory._validate()` enforces:

1. Matrix shape matches number of roles
2. **Identity axiom**: $\mathcal{C}(A,A) = 1$ for all $A$
3. All values in $[0,1]$

### Standard Proximity Matrix

```text
        NOM   ACC   GEN   DAT   INS   LOC   ABL   VOC
NOM   [1.00, 0.85, 0.60, 0.45, 0.35, 0.25, 0.20, 0.70]
ACC   [0.85, 1.00, 0.50, 0.55, 0.40, 0.30, 0.25, 0.40]
GEN   [0.60, 0.50, 1.00, 0.45, 0.30, 0.35, 0.40, 0.25]
DAT   [0.45, 0.55, 0.45, 1.00, 0.50, 0.40, 0.35, 0.30]
INS   [0.35, 0.40, 0.30, 0.50, 1.00, 0.55, 0.50, 0.20]
LOC   [0.25, 0.30, 0.35, 0.40, 0.55, 1.00, 0.65, 0.15]
ABL   [0.20, 0.25, 0.40, 0.35, 0.50, 0.65, 1.00, 0.15]
VOC   [0.70, 0.40, 0.25, 0.30, 0.20, 0.15, 0.15, 1.00]
```

This matrix encodes a gradient from core arguments (NOM–ACC, high proximity) to oblique cases (LOC–ABL, clustered together), matching typological observations from Dixon (1994).

---

## Usage Examples

```python
from src.enriched_cat import (
    EnrichedCategory, standard_enriched_category,
    STANDARD_ROLES, STANDARD_PROXIMITY_MATRIX,
)
from src.case_systems import CaseRole

# 1. Use the standard 8-case enriched category
cat = standard_enriched_category()

# 2. Query hom-values
print(f"NOM↔ACC: {cat.hom(CaseRole.NOM, CaseRole.ACC)}")   # 0.85
print(f"NOM↔ABL: {cat.hom(CaseRole.NOM, CaseRole.ABL)}")   # 0.20

# 3. Compute magnitude
mag = cat.magnitude()
print(f"Magnitude: {mag:.4f}")  # Effective size of the case system

# 4. Check composition inequality
holds = cat.check_composition_inequality(CaseRole.NOM, CaseRole.ACC, CaseRole.DAT)
print(f"C(NOM,DAT) >= C(NOM,ACC)·C(ACC,DAT): {holds}")

# 5. Find role clusters
clusters = cat.role_clusters(threshold=0.6)
for i, c in enumerate(clusters):
    print(f"Cluster {i}: {[r.name for r in c]}")

# 6. Full composition check
result = cat.full_composition_check()
print(f"Violations: {len(result['violations'])}/{result['total']}")
```

---

## Manuscript Equations Implemented

| Equation | Method | Description |
| -------- | ------ | ----------- |
| $\mathcal{C}(A,A) = 1$ | `_validate()` | Identity axiom |
| $\mathcal{C}(A,C) \geq \mathcal{C}(A,B) \cdot \mathcal{C}(B,C)$ | `check_composition_inequality()` | Composition inequality |
| $\|\mathcal{C}\| = \sum_{i,j} (Z^{-1})_{ij}$ | `magnitude()` | Categorical magnitude |
| $Zw = 1$ | `weighting()` | Weighting vector |
| $vZ = 1$ | `coweighting()` | Coweighting vector |
| $n - \|\mathcal{C}\|$ | `magnitude_deficit()` | Magnitude deficit |

---

## Related Documentation

- **Upstream**: [`case_systems`](case_systems.md) — provides `CaseRole` objects
- **Downstream**: [`topos_theory`](topos_theory.md), [`cognitive`](cognitive.md) (reanalysis), [`security`](security.md)
- **Theory map**: [theory_implementation_map.md](../theory_implementation_map.md) §5–§5b
- **Visualization**: [`visualization`](visualization.md) — `enriched_diagrams.py`
- **Figures**: [manuscript_figure_index.md](../manuscript_figure_index.md) — Figure 15 (`enriched_hom_matrix.png`, via `render_enriched_heatmap()`)

---

*Last updated: 2026-04-22. Source of truth: `src/enriched_cat/__init__.py`.*
