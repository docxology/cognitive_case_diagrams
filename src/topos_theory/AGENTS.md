# 🤖 AGENTS.md — src/topos_theory/

## Overview

The `topos_theory` subpackage implements **§6** of the manuscript: topos-theoretic bridges between case systems. Geometric theories classify case systems as theories of a topos; **Morita equivalence** provides the formal criterion for when two case systems are inter-translatable.

> **Scope of the implementation**: `check_morita_equivalence` tests **necessary
> conditions only**. A `True` result means "not ruled out", never "equivalent".
> Establishing Morita equivalence requires exhibiting an equivalence of
> classifying toposes, which this module does not do.

> **References**: Caramello (2018) *Theories, Sites, Toposes*; Phillips (2021) universality of Language of Thought; Morita (1958) equivalence of module categories.

## Module Inventory

Line coverage: `uv run pytest tests/ --cov=src --cov-report=term-missing` (project root).

| Module | Key Exports |
|--------|-------------|
| `topos.py` | `TheoryType`, `Axiom`, `GeometricTheory`, `ClassifyingTopos`, `check_morita_equivalence()`, `build_typological_theory()`, `build_enriched_theory()`, `bridge_transfer()` |

`__all__` in [`__init__.py`](__init__.py) re-exports all of the above **except**
`bridge_transfer`, which is imported from the module: `from src.topos_theory.topos import bridge_transfer`.

## `topos.py`

### `Axiom` (dataclass)

Fields: `name: str`, `antecedent: str`, `consequent: str`, `sort_variables: list[str]`.

### `GeometricTheory` (dataclass)

A geometric theory `T` over the language of case systems. Fields are `name`,
`theory_type`, `sorts`, `relation_symbols` and `axioms` — a theory is built up
through its `add_*` methods, not by passing a signature dict:

```python
theory = GeometricTheory(
    name="T_accusative",
    theory_type=TheoryType.TYPOLOGICAL,
)
theory.add_sort("NOM")
theory.add_sort("ACC")
# every sort named in an arity must already exist, or add_relation raises ValueError
theory.add_relation("acts_on", ("NOM", "ACC"))
theory.add_axiom(Axiom(
    name="identity",
    antecedent="x: CaseRole",
    consequent="∃ id_x: Hom(x, x)",
    sort_variables=["x"],
))
```

| Member | Returns | Description |
|--------|---------|-------------|
| `sorts` | `list[str]` | Sort names (one per case role / object) |
| `relation_symbols` | `dict[str, tuple[str, ...]]` | Relation name → arity tuple |
| `axioms` | `list[Axiom]` | Geometric axioms |
| `signature_invariant()` | `tuple[int, int, int]` | `(num_sorts, num_relations, num_axioms)` |
| `arity_spectrum()` | `list[int]` | Sorted arity lengths |

**`TheoryType` enum** — the four members defined in `topos.py`:
- `TheoryType.TYPOLOGICAL` (`"typological"`) — cross-linguistic case theory
- `TheoryType.TYPE_LOGICAL` (`"type_logical"`) — type-logical grammar variant
- `TheoryType.DISTRIBUTIONAL` (`"distributional"`) — distributional variant
- `TheoryType.ENRICHED` (`"enriched"`) — [0,1]-enriched variant

### `ClassifyingTopos` (dataclass)

The classifying topos `E_T` of a geometric theory — the universal model of `T`:
```python
ct = ClassifyingTopos(theory=theory)
```

Fields: `theory` and `invariants`. `__post_init__` populates `invariants` with
exactly four keys — `signature_shape` (`= theory.signature_invariant()`),
`arity_spectrum`, `axiom_count`, and `theory_type`. There is no `signature_hash`.

### `check_morita_equivalence(topos1, topos2)`

Necessary-condition screen for the inter-theoretic translation criterion:
```
T₁ ≡_Morita T₂ ⟺ E_{T₁} ≃ E_{T₂}
```

It takes two **`ClassifyingTopos`** values (not `GeometricTheory`) and returns a
**tuple** `(not_ruled_out: bool, mismatches: list[str])`. The screen is:

1. `arity_spectrum` equality
2. `signature_shape` equality — `(sorts, relations, axioms)` compared exactly

```python
from src.case_systems.case_category import standard_case_category, minimal_case_category

acc = ClassifyingTopos(theory=build_typological_theory(standard_case_category(), "accusative"))
mini = ClassifyingTopos(theory=build_typological_theory(minimal_case_category(), "minimal"))

not_ruled_out, mismatches = check_morita_equivalence(acc, mini)
```

**Interpretation**: `not_ruled_out=True` means the two theories agree on every
invariant this module computes — they are *not ruled out* as Morita equivalent.
Two signatures can agree here and still classify different theories, so do not
read a `True` as "there exists a functorial translation preserving all
grammatical structure". A `False` is the informative direction: it rules the
equivalence out.

### `build_typological_theory(category, alignment_name="typological")`

Factory that formalizes a `CaseCategory` as a geometric theory — objects become
sorts, morphisms become relation symbols, and the identity/composition laws
become the two `Axiom` entries:

```python
from src.case_systems.case_category import standard_case_category
from src.enriched_cat import standard_enriched_category

acc_theory = build_typological_theory(standard_case_category(), "accusative")
enriched_theory = build_enriched_theory(standard_enriched_category())
```

Because there is one relation per morphism, the standard 8-case category yields
**8 sorts and 8 relation symbols**, and the minimal 3-role category yields **3
and 3**; both carry exactly 2 axioms. Re-derive these with
`len(T.sorts)` / `len(T.relation_symbols)` rather than quoting them.

### `bridge_transfer(source_topos, target_topos, property_name)`

Attempts inter-theoretic transfer of a named property via the bridge theorem. It
takes two `ClassifyingTopos` values and a property **name**, and **returns a
dict** — it does not raise on non-equivalence:

```python
result = bridge_transfer(source_topos, target_topos, "case_frame")
result["morita_equivalent"]          # necessary conditions passed
result["transfer_possible"]          # same flag
result["necessary_conditions_only"]  # always True — see the scope note above
result["mismatches"]                 # list[str]; empty when not ruled out
```

Because `necessary_conditions_only` is always `True`, a passing check licenses
*attempting* the transfer, never asserting its validity.

## Chain of Morita Equivalences (Manuscript §6)

The manuscript proposes a chain:
```
AccusativeEnglish ≡ AccusativeFrench ≡ ... (accusative family)
ErgativeGeorgian  ≡ ErgativeBasque   ≡ ... (ergative family)
```

This is a proposed basis for cross-linguistic case transfer in multilingual NLP
models. The code in this subpackage screens the necessary conditions for such a
chain; it does not certify any link in it.

## Caramello Connection

Olivia Caramello's **Toposes as Bridges** (2018) shows that invariants computed in the classifying topos of `T` are automatically preserved under Morita equivalence. The `invariants` dict in `ClassifyingTopos` approximates this: invariants that match between two theories are candidates for cross-lingual transfer.

## Phillips' Language of Thought

The manuscript argues (§6) that Phillips' (2021) result on the universality of the Language of Thought corresponds to a Morita equivalence between:
- **Syntax-based** case theories (surface morphosyntax)
- **Semantic-based** case theories (thematic role assignment)

`check_morita_equivalence` on a `TheoryType.TYPOLOGICAL` topos vs. a
`TheoryType.ENRICHED` one screens this computationally — it can rule the
correspondence out, but a pass is not a proof of it.

## Common Patterns

```python
from src.case_systems.case_category import standard_case_category, minimal_case_category
from src.topos_theory.topos import (
    ClassifyingTopos, TheoryType,
    build_typological_theory, check_morita_equivalence, bridge_transfer,
)

# Build two case theories and their classifying toposes
accusative = ClassifyingTopos(
    theory=build_typological_theory(standard_case_category(), "accusative")
)
minimal = ClassifyingTopos(
    theory=build_typological_theory(minimal_case_category(), "minimal")
)

# Screen the necessary conditions — returns (bool, list[str])
not_ruled_out, mismatches = check_morita_equivalence(accusative, minimal)
print(f"Not ruled out: {not_ruled_out}; mismatches: {mismatches}")

# Attempt a property transfer (returns a dict; never raises on mismatch)
result = bridge_transfer(accusative, minimal, "case_frame")
print(result["transfer_possible"], result["necessary_conditions_only"])
```
