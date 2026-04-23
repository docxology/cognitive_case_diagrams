# Beyond the Sentence: State Wires Accumulate Semantic History Across Discourse {#sec:discocirc-discourse}

**Where we are in the argument.** \autoref{sec:categorical-semantics}–\autoref{sec:compact-closure-complexity} formalised individual sentences as compact-closed string diagrams and their complexity as a four-metric summary. This chapter extends composition *across* sentence boundaries: de Felice–Coecke DisCoCirc adds persistent entity wires that carry an entity's case-role history across a discourse, so that a three-sentence discourse traces Alice's NOM → ACC → NOM trajectory and Bob's ACC → NOM trajectory as first-class diagrammatic data rather than coreference annotation bolted on after the fact.

## DisCoCirc State Wires Resolve Coreference and Role Shifts

De Felice and Coecke [-@defelice2020discourse] address this limitation by formulating **DisCoCirc** (Distributional Compositional Circuits). DisCoCirc extends the base categorical framework, empowering it to dynamically handle discourse-level semantic structure.

Specifically, DisCoCirc introduces continuous *state wires* that actively persist across isolated sentence boundaries, continuously encoding the dynamically evolving states of distinct discourse entities (e.g., characters, objects, shifting topics). For example, a multi-sentence sequence like "Alice chased Bob. He was terrified." is explicitly represented as an integrated geometric circuit where:

- Alice and Bob are wires that persist across both sentences.
- The pronoun "He" is resolved by actively connecting its topological wire directly to Bob's wire.
- The shifting emotional state "terrified" seamlessly updates the cumulative state information carried exclusively by Bob's persistent wire.

De Felice et al. [-@defelice2022discocirc] subsequently extended this approach, developing a full-fledged, multi-layered circuit model built to systematically resolve ambiguity, tangled coreference, and overarching discourse coherence—all locked within the exact same continuous categorical formalism. A CCG-based pipeline for generating discourse circuits from syntactic parse trees has demonstrated that DisCoCirc can scale to text, dynamically composing sentence-level diagrams along shared entity wires via an iterative process of coreference resolution and wire merging [-@duneau2021parsing]. This pipeline approach has since been extended to a comparative framework for evaluating compositional AI model architectures [-@duneau2025comparative], confirming that the DisCoCirc wire-merging strategy generalizes across model families. Complementary work on **DiscoSG** (Discourse Scene Graphs) extends this approach to multi-sentence image captions, parsing text into scene graphs that capture cross-sentence coreference relations. \autoref{fig:discourse} illustrates a multi-sentence discourse diagram where entity wires persist across sentence boundaries. For case theory, DisCoCirc is significant because it shows how case-marked argument structure *composes across discourse*: the nominative subject of one sentence can become the accusative object of the next, and this transformation is tracked as a morphism in the discourse category.

![DisCoCirc type structure encodes discourse coherence as a tensor product of sentence types. DisCoPy pregroup grammar for "Alice chases Bob. Bob runs." showing inter-sentential composition. **Sentence 1** (left subdiagram): Alice ($n$) and Bob ($n$) contract into "chases" ($n^r \otimes s \otimes n^l$) via two Cups, yielding sentence type $s$. **Sentence 2** (right subdiagram): Bob ($n$) contracts into "runs" ($n^r \otimes s$) via one Cup, yielding $s$. The joint discourse type $s \otimes s$ encodes inter-sentential coherence as a tensor product, the computational primitive that DisCoCirc state wires exploit to propagate Bob's semantic state from ACC (sentence 1) to NOM (sentence 2). See \autoref{fig:native-discourse} for wire-colour confirmation of the role transition, and \autoref{fig:three-sentence-discourse} for the three-sentence DisCoPy tensor layout (role reversal; anaphora is developed in prose and in the `Discourse` API below, not as a separate pronoun box in the DisCoPy figure).](output/figures/discopy_discocirc_discourse.png){#fig:discourse}

![Wire colour provides independent visual confirmation of the ACC$\to$NOM role transition that \autoref{fig:discourse} encodes algebraically. Native matplotlib DisCoCirc diagram for the same two-sentence discourse, generated via `src.visualization.string_diagrams.render_discocirc_discourse()` without the DisCoPy library. **Vertical grey wires**: persistent entity wires for Alice and Bob, confirming that identity is tracked across the sentence boundary. **Colour-coded role discs**: Bob's wire is marked **red** (ACC) at sentence 1 (chased object) and **blue** (NOM) at sentence 2 (running agent). The ACC$\to$NOM colour change is directly readable from the diagram without algebraic computation — Shimojima's free-ride inference in action. This independent rendering cross-validates that `src.diagrams.string_diagram.Discourse` correctly resolves entity identity and role reassignment using only case-role metadata.](output/figures/discourse_string_diagram.png){#fig:native-discourse}

## Alice's Role Trajectory: NOM→ACC→NOM Across Three Sentences

The power of DisCoCirc for case theory becomes particularly vivid in multi-sentence discourses where the *same entity occupies different case roles* across sentences. Consider the three-sentence discourse:

> *"Alice chases Bob. Bob fears Alice. She smiles."*

In this discourse, Alice undergoes a complete cycle of case role reversals:

1. **Sentence 1**: Alice is $\text{NOM}$ (Proto-Agent, the one chasing) and Bob is $\text{ACC}$ (Proto-Patient, the one chased).
2. **Sentence 2**: Bob is now $\text{NOM}$ (the one fearing) and Alice is $\text{ACC}$ (the one feared)—a role reversal where Alice moves from agent to patient.
3. **Sentence 3**: "She" resolves anaphorically to Alice, who returns to $\text{NOM}$ as the agent of smiling.

This NOM $\to$ ACC $\to$ NOM trajectory for Alice across three sentences is precisely the kind of *dynamic case assignment* that static single-sentence analyses cannot capture. The categorical representation as a triple tensor product $s \otimes s \otimes s$ (\autoref{fig:three-sentence-discourse}) encodes each sentence as an independent pregroup derivation while preserving the entity identity that links them. This role reversal essentially requires applying the topological `Swap` operation (introduced for passivization in \autoref{sec:case-type-logic}) dynamically across the discourse boundary. In a full DisCoCirc implementation, Alice's entity wire would carry accumulated semantic state—the meaning of "She" in sentence 3 inherits the enriched state of an Alice who has first chased and then been feared, not merely the bare lexical entry for "Alice."

The trajectory is *executable*: the `src.diagrams.string_diagram.Discourse` class implements exactly this entity-wire-with-role-history bookkeeping. The following snippet, taken verbatim from the public API exercised by the test suite, builds the three-sentence Alice/Bob discourse and reads back the role history that drives \autoref{fig:three-sentence-discourse}:

```python
from src.diagrams.string_diagram import Sentence, Discourse

discourse = Discourse()
discourse.add_sentence(Sentence.transitive("Alice", "chases", "Bob"))
discourse.add_sentence(Sentence.transitive("Bob", "fears", "Alice"))
discourse.add_sentence(Sentence.intransitive("Alice", "smiles"))

# Persistent entity wires (DisCoCirc state-wire reading)
assert discourse.entities == {"Alice", "Bob"}
assert discourse.num_sentences == 3

# Role history per entity reproduces the NOM → ACC → NOM trajectory
assert [r.name for r in discourse.role_history["Alice"]] == ["NOM", "ACC", "NOM"]
assert [r.name for r in discourse.role_history["Bob"]]   == ["ACC", "NOM"]

# `role_reversal_entities` flags every entity whose case role
# changes across the discourse — the formal analogue of the
# trajectory pictured in \autoref{fig:three-sentence-discourse}.
assert set(discourse.role_reversal_entities()) == {"Alice", "Bob"}
```

Slavic discourse supplies a *morphologically overt* analogue of the persistent state wire: in Serbian/BCS, second-position clitics (Wackernagel position) such as *je* AUX.3SG, *mu* DAT.3SG.M, *ga* ACC.3SG.M form a fixed-order cluster that *carries the case role of the discourse referent forward in time*. *Marko ga je video* "Marko him.ACC AUX saw" and *Dao mu ga je* "He gave him.DAT it.ACC AUX" make Bob's wire-and-case-history visible in the surface string in a way that English pronouns (which collapse case morphology onto a tiny three-form `I/me/my` paradigm) cannot. Russian, which lacks the BCS clitic cluster, instead encodes the same persistence directly in the suffix on the noun or full pronoun (*ego* ACC, *emu* DAT, *im* INS), so role reversals like Alice's NOM$\to$ACC$\to$NOM trajectory in *Alisa gonyaet Boba. Bob boitsja Alisy. Ona ulybaetsja* are reconstructible *from the morphology alone*, with no positional ambiguity. These are the cleanest natural-language witnesses for the entity-wire-with-role-history bookkeeping that the `Discourse` API formalises.

The point of including the snippet in prose is reproducibility, not novelty: every assertion above is exercised in `tests/test_diagrams_string_diagram.py`, so a reader who clones the repository can re-derive the discourse-level role trajectories with no additional setup beyond `uv sync`. The same `Discourse` object is what `src.visualization.string_diagrams.render_discocirc_discourse()` consumes to produce \autoref{fig:native-discourse} — closing the loop between symbolic case assignment, computational state-wire bookkeeping, and the colour-coded role transitions visible in the diagram.

![Dynamic case role reversal tracks entity identity across three-sentence discourse. DisCoPy rendering with lexical heads matching the discourse above: "Alice chases Bob. Bob fears Alice. Alice smiles." (sentence 3 uses the subject node \emph{Alice}---same referent as anaphoric \emph{She} in the running text; DisCoPy boxes are lexical, not pronominal). **Sentence 1**: Alice NOM, Bob ACC. **Sentence 2**: Bob NOM, Alice ACC---a complete agent--patient reversal. **Sentence 3**: Alice NOM as agent of \emph{smiles}. Alice's trajectory NOM$\to$ACC$\to$NOM is tracked by the triple tensor $s \otimes s \otimes s$. In a full DisCoCirc implementation, Alice's entity wire carries accumulated semantic state---"She" in the gloss inherits the enriched state of an Alice who has both chased and been feared. This dynamic case assignment across discourse boundaries is what lambeq Gen II [@lambeq2025genii] compiles into parameterized quantum circuits.](output/figures/discopy_three_sentence_discourse.png){#fig:three-sentence-discourse}

The DisCoPy rendering encodes entity persistence *algebraically* (each sentence contributes a tensor factor $s_i$ and the entity wires are shared by construction), but the reader must infer the shared-entity structure from context. \autoref{fig:discocirc-persistence} makes the structure *visual*: each entity is given its own colour (Alice indigo, Bob amber), the three sentence panels sit side-by-side with cups coloured by the entity each one contracts, and the bottom *role-history ribbon* explicitly plots Alice's NOM $\to$ ACC $\to$ NOM trajectory and Bob's ACC $\to$ NOM trajectory with the case-role palette used throughout the paper. It is the same object as \autoref{fig:three-sentence-discourse} — re-presented with the Frobenius-spider entity-identity bookkeeping that DisCoCirc posits, made graphically explicit.

![DisCoCirc entity-persistence unpacking for *Alice chases Bob. Bob fears Alice. Alice smiles.* Three sentence panels (top) plus a role-history ribbon (bottom). Each entity has a dedicated colour (Alice indigo, Bob amber) and the cup contractions are coloured by the entity each one consumes. The ribbon shows Alice traversing NOM→ACC→NOM and Bob traversing ACC→NOM (with an "absent" marker for sentence 3), exhibiting graphically the Frobenius-spider entity persistence that motivates DisCoCirc. Generated programmatically from `src.visualization.category_unpacking.render_discocirc_entity_persistence()`.](output/figures/discocirc_entity_persistence.png){#fig:discocirc-persistence}

## lambeq Gen II Compiles DisCoCirc Discourse Diagrams

The categorical structure of DisCoCat maps naturally onto quantum circuits: the tensor product structure of $\mathbf{FVect}$ is identical to the tensor product structure of $\mathbf{Qubit}$, the category of qubit systems. This observation underlies the **QNLP** (Quantum Natural Language Processing) program [@meichanetzidis2020qnlp], which implements DisCoCat models as parameterized quantum circuits.

The **lambeq** library [@lorenz2021lambeq] provides a practical pipeline:

1. Parse a sentence into a pregroup derivation (via the neural CCG parser Bobcat or rule-based parsers)
2. Convert the derivation into a string diagram
3. Translate the diagram into a parameterized quantum circuit (or a classical tensor network)
4. Train the parameters on NLP tasks (classification, similarity, question answering)

Kartsaklis et al. [-@kartsaklis2021functorial] demonstrate that this pipeline achieves competitive performance on question-answering tasks, confirming that the categorical structure captures genuine linguistic regularities even when instantiated on noisy near-term quantum hardware.

**lambeq Gen II** (released May 21, 2025 by Quantinuum) marks a significant advance by incorporating full **DisCoCirc** support as its core mathematical foundation, enabling the framework to scale beyond single-sentence semantics to discourse-level NLP [@lambeq2025genii; @quantinuum2025genii]. With over 50,000 downloads, lambeq Gen II achieves language neutrality, improved trainability, and compositional interpretability for explainable AI on quantum hardware. The new `DisCoCircReader` API automatically compiles long texts and multi-page documents into discourse-level quantum circuits, with entity wires tracking semantic state persistence across sentence boundaries—closing the gap between sentence-level DisCoCat and discourse-level case role tracking. This is directly relevant to the case role reversal phenomena discussed in \autoref{fig:three-sentence-discourse}: lambeq Gen II can, in principle, compile such multi-sentence case-dynamic discourses into trainable quantum circuits.

Foundational work by Meyer and Lewis integrates DisCoCat with density matrices for modeling dynamic meaning and lexical ambiguity in text, treating semantic states as mixed quantum states—providing an alternative to pure-state vector models that naturally accommodates ambiguity and partial information [-@meyer2020modelling].

Recent work on **string diagram rewriting** by Bonchi et al. [-@bonchi2022rewriting] provides the theoretical foundation for diagram simplification, showing that string diagram rewrite systems modulo Frobenius structure can be interpreted as double-pushout hypergraph rewriting—ensuring that the algebraic simplifications applied during normal form computation are provably sound. De Huybrecht [-@dehuybrecht2024subcategorizing] extends DisCoCat with *subcategorization* for light verb constructions, demonstrating that the categorical framework accommodates sublexical compositional structure—a development that connects naturally to the monadic root syntax of Song [-@song2022act] discussed in \autoref{sec:categorial-grammar}.

For our case-theoretic framework, QNLP offers a concrete computational substrate: case categories could be implemented as quantum circuits where case roles correspond to quantum registers and grammatical relations correspond to parameterized gates. This connection between linguistic case structure and quantum information processing—mediated entirely by the shared categorical formalism—illustrates the power of the diagrammatic approach.

## No Barren Plateau for Local Observables

A central challenge for practical QNLP on near-term quantum hardware is the *trainability* of parameterized quantum circuits (PQCs): the vanishing gradient problem, or *barren plateau*, makes gradient-based optimization exponentially hard as circuit width and depth scale. Two recent results (2024) directly resolve this obstacle for linguistically motivated circuits:

1. **Rad et al. [-@rad2024trainability]** introduce *reduced-domain parameter initialization*: rather than sampling all parameters uniformly from $[0, 2\pi)$, one initializes the circuit in a small-angle domain close to the identity. For circuits of the depth typical of DisCoCirc discourse diagrams (compiled from multi-sentence texts via coreference resolution), this initialization provably yields polynomial rather than exponential gradient decay—keeping optimization tractable as discourse length grows.

2. **Letcher et al. [-@letcher2024tight]** derive tight, *assumption-free* lower bounds on the variance of cost function gradients for PQCs with local observables (e.g., Pauli operators restricted to a few-qubit subsystem). Their key finding is that, for POVMs restricted to local observables—exactly the structure of the case-role measurement operators $E_c$ of \autoref{eq:eq-8-1} (formalized in \autoref{sec:quantum-semantics})—no barren plateau effect occurs. This provides a theoretical guarantee that case-role classification circuits implemented via lambeq remain optimizable regardless of total circuit size, so long as the readout observable is local.

Together, these results underpin the practical feasibility of the F1 and F3 research directions of \autoref{sec:conclusion}: scaling case-marked DisCoCat/DisCoCirc models to corpora-scale quantum hardware without exponential gradient overhead. The geometric structure of lambeq's IQP and Sim4 ansätze, combined with these initialization and observable choices, provides a principled recipe for quantum case category training on near-term devices.

```{=latex}
\newpage
```
