# Quantum Active Inference: Topological Semantic Communication {#sec:quantum-active-inference}

The preceding sections have established that categorical string diagrams—from DisCoCat's pregroup derivations (\autoref{sec:categorical-semantics}) through enriched hom-values (\autoref{sec:enriched-categories}) to topos-theoretic transfer (\autoref{sec:topos-theory})—provide a unified diagrammatic language for case-theoretic reasoning. This section extends the framework into its natural quantum generalization: topological quantum neural networks (TQNNs), the ZX-calculus, and sheaf-theoretic quantum semantic communication. The central observation is that the same monoidal-categorical architecture that underlies DisCoCat string diagrams also underlies quantum circuits, TQFT cobordisms, and quantum information flow—making active inference on case-marked relational structure a quantum topological computation.

## Topological Quantum Neural Networks: Spin-Network Representations

### From Quantum Neural Networks to TQFT

Marcianò, Fields, and Glazebrook demonstrate that quantum neural networks (QNNs) admit a topological reformulation via spin-networks [@fields2022tqnn]. In their analysis, a QNN layer or connectivity pattern is represented as a graph whose edges carry representation labels (spins) and whose vertices carry intertwiners—precisely the graphical data of a spin-network in a 3-dimensional topological quantum field theory:

> "Quantum Neural Networks (QNNs) can be mapped onto spin-networks, with the consequence that the level of analysis of their operation can be carried out on the side of Topological Quantum Field Theory (TQFT)." [@fields2022tqnn]

This reformulation has three important structural consequences. First, the neural architecture becomes a topological diagram (spin-network / ribbon graph) whose evaluation by a TQFT functor gives a quantum process; the edges and nodes of the graph encode how quantum information flows and transforms. Second, the TQFT evaluation functorially assigns to boundary Hilbert spaces (inputs/outputs) linear maps obtained from topological invariants (Reshetikhin–Turaev, Turaev–Viro), playing the role of the network's forward pass: amplitudes "flow" through the topological diagram. Third, the topological control structure encodes information flow through the network's wiring topology rather than through any fixed geometric embedding [@fields2023tensor].

### Universal Quantum Computation via TQNNs

Fields and collaborators further demonstrate that TQNNs are universal quantum computers by identifying the Reshetikhin–Turaev invariant of a TQNN with a Turaev–Viro quantum error-correcting code:

> "TQNNs enable universal quantum computation, using the Reshetikhin-Turaev and Turaev-Viro models to show how TQNNs implement quantum error-correcting codes." [@fields2025amplituhedra]

The universality result is established via the concept of an *execution trace* for a quantum computation, leading to the representation of TQNNs in terms of the positive geometries provided by amplituhedra—a deep connection between quantum computation, scattering amplitudes, and topological combinatorics.

### Quantum Reference Frames and Holographic Screens

Fields and Glazebrook's work on quantum reference frames (QRFs) and holographic screens provides additional algebraic structure [@fields2021qrf]. A holographic screen—the information boundary between two interacting quantum systems—carries a qubit array encoding their interaction. The key insight is that QRFs deployed to identify systems and select pointer states induce decoherence, breaking the symmetry of the holographic encoding in an observer-relative way. This symmetry-breaking is precisely the mechanism by which a TQNN "observes" its input: the choice of QRF determines the basis in which the spin-network is evaluated.

For case-theoretic reasoning, this connects to the grammatical observer problem: a parser or comprehender selecting a case-assignment frame for a sentence is analogous to deploying a QRF that fixes the pointer basis for a quantum measurement on a holographic screen.

## The ZX-Calculus: Categorical Quantum Circuit Diagrams

### String Diagrams for Quantum Processes

The ZX-calculus provides a categorical, diagrammatic language in which quantum circuits are drawn as string diagrams in a symmetric monoidal category of finite-dimensional Hilbert spaces and linear maps [@kissinger2020zx]:

> "The ZX-calculus is a graphical language for reasoning about quantum computations and circuits... it can represent any linear map, and can be considered a diagrammatically complete generalization of the usual circuit representation." [@coeckekissinger2017]

Several structural features are critical for the connection to case-theoretic diagrams:

- **Diagrams as morphisms**: ZX-diagrams are string diagrams in a $\dagger$-compact closed category. Wires represent objects (qubits), spiders and boxes represent morphisms, and composition/tensor product correspond to vertical/horizontal gluing. No metric geometry enters—only the topology of connections. ZX is therefore already a *topological* representation of quantum processes.
- **Circuit extraction via generalized flow**: Kissinger and van de Wetering demonstrate that quantum circuits can be mapped into ZX-diagrams, subjected to purely graph-theoretic (topological) transformations, and then extracted as optimized circuits. They prove that "the underlying graph of our simplified ZX-diagram always has a graph-theoretic property called generalised flow, which in turn yields a deterministic circuit extraction procedure" [@kissinger2020zx].
- **Category-theoretic semantics**: The semantics of a ZX-diagram are determined entirely by how components are wired together—precisely the compositional principle underlying DisCoCat and the case categories of \autoref{sec:case-systems}.

### From DisCoCat to ZX: A Shared Categorical Architecture

The structural parallel between pregroup grammar diagrams and ZX-diagrams is not accidental. Both are instances of the same mathematical object: morphisms in a compact closed monoidal category with functorial semantics into Hilbert spaces. In DisCoCat, the functor assigns to each grammatical type a vector space and to each derivation a linear map computing sentence meaning [@coecke2010mathematical]. In ZX, the standard semantics functor assigns to each spider/Hadamard configuration a linear map in **FHilb**. The shared categorical architecture means:

1. **Pregroup contractions (cups) and ZX spiders** are both instances of the same algebraic operation: evaluation morphisms in a compact closed category.
2. **DisCoCat normal forms** and **ZX simplifications** are both applications of the same rewriting theory: equational reasoning modulo the axioms of a compact closed category.
3. **The snake equation** (Cap $\circ$ Cup = identity) that grounds all pregroup type reductions (\autoref{sec:categorical-semantics}) is a special case of the spider fusion rule in ZX.

This means that case-theoretic DisCoCat derivations can, in principle, be compiled into ZX circuits and executed on quantum hardware—a connection already exploited by the lambeq quantum NLP pipeline [@lorenz2023lambeq].

## TQNN-DisCoCat Alignment: Ribbon and Tensor Diagrams

### Common Language: Ribbon and Tensor Diagrams

Both ZX-diagrams and TQNNs are topological string diagrams evaluated by monoidal functors into the category of Hilbert spaces and linear maps. The alignment becomes explicit when stated precisely:

- **For TQNNs**: A 3-dimensional TQFT functor from a cobordism or skein category to **Hilb** assigns to each spin-network/ribbon graph a linear map representing the TQNN computation. The underlying topological skein theory treats network layers as *ribbon graphs* whose evaluation via Reshetikhin–Turaev and Turaev–Viro invariants gives quantum processes implementing computation and error correction [@fields2022tqnn; @fields2025amplituhedra].
- **For ZX**: The standard semantics functor from the free $\dagger$-compact category generated by Z/X spiders, Hadamards, etc. into **FHilb** assigns each ZX-diagram a linear map [@kissinger2020zx].
- **For DisCoCat**: The meaning functor from the pregroup grammar category to **FdVect** assigns to each grammatical derivation a multilinear map computing compositional meaning [@coecke2010mathematical].

Up to choice of labels and normalization, all three are graphical calculi for monoidal categories whose morphisms are quantum (or quantum-like) processes. A layer of a topological quantum flow network can be modeled as a ZX-diagram fragment whose input and output boundary wires are the "feature spaces" (Hilbert spaces) at successive processing steps, while internal spiders encode unitary/non-unitary channels that realize synaptic transformations.

### Neural Flow as Generalized Flow

The *generalized flow* condition used to guarantee deterministic circuit extraction from ZX-diagrams is a graph-theoretic constraint that ensures a well-defined causal ordering of operations [@kissinger2020zx]. This mirrors the requirement in TQNNs that the diagram encode a consistent *execution trace* of a quantum computation. Fields and colleagues make this connection explicit in their TQNN–amplituhedron correspondence:

> "...this formal correspondence is stated by Theorem 2 whose proof draws upon the concept of execution trace for a quantum computation... and thus leads to representing a TQNN in terms of the positive geometries as provided by amplituhedra." [@fields2025amplituhedra]

A topological quantum flow neural network can therefore be regarded as a ZX-style circuit where the graphical calculus is enriched to a 3D TQFT skein theory, but the *abstract type* of object—a topological string diagram with functorial semantics—remains the same.

## Distributional Semantics: Topological Quantum Flow

### Meaning Spaces as Hilbert Spaces

To connect TQNNs and ZX circuits to *distributional semantics*, one reinterprets the amplitudes and correlations in these diagrams as semantic quantities. Recent work on quantum semantic communication provides the theoretical bridge, modeling "meaning spaces" as Hilbert spaces at nodes of a graph with channels as completely positive trace-preserving (CPTP) maps along edges [@khatri2025quantum]:

> "Multi-agent semantic networks are modeled as quantum sheaves, where agents' meaning spaces are Hilbert spaces connected by quantum channels." [@khatri2025quantum]

A *quantum semantic sheaf* over a communication graph $G=(V,E)$ is defined as a triple $(H,F,\rho)$ where each vertex $v$ carries a finite-dimensional Hilbert space $H_v$, edges carry CPTP maps $F_e$, and each vertex has a local density operator $\rho_v$ encoding its "current semantic state." This is precisely a distributional-semantics picture: meanings are modeled as vectors/density operators in high-dimensional spaces, with co-occurrence and context encoded in how these spaces are functorially related across the network.

**Case assignment as quantum measurement.** The connection to case systems becomes concrete when we model case assignment as a *quantum measurement* on the semantic state. Define a set of POVM elements $\{E_{\text{NOM}}, E_{\text{ACC}}, E_{\text{DAT}}, \ldots\}$ with $\sum_c E_c = I$, where each $E_c$ projects onto the subspace of semantic states consistent with case role $c$. The probability of assigning case $c$ to a noun phrase in semantic state $\rho$ is:

$$P(c \mid \rho) = \text{Tr}(E_c \rho) $$ {#eq:eq-8-1}

![Quantum POVM case probabilities: (a) NOM/ACC projectors in a crisp case system showing non-overlapping probability density; (b) Graded case assignment in a proto-role system showing overlapping POVM elements and the resulting interference pattern in the semantic belief space. The probability $P(c \mid \rho)$ quantifies the agent's confidence in a given case assignment, providing a physical grounding for the distributional weights of \autoref{sec:enriched-categories}. Measurement in a rotated basis (different QRF) corresponds to a different alignment system (e.g., transition from ACC to ERG).](output/figures/quantum_povm_probabilities.png){#fig:quantum-povm}

For crisp case systems (NOM/ACC), the POVM elements are orthogonal projectors ($E_c E_{c'} = \delta_{cc'} E_c$), yielding deterministic case assignment. For graded proto-roles (Dowty's [-@dowty1991thematic] agent/patient continuum), the POVM elements overlap, yielding probabilistic case assignment—precisely the quantum generalization of the $[0,1]$-enrichment from \autoref{sec:enriched-categories}. The enriched hom-value $\mathcal{C}(v, c)$ is identified with $P(c \mid \rho_v)$, grounding the abstract enrichment in physical measurement theory. Fluid-S alignment (\autoref{sec:case-systems}) then corresponds to a context-dependent POVM: the measurement basis rotates depending on the volition feature $\theta$, so the same noun phrase has different case probabilities depending on whether the agent is construing the action as volitional or not.

![Active Inference belief trajectories during case-role disambiguation. The agent starts with a uniform prior over possible case frames (NOM-ACC vs. ERG-ABS). As categorical evidence (sensory input) is sampled from the TQNN evaluated diagram, the variational free energy for the incorrect frame rises, while the posterior belief in the correct frame converges to certainty. This visualization demonstrates the dynamic minimization of surprisal governed by the diagrammatic structure of the generative model.](output/figures/active_inference_belief.png){#fig:active-inference-belief}

### Grafting Distributional Semantics onto the TQNN/ZX Architecture

When this sheaf-theoretic semantics is grafted onto the TQNN/ZX architecture, three structural correspondences emerge:

1. **Edges as semantic feature channels**: In a TQNN or ZX-diagram, each wire carries not merely an abstract qubit but a semantic Hilbert space $H_v$ associated with a context, concept, or agent. Amplitudes or density matrices on that wire encode a distribution over semantic features—exactly as word vectors encode distributional meaning in classical compositional distributional semantics.

2. **Nodes as compositional operations**: Spiders/gates in ZX or intertwiners in TQNNs become *semantic composition maps*: they take distributed meanings on input wires and produce new distributed meanings on output wires, analogous to how DisCoCat composes word meanings into phrase/sentence meanings via multilinear maps.

3. **Topological wiring as contextual structure**: The topology of the diagram—the way wires and nodes are connected—encodes which semantic spaces interact and in what causal/structural pattern. This is the semantic analogue of syntactic structure in distributional semantics, realized as a topological quantum circuit.

In this reading, a topological quantum flow neural network becomes a *distributional semantic machine*: a functor that sends a topological diagram (graph of contexts and interactions) to a family of Hilbert spaces and maps where vectors/densities represent distributed meanings and their probabilistic transformations.

## Semantic Transfer: Sheaf-Theoretic Functorial Flow

### Sheaf Cohomology and Semantic Alignment

The sheaf-based framework proves that semantic alignment between agents is governed by cohomology classes of the quantum semantic sheaf; contextuality and entanglement act as resources that remove obstructions to alignment [@khatri2025quantum]:

> "We derive semantic channel capacity when sender and receiver share prior entanglement, proving it strictly exceeds classical capacity. The quantum advantage grows as channel noise increases—precisely when semantic communication most benefits over bit-level transmission." [@khatri2025quantum]

Two further results from this framework are particularly relevant:

- **Contextuality as a semantic resource**: "Quantum contextuality reduces cohomological obstructions to semantic alignment. Contextual correlations act as 'pre-shared semantic resolution,' establishing contextuality as a resource for semantic communication" [@khatri2025quantum].
- **Discord as integrated semantic information**: "Quantum discord equals integrated semantic information, linking quantum correlations to irreducible semantic content and connecting our framework to integrated information theory" [@khatri2025quantum].

These results establish that the topology of the semantic sheaf (and its cohomology) constrains how probabilistic semantic information can be transferred; quantum features (entanglement, contextuality, discord) change these constraints in well-defined ways.

### Topological Circuit as Semantic Sheaf Skeleton

A TQNN/ZX circuit implementing a quantum communication or computation protocol is itself a diagram over which one can define a sheaf of semantic spaces and channels. The underlying graph of the TQNN/ZX diagram serves as the base graph $G=(V,E)$ of the semantic sheaf: vertices inherit meaning spaces $H_v$, edges inherit CPTP maps $F_e$, and the TQFT/ZX functor gives the global linear map representing the protocol. Distributional semantics as diagram evaluation then becomes literal: passing an initial semantic state (distribution over meanings) through the TQNN/ZX diagram yields an output state whose components encode the posterior semantic distributions at boundary wires.

ZX rewrite rules, which change the internal topology of the diagram while preserving its overall semantics as a linear map, correspond to alternative factorizations of the same semantic transformation—different internal "flow architectures" for realizing the same semantic map.

## Case Assignment: Active Inference and Quantum Measurement

### Case Assignment as Quantum Measurement

The active inference model of case reasoning (\autoref{sec:cognitive-integration}) acquires a new dimension in this quantum topological setting. Case assignment—the cognitive process of determining *who does what to whom*—can be modeled as a quantum measurement process on a holographic screen, with the following correspondences:

| Classical Case Assignment | Quantum Topological Model |
| :--- | :--- |
| Case role (NOM, ACC, ...) | Pointer state selected by QRF |
| Case frame (alignment system) | Quantum reference frame |
| Relational structure of event | Spin-network topology |
| Free-energy minimization | TQFT evaluation of diagram |
| Prediction-error (P600/N400) | Symmetry-breaking on holographic screen |

### From Predictive Processing to Topological Flow

In the predictive processing account, a cognitive agent maintains a generative model that predicts the relational structure of incoming linguistic material. When this model is realized as a TQNN, prediction becomes evaluation of the topological diagram; prediction error becomes the discrepancy between the predicted TQFT evaluation and the observed data; and belief updating becomes modification of the spin-network's edge labels (representation labels) and vertex intertwiners.

The topological character of this computation confers significant advantages for active inference on case structure: topological invariants are robust to continuous deformation, so the generative model's predictions are stable under small perturbations of the input—a desirable property for language understanding in noisy environments.

### Quantum Advantage in Semantic Communication

The sheaf-theoretic results of Khatri et al. [-@khatri2025quantum] suggest that quantum features provide genuine advantages for semantic communication—not merely computational speedup, but qualitative enhancements in semantic alignment. If case-marked relational structure is communicated between agents via quantum channels, entanglement provides additional semantic capacity, contextuality removes alignment obstructions, and discord captures irreducible semantic content. These are not abstract possibilities but operational consequences of the mathematical framework developed across this review. Recent work by Sherborne et al. [-@sherborne2025paramqnlp] demonstrates this concretely: DisCoCirc string diagrams that represent discourse-level semantics (including case role assignments across sentences) can be *automatically* compiled into parameterized quantum circuits, closing the loop from linguistic case structure through categorical formalism to quantum computation.
