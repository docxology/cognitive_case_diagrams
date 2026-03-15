# Cognitive Integration: Active Inference and Diagrammatic Reasoning {#sec:cognitive-integration}

## The Missing Layer: A Dynamic Process Theory of Cognition

The preceding sections have developed a rich mathematical infrastructure for analyzing case systems—categorical, type-logical, distributional, enriched, and topos-theoretic. But these frameworks are *static*: they describe the structure of case without explaining how a cognitive agent *uses* that structure in real-time language understanding and production. What is needed is a *process theory* that explains how case-marked relational structure is deployed in the dynamic, embodied, context-sensitive activity of making sense of the world.

Active inference [@friston2017active] provides exactly this layer.

## Active Inference as a Process Theory of Language Understanding

### The Free Energy Principle and Surprise Minimization

Active inference is the process theory derived from the free energy principle (FEP): every self-organizing system maintains itself by minimizing the surprisal (negative log-probability) of its sensory observations under a *generative model* of its environment [-@friston2010free]. The system does this through two complementary strategies:

1. **Perceptual inference**: Update internal beliefs to better predict current observations (reduce prediction error)
2. **Active inference**: Act on the environment to bring observations in line with predictions (reduce expected prediction error)

Recent extensions of active inference to linguistics and cognitive science have modeled language comprehension and production as forms of sequential Bayesian inference. As Donnarumma, Frosolone, and Pezzulo (2023) note in their integration of large language models and active inference, "linguistic processing [is] inference over a hierarchical generative model, facilitating predictions and inferences at various levels of granularity, from syllables to sentences" [-@donnarumma2023integrating]. Similarly, Friston et al. (2021) have demonstrated how communication emerges between synthetic subjects: "linguistic outcomes (specifically, the spoken word)... are selected to minimise the free energy given current beliefs" via "high-order interactions among abstract (discrete) states in deep (hierarchical) models" [-@friston2021understanding; -@friston2020generative].

Both strategies minimize the same quantity—variational free energy—and both are driven by a single generative model that encodes the system's expectations about the structure of its world.

#### Generative Models of Relational Structure

Language understanding on this view is *active inference over relational structure*: the listener maintains a generative model of who-does-what-to-whom, and each incoming word provides evidence that updates this model. Case marking provides crucial evidence—a nominative suffix strongly predicts that the marked NP is the agent, reducing uncertainty about the relational structure of the unfolding event.

### Predictive Processing of Case

The process unfolds as follows:

1. **Prior**: The listener has a prior belief about the relational structure (a "case diagram" encoding expected roles and their connections)
2. **Observation**: Each word provides sensory evidence—its form, its case marking, its distributional properties
3. **Update**: The listener updates the case diagram to accommodate the evidence, using approximate Bayesian inference (typically variational message passing)
4. **Prediction**: The updated diagram generates predictions about upcoming words (case-marked NPs, verb valency patterns)
5. **Action**: In production, the speaker selects words and case markers that minimize expected free energy—choosing expressions that are informative, contextually appropriate, and syntactically well-formed

### Connection to Barwise and Perry's Situation Semantics

This active inference perspective connects directly to the **situation semantics** of Barwise and Perry [-@barwise1983situations], which conceptualized meaning as structured *situations*—collections of typed entities, properties, and relations individuated by spatial and temporal location. In our framework:

- A **situation** corresponds to an instantiated case diagram: a specific assignment of entities to case roles, with particular morphisms activated
- The **situation type** corresponds to the case category itself: the abstract pattern of roles and relations that the situation instantiates
- **Information flow** between situations corresponds to functorial mappings between case categories

Active inference adds the dynamic component: the agent moves through a sequence of situations, updating its case diagram in real time and using the diagram to predict which situation will come next.

## Distributional Active Inference: Convergence of Two Distributional Traditions

A remarkable convergence has recently emerged between *distributional semantics* in linguistics and *distributional reinforcement learning* in machine learning, mediated by active inference. Akgül et al. [-@akgul2026distributional] introduce **Distributional Active Inference (DAIF)**, which integrates active inference into the distributional RL framework of Bellemare, Dabney, and Munos [-@bellemare2017distributional]. Where classical RL optimizes *expected* returns (scalar values), distributional RL models the *full distribution* of returns—a shift from point estimates to distributional representations that parallels the shift from symbolic to distributional semantics in linguistics.

The formal architecture of DAIF proceeds through three stages: (1) reconstructing active inference via variational Bayesian inference on a controlled Markov process, expressing priors through Pearl's do-calculus; (2) defining a *push-forward* operation on representation paths that maps latent-space trajectories to return distributions; and (3) deriving a temporal-difference quantile-matching algorithm that implements active inference without requiring explicit transition dynamics modeling. The resulting "push-forward RL" template achieves active inference's sample-efficiency advantages within a model-free computational architecture:

$$\mathbb{E}\left[\sum_{t=0}^{\infty} \gamma^t R(x_t, a_t) \mid x_0, a_0\right] = \int_{\mathcal{S}^{\mathbb{N}_+}} R \circ f \, d(\mathbf{S}_{\#} \mathbb{P}_{x_0, a_0}^{P_\pi}) $$ {#eq:eq-7-1}

where $\mathbf{S}_{\#}$ denotes the push-forward measure on representation paths and $f: \mathcal{S} \to \mathcal{X}$ is the stochastic decoder.

The terminological collision between "distributional" in distributional semantics and "distributional" in distributional RL is not mere homonymy—it reflects a deep structural parallel. In both domains, the core move is the same: **replacing scalar summaries with full distributional representations.** In linguistics, this means replacing symbolic word identities with probability distributions over contexts (Firth's [-@firth1957papers] company-keeping principle). In RL, it means replacing expected-value estimates with full return distributions. In active inference, it means replacing point estimates of world states with variational posterior distributions. The enriched-categorical framework of \autoref{sec:enriched-categories} provides the unifying abstraction: all three are instances of $[0,1]$-enriched categories where hom-values encode distributional proximity rather than discrete identity.

For case-theoretic reasoning, DAIF suggests a computational architecture in which case assignment operates distributional-ly at every level: the agent maintains not a single case diagram but a *distribution over case diagrams*, weighted by their posterior probability given the observed linguistic evidence. Each incoming word updates this distribution via variational message passing, and the agent's production choices minimize expected free energy across the full distribution of possible relational structures—not merely the most likely one. This distributional perspective on case assignment aligns naturally with the graded proto-role structure of Dowty [-@dowty1991thematic]: a noun phrase is not categorically "agent" or "patient" but distributes probability mass across case roles, with the distribution sharpening as more evidence accumulates.

## CEREBRUM: The Computational Architecture

### Architecture and Design Principles

The **CEREBRUM** framework [@friedman2024cerebrum; @cerebrum2024github]—Case-Enabled Reasoning Engine with Bayesian Representations for Unified Modeling—provides a computational architecture that implements the categorical case framework within an active inference engine. CEREBRUM instantiates the view of Vasil et al. [-@vasil2020world] that human communication is itself active inference: a process of jointly constructing and refining generative models of shared relational structure.

CEREBRUM's key design principles:

| Principle | Implementation |
| :--- | :--- |
| **Cases as functional roles** | Model components carry case markings that determine their computational role in the inference cycle |
| **Morphisms as message passing** | Grammatical relations are implemented as message-passing channels between components |
| **Enriched weights as precision** | The $[0,1]$ weights on morphisms correspond to precision parameters in the variational inference scheme |
| **Alignment as model selection** | Different alignment types correspond to different generative model architectures, selected by Bayesian model comparison |
| **Diagrams as generative models** | Commutative diagrams serve as the structural specification of the generative model |

### Case Roles as Functional Specializations in CEREBRUM

CEREBRUM deploys the eight traditional cases as functional specializations:

| Case | CEREBRUM Function | Active Inference Role |
| :--- | :--- | :--- |
| NOM | Primary driver / agent | Source of action policies |
| ACC | Primary target / patient | Object of predictions |
| GEN | Source / possessor | Provider of priors |
| DAT | Recipient / goal | Target of information transfer |
| INS | Instrument / means | Tool for state transformation |
| LOC | Context / environment | Markov blanket boundary |
| ABL | Origin / cause | Source of causal influence |
| VOC | Addressee | Pragmatic pointer |

## Diagrammatic Reasoning as a Cognitive Process Theory

### Diagrams as the Format of Generative Models

The claim from \autoref{sec:introduction} can now be strengthened: commutative diagrams are not merely convenient representations of case structure---they are the *format* in which cognitive agents maintain their generative models of relational structure.

This claim is supported by converging evidence:

1. **Computational advantage** (Larkin & Simon, [-@larkin1987diagram]): Diagrams enable search, recognition, and inference operations that are computationally prohibitive in sentential format. A commutative case diagram allows the agent to verify consistency (does the direct path equal the composed path?) by simple spatial inspection.

2. **Free ride inferences** (Shimojima, [-@shimojima1996reasoning]): Properties of the diagram that are perceptually available but would require explicit computation in a sentential format. In a case diagram, transitivity of grammatical relations is *visible*—the existence of a path from NOM to DAT through ACC is spatially apparent.

3. **Hybrid reasoning** (Giardino, [-@giardino2017diagrammatic]): Mathematical diagrams engage a mode of reasoning that combines perceptual pattern recognition with background theoretical knowledge. Case diagrams similarly engage both the perceptual system (spatial layout) and linguistic knowledge (case constraints, verb valency).

4. **Peirce's existential graphs**: Peirce's graphical logic system demonstrated that first-order logic can be conducted entirely diagrammatically, without algebraic symbols. Our case diagrams extend this tradition: the relational structure of a sentence is represented graphically, and inference proceeds by diagram manipulation (adding/removing nodes, composing morphisms).

### Predictive Processing and Diagrammatic Belief Updating

The predictive processing framework—of which active inference is the most developed version—provides a natural account of how diagrammatic representations are used cognitively:

1. **Top-down predictions**: The current case diagram generates predictions about expected sensory input (e.g., "a nominative-marked NP should appear because the transitive verb requires an agent")

2. **Bottom-up prediction errors**: Incoming words that violate the diagrammatic predictions generate prediction errors (e.g., an unexpected case marker triggers a P600 event-related potential in the brain)

3. **Belief updating**: The diagram is updated to accommodate the prediction error, potentially restructuring the assignment of entities to case roles (garden-path reanalysis)

4. **Precision weighting**: The enriched weights on morphisms serve as *precision parameters* that control the relative influence of prior expectations and incoming evidence. A high-weight morphism generates strong predictions that are costly to override; a low-weight morphism generates weak predictions that are easily overridden.

### Electrophysiological Predictions: Case Violations as Prediction Error

The predictive processing account generates quantitative, falsifiable predictions about neural responses to case-marking violations. In the active inference framework, a case-assignment violation triggers a *prediction error* whose amplitude scales with the precision of the violated expectation—which is precisely the enriched hom-value of the violated morphism:

$$\text{PE}(f) \propto \pi_f \cdot |\mu_{\text{predicted}} - \mu_{\text{observed}}|$$

where $\pi_f = \mathcal{C}(A,B)$ is the enriched weight (precision) of the morphism $f: A \to B$ and $\mu$ are the expected vs. observed case features. This yields three concrete electrophysiological predictions:

1. **P600 amplitude scales with morphism weight**: A case violation on a high-weight morphism (NOM→ACC in a transitive clause, $w = 0.9$) should elicit a larger P600 than a violation on a low-weight morphism (NOM→INS in an experiencer construction, $w = 0.4$). The ratio of P600 amplitudes should approximate the ratio of enriched weights.

2. **N400 reflects distributional expectation**: Semantic case violations—where the case-marked NP satisfies the morphological case but not the distributional proto-role requirements (e.g., an inanimate NOM in an agentive construction)—should elicit N400 effects proportional to the *magnitude deficit* of the violated enriched category (\autoref{sec:enriched-categories}).

3. **Garden-path reanalysis costs track magnitude**: The processing cost of reanalyzing a garden-path sentence's case structure should correlate with the *change in categorical magnitude* between the initial and revised case diagrams, since magnitude quantifies how much relational information the agent's generative model encodes.

## Total Cognitive Scenario Understanding: The Integrated Framework

The full picture emerges when we combine all five pillars within the active inference framework:

1. **Case categories** (\autoref{sec:case-systems}) provide the *objects and morphisms* of the generative model—the vocabulary of roles and relations
2. **Categorial grammar** (\autoref{sec:categorial-grammar}) provides the *composition rules*—how roles combine to form structured derivations
3. **DisCoCat/DisCoCirc** (\autoref{sec:categorical-semantics}) provides the *semantic functor*—mapping syntactic structure to distributional meaning
4. **Enriched structure** (\autoref{sec:enriched-categories}) provides the *precision parameters*—graded weights that control inference
5. **Topos-theoretic bridges** (\autoref{sec:topos-theory}) provide *transfer theorems*—ensuring consistency across formalizations

The active inference agent uses this combined structure as a single, integrated generative model. Each scenario it encounters—a sentence heard, a scene observed, an action planned—is interpreted by instantiating a case diagram from structure (1), parsing the input using rules (2), computing meaning via the semantic functor (3), weighting confidence using enriched structure (4), and transferring results across representational formats using bridge techniques (5).

This is *total cognitive scenario understanding*: the agent doesn't just parse a sentence or assign case labels—it constructs a complete, internally consistent, generic, strongly typed, dynamically updating model of the relational structure of the situation, and uses that model to predict, explain, and act.

## Computational Verification and Results

The framework developed in this paper is not merely theoretical—it is computationally verified through a comprehensive implementation and test suite that exercises every categorical construction discussed above.

### System Architecture and Implementation

### Implementation Architecture and Categorical Core

The categorical core (`CaseCategory`, `EnrichedCategory`, `AlignmentFunctor`, `NaturalTransformation`) is implemented in Python with set-based object tracking and list-based morphism storage, enforcing categorical axioms at construction time. Five additional modules extend the core: `FluidSFunctor` (context-dependent alignment parameterized by volition), `CaseDiagramBelief` and active inference computations (variational free energy, prediction error, belief updating), `CasePOVM` and quantum case assignment (POVM-based probability via [@eq:eq-8-1]), `DitransitiveSentence` (three-argument verb support), and `CaseFrameValidator` (cognitive security via type-violation detection). The visualization layer produces all 15+ manuscript figures programmatically, ensuring exact correspondence between formal claims and visual evidence. The DisCoPy integration library (version 1.2.2) provides an independent validation path: pregroup types (`Ty`), lexical entries (`Word`), cup contractions (`Cup`), cap expansions (`Cap`), type permutations (`Swap`), normal form computation (`normal_form()`), and circuit depth analysis (`depth()`) are exercised against the same categorical structures described in \autoref{sec:categorial-grammar} and \autoref{sec:categorical-semantics}.

### Automated Test Suite and Verification

The implementation is validated by **261 automated tests** across 15 test files with **≥90% code coverage** (enforced in the build configuration). Every test uses real mathematical computations—no mocks or fakes:

- **Categorical axiom tests**: Identity morphism existence, composition associativity, weight invariants, `is_well_formed()` full axiom check
- **Enriched category tests**: Hom-value constraints, composition inequality, categorical magnitude, magnitude deficit, full composition check, role clustering
- **Diagram type tests**: Pregroup diagrams validated for `dom == Ty()` and `cod == s`, correct box counts, diagram equality
- **Metrics tests**: Normal form preservation, depth computation with graceful fallback for pregroup diagrams
- **Natural transformation tests** (16 tests): Component morphism construction, naturality condition verification for accusative-to-ergative functors, identity transformation generation, vertical composition of transformations, completeness checking over all domain objects
- **Complexity metrics tests** (17 tests): DisCoPy box/cup/cap counting on transitive/ditransitive diagrams, normal form computation and snake equation verification, syntactic complexity scoring with configurable weights, cross-diagram comparison utilities
- **Topos theory tests** (18 tests): Geometric theory construction from standard and minimal case categories, classifying topos invariant computation, Morita equivalence verification (positive and negative cases), bridge transfer between equivalent theories with transfer-blocking for non-equivalent theories, enriched theory construction
- **Fluid-S tests** (22 tests): Volitional/non-volitional mapping, probability splits, Bats language examples, kernel computation, enriched weight scaling
- **Active inference tests** (24 tests): Belief construction and entropy, variational free energy, Bayesian belief update, prediction error scaling (P600 prediction), magnitude-based garden-path reanalysis cost
- **Quantum case tests** (20 tests): Crisp POVM orthogonal projectors, graded proto-role POVM, Fluid-S basis rotation, density matrix creation, [@eq:eq-8-1] P(c|ρ) = Tr(E_c ρ) verification
- **Cognitive security tests** (18 tests): Type-violation detection, case frame validation, injection score computation, magnitude-based topological robustness, composition inequality as security boundary
- **Ditransitive tests** (12 tests): Three-argument sentence creation, NOM/ACC/DAT case assignment, DisCoPy diagram with 3 cups, complexity comparison with transitive
- **Visualization tests** (4 tests): Complexity comparison bar chart rendering, normal form comparison chart, radar chart generation—all producing valid PNG output files

This computational verification demonstrates that the category-theoretic framework is not just a mathematical convenience but a *working computational architecture*—the categorical abstractions compile, execute, and produce verifiable results, bridging the gap between formal theory and implemented system.
