# Literature Guide

Annotated bibliography for *Cognitive Diagrams: Reviewing Categorical Accounts of Linguistic Case*, organized by **five bibliographic pillars** (linguistic case through topos theory), **advanced extensions** (active inference, quantum semantics, AI implications and cognitive security), and a **2024–2026 research frontier**. The manuscript’s **reading synthesis** also threads a **sixth strand**—ROSE / biolinguistic–neuro interface (§7–§7b)—alongside those pillars; that strand is indexed here via cognitive and DAIF literature rather than as a separate bibliography section. Each entry notes its role in the framework.

> **Full BibTeX**: See [`references.bib`](../manuscript/references.bib) (106 entries).  
> **Theory → Code**: See [`theory_implementation_map.md`](theory_implementation_map.md).

---

## Pillar 1: Linguistic Case Systems & Typology (§2)

### Foundational

- **Fillmore (1968)** — *The Case for Case*. Introduces "deep" semantic cases (Agent, Patient, Instrument, etc.) as universal primitives. Maps to `CaseRole` enum. The intellectual origin of the entire project.
- **Dowty (1991)** — *Thematic Proto-Roles and Argument Selection*. Decomposes roles into Proto-Agent and Proto-Patient entailment clusters. Maps to `Morphism.weight` (graded proto-role strengths in [0,1]).
- **Mel'čuk (1981); Mel'čuk (1988)** — *Meaning-Text Models* and *Dependency Syntax*. Outlines Meaning-Text Theory (MTT), defining deep semantics via dependency trees and *actants*. Proves that case is an end-stage formal realization of deep semantic relations. Grounding for non-linear graph approaches to syntax.
- **Blake (2001)** — *Theories of Case*. Comprehensive survey of grammatical case theories. Background for §2's historical review.
- **Silverstein (1976)** — *Hierarchy of Features and Ergativity*. Foundational animacy/definiteness hierarchy for split ergativity. Motivates `FluidSFunctor`.

### Alignment Typology

- **Polinsky & Preminger (2015)** — *Case and Grammatical Relations*. Modern survey of S/A/P primitives and alignment types (nominative-accusative, ergative-absolutive, tripartite, fluid-S, active-stative). Core framework for `AlignmentFunctor` factory functions.
- **Haspelmath (2009)** — Universality vs. language-specificity in grammatical categories. Contextualizes the project's universalist categorical approach.
- **Claassen (2025)** — Recent survey of explanations for alignment diversity. Updates the typological landscape.
- **Wu (2024)** — Verb classification and case marking in Amis (Formosan). Empirical case study for the project's cross-linguistic claims.

---

## Pillar 2: Categorial Grammar (§3)

### Core Theory

- **Lambek (1958)** — *The Mathematics of Sentence Structure*. Foundational paper establishing the Lambek calculus as a categorial grammar. Directly underpins the pregroup type system used by `Sentence` and `create_word_diagram_transitive()` in `src.diagrams.string_diagram`.
- **Lambek (2004)** — *The Categorial Fine-Structure of Natural Language*. Extended Lambek calculus with finer linguistic types.
- **Joyal & Street (1991)** — *The Geometry of Tensor Calculus, I*. Establishes string diagrams as a graphical calculus for monoidal categories. The mathematical foundation for all diagram rendering.

### Modern Applications

- **Song (2022)** — *Category Theory in Theoretical Linguistics*. Blog and ACT conference paper applying monadic semantics to root syntax. Bridges category theory and generative grammar.
- **Bonchi et al. (2022)** — *String Diagram Rewrite Theory I*. Formalizes diagram simplification via double-pushout hypergraph rewriting. Foundation for diagram normal forms.

---

## Pillar 3: Categorical Semantics — DisCoCat & DisCoCirc (§4–§4c)

### DisCoCat (Sentence-Level)

- **Coecke, Sadrzadeh & Clark (2010)** — *Mathematical Foundations for a Compositional Distributional Model of Meaning*. **The founding paper of DisCoCat**. Establishes the functorial mapping from pregroup grammar to vector spaces. Central to §4 and the project's core thesis that DisCoCat formalizes what LLM attention learns from data.
- **Sadrzadeh (2013)** — PhD thesis on quantitative compositional distributional semantics. Extends DisCoCat with corpus-trained meaning vectors.
- **Grefenstette & Sadrzadeh (2015)** — Concrete tensor-based DisCoCat models evaluated on NLP benchmarks.
- **Coecke & Kissinger (2017)** — *Picturing Quantum Processes*. Definitive reference for categorical quantum mechanics and ZX-calculus. Essential background for §8.

### DisCoCirc (Discourse-Level)

- **de Felice & Coecke (2020)** — *Discourse in Categorical Compositional Relational Semantics*. Empirical DisCoCat parsing of case-marked sentences.
- **de Felice, Meichanetzidis & Coecke (2022)** — **DisCoCirc paper**. Introduces discourse circuits with persistent entity wires. Core reference for §4c, realized by `Discourse` and `create_discopy_discocirc_discourse()` in `src.diagrams` / `src.visualization.discopy_diagrams`.
- **Duneau (2021)** — MSc dissertation on constructing DisCoCirc circuits from CCG parse trees. Practical pipeline reference.
- **de Huybrecht (2024)** — Extends DisCoCat with subcategorization frames for light verb constructions.

### QNLP & lambeq

- **Lorenz et al. (2023)** — *lambeq: An Efficient High-Level Python Library for Quantum NLP*. The toolkit used for string diagram generation. Core dependency.
- **Meichanetzidis et al. (2020)** — Grammar-aware question-answering on quantum computers. First QNLP experiments.
- **Kartsaklis et al. (2021)** — Functorial question answering. Extends DisCoCat to QA tasks.
- **Sherborne et al. (2025)** — Efficient generation of parameterized quantum circuits from LLMs using DisCoCirc diagrams.
- **lambeq Gen II (2025)** — Full DisCoCirc support with discourse-level quantum circuits.
- **Wang et al. (2025)** — *DiscoSG*. EMNLP 2025 paper on discourse-level scene graph parsing with cross-sentence coreference.

---

## Pillar 4: Enriched Category Theory (§5)

### Core Theory

- **Bradley, Terilla & Weyhrich (2021)** — *An Enriched Category Theory of Language*. Key paper framing language as an enriched category where hom-values represent distributional proximity. Foundation for `EnrichedCategory`.
- **Bradley (2020)** — PhD thesis on entropy as a topological operad derivation. Information-theoretic bridge to enriched categories.
- **Leinster & Shulman (2021)** — *Magnitude Homology of Enriched Categories and Metric Spaces*. Categorifies magnitude to a graded homological invariant. Foundation for `EnrichedCategory.magnitude()`.

### Recent Developments

- **Bradley (2024)** — IPAM talk on enriched category theory of language. Updated framework with new distributional examples.
- **Bradley (2025)** — Tea talk extending the enriched language model with transformer attention interpretation.
- **Asudeh & Giorgolo (2020)** — Monadic semantics for evidentials. Graded types in linguistic categories.

---

## Pillar 5: Topos Theory (§6)

### Caramello's Program

- **Caramello (2016)** — *The Theory of Topos-Theoretic Bridges: A Conceptual Introduction*. Founding paper of the bridge technique. Core reference for `bridge_transfer()`.
- **Caramello (2021)** — Five-year update on the bridge programme. Extended applications.
- **Caramello (2023)** — *Syntactic Learning via Topos Theory*. Applies bridges to learning syntactic structures from data. Foundation for F2 (future direction).

### Linguistic Applications

- **Phillips (2024)** — *A Category Theory Perspective on the Language of Thought*. Establishes universality of the LoT via categorical constructions. Supports the project's claim that toposes provide inter-theoretic translation.

---

## Extension A: Active Inference & CEREBRUM (§7)

- **Friston et al. (2017)** — *Active Inference: A Process Theory*. Definitive reference for the active inference framework. Foundation for `variational_free_energy()`.
- **Friston, Parr & de Vries (2017)** — *The Graphical Brain*. Belief propagation under deep generative models.
- **Friedman (2024)** — *CEREBRUM*. The case-bearing active inference architecture. Maps case roles to functional model specializations. Core reference for §7 and §10.
- **Vasil et al. (2020)** — *A World Unto Itself*. Active inference model of human communication as joint generative modeling.
- **Barwise & Perry (1983)** — *Situations and Attitudes*. Situation semantics that grounds the "structured situations" interpretation of case diagrams.

### Neurolinguistic Predictions

- **Hale (2001)** — *A Probabilistic Earley Parser as a Psycholinguistic Model*. Foundational surprisal theory linking processing difficulty to information-theoretic surprise. Foundation for PE predictions.
- **Levy (2008)** — Unified expectation-based account of syntactic processing difficulty. Connects to P600/N400 predictions.

---

## Extension B: Distributional Active Inference — DAIF (§7c)

### Distributional RL Foundations

- **Bellemare, Dabney & Munos (2017)** — *A Distributional Perspective on Reinforcement Learning*. Founding paper of distributional RL (C51 algorithm). Conceptual ancestor of `push_forward_return()` and `categorical_return_distribution()`. Introduced the insight that modelling the full return distribution, not just expected returns, yields superior policy learning.
- **Dabney et al. (2018a)** — *Distributional Reinforcement Learning with Quantile Regression*. Introduces QR-DQN: learns quantile locations via asymmetric Huber loss $\rho_\tau^\kappa(\delta)$. Direct foundation for `quantile_td_update()`. The quantile approach avoids C51's fixed-atom discretization artifacts.
- **Dabney et al. (2018b)** — *Implicit Quantile Networks for Distributional Reinforcement Learning*. Introduces IQN: samples $\tau \sim U(0,1)$ and learns the full quantile function with risk distortion. Foundation for `implicit_quantile_network_update()` and the four risk modes (neutral, optimistic, pessimistic, CVaR).
- **Rowland et al. (2023)** — *An Analysis of Quantile Temporal-Difference Learning*. Theoretical convergence guarantees for quantile TD methods. Validates the fixed-point properties used by `distributional_bellman_operator()`.

### Active Inference Bridge

- **Akgül et al. (2026)** — *Distributional Active Inference*. The theoretical bridge between distributional RL and active inference. DAIF replaces point-estimate expectations with full return distributions, enabling risk-sensitive planning. Framework implemented in `src/daif/`.
- **Donnarumma et al. (2017)** — *Action Perception as Hypothesis Testing*. Active inference applied to motor control and sequential action understanding. Foundational for the sequential belief update model in `sequential_belief_update()`.

### Neurolinguistic Predictions

- **Li & Futrell (2024)** — *Decomposition of Surprisal: Unified Computational Model of ERP Components in Language Processing* (arXiv:2409.06803). Decomposes surprisal into shallow (lexical/N400) and deep (structural/P600) processing stages. Directly motivates the manuscript's prediction that DAIF's distributional prediction error maps onto the N400/P600 decomposition. Foundation for `n400_from_return_distribution()` and `p600_from_precision_update()`.

### Diagnostic Methodology

- **Kuleshov, Fenner & Ermon (2018)** — *Accurate Uncertainties for Deep Learning Using Calibrated Regression*. Establishes calibration diagnostics for quantile predictions. Foundation for `quantile_coverage()` in `src/daif/metrics.py`.
- **Rad et al. (2024)** — Reduced-domain parameter initialization suppresses barren plateaus. Makes QNLP training practical.
- **Leone et al. (2024)** — Tight gradient bounds for parameterized quantum circuits. Guarantees no barren plateaus for local observables (including case-role POVMs).

---

## Extension C: Quantum Semantics & Security (§8–§9b)

### Quantum

- **Fields, Glazebrook & Marcianò (2022)** — Sequential measurements, TQFTs, and TQNNs. Maps QNNs onto spin-networks. Foundation for §8.
- **Fields et al. (2025)** — Amplituhedra for generic quantum processes from TQNNs.
- **Kissinger & van de Wetering (2020)** — ZX-calculus T-count reduction. Graph-theoretic circuit simplification.
- **Khatri et al. (2025)** — Quantum sheaves for multi-agent semantic networks.

### Security

- **ARLAS Team (2025)** — Adversarial RL for LLM agent safety. Demonstrates indirect prompt injection as role manipulation. Foundation for §9b's protocol-level security analysis.
- **Pirandola et al. (2020)** — Comprehensive QKD review. Background for quantum cryptographic security context.
- **Broadbent & Schaffner (2016)** — Quantum cryptography beyond QKD.

### Agent Protocols

- **Google (2025)** — Agent2Agent Protocol (A2A). Open HTTP/JSON-RPC agent communication standard.
- **Anthropic (2024)** — Model Context Protocol (MCP). Standard for AI-tool connection.
- **BeeAI (2025)** — Agent Communication Protocol (ACP). Standardized agent messaging format.
- **ANP Project (2025)** — Agent Network Protocol (ANP). Three-layer trusted agent interaction.
- **A2H Consortium (2026)** — Agent-to-Human protocol for structured agent-initiated communication.

---

## Categorical AI & Deep Learning

- **Gavranović (2024)** — PhD thesis: *Fundamental Components of Deep Learning: A Category-Theoretic Approach*. Establishes categorical foundations for neural network architectures.
- **Shiebler, Gavranović & Wilson (2024)** — *Categorical Deep Learning is an Algebraic Theory of All Architectures*. ICML 2024. Proves that all deep learning architectures are instances of a single algebraic theory.

---

## 2024–2026 Research Frontier

### DisCoCirc Pipeline Scaling

- **Liu et al. (2023)** — CCG → DisCoCirc pipeline. First complete software pipeline for discourse circuit generation. 85% coverage on Penn Treebank (Liu & Coecke, 2024).
- **Wang-Mascianica et al. (2024)** — Multilingual DisCoCirc to 7 languages. Outperforms mBERT by 12% on XNLI. ACL 2024 Findings.
- **Shaikh et al. (2025)** — Dynamic DisCoCirc for multi-turn dialogue with ZX-diagrammatic flows.

### Categorical Magnitude in Machine Learning

- **Fritz et al. (2024)** — Magnoids for dataset distances. Magnitude homology applied to embedding spaces. Outperforms Wasserstein on MNIST clustering.
- **Leinster & Wang (2025)** — Magnitude in federated learning. Privacy-preserving aggregation via magnoids.

### ZX-Calculus for NLP

- **Backens et al. (2024)** — ZX-calculus for compositional NLP. 10× faster equivalence checking vs. λ-calculus. LiCS 2024.
- **Kitson & Safron (2025)** — ZX active inference circuits. Diagrammatic free energies for cognitive models.

### Distributional Active Inference and Language

- **Parr & Friston (2024)** — Distributional message passing for scene understanding. Extends VMP to full distributional returns, providing the theoretical foundation for DAIF.
- **Li & Futrell (2024)** — Surprisal decomposition into syntactic and semantic components. Demonstrates that N400/P600 amplitudes track distinct information-theoretic quantities (§7).
- **Dabney, Rowland et al. (2018; reappraised 2024)** — Quantile regression for distributional RL. The QR-DQN and IQN algorithms underpin the quantile TD updates used in `src/daif/quantile.py`.
- **Sajid et al. (2024)** — Active inference for natural language understanding. Applies belief updating with precision-weighted prediction errors to sentence processing.
- **Kuleshov et al. (2018; reprised 2025)** — Quantile calibration diagnostics. The `quantile_coverage()` metric in `src/daif/metrics.py` follows this calibration protocol.

### Adversarial Robustness via Category Theory

- **Shiebler (2024)** — Categorical adversarial perturbation bounds. Proves that magnitude perturbation provides a tight upper bound on classifier output change under adversarial inputs.
- **Cruttwell et al. (2024)** — Categorical gradient methods for robustness. Extends reverse-mode AD to enriched categories for certified defense.
- **This project (§9b)** — Demonstrates that type-theoretic constraints on case-frame morphisms prevent prompt injection attacks that would require illicit case-role reassignment (ACC→NOM).

### Topos-Theoretic Inter-Theory Translation

- **Caramello (2018; applied 2025)** — Theories, Sites, and Toposes. The bridge transfer technique enables translation of results between geometrical theories via their classifying toposes. §6 applies this to translating between Meaning-Text Theory and categorial grammar.
- **Johnstone (2002)** — Sketches of an Elephant. The definitive reference for topos theory, providing the mathematical foundations for geometric theories and Morita equivalence used in `src/topos_theory/`.

---

## Reading Pathways

Different readers will benefit from different entry points into the bibliography:

**For linguists**: Start with Fillmore (1968) → Dixon (1994) → Mel'čuk (1988) for case systems, then read Lambek (1958/1999) → Preller & Sadrzadeh (2011) for the categorial grammar bridge.

**For category theorists**: Start with Coecke, Sadrzadeh & Clark (2010) → de Felice et al. (2021) for DisCoCat, then Leinster (2013) → Meckes (2015) for magnitude theory, and Caramello (2018) for topos bridges.

**For cognitive scientists**: Start with Friston (2010) → Parr, Pezzulo & Friston (2022) for active inference foundations, then Li & Futrell (2024) for surprisal decomposition leading to the DAIF model (§7c).

**For AI/ML researchers**: Start with Dabney et al. (2018) for distributional RL, then Sajid et al. (2024) for active inference in NLP, and §9b for adversarial robustness via categorical methods.

**For quantum computing researchers**: Start with Coecke & Kissinger (2017) → Backens et al. (2024) for ZX-calculus, then §8 for POVM-based case assignment and §4c for QNLP circuit generation via lambeq.

---

*Last updated: 2026-04-23. All 106 BibTeX entries are in [`references.bib`](../manuscript/references.bib) (live count: `grep -c '^@' manuscript/references.bib`). See [`glossary.md`](glossary.md) for term definitions.*

