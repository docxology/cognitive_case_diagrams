# Conclusion: Elevating Language Models from Vectors to Enriched Category Frameworks {#sec:conclusion}

## What This Paper Actually Did: Eleven Concrete Deliverables

This paper developed a unified category-theoretic framework for linguistic case systems, synthesizing **five formal traditions**—typological, type-logical, distributional, enriched-categorical, and topos-theoretic—together with a **sixth strand**, the biolinguistic and neurocomputational interface (ROSE and related oscillatory accounts; \autoref{sec:introduction}, \autoref{sec:cognitive-integration}), and embedding the whole within an active inference model of cognition. Our eleven principal contributions are:

> **Notation**: Each entry is labelled **C**_n_ (*n*th contribution, **C1**–**C11**) or **F**_n_ (*n*th future direction, **F1**–**F8**).

### C1: Case Categories as a Formal Algebraic Framework

The review formalized case systems as categories with case roles as objects and grammatical relations as morphisms (\autoref{sec:case-systems}). This formalization captures the full typological range of alignment systems---nominative-accusative, ergative-absolutive, active-stative, tripartite, and fluid-S---within a single algebraic framework, with alignment functors providing structure-preserving mappings between systems. By tracing the lineage from Fillmore's [-@fillmore1968case] deep cases through Jakobson's binary distinctive features and Dowty's [-@dowty1991thematic] proto-roles, the analysis demonstrated how enriched (weighted) morphisms link the categorical formalization to the gradient nature of thematic role assignment.

### C2: String Diagrams for Case Derivation Visualization

Building on Joyal and Street's [-@joyalstreet1991geometry] string diagram formalism and its application in categorial grammar (\autoref{sec:categorial-grammar}), we showed how case-marked noun phrases receive type-logical assignments that are fully visualizable as string diagrams. The Curry–Howard correspondence ensures that syntactic well-formedness guarantees semantic compositionality, and the diagrammatic format provides Shimojima's [-@shimojima1996reasoning] "free ride" inferences—conclusions about argument structure that are perceptually available from the diagram without explicit computation. We further demonstrated that passivization reduces to a _type permutation_ (a Swap operation in the pregroup category), making voice alternation visible as a topological feature of the string diagram.

### C3: Case-Marked DisCoCat, the Distributional–Formal Synthesis, and Discourse Extension

We extended the DisCoCat framework (\autoref{sec:categorical-semantics}) with case-typed noun spaces and alignment-sensitive meaning functors, and showed how the recent DisCoCirc [@defelice2022discocirc] and QNLP [@lorenz2021lambeq] developments extend this analysis to discourse-level structure and quantum hardware respectively. We formalized the _compact closure axiom_ (snake equation) that underpins pregroup reductions, demonstrating that the cup-cap zigzag identity provides a visual coherence proof with genuine cognitive significance. Diagram complexity metrics—normal form and depth—provide a quantitative bridge between the type-logical and distributional perspectives on linguistic structure. A key contribution is the demonstration that DisCoCat constitutes the _algebraic formalization_ of the distributional programme that modern large language models—from Word2Vec [@mikolov2013efficient] through BERT [@devlin2019bert] and GPT [@radford2018improving]—implement empirically: the categorical meaning functor is the principled version of the composition that transformer attention mechanisms learn from data [@vaswani2017attention]. Case categories can serve as the structural backbone of compositional models of meaning at all levels—word, sentence, discourse, and dialogue.

### C4: Enriched Cases, Categorical Magnitude, and Information Theory

Through Bradley et al.'s [-@fritz2021enriched] enrichment framework and Bradley's [-@bradley2021entropy] information-theoretic analysis (\autoref{sec:enriched-categories}, \autoref{sec:magnitude-homology}), we showed that equipping case categories with $[0,1]$-valued hom-objects yields a principled bridge between symbolic case grammar and statistical semantics. Categorical magnitude (\autoref{sec:magnitude-homology}) provides a quantitative ``effective size'' invariant for comparing case systems; magnitude homology [-@leinster2021magnitude] refines that comparison when scalar magnitude does not separate two systems.

### C5: Topos-Theoretic Transfer via Morita Equivalence

Using Caramello's [-@caramello2016bridges; -@caramello2021five] bridge technique and Phillips's [-@phillips2024lot] universality result (\autoref{sec:topos-theory}), we articulate how **topos-theoretic invariants** of a classifying topos can scaffold inter-theoretic transfer: when two formalizations admit Morita-equivalent classifying toposes (or an explicit bridge topos, as sketched in \autoref{sec:topos-theory}), properties expressible as shared invariants transfer without separate proof in each framework. The schematic equivalence chain for typological, type-logical, distributional, and enriched case theories is a **research program**—not a single finished theorem covering all of linguistics—but it aligns the four perspectives with Caramello's methodology.

### C6: Diagrams as Cognitively Privileged Representations

The meta-contribution (Sections 1 and 7) is the argument---supported by the cognitive science of diagrams [@larkin1987diagram; @shimojima1996reasoning; @giardino2017diagrammatic; @manders2008euclidean]---that commutative diagrams are not merely convenient notation but cognitively privileged representations that provide inferential advantages in case reasoning. When embedded in an active inference framework [@namjoshi2026fundamentals] and the CEREBRUM architecture [@friedman2024cerebrum], these diagrams serve as the structural core of generative models for total cognitive scenario understanding.

### C7: Computational Verification and Test Suite (**implemented and tested**)

The framework is computationally implemented and verified through **1212** automated tests across **64** test files (sixty-four files). 95.79% line-and-branch coverage on ``src/`` (measured; see ``output/metrics.json`` and ``tests/AGENTS.md`` for provenance) A coverage floor of **≥90%** on ``src/`` is declared as ``fail_under = 90`` in ``pyproject.toml`` and enforced on any ``pytest --cov`` run (see \autoref{sec:diagrammatic-cognition}, DAIF in \autoref{sec:daif-results}, and `src/generate_manuscript_metrics.py` for injection of these values at build time; this repository ships no separate CI workflow, so the gate is the test-time coverage check itself). The `src/daif/` subpackage (7 modules, 25 symbols, 232 dedicated tests) provides distributional RL components (push-forward, quantile TD, VMP, Bethe FE, ERP profiles, policy selection, diagnostics). All tests use real mathematical computations—no mocks—ensuring results reflect genuine behaviour of the for…

### C8: Quantum Active Inference and Topological Semantic Flow (**theoretical bridge**)

The framework's categorical string diagrams connect to literature on topological quantum neural networks, the ZX-calculus, and sheaf-theoretic quantum semantic communication (\autoref{sec:quantum-active-inference}). The `src/quantum/` module implements a POVM measurement model for case roles (**implemented and tested**). The broader TQNN spin-networks, full ZX circuit compilation, and hardware claims represent a theoretical bridge rather than complete local execution in this repository.

### C9: Cognitive Security and Case-Theoretic AI Safety (**specification and proxy implementation**)

The framework provides a case-theoretic analysis of AI security (\autoref{sec:cognitive-security}; see also compositional protocol typing in \autoref{sec:ai-implications}). Prompt injection is analyzed as structurally equivalent to illicit case-role re-assignment (type violation in the interaction grammar; **implemented as type-checking proxy in `src/security/` and `src/diagrams/`**). This leads to the proposal of case-theoretic firewalls and epistemic case security as a framework. The `src/security/cognitive_security.py` implements finite-category validation and scoring (tested). Full production enforcement and non-cartesian monoidal constraints remain open engineering targets, as detailed in the limitations section of \autoref{sec:cognitive-security}.

### C10: Falsifiable Neurolinguistic Predictions

The integration of enriched category theory with active inference generates quantitative, testable predictions about neural processing of case structure (\autoref{sec:cognitive-integration}). Specifically, the amplitude of prediction-error ERP components (P600, N400) is predicted to scale with the enriched hom-value (precision) of the violated morphism, and garden-path reanalysis costs are predicted to correlate with the change in categorical magnitude between the initial and revised case diagrams. These hypotheses **extend** computational accounts that decompose surprisal into components linked to N400- vs P600-like signatures [@li2023decomposition; @li2024shallow], by tying amplitudes to enriched morphism weights and magnitude change in an explicit case-diagram prior. They bridge abstract categorical formalism and empirical neurolinguistics, making the framework falsifiable at the single-trial level.

### C11: Categorical Communication Protocols for Multi-Agent AI

The synthesis of case categories with modern agent communication standards (A2A, MCP, ACP, ANP) yields a principled design for compositional, type-safe agent protocols (\autoref{sec:ai-implications}). By assigning case roles (NOM, ACC, INS, LOC, DAT) to interaction participants and enforcing relational type constraints at protocol boundaries, the framework provides interpretable, composable interaction schemas that go beyond the flat JSON payloads of current standards, with topos-level invariants transferable across Morita-equivalent formalizations when equivalence is exhibited (\autoref{sec:topos-theory}). The DisCoCirc extension enables discourse-level tracking of agent states across multi-turn dialogues, with protocol correctness reducing to categorical type-checking.

## Eight Open Directions {#sec:future-directions}

The following eight directions (**F1**–**F8**) identify the most tractable and impactful extensions of this framework:

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

### F8: Synthesizing Biolinguistic Syntax with Neuropragmatic Inference via the ROSE Model

A critical open direction is fully computationalizing the handoff between the rigid algebraic geometry of syntax and the highly associative probabilistic inference of discourse. Murphy's **ROSE** (Representation, Operation, Structure, Encoding) model [@murphy2023rose] suggests that the brain achieves this via cross-frequency phase-amplitude coupling (PAC), establishing a "mesoscopic protectorate" for formal operations. Future extensions should:

- Model PAC directly within CEREBRUM by assigning distinct temporal decay rates to syntactic operators vs. pragmatic context vectors.
- Simulate the export of case-marked commutative diagrams from a simulated "core language network" to a simulated Default Mode Network using Gutiérrez Cisneros et al.'s [-@gutierrez2026neuropragmatics] framework for speech-act evaluation.
- Test whether the diagrammatic free-ride inferences (\autoref{fig:case-minimal}) predicted by our categorical model map onto the theta-gamma cross-frequency signatures observed during pragmatic garden-path recovery.

## Five Takeaways: One Argumentative Line per Formal Pillar

For the reader who absorbs nothing else, the argumentative line reduces to these five points — one per pillar of the formal architecture:

1. **Case is category-theoretic, not morphological.** The universal fact of linguistic case is that every language wires up *who did what to whom*; the formal content of that wiring is precisely the data of a category with case roles as objects and grammatical relations as morphisms. Alignment typologies (nominative, ergative, tripartite, active-stative, fluid-S) are structure-preserving functors between case categories — a typological taxonomy becomes a proof-by-functor.

2. **String diagrams make the grammar executable.** Lambek pregroup types, compact closure, and the snake equation compile each sentence into a DisCoPy string diagram whose normal form is the sentence type $s$; each reduction is a proof of well-typedness, and the reduction *is* the diagram. The three-sentence DisCoCirc example ships a working discourse with per-entity role-history ribbons showing Alice traversing NOM → ACC → NOM.

3. **Enriched weights ground graded intuitions.** Moving from $\mathbf{Bool}$- to $[0,1]$-enrichment replaces binary admissibility with graded distributional proximity, makes categorical magnitude $|\mathcal{C}| \approx 2.50$ a computable summary of effective role distinctions, and gives the enriched weight $w_f = \mathcal{C}(A, B)$ used throughout \autoref{sec:cognitive-integration} / \autoref{sec:daif-results} as the precision on every prediction error.

4. **DAIF ports the whole scaffolding into active inference.** Variational message passing, the Bethe free energy, and a four-term expected free energy $G(\pi)$ turn distributional case assignment into a first-principles inference loop. The N400 and P600 ERP amplitudes fall out of a first-order expansion $\Delta F \approx -\Delta \mathbb{E}[Z] + \tfrac{1}{2}\Delta\Lambda\sigma_Z^{2}$ — derivations, not empirical ansätze.

5. **The same formal layers give AI-safety researchers three concrete handles.** Type discipline on messages, decidable admissibility of multi-turn sequences, and graded-confidence attenuation (\autoref{sec:ai-implications}) give prompt injection a type-theoretic reformulation (\autoref{sec:cognitive-security}) — an engineering specification for agent protocols, not a guarantee on untyped present-day LLM APIs.

## What the Paper Does *Not* Claim: Consolidated Limitations

Four limitations recur across the framework and are recorded here explicitly rather than left implicit in their sections of origin:

- **The mean-field approximation in `push_forward_return`** maintains one belief-weighted return distribution instead of per-state distributions $Z(s)$. By the mean-field bound recorded in \autoref{sec:daif-limitations} the approximation error is at most $\gamma \cdot R_{\max} \cdot H[q]$ in the $W_1$ metric — tight for sharp posteriors, linearly degrading as entropy grows.
- **The enriched-categorical unification is a conjecture.** Distributional semantics, distributional RL, and active-inference posteriors all instantiate $[0,1]$-enriched structures, but a strict categorical proof that the three share a common enriching monoidal base remains open (\autoref{sec:daif-limitations}).
- **Empirical validation is narrow.** Case-assignment demonstrations use a single German sentence. Cross-linguistic and cross-register generalisation is left to future work; the hooks in `make_daif_belief_trajectory_data()` make adding corpora a one-function change.
- **ERP amplitudes are not calibrated to μV.** The DAIF predictions are on a dimensionless return/log-probability scale; converting to μV would require a per-subject scaling constant fit to empirical ERP data. The qualitative ordering and graded precision response are predictions the current framework *does* make.

## Anticipated Objections and Responses {#sec:reviewer-objections}

Four lines of objection stand out; we address each honestly rather than waiting for a reviewer.

**Objection 1 — "The mean-field approximation throws away the whole point of distributional RL."** *Response.* The belief-weighted collapse gives $\mathcal{O}(n)$ memory in place of $\mathcal{O}(n \cdot N_{\text{atoms}})$ and is exact in the sharp-posterior limit. The mean-field bound recorded in \autoref{sec:daif-limitations} quantifies the degradation as $H[q]$ grows. The alternative — maintaining per-state return distributions throughout a linguistic parse — would multiply the runtime of `distributional_case_assignment()` by a factor of $n$ (the role count) for a gain that vanishes as the posterior sharpens after the first few words of a sentence.

**Objection 2 — "The enriched-categorical unification is only stated, never proven."** *Response.* Conceded, and flagged in \autoref{sec:daif-limitations} and in the What's New block of \autoref{sec:whats-new}. Distributional semantics, distributional RL, and active-inference posteriors all *instantiate* $[0,1]$-enriched structure; whether they share a common enriching monoidal base in the strict sense of Kelly enriched-category theory is an open question. The repository's tests verify the enriched axioms hold in each instance; they do not construct the common base functor, and the manuscript nowhere uses the strict unification as a load-bearing step in any downstream argument.

**Objection 3 — "Cross-linguistic evidence is a single German sentence."** *Response.* The empirical scope reflects the publication's focus on *specification* rather than *corpus study*. The `Discourse.role_reversal("Alice", "Bob")` and `make_daif_belief_trajectory_data()` interfaces accept arbitrary lexical heads and observation sequences; extending to Basque, Dyirbal, Russian, Serbian/BCS, or any other language is a one-function change. \autoref{fig:multilingual-isomorphism} (in \autoref{sec:categorial-grammar}) already shows a pregroup multilingual isomorphism across English / Latin / Japanese, and the Slavic discussion in \autoref{sec:case-systems} extends the same type calculus to overtly case-marked Russian and Serbian noun phrases. Slavic-language ERP datasets — Bornkessel-Schlesewsky and colleagues' eADM-aligned Russian case-violation paradigms in particular [@bornkessel2006extended] — would provide a near-term empirical test for the precision-weighted P600 prediction in **C10** / **F4**. The three-sentence Alice/Bob discourse is a proof-of-concept, not a typological claim.

**Objection 4 — "The ROSE phase–amplitude coupling gap means you cannot predict ERP latencies."** *Response.* Conceded and flagged explicitly in \autoref{sec:daif-limitations}. The current implementation keeps N400 and P600 *peak latencies* as fixed Gaussian peaks at 380 ms and 600 ms respectively (see `DEFAULT_N400_PEAK_MS` / `DEFAULT_P600_PEAK_MS` in `src/daif/prediction.py`). A principled latency prediction would require a cross-frequency-coupling delay parameter inside the CEREBRUM layer; we flag this as the cleanest next research step.

## What to Read Next, by Reader Profile

Readers who entered this paper from different fields will want different onward paths:

- **Linguists / typologists**: skip ahead to \autoref{sec:case-systems}–\autoref{sec:case-categories} for the categorical formalisation of case and the five alignment functors; then \autoref{sec:compact-closure-complexity} for the complexity metrics that make cross-linguistic comparison quantitative.
- **Machine-learning researchers**: \autoref{sec:daif-results} first for the Distributional Active Inference extension of the Bellemare-Dabney-Munos programme to linguistic case; then \autoref{sec:daif-erp} for how DAIF yields falsifiable ERP predictions.
- **Cognitive / computational neuroscientists**: \autoref{sec:cognitive-integration} for the active-inference framing; \autoref{sec:diagrammatic-cognition} for the three falsifiable ERP predictions; \autoref{sec:daif-limitations} for the PAC-latency gap that is the cleanest experimental entry point.
- **QNLP / quantum-semantics engineers**: \autoref{sec:quantum-active-inference} and \autoref{sec:quantum-semantics} for the POVM-based case assignment and the honest separation of implemented POVM machinery from literature-bridge TQNN / ZX / lambeq claims.
- **AI-safety / agent-protocol practitioners**: \autoref{sec:ai-implications} for the three concrete handles (type discipline, decidable admissibility, graded confidence) and \autoref{sec:cognitive-security} for prompt injection as a type violation — engineering specification rather than automatic guarantee on today's APIs.

## Case Categories Are the Geometry of Meaning: A Unifying Coda

The commutative diagram is the central motif of this review---both as a mathematical tool and as a cognitive instrument. The analysis has demonstrated that the same diagrammatic language that makes category theory effective for formalizing case systems also makes it effective for _thinking about_ case systems: the spatial structure of a commutative diagram encodes relational information in a format that supports rapid search, pattern recognition, and free-ride inference.

This convergence of mathematical utility and cognitive efficacy is not accidental. If the active inference framework is correct, then the brain operates by constructing and updating generative models of the world's relational structure. Category theory provides the structural algebra for these generative models; commutative diagrams supply their natural topology; and case categories instantiate the precise relational vocabulary that cognitive systems deploy to organize experience into coherent narratives of _who does what to whom_. The distributional revolution in both semantics and reinforcement learning—from Firth's [-@firth1957papers] co-occurrence statistics through transformer attention weights to Distributional Active Inference [@akgul2026distributional]—confirms that meaning is not an atomic property of symbols but emerges from the relational structure of contexts, a principle that enriched category theory captures with mathematical precision.

Crucially, **this synthesis clarifies a mathematical angle on alignment for relational agent cognition.** Moving from flat token streams toward **explicitly typed** enriched categorical interaction grammars lets one state **when** prompt injection corresponds to a **type error relative to a fixed protocol**---the conditional analysis in \autoref{sec:cognitive-security}. Default LLM stacks do not yet enforce such protocols end-to-end; the payoff is sharper **specification** (what boundary checks would guarantee) and a research agenda for non-cartesian wiring, not a blanket claim that injection is already impossible in production systems.

Ultimately, the mathematics of case alignment presents a highly structured formal geometry of meaning—the relational algebra through which cognitive agents navigate and render intelligible the structured world of events, participants, and relations. The convergence of formal semantics, distributional semantics, and active inference within a single categorical framework suggests that commutative diagrams offer a natural formalism in which relational cognition can be modeled.
