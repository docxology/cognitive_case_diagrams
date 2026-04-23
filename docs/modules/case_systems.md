# Module: `case_systems` — Case Systems & Categories (§2)

> **Package**: `src.case_systems`
> **Manuscript**: §2 *Case Systems*, §2b *Case Categories*
> **Dependency**: None (foundation layer)
> **Test files**: `tests/test_case_systems*.py`

---

## Purpose

The `case_systems` package is the **foundational layer** of the entire project. It formalizes linguistic case systems as categories in the mathematical sense:

- **Objects** are case roles (`CaseRole` enum: NOM, ACC, GEN, DAT, INS, LOC, ABL, VOC, ERG, ABS, S, A, P)
- **Morphisms** are grammatical relations between roles (`Morphism` dataclass)
- **Composition** is associative and weight-multiplicative: $w(g \circ f) = w(f) \cdot w(g)$
- **Alignment functors** map pre-alignment primitives (S, A, P) to surface case roles

Every other `src/` package depends on `case_systems` — it provides the objects that all subsequent categorical machinery operates on.

---

## Architecture

```text
case_systems/
├── __init__.py              # Public API re-exports
├── case_category.py         # CaseRole, Morphism, CaseCategory
├── functor.py               # AlignmentFunctor, MonoidalFunctor
├── natural_transformation.py # NaturalTransformation, ComponentMorphism
└── fluid_s.py               # FluidSFunctor, VolitionContext
```

### Dependency Position

```text
case_systems ← enriched_cat ← topos_theory
     ↑              ↑
  cognitive       diagrams
     ↑
    daif
     ↑
MonoidalFunctor (functor.py) → security topology enforcement
```

`case_systems` is the **root** of the dependency DAG. No circular imports exist.

---

## Module Reference

### `case_category.py` — Core Categorical Structure

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `CaseRole` | `Enum` | 13 case roles: NOM, ACC, GEN, DAT, INS, LOC, ABL, VOC, ERG, ABS, S, A, P |
| `Morphism` | `@dataclass(frozen=True)` | Arrow with `source`, `target`, `label`, `weight ∈ [0,1]` |
| `CaseCategory` | `@dataclass` | Category with `objects`, `morphisms`, `compose()`, `identity()` |
| `standard_case_category()` | factory | 8-case system with 8 canonical morphisms |
| `minimal_case_category()` | factory | 3-role transitive triangle (NOM, ACC, INS) |
| `introductory_case_category()` | factory | 4-role category for manuscript Figure 1 |
| `accusative_alignment()` | `→ dict` | {S,A}→NOM, P→ACC |
| `ergative_alignment()` | `→ dict` | {S,P}→ABS, A→ERG |
| `tripartite_alignment()` | `→ dict` | S→ABS, A→ERG, P→ACC (injective) |
| `active_stative_alignment()` | `→ dict` | Split-S: active vs. stative sub-alignments |

**Instance methods added in Phase 2 (DAIF & Security hardening)**:

| Method | Signature | Description |
| ------ | --------- | ----------- |
| `CaseCategory.assess_daif_surprisal()` | `(self, observed: Morphism, predicted_weight: float) → dict[str, float]` | Returns `{"N400_amplitude": float, "P600_amplitude": float}` — N400 = `|predicted_weight − observed.weight|`; P600 = `1.0` if `observed` is *not* structurally licensed by any morphism in the category, else `0.0`. Li & Futrell (2024) / Rabovsky et al. (2025) shallow/deep surprisal decomposition. |

For categorical type-checking of candidate morphisms / role assignments, use `src.security.cognitive_security.CaseFrameValidator.validate_assignment()`. See `§9b` (`09b_cognitive_security.md`) for formal proof that this check is decidable.

**Key method — `CaseCategory.compose(f, g)`**:

```python
def compose(self, f: Morphism, g: Morphism) -> Morphism:
    """g ∘ f: requires f.target == g.source.
    Weight: w(g∘f) = w(f) · w(g) — multiplicative over [0,1]."""
```

**Categorical axiom verification**:

- `associativity_holds()` — tests all composable triples
- `is_well_formed()` — identity + associativity + unit law

### `functor.py` — Alignment Functors

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `AlignmentFunctor` | class | Functor between case categories with `object_map`, `map_object()`, `map_morphism()` |
| `accusative_to_ergative_functor()` | factory | ACC→ABS morphism-preserving functor |
| `tripartite_functor()` | factory | Injective S→ABS, A→ERG, P→ACC |
| `MonoidalFunctor` | class | Monoidal functor with `preserves_tensor(role_a, role_b) -> bool` for tensor-preservation checks used in the §9b **protocol-level** security story (specification target, not a deployed-API guarantee). |

`AlignmentFunctor.preserves_composition` compares composed weights to ensure functorial weight preservation. `MonoidalFunctor` extends this to tensor preservation checks that flag illicit role merges consistent with the prompt-injection analysis in [`09b_cognitive_security.md`](../../manuscript/09b_cognitive_security.md).

### `natural_transformation.py` — Inter-Alignment Maps

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `ComponentMorphism` | `@dataclass(frozen=True)` | Single component α_A: F(A)→G(A) |
| `NaturalTransformation` | class | Collection of components with `naturality_holds()` / `verify_naturality()` |
| `IdentityNaturalTransformation` | class | id: F ⇒ F |
| `compose_transformations()` | function | Vertical composition β ∘ α |

**Naturality condition** (`naturality_holds()`): For every morphism $f: A \to B$ in the source category:

$$G(f) \circ \alpha_A = \alpha_B \circ F(f)$$

Quantifies over `source_functor.source.morphisms` whose endpoints lie in `object_map`. Requires `is_complete()`.

### `fluid_s.py` — Context-Dependent Alignment

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `VolitionContext` | `Enum` | Enumerates volition categories (`VOLITIONAL`, `NONVOLITIONAL`, `NEUTRAL`) used by `FluidSFunctor` |
| `FluidSFunctor` | `@dataclass` | Context-dependent functor with `map_object()`, `map_object_in_context()`, `split_probability()`, `map_morphism()`, `kernel()` |
| `create_fluid_s_functor()` | factory | General constructor |
| `bats_fluid_s()` | factory | Batsbi (Tsova-Tush) Fluid-S exemplar — returns `(volitional, nonvolitional)` functor pair |
| `fluid_s_enriched_weight()` | function | Computes enriched weight from volition probability and base weight |

Implements the Fluid-S alignment where the intransitive subject S splits probabilistically between ERG and ABS depending on volition features (§2b).

---

## Usage Examples

```python
from src.case_systems import (
    CaseRole, Morphism, CaseCategory,
    standard_case_category, AlignmentFunctor,
    NaturalTransformation, FluidSFunctor,
)

# 1. Build a case category
cat = standard_case_category()
assert cat.is_well_formed()
print(f"Category: {len(cat.objects)} objects, {len(cat.morphisms)} morphisms")

# 2. Compose morphisms (weight-multiplicative)
f = Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on", weight=0.9)
g = Morphism(CaseRole.ACC, CaseRole.DAT, "received_by", weight=0.7)
cat.add_role(CaseRole.NOM); cat.add_role(CaseRole.ACC); cat.add_role(CaseRole.DAT)
h = cat.compose(f, g)
assert abs(h.weight - 0.63) < 1e-10  # 0.9 × 0.7

# 3. Alignment functors
from src.case_systems import accusative_alignment, ergative_alignment
acc = accusative_alignment()
assert acc[CaseRole.S] == CaseRole.NOM
assert acc[CaseRole.P] == CaseRole.ACC
```

---

## Manuscript Equations Implemented

| Equation | Function | Description |
| -------- | -------- | ----------- |
| Eq 2-1: $w(g \circ f) = w(g) \cdot w(f)$ | `CaseCategory.compose()` | Multiplicative weight composition |
| Def 2.1: Case category $\mathcal{L}$ | `CaseCategory` | Objects, morphisms, composition |
| Def 2.2: Alignment functor $F_\text{acc}$ | `AlignmentFunctor` | Object/morphism mapping |
| Naturality: $G(f) \circ \alpha_A = \alpha_B \circ F(f)$ | `NaturalTransformation.naturality_holds()` | Naturality square |
| Fluid-S: $P(\text{ERG} \mid S) = p_\text{vol}$ | `FluidSFunctor.split_probability()` | Context-dependent split |
| Monoidal: $F(A \otimes B) = F(A) \otimes F(B)$ | `MonoidalFunctor.preserves_tensor()` | Tensor checks for §9b protocol narrative |
| DAIF surprisal: N400, P600 | `CaseCategory.assess_daif_surprisal()` | Li & Futrell decomposition (§7c) |
| Injection detect: ACC→NOM | `src.security.cognitive_security.CaseFrameValidator.validate_assignment()` | Decidable type-violation check (§9b) |

---

## Related Documentation

- **Theory mapping**: [theory_implementation_map.md](../theory_implementation_map.md) §2
- **API signatures**: [api_reference.md](../api_reference.md) §2
- **Glossary**: [glossary.md](../glossary.md) — CaseRole, Morphism, Functor, Natural Transformation
- **Figures**: [manuscript_figure_index.md](../manuscript_figure_index.md) — Figures 1–5
- **Extension guide**: [extension_guide.md](../extension_guide.md) — adding new case roles or alignment types
- **Downstream**: [`enriched_cat`](enriched_cat.md), [`cognitive`](cognitive.md), [`diagrams`](diagrams.md)

---

*Last updated: 2026-04-22. Source of truth: `src/case_systems/__init__.py`.*
