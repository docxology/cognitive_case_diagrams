# Conclusion: Eleven Formal and Computational Contributions {#sec:conclusion}

## What This Paper Actually Did: Eleven Concrete Deliverables

This paper developed a unified category-theoretic framework for linguistic case systems, synthesizing five research traditions—typological, type-logical, distributional, enriched-categorical, and topos-theoretic—and embedding the result within an active inference model of cognition. Our eleven principal contributions are:

> **Notation**: Each entry is labelled **C**_n_ (*n*th contribution, **C1**–**C11**) or **F**_n_ (*n*th future direction, **F1**–**F7**).

### C1: Case Categories as a Formal Algebraic Framework

The review formalized case systems as categories with case roles as objects and grammatical relations as morphisms (\autoref{sec:case-systems}). This formalization captures the full typological range of alignment systems---nominative-accusative, ergative-absolutive, active-stative, tripartite, and fluid-S---within a single algebraic framework, with alignment functors providing structure-preserving mappings between systems. By tracing the lineage from Fillmore's [-@fillmore1968case] deep cases through Jakobson's binary distinctive features and Dowty's [-@dowty1991thematic] proto-roles, the analysis demonstrated how enriched (weighted) morphisms link the categorical formalization to the gradient nature of thematic role assignment.

### C2: String Diagrams for Case Derivation Visualization

Building on Joyal and Street's [-@joyalstreet1991geometry] string diagram formalism and its application in categorial grammar (\autoref{sec:categorial-grammar}), we showed how case-marked noun phrases receive type-logical assignments that are fully visualizable as string diagrams. The Curry–Howard correspondence ensures that syntactic well-formedness guarantees semantic compositionality, and the diagrammatic format provides Shimojima's [-@shimojima1996reasoning] "free ride" inferences—conclusions about argument structure that are perceptually available from the diagram without explicit computation. We further demonstrated that passivization reduces to a _type permutation_ (a Swap operation in the pregroup category), making voice alternation visible as a topological feature of the string diagram.

### C3: Case-Marked DisCoCat, the Distributional–Formal Synthesis, and Discourse Extension

We extended the DisCoCat framework (\autoref{sec:categorical-semantics}) with case-typed noun spaces and alignment-sensitive meaning functors, and showed how the recent DisCoCirc [@defelice2022discocirc] and QNLP [@lorenz2023lambeq] developments extend this analysis to discourse-level structure and quantum hardware respectively. We formalized the _compact closure axiom_ (snake equation) that underpins pregroup reductions, demonstrating that the cup-cap zigzag identity provides a visual coherence proof with genuine cognitive significance. Diagram complexity metrics—normal form and depth—provide a quantitative bridge between the type-logical and distributional perspectives on linguistic structure. A key contribution is the demonstration that DisCoCat constitutes the _algebraic formalization_ of the distributional programme that modern large language models—from Word2Vec [@mikolov2013efficient] through BERT [@devlin2019bert] and GPT [@radford2018improving]—implement empirically: the categorical meaning functor is the principled version of the composition that transformer attention mechanisms learn from data [@vaswani2017attention]. Case categories can serve as the structural backbone of compositional models of meaning at all levels—word, sentence, discourse, and dialogue.

### C4: Enriched Cases, Categorical Magnitude, and Information Theory

Through Bradley et al.'s [-@fritz2021enriched] enrichment framework and Bradley's [-@bradley2021entropy] information-theoretic analysis (\autoref{sec:enriched-categories}), we showed that equipping case categories with $[0,1]$-valued hom-objects yields a principled bridge between symbolic case grammar and statistical semantics. Categorical magnitude provides a quantitative ``effective size'' invariant for comparing case systems; magnitude homology [-@leinster2021magnitude] refines that comparison when scalar magnitude does not separate two systems.

### C5: Topos-Theoretic Transfer via Morita Equivalence

Using Caramello's [-@caramello2016bridges; -@caramello2021five] bridge technique and Phillips's [-@phillips2024lot] universality result (\autoref{sec:topos-theory}), we articulate how **topos-theoretic invariants** of a classifying topos can scaffold inter-theoretic transfer: when two formalizations admit Morita-equivalent classifying toposes (or an explicit bridge topos, as sketched in \autoref{sec:topos-theory}), properties expressible as shared invariants transfer without separate proof in each framework. The schematic equivalence chain for typological, type-logical, distributional, and enriched case theories is a **research program**—not a single finished theorem covering all of linguistics—but it aligns the four perspectives with Caramello's methodology.

### C6: Diagrams as Cognitively Privileged Representations

The meta-contribution (Sections 1 and 7) is the argument---supported by the cognitive science of diagrams [@larkin1987diagram; @shimojima1996reasoning; @giardino2017diagrammatic; @manders2008euclidean]---that commutative diagrams are not merely convenient notation but cognitively privileged representations that provide inferential advantages in case reasoning. When embedded in an active inference framework [@friston2017active] and the CEREBRUM architecture [@friedman2024cerebrum], these diagrams serve as the structural core of generative models for total cognitive scenario understanding.

### C7: Computational Verification and Test Suite

The entire framework is computationally implemented and verified through **804 automated tests across 47 test files with ≥90% code coverage target** (\autoref{sec:diagrammatic-cognition}; DAIF implementation and metrics in \autoref{sec:daif-results}), enforced in the build configuration. The DisCoPy integration exercises pregroup type theory (types, words, cups, caps, swaps, normal forms, depth analysis) against the same algebraic structures described theoretically, confirming that the categorical abstractions are not just mathematically elegant but computationally executable. The `src/daif/` subpackage (7 modules, 24 symbols, 161 dedicated tests) provides the full distributional RL implementation: push-forward returns, quantile TD, variational message passing, Bethe free energy, ERP profile generation, policy selection, and convergence diagnostics. Every test uses real mathematical computations—no mocks or fakes—ensuring that results reflect genuine behaviour of the formal structures.

### C8: Quantum Active Inference and Topological Semantic Flow

The framework's categorical string diagrams were extended into their natural quantum generalization through topological quantum neural networks, the ZX-calculus, and sheaf-theoretic quantum semantic communication (\autoref{sec:quantum-active-inference}). By demonstrating that DisCoCat derivations, ZX circuits, and TQNN spin-networks are all morphisms in compact closed monoidal categories with functorial semantics into Hilbert spaces, the analysis established that case assignment can be modeled as quantum measurement on a holographic screen—and that quantum features (entanglement, contextuality, discord) provide genuine advantages for semantic communication of relational structure.

### C9: Cognitive Security and Case-Theoretic AI Safety

The framework yielded a novel analysis of AI security through the lens of case theory (\autoref{sec:cognitive-security}; compositional protocol typing in \autoref{sec:ai-implications}). We demonstrated that prompt injection attacks—the predominant vulnerability in LLM-based agent systems—are structurally equivalent to _illicit case-role re-assignments_: adversarial text promotes itself from ACC (passive data) to NOM (active commander), constituting a type violation in the interaction grammar. This analysis led to the proposal of _case-theoretic firewalls_ that enforce relational type constraints on agent communication boundaries, and _epistemic case security_ as a framework for protecting multi-agent relational reasoning against belief injection, precision poisoning, and cascade corruption when results are transferred across Morita-equivalent formalizations. The compositional structure of the categorical framework enables local verification—each morphism can be independently authenticated—providing defense-in-depth that content-based filtering cannot achieve.

### C10: Falsifiable Neurolinguistic Predictions

The integration of enriched category theory with active inference generates quantitative, testable predictions about neural processing of case structure (\autoref{sec:cognitive-integration}). Specifically, the amplitude of prediction-error ERP components (P600, N400) is predicted to scale with the enriched hom-value (precision) of the violated morphism, and garden-path reanalysis costs are predicted to correlate with the change in categorical magnitude between the initial and revised case diagrams. These hypotheses **extend** computational accounts that decompose surprisal into components linked to N400- vs P600-like signatures [@li2023decomposition; @li2024shallow], by tying amplitudes to enriched morphism weights and magnitude change in an explicit case-diagram prior. They bridge abstract categorical formalism and empirical neurolinguistics, making the framework falsifiable at the single-trial level.

### C11: Categorical Communication Protocols for Multi-Agent AI

The synthesis of case categories with modern agent communication standards (A2A, MCP, ACP, ANP) yields a principled design for compositional, type-safe agent protocols (\autoref{sec:ai-implications}). By assigning case roles (NOM, ACC, INS, LOC, DAT) to interaction participants and enforcing relational type constraints at protocol boundaries, the framework provides interpretable, composable interaction schemas that go beyond the flat JSON payloads of current standards, with topos-level invariants transferable across Morita-equivalent formalizations when equivalence is exhibited (\autoref{sec:topos-theory}). The DisCoCirc extension enables discourse-level tracking of agent states across multi-turn dialogues, with protocol correctness reducing to categorical type-checking.

## Seven Open Directions

The following seven directions (**F1**–**F7**) identify the most tractable and impactful extensions of this framework:

### F1: Computational Experiments with DisCoCirc and lambeq

The DisCoCirc framework [@defelice2022discocirc] offers a natural platform for testing our case-theoretic predictions computationally. The release of **lambeq Gen II** [@lambeq2025genii] with full DisCoCirc support makes this direction immediately tractable: discourse-level case role tracking—including the dynamic role reversals of \autoref{fig:three-sentence-discourse}—can now be compiled into parameterized quantum circuits (PQCs) and trained end-to-end. Krawchuk et al. [@krawchuk2025paramqnlp] demonstrate efficient generation of PQCs from large-scale texts (up to 6,410 words) with competitive performance on sentiment classification; [@letcher2024tight] and [@rad2024trainability] provide gradient bounds and reduced-domain initialization techniques that mitigate barren plateaus, making discourse-level circuit training practically feasible. Concrete experiments could include:

- Implementing case-marked DisCoCat models in **lambeq Gen II** and evaluating them on semantic role labeling (SRL) tasks, leveraging the discourse-level wiring to track case roles across sentence boundaries
- Comparing the accuracy of alignment-specific meaning functors (accusative vs. ergative) on typologically diverse corpora
- Measuring the categorical magnitude of empirically derived enriched case categories and correlating it with typological complexity measures
- Using the `complexity_metrics` module to quantify derivational complexity across sentence types and correlating syntactic complexity scores with human processing difficulty (reading times, surprisal)
- Training lambeq Gen II circuits on case role reversal discourses using reduced-domain parameter initialization [@rad2024trainability] to avoid local minima

### F2: Topos-Theoretic Grammatical Induction from Corpora

Caramello's [-@caramello2023syntactic] syntactic learning technique could be applied to induce case-theoretic axioms from annotated corpora. The program would:

1. Extract case-labeled dependency structures from a Universal Dependencies treebank
2. Construct the classifying topos of the implicit case theory
3. Read off the alignment type, morphism structure, and enriched weights from the topos-theoretic axioms
4. Compare the induced theory against typological descriptions

### F3: Quantum Case Categories on Near-Term Hardware

The QNLP connection (\autoref{sec:categorical-semantics}) opens the possibility of implementing case categories directly as quantum circuits. Case roles would correspond to quantum registers, grammatical relations to parameterized gates, and alignment functors to circuit transformations. This would provide a genuinely new computational paradigm for grammatical inference—exploiting quantum parallelism to explore the space of case assignments simultaneously. Two recent results make this direction practically tractable: (1) Rad et al.'s [-@rad2024trainability] reduced-domain parameter initialization yields polynomial gradient decay, suppressing the barren plateau problem for circuits of linguistic depth; and (2) Letcher et al.'s [-@letcher2024tight] assumption-free gradient bounds rule out vanishing gradients for circuits with local observables, which includes the case-role measurement POVMs of \autoref{eq:eq-8-1}. Together these results suggest that near-term quantum hardware can support case category training without exponential gradient overhead.

### F4: Neural Predictive Processing and Electrophysiological Predictions

The predictive processing account of \autoref{sec:cognitive-integration} generates testable neuroscientific predictions:

- Case-marking violations should elicit prediction-error responses (P600/N400) proportional to the enriched weight of the violated morphism
- Typologically unusual case patterns should require more precision updating than expected patterns
- Diagrammatic representations of case structure should be decodable from neural activity during sentence comprehension

### F5: Cross-Modal Case Structure in Embodied Cognition

The situation semantics connection (\autoref{sec:cognitive-integration}) suggests extending case categories beyond language to multi-modal perception. Visual scene understanding also requires assigning relational roles—who is acting on what, where things are located, what instruments are being used. An active inference agent should maintain a unified case diagram that integrates linguistic, visual, and motor information, using the same categorical structure for all modalities. This would provide a formal account of how language grounds in perception and action—a key challenge for embodied AI.

### F6: Enriched Category Learning from Distributional Data

Bradley's [-@bradley2024ipam; -@bradley2025tea] program of treating language itself as an enriched category suggests a learning algorithm: estimate the enriched hom-values from corpus data and then extract the categorical structure that best explains the observed distributional patterns. Applied to case, this would yield _empirically grounded_ case categories whose objects (roles) and morphisms (relations) emerge from data rather than being stipulated a priori.

### F7: Extending Distributional Active Inference for Linguistic Agents

The Distributional Active Inference (DAIF) framework of Akgül et al. [-@akgul2026distributional] has been computationally implemented in this paper's `src/daif/` subpackage, integrating active inference into distributional reinforcement learning [@bellemare2017distributional] via push-forward measures on representation paths (\autoref{sec:daif-results}). The current implementation models case assignment distributionally: agents maintain _distributions over case diagrams_, sharpening beliefs through variational message passing as linguistic evidence accumulates. Key open extensions include:

- Training distributional case-assignment circuits end-to-end in **lambeq Gen II** using quantile regression losses, enabling gradient-based learning of the enriched weight matrix from annotated corpora
- Extending the DAIF policy selection (`G_policy`, `softmax_policy_selection`) to multi-turn dialogue management with DisCoCirc entity persistence—tracking agent state distributions across sentence boundaries
- Cross-lingual transfer of Bethe free energy convergence profiles: testing whether the free energy minima differ systematically between nominative-accusative and ergative-absolutive languages, operationalizing the typological complexity predictions of \autoref{sec:enriched-categories}
- Integrating IQN risk distortion modes (optimistic/pessimistic/CVaR) into the CEREBRUM architecture to model individual differences in syntactic risk tolerance

## Case Categories Are the Geometry of Meaning: A Unifying Coda

The commutative diagram is the central motif of this review---both as a mathematical tool and as a cognitive instrument. The analysis has demonstrated that the same diagrammatic language that makes category theory effective for formalizing case systems also makes it effective for _thinking about_ case systems: the spatial structure of a commutative diagram encodes relational information in a format that supports rapid search, pattern recognition, and free-ride inference.

This convergence of mathematical utility and cognitive efficacy is not accidental. If the active inference framework is correct, then the brain operates by constructing and updating generative models of the world's relational structure. Category theory provides the structural algebra for these generative models; commutative diagrams supply their natural topology; and case categories instantiate the precise relational vocabulary that cognitive systems deploy to organize experience into coherent narratives of _who does what to whom_. The distributional revolution in both semantics and reinforcement learning—from Firth's [-@firth1957papers] co-occurrence statistics through transformer attention weights to Distributional Active Inference [@akgul2026distributional]—confirms that meaning is not an atomic property of symbols but emerges from the relational structure of contexts, a principle that enriched category theory captures with mathematical precision.

Ultimately, the mathematics of case alignment presents a highly structured formal geometry of meaning—the relational algebra through which cognitive agents navigate and render intelligible the structured world of events, participants, and relations. The convergence of formal semantics, distributional semantics, and active inference within a single categorical framework suggests that commutative diagrams offer a natural formalism in which relational cognition can be modeled.
