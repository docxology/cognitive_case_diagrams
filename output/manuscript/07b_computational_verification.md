# Diagrams as Generative Models {#sec:diagrammatic-cognition}

## Why the Brain Prefers Diagrams

We can now substantially strengthen our initial architectural claim from \autoref{sec:introduction}: formal commutative diagrams do not merely provide a convenient pedagogical representation illustrating abstract case structure---they mathematically constitute the exact native *computational format* through which biological cognitive agents actively maintain and query their internal generative models representing relational environmental structure.

This strong structural claim draws support from powerful converging empirical evidence:

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
\text{PE}(f) \propto \pi_f \cdot |\mu_{\text{predicted}} - \mu_{\text{observed}}|
\label{eq:pe-precision-error}
\end{equation}

where $\pi_f = \mathcal{C}(A,B)$ is the enriched weight (precision) of the morphism $f: A \to B$ and $\mu$ are the expected vs. observed case features. This yields three concrete electrophysiological predictions:

1. **P600 amplitude scales with morphism weight**: A case violation on a high-weight morphism (NOM→ACC in a transitive clause, $w = 0.9$) should elicit a larger P600 than a violation on a low-weight morphism (NOM→INS in an experiencer construction, $w = 0.4$). The ratio of P600 amplitudes should approximate the ratio of enriched weights.

2. **N400 reflects distributional expectation**: Semantic case violations—where the case-marked NP satisfies the morphological case but not the distributional proto-role requirements (e.g., an inanimate NOM in an agentive construction)—should elicit N400 effects proportional to the *magnitude deficit* of the violated enriched category (\autoref{sec:enriched-categories}).

3. **Garden-path reanalysis costs track magnitude**: The processing cost of reanalyzing a garden-path sentence's case structure should correlate with the *change in categorical magnitude* between the initial and revised case diagrams, since magnitude quantifies how much relational information the agent's generative model encodes.

## Integration: Five Pillars Become One Generative Model

The full picture emerges when we combine all five pillars within the active inference framework:

1. **Case categories** (\autoref{sec:case-systems}) provide the *objects and morphisms* of the generative model—the vocabulary of roles and relations
2. **Categorial grammar** (\autoref{sec:categorial-grammar}) provides the *composition rules*—how roles combine to form structured derivations
3. **DisCoCat / DisCoCirc** (\autoref{sec:categorical-semantics}, \autoref{sec:compact-closure-complexity}, \autoref{sec:discocirc-discourse}) provides the *semantic functor* and discourse extension—mapping syntactic structure to distributional meaning
4. **Enriched structure** (\autoref{sec:enriched-categories}) provides the *precision parameters*—graded weights that control inference
5. **Topos-theoretic bridges** (\autoref{sec:topos-theory}) provide *transfer theorems*—ensuring consistency across formalizations

The active inference agent uses this combined structure as a single, integrated generative model. Each scenario it encounters—a sentence heard, a scene observed, an action planned—is interpreted by instantiating a case diagram from structure (1), parsing the input using rules (2), computing meaning via the semantic functor (3), weighting confidence using enriched structure (4), and transferring results across representational formats using bridge techniques (5).

This is *total cognitive scenario understanding*: the agent doesn't just parse a sentence or assign case labels—it constructs a complete, internally consistent, generic, strongly typed, dynamically updating model of the relational structure of the situation, and uses that model to predict, explain, and act.

## 804 Automated Tests Confirm the Formalism Is Executable

The framework developed in this paper is not merely theoretical—it is computationally verified through a comprehensive implementation and test suite that exercises every categorical construction discussed above.

### System Architecture and Categorical Core

The categorical core (`CaseCategory`, `EnrichedCategory`, `AlignmentFunctor`, `NaturalTransformation`) is implemented in Python with set-based object tracking and list-based morphism storage, enforcing categorical axioms at construction time. Six additional modules extend the core: `FluidSFunctor` (context-dependent alignment parameterized by volition), `CaseDiagramBelief` and active inference computations (variational free energy, prediction error, belief updating), the **`src/daif/` subpackage** (7 modules, 24 symbols—full distributional RL inference: push-forward returns, quantile TD, VMP, Bethe FE, EIG, ERP profiles, policy selection, and metrics), `CasePOVM` and quantum case assignment (POVM-based probability via \autoref{eq:eq-8-1} in \autoref{sec:quantum-semantics}), `DitransitiveSentence` (three-argument verb support), and `CaseFrameValidator` (cognitive security via type-violation detection). The visualization layer produces all manuscript figures programmatically, ensuring exact correspondence between formal claims and visual evidence. The DisCoPy integration library (version 1.2.2) provides an independent validation path: pregroup types (`Ty`), lexical entries (`Word`), cup contractions (`Cup`), cap expansions (`Cap`), type permutations (`Swap`), normal form computation (`normal_form()`), and circuit depth analysis (`depth()`) are exercised against the same categorical structures described in \autoref{sec:categorial-grammar} and \autoref{sec:categorical-semantics}.

### Automated Test Suite and Verification

The implementation is validated by **804 automated tests** across 47 test files with **≥90% code coverage** (enforced in the build configuration). Every test uses real mathematical computations—no mocks or fakes. The **per-category inventory** (counts, modules, and DAIF file breakdown) is listed in \autoref{sec:test-suite-inventory}.

This computational verification demonstrates that the category-theoretic framework is not just a mathematical convenience but a *working computational architecture*—the categorical abstractions compile, execute, and produce verifiable results, bridging the gap between formal theory and implemented system.
