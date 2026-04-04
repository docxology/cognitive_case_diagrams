# 🤖 AGENTS.md — src/diagrams/

## Overview

The `diagrams` subpackage implements **§3–§4c** of the manuscript: DisCoCat string diagrams, diagram complexity metrics (manuscript §4b / `04b_compact_closure_complexity.md`), DisCoCirc discourse via `Discourse` in `string_diagram.py` (§4c), and ditransitive sentence structures. This is the core computational linguistics layer connecting categorical grammar to natural language.

## Module Inventory

Line coverage: `uv run pytest tests/ --cov=src --cov-report=term-missing` (project root).

| Module | Key Exports | § |
|--------|-------------|---|
| `string_diagram.py` | `Sentence`, `Discourse`, `Wire`, `Box`, string parsers; multi-sentence discourse / entity wires | §3–§4c |
| `complexity_metrics.py` | `DiagramMetrics`, `box_count()`, `cup_count()`, `word_count()`, `normal_form_steps()` | §4b |
| `complexity_examples.py` | `build_complexity_examples()` — canonical DisCoPy diagrams for complexity figures | §4b |
| `ditransitive.py` | `DitransitiveSentence`, `ThreeParticipantFrame` | §3 |

## `string_diagram.py` — `Sentence` and `Discourse`

### DisCoCat Sentence Representation

A `Sentence` encodes a sentence as a DisCoCat string diagram:
- Each word is a `Box` with a pregroup type
- Types compose via cups (identity contractions) and caps
- The grammatical type of a sentence reduces to `s` (sentence)

```python
sent = Sentence(
    words=["John", "sees", "Mary"],
    case_roles=[CaseRole.NOM, None, CaseRole.ACC],
    type_string="n s n",   # Pregroup type before reduction
)
```

**Key operations**:

| Method | Returns | Description |
|--------|---------|-------------|
| `type_reduce()` | `str` | Reduce pregroup type → canonical type string |
| `as_discopy()` | `discopy.grammar.Diagram` | Convert to real DisCoPy diagram object |
| `complexity()` | `DiagramMetrics` | Compute all complexity metrics |
| `to_normal_form()` | `Sentence` | Apply cup reductions to normal form |
| `wires()` | `list[Wire]` | All connecting wires between boxes |

### DisCoCirc Discourse Representation

A `Discourse` extends sentences to multi-sentence discourse via entity state wires (DisCoCirc; manuscript §4c):

```python
discourse = Discourse(
    sentences=[sent1, sent2, sent3],
    entity_ids={"John": 0, "Mary": 1},
)
# Entity wires persist across sentences: John's state in sent1 feeds into sent2
```

**Key concepts**:
- **State wires**: persistent entity representations flowing between sentences
- **Case role reversal**: passive constructions reorder argument wires
- **Discourse entanglement**: later sentences constrain earlier entity interpretations

### Discopy Integration

When `discopy >= 1.0.0` is installed, `Sentence.as_discopy()` generates real DisCoPy diagram objects that can be further composed, rendered, or compiled to quantum circuits via lambeq.

## `complexity_metrics.py` — `DiagramMetrics`

### Complexity Invariants

The manuscript §4b defines complexity metrics for string diagrams as publishing standards:

| Metric | Formula | Interpretation |
|--------|---------|---------------|
| `box_count` | `\|{boxes}\|` | Word complexity (number of semantic units) |
| `cup_count` | `\|{cups}\|` | Contraction depth (syntactic dependency density) |
| `word_count` | `\|{words}\|` | Surface form length |
| `normal_form_steps` | `n_reductions` | Abstractness (steps to canonical form) |
| `complexity_score` | Weighted combination | Single-number complexity index |

```python
metrics = DiagramMetrics(sentence=sent)
print(f"Box count: {metrics.box_count()}")
print(f"Cup count: {metrics.cup_count()}")
print(f"Score: {metrics.complexity_score():.3f}")
```

**Categorical magnitude** of a sentence can be approximated via:
```
|sent| ≈ box_count - cup_count (net diagram size)
```

### Normal Form Comparison

```python
before = sentence.complexity()
after = sentence.to_normal_form().complexity()
reduction = before.complexity_score() - after.complexity_score()
# reduction > 0 → non-trivial simplification available
```

## `ditransitive.py` — `DitransitiveSentence`

### Three-Participant Frames

Ditransitive sentences have three core arguments:

```python
frame = DitransitiveSentence(
    agent=("John", CaseRole.NOM),
    theme=("book", CaseRole.ACC),
    recipient=("Mary", CaseRole.DAT),
    verb="gave",
)
# Encodes: John [NOM] gave the book [ACC] to Mary [DAT]
```

**Dative alternation** (syntactic transformation preserving meaning):
```python
double_object = frame.dative_alternation()
# → "John gave Mary the book" — different surface, same semantic frame
```

## Connecting to the Quantum Layer

The string diagram framework connects directly to §8 via:
1. DisCoPy sentence diagrams → lambeq → Parameterized Quantum Circuit (PQC)
2. PQC operates on Hilbert space ℋ^n ⊗ ... ⊗ ℋ^n (one qudit per case role)
3. Case role assignment = POVM measurement on the output state

The **PQC trainability** results (manuscript §4c, discourse / QNLP) — barren plateau bounds for IQP/Sim4 ansätze — address gradient scaling for discourse-level circuits.
