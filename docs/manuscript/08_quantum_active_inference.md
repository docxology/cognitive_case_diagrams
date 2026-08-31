# Topological Quantum Neural Networks and ZX-Calculus: From Spin-Networks to Categorical Case Diagrams {#sec:quantum-active-inference}

**Where we are in the argument.** The preceding sections have established that categorical string diagrams—from DisCoCat's pregroup derivations (\autoref{sec:categorical-semantics}) through enriched hom-values (\autoref{sec:enriched-categories}) to topos-theoretic transfer (\autoref{sec:topos-theory})—provide a unified diagrammatic language for case-theoretic reasoning (**theoretical synthesis**). This section extends the framework with a literature bridge to topological quantum neural networks (TQNNs), the ZX-calculus, and sheaf-theoretic quantum semantic communication (**theoretical bridge to prior art**).

The `src/quantum/quantum_case.py` module implements a concrete POVM-based measurement model for case roles (tested in the project suite; see \autoref{sec:quantum-semantics}). The broader TQNN, ZX-rewrite, and lambeq compilation claims remain literature connections and proposed extensions rather than full local implementations. The central observation is that the same monoidal-categorical architecture underlies both classical DisCoCat diagrams and quantum processes.

**Position relative to prior work.** Each ingredient we draw on has independent prior art. TQNNs as spin-network computations are due to Fields, Marcianò, and collaborators [@fields2022tqnn; @fields2025amplituhedra]; the ZX-calculus and its circuit-extraction theory are due to Kissinger, van de Wetering, Coecke, and the Picturing-Quantum-Processes school [@kissinger2020zx; @coeckekissinger2017]; and quantum natural language processing on present-day hardware has been demonstrated by the lambeq pipeline [@lorenz2021lambeq] and the Quantinuum quantum-NLP programme. What is *new* in this section is none of those constructions individually; rather it is the **identification** that the *same* monoidal-functorial scaffolding can carry a *case-theoretic* payload — in particular, that the POVM family $\{E_c\}$ of \autoref{sec:quantum-semantics} can be read both as a Born-rule case-assignment device and as the pointer-basis selected by a quantum reference frame in a TQNN — and the consequent claim that case assignment, ZX-rewrite verification, and DAIF-style distributional inference (\autoref{sec:daif-results}) are three views of one diagrammatic process. This is a *bridge* result, not a hardware claim: nothing in this section asserts that fault-tolerant quantum hardware is required, and the \autoref{sec:daif-results} distributional pipeline runs entirely on classical numerics.

## QNNs as Spin-Networks

### TQFT as the Forward Pass: Reshetikhin–Turaev Invariants Compute Network Amplitudes

Marcianò, Fields, and Glazebrook show that quantum neural networks (QNNs) admit a topological reformulation using spin-networks [@fields2022tqnn]. Any QNN layer can be represented as a graph whose edges carry representation labels (spins) and whose vertices carry intertwiners—precisely the data defining a spin-network in a 3-dimensional topological quantum field theory (TQFT):

> "Quantum Neural Networks (QNNs) can be mapped onto spin-networks, with the consequence that the level of analysis of their operation can be carried out on the side of Topological Quantum Field Theory (TQFT)." [@fields2022tqnn]

This reformulation has three structural consequences. First, the network becomes a topological diagram—spin-network or ribbon graph—evaluated by a continuous TQFT functor; edges encode information flow and nodes encode transformation. Second, the TQFT evaluation assigns boundary Hilbert spaces to the diagram via the Reshetikhin–Turaev and Turaev–Viro invariants, playing the role of the neural forward pass: quantum amplitudes propagate through the topological structure. Third, information flow is encoded in the topology of the wiring rather than in any fixed geometric embedding, giving the architecture inherent robustness to continuous deformation [@fields2023tensor].

### TQNNs Are Universal

Fields and collaborators further demonstrate that TQNNs are universal quantum computers by identifying the Reshetikhin–Turaev invariant of a TQNN with a Turaev–Viro quantum error-correcting code:

> "TQNNs enable universal quantum computation, using the Reshetikhin-Turaev and Turaev-Viro models to show how TQNNs implement quantum error-correcting codes." [@fields2025amplituhedra]

The universality result is established via the concept of an *execution trace* for a quantum computation, leading to the representation of TQNNs in terms of the positive geometries provided by amplituhedra—a deep connection between quantum computation, scattering amplitudes, and topological combinatorics.

### QRFs Select the Measurement Basis

Fields and Glazebrook's work on quantum reference frames (QRFs) and holographic screens provides additional algebraic structure [@fields2021qrf]. A holographic screen—the information boundary between two interacting quantum systems—carries a qubit array encoding their interaction. The key insight is that QRFs deployed to identify systems and select pointer states induce decoherence, breaking the symmetry of the holographic encoding in an observer-relative way. This symmetry-breaking is precisely the mechanism by which a TQNN "observes" its input: the choice of QRF determines the basis in which the spin-network is evaluated.

For case-theoretic reasoning, this connects to the grammatical observer problem: a parser or comprehender selecting a case-assignment frame for a sentence is analogous to deploying a QRF that fixes the pointer basis for a quantum measurement on a holographic screen.

## ZX-Calculus: Topological String Diagrams Where Graph Rewrites Are Quantum Proofs

### String Diagrams for Quantum Processes

The ZX-calculus provides a diagrammatic language for quantum circuits, representing them as string diagrams in a symmetric monoidal category of finite-dimensional Hilbert spaces and linear maps [@kissinger2020zx]:

> "The ZX-calculus is a graphical language for reasoning about quantum computations and circuits... it can represent any linear map, and can be considered a diagrammatically complete generalization of the usual circuit representation." [@coeckekissinger2017]

Three structural features connect ZX to case-theoretic diagrams:

- **Diagrams as morphisms**: ZX-diagrams are string diagrams in a $\dagger$-compact closed category. Wires represent objects (qubits), spiders and boxes represent morphisms, and composition/tensor product correspond to vertical/horizontal concatenation. Only topology matters, not geometry.
- **Deterministic circuit extraction via generalized flow**: Kissinger and van de Wetering show that quantum circuits map to ZX-diagrams, undergo graph-theoretic rewriting, and extract as optimized circuits—with topological abstraction preserving the invariants needed for optimization [@kissinger2020zx].
- **Category-theoretic semantics**: A ZX-diagram's semantics are determined entirely by how components are wired—the same compositional principle underlying DisCoCat and the case categories of \autoref{sec:case-systems}.

### Pregroup Cups and ZX Spiders Are Instances of the Same Compact-Closed Morphism

The structural parallel between pregroup grammar diagrams and ZX-diagrams is not accidental. Both are instances of the same mathematical object: morphisms in a compact closed monoidal category with functorial semantics into Hilbert spaces. In DisCoCat, the functor assigns to each grammatical type a vector space and to each derivation a linear map computing sentence meaning [@coecke2010mathematical]. In ZX, the standard semantics functor assigns to each spider/Hadamard configuration a linear map in **FHilb**. The shared categorical architecture means:

1. **Pregroup contractions (cups) and ZX spiders** are both instances of the same algebraic operation: evaluation morphisms in a compact closed category.
2. **DisCoCat normal forms** and **ZX simplifications** are both applications of the same rewriting theory: equational reasoning modulo the axioms of a compact closed category.
3. **The snake equation** (Cap $\circ$ Cup = identity) that grounds all pregroup type reductions (\autoref{sec:categorical-semantics}) is a special case of the spider fusion rule in ZX.

This means that case-theoretic DisCoCat derivations can, in principle, be compiled into ZX circuits and executed on quantum hardware—a connection already exploited by the lambeq quantum NLP pipeline [@lorenz2021lambeq].

## One Diagram, Three Interpretations: TQNN, ZX, and DisCoCat Share a Monoidal Functor

### A Common Language of Ribbon and Tensor Diagrams

Both ZX-diagrams and TQNNs are topological string diagrams evaluated by monoidal functors into the category of Hilbert spaces and linear maps. The alignment becomes explicit when stated precisely:

- **For TQNNs**: A 3-dimensional TQFT functor from a cobordism or skein category to **Hilb** assigns to each spin-network/ribbon graph a linear map representing the TQNN computation. The underlying topological skein theory treats network layers as *ribbon graphs* whose evaluation via Reshetikhin–Turaev and Turaev–Viro invariants gives quantum processes implementing computation and error correction [@fields2022tqnn; @fields2025amplituhedra].
- **For ZX**: The standard semantics functor from the free $\dagger$-compact category generated by Z/X spiders, Hadamards, etc. into **FHilb** assigns each ZX-diagram a linear map [@kissinger2020zx].
- **For DisCoCat**: The meaning functor from the pregroup grammar category to **FdVect** assigns to each grammatical derivation a multilinear map computing compositional meaning [@coecke2010mathematical].

Up to choice of labels and normalization, all three are graphical calculi for monoidal categories whose morphisms are quantum (or quantum-like) processes. A layer of a topological quantum flow network can be modeled as a ZX-diagram fragment whose input and output boundary wires are the "feature spaces" (Hilbert spaces) at successive processing steps, while internal spiders encode unitary/non-unitary channels that realize synaptic transformations.

### Generalized Flow Guarantees Causal Order

The *generalized flow* condition used to guarantee deterministic circuit extraction from ZX-diagrams is a graph-theoretic constraint that ensures a well-defined causal ordering of operations [@kissinger2020zx]. This mirrors the requirement in TQNNs that the diagram encode a consistent *execution trace* of a quantum computation. Fields and colleagues make this connection explicit in their TQNN–amplituhedron correspondence:

> "...this formal correspondence is stated by Theorem 2 whose proof draws upon the concept of execution trace for a quantum computation... and thus leads to representing a TQNN in terms of the positive geometries as provided by amplituhedra." [@fields2025amplituhedra]

A topological quantum flow neural network can therefore be regarded as a ZX-style circuit where the graphical calculus is enriched to a 3D TQFT skein theory, but the *abstract type* of object—a topological string diagram with functorial semantics—remains the same.
