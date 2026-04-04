# 🤖 AGENTS.md — src/topos_theory/

## Overview

The `topos_theory` subpackage implements **§6** of the manuscript: topos-theoretic bridges between case systems. Geometric theories classify case systems as theories of a topos; **Morita equivalence** provides the formal criterion for when two case systems are inter-translatable.

> **References**: Caramello (2018) *Theories, Sites, Toposes*; Phillips (2021) universality of Language of Thought; Morita (1958) equivalence of module categories.

## Module Inventory

Line coverage: `uv run pytest tests/ --cov=src --cov-report=term-missing` (project root).

| Module | Key Exports |
|--------|-------------|
| `topos.py` | `GeometricTheory`, `ClassifyingTopos`, `TheoryType`, `check_morita_equivalence()`, `build_typological_theory()`, `bridge_transfer()` |

## `topos.py`

### `GeometricTheory` (dataclass)

A geometric theory `T` over the language of case systems:
```python
theory = GeometricTheory(
    name="AccusativeTheory",
    theory_type=TheoryType.TYPOLOGICAL,
    axioms=["NOM_agent", "ACC_patient", "nom_acc_alignment"],
    signature={"case_roles": 8, "alignment": "accusative"},
    functors=["acts_on", "receives"],
    invariants={"arity": 2},
)
```

**Axioms** encode the case-role assignments and morphism constraints of a language's case system.

**`TheoryType` enum**:
- `TheoryType.TYPOLOGICAL` — cross-linguistic case theory
- `TheoryType.ALIGNMENT` — accusative/ergative/tripartite
- `TheoryType.ENRICHED` — [0,1]-enriched variant
- `TheoryType.FLUID_S` — split-intransitive

### `ClassifyingTopos` (dataclass)

The classifying topos `Set[T^op]` of a geometric theory — the universal model of `T`:
```python
ct = ClassifyingTopos(theory=theory)
```

**Computed invariants** (in `__post_init__`):
- `signature_hash`: canonical hash of the theory signature for Morita comparison
- `invariants`: arity spectrum, functor count, axiom count

### `check_morita_equivalence(theory_a, theory_b)`

The central inter-theoretic translation check:
```
T₁ ≡_Morita T₂ ⟺ Set[T₁^op] ≅ Set[T₂^op]
```

In the implementation, equivalence is checked via:
1. `arity_spectrum` equality (same functor arities)
2. Structural invariant matching (annotation-level checks)

```python
accusative = build_typological_theory("accusative", ["acts_on", "receives"])
ergative = build_typological_theory("ergative", ["is_agent_of", "is_patient_of"])

result = check_morita_equivalence(accusative, ergative)
# result = {"equivalent": bool, "reason": str, "shared_invariants": dict}
```

**Interpretation**: If `equivalent=True`, there exists a functorial translation between the two case systems that preserves all grammatical structure — a cross-linguistic universal.

### `build_typological_theory(alignment_type, functors)`

Factory for alignment-specific geometric theories:

```python
acc_theory = build_typological_theory("accusative", ["acts_on", "receives"])
erg_theory = build_typological_theory("ergative", ["is_agent_of", "is_patient_of"])
enriched_theory = build_enriched_theory(standard_enriched_category())
```

### `bridge_transfer(source_theory, target_theory, knowledge)`

If two theories are Morita-equivalent, transfer knowledge (case frame, lexical knowledge, etc.) from source's model to target's model:

```python
equiv_check = check_morita_equivalence(german_theory, latin_theory)
if equiv_check["equivalent"]:
    transferred = bridge_transfer(german_theory, latin_theory, knowledge_payload)
    # transferred: dict with keys from target_theory's vocabulary
```

Raises `ValueError` if theories are not Morita-equivalent (transfer would be invalid).

## Chain of Morita Equivalences (Manuscript §6)

The manuscript establishes a chain:
```
AccusativeEnglish ≡ AccusativeFrench ≡ ... (accusative family)
ErgativeGeorgian  ≡ ErgativeBasque   ≡ ... (ergative family)
```

This provides a computational basis for cross-linguistic case transfer in multilingual NLP models.

## Caramello Connection

Olivia Caramello's **Toposes as Bridges** (2018) shows that invariants computed in the classifying topos of `T` are automatically preserved under Morita equivalence. The `invariants` dict in `ClassifyingTopos` approximates this: invariants that match between two theories are candidates for cross-lingual transfer.

## Phillips' Language of Thought

The manuscript argues (§6) that Phillips' (2021) result on the universality of the Language of Thought corresponds to a Morita equivalence between:
- **Syntax-based** case theories (surface morphosyntax)
- **Semantic-based** case theories (thematic role assignment)

`check_morita_equivalence` with `TheoryType.TYPOLOGICAL` vs. `TheoryType.ENRICHED` tests this computationally.

## Common Patterns

```python
from src.topos_theory.topos import (
    GeometricTheory, TheoryType,
    build_typological_theory, check_morita_equivalence, bridge_transfer,
)

# Build two case theories
accusative = build_typological_theory("accusative", ["acts_on", "receives"])
tripartite = build_typological_theory("tripartite", ["acts_on", "receives", "is_sole"])

# Check if they are Morita-equivalent
result = check_morita_equivalence(accusative, tripartite)
print(f"Equivalent: {result['equivalent']}, reason: {result['reason']}")

# Transfer knowledge if equivalent
if result["equivalent"]:
    transferred = bridge_transfer(accusative, tripartite, knowledge={"acts_on": "John sees Mary"})
```
