# Module: `diagrams` — From Phrase Structure to DisCoCat (§3–4c)

> **Package**: `src.diagrams`
> **Manuscript**: §3 *Categorial Grammar*, §4 *Categorical Semantics*, §4b *Compact Closure & Complexity*, §4c *DisCoCirc Discourse*
> **Dependencies**: `case_systems` (for `CaseRole`); `discopy >= 1.0.0` (optional, for DisCoPy integration)
> **Test files**: `tests/test_diagrams*.py`, `tests/test_discopy_extended.py`

---

## Purpose

The `diagrams` package implements the **string-diagrammatic** representations central to compositional distributional semantics (DisCoCat and DisCoCirc). It provides:

1. **DisCoCat sentences**: Native `Sentence` representation + real DisCoPy diagram generation
2. **DisCoCirc discourse**: Multi-sentence entity persistence via `Discourse` with prompt injection detection
3. **Complexity metrics**: Cup/cap/box counting, depth/width, syntactic complexity scores, normal-form comparison
4. **Ditransitive constructions**: Three-argument verb diagrams (give, show, tell)
5. **DisCoPy integration**: Three layers — `rigid.Box` (base), `grammar.pregroup.Word` (extended), `tensor.eval()` (semantic)

---

## Architecture

```text
diagrams/
├── __init__.py            # Public API: 13 exported symbols
├── string_diagram.py      # Native: AtomicType, Wire, Box, Sentence, Discourse
│                          # DisCoPy base: create_discopy_*(rigid.Box)
│                          # DisCoPy extended: create_word_diagram_*(grammar.pregroup.Word)
│                          # DisCoPy tensor: create_tensor_semantics(tensor.eval)
├── complexity_metrics.py  # diagram_depth, diagram_width, syntactic_complexity_score,
│                          # analyze_diagram, DiagramMetrics, MagnitudeHomologyMetrics
├── complexity_examples.py # 10 canonical DisCoPy diagrams for complexity figures
└── ditransitive.py        # DitransitiveSentence, create_discopy_ditransitive
```

### Dependency Position

```text
case_systems.CaseRole
    ↓
diagrams (imports CaseRole for case assignment)
    ↓
visualization.string_diagrams (matplotlib rendering)
visualization.complexity_plots (metric charts)
visualization.discopy_diagrams (DisCoPy .draw() rendering)
```

---

## Module Reference

### `string_diagram.py` — Native Representations

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `AtomicType` | `@dataclass(frozen=True)` | Atomic pregroup type: `name: str` |
| `N`, `S` | constant | Noun type, Sentence type |
| `Wire` | `@dataclass(frozen=True)` | Typed wire: `wire_type`, `entity`, `case_role` |
| `Box` | `@dataclass` | Box (word): `name`, `dom: list[Wire]`, `cod: list[Wire]` |
| `Sentence` | `@dataclass` | DisCoCat single-sentence: `text`, `boxes`, `wires`, `case_assignments` |
| `Discourse` | `@dataclass` | DisCoCirc multi-sentence: `sentences`, `entity_wires`, `role_history` |

**`Sentence` factory methods**: `Sentence.transitive(subj, verb, obj)`, `Sentence.intransitive(subj, verb)`

**`Discourse` factory methods**: `Discourse.two_sentence(...)`, `Discourse.role_reversal(entity, partner)`

For discourse-level prompt-injection detection (§9b cognitive security), feed per-entity assignments from `Discourse.role_history` into `src.security.cognitive_security.CaseFrameValidator.validate_assignment()`.

### `string_diagram.py` — DisCoPy Integration

**Base functions** (`discopy.rigid.Box` — manual Cup placement):

| Function | Returns | Description |
|----------|---------|-------------|
| `create_discopy_transitive(subj, verb, obj)` | `rigid.Diagram` | 3 boxes + 2 cups → s |
| `create_discopy_intransitive(subj, verb)` | `rigid.Diagram` | 2 boxes + 1 cup → s |
| `create_discopy_passive(subj, verb, agent)` | `rigid.Diagram` | Passive voice |
| `create_discopy_complex_transitive()` | `rigid.Diagram` | 9-word sentence |
| `create_discopy_snake_equation()` | 3-tuple | Compact closure axiom |
| `create_discopy_composition(subj, verb, obj)` | 2-tuple | Pre/post-contraction |
| `create_discopy_multilingual(translations)` | `dict[str, Diagram]` | 6-language isomorphism |

**Extended functions** (`discopy.grammar.pregroup.Word` + `eager_parse`):

| Function | Returns | Description |
|----------|---------|-------------|
| `create_word_diagram_transitive(subj, verb, obj)` | `pregroup.Diagram` | Automatic cup placement |
| `create_word_diagram_intransitive(subj, verb)` | `pregroup.Diagram` | 2-word parsing |
| `create_swap_passive(subj, verb, agent)` | `pregroup.Diagram` | Swap morphism passivization |
| `create_word_diagram_ditransitive(subj, verb, io, do)` | `pregroup.Diagram` | 4-word parsing |

**Tensor semantics** (`discopy.tensor` — DisCoCat F: Preg → FVect):

| Function | Returns | Description |
|----------|---------|-------------|
| `create_tensor_semantics(subj, verb, obj, ...)` | `(Diagram, ndarray)` | Meaning functor evaluation |

### `complexity_metrics.py` — Diagram Complexity

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `DiagramMetrics` | `@dataclass` | `box_count`, `word_count`, `cup_count`, `cap_count`, `depth`, `width`, `is_normal_form` |
| `count_boxes(diagram)` | function | Total boxes |
| `count_words(diagram)` | function | Lexical boxes (excluding Cup/Cap) |
| `count_cups(diagram)` | function | Cup contractions |
| `count_caps(diagram)` | function | Cap expansions |
| `diagram_depth(diagram)` | function | `diagram.depth()` — sequential layers |
| `diagram_width(diagram)` | function | `diagram.width` — max parallel wires |
| `syntactic_complexity_score(diagram)` | function | `words + 0.5*cups + 0.25*caps + 0.1*depth` |
| `analyze_diagram(diagram, name)` | function | Comprehensive `DiagramMetrics` |
| `compare_diagrams(diagrams)` | function | Multi-diagram comparison |
| `MagnitudeHomologyMetrics` | `@dataclass` | Quantum environment bounds (§5b) |
| `compute_quantum_magnitude_homology(diagram, noise)` | function | Decoherence safety bounds |

### `ditransitive.py` — Three-Argument Verbs

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `DitransitiveSentence` | `@dataclass` | `subject`, `verb`, `direct_object`, `indirect_object` (NOM/ACC/DAT) |
| `create_ditransitive(subj, verb, io, do)` | factory | Native ditransitive sentence |
| `create_discopy_ditransitive(subj, verb, io, do)` | factory | DisCoPy diagram with `n.r @ s @ n.l @ n.l` type |

---

## Usage Examples

```python
# Native representation
from src.diagrams.string_diagram import Sentence, Discourse
from src.security.cognitive_security import CaseFrameValidator
sent = Sentence.transitive("Alice", "chases", "Bob")
disc = Discourse.role_reversal("Alice", "Bob")
validator = CaseFrameValidator()
# Validate the final role assignment snapshot from the discourse
final_assignment = {e: roles[-1] for e, roles in disc.role_history.items()}
violations = validator.validate_assignment(final_assignment)  # [] if well-typed

# DisCoPy base (rigid.Box)
from src.diagrams.string_diagram import create_discopy_transitive
diagram = create_discopy_transitive("Alice", "chases", "Bob")
assert diagram.cod == Ty('s')

# DisCoPy extended (grammar.pregroup.Word + eager_parse)
from src.diagrams.string_diagram import create_word_diagram_transitive
diagram = create_word_diagram_transitive("Alice", "chases", "Bob")

# DisCoPy tensor semantics (F: Preg → FVect)
from src.diagrams.string_diagram import create_tensor_semantics
_, meaning = create_tensor_semantics("Alice", "chases", "Bob")
# meaning.shape == (4,) — sentence meaning vector

# Complexity metrics
from src.diagrams.complexity_metrics import diagram_depth, syntactic_complexity_score
depth = diagram_depth(diagram)
score = syntactic_complexity_score(diagram)
```

---

## Manuscript Equations Implemented

| Equation | Function | Description |
| -------- | -------- | ----------- |
| Pregroup types $n, s, n^l, s^r$ | `AtomicType` + DisCoPy `Ty` | Lambek 1958/1999 |
| DisCoCat meaning functor $F: \mathbf{Preg} \to \mathbf{FVect}$ | `create_tensor_semantics()` | Coecke, Sadrzadeh & Clark 2010 |
| Cup contraction $\varepsilon: n \otimes n^r \to 1$ | DisCoPy `Cup` | §3 |
| Snake equation (eq. 4-3) | `create_discopy_snake_equation()` + `normal_form()` | §4b |
| Complexity (eq. 4-4) | `syntactic_complexity_score()` | words + 0.5·cups + 0.25·caps + 0.1·depth |
| Circuit depth | `diagram_depth()` | §4b |
| DisCoCirc entity persistence | `Discourse` + `entity_wires` | de Felice et al. 2022 |
| Passivization as Swap | `create_swap_passive()` | §3b |
| Prompt injection detection (ACC→NOM) | `src.security.cognitive_security.CaseFrameValidator.validate_assignment()` | §9b |
| Ditransitive 3-argument | `DitransitiveSentence` + `create_discopy_ditransitive()` | §3 |

---

## DisCoPy API Surface Coverage

| DisCoPy Module | Classes/Functions Used | Project Functions |
|----------------|----------------------|-------------------|
| `discopy.rigid` | `Ty`, `Box`, `Cup`, `Cap`, `Id`, `Diagram` | `create_discopy_*()` |
| `discopy.grammar.pregroup` | `Word`, `eager_parse`, `Swap`, `Cup` | `create_word_diagram_*()`, `create_swap_passive()` |
| `discopy.tensor` | `Box`, `Cup`, `Id`, `Dim`, `.eval()` | `create_tensor_semantics()` |
| `discopy.drawing` | `Equation` | `visualization/discopy_diagrams.py` |
| `Diagram` methods | `.normal_form()`, `.depth()`, `.width`, `.boxes`, `.dom`, `.cod` | Complexity metrics |

---

*Last updated: 2026-04-22. Source of truth: `src/diagrams/__init__.py`.*
