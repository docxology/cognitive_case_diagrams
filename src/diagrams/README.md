# diagrams/ — §3–4: Categorial Grammar, DisCoCat, and Complexity

DisCoCat string diagrams, diagram complexity metrics (§4b), DisCoCirc-style discourse (§4c), ditransitive structures, and DisCoPy integration.

## Quick Import

```python
from src.diagrams.string_diagram import Sentence, Discourse
from src.diagrams.complexity_metrics import DiagramMetrics, diagram_depth, diagram_width
from src.diagrams.ditransitive import DitransitiveSentence

# DisCoPy integration (requires discopy >= 1.0.0)
from src.diagrams.string_diagram import (
    create_discopy_transitive,          # rigid.Box-based
    create_word_diagram_transitive,     # grammar.pregroup.Word + eager_parse
    create_swap_passive,                # Swap morphism for passivization
    create_tensor_semantics,            # F: Preg → FVect via tensor.eval()
)
```

## Key APIs

| Class/Function | Description |
|---------------|-------------|
| `Sentence` | DisCoCat string diagram with case-role metadata |
| `Sentence.transitive(subj, verb, obj)` | Factory for SVO sentences |
| `Discourse` | Multi-sentence DisCoCirc circuit with entity persistence |
| `DiagramMetrics` | `box_count`, `cup_count`, `depth`, `width`, `is_normal_form` |
| `diagram_depth(diagram)` | Sequential layers via `diagram.depth()` |
| `diagram_width(diagram)` | Max parallel wires via `diagram.width` |
| `syntactic_complexity_score(diagram)` | `words + 0.5*cups + 0.25*caps + 0.1*depth` |
| `create_word_diagram_*(...)` | Word-based diagrams via `grammar.pregroup.eager_parse` |
| `create_tensor_semantics(...)` | DisCoCat meaning functor evaluation in `discopy.tensor` |
| `DitransitiveSentence` | Three-argument frame (NOM, ACC, DAT) |

See [`AGENTS.md`](AGENTS.md) for full API reference and DisCoPy surface coverage; [`SKILL.md`](SKILL.md) for agent routing.
