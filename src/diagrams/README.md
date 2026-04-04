# diagrams/ — §3–§4c: String diagrams

DisCoCat string diagrams, diagram complexity metrics (§4b), DisCoCirc-style discourse (`Discourse`, §4c), ditransitive structures.

## Quick Import

```python
from src.diagrams.string_diagram import Sentence, Discourse
from src.diagrams.complexity_metrics import DiagramMetrics
from src.diagrams.ditransitive import DitransitiveSentence
```

## Key APIs

| Class/Function | Description |
|---------------|-------------|
| `Sentence` | DisCoCat string diagram for a sentence |
| `Sentence.type_reduce()` | Reduce pregroup type to canonical form |
| `Sentence.complexity()` | Returns `DiagramMetrics` |
| `Sentence.as_discopy()` | Convert to real DisCoPy diagram |
| `Discourse` | Multi-sentence DisCoCirc circuit with entity state wires |
| `DiagramMetrics` | `box_count`, `cup_count`, `word_count`, `normal_form_steps`, `complexity_score` |
| `DitransitiveSentence` | Three-argument frame (NOM, ACC, DAT) with dative alternation |

See [`AGENTS.md`](AGENTS.md) for full API reference, complexity metric formulas, and quantum compilation pathway; [`SKILL.md`](SKILL.md) for agent routing.
