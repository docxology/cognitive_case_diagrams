# diagrams: implementation reference

Explicit DisCoPy pregroup constructions, tensor examples, diagram counts, and entity-name bookkeeping. `Discourse` does not infer coreference or implement a complete DisCoCirc semantic state update. `MagnitudeHomologyMetrics` contains a synthetic cup/cap score, not homology or measured decoherence.

| Source module | Defined entry points |
| :--- | :--- |
| [complexity_examples.py](../../src/diagrams/complexity_examples.py) | `build_complexity_examples` |
| [complexity_metrics.py](../../src/diagrams/complexity_metrics.py) | `DiagramMetrics`, `count_boxes`, `count_words`, `count_cups`, `count_caps`, `diagram_depth`, `diagram_width`, `compute_normal_form`, `is_in_normal_form`, `diagrams_equal`, `analyze_diagram`, `syntactic_complexity_score`, `compare_diagrams`, `MagnitudeHomologyMetrics`, `compute_pqc_decoherence_proxy` |
| [ditransitive.py](../../src/diagrams/ditransitive.py) | `DitransitiveSentence`, `create_ditransitive`, `create_discopy_ditransitive` |
| [string_diagram.py](../../src/diagrams/string_diagram.py) | `AtomicType`, `Wire`, `Box`, `Sentence`, `Discourse`, `create_discopy_transitive`, `create_discopy_complex_transitive`, `create_discopy_intransitive`, `create_discopy_passive`, `create_discopy_snake_equation`, `create_discopy_composition`, `create_discopy_multilingual`, `create_word_diagram_transitive`, `create_word_diagram_intransitive`, `create_swap_passive`, `create_word_diagram_ditransitive`, `create_tensor_semantics` |

See the [package guide](../../src/diagrams/README.md), [method contracts](../method_contracts.md), and [claim ledger](../claim_ledger.md). These describe implementation scope; the manuscript distinguishes implemented examples from proposed extensions.
