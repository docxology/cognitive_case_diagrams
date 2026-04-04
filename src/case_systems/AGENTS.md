# 🤖 AGENTS.md — src/case_systems/

## Overview

The `case_systems` subpackage implements **§2** of the manuscript: the categorical formalization of linguistic case systems. Case roles become category-theoretic objects, grammatical relations become morphisms, and cross-linguistic alignment systems become functors.

## Module Inventory

Per-file line coverage changes with edits; the source of truth is:

`uv run pytest tests/ --cov=src --cov-report=term-missing` (from this project’s root directory: parent of `src/`).

| Module | Key Exports | Manuscript |
|--------|-------------|-----------|
| `case_category.py` | `CaseRole`, `Morphism`, `CaseCategory`, factory functions | §2.3–§2.5 |
| `functor.py` | `AlignmentFunctor` | §2.6 |
| `natural_transformation.py` | `ComponentMorphism`, `NaturalTransformation`, `IdentityNaturalTransformation`, `compose_transformations`, `naturality_holds` / `verify_naturality` | §2.7 |
| `fluid_s.py` | `FluidSFunctor` (`map_object`, `map_morphism`, `split_probability`, …), `VolitionContext`, `bats_fluid_s()`, `fluid_s_enriched_weight()` | §2.8 |

## `case_category.py`

### `CaseRole` (Enum)
The 12 case roles as enumeration members, divided into:
- **Standard 8-case system**: `NOM`, `ACC`, `GEN`, `DAT`, `INS`, `LOC`, `ABL`, `VOC`
- **Alignment roles** (Dixon/Comrie): `ERG`, `ABS`
- **Core argument primitives**: `S` (sole), `A` (agent), `P` (patient)

### `Morphism` (frozen dataclass)
Represents a grammatical relation as a morphism `f: A → B`:
```python
Morphism(source=CaseRole.NOM, target=CaseRole.ACC, label="acts_on", weight=1.0)
```
`weight ∈ [0,1]` encodes the proto-role satisfaction (Dowty's agent/patient entailments).

### `CaseCategory`
A category where:
- Objects = `CaseRole` enum values
- Morphisms = `Morphism` instances
- Composition = `compose(f, g)` → `g ∘ f`
- Identity = `identity(role)` → `id: role → role`

**Key methods**:

| Method | Returns | Description |
|--------|---------|-------------|
| `add_role(role)` | — | Add object to category |
| `add_morphism(m)` | — | Add morphism (validates source/target) |
| `compose(f, g)` | `Morphism` | Categorical composition g ∘ f; enriched weight ``w(g∘f)=w(f)·w(g)`` |
| `identity(role)` | `Morphism` | Identity morphism for role |
| `associativity_holds()` | `bool` | Verify associativity for all composable triples |
| `is_well_formed()` | `bool` | Full categorical axiom check |
| `get_morphisms_from(role)` | `list[Morphism]` | All morphisms out of a role |
| `get_morphisms_to(role)` | `list[Morphism]` | All morphisms into a role |

### Factory Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `standard_case_category()` | `CaseCategory` | Standard 8-case system with 8 canonical morphisms |
| `minimal_case_category()` | `CaseCategory` | Minimal 3-role transitive: NOM, ACC, INS |
| `introductory_case_category()` | `CaseCategory` | Intro figure (`fig:case-minimal`): NOM, ACC, INS, VOC + weighted triangle and `addresses`; PNG layout and `f`/`g`/`h=g∘f` edge prefixes live in `scripts/generate_category_figures.py` (`CASE_MINIMAL_*`) |
| `accusative_alignment()` | `dict[CaseRole, CaseRole]` | {S,A} → NOM; P → ACC |
| `ergative_alignment()` | `dict[CaseRole, CaseRole]` | {S,P} → ABS; A → ERG |
| `tripartite_alignment()` | `dict[CaseRole, CaseRole]` | S → ABS, A → ERG, P → ACC (injective) |
| `active_stative_alignment()` | `dict` | Split-S: active and stative contexts |

## `functor.py` — `AlignmentFunctor`

Maps between case categories (e.g., from Universal Case to Language-Specific Case), encoding cross-linguistic alignment as a functor:

```python
functor = AlignmentFunctor(name="F", source=source_cat, target=target_cat, object_map={...})
mapped_role = functor.map_object(CaseRole.S)
mapped_morphism = functor.map_morphism(m)  # preserves morphism.weight
```

**Functor laws** (checked via `preserves_identity` / `preserves_composition` on sample morphisms):
1. Identity preservation: `F(id_A) = id_{F(A)}`
2. Composition preservation: `F(g ∘ f) = F(g) ∘ F(f)`

## `natural_transformation.py` — `NaturalTransformation`

Natural transformations between alignment functors — captures systematic morphisms between case systems (e.g., dative alternation as a natural transformation):

```python
eta = NaturalTransformation(name="eta", source_functor=F, target_functor=G)
# populate via set_component(...) until is_complete()
assert eta.naturality_holds()   # G(f)∘α_A = α_B∘F(f) on relevant source morphisms
assert eta.verify_naturality()  # alias
composed = compose_transformations(eta, mu)
```

**`IdentityNaturalTransformation`**: Built-in identity `id_F: F ⇒ F` (naturality holds trivially once `source.source.morphisms` is respected).

## `fluid_s.py` — `FluidSFunctor`

Implements Fluid-S alignment (manuscript §2.8): a context-dependent functor parameterized by volitional construal probability `p ∈ [0,1]`.

The Bats (Nakh-Daghestanian) language example:
- `fall (volitional)` → `S_ERG`: ERG marking
- `fall (accidental)` → `S_ABS`: ABS marking

```python
vol_functor = create_fluid_s_functor(volitional=True, probability=0.9)
nonvol_functor = create_fluid_s_functor(volitional=False, probability=0.1)

# Graded probability distribution over case assignments
dist = vol_functor.split_probability(CaseRole.NOM)
# → {CaseRole.NOM: 0.9, CaseRole.ACC: 0.1}
```

**Key functions**:

| Function | Description |
|----------|-------------|
| `FluidSFunctor.map_object(role)` | Deterministic mapping under current context |
| `FluidSFunctor.map_object_in_context(role, p)` | Graded probability mapping |
| `FluidSFunctor.split_probability(role)` | Convenience: uses stored `volition_probability` |
| `FluidSFunctor.kernel()` | Pairs of roles mapped to same target |
| `create_fluid_s_functor(volitional, probability)` | Factory: build volitional or non-volitional functor |
| `bats_fluid_s()` | Returns canonical Bats language pair `(vol_functor, nonvol_functor)` |
| `fluid_s_enriched_weight(p, base)` | Enriched weight for S-morphism under volition |

## Common Patterns

### Building and composing morphisms
```python
cat = standard_case_category()
f = Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on")
g = Morphism(CaseRole.ACC, CaseRole.DAT, "received_by")
h = cat.compose(f, g)   # NOM → DAT via NOM→ACC→DAT
```

### Checking well-formedness
```python
cat = minimal_case_category()
assert cat.is_well_formed()    # All categorical axioms satisfied
```

### Fluid-S graded construal
```python
functor = create_fluid_s_functor(volitional=True, probability=0.7)
dist = functor.split_probability(CaseRole.NOM)
# → {NOM: 0.7, ACC: 0.3}  — 70% chance of agent marking
```
