# Module: `topos_theory` — Topos-Theoretic Bridges (§6)

> **Package**: `src.topos_theory`
> **Manuscript**: §6 *Topos-Theoretic Bridges*
> **Dependencies**: `case_systems`, `enriched_cat`
> **Test files**: `tests/test_topos*.py`

---

## Purpose

The `topos_theory` package formalizes the **inter-theoretic translation** machinery that enables the project's central synthesis. Following Caramello's bridge technique, it axiomatizes case-theoretic frameworks as geometric theories, constructs their classifying toposes, and checks Morita equivalence to enable property transfer between theories.

The key insight: Meaning-Text Theory (Mel'čuk) and categorial grammar (Lambek) can be axiomatized as geometric theories whose classifying toposes are *conjectured* Morita-equivalent — under which any invariant property proved in one framework would transfer automatically to the other. What the code supplies is a screen, not the equivalence: `check_morita_equivalence()` tests necessary conditions only (see [Bridge Transfer](#bridge-transfer) below).

---

## Architecture

```text
topos_theory/
├── __init__.py    # 7 exported symbols
└── topos.py       # TheoryType, Axiom, GeometricTheory, ClassifyingTopos
```

### Dependency Position

```text
case_systems → enriched_cat → topos_theory
```

`topos_theory` sits at the **apex** of the dependency DAG — it imports from both `case_systems` and `enriched_cat` to build geometric theories from their structures.

---

## Module Reference

### `topos.py` — Complete API

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `TheoryType` | `Enum` | `TYPOLOGICAL`, `TYPE_LOGICAL`, `DISTRIBUTIONAL`, `ENRICHED` |
| `Axiom` | `@dataclass` | Geometric axiom sequent: `antecedent ⊢_x consequent` |
| `GeometricTheory` | `@dataclass` | Full theory: `sorts`, `relation_symbols`, `axioms` |
| `ClassifyingTopos` | `@dataclass` | Wraps theory with computed invariants |
| `check_morita_equivalence()` | function | Necessary conditions for $E_{T_1} \simeq E_{T_2}$ |
| `build_typological_theory()` | function | `CaseCategory → GeometricTheory` |
| `build_enriched_theory()` | function | `EnrichedCategory → GeometricTheory` |

### `GeometricTheory` Methods

| Method | Returns | Description |
| ------ | ------- | ----------- |
| `add_sort(name)` | `None` | Add a sort to the theory's signature |
| `add_relation(name, arity)` | `None` | Add a relation symbol with sort arity |
| `add_axiom(axiom)` | `None` | Add a geometric axiom |
| `signature_invariant()` | `tuple[int,int,int]` | (sorts, relations, axioms) — Morita invariant |
| `arity_spectrum()` | `list[int]` | Sorted list of arity lengths — Morita invariant |

### `ClassifyingTopos`

On construction (`__post_init__`), computes topos-theoretic invariants:

- `signature_shape`: (sorts, relations, axioms)
- `arity_spectrum`: sorted arity lengths
- `axiom_count`: total number of geometric axioms
- `theory_type`: the framework type string

### Theory Builders

**`build_typological_theory(category)`**: Converts a `CaseCategory` into a geometric theory by:

1. Each `CaseRole` object → sort
2. Each `Morphism` → relation symbol with arity `(source.name, target.name)`
3. Identity axiom: $x: \text{CaseRole} \vdash \exists \text{id}_x: \text{Hom}(x,x)$
4. Composition axiom: $f: \text{Hom}(A,B) \wedge g: \text{Hom}(B,C) \vdash \exists g \circ f: \text{Hom}(A,C)$

**`build_enriched_theory(enriched_cat)`**: Converts an `EnrichedCategory` by:

1. Each role → sort
2. Each significant hom-pair (proximity > 0.1) → relation symbol
3. Enriched identity: $\text{hom}(x,x) = 1$
4. Composition inequality: $\text{hom}(A,B) = p \wedge \text{hom}(B,C) = q \vdash \text{hom}(A,C) \geq p \cdot q$

### Bridge Transfer

```python
# Not re-exported from the package __init__ — import from the module:
from src.topos_theory.topos import bridge_transfer

def bridge_transfer(source_topos, target_topos, property_name) -> dict:
```

Runs `check_morita_equivalence()` and, when the necessary conditions hold, reports that the named property is *not ruled out* for transfer. Returns a dict with `property`, `source_theory`, `target_theory`, `morita_equivalent`, `transfer_possible`, `necessary_conditions_only` (always `True`), and any `mismatches`.

> **Necessary conditions only.** `check_morita_equivalence()` compares the signature shape (sorts, relations, axioms — exactly) and the arity spectrum. A `True` result means "not ruled out", never "equivalent": two signatures can agree on every invariant computed here and still classify different theories. Establishing $E_{T_1} \simeq E_{T_2}$ requires exhibiting the equivalence of classifying toposes, which this module does not do — so `transfer_possible` licenses *attempting* a transfer, not asserting its validity.

---

## Usage Examples

```python
from src.case_systems import standard_case_category
from src.enriched_cat import standard_enriched_category
from src.topos_theory import (
    build_typological_theory, build_enriched_theory,
    ClassifyingTopos, check_morita_equivalence,
)

# 1. Build theories from existing categories
cat = standard_case_category()
enriched = standard_enriched_category()

T_typ = build_typological_theory(cat, alignment_name="accusative")
T_enr = build_enriched_theory(enriched)

print(f"Typological: {len(T_typ.sorts)} sorts, {len(T_typ.axioms)} axioms")
print(f"Enriched: {len(T_enr.sorts)} sorts, {len(T_enr.axioms)} axioms")

# 2. Wrap in classifying toposes
E_typ = ClassifyingTopos(theory=T_typ)
E_enr = ClassifyingTopos(theory=T_enr)

# 3. Check the necessary conditions for Morita equivalence
not_ruled_out, mismatches = check_morita_equivalence(E_typ, E_enr)
print(f"Morita equivalence not ruled out: {not_ruled_out}")
if mismatches:
    for m in mismatches:
        print(f"  Mismatch: {m}")
```

---

## Manuscript Equations Implemented

| Equation | Function | Description |
| -------- | -------- | ----------- |
| Geometric sequent: $\varphi \vdash_x \psi$ | `Axiom.__str__()` | Geometric axiom format |
| Signature invariant | `GeometricTheory.signature_invariant()` | Morita necessary condition |
| Arity spectrum | `GeometricTheory.arity_spectrum()` | Morita necessary condition |
| $E_{T_1} \simeq E_{T_2}$ | `check_morita_equivalence()` | Necessary-condition screen for topos equivalence (never sufficient) |
| Bridge transfer | `bridge_transfer()` | Inter-theoretic property transfer, gated on that screen |

---

## Related Documentation

- **Upstream**: [`case_systems`](case_systems.md), [`enriched_cat`](enriched_cat.md)
- **Theory map**: [theory_implementation_map.md](../theory_implementation_map.md) §6
- **Literature**: [literature_guide.md](../literature_guide.md) — Caramello, Johnstone references
- **Glossary**: [glossary.md](../glossary.md) — Geometric Theory, Classifying Topos, Morita Equivalence

---

*Last updated: 2026-04-22. Source of truth: `src/topos_theory/__init__.py`.*
