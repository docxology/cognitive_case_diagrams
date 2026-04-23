# Diagrams as Cognitively Privileged Representations: Free Rides, ERP Predictions, and Six-Strand Synthesis {#sec:diagrammatic-cognition}

**Where we are in the argument.** \autoref{sec:cognitive-integration} supplied the process theory (active inference over a case-role posterior). This chapter cashes that theory out in two ways: first with three falsifiable ERP predictions (precision-weighted P600 amplitude, magnitude-change N400 proxy, garden-path reanalysis cost) that empirically test the framework, and second with an automated test inventory demonstrating that every formal claim is backed by executable code — the "six-strand synthesis" that brings typology, type logic, distributional semantics, enriched structure, topos theory, and biolinguistic interfacing into a single generative model.

## Why the Brain Prefers Diagrams

We can now substantially strengthen our initial architectural claim from \autoref{sec:introduction}: formal commutative diagrams do not merely provide a convenient pedagogical representation illustrating abstract case structure---they mathematically constitute the exact native *computational format* through which biological cognitive agents actively maintain and query their internal generative models representing relational environmental structure.

This structural claim draws support from converging empirical evidence:

1. **Computational advantage** (Larkin & Simon, [-@larkin1987diagram]): Diagrams enable search, recognition, and inference operations that are computationally prohibitive in sentential format. A commutative case diagram allows the agent to verify consistency (does the direct path equal the composed path?) by simple spatial inspection.

2. **Free ride inferences** (Shimojima, [-@shimojima1996reasoning]): Properties of the diagram that are perceptually available but would require explicit computation in a sentential format. In a case diagram, transitivity of grammatical relations is *visible*—the existence of a path from NOM to DAT through ACC is spatially apparent.

3. **Hybrid reasoning** (Giardino, [-@giardino2017diagrammatic]): Mathematical diagrams engage a mode of reasoning that combines perceptual pattern recognition with background theoretical knowledge. Case diagrams similarly engage both the perceptual system (spatial layout) and linguistic knowledge (case constraints, verb valency).

4. **Peirce's existential graphs**: Peirce's graphical logic system demonstrated that first-order logic can be conducted entirely diagrammatically, without algebraic symbols. Our case diagrams extend this tradition: the relational structure of a sentence is represented graphically, and inference proceeds by diagram manipulation (adding/removing nodes, composing morphisms).

## P600 Signals and Garden-Path Reanalysis in Diagrammatic Models

The standard predictive processing framework—for which active inference operates as the most formally mathematically developed version—provides a remarkably natural, mechanistically precise account detailing exactly how biological agents actively deploy these diagrammatic representations cognitively during real-time processing:

1. **Top-down structural predictions**: The currently active internal case diagram continuously generates precise, high-precision predictions anticipating incoming expected sensory input (e.g., the system computationally predicts "a nominative-marked noun phrase must immediately appear because the parsed transitive verb structurally demands an active agent").

2. **Bottom-up prediction errors**: Incoming sensory words that physically violate the model's top-down diagrammatic predictions instantly generate massive, measurable prediction errors (e.g., encountering a structurally unexpected morphological case marker directly triggers a quantifiable P600 event-related neural potential measurable in the biological brain).

3. **Belief updating**: The diagram is updated to accommodate the prediction error, potentially restructuring the assignment of entities to case roles (garden-path reanalysis)

4. **Precision weighting**: The enriched weights on morphisms serve as *precision parameters* that control the relative influence of prior expectations and incoming evidence. A high-weight morphism generates strong predictions that are costly to override; a low-weight morphism generates weak predictions that are easily overridden.

## Three Falsifiable ERP Predictions

The predictive processing account generates quantitative, falsifiable predictions about neural responses to case-marking violations. In the active inference framework, a case-assignment violation triggers a *prediction error* whose amplitude scales with the precision of the violated expectation—which is precisely the enriched hom-value of the violated morphism:

\begin{equation}
\text{PE}(f) \propto w_f \cdot |\mu_{\text{predicted}} - \mu_{\text{observed}}|
\label{eq:pe-precision-error}
\end{equation}

where $w_f = \mathcal{C}(A,B)$ is the enriched morphism weight (acting as a precision on prediction error) for $f: A \to B$ and $\mu$ are the expected vs. observed case features. This yields three concrete electrophysiological predictions:

1. **P600 amplitude scales with morphism weight**: A case violation on a high-weight morphism (NOM→ACC in a transitive clause, $w = 0.85$ per $\mathcal{C}(\text{NOM},\text{ACC})$ in the standard enriched category) should elicit a larger P600 than a violation on a low-weight morphism (NOM→INS in an experiencer construction, $w = 0.35$ per $\mathcal{C}(\text{NOM},\text{INS})$). The ratio of P600 amplitudes should approximate the ratio of enriched weights ($0.85/0.35 \approx 2.4$).

2. **N400 reflects distributional expectation**: Semantic case violations—where the case-marked NP satisfies the morphological case but not the distributional proto-role requirements (e.g., an inanimate NOM in an agentive construction)—should elicit N400 effects proportional to the *absolute change in categorical magnitude* induced by the violation, $\big\lvert |\mathcal{C}_{\text{after}}| - |\mathcal{C}_{\text{before}}|\big\rvert$ (\autoref{sec:enriched-categories}). The N400 is thus time-locked to the transition between pre-violation and post-violation diagrams, not to any static property of either category alone; the `n400_amplitude_proxy()` function in `src/cognitive/reanalysis.py` computes precisely this quantity.

3. **Garden-path reanalysis costs track magnitude**: The processing cost of reanalyzing a garden-path sentence's case structure should correlate with the *change in categorical magnitude* between the initial and revised case diagrams, since magnitude quantifies how much relational information the agent's generative model encodes.

## Integration: Six Strands Become One Generative Model

The full picture emerges when we combine the **five formal layers** of \autoref{sec:introduction} (Pillars 1–5) with the **sixth strand** (Pillar 6: biolinguistics and oscillatory interfacing via ROSE), all within the active inference framework:

1. **Case categories** (\autoref{sec:case-systems}) provide the *objects and morphisms* of the generative model—the vocabulary of roles and relations
2. **Categorial grammar** (\autoref{sec:categorial-grammar}) provides the *composition rules*—how roles combine to form structured derivations
3. **DisCoCat / DisCoCirc** (\autoref{sec:categorical-semantics}, \autoref{sec:compact-closure-complexity}, \autoref{sec:discocirc-discourse}) provides the *semantic functor* and discourse extension—mapping syntactic structure to distributional meaning
4. **Enriched structure** (\autoref{sec:enriched-categories}) provides the *precision parameters*—graded weights that control inference
5. **Topos-theoretic bridges** (\autoref{sec:topos-theory}) provide *transfer theorems*—ensuring consistency across formalizations
6. **Biolinguistic and neurocomputational interface** (\autoref{sec:introduction}, \autoref{sec:cognitive-integration}): ROSE-style cross-frequency coupling links hierarchical syntax (MERGE-level constraints) to the associative dynamics of comprehension—supplying the neural-timescale bridge under which the formal diagram is *deployed* in real time.

The active inference agent uses this combined structure as a single, integrated generative model. Each scenario it encounters—a sentence heard, a scene observed, an action planned—is interpreted by instantiating a case diagram from structure (1), parsing the input using rules (2), computing meaning via the semantic functor (3), weighting confidence using enriched structure (4), transferring results across representational formats using bridge techniques (5), and routing syntactic structure through the oscillatory interface (6) during online comprehension and production.

This is *total cognitive scenario understanding*: the agent doesn't just parse a sentence or assign case labels—it constructs a complete, internally consistent, generic, strongly typed, dynamically updating model of the relational structure of the situation, and uses that model to predict, explain, and act.

## ${total_test_count} Automated Tests Confirm the Formalism Is Executable

The framework developed in this paper is computationally verified through an implementation and test suite that exercises every categorical construction discussed above.

### System Architecture and Categorical Core

The categorical core (`CaseCategory`, `EnrichedCategory`, `AlignmentFunctor`, `NaturalTransformation`) is implemented in Python with set-based object tracking and list-based morphism storage, enforcing categorical axioms at construction time. **${domain_subpackages}** first-level packages under ``src/`` structure the domain code; six further module groups extend the core: `FluidSFunctor` (context-dependent alignment parameterized by volition), `CaseDiagramBelief` and active inference computations (variational free energy, prediction error, belief updating), the **`src/daif/` subpackage** (${daif_modules} modules, ${daif_symbols} symbols—full distributional RL inference: push-forward returns, quantile TD, VMP, Bethe FE, EIG, ERP profiles, policy selection, and metrics), `CasePOVM` and quantum case assignment (POVM-based probability via \autoref{eq:eq-8-1} in \autoref{sec:quantum-semantics}), `DitransitiveSentence` (three-argument verb support), and `CaseFrameValidator` (cognitive security via type-violation detection). The visualization layer produces all manuscript figures programmatically, ensuring exact correspondence between formal claims and visual evidence. The DisCoPy integration library (installed version ${discopy_version_pretty}) provides an independent validation path: pregroup types (`Ty`), lexical entries (`Word`), cup contractions (`Cup`), cap expansions (`Cap`), type permutations (`Swap`), normal form computation (`normal_form()`), and circuit depth analysis (`depth()`) are exercised against the same categorical structures described in \autoref{sec:categorial-grammar} and \autoref{sec:categorical-semantics}.

### Automated Test Suite and Verification

The implementation is validated by **${total_test_count}** automated tests across **${total_test_files}** test files. ${coverage_summary} The configuration enforces **≥90%** coverage on ``src/``. Every test uses real mathematical computations—no mocks or fakes. The **per-category inventory** (counts, modules, and DAIF file breakdown) is listed in \autoref{sec:test-suite-inventory}.

This computational verification demonstrates that the category-theoretic framework is a *working computational architecture*: the categorical abstractions compile, execute, and produce verifiable results, bridging the gap between formal theory and implemented system.
