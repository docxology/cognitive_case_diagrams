# 🤖 AGENTS.md — src/enriched_cat/

## Overview

The `enriched_cat` subpackage implements **§5** (and **§5b** magnitude homology) of the manuscript: [0,1]-enriched category theory as a distributional semantic framework. Each pair of case roles carries a hom-value in [0,1] representing their distributional proximity — the categorical analogue of word embedding cosine similarity.

> **Reference**: Bradley, Terilla & Weyhrich (2021). *An enriched category theory of language: from syntax to semantics*. `[@bradley2021enriched]`

## Module Inventory

Line coverage: `uv run pytest tests/ --cov=src --cov-report=term-missing` (project root).

| Module | Key Exports |
|--------|-------------|
| `enriched.py` | `EnrichedCategory`, `standard_enriched_category()`, `STANDARD_ROLES`, `STANDARD_PROXIMITY_MATRIX` |

## `enriched.py` — `EnrichedCategory`

### Core Concept

An enriched category `C` enriched over `[0,1]` consists of:
- **Objects**: set of `CaseRole` members
- **Hom-values**: `C(A,B) ∈ [0,1]` — distributional proximity
- **Identity axiom**: `C(A,A) = 1` for all objects
- **Composition inequality**: `C(A,C) ≥ C(A,B) · C(B,C)` for all triples

The proximity matrix encodes these hom-values as an `n×n` numpy array.

### Constructor

```python
ec = EnrichedCategory(
    name="MyCategory",
    roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
    proximity_matrix=np.array([
        [1.0, 0.85, 0.45],
        [0.85, 1.0, 0.55],
        [0.45, 0.55, 1.0],
    ]),
)
```

**Validation** (in `__post_init__`):
- Matrix shape must be `(n, n)` where `n = len(roles)`
- Diagonal must be `1.0` (identity axiom)
- All values must be in `[0, 1]`

### Instance Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `hom(source, target)` | `float` | Returns `C(source, target)` proximity value |
| `check_composition_inequality(a, b, c)` | `bool` | `C(A,C) ≥ C(A,B)·C(B,C)` |
| `magnitude()` | `float` | `\|C\| = Σᵢⱼ (Z⁻¹)ᵢⱼ` — categorical magnitude |
| `weighting()` | `np.ndarray` | Solves `Z w = 1`, i.e. **row** sums of `Z⁻¹` — role importance weights |
| `coweighting()` | `np.ndarray` | Solves `v Z = 1`, i.e. **column** sums of `Z⁻¹` — dual weight vector |
| `magnitude_deficit()` | `float` | `n - \|C\|` — information lost to distributional overlap |
| `full_composition_check()` | `dict` | Checks all distinct triples; returns stats dict |
| `role_clusters(threshold)` | `list[set]` | BFS clustering by proximity threshold |

### Categorical Magnitude

Equation §5 (Manuscript):
```
|C| = Σᵢⱼ (Z⁻¹)ᵢⱼ
```
where `Z` is the proximity matrix. Magnitude quantifies the **effective number of distinct roles** — a system where all roles are maximally distinct has `|C| = n`; overlapping roles reduce magnitude.

**Interpretation**:
- `|C| = n`: maximally distinct roles (identity matrix)
- `|C| < n`: distributional redundancy (roles share contexts)
- `magnitude_deficit() = n - |C|`: information lost to overlap

### Composition Inequality

The enriched analogue of categorical composition:
```
C(A,C) ≥ C(A,B) · C(B,C)
```
Violations indicate **distributional inconsistencies** that could be exploited by adversarial inputs (used in `src/security/cognitive_security.py::semantic_integrity_check()`).

### Role Clustering

BFS clustering at a proximity threshold reveals the distributional structure:
```python
ec = standard_enriched_category()
clusters = ec.role_clusters(threshold=0.6)
# Returns list of sets, each containing mutually-close case roles
```

**Standard clustering (`standard_enriched_category()`, threshold=0.6)** — four components:
- NOM/ACC/GEN/VOC → core argument cluster (NOM–VOC at 0.70 pulls VOC in; NOM–GEN at 0.60 meets the threshold)
- LOC/ABL → oblique cluster (0.65)
- DAT → singleton at this threshold
- INS → singleton at this threshold

Lower the threshold to widen the oblique cluster; the exact partition is a
function of `STANDARD_PROXIMITY_MATRIX`, so re-run `role_clusters()` rather than
quoting this list after any matrix change.

### Standard Proximity Matrix

The empirically-motivated 8×8 matrix (`STANDARD_PROXIMITY_MATRIX`) encodes:

| Row/Col | NOM | ACC | GEN | DAT | INS | LOC | ABL | VOC |
|---------|-----|-----|-----|-----|-----|-----|-----|-----|
| **NOM** | 1.00 | 0.85 | 0.60 | 0.45 | 0.35 | 0.25 | 0.20 | 0.70 |
| **ACC** | 0.85 | 1.00 | 0.50 | 0.55 | 0.40 | 0.30 | 0.25 | 0.40 |
| **GEN** | 0.60 | 0.50 | 1.00 | 0.45 | 0.30 | 0.35 | 0.40 | 0.25 |
| *...* | | | | | | | | |

### Factory Function

```python
ec = standard_enriched_category()
# 8-role, empirically-motivated proximity matrix
# Validated: identity axiom, [0,1] values
mag = ec.magnitude()   # < 8.0 (distributional overlap)
```

## LLM Attention Connection

**Manuscript §4**: LLM attention weights are interpreted as context-dependent enriched hom-values:
```
Attention(Q, K) ≈ C_context(A, B)
```
Each attention head instantiates a contextual enriched category, and the multi-head structure represents a polycategory over distributional case relations.

## Common Patterns

```python
# Check if composition inequality holds for all triples
result = ec.full_composition_check()
print(f"{result['violation_rate']:.1%} of triples violate composition")

# Find role clusters
clusters = ec.role_clusters(threshold=0.7)
for cluster in clusters:
    print({r.name for r in cluster})

# Compute magnitude and deficit
mag = ec.magnitude()
deficit = ec.magnitude_deficit()
print(f"Effective roles: {mag:.2f}/{len(ec.roles)} (deficit: {deficit:.2f})")
```
