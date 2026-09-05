# 🤖 AGENTS.md — src/diagrams/

## Overview

The `diagrams` subpackage implements **§3–4** of the manuscript: DisCoCat string diagrams, diagram complexity metrics (§4b), DisCoCirc discourse (§4c), and ditransitive sentence structures. This is the core computational linguistics layer connecting categorical grammar to natural language.

## Module Inventory

| Module | Key Exports | § |
|--------|-------------|---|
| `string_diagram.py` | `Sentence`, `Discourse`, `Wire`, `Box`; DisCoPy integration (`create_discopy_*`, `create_word_diagram_*`, `create_tensor_semantics`) | §3–4 |
| `complexity_metrics.py` | `DiagramMetrics`, `diagram_depth()`, `diagram_width()`, `syntactic_complexity_score()`, `compute_pqc_decoherence_proxy()` | §4b |
| `complexity_examples.py` | `build_complexity_examples()` — 10 canonical DisCoPy diagrams for complexity figures | §4b |
| `ditransitive.py` | `DitransitiveSentence`, `create_ditransitive()`, `create_discopy_ditransitive()` | §3 |

## `string_diagram.py` — Native + DisCoPy Integration

### Native Representations

A `Sentence` encodes a sentence as a DisCoCat string diagram with case-role metadata:

```python
sent = Sentence.transitive("Alice", "chases", "Bob")
sent.case_assignments  # {"Alice": CaseRole.NOM, "Bob": CaseRole.ACC}
sent.num_boxes         # 3 (2 nouns + 1 verb)
sent.codomain_type     # "s"
```

A `Discourse` extends to multi-sentence text with persistent entity wires (DisCoCirc):

```python
disc = Discourse.two_sentence("Alice", "chases", "Bob", "Bob", "runs")
disc.role_reversal_entities()     # entities with changing case roles

# For ACC→NOM hijacking detection (§9b), use CaseFrameValidator:
from src.security.cognitive_security import CaseFrameValidator
validator = CaseFrameValidator()
final = {e: roles[-1] for e, roles in disc.role_history.items()}
violations = validator.validate_assignment(final)
```

### DisCoPy Integration — Base Functions (`discopy.rigid`)

These use `discopy.rigid.Box` and manual Cup placement:

| Function | Returns | Description |
|----------|---------|-------------|
| `create_discopy_transitive(subj, verb, obj)` | `rigid.Diagram` | SVO sentence |
| `create_discopy_intransitive(subj, verb)` | `rigid.Diagram` | SV sentence |
| `create_discopy_passive(subj, verb, agent)` | `rigid.Diagram` | Passive voice |
| `create_discopy_snake_equation()` | 3-tuple | Compact closure axiom (left, id, right) |
| `create_discopy_composition(subj, verb, obj)` | 2-tuple | Pre/post-contraction |
| `create_discopy_multilingual(translations)` | `dict[str, Diagram]` | 6-language isomorphism |
| `create_discopy_complex_transitive()` | `rigid.Diagram` | 9-word complex sentence |

### DisCoPy Integration — Extended Functions (`discopy.grammar.pregroup`)

These use `grammar.pregroup.Word` and `eager_parse` for proper lexical entries with automatic Cup placement:

| Function | Returns | Description |
|----------|---------|-------------|
| `create_word_diagram_transitive(subj, verb, obj)` | `pregroup.Diagram` | Word-based SVO via eager_parse |
| `create_word_diagram_intransitive(subj, verb)` | `pregroup.Diagram` | Word-based SV via eager_parse |
| `create_swap_passive(subj, verb, agent)` | `pregroup.Diagram` | Passivization via Swap morphism |
| `create_word_diagram_ditransitive(subj, verb, io, do)` | `pregroup.Diagram` | 4-word ditransitive via eager_parse |

### DisCoPy Integration — Tensor Semantics (`discopy.tensor`)

Implements the DisCoCat meaning functor F: Preg → FVect:

```python
from src.diagrams.string_diagram import create_tensor_semantics
diagram, meaning = create_tensor_semantics("Alice", "chases", "Bob")
# meaning.shape == (4,) — sentence meaning vector in FVect
```

## `complexity_metrics.py` — Metrics & Quantum Bounds

### Complexity Metrics

All metrics operate on real DisCoPy `rigid.Diagram` objects:

| Function | Returns | Description |
|----------|---------|-------------|
| `count_boxes(diagram)` | `int` | Total box count |
| `count_words(diagram)` | `int` | Lexical boxes (excluding Cup/Cap) |
| `count_cups(diagram)` | `int` | Cup contractions |
| `count_caps(diagram)` | `int` | Cap expansions |
| `diagram_depth(diagram)` | `int` | Sequential layers (`diagram.depth()`) |
| `diagram_width(diagram)` | `int` | Max parallel wires (`diagram.width`) |
| `syntactic_complexity_score(diagram, w_words=1.0, w_cups=0.5, w_caps=0.25, w_depth=0.1)` | `float` | `w_words·words + w_cups·cups + w_caps·caps + w_depth·depth` — the four weights are tunable kwargs, and the term is **words** (lexical boxes), not total boxes |
| `analyze_diagram(diagram, name)` | `DiagramMetrics` | All metrics in one call |
| `compare_diagrams(diagrams)` | `list[DiagramMetrics]` | Multi-diagram comparison |

### Quantum Magnitude Homology (§5b)

```python
metrics = compute_pqc_decoherence_proxy(diagram, environmental_noise=0.05)
metrics.quantum_environment_commutes  # True if the cup/cap proxy decoherence < 0.25
```

`MagnitudeHomologyMetrics` holds exactly four fields —
`base_syntactic_complexity: float`, `topological_holes_1d: int`,
`estimated_decoherence_rate: float`, `quantum_environment_commutes: bool`. It
records a scalar complexity, a 1-D hole count and a decoherence estimate; it does
**not** hold graded homology groups. Treat the Leinster–Shulman graded invariant
as the theoretical target this class gestures at, not the implemented object.

## `ditransitive.py` — Three-Argument Verbs

```python
ds = DitransitiveSentence(subject="Alice", verb="gave",
                          direct_object="book", indirect_object="Bob")
ds.case_assignments  # {"Alice": NOM, "Bob": DAT, "book": ACC}
ds.num_arguments     # 3
```

DisCoPy integration: `create_discopy_ditransitive()` builds `n.r @ s @ n.l @ n.l` verb type with 3 cups.

## DisCoPy API Surface Used

| DisCoPy Module | Classes/Functions | Purpose |
|----------------|-------------------|---------|
| `discopy.rigid` | `Ty`, `Box`, `Cup`, `Cap`, `Id`, `Diagram` | Base pregroup diagrams |
| `discopy.grammar.pregroup` | `Word`, `eager_parse`, `Swap`, `Cup` | Proper lexical entries, automatic parsing |
| `discopy.tensor` | `Box`, `Cup`, `Id`, `Dim`, `.eval()` | Semantic evaluation (F: Preg → FVect) |
| `discopy.drawing` | `Equation` | Multi-panel diagram rendering |
| `Diagram` methods | `.normal_form()`, `.depth()`, `.width`, `.boxes`, `.dom`, `.cod` | Metrics and verification |
