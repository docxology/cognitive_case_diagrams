# Discourse: Entity Bookkeeping and State-Update Proposals {#sec:discocirc-discourse}

The same participant can occupy different grammatical roles across sentences. The `Discourse` helper records explicitly supplied entity names and role histories. For “Alice chases Bob. Bob fears Alice. Alice smiles,” Alice's stored sequence is NOM, ACC, NOM. This is bookkeeping over supplied sentence objects. It does not infer that the pronoun “she” refers to Alice.

```python
from src.diagrams.string_diagram import Sentence, Discourse
discourse = Discourse()
discourse.add_sentence(Sentence.transitive("Alice", "chases", "Bob"))
discourse.add_sentence(Sentence.transitive("Bob", "fears", "Alice"))
discourse.add_sentence(Sentence.intransitive("Alice", "smiles"))
assert [r.name for r in discourse.role_history["Alice"]] == ["NOM", "ACC", "NOM"]
```

![Tensor juxtaposition of two independently typed sentence diagrams. The output $s\otimes s$ does not itself encode coreference or a shared semantic memory.](output/figures/discopy_discocirc_discourse.png){#fig:discourse}

![Native entity-history drawing for the two-sentence example. Persistent lines visualize explicit name matching in the supplied data.](output/figures/discourse_string_diagram.png){#fig:native-discourse}

![Three independently constructed sentence diagrams with repeated entity labels. Shared spelling is visible, but a tensor of sentence outputs does not implement a DisCoCirc state-update circuit.](output/figures/discopy_three_sentence_discourse.png){#fig:three-sentence-discourse}

![A separate history ribbon makes the supplied role changes readable. The construction illustrates entity persistence without claiming learned coreference or implemented Frobenius updates.](output/figures/discocirc_entity_persistence.png){#fig:discocirc-persistence}

A full discourse model would specify persistent semantic states and the update maps applied by sentences. It would also need a policy for aliases, repeated names, pronouns, and distinct participants with identical surface forms. These are open requirements here. Quantum compilation and trainability would introduce further choices of encoding, ansatz, observable, optimization, and hardware. Local observables alone do not justify an unconditional claim that barren plateaus are absent. No quantum circuit is trained in this project.
