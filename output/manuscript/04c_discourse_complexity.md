# Beyond the Sentence: State Wires Accumulate Semantic History Across Discourse {#sec:discocirc-discourse}

## DisCoCirc State Wires Resolve Coreference and Role Shifts

De Felice and Coecke [-@defelice2020discourse] address this limitation by formulating **DisCoCirc** (Distributional Compositional Circuits). DisCoCirc extends the base categorical framework, empowering it to dynamically handle discourse-level semantic structure.

Specifically, DisCoCirc introduces continuous *state wires* that actively persist across isolated sentence boundaries, continuously encoding the dynamically evolving states of distinct discourse entities (e.g., characters, objects, shifting topics). For example, a multi-sentence sequence like "Alice chased Bob. He was terrified." is explicitly represented as an integrated geometric circuit where:

- Alice and Bob are wires that persist across both sentences.
- The pronoun "He" is resolved by actively connecting its topological wire directly to Bob's wire.
- The shifting emotional state "terrified" seamlessly updates the cumulative state information carried exclusively by Bob's persistent wire.

De Felice et al. [-@defelice2022discocirc] subsequently extended this approach, developing a full-fledged, multi-layered circuit model built to systematically resolve ambiguity, tangled coreference, and overarching discourse coherence—all locked within the exact same continuous categorical formalism. A CCG-based pipeline for generating discourse circuits from syntactic parse trees has demonstrated that DisCoCirc can scale to text, dynamically composing sentence-level diagrams along shared entity wires via an iterative process of coreference resolution and wire merging [-@duneau2021parsing]. Complementary work on **DiscoSG** (Discourse Scene Graphs) extends this approach to multi-sentence image captions, parsing text into scene graphs that capture cross-sentence coreference relations. \\autoref{fig:discourse} illustrates a multi-sentence discourse diagram where entity wires persist across sentence boundaries. For case theory, DisCoCirc is significant because it shows how case-marked argument structure *composes across discourse*: the nominative subject of one sentence can become the accusative object of the next, and this transformation is tracked as a morphism in the discourse category.

![Entity persistence across sentence boundaries enables case role tracking. A DisCoCirc-style discourse diagram for "Alice chases Bob. Bob runs." generated via DisCoPy's pregroup grammar. **Sentence 1**: three Word boxes contract Alice ($n$) and Bob ($n$) into the transitive verb "chases" ($n^r \otimes s \otimes n^l$), producing sentence type $s$. **Sentence 2**: Bob ($n$) contracts into the intransitive "runs" ($n^r \otimes s$), producing a second $s$. The full discourse type is $s \otimes s$, encoding inter-sentential coherence. In a full DisCoCirc implementation, Bob's shared entity wire would carry accumulated semantic state across the sentence boundary---the foundation for dynamic case role tracking in \autoref{fig:three-sentence-discourse}.](output/figures/discopy_discocirc_discourse.png){#fig:discourse}

![Wire colour directly encodes dynamic case-role transitions across sentence boundaries. Native matplotlib DisCoCirc diagram for "Alice chases Bob. Bob runs." generated via `src.visualization.string_diagrams.render_discocirc_discourse()`, cross-validating \autoref{fig:discourse} without library dependency. **Vertical wires** (grey) are persistent entity wires for Alice and Bob. At each sentence boundary, a coloured disc marks Bob's case role: **red** (ACC) in sentence 1 (chased object), **blue** (NOM) in sentence 2 (running agent). The ACC $\to$ NOM transition is read directly from wire colour at successive levels. This confirms that our native string-diagram module correctly resolves entity identity and tracks role reassignment using `src.diagrams.string_diagram.Discourse` data structures.](output/figures/discourse_string_diagram.png){#fig:native-discourse}

## Alice's Trajectory NOM→ACC→NOM

The power of DisCoCirc for case theory becomes particularly vivid in multi-sentence discourses where the *same entity occupies different case roles* across sentences. Consider the three-sentence discourse:

> *"Alice chases Bob. Bob fears Alice. She smiles."*

In this discourse, Alice undergoes a complete cycle of case role reversals:

1. **Sentence 1**: Alice is $\text{NOM}$ (Proto-Agent, the one chasing) and Bob is $\text{ACC}$ (Proto-Patient, the one chased).
2. **Sentence 2**: Bob is now $\text{NOM}$ (the one fearing) and Alice is $\text{ACC}$ (the one feared)—a role reversal where Alice moves from agent to patient.
3. **Sentence 3**: "She" resolves anaphorically to Alice, who returns to $\text{NOM}$ as the agent of smiling.

This NOM $\to$ ACC $\to$ NOM trajectory for Alice across three sentences is precisely the kind of *dynamic case assignment* that static single-sentence analyses cannot capture. The categorical representation as a triple tensor product $s \otimes s \otimes s$ (\autoref{fig:three-sentence-discourse}) encodes each sentence as an independent pregroup derivation while preserving the entity identity that links them. This role reversal essentially requires applying the topological `Swap` operation (introduced for passivization in \autoref{sec:case-type-logic}) dynamically across the discourse boundary. In a full DisCoCirc implementation, Alice's entity wire would carry accumulated semantic state—the meaning of "She" in sentence 3 inherits the enriched state of an Alice who has first chased and then been feared, not merely the bare lexical entry for "Alice."

![Dynamic case role reversal tracks entity identity across three-sentence discourse. DisCoPy rendering of "Alice chases Bob. Bob fears Alice. She smiles." **Sentence 1**: Alice NOM, Bob ACC. **Sentence 2**: Bob NOM, Alice ACC---a complete agent--patient reversal. **Sentence 3**: anaphoric "She" resolves to Alice, who returns to NOM. Alice's trajectory NOM$\to$ACC$\to$NOM is tracked by the triple tensor $s \otimes s \otimes s$. In a full DisCoCirc implementation, Alice's entity wire carries accumulated semantic state---"She" in sentence 3 inherits the enriched state of an Alice who has both chased and been feared. This dynamic case assignment across discourse boundaries is what lambeq Gen II [@lambeq2025genii] compiles into parameterized quantum circuits.](output/figures/discopy_three_sentence_discourse.png){#fig:three-sentence-discourse}

## lambeq Gen II Compiles DisCoCirc Discourse Diagrams

The categorical structure of DisCoCat maps naturally onto quantum circuits: the tensor product structure of $\mathbf{FVect}$ is identical to the tensor product structure of $\mathbf{Qubit}$, the category of qubit systems. This observation underlies the **QNLP** (Quantum Natural Language Processing) program [@meichanetzidis2020qnlp], which implements DisCoCat models as parameterized quantum circuits.

The **lambeq** library [@lorenz2023lambeq] provides a practical pipeline:

1. Parse a sentence into a pregroup derivation (via the neural CCG parser Bobcat or rule-based parsers)
2. Convert the derivation into a string diagram
3. Translate the diagram into a parameterized quantum circuit (or a classical tensor network)
4. Train the parameters on NLP tasks (classification, similarity, question answering)

Kartsaklis et al. [-@kartsaklis2021functorial] demonstrate that this pipeline achieves competitive performance on question-answering tasks, confirming that the categorical structure captures genuine linguistic regularities even when instantiated on noisy near-term quantum hardware.

**lambeq Gen II** (released May 22, 2025 by Quantinuum) marks a significant advance by incorporating full **DisCoCirc** support as its core mathematical foundation, enabling the framework to scale beyond single-sentence semantics to discourse-level NLP [@lambeq2025genii; @quantinuum2025genii]. With over 50,000 downloads, lambeq Gen II achieves language neutrality, improved trainability, and compositional interpretability for explainable AI on quantum hardware. The new `DisCoCircReader` API automatically compiles long texts and multi-page documents into discourse-level quantum circuits, with entity wires tracking semantic state persistence across sentence boundaries—closing the gap between sentence-level DisCoCat and discourse-level case role tracking. This is directly relevant to the case role reversal phenomena discussed in \autoref{fig:three-sentence-discourse}: lambeq Gen II can, in principle, compile such multi-sentence case-dynamic discourses into trainable quantum circuits.

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
