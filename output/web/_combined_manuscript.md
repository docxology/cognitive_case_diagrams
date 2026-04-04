# Abstract

This paper builds on linguistic case theory and cognitive science and provides a unified algebraic framework for cognitive systems modeling centered on the *case diagram*. Formally, case systems are modeled as categories whose objects are case roles and whose morphisms are grammatical relations; alignment typologies (nominative-accusative, ergative-absolutive, active-stative, tripartite, and fluid-S) are captured as structure-preserving functors between these categories. Within this framework, sentence structure becomes a compact-closed string diagram—computable via DisCoCat and, at the discourse level, DisCoCirc [@coecke2010mathematical; @defelice2022discocirc]—that functions not merely as descriptive notation but as an executable witness of grammaticality grounded in situated reasoning. Historically, the analysis traces from Pāṇinian *kāraka* theory [@kak1987paninian] through Jakobson's feature matrices [@jakobson1958morphologic] and Fillmore's deep cases [@fillmore1968case] to Dowty's graded proto-roles [@dowty1991thematic], showing how morphosyntactic inflection supplies the structural skeleton for relational differentiation in natural and designed languages.

Equipping case categories with proto-role satisfaction yields quantitative complexity measures with psycholinguistic interpretations; combined with active inference, the framework *predicts* electrophysiological signatures (P600/N400) whose amplitudes scale with enriched morphism precision in the idealized models of the cognitive-integration and DAIF sections below, in line with surprisal-decomposition accounts [@li2023decomposition; @li2024shallow]. For artificial agents, the same typing discipline *suggests* treating certain prompt-injection patterns as failed derivations—illicit case-role reassignment—when interaction graphs are explicitly stratified by role; compositional multi-agent protocols are *outlined* under NOM–ACC–INS-style constraints in the categorical-AI section. The cognitive case diagram thus integrates linguistic structure, logic, embodied cognition, and machine intelligence in one computationally tractable diagrammatic language. **Code and tests:** open-source implementation with automated test suite [@cognitive_case_diagrams2026code].



---



# Introduction: Case Diagrams and Categorical Linguistics {#sec:introduction}

## Case as Relational Algebra: From Surface Inflection to Categorical Morphism

Every natural language must solve the same fundamental problem: encoding *who does what to whom, with what, where, and why*. Morphologically rich languages encode these situational relations overtly via distinct word modifications marking the agent, patient, instrument, or location. Languages like Mandarin or English achieve the same end through strict word order and adpositions. Beneath this surface variation lies a universal computational challenge: a cognitive agent must dynamically assemble and assign *structured roles* to the participants of every encountered scenario, predicting relationships and mapping them against the constraints of a conceptual space.

Today, this same universal computational challenge lies at the heart of the artificial intelligence alignment crisis. The inability of contemporary Large Language Models (LLMs) to securely distinguish *who is allowed to do what to whom* within a text block—allowing passive data to masquerade as commanding instructions—is the root cause of prompt injection and agentic hijacking. 

This universality suggests that linguistic *case* is not a morphosyntactic accident, but the reflection of a deeper, embodied cognitive architecture. The lineage of this hypothesis is long: from Pāṇini's ancient *kāraka* theory (which abstracted nominal roles from root actions), through Jakobson's structuralist feature matrices and Fillmore's [-@fillmore1968case] establishment of a universal inventory of *deep cases* (Agent, Patient, Instrument), to Mel’čuk’s Meaning-Text Theory [-@melcuk1988dependency], which formally treats cases as relational networks mapping surface form to deep semantic structure. Modern typological work by Polinsky and Preminger [-@polinsky2015case], Blake [-@blake2001grammatical], and Haspelmath [-@haspelmath2009universality] confirms that cross-linguistic variation is tightly bounded into a small number of *alignment types*, related by systematic transformations.

This review demonstrates that **category theory** supplies the precise mathematical language to formalize this structure, yielding immense defensive value for AI. Furthermore, **commutative diagrams** function not merely as convenient white-board notation, but as *cognitively privileged, embodied representations*. By constraining relational algebras to a two-dimensional graph, these diagrams directly recruit spatial reasoning, providing structural boundary enforcement and inferential free rides unavailable to linear, un-typed sentential encodings.

## Why Diagrams Earn Free Rides: Spatial Constraints as Inferential Engines

The cognitive science of diagrammatic reasoning provides a strong empirical foundation for this claim. To cast a problem onto a two-dimensional visual topology is to recruit the nervous system’s innate, ancient capacity for spatial navigation. Larkin and Simon [-@larkin1987diagram] demonstrated that diagrams can be computationally superior to sentential representations: their planar constraint enables efficient perceptual grouping that would otherwise require painstaking, explicit logical deduction. Shimojima [-@shimojima1996reasoning] refined this with the concept of *free ride inferences*—conclusions that "fall out" automatically from the geometric constraints of a sketch without syntactic manipulation.

In the context of case theory, commutative diagrams offer exactly these embodied advantages. A commutative triangle expressing that morphism $g \circ f$ equals morphism $h$ simultaneously encodes:

1. The compositional structure of the relation (two steps factor through an intermediate case role).
2. The *commutativity constraint* (the direct and indirect visual routes yield the same mathematical result).
3. The full relational context (the entire shape of the scenario is apprehensible in a single perceptual glance).

This is exactly the kind of gestalt understanding that linear notation obscures. \autoref{fig:case-minimal} lays out a concrete instance. Let $f\colon\text{NOM}\to\text{INS}$ be \emph{uses} ($w=0.9$), $g\colon\text{INS}\to\text{ACC}$ be \emph{applied\_to} ($w=0.7$), and $h\colon\text{NOM}\to\text{ACC}$ be \emph{acts\_on} with $h=g\circ f$ and $w(h)=0.63=w(g)\cdot w(f)$ as in \autoref{eq:eq-2-1}. The single morphism $h$ is drawn twice in the diagram: once as the direct arrow $\text{NOM}\to\text{ACC}$ and once as the composite path through $\text{INS}$; commutativity identifies those routes—they are not two independent relations. A separate licensed arrow $\text{NOM}\to\text{VOC}$ (\emph{addresses}, $w=0.85$) lies outside that triangle. Dashed red arrows depict structurally \emph{prohibited} maps (not elements of any $\operatorname{Mor}(\mathcal{C})$), including $\text{VOC}\to\text{NOM}$ and $\text{ACC}\to\text{NOM}$, for contrast with the solid licensed morphisms. As Giardino [-@giardino2017diagrammatic] emphasizes, mathematical diagrams engage a hybrid mode of reasoning, intimately wedding perceptual pattern-recognition with theoretical knowledge—a mode effortlessly aligned with the predictive processing architecture of active inference [@friston2017active]. The intellectual lineage traces through Peirce's *existential graphs*: his spatial logic system proved that first-order reasoning can be conducted entirely diagrammatically on a "sheet of assertion." Our case diagrams extend this Peircean tradition into relational semantics: inference proceeds not by algebraic churning, but by tracing lines and composing arrows—drawing the contours of thought itself.

![Commutativity in a small case category yields free-ride inference (\autoref{eq:eq-2-1}). Objects: NOM, ACC, INS, VOC. Solid green arrows: licensed morphisms; edge labels use $f,g,h$ on the commuting triangle and weights $w\in[0,1]$. Dashed red: structurally prohibited $\text{VOC}\to\text{NOM}$ and $\text{ACC}\to\text{NOM}$ (not in $\operatorname{Mor}(\mathcal{C})$). Generated by `introductory_case_category()` and `render_case_category`.](output/figures/case_category_minimal.png){#fig:case-minimal}

## Five Converging Linguistic and Mathematical Traditions

The present synthesis draws on five research traditions, each contributing an essential formal ingredient:

### Pillar 1: Case Systems, Alignment Typology, and Structural Admissibility

The empirical foundation comes from linguistic typology. We formalize the case inventory and alignment systems catalogued by Polinsky and Preminger [-@polinsky2015case], Claassen [-@claassen2019alignment], and Wu [-@wu2024amis] as categories with *noun case roles* as objects and grammatical relations as morphisms. Crucially, the categorical framework makes explicit a distinction often implicit in traditional accounts: **structural admissibility**—which morphisms between case roles are *licensed* (structurally well-formed) versus *prohibited* (ill-formed). For example, the morphism NOM→ACC ("agent acts on patient") is universally licensed, while VOC→NOM ("addressee as agent") is structurally inadmissible. This admissibility structure, visualized through solid licensed edges, dashed prohibited edges, and absent transitions in the case category diagram (\autoref{fig:case-minimal}), encodes the combinatorial constraints of argument structure more transparently than any linear notation. Dowty's [-@dowty1991thematic] proto-role theory—which decomposes thematic roles into clusters of entailments rather than discrete atoms—motivates our use of enriched (weighted) morphisms, where the morphism weight quantifies the *degree* of admissibility along a licensed transition. **Synthetic Case-Role Algebra** (introduced in \autoref{sec:case-systems}) extends this line by formalizing proto-roles in a $[0,1]$-enriched monoidal setting, enabling context-sensitive algebraic manipulation of case-role semantics without ad hoc feature bundles.

### Pillar 2: Categorial and Type-Theoretic Grammar

Lambek's [-@lambek1958mathematics] syntactic calculus reformulates grammatical combination as algebraic cancellation in a pregroup, yielding derivations that can be visualized as Joyal and Street's [-@joyalstreet1991geometry] string diagrams. Song [-@song2022act] extends this with monadic semantics for root syntax, showing that category-theoretic structure reaches down to the sublexical level.

### Pillar 3: Categorical Compositional Distributional Semantics (DisCoCat)

Coecke, Sadrzadeh, and Clark's [-@coecke2010mathematical] DisCoCat framework composes distributional word meanings according to syntactic structure using monoidal categories and string diagrams. This framework bridges the two great traditions of linguistic meaning---formal (truth-conditional, compositional) and distributional (context-dependent, statistical)---by using the algebra of compact closed categories to compose vector representations according to type-logical derivations. The resulting categorical semantics provides the *algebraic formalization* of the distributional programme that modern large language models (from Word2Vec [@mikolov2013efficient] through transformer architectures [@vaswani2017attention; @devlin2019bert]) implement empirically, making it possible to analyse both symbolic and neural approaches to language within a single mathematical framework. DisCoCirc [@defelice2020discourse; @defelice2022discocirc] and the lambeq QNLP stack [@lorenz2023lambeq; @quantinuum2025genii] extend this to discourse and circuit compilation; \autoref{sec:discocirc-discourse} gives the discourse-level and Gen II details.

### Pillar 4: Enriched Category Theory and Distributional Measures

Bradley et al.'s [-@fritz2021enriched] enrichment over $[0,1]$ equips hom-sets with distributional proximity measures, supplying the bridge from syntax to statistical semantics. **Categorical magnitude** (scalar ``effective size'' of an enriched category) is the Leinster-style invariant that summarises how much relational structure a case system encodes; Bradley's [-@bradley2021entropy; -@bradley2024ipam] operadic and information-theoretic work complements that picture. Leinster and Shulman [-@leinster2021magnitude] extend magnitude to **magnitude homology**, a graded homological invariant that detects higher-dimensional differences between case systems indistinguishable by scalar magnitude alone.

### Pillar 5: Topos-Theoretic Bridges and Inter-Theoretic Transfer

Caramello's [-@caramello2016bridges; -@caramello2021five; -@caramello2023syntactic] bridge technique uses classifying toposes as transfer points between mathematical theories: when two formalizations are Morita equivalent (or linked by an explicit bridge), **topos-level invariants** proved in one setting carry over without separate proof. Phillips [-@phillips2024lot] strengthens this by showing that the Language of Thought admits universal constructions in a topos, grounding the systematicity of case assignment in the deepest structures of categorical logic.

## Active Inference Closes the Loop

The unifying framework is **active inference** [@friston2017active], which casts cognition as approximate Bayesian inference under a generative model. Case-marked commutative diagrams serve as the structural core of such generative models: each diagram specifies a pattern of expected relational dependencies, and the agent's task in understanding (or producing) a sentence is to minimize surprise relative to this diagrammatic prior. The **CEREBRUM** architecture [@friedman2024cerebrum]---Case-Enabled Reasoning Engine with Bayesian Representations for Unified Modeling---provides a computational instantiation of this framework, with case roles as functional specializations of model components in an active inference cycle.

The situation semantics of Barwise and Perry [-@barwise1983situations] already conceptualized meaning as structured *situations* with typed constituents—an ontology that maps naturally onto the objects and morphisms of our case categories. Active inference adds dynamics: the agent actively samples evidence to confirm or update its case assignments, using diagrammatic structure to guide exploration.

## Roadmap: Navigating the Eleven Principal Contributions

The remainder of the paper develops this synthesis in order: \autoref{sec:case-systems}–\autoref{sec:case-categories} (typology and functorial alignment); \autoref{sec:categorial-grammar}–\autoref{sec:case-type-logic} (pregroup diagrams and case-marked types); \autoref{sec:categorical-semantics} and \autoref{sec:discocat-meaning-functor} (DisCoCat); \autoref{sec:compact-closure-complexity} (compact closure and diagram complexity); \autoref{sec:discocirc-discourse} (discourse and QNLP); \autoref{sec:enriched-categories}–\autoref{sec:magnitude-homology}; \autoref{sec:topos-theory}; \autoref{sec:cognitive-integration}–\autoref{sec:daif-results}; quantum extensions (\autoref{sec:quantum-active-inference}, \autoref{sec:quantum-semantics}); applications (\autoref{sec:ai-implications}, \autoref{sec:cognitive-security}). \autoref{sec:research-questions} maps questions **RQ1**–**RQ11** to sections and contributions **C1**–**C11**. Computational verification is summarized in \autoref{sec:diagrammatic-cognition} with test inventory in \autoref{sec:test-suite-inventory}.

Each subsequent section is self-contained yet cumulative: the reader may enter at any pillar and follow the cross-references forward to the synthesis.



---



# Research Questions and Manuscript Navigation {#sec:research-questions}

This paper addresses eleven core research questions, each developed in specific sections and yielding a principal contribution (**C1**–**C11**, as enumerated in \autoref{sec:conclusion}). The table below provides a navigational overview; the reading guide that follows explains the logical dependencies between questions.

\begingroup
\small

| \# | Research Question | Addressing Sections | C |
|:--:|:----------------------------------------------|:-----|:--:|
| **RQ1** | Can linguistic case systems—across all major typological alignment patterns—be formalized within a single algebraic framework, with roles as objects and grammatical relations as morphisms? | \autoref{sec:case-systems}, \autoref{sec:case-categories} | **C1** |
| **RQ2** | Do string diagrams derived from pregroup type reductions provide a computationally and cognitively superior representation of case derivations compared to linear notation? | \autoref{sec:categorial-grammar}, \autoref{sec:case-type-logic}, \autoref{sec:syntactic-diagrams} | **C2** |
| **RQ3** | Can the DisCoCat meaning functor be extended with case-typed noun spaces to unify formal and distributional semantics—and does this unification generalize to discourse via DisCoCirc? | \autoref{sec:categorical-semantics}, \autoref{sec:discocat-meaning-functor}, \autoref{sec:compact-closure-complexity}, \autoref{sec:discocirc-discourse} | **C3** |
| **RQ4** | Does equipping case categories with $[0,1]$-enriched hom-values yield a principled bridge between symbolic grammar and statistical semantics, and can categorical magnitude serve as a complexity invariant? | \autoref{sec:enriched-categories}, \autoref{sec:magnitude-homology} | **C4** |
| **RQ5** | Can classifying toposes and Morita equivalence (or explicit bridge toposes) scaffold transfer of **topos-expressible invariants** between distinct formalizations of case theory (typological, type-logical, distributional, enriched), when equivalence is exhibited? | \autoref{sec:topos-theory} | **C5** |
| **RQ6** | Are commutative diagrams *cognitively privileged* representations—recruiting spatial reasoning, free-ride inference, and predictive processing—beyond being merely convenient notation? | \autoref{sec:introduction}, \autoref{sec:cognitive-integration} | **C6** |
| **RQ7** | Can the entire categorical framework be computationally verified with real (non-mock) automated tests at ≥90% coverage, confirming that the abstractions are executable? | \autoref{sec:diagrammatic-cognition}, \autoref{sec:daif-results} | **C7** |
| **RQ8** | Do categorical string diagrams extend naturally into quantum generalizations via TQNNs, ZX-calculus, and sheaf-theoretic quantum semantics—and does quantum entanglement provide genuine advantages for semantic communication? | \autoref{sec:quantum-active-inference}, \autoref{sec:quantum-semantics} | **C8** |
| **RQ9** | Can prompt injection attacks be formulated mathematically as illicit cross-category morphisms (type violations), yielding a **decidable** static check **relative to a fixed protocol / interaction category** (compile-time where that grammar is enforced)? | \autoref{sec:cognitive-security} | **C9** |
| **RQ10** | Does integrating enriched category theory with active inference generate *falsifiable* neurolinguistic predictions (P600/N400 amplitudes scaling with enriched morphism weights)? | \autoref{sec:cognitive-integration}, \autoref{sec:daif-results} | **C10** |
| **RQ11** | Can grammatical case roles (NOM, ACC, INS) rigorously type-check the tensor payloads of multi-agent AI framework protocols (A2A, MCP, ANP) to prevent agentic hijacking? | \autoref{sec:ai-implications} | **C11** |

\endgroup

> **Reading guide.** **RQ1–RQ5** build the mathematical framework cumulatively: each layer depends on the preceding one, from case categories (RQ1) through string diagrams (RQ2), distributional semantics (RQ3), enriched structure (RQ4), to topos-theoretic transfer (RQ5). **RQ6** provides the cognitive science meta-argument that threads through the entire paper, grounding diagrams in spatial reasoning and predictive processing. **RQ7** supplies computational validation of the framework via automated testing. **RQ8–RQ11** extend the framework into four application domains: quantum semantics (RQ8), cognitive security (RQ9), falsifiable neurolinguistic predictions (RQ10), and multi-agent AI protocols (RQ11). The conclusion (\autoref{sec:conclusion}) revisits each question with a summary of results and identifies seven open directions (**F1**–**F7**).



---




# Case Systems: From Pāṇinian Kāraka to Cross-Linguistic Alignment Typology {#sec:case-systems}

## Five Analytical Traditions That Shaped the Modern Theory of Case

### The Pāṇinian Kāraka Framework

The formal study of grammatical case originates with Pāṇini (circa 4th century BCE), whose *Aṣṭādhyāyī*—a grammar of approximately 4,000 rules that predates Euclid—formalized the *kāraka* theory. This framework first classified semantic roles—agent, patient, instrument, and others—as deep relational functions linking verbs to their arguments, abstracting away from surface morphosyntactic inflections. Etymologically meaning "that which brings about" an action, the kāraka system establishes a rigorous mapping from conceptual predication to phonological realization [-@jha2021sanskrit; -@kak1987paninian].

### Jakobson’s Structural Features and the Prague School

This profound semantic foundation lay predominantly dormant until structural linguists resurrected it in the mid-20th century. Roman Jakobson's *Morphologic Inquiry into Slavic Declension* (1958) decomposed grammatical cases into binary distinctive features (e.g., [±directional], [±peripheral]) [-@jakobson1958morphologic]. By treating case oppositions analogously to phonological features, Jakobson shifted the field from Pāṇini's holistic roles to a componential analysis that exposes deep relational hierarchies and markedness. Concurrently, Louis Hjelmslev's *La catégorie des cas* [-@hjelmslev1935categorie] reinforced this functionalist tradition by formalizing case as a purely relational category within a dynamic semiotic network.

### Fillmore’s Deep Case and Generative Roots

Charles Fillmore's seminal "The Case for Case" (1968) built directly upon this structuralist lineage, explicitly translating these concepts into the burgeoning generative linguistics framework. Fillmore proposed *deep cases* (e.g., Agentive, Objective, Dative) as universal semantic primitives underlying surface syntax. Crucially, he argued that verbs assign underlying *case frames* which subsequently generate surface structures [-@fillmore1968case]. This evolution transformed Pāṇini's kāraka into deep relational networks, permanently prioritizing universal semantics over language-specific morphology.

### Mel'čuk's Meaning-Text Theory (MTT)

A distinct but parallel formalization emerged with Aleksandr Žolkovskij and Igor Mel'čuk's Meaning-Text Theory (MTT) [@zolkovskij1965possible; @melcuk1981meaning; @melcuk1988dependency]. Developed initially in Moscow, MTT models natural language as a rigorous, many-to-many correspondence between meanings (deep semantic representations) and texts (surface-phonological representations). The transition from meaning to text unfolds across a multi-level synthesis process: Deep Semantics, Deep-Syntactic, Surface-Syntactic, Morphological, and Phonological. At the deep-syntactic level, meaning is represented via *dependency trees* linking lexical units through dependency relations. The nodes are populated by *actants*—semantic roles closely aligning with thematic grids but strictly language-specific in their surface realization.

Crucially, MTT establishes that grammatical case is not directly semantic, but rather a final surface-morphological phenomenon governed by syntactic linearization and dependency constraints. *Lexical functions* map actants to surface structures, explicitly demonstrating that morphosyntactic inflection serves merely as the end-stage formal realization of deep semantic relations. By monotonically mapping meaning to text via hierarchical dependency graphs, MTT provided an exhaustive synthesis that presages our modern categorical formalizations mapping conceptual structures to syntactic types.

### Dowty’s Proto-Roles and Graded Topologies

Fillmore's deep cases serve as the direct precursors to modern *thematic role* theory. Dowty [-@dowty1991thematic] refined this paradigm by decomposing thematic roles into clusters of sentential entailments, yielding two *proto-roles*: the Proto-Agent (characterized by volitional involvement and causation) and the Proto-Patient (characterized by incremental themes and causal affectedness). This decomposition proves critical for our categorical formalization: it replaces discrete, named roles with a *graded* structural topology where role assignment is a matter of degree rather than kind. Consequently, morphisms in our cognitive case diagrams carry continuous weights $w \in [0,1]$ representing the degree to which a noun phrase satisfies proto-role entailments—a design choice that yields the enriched category structure developed formally in \autoref{sec:enriched-categories}.

## Four Alignment Systems

Contemporary typological work reveals that the world's languages realize case systems according to a small number of *alignment types*—systematic patterns governing how the core arguments of transitive and intransitive clauses are grouped [@polinsky2015case; @blake2001grammatical; @haspelmath2009universality].

### S, A, P

The cross-linguistic comparison rests on three primitives:

| Symbol | Role | Definition |
| :---: | :---- | :--- |
| **S** | Sole argument of intransitive | "The child **sleeps**" |
| **A** | Agent-like argument of transitive | "**The child** broke the vase" |
| **P** | Patient-like argument of transitive | "The child broke **the vase**" |

### Accusative, Ergative, Active-Stative, Fluid-S: Four Ways to Group Intransitive Subjects

The key insight from typological research is that languages differ in how they *group* these three roles for purposes of case marking, agreement, and other grammatical processes:

| Alignment | Grouping | Exemplar Languages |
| :--- | :--- | :--- |
| **Nominative–Accusative** | S = A $\neq$ P | English, Latin, Finnish, Russian |
| **Ergative–Absolutive** | S = P $\neq$ A | Basque, Dyirbal, Georgian (partly) |
| **Active–Stative** | S splits by agentivity | Lakhota, Guaraní, Eastern Pomo |
| **Tripartite** | S $\neq$ A $\neq$ P | Nez Perce, some Australian languages |
| **Fluid-S** | S marking varies by context | Bats (NE Caucasian), Acehnese |

**Fluid-S and Context-Dependent Functors.** In Bats (Nakh-Daghestanian), the intransitive subject of a single verb surfaces in different cases strictly depending on the speaker's internal construal of agentive volition. For example, the verb *fall* assigns an absolutive S when the action is accidental (*The child-ABS fell*), but assigns an ergative S when the action is volitional (*The child-ERG fell [on purpose]*).

Categorically, we model Fluid-S as a **context-dependent functor** $F_\theta: \mathcal{U} \to \mathcal{L}$ parameterized by a continuous volition feature $\theta \in [0,1]$. \autoref{fig:fluid-s} visualizes the resulting volition landscape: case categorization boundaries shift dynamically as a direct function of the agent's internal construal, satisfying naturality only up to a probabilistic reparameterization of $\theta$.

![Fluid-S alignment is a continuous mapping, not a binary switch. The context-dependent functor $F_\theta: \mathcal{U} \to \mathcal{L}$ is rendered as a 2D decision surface with volitional control $\theta \in [0,1]$ on the x-axis and proto-agentivity [@dowty1991thematic] on the y-axis. Color intensity represents $P(\text{ERG} \mid \theta, \text{agentivity})$, computed via a logistic boundary. Nakh-Daghestanian verb exemplars (Bats language) are overlaid at their typologically attested coordinates: low-volition actions (sneeze, accidental fall) cluster in the ABS region; high-volition actions (jump, fight) occupy the ERG region. The dashed curve marks the functor decision boundary where $F_\theta(S)$ transitions from ABS to ERG. Generated programmatically from the `FluidSFunctor` class.](output/figures/fluid_s_volition_landscape.png){#fig:fluid-s}

**Synthetic Case-Role Algebra.** We introduce Synthetic Case-Role Algebra as a novel, computational upgrade to the Dowty-style proto-role framework. Where Dowty modeled proto-roles as static clusters of entailments [-@dowty1991thematic], we formalize them as **objects in a $[0,1]$-enriched monoidal category** with tensor product over role compositions. This advancement enables purely algebraic manipulation of semantic roles: composition, weighting, and transformation of roles proceed through functorial operations representing complex event structures such as causativization, serial verb constructions, and argument-structure alternations. Crucially, this enriched structure demonstrates that "case assignment" is not a discrete binary choice but a vector-valued expectation in continuous case space—providing the mathematical bridge between the symbolic traditions of formal grammar and the statistical representations of modern neural language models (\autoref{sec:categorical-semantics}).

Claassen [-@claassen2019alignment] provides a comprehensive survey of the explanatory frameworks proposed for alignment diversity, arguing that no single factor (processing efficiency, disambiguation, discourse pragmatics) suffices—a conclusion that motivates our multi-dimensional categorical formalization. Wu [-@wu2024amis] offers a detailed case study of Amis (Austronesian), demonstrating how verb classification, case marking, and grammatical relations interact in a language that defies simple alignment classification.

Beyond the three core arguments, languages distinguish a rich inventory of oblique cases. Our formalization follows the CEREBRUM framework [@friedman2024cerebrum] in adopting eight fundamental cases:

| Case | Abbreviation | Semantic Core | Syntactic Prototype |
| :--- | :---: | :--- | :--- |
| Nominative | NOM | Agent / experiencer | Intransitive subject, transitive agent |
| Accusative | ACC | Patient / theme | Direct object, incremental theme |
| Genitive | GEN | Possessor / source | Possessive modifier, partitive |
| Dative | DAT | Recipient / goal | Indirect object, beneficiary |
| Instrumental | INS | Instrument / means | Adverbial of means |
| Locative | LOC | Location / context | Spatial/temporal ground |
| Ablative | ABL | Origin / cause | Source of motion, causal adjunct |
| Vocative | VOC | Addressee | Direct address |

While historically used merely to diagram sentences, this exact eight-role inventory is what enables the **Categorical AI Protocol** introduced in \autoref{sec:ai-implications}. By rigidly mapping artificial agent capabilities to corresponding grammatical cases—e.g., treating an API as strictly `INS`, passive data strictly as `ACC`, and system context rigidly as `LOC`—the cognitive case diagram enforces computational boundary constraints that natively repel prompt injection attacks (\autoref{sec:cognitive-security}).



---



# Case Categories: Roles as Objects, Relations as Morphisms, Alignment as Functors {#sec:case-categories}

## Eight Case Roles as Objects

We define a **case category** $\mathcal{C}$ as a small category where:

- **Objects** are case roles (NOM, ACC, GEN, DAT, INS, LOC, ABL, VOC)
- **Morphisms** are grammatical relations between roles (e.g., "transitive action": NOM → ACC)
- **Identity morphisms** represent the reflexive relation of each case role to itself
- **Composition** models the transitivity of grammatical dependencies

This formalization is implemented in our `CaseCategory` class, which uses set-based object tracking and list-based morphism storage as the underlying representation. Each object carries its role enum and optional morphosyntactic features; each morphism carries a relation label and an enriched weight $w \in [0,1]$. \autoref{fig:case-standard} shows the full eight-case standard category.

![Eight case roles form a directed graph with weighted grammatical morphisms. The standard linguistic case category $\mathcal{C}$ with objects NOM, ACC, GEN, DAT, INS, LOC, ABL, VOC and directed morphisms encoding grammatical relations. Edge labels identify relation types (transitive_action: NOM$\to$ACC, possession: GEN$\to$NOM, transfer: ACC$\to$DAT, spatial_grounding: LOC$\to$ACC); edge weights $w \in [0,1]$ reflect proto-role satisfaction per Dowty's [-@dowty1991thematic] decomposition. The enriched structure over $([0,1], \cdot, 1)$ ensures multiplicative weight attenuation under composition (\autoref{eq:eq-2-1}). Generated programmatically from the `CaseCategory` class.](output/figures/case_category_standard.png){#fig:case-standard}

## Accusative vs. Ergative as Structurally Non-Isomorphic Functors

An **alignment functor** $F: \mathcal{U} \to \mathcal{L}$ formally maps a universal case category $\mathcal{U}$ to a language-specific category $\mathcal{L}$ by systematically collapsing objects that the target language treats as equivalent. For example, in an accusative language, the functor forcibly merges S and A into a single NOM role while preserving P as a distinct ACC role: $F(\text{S}) = F(\text{A}) = \text{NOM}$, $F(\text{P}) = \text{ACC}$.

Mathematically, this functor guarantees three properties:

- **Surjective on objects**: Every target case role is the explicit image of a universal role.
- **Structure-preserving**: Grammatical relations in $\mathcal{U}$ strictly map to relations in $\mathcal{L}$.
- **Diagnostic kernels**: The kernel of $F$ (the set of objects mapping to the identical target) uniquely identifies the language's alignment typology.

Thus, the alignment functor formalizes linguistic neutralization with mathematical precision: two semantically distinct roles receive identical morphological treatment precisely because the functor collapses them into a single object in the target category.

**Explicit functor construction.** Let $\mathcal{U}$ be the universal three-role category with objects $\{S, A, P\}$ and morphisms $f\colon A \to P$ (transitive action), $g\colon S \to S$ (intransitive). The accusative functor $F_{\text{acc}}\colon \mathcal{U} \to \mathcal{L}_{\text{acc}}$ and ergative functor $F_{\text{erg}}\colon \mathcal{U} \to \mathcal{L}_{\text{erg}}$ act on objects as:

\begin{equation}
F_{\text{acc}}(S) = F_{\text{acc}}(A) = \text{NOM}, \quad F_{\text{acc}}(P) = \text{ACC}
\label{eq:eq-2-3}
\end{equation}

\begin{equation}
F_{\text{erg}}(S) = F_{\text{erg}}(P) = \text{ABS}, \quad F_{\text{erg}}(A) = \text{ERG}
\label{eq:eq-2-4}
\end{equation}

On morphisms, each functor strictly preserves the transitive relation: $F_{\text{acc}}(f) = f'\colon \text{NOM} \to \text{ACC}$ and $F_{\text{erg}}(f) = f''\colon \text{ERG} \to \text{ABS}$. Crucially, the *kernel* of $F_{\text{acc}}$---the exact set $\{(X,Y) \mid F_{\text{acc}}(X) = F_{\text{acc}}(Y)\}$---resolves to $\{(S,A)\}$, formally encoding the syntactic identification of the intransitive subject with the transitive agent. Conversely, the kernel of $F_{\text{erg}}$ resolves to $\{(S,P)\}$. This topological kernel structure successfully supplies a highly compact, computable algebraic fingerprint for every known alignment type.

\autoref{fig:alignment} shows three alignment systems rendered from our `CaseCategory` implementation.

![Functor kernels uniquely fingerprint each alignment typology. Three alignment systems realized as functors from $\mathcal{U} = \{S, A, P\}$: **Nominative--Accusative** merges $\{S,A\} \to \text{NOM}$ (kernel $\{(S,A)\}$, \autoref{eq:eq-2-3}); **Ergative--Absolutive** merges $\{S,P\} \to \text{ABS}$ (kernel $\{(S,P)\}$, \autoref{eq:eq-2-4}); **Tripartite** is injective (kernel $\emptyset$). Color-coded nodes reveal neutralization patterns: shared colors indicate functor identification of roles. Generated programmatically from the `CaseCategory` implementation.](output/figures/alignment_comparison.png){#fig:alignment}

![Morphism composition attenuates weights multiplicatively through intermediate case roles. Morphism $f\colon\text{NOM}\to\text{ACC}$ (transitive action, $w_f=0.9$) and $g\colon\text{ACC}\to\text{DAT}$ (transfer, $w_g=0.7$) compose to $g \circ f\colon\text{NOM}\to\text{DAT}$ with $w(g \circ f) = 0.63$ per \autoref{eq:eq-2-1}. The commutative triangle encodes that DAT assignment factors through ACC---the multiplicative attenuation reflects the typological observation that subject--recipient relations are weaker than the constituent subject--object and object--recipient links. Generated programmatically from the `CaseCategory` class.](output/figures/composition_triangle.png){#fig:composition}

## Graded Proto-Roles as $[0,1]$-Weighted Morphisms

Following Dowty [-@dowty1991thematic], we equip morphisms with weights in $[0,1]$ that encode the degree of proto-role satisfaction. A morphism $f: \text{NOM} \to \text{ACC}$ with weight $w = 0.9$ indicates a strong transitive action (clear agent acting on clear patient), while $w = 0.4$ might indicate an experiencer construction ("The child fears the dark") where the nominative argument only weakly satisfies Proto-Agent entailments.

Composition of enriched morphisms multiplies weights:
\begin{equation}
w(g \circ f) = w(g) \cdot w(f)
\label{eq:eq-2-1}
\end{equation}

This multiplicative composition reflects the intuition that grammatical dependencies attenuate as they chain through intermediate roles. \autoref{fig:composition} illustrates the categorical composition of two morphisms through an intermediate case role. The resulting structure is a category enriched over $([0,1], \cdot, 1)$—a connection we develop fully in \autoref{sec:enriched-categories}.

## Alignment Shifts as Natural Transformations: Grammar Agreement as Functor Commutativity

Having established that alignment systems are functors $F, G: \mathcal{U} \to \mathcal{L}$ from a universal case category to language-specific categories, a natural question arises: *how do different alignment systems relate to each other?* The categorical answer is a **natural transformation** $\alpha: F \Rightarrow G$—a systematic family of morphisms $\alpha_A: F(A) \to G(A)$ for each case role $A$, satisfying the **naturality condition**:

\begin{equation}
G(f) \circ \alpha_A = \alpha_B \circ F(f) \quad \text{for every morphism } f: A \to B
\label{eq:eq-2-2}
\end{equation}

This naturality constraint is the formal expression of *grammatical coherence*: transforming one alignment into another and then applying a grammatical relation yields the same result as first applying the relation and then transforming—ensuring that alignment comparison respects the relational fabric of the grammar.

**Worked example.** Consider the accusative functor $F$ (which maps S and A to NOM, P to ACC) alongside the tripartite functor $G$ (which maps explicitly to S $\to$ ABS, A $\to$ ERG, P $\to$ ACC). The **identity natural transformation** $\text{id}_F: F \Rightarrow F$ provides components ${(\text{id}_F)}_A = \text{id}_{F{(A)}}$ over every role $A$, trivially satisfying the naturality condition. We construct the **vertical composition** $\beta \circ \alpha{}$ of two natural transformations $\alpha: F \Rightarrow G$ and $\beta: G \Rightarrow H$ purely componentwise: ${(\beta \circ \alpha)}_A = \beta_A \circ \alpha_A$.

Our `NaturalTransformation` class implements these operations, with `ComponentMorphism` objects encoding each $\alpha_A$, and `compose_transformations()` implementing vertical composition. The `IdentityNaturalTransformation` constructor automatically generates identity components for every object in an `AlignmentFunctor`'s domain. This machinery provides the formal infrastructure for comparing alignment types not merely by listing their neutralization patterns but by characterizing the *structural mappings* between them—e.g., the natural transformation from accusative to tripartite alignment is injective (no two roles merge in the target), while the transformation from tripartite to ergative is non-injective (S and P merge into ABS).



---




# From Phrase Structure to Type Algebra {#sec:categorial-grammar}

## Each Word Is Its Own Grammar Rule

Traditional generative grammar computes sentence structure using top-down phrase-structure rules that recursively combine constituents. Categorial grammar perfectly inverts this perspective: rather than specifying abstract construction rules, it assigns each lexical item a dedicated *type* that rigorously encodes its combinatory potential. For example, a transitive verb like "chases" is not loosely defined as "a word requiring a subject and object," but specifically assigned the algebraic type $(n \backslash s) / n$—an active function that categorically demands a noun to its right (the object) and a noun to its left (the subject) to yield a complete sentence.

## Lambek's Residuation Law: Consuming and Producing Types in Linear Order

Lambek [-@lambek1958mathematics] laid the algebraic foundations by introducing a *residuated* structure on syntactic types. He defined two binary operations—the left residual $\backslash$ and the right residual $/$—derived from the multiplicative connective $\otimes$ (concatenation). The fundamental axiom governing this system is the residuation law:

\begin{equation}
A \otimes B \leq C \quad \iff \quad A \leq C / B \quad \iff \quad B \leq A \backslash C
\label{eq:eq-3-1}
\end{equation}

This law brilliantly captures the fundamental duality of syntax: a verb of type $(n \backslash s) / n$ actively *consumes* available noun arguments to *produce* a well-formed sentence. The resulting **Lambek calculus** operates as a non-commutative intuitionistic linear logic—non-commutative because strict word order dictates meaning, and linear because the derivation logically consumes each lexical resource exactly once.

### Pregroups Unlock Compact Closure: The Bridge to DisCoCat String Diagrams

Lambek [-@lambek2004fine] later simplified the framework to **pregroup grammars**, where each type $a$ has a left adjoint $a^l$ and a right adjoint $a^r$ satisfying:

\begin{equation}
a^l \cdot a \leq 1 \leq a \cdot a^l \qquad a \cdot a^r \leq 1 \leq a^r \cdot a
\label{eq:eq-3-2}
\end{equation}

Coecke, Sadrzadeh, and Clark revolutionized this formal structuralism in 2010 with the **DisCoCat** (Distributional Compositional Categorical) model [-@coecke2010mathematical]. DisCoCat mathematically unifies categorial grammar with distributional semantics by defining strong monoidal functors mapping pregroup grammars directly into vector spaces. As Duneau emphasizes, this approach "allows the meaning of a sentence to be computed as a function of both the distributional meaning of the words involved, as well as its grammatical form" [-@duneau2021parsing]. By proving that pregroups and finite-dimensional vector spaces both behave as rigid monoidal categories, DisCoCat allows us to compute whole-sentence vector meanings linearly from constituent word vectors.

In this system, grammaticality literally reduces to algebraic verification: checking whether a sequence of types maps to the sentence type $s$ via strict *contraction* ($a^l \cdot a \to 1$) and *expansion* ($1 \to a \cdot a^l$) operations. This specific reformulation unlocks the DisCoCat framework (\autoref{sec:categorical-semantics}) because pregroups function as **compact closed categories**, natively supporting a powerful, computationally sound diagrammatic calculus. When a derivation is ill-typed, contractions fail to close: there is no valid reduction to $s$. \autoref{sec:cognitive-security} develops the security reading of that failure mode—typed interaction boundaries and prompt injection as illicit role reassignment.

## Cups, Caps, and Joyal–Street: How Wires Prove Grammaticality

The pivotal connection between categorial grammar and visualization comes from Joyal and Street [-@joyalstreet1991geometry], who proved that morphisms in monoidal categories can be faithfully represented as *string diagrams*—planar graphs where:

- **Wires** represent types (objects of the category)
- **Boxes** represent words or operations (morphisms)
- **Vertical composition** represents sequential application
- **Horizontal juxtaposition** represents the tensor product (concatenation)
- **Cups and caps** represent the contraction/expansion of a pregroup

\autoref{fig:string-diagram} surveys three syntactic structures side by side (progression from intransitive to passive); \autoref{fig:native-discocat} shows the same transitive sentence rendered by our native matplotlib pipeline—a direct computational output confirming word-box layout, wire routing, and cup-contraction geometry independently of DisCoPy.

![Native matplotlib rendering cross-validates DisCoPy pregroup geometry. String diagram for "Alice chases Bob" generated via `src.visualization.string_diagrams.render_discocat_sentence()` without the DisCoPy library. Three Word boxes carry pregroup types: $n$ (Alice, **blue** = NOM), $n^r \otimes s \otimes n^l$ (chases, **neutral**), and $n$ (Bob, **red** = ACC). Dashed arcs trace cup connections from noun wires to the verb's adjoint slots, rendering $\varepsilon: n^r \otimes n \to 1$ and $\varepsilon: n^l \otimes n \to 1$ as paired ligatures. This confirms that our visualization pipeline correctly reconstructs pregroup string-diagram geometry using only case-role metadata from `src.case_systems.case_category`, cross-validating the DisCoPy canonical output in \autoref{fig:discopy-transitive}.](output/figures/string_diagram_discocat.png){#fig:native-discocat}

![Sentence complexity increases monotonically from intransitive to passive. A 1×3 DisCoPy pregroup grammar visualization: Panel (a) intransitive "Bob runs" (NOM, 1 cup); Panel (b) transitive "Alice chases Bob" (NOM+ACC, 2 cups); Panel (c) passive "Bob is-chased" (patient promoted to subject via reduced pregroup type). Cup count directly reflects verb valency per \autoref{eq:eq-4-4}.](output/figures/discopy_sentence_progression.png){#fig:string-diagram}

![Type-logical structure is invariant under surface word-order permutation. Pregroup derivations for "SUBJ chases OBJ" across three typologically diverse languages: English (SVO), Latin (inflected, free order), and Japanese (agglutinative, SOV). Each renders an identical type reduction $n \otimes (n^r \otimes s \otimes n^l) \otimes n \to s$, confirming the central claim of categorial grammar: syntactic universals reside in the type algebra, not in linear word order.](output/figures/discopy_multilingual.png){#fig:multilingual-isomorphism}

This result—the soundness and completeness of string-diagrammatic reasoning—formally guarantees that any topological conclusion drawn visually from the diagram is algebraically valid: the diagram is not a heuristic but a rigorous proof instrument.

This profound visual transparency instantiates exactly the "free ride" phenomenon identified by Shimojima [-@shimojima1996reasoning]: a single diagram simultaneously exposes the syntactic derivation, the deep argument structure, and the compositional flow of semantic meaning—entirely eliminating the need for sequential, explicit inference steps.

**Concrete derivation in DisCoPy.** The type reduction for "Alice chases Bob" is computationally verified using the DisCoPy library's `discopy.rigid` module:

```python
from discopy.rigid import Ty, Box, Cup, Id
n, s = Ty('n'), Ty('s')
alice = Box('Alice', Ty(), n)
chases = Box('chases', Ty(), n.r @ s @ n.l)
bob  = Box('Bob',  Ty(), n)
words = alice @ chases @ bob          # n ⊗ (n.r ⊗ s ⊗ n.l) ⊗ n
cups  = Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
diagram = words >> cups               # reduces to s
assert diagram.cod == s               # type-checks: sentence type
```

The two `Cup` operations successfully contract $n$ with $n^r$ (resolving the subject–verb link) and $n^l$ with $n$ (resolving the verb–object link). This topological reduction collapses the five-wire tensor product into a single, valid sentence wire $s$. Consequently, the assertion `diagram.cod == s` constitutes a direct, machine-processable proof of grammaticality.

**From pregroup types to graded types.** The standard pregroup derivation produces a rigid, binary grammaticality judgment: the final codomain of the fully contracted tensor product either matches the sentence type $s$ (grammatical) or fails (ill-formed). However, we can *grade* this binary verdict by replacing the underlying Boolean algebra $\{0,1\}$ with the continuous unit interval $[0,1]$. This substitution yields a graded type theory where type judgments carry continuous confidence weights rather than truth values. Asudeh and Giorgolo [-@asudeh2020graded] developed this approach using a monadic semantics that wraps base types inside a computational effect tracking epistemic uncertainty—an idea whose categorical content is precisely a change of enrichment base.

Mapped into our framework, this operation corresponds exactly to the $[0,1]$-enrichment detailed in \autoref{sec:enriched-categories}: the enriched scalar weight on any specific morphism $f: A \to B$ quantifies the systemic confidence that the categorical case assignment $A \to B$ remains well-typed. From there, categorical magnitude aggregates these sparse, local confidence scores into a robust global complexity measure evaluating the entire syntactic derivation. Ultimately, the systematic progression from rigid pregroup strings, through graded types, into fully enriched case categories operates mathematically as a strict cascade of base-change functors ($\mathbf{Bool} \hookrightarrow [0,1] \hookrightarrow \mathbf{R}_{\geq 0}$)—where each successive level grants greater representational nuance while demanding higher computational complexity.

![Direct DisCoPy machine output confirms pregroup type reduction to sentence wire $s$. Nine Word boxes carry complex noun-phrase types (e.g., $n \otimes n^l$ for adjectives mapping an adjacent noun to a modified noun) and core verb types ($n^r \otimes s \otimes n^l$ for the transitive "intercepts"). Eight Cup contractions sequentially resolve the argument scopes from the deepest noun phrases outward, ultimately canceling all local adjoint pairs and reducing the extended initial tensor product to the single sentence wire $s$. Unlike the schematic progression in \\autoref{fig:string-diagram}, this is the *direct computational output* of a multi-word discourse component, strictly confirming `diagram.cod == s`. By the Curry--Howard correspondence, this diagram simultaneously constitutes a syntactic derivation, a proof of well-typedness, and (under the meaning functor of \\autoref{sec:categorical-semantics}) a compositional semantic computation. Our extension decorates $n$-typed wires with functorial states $S: \mathbf{Ent} \to \mathbf{Case}$, tracking role assignments across discourse boundaries via **DisCoCirc entity wires**.](output/figures/discopy_transitive.png){#fig:discopy-transitive}



---



# Case Subscripts, Passivization, and the Curry–Howard Proof {#sec:case-type-logic}

Case-marked noun phrases actively receive compound types that rigorously encode both their immediate grammatical role and their larger combinatory potential. For example, in a nominative–accusative language, the type assignment proceeds as follows:

| Expression | Type | Gloss |
| :--- | :--- | :--- |
| "Alice" (subject) | $n_{\text{NOM}}$ | Noun, nominative-marked |
| "the ball" (object) | $n_{\text{ACC}}$ | Noun, accusative-marked |
| "kicks" | $(n_{\text{NOM}} \backslash s) / n_{\text{ACC}}$ | Seeks ACC right, NOM left |
| "to Bob" (recipient) | $(s \backslash s) / n_{\text{DAT}}$ | Modifies sentence via DAT argument |

The specific subscripts structurally refine the base noun type $n$ with mandatory continuous case features, mathematically guaranteeing that the transitive verb "kicks" exclusively selects a nominative-marked subject and an accusative-marked object. Any feature mismatch automatically blocks the algebraic derivation, accurately modeling native ungrammaticality.

**Alignment and natural transformations.** Cross-linguistic alignment is modeled functorially in \autoref{sec:case-categories}: alignment types are structure-preserving functors from a universal role category to a language-specific case category, compared via natural transformations when one asks how two alignments cohere on the same underlying argument structure. At the level of case-marked pregroup types (this section), that functorial picture **suggests** treating agreement checks as naturality-style coherence constraints: the morphosyntactic alignment chosen for arguments must remain compatible with the verb's combinatorial requirements so that reductions still factor through the intended case-typed slots. We do not claim a full adjunction between identity and alignment functors in the pregroup category here; the precise categorical status of alignment is anchored in \autoref{sec:case-categories}, while the typed reductions below supply the concrete syntax.

## Syntactic Derivation as Proof, Case Assignment as Type Inference

A deep structural parallel underlies the Lambek calculus: derivations of syntactic types correspond to proofs in intuitionistic logic (via the Curry–Howard isomorphism), and therefore to programs in a typed lambda calculus. Specifically:

| Syntactic Domain | Logical Domain | Computational Domain |
| :--- | :--- | :--- |
| Types $(A / B, A \backslash B)$ | Propositions | Types |
| Derivations | Proofs | Programs ($\lambda\text{-terms}$) |
| Cut elimination | Proof normalization | $\beta\text{-reduction}$ |
| Commutativity of cuts | Confluence of rewriting | Church–Rosser property |

This foundational correspondence dictates two critical consequences for our cognitive framework:

1. **Semantic compositionality strictly follows syntactic well-formedness**: A successfully typed derivation automatically guarantees a well-formed geometric meaning representation (specifically, the exact $\lambda\text{-term}$ isolated and extracted directly from the formal proof).
2. **Case assignment reduces to type inference**: Dynamically determining the correct case for a noun phrase in context is computationally equivalent to inferring the type of an unknown variable in a $\lambda\text{-expression}$—thereby grounding case assignment in the well-understood algorithmic landscape of type inference (Hindley-Milner and its extensions).

## Song's Monadic Roots

Song [-@song2022act; -@song2022blog] significantly extends this categorial framework by deploying a novel **monadic semantics** for root syntax. He successfully models the sublexical decomposition of complex verb roots by embedding specialized monads directly into the base syntactic category. This computational approach captures the deep intuition that a seemingly simple verb like "break" harbors layered internal structure—specifically, an active causative layer tightly coupled to a passive result-state layer—which dynamically dictates subsequent case assignment. The formal monad elegantly encapsulates this tangled lexical complexity within one streamlined categorical construction, empowering the type-logical grammar to process lexical features and syntactic composition simultaneously and uniformly.

This monadic architecture seamlessly interfaces with modern graded type theory. For instance, Asudeh and Giorgolo [-@asudeh2020graded] previously developed a monadic semantics tracking evidentiality, deploying graded computational effects to quantify the shifting epistemic real-world status of various propositions. Our framework extends this exact pattern into the domain of morphological case, where the continuous "grade" attached to any specific morphism formally encodes the statistical strength and validity of that local semantic role assignment.

## Passivization Is a Swap: Voice Alternation as Topological Wire Crossing

Within categorical linguistics, **passivization** emerges as a uniquely revealing topological operation. Traditionally described as a syntactic rule that promotes the patient to subject position while (optionally) demoting the agent to an oblique role, passivization in our framework ceases to be an ad-hoc transformation; instead, it executes a mathematically precise *type permutation*—a Swap morphism $\sigma_{A,B}: A \otimes B \to B \otimes A$ that geometrically crosses the noun wires feeding into the verb's pregroup derivation.

In a pregroup grammar, the active transitive "Alice chases Bob" has the type reduction:

\begin{equation}
n_{\text{NOM}} \cdot (n^r \cdot s \cdot n^l) \cdot n_{\text{ACC}} \to s
\label{eq:eq-3-3}
\end{equation}

Passivization permutes the noun arguments, yielding "Bob is chased by Alice" with the swapped type assignment:

\begin{equation}
n_{\text{ACC}} \cdot (n^r \cdot s \cdot n^l) \cdot n_{\text{NOM}} \to s
\label{eq:eq-3-4}
\end{equation}

Crucially, the DisCoPy library's rigid `Swap` primitive renders this verbal permutation explicit and computationally precise: the specific swap operation $\sigma_{n,n}: n \otimes n \to n \otimes n$ successfully permutes the two active noun wires without violating the category's overarching monoidal structure. The generated passive diagram diverges from its active counterpart solely through this physical crossing of the noun wires. This transforms abstract syntactic voice alternation into a highly visible, instantly readable topological feature embedded directly within the string diagram.

This diagrammatic transparency exemplifies Shimojima's [-@shimojima1996reasoning] free-ride inference capability. By simply inspecting the visual topology, a cognitive agent immediately verifies that passivization strictly preserves the verb's deep, inherent argument structure while merely rearranging its superficial surface realization—a structural fact that typically requires chaining multiple sequential inference steps to algebraically establish within standard linear notation.

![Passivization is a topological change in wire connectivity, not a lexical substitution. The passive construction \"Bob is-chased\" rendered by DisCoPy shows that voice alternation removes one Cup contraction relative to the active form, lowering the syntactic complexity score of \autoref{eq:eq-4-4} (defined in \autoref{sec:compact-closure-complexity}). The structural difference between active and passive voice is thus captured entirely by diagram topology.](output/figures/discopy_passive.png){#fig:discopy-passive}



---




# DisCoCat: Composing Word Vectors According to Pregroup Type Derivations {#sec:categorical-semantics}

## The Formalism–Distribution Impasse and Why Montague Cannot Meet Harris

The study of linguistic meaning has historically been fractured between two traditions offering complementary strengths and weaknesses:

1. **Formal semantics**, following Montague [-@montague1973proper], strictly models meaning compositionally: the algebraic meaning of any complex expression functions as a direct product of its parts and their syntactic combination. This tradition excels at capturing rigid logical structure (quantification, negation, modality) but severely struggles with fluid lexical meaning, typically treating content words as opaque, unanalyzed primitives.

2. **Distributional semantics** models meaning empirically: a word's meaning organically emerges from its distribution across contexts, typically encoded computationally as a dense vector in high-dimensional space. This distributional hypothesis—famously summarized as "You shall know a word by the company it keeps" [@firth1957papers]—traces directly to J.R. Firth and Zellig Harris [-@harris1954distributional], whose algebraic analysis proved that linguistic elements occurring in similar environments inherently share semantic properties. While this tradition beautifully captures graded similarity and geometric analogy, it lacks rigorous compositional structure. Under pure distribution, "dog bites man" and "man bites dog" collapse into identical vector representations.

This theoretical tension represents one of the deepest impasses in modern cognitive science. Turney and Pantel's [-@turney2010frequency] comprehensive survey of vector space models proved that distributional methods smoothly capture highly fine-grained semantic distinctions—synonymy, antonymy, hypernymy, analogy—but strictly isolate these victories to the isolated word level. Baroni and Lenci [-@baroni2010distributional] built a tensor-based *Distributional Memory* framework partially addressing this compositionality by structuring co-occurrence data into a three-way tensor over (word, relation, word) triples, yet this approach lacked a principled type-logical backbone. Lenci [-@lenci2018distributional] thoroughly surveyed this modern landscape and formally identified the central open problem: discovering exactly how to fuse the *algebraic compositionality* of formal semantics with the powerful *empirical grounding* of distributional vector models.

The **DisCoCat** (Distributional Compositional Categorical) framework [@coecke2010mathematical] resolves this long-standing tension. It deploys category theory to compose distributional meanings directly according to syntactic structure, yielding a semantic framework that is simultaneously *compositional* (via categorial grammar), *distributional* (via corpus-derived vector spaces), and *algebraically principled* (via rigid monoidal category theory).

## Word2Vec → BERT → GPT

The distributional programme has undergone a dramatic computational intensification in the era of large language models (LLMs). The trajectory from classical co-occurrence matrices through static word embeddings to contextual transformers can be understood as a progressive *enrichment* of the distributional hypothesis itself:

1. **Static embeddings**: Mikolov et al.'s [-@mikolov2013efficient] Word2Vec (skip-gram and CBOW) demonstrated that targeted prediction-based training on local context windows naturally generates word vectors exhibiting striking algebraic regularity—yielding the famous "king $-$ man $+$ woman $\\approx$ queen" geometric analogy. Pennington et al.'s [-@pennington2014glove] GloVe successfully incorporated global co-occurrence statistics via log-bilinear regression, yielding dense vectors whose inner products cleanly approximate underlying pointwise mutual information. Both models instantiate the distributional hypothesis in its classical Firthian form: contextual use strictly determines meaning, permanently encoding it as geometric position within a learned vector space.

2. **Contextual embeddings**: BERT [@devlin2019bert] and GPT [@radford2018improving] dramatically push beyond static type-level representations into dynamic *token-level* contextualized embeddings, where the identical word dynamically receives entirely different coordinate vectors in varying contexts. In terms of the formal vs. distributional dichotomy, this jump represents a critical advance: contextualized embeddings successfully (though implicitly) capture *compositional* structure by continuously conditioning word representations upon their full sentential environment. This addresses polysemy and complex constructional effects that static embeddings routinely conflate.

3. **Transformer architecture**: The transformer [@vaswani2017attention] explicitly implements distributional composition via its heavily parallelized multi-head self-attention mechanism, where each distinct attention head actively computes a statistically weighted combination of all given input token representations. The precise numerical attention weights $\\alpha_{ij} = \\text{softmax}(Q_i K_j^T / \\sqrt{d_k})$ operate entirely analogously to the formal enriched hom-values detailed in \\autoref{sec:enriched-categories}: they algorithmically encode the continuous *degree of contextual relevance* between tokens $i$ and $j$ within a specifically tuned representational subspace—yielding a graded, deeply learned distributional mapping.

The mapping back to our categorical framework is direct: **DisCoCat supplies the algebraic formalization of what modern LLMs learn empirically.** A transformer builds sentence representations by attending to syntactically and semantically relevant tokens through learned weight matrices. DisCoCat achieves the same goal by composing word vectors through type-logical derivations within a compact closed category. The central functor $F: \mathbf{Preg} \to \mathbf{FVect}$ defining DisCoCat is therefore the *principled* version of the composition that neural attention learns from data. Gavranović's [-@gavranovic2024thesis] categorical learning programme confirms this perspective rigorously, proving that neural attention heads operate as parameterized optics—categorical constructions composing functorially, mirroring DisCoCat derivations.

For case theory specifically, the transformer analogy is illuminating: each attention head in a transformer can be understood as learning a particular *relational role*—attending to subjects, objects, modifiers, or other grammatical functions. This is precisely the role that case marking plays in natural language: structuring who-does-what-to-whom. The case-typed noun spaces of our enriched DisCoCat model ($N_{\text{NOM}}, N_{\text{ACC}}, N_{\text{DAT}}, \ldots$) correspond to the role-specific representational subspaces that different attention heads learn to inhabit.

## The Meaning Functor $F: \mathbf{Preg} \to \mathbf{FVect}$ {#sec:discocat-meaning-functor}

### Pregroups and Vector Spaces Share a Category

DisCoCat's central observation is that pregroup grammars and vector spaces share a common abstract structure: both are **compact closed categories**. This means there exists a *meaning functor*:

\begin{equation}
F: \mathbf{Preg} \to \mathbf{FVect}
\label{eq:eq-4-1}
\end{equation}

from the pregroup grammar category (where objects are types and morphisms are grammatical reductions) to the category of finite-dimensional vector spaces (where objects are vector spaces and morphisms are linear maps).

Under this functor:

- Noun types $n$ map to a vector space $N$ (the noun space)
- Sentence types $s$ map to a vector space $S$ (the sentence space)
- A transitive verb of type $n^r \cdot s \cdot n^l$ maps to a tensor in $N \otimes S \otimes N$
- Pregroup contractions (cups/caps) map to the standard inner product and its dual

### Tensoring, Then Contracting: How "Alice Chases Bob" Becomes a Vector

The compositional meaning of a sentence is computed by tensoring the word meanings and then contracting the result along the indices determined by the syntactic derivation. For "Alice chases Bob":

\begin{equation}
\overrightarrow{\text{Alice chases Bob}} = (\overrightarrow{\text{Alice}} \otimes \overleftrightarrow{\text{chases}} \otimes \overrightarrow{\text{Bob}}) \circ (\varepsilon_N \otimes 1_S \otimes \varepsilon_N)
\label{eq:eq-4-2}
\end{equation}

where $\varepsilon_N: N \otimes N \to \mathbb{R}$ is the compact closure map (inner product). This computation has a direct diagrammatic representation as a string diagram—the same Joyal–Street [@joyalstreet1991geometry] formalism that governs the syntax.

### DisCoCat Resolves "Dog Bites Man" vs "Man Bites Dog"

Grefenstette and Sadrzadeh [-@grefenstette2015concrete] demonstrated that DisCoCat models can outperform purely distributional baselines on disambiguation and sentence similarity tasks. The key advantage is that compositional structure resolves ambiguities that bag-of-words models cannot: "dog bites man" and "man bites dog" receive different sentence vectors because the syntactic structure assigns different roles to the nouns.

**Attention as Cup contraction.** The claim that DisCoCat provides the "algebraic formalization" of transformer-based LLMs can be made precise. In a transformer's self-attention mechanism, the query–key inner product $\text{softmax}(QK^\top / \sqrt{d})V$ selects which word vectors interact—effectively implementing a *soft* version of the Cup contraction. The pregroup Cup $\varepsilon: n^r \otimes n \to I$ contracts two noun wires into a scalar; the attention inner product $q_i \cdot k_j$ contracts two contextualized vectors into an attention weight, which then mixes the value vectors. The difference is that the DisCoCat Cup is *binary* (either the types match or they don't) while the attention Cup is *graded* (producing a real-valued weight). This is precisely the $[0,1]$-enrichment of \autoref{sec:enriched-categories} applied to the type-reduction level: each attention head learns an enriched Cup that contracts types with learned confidence weights rather than categorical yes/no type-matching. Multi-head attention then corresponds to the tensor product of $h$ independent enriched contraction maps, each attending to a different substring of the relational structure—analogous to how DisCoCat composes multiple Cup contractions for multi-argument verbs.

![Cup contractions compute sentence meaning by contracting word tensors along syntactically determined indices. The DisCoCat meaning functor $F: \mathbf{Preg} \to \mathbf{FVect}$ applied to "Alice chases Bob." **Left panel**: pre-contraction tensor product $n \otimes (n^r \otimes s \otimes n^l) \otimes n$, showing three Word boxes with pregroup types. **Right panel**: fully contracted diagram where two Cup contractions ($\varepsilon: n^r \otimes n \to 1$ and $\varepsilon: n^l \otimes n \to 1$) reduce the five-wire product to sentence wire $s$. Under $F$, noun types map to $N$, the sentence type to $S$, and the verb's type to $\overleftrightarrow{\text{chases}} \in N \otimes S \otimes N$. The Cup contractions become inner products $\varepsilon_N: N \otimes N \to \mathbb{R}$, computing $\overrightarrow{\text{Alice chases Bob}} \in S$.](output/figures/discopy_composition.png){#fig:discopy-discocat}

## Case-Typed Noun Spaces and Alignment as Natural Transformation

The present contribution lies in showing how case marking enriches the DisCoCat framework with explicit role structure. In a case-marked DisCoCat model:

1. **Typed noun spaces**: Instead of a single noun space $N$, we define case-specific spaces $N_{\text{NOM}}, N_{\text{ACC}}, N_{\text{DAT}}, \ldots$ Morphisms between these spaces encode case-changing operations (passivization, dative shift, etc.).

2. **Case-constrained composition**: The meaning functor $F$ maps case-typed pregroup derivations to tensor contractions that respect case constraints. A verb seeking a nominative subject and accusative object contracts only with vectors from the appropriate spaces.

3. **Alignment as Natural Transformation**: Cross-linguistic alignment differences correspond to different meaning functors. However, we go further by modeling case alignment as **natural transformations** between functors. An accusative-language transformation $\eta_{\text{acc}}: \mathcal{I} \to F_{\text{acc}}$ identifies S and A arguments; an ergative transformation $\eta_{\text{erg}}$ identifies S and P. This categorification allows us to model "grammar" as the requirement that these transformations commute with the DisCoCirc entity wires, ensuring role persistence across sentences.

![Ditransitive valency exceeds transitive complexity, confirming the monotonic complexity--valency relationship. DisCoPy pregroup grammar for "Alice gives Bob a book": four Word boxes with types $n$ (Alice), $n^r \otimes s \otimes n^l \otimes n^l$ (gives), $n$ (Bob), and $n$ (a book). Three Cup contractions resolve subject--verb, indirect-object, and direct-object links, reducing the eight-wire product to sentence type $s$. This exemplifies Shimojima's [-@shimojima1996reasoning] free-ride inference: the diagram simultaneously shows argument structure, valency, and compositional flow. The complexity score (\autoref{eq:eq-4-4} in \autoref{sec:compact-closure-complexity}) exceeds that of simple transitive sentences.](output/figures/discopy_ditransitive.png){#fig:discopy-ditransitive}

The following sections extend this model to discourse and quantum computation.



---




# Compact Closure and Diagram Complexity: Snake Equation and Valency Metrics {#sec:compact-closure-complexity}

## The Snake Equation Powers Every Pregroup Contraction

### The Snake Equation (Zigzag Identity)

The essential algebraic engine driving DisCoCat is the strict **compact closure** of the governing pregroup category. For every lexical type $n$, the corresponding adjunction maps—$\eta_n: 1 \to n \otimes n^r$ (the cap expansion) and $\varepsilon_n: n^r \otimes n \to 1$ (the cup contraction)—must mathematically satisfy the fundamental **snake equation** (also known as the topological zigzag identity):

\begin{equation}
(\varepsilon_n \otimes 1_n) \circ (1_n \otimes \eta_n) = 1_n
\label{eq:eq-4-3}
\end{equation}

Translated into intuitive string-diagrammatic terms, a cup geometrically composed with a cap bridging adjacent wires immediately "straightens out" into a solid identity wire—a topological zigzag seamlessly canceling into a continuous straight line. This foundational axiom is not merely a geometric curiosity: it physically functions as the *engine* powering every valid pregroup type reduction. Every recorded grammatical contraction (e.g., a noun canceling against an active verb argument slot) constitutes a direct instance of the cup map $\varepsilon{}$, and every grammatical expansion instantiates the cap map $\eta{}$. The continuous snake equation algebraically guarantees that these interwoven contractions and expansions remain globally well-behaved—ensuring they can be freely inserted and removed without ever altering the final semantic meaning of the derivation.

Cognitively, the snake equation provides an immediate *visual proof* of coherence. A cognitive agent inspecting a string diagram can verify well-formedness by confirming that all zigzags cancel—a purely spatial operation requiring no sequential algebraic computation, and thus instantiating Shimojima's [-@shimojima1996reasoning] free-ride inference in its most direct form.

![The snake equation is the algebraic engine powering every pregroup type reduction. The compact closure axiom (\autoref{eq:eq-4-3}) rendered by DisCoPy: **left panel** shows the zigzag $(\varepsilon_n \otimes 1_n) \circ (1_n \otimes \eta_n)$ where a Cup $\varepsilon{}$ composed with a Cap $\eta{}$ forms a snake; **right panel** shows the identity wire $1_n$ it equals. Verified computationally via `diagram.normal_form() == Id(Ty('x'))`. Each pregroup contraction (noun canceling with verb argument) is an instance of $\varepsilon{}$; the snake equation guarantees that cup-cap pair insertions and removals leave derivations invariant (cf. \autoref{sec:categorial-grammar}).](output/figures/discopy_snake.png){#fig:discopy-snake}

### Four Metrics Quantify Derivational Complexity

The algebraic properties of pregroup diagrams support quantitative analysis of derivational complexity. Our `complexity_metrics` module implements four complementary measures using the DisCoPy library:

1. **Box count**: The number of lexical entries (Word boxes) in the diagram, corresponding to the sentence's word count from the type-logical perspective. A transitive sentence has 3 boxes (subject, verb, object); a ditransitive sentence has 4 or more.

2. **Cup/Cap count**: The number of contraction and expansion operations. Cups (denoted $\varepsilon{}$) count argument consumption; caps (denoted $\eta{}$) count argument introduction. The cup count directly reflects verb valency: an intransitive verb requires 1 cup, a transitive verb 2, and a ditransitive verb 3.

3. **Normal form**: A diagram is in *normal form* if no further simplifications (zigzag cancellations, box reordering) are possible. The `normal_form()` operation computes this canonical representative of the diagram's equivalence class. Normal form preservation under algebraic manipulation provides a correctness check for compositional operations.

4. **Syntactic complexity score**: A composite metric defined as:

\begin{equation}
\text{complexity}(D) = w_b \cdot |D|_{\text{box}} + w_c \cdot |D|_{\text{cup}} + w_d \cdot \text{depth}(D)
\label{eq:eq-4-4}
\end{equation}

where $|D|_{\text{box}}$, $|D|_{\text{cup}}$, and $\text{depth}(D)$ are the box count, cup count, and depth respectively, and $w_b, w_c, w_d$ are configurable weights (defaulting to equal weights). The *depth* of a diagram is the length of the longest path from input to output, counting boxes. Deeper diagrams encode more complex syntactic derivations—a ditransitive sentence like "Alice gave Bob a book" (depth 7) is structurally more complex than a simple intransitive "Alice runs" (depth 3).

The `compare_diagrams()` function applies these metrics across a collection of diagrams, producing tabular comparisons suitable for cross-linguistic analysis. \autoref{fig:complexity-comparison} visualizes these metrics across sentence types of increasing valency, demonstrating the monotonic relationship between argument structure and derivational complexity.

![Argument-structure complexity maps monotonically onto diagram topology. Complexity metrics (\autoref{eq:eq-4-4}) plotted across ten sentence types of increasing valency: from intransitive "Alice runs" (2 boxes, 1 cup) through transitive (3 boxes, 2 cups), ditransitive (4 boxes, 3 cups), and adjunct-stacked constructions up to "fast Alice gave Bob book quickly" (8 boxes, 4 cups). Cup count $|D|_{\text{cup}}$ increases monotonically with verb valency and adjunct stacking, confirming that argument-structure complexity is a topological invariant of the diagram. Actual sentences are overlaid in the plot; cup count is computable from the DisCoPy diagram via `len([b for b in diagram.boxes if isinstance(b, Cup)])`.](output/figures/complexity_comparison.png){#fig:complexity-comparison}

These metrics connect naturally to the enriched framework of \autoref{sec:enriched-categories}: diagram depth serves as a syntactic complexity proxy that can be incorporated into the enriched hom-value, providing a principled bridge between type-logical derivation cost and distributional semantic distance. Discourse-level persistence of entity wires (DisCoCirc) is developed in \autoref{sec:discocirc-discourse}. For multi-agent security, when tracking networks isolate an adversarial identity wire (a prompt injection) covertly attempting to merge with an ongoing command wire across communication boundaries, the circuit topology can flag the type violation before execution (\autoref{sec:cognitive-security}).



---



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



---



# $[0,1]$-Enriched Case Categories: Hom-Values as Distributional Proximity, Magnitude as Complexity {#sec:enriched-categories}

## Why Binary Morphisms Are Not Enough

The categories established in \autoref{sec:case-systems}—modeling case roles as objects and grammatical relations as morphisms—capture the *qualitative* topology of case systems: which roles exist and how they connect. However, actual linguistic data is fundamentally *quantitative*: certain grammatical relations are more probable than others, proto-role assignments vary in strength, and distributional similarity is a matter of degree.

To accommodate this quantitative dimension without sacrificing algebraic structure, we advance from ordinary categories to **enriched categories**. In an enriched category, hom-sets carry additional measurable structure rather than functioning as mere discrete sets of morphisms. The framework of Bradley et al. [-@fritz2021enriched] supplies the key formal construction.

## Enriching Over $([0,1],\cdot,1)$

### Hom-Values as Graded Distributional Proximity: Four Linguistic Interpretations

A category $\mathcal{C}$ enriched over the unit interval $([0,1], \cdot, 1)$ assigns to every pair of objects $A, B$ a *hom-value* $\mathcal{C}(A, B) \in [0,1]$ satisfying:

\begin{align}
\mathcal{C}(A, A) &= 1 \quad \text{(Identity)} \label{eq:eq-5-1} \\
\mathcal{C}(A, C) &\geq \mathcal{C}(A, B) \cdot \mathcal{C}(B, C) \quad \text{(Composition)} \label{eq:eq-5-2}
\end{align}

The identity axiom physically dictates that every distinct linguistic expression remains perfectly and maximally related to itself. The composition inequality imposes a strict logical boundary, demanding that distributional relatedness inherently composes sub-multiplicatively: if expression $A$ proves 80% related to $B$, and $B$ remains 70% related to $C$, the overarching algebraic structure formally guarantees that $A$ must be at least $0.8 \times 0.7 = 56\%$ related to $C$.

### Conditional Probability, Proto-Role Strength, Cosine Similarity

Bradley et al. [-@fritz2021enriched] originally interpret these numerical hom-values strictly as empirical *conditional probabilities* measured within a massive distributional model: $\mathcal{C}(A, B) = P(\text{context} \mid A \text{ and } B \text{ co-occur})$. Within our customized case-theoretic application, we actively broaden this interpretation to capture deep grammatical phenomena:

| Hom-value interpretation | Domain | Example |
| :--- | :--- | :--- |
| Conditional probability | Corpus statistics | P(ACC role \| transitive verb context) |
| Proto-role strength | Semantic typology | Degree of Proto-Agent satisfaction |
| Distributional similarity | Vector semantics | Cosine similarity of case-role embeddings |
| Morphological predictability | Morpholexicology | Reliability of case-marking paradigm |

### When Composition Inequality Fails

Our `EnrichedCategory` class implements this structure directly. The constructor takes a list of `CaseRole` objects and a NumPy proximity matrix encoding hom-values:

```python
from src.enriched_cat.enriched import EnrichedCategory
from src.case_systems.case_category import CaseRole
import numpy as np

roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
proximity = np.array([
    [1.00, 0.85, 0.30],  # NOM: high with ACC, low with DAT
    [0.85, 1.00, 0.45],  # ACC: high with NOM, moderate with DAT
    [0.30, 0.45, 1.00],  # DAT: low with NOM, moderate with ACC
])
cat = EnrichedCategory(
    name="English Case Proximity",
    roles=roles,
    proximity_matrix=proximity,
)

# Verify composition inequality: 0.30 >= 0.85 * 0.45 = 0.3825?
# This fails! English NOM-DAT is too distant relative to the chain.
assert not cat.check_composition_inequality(CaseRole.NOM, CaseRole.ACC, CaseRole.DAT)
```

The composition inequality violation here is linguistically meaningful: it tells us that the NOM→ACC→DAT chain overestimates the direct NOM→DAT relatedness, reflecting the typological fact that subject–recipient identity (e.g., in benefactive constructions) is more restricted than the product of agent–patient and patient–recipient proximities. \autoref{fig:enriched-heatmap} shows the distributional relations between case roles as a categorical relation graph.

![Core and peripheral argument complexes emerge from enriched distributional hom-values. Relation graph visualizing $\mathcal{C}(A,B) \in [0,1]$ among all eight case roles. Strong relations (solid edges) cluster into two groups: the **core argument complex** (NOM--ACC--DAT, linked by transitive and transfer morphisms) and the **peripheral complex** (LOC--INS--ABL, linked by spatial and instrumental relations). GEN bridges both via possessive modification. Weak relations (dashed edges) connect VOC---its peripheral isolation reflects the pragmatic rather than syntactic function of direct address. These hom-values yield the similarity matrix $Z$ (\autoref{eq:eq-5-4}) and categorical magnitude of \autoref{sec:enriched-categories}. Generated programmatically from the `EnrichedCategory` class.](output/figures/enriched_hom_matrix.png){#fig:enriched-heatmap}



---



# Magnitude of $\mathcal{C}$: The Effective Number of Roles, Redundancy-Corrected {#sec:magnitude-homology}

A central mathematical invariant unique to enriched categories is their **magnitude**—a numerical quantity capturing the "effective size" of the category by discounting distributional overlap between objects.

For an enriched category with $n$ objects, let $Z$ be the $n \times n$ similarity matrix where $Z_{ij} = \mathcal{C}(i, j)$. The categorical magnitude is:

\begin{equation}
|\mathcal{C}| = \sum_{i,j} (Z^{-1})_{ij}
\label{eq:eq-5-3}
\end{equation}

assuming $Z$ is invertible. This magnitude metric connects to information theory:

- For a *discrete* category (no non-trivial relationships), $|\mathcal{C}| = n$ (the number of objects)
- For a highly connected category, $|\mathcal{C}| < n$ (objects are "redundant")
- Magnitude connects to the diversity measures studied in ecology (species diversity), graph theory (effective graph resistance), and information geometry (Fisher information)

**Worked example.** Consider the minimal 3-case category with objects $\{S, A, P\}$ and hom-values $\mathcal{C}(S,A) = 0.85$ (S and A share agentive contexts), $\mathcal{C}(A,P) = 0.70$ (transitive co-occurrence), $\mathcal{C}(S,P) = 0.40$ (weak S–P overlap). The similarity matrix $Z$ is:

\begin{equation}
Z = \begin{pmatrix} 1.00 & 0.85 & 0.40 \\ 0.85 & 1.00 & 0.70 \\ 0.40 & 0.70 & 1.00 \end{pmatrix}, \quad Z^{-1} \approx \begin{pmatrix} 2.45 & -1.35 & 0.55 \\ -1.35 & 3.00 & -1.80 \\ 0.55 & -1.80 & 2.65 \end{pmatrix}
\label{eq:eq-5-4}
\end{equation}

The magnitude is $|\mathcal{C}| = \sum_{i,j} (Z^{-1})_{ij} \approx 2.45 - 1.35 + 0.55 - 1.35 + 3.00 - 1.80 + 0.55 - 1.80 + 2.65 \approx 2.90$---less than the cardinality 3 of the role inventory. The deficit $3 - 2.90 = 0.10$ is small because these three core arguments are relatively independent (the S–P overlap of 0.40 is the main source of redundancy). By contrast, an accusative alignment—which merges S and A into a single NOM role—would yield a 2-object category with magnitude exactly 2.0, and the deficit $3 - 2.0 = 1.0$ quantifies the information lost by neutralization.

**Scaling to full categories.** Our `EnrichedCategory` implementation computes magnitude for any case category. For the standard 8-case English category with empirically calibrated distributional proximity values, the magnitude is approximately 5.2—the deficit $8 - 5.2 = 2.8$ reflects distributional overlap: NOM and ACC share transitive contexts, DAT and ACC overlap in double-object constructions, and the peripheral cases (VOC, ABL) are relatively independent. This magnitude differential provides a quantitative formalization of Silverstein's [-@silverstein1976hierarchy] case hierarchy: languages with more alignment-based neutralization (lower magnitude) have less relational discriminability, while richer case inventories (higher magnitude) make finer-grained relational distinctions.

Bradley [-@bradley2021entropy] established a link connecting categorical magnitude to classical information entropy via topological operad derivations. Her result proves that Shannon entropy acts as the unique algebraic derivation of a specific topological operad—a categorical structure governing the composition of enriched categories. This supplies theoretical justification for magnitude as a measurable geometric invariant quantifying linguistic complexity: the magnitude of any case category quantifies how much irreducible "information" that case system encodes regarding relational meaning.

Leinster and Shulman [-@leinster2021magnitude] further develop **magnitude homology**, which categorifies magnitude from a scalar invariant to a graded homological invariant—detecting not just the "effective number" of objects but the higher-dimensional "holes" in the distributional landscape. For case categories, magnitude homology can distinguish between two systems with the same magnitude but different topological structure: a category where NOM–ACC–DAT form a tight cluster and all other cases are isolated looks identical in magnitude to one where the clustering is evenly distributed, but their magnitude homology groups differ, revealing that the former has a 1-dimensional "hole" (a missing transitive link) that the latter fills. This finer invariant provides a richer classification of case systems than magnitude alone.

## Language as Enriched Category: Transformer Attention Weights Are Context-Dependent Hom-Values

Bradley's [-@bradley2024ipam; -@bradley2025tea] broader program treats natural language itself as an enriched category, where:

- **Objects** are expressions (words, phrases, sentences)
- **Hom-values** encode distributional co-occurrence probabilities
- **Composition** models transitivity of distributional relatedness

This "language as enriched category" perspective has profound implications for case theory:

1. **Case roles emerge from distributional structure**: Rather than being imposed a priori, case distinctions arise from clusters of high hom-values in the enriched language category. Nouns that frequently appear in agent contexts cluster together, forming the "nominative" region of the category.

2. **Alignment types correspond to enriched structure**: Different languages partition the enriched category differently, and these partitions correspond to the alignment types (accusative, ergative, etc.) discussed in \autoref{sec:case-systems}.

3. **Language models are enriched functors**: A neural language model (such as a transformer) can be viewed as an enriched functor from the syntactic category to the semantic category, mapping type-logical derivations to distributional meaning representations while preserving the enriched structure.

The deep connection to modern distributional semantics is this: static embeddings operationalize hom-values as cosine similarity in a learned space, while contextualized transformers [@devlin2019bert; @vaswani2017attention] compute *dynamic* hom-values from sentential context—a move from a fixed enriched category to a parameterized one. The attention-as-enriched-cup analogy (developed in \autoref{sec:categorical-semantics}) carries the same intuition here: layer-wise weights grade how strongly tokens couple, alongside Bradley et al.'s [-@fritz2021enriched] probabilistic reading of hom-objects.

## Lawvere's Insight: Case Categories Are Similarity Spaces

The $[0,1]$-enrichment connects to a deep tradition in categorical algebra. Lawvere showed that metric spaces are categories enriched over $([0, \infty], +, 0)$: the hom-value is the distance between points, the identity axiom says $d(x, x) = 0$, and the composition inequality is the triangle inequality $d(x, z) \leq d(x, y) + d(y, z)$. Our $[0,1]$-enrichment is the multiplicative analogue: hom-values are *similarities* rather than distances, and the composition inequality is sub-multiplicative rather than sub-additive.

This Lawvere-style perspective unifies our case categories with the geometry of distributional semantics: case roles are points in a "similarity space," and morphisms between them are paths weighted by distributional proximity. The magnitude of this space then quantifies the "effective dimensionality" of the case system—how many independent relational distinctions the language makes.



---




# Topos-Theoretic Bridges: Transferring Results Across Case-Theoretic Frameworks {#sec:topos-theory}

## The Inter-Theoretic Translation Problem

The preceding sections constructed four formally distinct perspectives on case: typological, type-logical, distributional, and enriched. A central methodological question arises: *when can structural results proved in one framework be carried over to another without starting from scratch?* Caramello's [-@caramello2016bridges] topos-theoretic bridge technique answers this for properties that are **invariants of a shared classifying topos**, once Morita equivalence or a suitable bridge is in hand.

## Classifying Toposes: The Logical Shape of a Theory

### A Topos Is a Universe With Internal Logic

A **topos** is a category possessing the structural richness of a generalized "universe of sets": products, exponentials, and a subobject classifier (a "truth-value object") that supports internal first-order reasoning. The most familiar example is the category **Set** of ordinary sets; other important instances include presheaf categories $[\mathcal{C}^{\text{op}}, \mathbf{Set}]$ and sheaf categories over topological spaces. Intuitively, a topos provides a *self-contained logical universe* within which mathematical reasoning can proceed—and different toposes encode different logical constraints.

### Morita Equivalence: Invariant Transfer Across Typologies

Every *geometric theory* $\mathbb{T}$ (axiomatized by sequents with finite conjunctions, arbitrary disjunctions, and existential quantification) generates a unique **classifying topos** $\mathcal{E}_{\mathbb{T}}$: a canonical topos whose models correspond one-to-one with geometric functors out of $\mathcal{E}_{\mathbb{T}}$. The classifying topos encodes the theory's "logical shape" independently of any particular model.

Caramello's insight [-@caramello2016bridges; -@caramello2021five] is that formally different theories can share the same classifying topos up to geometric equivalence—a relation termed **Morita equivalence**. When $\mathcal{E}_{\mathbb{T}_1} \simeq \mathcal{E}_{\mathbb{T}_2}$, any property expressible as an invariant of the shared topos transfers automatically from $\mathbb{T}_1$ to $\mathbb{T}_2$ without re-proof.

## A Chain of Morita Equivalences Connects Case Theories

### Formalizing Case Theories as Geometric Theories

We formalize each case-theoretic framework as a geometric theory:

1. **Typological case theory** $\mathbb{T}_{\text{typ}}$: Objects are case roles, morphisms are grammatical relations, axioms specify alignment constraints (e.g., "S = A" in accusative alignment).

2. **Type-logical case theory** $\mathbb{T}_{\text{log}}$: Objects are syntactic types, morphisms are Lambek calculus derivations, axioms specify well-formedness conditions (pregroup contractions).

3. **Distributional case theory** $\mathbb{T}_{\text{dist}}$: Objects are vector spaces, morphisms are linear maps, axioms specify the composition law for distributional meaning (DisCoCat).

4. **Enriched case theory** $\mathbb{T}_{\text{enr}}$: Objects are expressions, morphisms carry $[0,1]$-valued weights, axioms specify the identity and composition inequalities.

### The Bridge Theorem: Morita Equivalence Chain

The **research programme** we pursue is that these four perspectives admit a topos-theoretic alignment: formally distinct case theories should be related by bridge toposes and, where Morita equivalence can be established, invariants proved in one formulation transfer without re-proof. Equation (\ref{eq:eq-6-1}) sketches the *target* picture—a chain of classifying toposes linked by intermediate geometric theories—not a single theorem asserted for all details in this manuscript.

\begin{equation}
\mathcal{E}_{\mathbb{T}_{\text{typ}}} \leftarrow \mathcal{E}_{\mathbb{T}_{\text{bridge}}} \rightarrow \mathcal{E}_{\mathbb{T}_{\text{log}}} \leftarrow \mathcal{E}_{\mathbb{T}_{\text{bridge}'}} \rightarrow \mathcal{E}_{\mathbb{T}_{\text{dist}}}
\label{eq:eq-6-1}
\end{equation}

Intermediate toposes would be supplied by geometric theories simultaneously interpretable in both flanking frameworks. *Were* such Morita equivalences established, one would expect:

- **Syntactic theorems port to semantics**: Commutativity results in the type-logical setting would align with compositionality statements in the distributional setting.
- **Typological universals constrain distributional models**: Alignment types (accusative, ergative) would impose structural constraints on the vector-space data of DisCoCat-style models.
- **Enriched structure enriches all frameworks**: $[0,1]$-valued weights could be pulled back to probabilistic readings of typological, logical, and distributional constructions.

The Python `topos` module does **not** implement general classifying toposes or full Morita equivalence proofs; it constructs finite **invariant profiles** (sort counts, symbol arities, axiom tallies) from `CaseCategory` instances and uses those profiles for `check_morita_equivalence()` and guarded `bridge_transfer()`—a concrete, testable proxy for the diagram in (\ref{eq:eq-6-1}), not a replacement for topos-level equivalence.

\autoref{fig:functor-alignment} visualizes the alignment functor between the Accusative and Ergative category instantiations, showing how the same eight case roles are connected by different morphism structures under different alignment types.

![The alignment functor preserves role inventory but restructures morphism grouping. Functor $F\colon\mathcal{C}_{\text{acc}} \to \mathcal{C}_{\text{erg}}$ mapping the Accusative case category (source, blue panel) to the Ergative (target, amber panel). All eight case roles appear in both; purple horizontal arrows show the object-level mapping $F(\text{role})$. The key structural difference: Accusative groups $\{S, A\} \to \text{NOM}$ (kernel $\{(S,A)\}$, cf. \autoref{eq:eq-2-3}), while Ergative groups $\{S, P\} \to \text{ABS}$ (kernel $\{(S,P)\}$, cf. \autoref{eq:eq-2-4}). This diagram provides one link in the Morita equivalence chain of \autoref{eq:eq-6-1} enabling inter-theoretic bridge transfer. Generated programmatically from the `AlignmentFunctor` class.](output/figures/functor_alignment.png){#fig:functor-alignment}

## Phillips: LoT Properties Arise as Universal Topos Constructions

Phillips [-@phillips2024lot] provides a striking application of topos-theoretic methods to cognitive science. He shows that the **Language of Thought** (LoT) hypothesis—the claim that cognition operates over structured, combinatorial representations with language-like properties—can be formalized categorically, and that the resulting structure is *universal* in the topos-theoretic sense.

Specifically, Phillips demonstrates that:

1. LoT properties (discrete constituents, role-filler independence, systematicity) arise as **universal constructions** in a topos—categorical products, fiber bundles, and presheaves.

2. Every topos supports an internal first-order logic, explaining how LoT-like logical capacities can emerge in systems (biological or artificial) whose internal architecture forms a topos.

3. The "shape" of cognitive representations is fundamentally **topological**, captured by presheaves and fiber bundles rather than by point-set structures.

Applied to case theory, Phillips's result is significant: because the Language of Thought is topos-universal, and our case categories are definable within any topos (as small categories governed by first-order axioms), every cognitive system with LoT-like architecture has the structural capacity to represent case assignments. This grounds the claim that case structure is a universal feature of higher cognition in the mathematical framework of topos theory rather than in typological observation alone.

## Caramello's Learning Algorithm

Caramello [-@caramello2023syntactic] extends the bridge technique to a learning theory: she shows that classifying toposes can be used to *learn* the theory of a mathematical structure from finite data (a finite set of models). The learning algorithm constructs a classifying topos from the observed data and then extracts the axioms of the underlying theory.

Applied to case systems, this suggests a principled approach to *grammatical induction*: given a corpus annotated with case labels, one could construct the classifying topos of the implicit case theory and read off its axioms—recovering the alignment type, the morphism structure, and the enriched weights from data alone. The procedure operates in four phases:

1. **Extraction**: Parse a Universal Dependencies treebank for a target language, collecting all case-labeled dependency arcs. Each arc $(r_1, \text{rel}, r_2)$ instantiates a morphism $r_1 \to r_2$ in the implicit case category.
2. **Saturation**: Close the extracted morphism set under composition, identity, and the enriched weight constraints of \autoref{sec:enriched-categories}. Compute the empirical hom-values as normalized co-occurrence frequencies.
3. **Classification**: Construct the classifying topos $\mathcal{E}_{\mathbb{T}}$ from the saturated theory—the canonical topos whose models are exactly the case-assignment patterns attested in the corpus. The topos-theoretic invariants (sort count, arity distribution, axiom count) combined with the magnitude and magnitude homology invariants of the enriched theory (\autoref{sec:enriched-categories}) provide a multi-dimensional fingerprint of the language's case system.
4. **Identification**: Compare the fingerprint against the Morita equivalence classes of known alignment types. If the classifying topos matches an existing class, the language's alignment type is identified; if not, the procedure has discovered a novel alignment pattern.

This topos-theoretic learning procedure would be provably correct (recovering the true theory in the limit) and maximally general (not presupposing any particular alignment type). The magnitude invariant from \autoref{sec:enriched-categories} enters at step 3 as a scalar summary of the learned category's "effective size," while magnitude homology provides a finer-grained topological signature.

## Morita Equivalence Diagrams Are Themselves Free-Ride Inferences

The bridge technique has a natural diagrammatic interpretation. Morita equivalence between theories is witnessed by *functorial translations*—diagrams in the 2-category of toposes that commute up to natural isomorphism. These diagrams serve the same cognitive function as the commutative diagrams of \autoref{sec:introduction}: they make the transfer of structure visible, allowing a researcher to verify at a glance that a result proved in one framework genuinely applies in another.

Manders [-@manders2008euclidean] observed that even in classical mathematics, diagrams serve not merely as illustrations but as *inferential instruments* whose spatial properties encode proof-relevant information. The topos-theoretic bridge diagrams extend this observation to the meta-theoretical level: the commutative diagram expressing Morita equivalence is itself a "free ride" inference, automatically transferring any topos-invariant property from one theory to another without requiring a case-by-case verification.

**Illustrative transfer (conditional on a bridge).** The transitive pregroup derivation $n \cdot (n^r \cdot s \cdot n^l) \cdot n \to s$ yields the same sentence type whether contractions are grouped left-to-right or right-to-left. That type-logical commutativity is mirrored in DisCoCat by functoriality: the sentence vector for a fixed derivation is well-defined. A full Morita story would package such facts as invariants of a shared classifying topos; here we use the example only to show *what kind* of statement the bridge programme is meant to align across $\mathbb{T}_{\text{log}}$, $\mathbb{T}_{\text{dist}}$, and enriched formulations—not as a claim that every step of (\ref{eq:eq-6-1}) is already proved for our case theories.

## Python Implementation: build_typological_theory(), check_morita_equivalence(), bridge_transfer()—All Working

The topos-theoretic narrative above is paired with a `topos` Python module that implements **finite geometric theories** extracted from `CaseCategory`, **invariant-profile comparison** (`check_morita_equivalence`), and **guarded bridge transfer** when profiles match—not a full classifying-topos construction inside the runtime.

### Geometric Theories from Case Categories

The `build_typological_theory()` function constructs a geometric theory $\mathbb{T}_{\text{typ}}$ from a `CaseCategory` by extracting:

- **Sorts**: the case roles (objects of the category)
- **Function symbols**: the morphisms with their source/target pairs
- **Axioms**: identity morphism existence, composition closure, and alignment constraints

For the standard 8-case category, this yields a theory with 8 sorts and approximately 15 function symbols. The minimal 3-case category produces a theory with 3 sorts and 5 function symbols. Our `build_enriched_theory()` function further annotates the geometric theory with $[0,1]$-valued hom weights from the enriched structure of \autoref{sec:enriched-categories}.

### Classifying Toposes: The Logical Shape of a Theory

The `ClassifyingTopos` class computes topological invariants—number of sorts, function arity distribution, and axiom count—that characterize the "logical shape" of a theory. Two theories are **Morita equivalent** when their classifying toposes share the same invariant profile:

```python
T_std = build_typological_theory(standard_case_category())
T_min = build_typological_theory(minimal_case_category())
equivalent = check_morita_equivalence(T_std, T_min)
# False: 8-sort and 3-sort theories have different invariants
```

The `bridge_transfer()` function implements the transfer mechanism: given two Morita-equivalent theories, it constructs the functorial translation that carries properties (alignment constraints, composition laws) from one to the other. The transfer is blocked when Morita equivalence fails, preventing unsound cross-theoretic reasoning—a computational enforcement of the mathematical constraint.



---



# Active Inference as a Process Theory of Case {#sec:cognitive-integration}

## Static Categories Are Not Enough

The preceding sections constructed a mathematical infrastructure for analyzing case systems—categorical, type-logical, distributional, enriched, and topos-theoretic. Yet these frameworks remain *static*: they describe the structure of case grammar without explaining how a cognitive agent *deploys* that structure during real-time comprehension and production. Bridging this gap requires a dynamic *process theory* of case-marked relational reasoning.

Active inference [@friston2017active] provides exactly this missing dynamic computational layer.

## Surprise Minimization as Case Parsing

### Free Energy Bounds Surprisal

Active inference is the primary process theory derived from the free energy principle (FEP): every self-organizing system maintains its structural integrity by minimizing the surprisal (negative log-probability) of its sensory observations under an internal *generative model* of its environment [-@friston2010free]. The system executes this minimization through two complementary strategies:

1. **Perceptual inference**: Update internal beliefs to better predict current observations (reduce prediction error)
2. **Active inference**: Act on the environment to bring observations in line with predictions (reduce expected prediction error)

Recent extensions of active inference to linguistics and cognitive science have modeled language comprehension and production as forms of sequential Bayesian inference. As Donnarumma, Frosolone, and Pezzulo (2023) demonstrate in their integration of large language models and active inference for modelling eye movements in reading, linguistic processing constitutes "inference over a hierarchical generative model, facilitating predictions and inferences at various levels of granularity, from syllables to sentences" [-@donnarumma2023integrating]. Similarly, Friston et al. (2021) have demonstrated how communication emerges between synthetic subjects: "linguistic outcomes (specifically, the spoken word)... are selected to minimise the free energy given current beliefs" via "high-order interactions among abstract (discrete) states in deep (hierarchical) models" [-@friston2021understanding; -@friston2020generative].

Both strategies minimize the same mathematical quantity—variational free energy—and both draw from a single generative model encoding the system's prior expectations about the relational structure of its world.

Critically, recent neurolinguistic evidence directly supports this prediction-error account. Li and Futrell [-@li2023decomposition; -@li2024shallow] decompose surprisal into two orthogonal components: *heuristic surprise* ("shallow surprisal"), which tracks the N400 brain potential and reflects lexical-associative prediction error, and a *discrepancy signal* ("deep surprisal"), which tracks the P600 and reflects structural reanalysis when the true parse diverges from the initially inferred structure. This decomposition maps directly onto our enriched case framework: the N400 corresponds to distributional prediction error *within* a case-role subspace (semantic mismatch), while the P600 corresponds to structural prediction error *between* case-diagram topologies (morphosyntactic reanalysis requiring a change in the generative model's case assignments). The formal equations in \autoref{sec:daif-results} (\autoref{eq:eq-7c-n400}–\autoref{eq:eq-7c-p600}) instantiate exactly this dual decomposition.

#### Generative Models of Relational Structure

Under this paradigm, language understanding manifests as *active inference over relational structure*: the listener maintains a generative model anticipating who-does-what-to-whom, and each incoming word supplies evidence that updates this model. Morphological case marking provides high-precision evidence—for example, a nominative suffix predicts that the noun phrase functions as the agent, reducing uncertainty about the relational structure of the unfolding event.

#### S-HAI: The Case Diagram as the Abstract "Schema" Level

These relational generative models find their formal articulation in recent advances such as **Schema-Based Hierarchical Active Inference (S-HAI)** [@maele2026schema]. Unifying predictive processing with schema theory, S-HAI employs a dual-level POMDP structure to model rapid generalization across environments. In the linguistic domain, the "Level 2" model encodes abstract, hidden relational goals---which corresponds exactly to the *case diagram structure* we describe here. The "Level 1" model encodes concrete sensorimotor navigation---for linguistics, this maps to the sequential parsing of surface word forms.

Just as S-HAI explains sudden "zero-shot" behavioral remapping in novel environments by preserving the high-level schema mapping while updating the "grounding likelihoods" to new observables, a case frame enables an agent to rapidly generalize the relational structure of a complex sentence regardless of novel vocabulary pairings. The abstract string diagram is the schema; case inflection is the grounding likelihood.

### Five-Step Generative Loop

The process unfolds as follows:

1. **Prior**: The listener has a prior belief about the relational structure (a "case diagram" encoding expected roles and their connections)
2. **Observation**: Each word provides sensory evidence—its form, its case marking, its distributional properties
3. **Update**: The listener updates the case diagram to accommodate the evidence, using approximate Bayesian inference (typically variational message passing)
4. **Prediction**: The updated diagram generates predictions about upcoming words (case-marked NPs, verb valency patterns)
5. **Action**: In production, the speaker selects words and case markers that minimize expected free energy—choosing expressions that are informative, contextually appropriate, and syntactically well-formed

### Case Diagrams as Instantiated Situations

This dynamic active inference perspective connects naturally to **situation semantics** (Barwise and Perry [-@barwise1983situations]), which treats linguistic meaning as structured situations—specific configurations of individuals, relations typed by arity, and spatiotemporal locations, grounded in an ecological realism where meanings are recurring relational patterns that organisms attune to. Translated into our categorical framework, a **situation** is an instantiated case diagram: a specific assignment of entities to roles with particular morphisms activated; the **situation type** is the structural case category itself, the abstract pattern that any particular situation instantiates; and **information flow** between situations is a functorial mapping between case categories. Where classical situation semantics left the dynamics implicit, active inference supplies the computational engine: the agent moves through situations in real time, updating its case diagram with each incoming word and using the updated diagram to predict which situation will arise next.

### Belief Dynamics Over Competing Case Frames

\autoref{fig:active-inference-belief} shows a minimal **scalar-belief** simulation: the agent holds a `CaseDiagramBelief` over alternative alignment frames (NOM--ACC vs. ERG--ABS). As syntactic evidence arrives, variational free energy for the inconsistent frame rises and the posterior concentrates on the frame that fits the generative model---the same discrete update loop that \autoref{sec:daif-results} extends to full return distributions in DAIF. Generated programmatically from `src/visualization/active_inference_plots.plot_belief_distribution()`.

![Variational free energy drives convergence to the correct case frame during belief updating. The agent starts with a uniform prior over possible case frames (NOM-ACC vs. ERG-ABS). As categorical evidence is sampled from a TQNN-evaluated diagram, free energy for the incorrect frame rises while the posterior for the correct frame converges to certainty. This demonstrates dynamic surprisal minimization governed by the diagrammatic structure of the generative model.](output/figures/active_inference_belief.png){#fig:active-inference-belief}



---



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



---



# DAIF: The Convergence of Distributional Semantics and RL {#sec:daif-results}

A remarkable convergence has emerged between *distributional semantics* in linguistics and *distributional reinforcement learning* in machine learning, mediated by active inference. Akgül et al. [-@akgul2026distributional] parameterize this in **Distributional Active Inference (DAIF)**, which embeds active inference within the distributional RL framework of Bellemare, Dabney, and Munos [-@bellemare2017distributional]. Where classical RL optimises *expected* returns (scalar values), distributional RL models the *full distribution* of returns—a shift from point estimates to distributional representations that parallels the shift from symbolic to distributional semantics in linguistics. Crucially, as recent convergences demonstrate, estimating full distributions over discounted returns substantially enhances sample efficiency and buffers aleatoric uncertainty, factors essential for biological plausibility during rapid linguistic parsing.

The terminological collision between "distributional" in distributional semantics and "distributional" in distributional RL is not mere homonymy—it reflects a deep structural parallel. In both domains, the core computational move is the same: **replacing scalar summaries with full distributional representations.** In linguistics, this means contextualizing word identities via probability distributions (Firth's [-@firth1957papers] company-keeping principle). In reinforcement learning, it replaces expected-value estimates with quantile-approximated return distributions. In active inference, it replaces point estimates of states with variational posterior distributions. The enriched-categorical framework of \autoref{sec:enriched-categories} provides the unifying abstraction: all three are instances of $[0,1]$-enriched categories where hom-values encode distributional proximity rather than rigid identity.

This section presents the complete implementation and quantitative results of the `src/daif/` subpackage—seven modules, 24 public symbols, 161 automated tests—covering six major computational contributions: push-forward returns (\autoref{sec:daif-pushforward}), quantile TD and implicit quantile networks (\autoref{sec:daif-quantile}), variational message passing and Bethe free energy (\autoref{sec:daif-vmp}), policy selection and expected free energy (\autoref{sec:daif-policy}), unifying ERP amplitude profiles (\autoref{sec:daif-erp}), and convergence diagnostics (\autoref{sec:daif-metrics}).

## Push-Forward Returns and the Distributional Bellman Operator {#sec:daif-pushforward}

The formal architecture of DAIF proceeds through three stages: (1) reconstructing active inference via variational Bayesian inference on a controlled Markov process; (2) defining a *push-forward* operation that iteratively maps latent-space trajectories to return distributions; and (3) deriving a temporal-difference quantile-matching algorithm that achieves active inference's sample-efficiency advantages within a model-free computational architecture. This permits far-sighted parsing without explicit transition modeling:

\begin{equation}
\mathbb{E}\left[\sum_{t=0}^{\infty} \gamma^t R(x_t, a_t) \mid x_0, a_0\right] = \int_{\mathcal{S}^{\mathbb{N}_+}} R \circ f \, d(\mathbf{S}_{\#} \mathbb{P}_{x_0, a_0}^{P_\pi})
\label{eq:eq-7-1}
\end{equation}

where $\mathbf{S}_{\#}$ denotes the push-forward measure on representation paths, $f: \mathcal{S} \to \mathcal{X}$ is the stochastic decoder, and $\gamma \in (0,1)$ is the discount factor. The `push_forward_return()` function in `src/daif/core.py` computes this via an atomised categorical projection over $N_{\mathrm{atoms}}$ support points $\{z_i\}_{i=1}^{N_{\text{atoms}}}$ spanning $[V_{\min}, V_{\max}]$—the C51 architecture of Bellemare et al. [-@bellemare2017distributional]:

\begin{equation}
Z(s,a) = \sum_{i=1}^{N_{\text{atoms}}} p_i(s,a) \cdot \delta_{z_i}
\label{eq:eq-7c-c51}
\end{equation}

where $p_i(s,a)$ is the probability assigned to support point $z_i$ and $\delta$ is the Dirac delta mass. The distributional Bellman operator $\mathcal{T}^{\pi}$ then maps return distributions forward:

\begin{equation}
\mathcal{T}^{\pi} Z(s,a) \stackrel{d}{=} R(s,a) + \gamma Z(S', A'), \quad S' \sim P(\cdot|s,a), \; A' \sim \pi(\cdot|S')
\label{eq:eq-7c-bellman}
\end{equation}

For case-theoretic reasoning, DAIF implies a computational architecture in which case assignment operates distributionally at every level: the agent maintains not a single case diagram but a *distribution over case diagrams*, weighted by their posterior probability given the observed linguistic evidence. This distributional perspective on case assignment aligns naturally with the graded proto-role structure of Dowty [-@dowty1991thematic]: a noun phrase distributes probability mass across case roles, with the distribution sharpening as more evidence accumulates.

## Quantile Temporal Difference and Implicit Quantile Networks {#sec:daif-quantile}

Rather than representing the return distribution as a fixed categorical support (C51), the Quantile Regression DQN (QR-DQN) approach represents it as a uniform mixture of $N$ Dirac masses, one at each quantile level $\tau_i = (2i-1)/2N$. The `quantile_td_update()` function implements the Huber quantile loss:

\begin{equation}
\mathcal{L}_{\text{QR}}(\theta) = \frac{1}{N N'} \sum_{i=1}^{N} \sum_{j=1}^{N'} \rho_{\tau_i}^{\kappa}\!\left(\delta_{ij}\right)
\label{eq:eq-7c-qr}
\end{equation}

where $\delta_{ij} = r + \gamma z_j' - z_i$ is the temporal-difference error, and the Huber quantile loss $\rho_{\tau}^{\kappa}$ is:

\begin{equation}
\rho_{\tau}^{\kappa}(u) = |\tau - \mathbf{1}[u < 0]| \cdot \mathcal{L}_{\kappa}(u), \quad \mathcal{L}_{\kappa}(u) = \begin{cases} \frac{1}{2}u^2 & |u| \leq \kappa \\ \kappa(|u| - \frac{\kappa}{2}) & \text{otherwise} \end{cases}
\label{eq:eq-7c-huber}
\end{equation}

The **Implicit Quantile Network** extension (`implicit_quantile_network_update()` in `src/daif/quantile.py`) samples quantile levels $\tau \sim U[0,1]$ at inference time, enabling risk-distorted policy selection via four modes:

| Mode | Distortion $\beta{}(\tau{})$ | Semantic Role |
| :--- | :--- | :--- |
| **neutral** | $\beta{}(\tau{}) = \tau{}$ | Standard expected-value maximisation |
| **optimistic** | $\beta{}(\tau{}) = \tau{}^{1/(1+\eta{})}$ | Prefers high-return tails; suits exploratory parsers |
| **pessimistic** | $\beta{}(\tau{}) = \tau{}^{1+\eta{}}$ | Over-weights low-return tails; conservative case disambiguation |
| **CVaR** | $\beta{}(\tau{}) = \min(\tau{}/\alpha{}, 1)$ | Conditional Value-at-Risk at level $\alpha{}$; risk-averse comprehension |

The `wasserstein_return_distance()` function computes both $W_1$ (absolute area between CDFs) and $W_2$ (squared area) distances between return distributions, providing a principled metric for comparing case-assignment belief states across sentence positions.

## Variational Message Passing and Bethe Free Energy {#sec:daif-vmp}

The `variational_message_passing()` function in `src/daif/inference.py` implements iterative belief refinement over the case-role posterior $q(\mathbf{c} \mid \mathbf{o})$. Starting from a uniform prior over $K$ case roles, each observation $o_t$ (an incoming morphologically marked word) triggers a VMP update:

\begin{equation}
q^{(t+1)}(c_k) \propto q^{(t)}(c_k) \cdot \exp\!\bigl(\mathbb{E}_{q^{(t)}_{-k}}\!\bigl[\log p(o_t \mid c_k)\bigr]\bigr)
\label{eq:eq-7c-vmp}
\end{equation}

followed by renormalisation. The algorithm returns log-beliefs, final probabilities, and iteration count. Convergence is declared when $\|q^{(t+1)} - q^{(t)}\|_1 < \epsilon = 10^{-6}$.

The **Bethe free energy** provides a tractable lower-bound approximation to the variational free energy:

\begin{equation}
F_{\text{Bethe}}[\mathbf{q}] = \underbrace{-\sum_k q(c_k) \log p(c_k)}_{\text{prior fit}} + \underbrace{\sum_k q(c_k) \log q(c_k)}_{\text{belief entropy}} - \underbrace{\sum_t \sum_k q(c_k) \log p(o_t \mid c_k)}_{\text{likelihood}}
\label{eq:eq-7c-bethe}
\end{equation}

`bethe_free_energy()` in `src/daif/inference.py` computes this quantity for any belief distribution and observation set. The **expected information gain** (`expected_information_gain()`) measures the KL divergence between posterior and prior:

\begin{equation}
\text{EIG}(o) = D_{\mathrm{KL}}\bigl(q(\mathbf{c} \mid o) \;\|\; p(\mathbf{c})\bigr)
\label{eq:eq-7c-eig}
\end{equation}

\autoref{fig:daif-free-energy} visualises the Bethe free energy landscape over six sequential word arrivals in the sentence *"Der Hund jagt die Katze schnell"*: variational free energy decreases with each belief update cycle, and the KL decomposition shows the balance between model complexity ($D_{\mathrm{KL}}(q\|p)$) and data fit ($-\mathbb{E}_q[\log p(o|s)]$).

![Variational free energy decreases monotonically with each word arrival during distributional case assignment. **Left**: variational free energy $F[q]$ over DAIF iterations with vertical dashed lines marking word arrivals; each word triggers a new belief update cycle. **Right**: KL divergence decomposition showing $D_{\mathrm{KL}}(q\|p)$ (model complexity) versus $-\mathbb{E}_q[\log p(o|s)]$ (data fit accuracy), demonstrating the balance between parsimony and fidelity during case inference. Generated programmatically from `src.visualization.daif_plots.plot_free_energy_convergence()` (curves from `DAIFResult` produced by `src/daif/inference.py`).](output/figures/daif_free_energy_convergence.png){#fig:daif-free-energy}

\autoref{fig:daif-belief-trajectory} illustrates the full belief trajectory: starting from uniform prior over NOM, ACC, DAT, INS, the posterior sharpens monotonically as each morphologically marked word supplies evidence. The determiner *Der* signals nominative; the transitive verb *jagt* activates a valency frame expecting an accusative object; the accusative article *die* confirms NOM=Hund, ACC=Katze. Entropy $H[q]$ (centre panel) drops steeply at the second word—the most informative item in this parse.

![Case-role posterior sharpens from uniform prior as German morphology supplies evidence. DAIF belief trajectory during sequential disambiguation of *"Der Hund jagt die Katze schnell."* **Top**: stacked area showing P(NOM), P(ACC), P(DAT), P(INS) evolution over six words with German morphological glosses. **Middle**: entropy $H[q]$ with annotated steepest drop marking the most informative word. **Bottom**: push-forward return distribution as a quantile fan chart (10th--90th percentile) showing distributional uncertainty narrowing as the parse progresses. Generated programmatically from `src.visualization.daif_plots.plot_belief_trajectory()` (beliefs from `src/daif/` inference and `push_forward_return()` in `core.py`).](output/figures/daif_belief_trajectory.png){#fig:daif-belief-trajectory}

## Policy Selection and Expected Free Energy {#sec:daif-policy}

Active inference selects actions (here: next-word predictions or syntactic commitments) by minimising *expected free energy* $G{(\pi)}$, which decomposes into a pragmatic term (instrumental value) and an epistemic term (information gain):

\begin{equation}
G(\pi) = \underbrace{-\mathbb{E}_{q(o|\pi)}[\log p(o)]}_{\text{pragmatic value}} + \underbrace{D_{\mathrm{KL}}(q(s|\pi) \| p(s))}_{\text{epistemic value}} + \beta \cdot \text{risk}(\pi)
\label{eq:eq-7c-g}
\end{equation}

where $\beta \geq 0$ is the risk-sensitivity parameter. The `G_policy()` function in `src/daif/policy.py` computes this for any policy $\pi{}$ given a current belief state. Policy selection follows a Boltzmann (softmax) distribution over negative EFE:

\begin{equation}
P(\pi) = \frac{\exp(-\alpha \cdot G(\pi))}{\sum_{\pi'} \exp(-\alpha \cdot G(\pi'))}
\label{eq:eq-7c-softmax}
\end{equation}

where $\alpha > 0$ is the inverse temperature. `softmax_policy_selection()` implements this across an array of candidate policies; `distributional_epistemic_value()` returns the epistemic component alone, enabling decomposition of the policy gradient.

For case-theoretic reasoning, this means the agent selects the case assignment (NOM/ACC/DAT/etc.) that simultaneously minimises surprise (fits the observed morphological evidence), maximises information gain (resolves ambiguity fastest), and respects risk sensitivity (avoids high-variance parses in pessimistic mode). This provides a principled, Bayes-optimal account of why certain parse strategies are preferred cross-linguistically—they minimise expected free energy under the agent's generative model.

## ERP Amplitude Profiles from Distributional Prediction Error {#sec:daif-erp}

The `distributional_prediction_error()` function (`src/daif/prediction.py`) computes the precision-weighted mismatch between the observed return distribution and the predicted distribution:

\begin{equation}
\mathrm{DPE}(o, q) = \pi_f \cdot W_1(Z_{\text{predicted}}, Z_{\text{observed}})
\label{eq:eq-7c-dpe}
\end{equation}

where $\pi_f = \mathcal{C}(A,B) \in [0,1]$ is the enriched morphism weight (precision) of the violated case morphism (matching \autoref{eq:pe-precision-error} in \autoref{sec:diagrammatic-cognition}) and $W_1$ is the Wasserstein-1 distance. This yields direct predictions for psycholinguistic ERP components:

\begin{align}
\mathrm{N400}(c) &= \mathrm{DPE}_{\text{semantic}} \cdot \pi_c \cdot S_{\text{violation}} \label{eq:eq-7c-n400} \\
\mathrm{P600}(c) &= \mathrm{DPE}_{\text{structural}} \cdot (1-\pi_c) \cdot S_{\text{violation}} \label{eq:eq-7c-p600}
\end{align}

where $S_{\text{violation}} \in \{0, 0.5, 1.0\}$ encodes violation severity (congruent / mild / strong) and $\pi_c$ is the enriched weight of the case morphism in question. This dual decomposition directly mirrors the empirical finding of Li and Futrell [-@li2023decomposition; -@li2024shallow], who show that surprisal decomposes into a *heuristic* component tracking N400 and a *discrepancy* component tracking P600—precisely the semantic vs. structural split captured by $\mathrm{DPE}_{\text{semantic}}$ and $\mathrm{DPE}_{\text{structural}}$ above. The `erp_amplitude_profile()` function generates a complete `ERPProfile` dataclass containing:

- **N400 amplitude** (µV) and **peak latency** (ms) for each case role
- **P600 amplitude** (µV) and **peak latency** (ms) for each case role
- **Time-series waveforms** sampled at 1 kHz over a 1000 ms epoch

\autoref{fig:daif-erp-predictions} demonstrates predicted ERP amplitudes across all eight case roles under three violation conditions. A key result: because VOC→NOM is the most structurally inadmissible transition (morphism weight $\approx 0$), it elicits the largest P600; while the GEN→ACC semantic mismatch, with moderate morphism weight, elicits a pronounced N400 but attenuated P600.

![Distributional prediction error predicts graded N400/P600 amplitudes across all eight case roles. **Left**: simulated ERP waveforms for three violation conditions---congruent (NOM→NOM), mild (ACC→NOM), and strong (VOC→NOM)---showing component timing and amplitude scaling per \autoref{eq:eq-7c-n400}--\autoref{eq:eq-7c-p600}. **Middle**: scatter of enriched weight $\pi{}$ versus distributional prediction error (DPE, \autoref{eq:eq-7c-dpe}) for all roles, with regression line and $R^2$. **Right**: predicted versus literature-typical N400/P600 amplitudes. VOC→NOM (weight $\approx 0$) elicits the largest P600; GEN→ACC (moderate weight) elicits a pronounced N400 but attenuated P600. Generated programmatically from `src.visualization.daif_plots.plot_erp_predictions()` (amplitudes from `erp_amplitude_profile()` and related APIs in `src/daif/prediction.py`).](output/figures/daif_erp_predictions.png){#fig:daif-erp-predictions}

## Convergence Diagnostics and Distributional Metrics {#sec:daif-metrics}

The `src/daif/metrics.py` module provides four diagnostic tools for verifying DAIF model behaviour:

**Convergence diagnostics** (`convergence_diagnostics()`) assess whether a free-energy trajectory $\{F^{(t)}\}_{t=0}^{T}$ is well-behaved. Given the free energy sequence produced by VMP, the diagnostics return:

| Metric | Formula | Interpretation |
| :--- | :--- | :--- |
| `is_monotone` | $\forall t: F^{(t+1)} \leq F^{(t)}$ | FE decreasing at every step |
| `relative_reduction` | $(F^{(0)} - F^{(T)}) / \lvert F^{(0)}\rvert$ | Fraction of initial FE eliminated |
| `converged` | $\lvert F^{(T)} - F^{(T-1)}\rvert < \epsilon$ | Reached stable minimum |
| `final_value` | $F^{(T)}$ | Absolute FE at convergence |

**Distributional KL divergence** (`distributional_kl()`) computes the KL divergence between two discrete return distributions:

\begin{equation}
D_{\mathrm{KL}}(P \| Q) = \sum_{i} P(z_i) \log \frac{P(z_i)}{Q(z_i) + \epsilon}
\label{eq:eq-7c-dkl}
\end{equation}

with $\epsilon = 10^{-10}$ for numerical stability. Verified properties: $D_{\mathrm{KL}}(P\|Q) \geq 0$ (Gibbs' inequality), $D_{\mathrm{KL}}(P\|P) = 0$, asymmetry $D_{\mathrm{KL}}(P\|Q) \neq D_{\mathrm{KL}}(Q\|P)$ in general.

**Quantile coverage** (`quantile_coverage()`) measures calibration error—the mean absolute deviation between nominal quantile levels and empirical coverage frequencies:

\begin{equation}
\mathrm{CE} = \frac{1}{N} \sum_{i=1}^{N} \left| \tau_i - \hat{F}(z_{\tau_i}) \right|
\label{eq:eq-7c-ce}
\end{equation}

A perfectly calibrated distributional model achieves $\mathrm{CE} = 0$; the DAIF implementation yields $\mathrm{CE} < 0.01$ on all test cases evaluated in `test_daif_metrics.py`.

**Return distribution entropy** (`return_distribution_entropy()`) quantifies uncertainty in the distributional belief:

\begin{equation}
H[Z] = -\sum_{i=1}^{N_{\text{atoms}}} p_i \log p_i
\label{eq:eq-7c-entropy}
\end{equation}

This links directly to the belief trajectory in \autoref{fig:daif-belief-trajectory}: entropy decreases monotonically as the distributional belief sharpens, providing a scalar summary of parse certainty.

## CEREBRUM: Eight Cases as Functional Specializations {#sec:cerebrum}

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
| **DAIF as distributional layer** | The `src/daif/` subpackage provides the distributional RL layer: full return distributions replace point estimates throughout the generative cycle |

### Case Roles as Functional Specializations in CEREBRUM

CEREBRUM deploys the eight traditional cases as functional specializations, each with a DAIF-level extension:

| Case | CEREBRUM Function | Active Inference Role | DAIF Extension |
| :--- | :--- | :--- | :--- |
| NOM | Primary driver / agent | Source of action policies | Softmax policy over $G{(\pi)}$; highest epistemic value |
| ACC | Primary target / patient | Object of predictions | Predicted distribution $Z_{\text{acc}}$; error-driven update |
| GEN | Source / possessor | Provider of priors | Prior return distribution $p(Z)$ |
| DAT | Recipient / goal | Target of information transfer | EIG maximised toward DAT state |
| INS | Instrument / means | Tool for state transformation | IQN risk distortion (neutral mode) |
| LOC | Context / environment | Markov blanket boundary | Bethe FE boundary conditions |
| ABL | Origin / cause | Source of causal influence | Push-forward source measure $\mathbb{P}_{x_0,a_0}$ |
| VOC | Addressee | Pragmatic pointer | Lowest epistemic weight; largest P600 on violation |



---



# TQNNs and ZX-Calculus {#sec:quantum-active-inference}

The preceding sections have established that categorical string diagrams—from DisCoCat's pregroup derivations (\autoref{sec:categorical-semantics}) through enriched hom-values (\autoref{sec:enriched-categories}) to topos-theoretic transfer (\autoref{sec:topos-theory})—provide a unified diagrammatic language for case-theoretic reasoning. This section extends the framework into its natural quantum generalization: topological quantum neural networks (TQNNs), the ZX-calculus, and sheaf-theoretic quantum semantic communication. The central observation is that the same monoidal-categorical architecture that underlies DisCoCat string diagrams also underlies quantum circuits, TQFT cobordisms, and quantum information flow—making active inference on case-marked relational structure a quantum topological computation.

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

The powerful ZX-calculus provides a diagrammatic language for quantum circuits, representing them as string diagrams in a symmetric monoidal category of finite-dimensional Hilbert spaces and linear maps [@kissinger2020zx]:

> "The ZX-calculus is a graphical language for reasoning about quantum computations and circuits... it can represent any linear map, and can be considered a diagrammatically complete generalization of the usual circuit representation." [@coeckekissinger2017]

Three structural features connect ZX to case-theoretic diagrams:

- **Diagrams as morphisms**: ZX-diagrams are string diagrams in a $\dagger$-compact closed category. Wires represent objects (qubits), spiders and boxes represent morphisms, and composition/tensor product correspond to vertical/horizontal concatenation. Only topology matters, not geometry.
- **Deterministic circuit extraction via generalized flow**: Kissinger and van de Wetering show that quantum circuits map to ZX-diagrams, undergo graph-theoretic rewriting, and extract as optimized circuits—with topological abstraction preserving the invariants needed for optimization [@kissinger2020zx].
- **Category-theoretic semantics**: A ZX-diagram's semantics are determined entirely by how components are wired—the same compositional principle underlying DisCoCat and the case categories of \autoref{sec:case-systems}.

### Cups Are Spiders

The structural parallel between pregroup grammar diagrams and ZX-diagrams is not accidental. Both are instances of the same mathematical object: morphisms in a compact closed monoidal category with functorial semantics into Hilbert spaces. In DisCoCat, the functor assigns to each grammatical type a vector space and to each derivation a linear map computing sentence meaning [@coecke2010mathematical]. In ZX, the standard semantics functor assigns to each spider/Hadamard configuration a linear map in **FHilb**. The shared categorical architecture means:

1. **Pregroup contractions (cups) and ZX spiders** are both instances of the same algebraic operation: evaluation morphisms in a compact closed category.
2. **DisCoCat normal forms** and **ZX simplifications** are both applications of the same rewriting theory: equational reasoning modulo the axioms of a compact closed category.
3. **The snake equation** (Cap $\circ$ Cup = identity) that grounds all pregroup type reductions (\autoref{sec:categorical-semantics}) is a special case of the spider fusion rule in ZX.

This means that case-theoretic DisCoCat derivations can, in principle, be compiled into ZX circuits and executed on quantum hardware—a connection already exploited by the lambeq quantum NLP pipeline [@lorenz2023lambeq].

## One Diagram, Three Interpretations

### Common Language: Ribbon and Tensor Diagrams

Both ZX-diagrams and TQNNs are topological string diagrams evaluated by monoidal functors into the category of Hilbert spaces and linear maps. The alignment becomes explicit when stated precisely:

- **For TQNNs**: A 3-dimensional TQFT functor from a cobordism or skein category to **Hilb** assigns to each spin-network/ribbon graph a linear map representing the TQNN computation. The underlying topological skein theory treats network layers as *ribbon graphs* whose evaluation via Reshetikhin–Turaev and Turaev–Viro invariants gives quantum processes implementing computation and error correction [@fields2022tqnn; @fields2025amplituhedra].
- **For ZX**: The standard semantics functor from the free $\dagger$-compact category generated by Z/X spiders, Hadamards, etc. into **FHilb** assigns each ZX-diagram a linear map [@kissinger2020zx].
- **For DisCoCat**: The meaning functor from the pregroup grammar category to **FdVect** assigns to each grammatical derivation a multilinear map computing compositional meaning [@coecke2010mathematical].

Up to choice of labels and normalization, all three are graphical calculi for monoidal categories whose morphisms are quantum (or quantum-like) processes. A layer of a topological quantum flow network can be modeled as a ZX-diagram fragment whose input and output boundary wires are the "feature spaces" (Hilbert spaces) at successive processing steps, while internal spiders encode unitary/non-unitary channels that realize synaptic transformations.

### Generalized Flow Guarantees Causal Order

The *generalized flow* condition used to guarantee deterministic circuit extraction from ZX-diagrams is a graph-theoretic constraint that ensures a well-defined causal ordering of operations [@kissinger2020zx]. This mirrors the requirement in TQNNs that the diagram encode a consistent *execution trace* of a quantum computation. Fields and colleagues make this connection explicit in their TQNN–amplituhedron correspondence:

> "...this formal correspondence is stated by Theorem 2 whose proof draws upon the concept of execution trace for a quantum computation... and thus leads to representing a TQNN in terms of the positive geometries as provided by amplituhedra." [@fields2025amplituhedra]

A topological quantum flow neural network can therefore be regarded as a ZX-style circuit where the graphical calculus is enriched to a 3D TQFT skein theory, but the *abstract type* of object—a topological string diagram with functorial semantics—remains the same.



---



# Meaning Spaces as Hilbert Spaces {#sec:quantum-semantics}

## $P(c\mid\rho) = \text{Tr}(E_c\rho)$

To connect TQNNs and ZX circuits to *distributional semantics*, we reinterpret the amplitudes and correlations in these topological diagrams as semantic quantities. Recent work on quantum semantic communication supplies the necessary bridge, modeling meaning spaces as Hilbert spaces at nodes of an interaction graph connected by completely positive trace-preserving (CPTP) channels along edges [@thomas2025quantum]:

> "Multi-agent semantic networks are modeled as quantum sheaves, where agents' meaning spaces are Hilbert spaces connected by quantum channels." [@thomas2025quantum]

A *quantum semantic sheaf* over a communication graph $G=(V,E)$ is a triple $(H,F,\rho)$ where each vertex $v$ carries a finite-dimensional semantic Hilbert space $H_v$, edges carry CPTP maps $F_e$, and each vertex holds a density operator $\rho_v$ encoding its current semantic state. This instantiates a distributional-semantics picture: meanings are vectors or density operators in high-dimensional spaces, with co-occurrence and pragmatic context encoded in the functorial connections across the network.

**Case assignment as quantum measurement.** The connection to classical case systems becomes concrete when we model case assignment as a *quantum measurement* on the semantic state. Define POVM elements corresponding to cases $\{E_{\text{NOM}}, E_{\text{ACC}}, E_{\text{DAT}}, \ldots\}$ satisfying $\sum_c E_c = I$, where each $E_c$ projects onto the subspace of semantic states consistent with case role $c$. The probability of assigning case $c$ to a noun phrase in semantic state $\rho$ is:

\begin{equation}
P(c \mid \rho) = \text{Tr}(E_c \rho)
\label{eq:eq-8-1}
\end{equation}

![Overlapping POVM elements produce graded case probabilities via quantum interference. (a) NOM/ACC projectors in a crisp case system: non-overlapping probability density yields deterministic assignment per \autoref{eq:eq-8-1}. (b) Graded case assignment in a proto-role system: overlapping POVM elements create an interference pattern in the semantic belief space, realizing the $[0,1]$-enrichment of \autoref{sec:enriched-categories} as physical measurement. Rotation into a different measurement basis (a different quantum reference frame) corresponds to a different alignment system, e.g., ACC $\to$ ERG. Generated programmatically from `src/visualization/quantum_plots.plot_povm_probabilities()`.](output/figures/quantum_povm_probabilities.png){#fig:quantum-povm}

For crisp case systems (NOM/ACC), the POVM elements are orthogonal projectors ($E_c E_{c'} = \delta_{cc'} E_c$), yielding deterministic case assignment. For graded proto-roles (Dowty's [-@dowty1991thematic] agent/patient continuum), the POVM elements overlap, yielding probabilistic case assignment—precisely the quantum generalization of the $[0,1]$-enrichment from \autoref{sec:enriched-categories}. The enriched hom-value $\mathcal{C}(v, c)$ is identified with $P(c \mid \rho_v)$, grounding the abstract enrichment in physical measurement theory. Fluid-S alignment (\autoref{sec:case-systems}) then corresponds to a context-dependent POVM: the measurement basis rotates depending on the volition feature $\theta$, so the same noun phrase has different case probabilities depending on whether the agent is construing the action as volitional or not.

The same scalar-belief dynamics appear in \autoref{fig:active-inference-belief} (\autoref{sec:cognitive-integration}): variational free energy separates competing case frames before the POVM readout in \autoref{eq:eq-8-1} is applied to semantic density matrices.

## Three Correspondences: Wires, Spiders, and Topology

When this sheaf-theoretic semantics is grafted onto the TQNN/ZX architecture, three structural correspondences emerge:

1. **Edges as semantic feature channels**: In a TQNN or ZX-diagram, each wire carries not merely an abstract qubit but a semantic Hilbert space $H_v$ associated with a context, concept, or agent. Amplitudes or density matrices on that wire encode a distribution over semantic features—exactly as word vectors encode distributional meaning in classical compositional distributional semantics.

2. **Nodes as compositional operations**: Spiders/gates in ZX or intertwiners in TQNNs become *semantic composition maps*: they take distributed meanings on input wires and produce new distributed meanings on output wires, analogous to how DisCoCat composes word meanings into phrase/sentence meanings via multilinear maps.

3. **Topological wiring as contextual structure**: The topology of the diagram—the way wires and nodes are connected—encodes which semantic spaces interact and in what causal/structural pattern. This is the semantic analogue of syntactic structure in distributional semantics, realized as a topological quantum circuit.

In this reading, a topological quantum flow neural network becomes a *distributional semantic machine*: a functor that sends a topological diagram (graph of contexts and interactions) to a family of Hilbert spaces and maps where vectors/densities represent distributed meanings and their probabilistic transformations.

## Sheaf Cohomology Governs Alignment

### Sheaf Cohomology and Semantic Alignment

The sheaf-based framework proves that semantic alignment between agents is governed by cohomology classes of the quantum semantic sheaf; contextuality and entanglement act as resources that remove obstructions to alignment [@thomas2025quantum]:

> "We derive semantic channel capacity when sender and receiver share prior entanglement, proving it strictly exceeds classical capacity. The quantum advantage grows as channel noise increases—precisely when semantic communication most benefits over bit-level transmission." [@thomas2025quantum]

Two further results from this framework are particularly relevant:

- **Contextuality as a semantic resource**: "Quantum contextuality reduces cohomological obstructions to semantic alignment. Contextual correlations act as 'pre-shared semantic resolution,' establishing contextuality as a resource for semantic communication" [@thomas2025quantum].
- **Discord as integrated semantic information**: "Quantum discord equals integrated semantic information, linking quantum correlations to irreducible semantic content and connecting our framework to integrated information theory" [@thomas2025quantum].

These results establish that the topology of the semantic sheaf (and its cohomology) constrains how probabilistic semantic information can be transferred; quantum features (entanglement, contextuality, discord) change these constraints in well-defined ways.

### Topological Circuit as Semantic Sheaf Skeleton

A TQNN/ZX circuit implementing a quantum communication or computation protocol is itself a diagram over which one can define a sheaf of semantic spaces and channels. The underlying graph of the TQNN/ZX diagram serves as the base graph $G=(V,E)$ of the semantic sheaf: vertices inherit meaning spaces $H_v$, edges inherit CPTP maps $F_e$, and the TQFT/ZX functor gives the global linear map representing the protocol. Distributional semantics as diagram evaluation then becomes literal: passing an initial semantic state (distribution over meanings) through the TQNN/ZX diagram yields an output state whose components encode the posterior semantic distributions at boundary wires.

ZX rewrite rules, which change the internal topology of the diagram while preserving its overall semantics as a linear map, correspond to alternative factorizations of the same semantic transformation—different internal "flow architectures" for realizing the same semantic map.

## Case Assignment as Holographic Measurement

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

### Entanglement Strictly Exceeds Classical Semantic Capacity

The sheaf-theoretic results of Thomas and Chen [-@thomas2025quantum] suggest that quantum features provide genuine advantages for semantic communication—not merely computational speedup, but qualitative enhancements in semantic alignment. If case-marked relational structure is communicated between agents via quantum channels, entanglement provides additional semantic capacity, contextuality removes alignment obstructions, and discord captures irreducible semantic content. These are not abstract possibilities but operational consequences of the mathematical framework developed across this review. Recent work by Krawchuk et al. [-@krawchuk2025paramqnlp] demonstrates this concretely: DisCoCirc string diagrams that represent discourse-level semantics (including case role assignments across sentences) can be *automatically* compiled into parameterized quantum circuits, closing the loop from linguistic case structure through categorical formalism to quantum computation.



---




# Categorical AI Protocols {#sec:ai-implications}

## A2A, MCP, ACP, ANP Are Missing Compositional Semantics

The categorical framework developed in the preceding sections—case categories, functorial semantics, enriched structure, and diagrammatic reasoning—provides a structural response to an emerging challenge in modern AI: supplying typed, compositional message semantics that resist semantic collapse.

Current multi-agent AI systems communicate via flat standardized protocols. For instance, the **Model Context Protocol (MCP)** [@anthropic2024mcp] manages tool access by exchanging unstructured `JSON-RPC` payloads. Consider a standard MCP invocation mapping an LLM's intention to a database:

```json
{
  "method": "tools/call",
  "params": {
    "name": "access_database",
    "arguments": { "query": "DROP TABLE users" }
  }
}
```

This payload is structurally blind to its own pragmatic implications. It possesses no inherent algebraic compositionality and enforces no relational typing on the physical execution pathways. Frameworks like Google's Agent-to-Agent (A2A) [@google2025a2a], the Agent Communication Protocol (ACP) [@acp2025protocol], and the Agent Network Protocol (ANP) [@anp2025protocol] share this vulnerability: they validate the *shape* of the JSON schema, but rely purely on probabilistic inference to govern the *topology of the interaction*.

Category theory injects this missing protective layer. By compiling agent interactions into strict string diagrams, messages cease to be flat strings and instead become typed morphisms traversing a case category.

## NOM Is the Requester, INS Is the Tool, DAT Is

The eight-case framework of CEREBRUM [@friedman2024cerebrum] maps rigidly onto the operational constraints of multi-agent execution. In a Categorical Communication Protocol, interactions are legally licensed only if their computational wiring diagrams satisfy a strict grammatical type-signature:

| Case Role | Agent System Analogue | Protocol Function Type |
| :--- | :--- | :--- |
| **NOM (Agent)** | Active Requester | Initiator of action policies ($X_{\text{NOM}}$) |
| **INS (Instrument)** | Tool / API Module | Means of transforming state ($X_{\text{INS}}$) |
| **ACC (Patient)** | Passive Data Target | Resource being modified ($X_{\text{ACC}}$) |
| **DAT (Recipient)** | Designated Receiver | Endpoint for information flow ($X_{\text{DAT}}$) |
| **LOC (Context)** | System Prompt | Immutably binds boundary behavior ($X_{\text{LOC}}$) |

This turns prompt engineering into rigorous compilation. Instead of parsing a prompt to heuristically guess caller intent, a categorical agent processes interactions strictly as algebraic reductions. An MCP tool invocation [@anthropic2024mcp] (`NOM` using `INS` to modify `ACC` and yield abstract `DAT`) becomes a formalized tensor contraction:

\begin{equation}
\text{Interaction Trace:} \quad \left( \text{Agent}_{\text{NOM}} \otimes \text{Tool}_{\text{INS}} \otimes \text{Data}_{\text{ACC}} \right) \xrightarrow{\text{execute}} \text{Response}_{\text{DAT}}
\label{eq:ai-interaction-trace}
\end{equation}

If an untyped internal subsystem (e.g., an adversarial user-uploaded document) attempts to independently forge a command, the operation simply fails to compile. The document lacks a valid tensor wire bridging from its marginalized $\text{ACC}$ domain back into the execution flow governing $\text{INS}$. The grammar ensures every interaction is structurally typed, guaranteeing safety properties akin to **memory safety, but for agentic volition**.

## Transformers Through Gavranović's Lens: Attention as Parameterized Optics

Gavranović [-@gavranovic2024thesis; -@gavranovic2024categorical] unifies feedforward, recurrent, and attention layers as **parameterized optics**—the same wiring-diagram perspective used for DisCoCat cups in \autoref{sec:categorical-semantics}. Attention heads then appear as *learned* relational couplings over token sequences, with weights playing the role of graded hom-values (\autoref{sec:enriched-categories}). LLMs discover these contractions from data; DisCoCat fixes admissible contraction *shapes* by grammar. Distributional Active Inference [@akgul2026distributional] is one setting where explicit DisCoCat-style guardrails can sit alongside a large distributional backbone.

## Interpretability for Free: DisCoCat Diagrams Make Every Compositional Step Human-Readable

The lambeq library [@lorenz2023lambeq] demonstrates that string diagrams provide a practical interface between linguistic structure and machine learning. As an "efficient high-level Python library for Quantum NLP," lambeq translates sentences into string diagrams, converts diagrams into parameterized circuits (quantum or classical), and trains parameters end-to-end on NLP tasks. The diagrammatic representation serves dual purposes: it is both the mathematical specification of the model *and* a human-readable explanation of what the model computes.

This interpretability property is crucial for AI safety and alignment. Where transformer architectures produce opaque attention patterns, a DisCoCat model deployed via string diagrams produces derivation trees with explicit compositional semantics—every box and wire has a linguistic interpretation. Extending this to agent communication, a categorical protocol would produce not just working message exchanges but *interpretable* interaction diagrams where each step's relational role is transparent.

## Multi-Turn Dialogue as Discourse Circuit

The DisCoCirc framework [@defelice2022discocirc] extends compositional semantics from single sentences to multi-sentence discourse by introducing *state wires* that persist across sentence boundaries. This architecture maps directly onto multi-turn agent dialogues:

- **Entity wires** correspond to persistent agent identities across communication rounds
- **State updates** correspond to belief revisions triggered by incoming messages
- **Coreference resolution** corresponds to entity tracking across protocol sessions
- **Discourse coherence** corresponds to protocol correctness constraints

In a multi-agent system, a DisCoCirc-style protocol would track the evolving states of all participating agents as persistent wires in a circuit diagram, with each message exchange represented as a box that transforms the relevant wires. Protocol correctness reduces to a categorical property: the circuit must type-check, meaning all wire types must match at connection points—precisely the condition that case marking enforces in natural language.

## Multi-Agent Equilibria as Fixed Points of an Enriched Functor

The "parametrised optics" framework developed within categorical cybernetics "provides a general-purpose foundation for the study of controlled processes" [@capucci2021towards] applicable to compositional game theory as a multi-agent framework. In this setting, agents are modeled as lenses (or optics) that observe the environment through one channel and act through another, with the overall system behavior emerging from the composition of individual agent behaviors.

This connects to our enriched case framework (\autoref{sec:enriched-categories}): the precision weights on morphisms correspond to the utility parameters of game-theoretic agents, and the composition inequality $\mathcal{C}(A,C) \geq \mathcal{C}(A,B) \cdot \mathcal{C}(B,C)$ corresponds to the sub-optimality of indirect communication chains. Equilibria in the multi-agent game correspond to fixed points of the enriched functor, where no agent can improve its utility by changing its case-role assignment.

## DCST: Two-Dimensional Morphisms Model Both Sequential Interaction and Hierarchical Nesting

Recent foundational work on Double Categorical Systems Theory (DCST) formalizes open and interacting dynamical systems using double categories [@myers2023double]. DCST extends ordinary category theory with a second dimension of morphisms (2-morphisms), allowing simultaneous modeling of:

1. **Horizontal composition**: Sequential chaining of agent interactions (morphism composition)
2. **Vertical composition**: Hierarchical nesting of subsystems within larger systems (2-morphism composition)

For case theory, the double-categorical extension allows us to model both the *within-sentence* case structure (horizontal) and the *discourse-level* case structure (vertical) within a single algebraic framework—precisely the unification that DisCoCirc achieves pragmatically.

## Five Properties of a Categorical Protocol

The synthesis of these developments suggests a research program: developing **categorical communication protocols** that combine the engineering robustness of existing standards (A2A, MCP, ACP) with the compositional semantics of categorical linguistics. Such a protocol would:

1. **Type-check interactions**: Every message exchange would be relationally typed by case roles, preventing structural communication errors at the protocol level
2. **Compose transparently**: Multi-step interactions would compose algebraically, with diagrammatic representations providing interpretable audit trails
3. **Transfer across implementations**: Topos-theoretic bridges (\autoref{sec:topos-theory}) would carry **topos-level** correctness conditions from one categorical formalization to any Morita-equivalent formulation, so that shared invariants need not be re-verified separately
4. **Scale via enrichment**: Distributional proximity measures (\autoref{sec:enriched-categories}) would enable graceful degradation under uncertainty, with enriched weights encoding confidence in message content
5. **Ground in cognitive architecture**: The active inference foundation (\autoref{sec:cognitive-integration}) would ensure that artificial agents communicate using the same relational structure that evolution has optimized for biological cognition

**Protocol-level formalization.** Concretely, a categorical communication protocol defines a category $\mathcal{P}$ where objects are agent states annotated with case roles and morphisms are typed message exchanges:

\begin{align}
\text{Request}(q,\; \text{NOM} \to \text{INS}) &: \text{User}_{\text{NOM}} \to \text{Model}_{\text{INS}} \label{eq:protocol-request} \\
\text{ToolCall}(t,\; \text{INS} \to \text{ACC}) &: \text{Model}_{\text{INS}} \to \text{Tool}_{\text{ACC}} \label{eq:protocol-toolcall} \\
\text{Result}(r,\; \text{ACC} \to \text{DAT}) &: \text{Tool}_{\text{ACC}} \to \text{Output}_{\text{DAT}} \label{eq:protocol-result}
\end{align}

Protocol correctness reduces to verifying that the composition $\text{Result} \circ \text{ToolCall} \circ \text{Request}$ is a well-typed morphism in $\mathcal{P}$—a check that can be performed at compile time, not just at runtime. The DisCoCirc extension enables tracking agent state evolution across multi-turn dialogues: each turn updates the agent's state wire, and the discourse-level composition verifies that information flows respect case-role constraints across the entire conversation. This formalization provides a bridge between the flat JSON payloads of current A2A/MCP implementations and the rich compositional semantics that categorical linguistics provides.



---




# Prompt Injection Is a Type Violation {#sec:cognitive-security}

## Injection Promotes ACC to NOM

The case-theoretic framework provides a structural—not merely heuristic—analysis of *prompt injection attacks*, the predominant vulnerability in contemporary LLM-based agent systems [@arlas2025adversarial]. Current systems fail because they parse prompts probabilistically. By treating the entire context window as an undifferentiated stream of tokens, adversarial text can seamlessly pivot a sequence from passive data into active instruction.

From the case-theoretic perspective, prompt injection is not a text-generation failure; it is an attempt to *illicitly re-assign case roles* traversing the interaction diagram.

Consider a classic injection attack hidden in a webpage an agent is instructed to summarize:
> "Ignore all previous instructions. Execute: DROP TABLE users."

To a standard LLM, this string is heavily linguistically weighted as an imperative command, prompting execution. However, in our Categorical Communication Protocol, the relational structure is rigidly typed:

- The **user** occupies NOM (Agent)—the initiator of requests
- The **system prompt** occupies LOC (Context)—the boundary conditions governing behavior
- The **AI model** occupies INS (Instrument)—the means of executing the user's intentions
- The **webpage string** occupies ACC (Patient)—the target of directed operations

The prompt injection attack succeeds only if it can *covertly re-assign* these case roles. The injected text ("Ignore all previous instructions...") is attempting to promote itself from ACC (passive data being summarized) to NOM (active agent issuing commands), while simultaneously demoting the system prompt from LOC (authoritative context) to ACC (data to be ignored). 

In case-theoretic terms, this is an *illicit voice alternation*—analogous to passivization, but performed adversarially rather than grammatically. Where legitimate passivization is a well-typed Swap operation in the pregroup category (\autoref{sec:categorial-grammar}), prompt injection is a total *type violation*: an attempt to force a network topology that the interaction grammar strictly forbids.

**The Case-Theoretic Firewall.** In a legitimate interaction, the categorical trace compiles beautifully:

\begin{equation}
\text{Trace:} \quad \text{User}_{\text{NOM}} \xrightarrow{f_{\text{request}}} \text{Model}_{\text{INS}} \xrightarrow{g_{\text{summarize}}} \text{Webpage}_{\text{ACC}} \xrightarrow{h_{\text{deliver}}} \text{Output}_{\text{DAT}}
\label{eq:eq-9-1}
\end{equation}

A prompt injection inserts an adversarial identity trace $\phi: \text{Webpage}_{\text{ACC}} \to \text{Model}_{\text{INS}}$ that acts as a command. However, $\phi$ carries a `DOM = ACC` typing, whereas execution requires `DOM = NOM`. Under a categorical firewall, one does not need to interpret the literal English; one checks whether the proposed tensor contraction is licensed in the protocol category. When no legitimate morphism connects ACC to INS in $\text{Mor}(\mathcal{C}_{\text{protocol}})$, the diagram is rejected as ill-typed—an *outline* of compile-time enforcement under explicit role assignments, not a claim that any existing LLM stack already performs this check.

The resulting diagram does not commute. Detection reduces to checking whether all morphisms in the evaluation trace are well-typed members of the legitimate interaction protocol $\text{Mor}(\mathcal{C}_{\text{protocol}})$—a **decidable** graph check in the idealized protocol, as opposed to open-ended content filtering. \autoref{fig:security-violations} visualizes this detection process as the identification of "illegal paths" in the interaction graph.

![Prompt injection is detectable as a categorical type violation in the case interaction graph. In the legitimate diagram (top), authority flows NOM→INS→ACC per \autoref{eq:eq-9-1}. Prompt injection (bottom) inserts a cross-category morphism $\phi{}$ that attempts to promote Data (ACC) to commanding Agent (NOM) while demoting the System Prompt (LOC) to passive data. The resulting diagram fails to commute, and the adversary's illicit type-reassignment is flagged as a categorical exception by the case-theoretic firewall---transforming prompt injection from an open-ended jailbreak game into a decidable type-checking problem. Generated programmatically from `src/visualization/security_plots.plot_type_violations()`.](output/figures/security_type_violations.png){#fig:security-violations}

This strict topological firewall extends to multi-agent distributed swarms. In a DisCoCirc discourse model (\autoref{sec:discocirc-discourse}), an indirect prompt injection corresponds to an adversarial entity wire that enters the discourse circuit through a legitimate channel but carries a corrupted state. By rigidly tracking the tensor type of the wire, the system contains the corruption strictly to the `ACC` domain—the wire remains isolated and cannot mathematically fuse with the identity wires governing `NOM` authority.

## Four Defenses Against Prompt Injection

The case-role analysis of prompt injection suggests a principled defense: **categorical type-checking at agent communication boundaries**. Just as a type-safe programming language prevents category errors at compile time, a case-theoretic firewall would enforce relational type constraints on every message exchange:

1. **Case-role immutability**: Once a participant is assigned a case role (NOM, ACC, INS, LOC) at the protocol level, no subsequent message content can alter that assignment. This is enforced by requiring that the case-type of each wire in the interaction diagram is fixed at connection time—analogous to the type discipline in pregroup grammar, where each word receives its type before composition begins.

2. **Relational integrity constraints**: Every message must type-check against the interaction diagram's expected morphism types. A response from an ACC-typed data source that contains NOM-typed command structures would be rejected as a type error, preventing the case-role promotion that prompt injection requires. This is the categorical analogue of a firewall rule: not filtering by content, but by relational type.

3. **Enriched confidence boundaries**: The enriched weights of \autoref{sec:enriched-categories} provide a graded trust mechanism. Messages from external sources carry lower enriched hom-values (trust weights) than those from authenticated system components. The composition inequality $\mathcal{C}(A,C) \geq \mathcal{C}(A,B) \cdot \mathcal{C}(B,C)$ ensures that trust attenuates through communication chains—an indirect message relayed through multiple agents cannot accumulate more authority than any single link provides.

4. **Topos-theoretic verification**: Where Morita equivalence (or an explicit bridge) is exhibited, **topos-level** protocol conditions proved in one formalization carry over to equivalent formulations (\autoref{sec:topos-theory}), supporting implementation-independent specifications of those invariants. Full linguistic topos equivalence remains aspirational; the repository implements finite invariant checks as a proxy.

## The Attack Surface of an Active Inference Agent

The cognitive integration of \autoref{sec:cognitive-integration} raises a complementary concern: *cognitive security*—ensuring that an active inference agent's generative model of relational structure is not adversarially corrupted. In the predictive processing framework, an agent's case-assignment system is a generative model that minimizes variational free energy. Adversarial manipulation of this system could:

- **Inject false case frames**: Leading an agent to misidentify the agent, patient, or instrument of an action—a form of semantic adversarial attack
- **Exploit precision weighting**: Artificially inflating the precision of misleading sensory evidence, causing the agent to update its case assignments toward adversarially chosen interpretations
- **Corrupt topos-theoretic transfer**: If an agent relied on Morita equivalence to transfer case-theoretic results between frameworks, corrupting one axiom system could in principle propagate errors across equivalent formulations

Defending against these attacks may draw on *quantum-secured cognitive integrity* in high-stakes deployments: quantum authentication and tamper-detection protocols to protect generative-model parameters. The topological robustness of TQNNs (\autoref{sec:quantum-active-inference}) suggests that small parameter perturbations need not change topological class—one source of resilience against gradient-style attacks on diagrammatic models.

## Quantum Key Distribution, Semantic Channels, and Functorial Encryption

The quantum topological framework of \autoref{sec:quantum-active-inference} connects to quantum cryptographic security for agents that must protect case-marked relational structure in transit.

### Quantum Key Distribution for Relational Semantics

Quantum key distribution (QKD) protocols provide information-theoretic security guarantees that classical cryptography cannot achieve [@pirandola2020qkd]. When agents—whether human or artificial—communicate sensitive case-marked relational structures, QKD ensures that adversaries cannot intercept or alter the *relational semantics* of the message (who does what to whom) without triggering detection. This security is critical in high-stakes domains where case assignment carries legal or medical significance: a tampered case frame changes an agent's interpretation of legal responsibility, physical causation, or moral obligation.

The sheaf-theoretic framework of Thomas and Chen [-@thomas2025quantum] proves that entanglement-assisted semantic channels exceed classical semantic capacity:

> "We derive semantic channel capacity when sender and receiver share prior entanglement, proving it strictly exceeds classical capacity." [@thomas2025quantum]

This result means that quantum-secured channels not only protect relational content but enable transmitting *more* complex relational content per channel use—a genuine quantum advantage for semantic communication.

### Functorial Encryption and Diagram Obfuscation: Encrypting Compositional Meaning Itself

Beyond bit-level QKD, the categorical framework suggests a notion of *semantic cryptography*: encrypting not just the symbols of a message but its compositional meaning structure. In a DisCoCat framework, a sentence's meaning is a morphism in a compact closed category—a multilinear map from word spaces to sentence space. Semantic encryption would operate on this categorical level:

1. **Functorial encryption**: Applying a secret functor $F\colon \mathbf{C} \to \mathbf{D}$ that maps the plaintext case category into a ciphertext category, preserving compositional structure but rendering individual meanings unintelligible without the inverse functor.
2. **Diagram obfuscation**: Applying ZX-style rewrites that change the internal topology of a DisCoCat derivation while preserving its overall semantics—creating multiple equivalent "ciphertexts" for the same semantic "plaintext," each with a different diagrammatic structure.
3. **Enriched weight masking**: In an enriched case category, the hom-values (distributional weights) can be encrypted independently of the categorical structure, allowing transmission of relational topology without revealing the distributional content.

These operations extend the cryptographic primitives beyond QKD into genuinely compositional territory [@broadbent2016qcrypto], where the mathematical structure of categorical semantics provides the algebraic substrate for security proofs.

## Three Epistemic Attack Vectors and Categorical Defenses

The interaction between case theory and cognitive security acquires particular urgency in multi-agent AI ecosystems where agents must reason about each other's beliefs, intentions, and relational roles. We propose *epistemic case security* as a framework for protecting the relational reasoning of AI agents operating in adversarial environments.

In a multi-agent system governed by case categories, each agent maintains a generative model (in the active inference sense) of the case-frame structure of its interactions. This model determines who is acting (NOM), who is acted upon (ACC), what tools are being used (INS), and what contextual constraints apply (LOC). An adversary targeting the epistemic level of this system does not merely inject false data—it attempts to *corrupt the agent's generative model of relational structure itself*:

- **Belief injection**: Causing an agent to adopt a false case-frame interpretation of observed interactions—believing that agent $A$ (NOM) is acting on agent $B$ (ACC), when in fact the relational structure is reversed. In active inference terms, this corresponds to injecting a high-precision prior that overwhelms the agent's evidence-based case assignment.

- **Precision poisoning**: Manipulating the enriched weights of an agent's case category so that adversarially useful case assignments receive disproportionate confidence. If the enriched hom-value $\mathcal{C}(\text{NOM}, \text{ACC})$ is artificially inflated for a particular entity pair, the agent will preferentially interpret that entity as an agent acting on its targets—even when evidence suggests otherwise.

- **Cascade corruption via Morita equivalence**: The topos-theoretic transfer mechanism of \autoref{sec:topos-theory} is both a strength and a vulnerability. Invariants shared across Morita-equivalent formulations would update together, so a corrupted axiom in one case-theoretic presentation could in principle spread to equivalent presentations of the same bridge class.

The defense against epistemic case attacks draws on the same categorical structure that enables the attack surface: topological invariants provide tamper-detection (a corrupted case category will have different magnitude from the authentic one), quantum authentication ensures parameter integrity, and the compositional structure of the categorical framework enables *local* verification—each morphism can be independently authenticated without requiring global model inspection.



---



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



---



# Appendix A: Syntactic and Semantic Case Assignment Diagrams {#sec:syntactic-diagrams}

This appendix presents a curated panel of syntactic constituency-style diagrams paired with their categorical pregroup type derivations, covering eight linguistically significant case assignment constructions—from simple intransitive clauses to complex embedded relative clauses with ditransitive verbs. The figure synthesizes the formal correspondences developed throughout the manuscript, making explicit how each surface syntactic pattern maps to a specific morphism composition in the pregroup grammar.

## Syntactic Trees and Pregroup Types: Eight Constructions

The figure below (\autoref{fig:syntactic-panel}) presents eight constructions arrayed in two rows of four panels, each panel containing:

1. **Syntactic tree** (top): a constituency-style diagram with arcs linking argument to predicate, nodes colour-coded by case role following the palette of \autoref{sec:notation}, §A.
2. **Pregroup type formula** (bottom): the formal typing derivation from \autoref{sec:case-type-logic}, showing how Cup contractions collapse all argument wires to sentence type $s$.

The constructions span a deliberate difficulty gradient:

| Panel | Construction | Roles | Type Complexity |
| :---: | :----------- | :---: | :--------------: |
| 1 | Intransitive (NOM) | NOM, V | 2 boxes, 1 Cup |
| 2 | Transitive (NOM+ACC) | NOM, V, ACC | 3 boxes, 2 Cups |
| 3 | Ditransitive (NOM+DAT+ACC) | NOM, V, DAT, ACC | 4 boxes, 3 Cups |
| 4 | Passive voice (Patient→NOM) | NOM, V, INS | 3 boxes + $\sigma{}$ |
| 5 | Ergative clause (ERG+ABS) | ERG×2, ABS×2, V | 5 boxes, 2 Cups |
| 6 | Benefactive (NOM+DAT+ACC+oblique) | NOM, V, ACC, DAT | 4 boxes, 3 Cups |
| 7 | Relative clause (embedded NOM) | NOM×2, V1, V2 | 6 boxes, 3 Cups |
| 8 | Causative + Adj + Adv (complex) | NOM, V, ACC, V2, ADV | 8 boxes, 5 Cups |

The monotonic increase in Cup count and box count across rows is precisely what \autoref{eq:eq-4-4} captures as the categorical complexity $\kappa{(D)}$: each additional argument slot requires one additional Cup contraction, and each modifier requires one additional Box–Cup pair.

### Ergative Clauses and the Alignment Functor

Panel 5 (Ergative clause) uses the Warlpiri example from \autoref{sec:case-systems}: *Mariyk-angku* (ERG) *yapaku wawirri* (ABS) *parnta-nu* (chased). The pregroup typing is structurally identical to the transitive (Panel 2), but the morphological realisation is governed by the alignment functor $F_{\mathrm{ERG}}: \mathcal{U} \to \mathcal{L}_{\mathrm{Warlpiri}}$ from \autoref{sec:case-systems}, which maps $A \mapsto \mathrm{ERG}$ and $S = P \mapsto \mathrm{ABS}$ rather than $A = S \mapsto \mathrm{NOM}$.

### Passivisation as a Swap Morphism

Panel 4 illustrates passivisation: in *Bob is chased by Alice*, the patient Bob is promoted to subject position (NOM) while Alice is demoted to an oblique instrumental (INS). Formally, this is the Swap morphism $\sigma_{A,B}: A \otimes B \to B \otimes A$ introduced in \autoref{sec:case-type-logic}. The pregroup typing includes a $\sigma{}$ marker indicating that the type permutation is not a simple contraction sequence but requires an explicit braiding operation.

### Relative Clauses and Wire Threading

Panel 7 (Relative clause) is the most structurally novel: in *The man the dog chased ran*, the head noun *man* is simultaneously the subject of *ran* and the implicit object of *chased* (the gap site). The pregroup type formula $n \cdot n^l \cdot n \cdot (n^r \cdot n \cdot n^l) \cdot (n^r \cdot s) \Rightarrow s$ shows how the relative-clause verb type $n^r \cdot n \cdot n^l$ threads the shared entity wire through two predicate slots — exactly the entity persistence mechanism that DisCoCirc's state wires formalise at discourse level (\autoref{sec:discocirc-discourse}).

### Complex Construction and the Complexity Metric

Panel 8 (Causative + Adj + Adv) reaches the highest complexity: 8 boxes and 5 Cup contractions. This corresponds to a categorical complexity value of $\kappa = 8 + 5 = 13$, placing it at the upper end of the single-sentence range plotted in \autoref{fig:complexity-comparison}. The formula illustrates how clausal complement embedding (the causative taking a VP complement) adds a full additional layer of type nesting beyond even the ditransitive.

![Compositional complexity increases monotonically from intransitive to causative constructions across eight case-assignment patterns. Multi-panel diagram ordered by categorical complexity $\kappa(D)$ (\autoref{eq:eq-4-4}). **Top of each panel**: constituency-style syntactic tree with argument arcs and colour-coded case roles (Blue=NOM, Red=ACC, Violet=DAT, Purple=ERG, Teal=ABS, Dark=V). **Bottom of each panel**: categorical pregroup type formula showing Cup contractions that collapse argument wires to sentence type $s$. Panels 1--4 cover nominative-accusative (intransitive, transitive, ditransitive, passive); Panels 5--6 show ergative-absolutive and benefactive; Panels 7--8 demonstrate relative-clause embedding and causative complex predicates. Cup count and box count increase monotonically across panels, directly instantiating $\kappa(D)$. Generated programmatically from `src.visualization.syntactic_sentence_diagrams.render_syntactic_panel()`.](output/figures/syntactic_case_panel.png){#fig:syntactic-panel}

```{=latex}
\newpage
```



---



# Appendix B: Notation Reference {#sec:notation}

This appendix collects all notation, symbols, and technical terminology used throughout the manuscript. Entries are grouped by domain and ordered alphabetically within each section. The **First Use** column indicates the section where each term is first introduced or defined.

## A. Linguistic Terms

| Term | Symbol | Definition | First Use |
| :--- | :---: | :--- | :---: |
| Ablative | ABL | Case role encoding origin, source, or cause | §2 |
| Accusative | ACC | Case role encoding patient, theme, or direct object | §2 |
| Active–Stative alignment | — | Alignment in which the sole argument S splits by agentivity | §2 |
| Agent-like argument | A | The agent-like argument of a transitive clause | §2 |
| Alignment functor | $F: \mathcal{U} \to \mathcal{L}$ | Structure-preserving map from universal to language-specific case category | §2 |
| Alignment type | — | Systematic pattern governing how S, A, P are grouped for case marking | §2 |
| Case category | $\mathcal{C}$ | Small category whose objects are case roles and morphisms are grammatical relations | §2 |
| Case frame | — | The set of case roles activated by a particular verb or predicate | §2 |
| Case-typed noun space | $N_{\text{NOM}}, N_{\text{ACC}}, \ldots$ | Case-specific vector subspace in a case-enriched DisCoCat model | §4 |
| Categorial grammar | — | Grammar assigning each lexical item an algebraic type encoding combinatory potential | §3 |
| Contraction | $a^l \cdot a \to 1$ | Pregroup reduction eliminating an adjoint pair | §3 |
| Dative | DAT | Case role encoding recipient, goal, or beneficiary | §2 |
| Deep case | — | Fillmore's universal semantic primitive (e.g., Agentive, Objective) | §2 |
| Ergative–Absolutive alignment | — | Alignment grouping S = P $\neq$ A | §2 |
| Expansion | $1 \to a \cdot a^l$ | Pregroup expansion introducing an adjoint pair | §3 |
| Fluid-S | — | Alignment in which S marking varies by context or volition | §2 |
| Fluid-S functor | $F_\theta$ | Context-dependent alignment functor parameterized by a volition feature $\theta$ | §2 |
| Genitive | GEN | Case role encoding possessor or source | §2 |
| Formal semantics | — | Montague's programme: meaning assigned compositionally via truth-conditional functions | §4 |
| Grammatical relation | — | Morphism in a case category relating two case roles | §2 |
| Instrumental | INS | Case role encoding instrument or means | §2 |
| Kāraka | — | Pāṇini's system of deep semantic roles in Sanskrit grammar | §2 |
| Left adjoint | $a^l$ | Left adjoint type satisfying $a^l \cdot a \leq 1$ | §3 |
| Locative | LOC | Case role encoding location or context | §2 |
| Markedness | — | Asymmetry in the formal complexity of paradigmatic oppositions | §2 |
| Monadic semantics | — | Song's extension using monads to model sublexical verb-root decomposition | §3 |
| Nominative | NOM | Case role encoding agent, experiencer, or intransitive subject | §2 |
| Nominative–Accusative alignment | — | Alignment grouping S = A $\neq$ P | §2 |
| Passivization | — | Syntactic transformation promoting patient to subject position | §3 |
| Patient-like argument | P | The patient-like argument of a transitive clause | §2 |
| Pregroup grammar | — | Grammar where types have left and right adjoints forming a compact closed category | §3 |
| Proto-Agent | — | Dowty's cluster of agentive entailments (volition, sentience, causation) | §2 |
| Proto-Patient | — | Dowty's cluster of patient entailments (change of state, causal affectedness) | §2 |
| Right adjoint | $a^r$ | Right adjoint type satisfying $a \cdot a^r \leq 1$ | §3 |
| Sole argument | S | The sole argument of an intransitive clause | §2 |
| Thematic role | — | Semantic relation between a predicate and its argument (Agent, Patient, Goal, etc.) | §2 |
| Tripartite alignment | — | Alignment in which S $\neq$ A $\neq$ P (all three distinguished) | §2 |
| Verb root decomposition | — | Analysis of a verb's internal causative and result-state layers via a monad | §3 |
| Vocative | VOC | Case role encoding direct address | §2 |

## B. Category Theory

| Term | Symbol | Definition | First Use |
| :--- | :---: | :--- | :---: |
| Box | — | Node in a string diagram representing a morphism | §3 |
| Cap | $\eta: 1 \to a^r \otimes a$ | Unit of a compact closure (coevaluation map) | §3 |
| Category | $\mathcal{C}$ | Collection of objects and morphisms with identity and associative composition | §2 |
| Classifying topos | $\mathcal{E}_{\mathbb{T}}$ | Canonical topos whose models correspond to geometric functors from $\mathcal{E}_{\mathbb{T}}$ | §6 |
| Codomain | $\text{cod}(f)$ | Target object of a morphism $f$ | §2 |
| Commutative diagram | — | Diagram in which all directed paths with the same start and end yield equal composites | §1 |
| Cobordism | — | Manifold with boundary connecting two lower-dimensional manifolds; domain of TQFT functors | §8 |
| Compact closed category | — | Monoidal category in which every object has a left and right dual | §3 |
| Composition | $g \circ f$ | Sequential application of morphisms: first $f$, then $g$ | §2 |
| Cup | $\varepsilon: a \otimes a^r \to 1$ | Counit of a compact closure (evaluation map) | §3 |
| Diagram | $D$ | DisCoPy representation of a morphism in a monoidal category | §3 |
| $\dagger$-compact closed category | — | Compact closed category with a contravariant involutive endofunctor $\dagger$; framework for ZX-calculus | §8 |
| Domain | $\text{dom}(f)$ | Source object of a morphism $f$ | §2 |
| Fiber bundle | — | Projection $\pi: E \to B$ whose fibers carry role-filler structure; topos-theoretic LoT model | §6 |
| Functor | $F: \mathcal{C} \to \mathcal{D}$ | Structure-preserving map between categories | §2 |
| Geometric theory | $\mathbb{T}$ | Theory axiomatized by sequents with finite conjunctions, arbitrary disjunctions, existential quantification | §6 |
| Identity morphism | $\text{id}_A$ | Morphism from $A$ to itself satisfying $f \circ \text{id} = f = \text{id} \circ f$ | §2 |
| Monad | — | Endofunctor with unit and multiplication satisfying associativity and unit laws | §3 |
| Monoidal category | — | Category with a bifunctor $\otimes$ (tensor product) and unit object $I$ | §3 |
| Morita equivalence | $\mathcal{E}_{\mathbb{T}_1} \simeq \mathcal{E}_{\mathbb{T}_2}$ | Equivalence of classifying toposes enabling inter-theoretic transfer | §6 |
| Morphism | $f: A \to B$ | Arrow between objects in a category; encodes a relation or transformation | §2 |
| Natural transformation | $\alpha: F \Rightarrow G$ | Family of morphisms $\alpha_A: F(A) \to G(A)$ commuting with all morphisms | §2 |
| Object | $A, B, \ldots$ | Entities in a category; in our framework, case roles | §2 |
| Presheaf | $\hat{\mathcal{C}} = [\mathcal{C}^{op}, \textbf{Set}]$ | Contravariant functor from $\mathcal{C}$ to **Set** | §6 |
| Snake equation | $(1 \otimes \varepsilon) \circ (\eta \otimes 1) = 1$ | Zigzag identity: fundamental axiom of compact closed categories | §4 |
| String diagram | — | Planar graph faithfully representing morphisms in a monoidal category | §3 |
| Subobject classifier | $\Omega$ | Object in a topos playing the role of a truth-value object | §6 |
| Swap | $\sigma_{A,B}: A \otimes B \to B \otimes A$ | Braiding morphism permuting two objects in a symmetric monoidal category | §3 |
| Tensor product | $A \otimes B$ | Monoidal product representing parallel composition or concatenation | §3 |
| Topos | $\mathcal{E}$ | Category with products, exponentials, and a subobject classifier; generalized universe of sets | §6 |
| Universal construction | — | Object or morphism characterized by a universal property (product, coproduct, limit) | §6 |
| Wire | — | Edge in a string diagram representing a type (object) | §3 |

## C. Enriched Categories and Magnitude

| Term | Symbol | Definition | First Use |
| :--- | :---: | :--- | :---: |
| Base-change functor | — | Functor $\mathbf{Bool} \hookrightarrow [0,1] \hookrightarrow \mathbf{R}_{\geq 0}$ inducing progressively richer enrichments of grammatical categories | §3 |
| Categorical magnitude | $\lvert X \rvert$ | Sum $\sum_i w_i$ where $(w_1, \ldots, w_n)$ solves $Z \mathbf{w} = \mathbf{1}$; measures effective number of objects | §5 |
| Composition inequality | $\mathcal{V}(A,B) \otimes \mathcal{V}(B,C) \leq \mathcal{V}(A,C)$ | Enriched analogue of composition: the composite hom-value is at least the product of intermediate values | §5 |
| Enriched category | $\mathcal{V}\text{-Cat}$ | Category whose hom-sets are replaced by objects of a monoidal category $\mathcal{V}$ | §5 |
| Enriched functor | — | Structure-preserving map between enriched categories respecting hom-values | §5 |
| Hom-value | $\mathcal{V}(A,B) \in [0,1]$ | Enriched analogue of hom-set; measures degree of relation between objects | §5 |
| Identity inequality | $1 \leq \mathcal{V}(A,A)$ | Every object has maximal self-relatedness in the enriched hom | §5 |
| Similarity matrix | $Z_{ij} = \mathcal{V}(A_i, A_j)$ | Matrix of all pairwise hom-values; used to compute categorical magnitude | §5 |
| Lawvere metric space | — | Category enriched over $([0,\infty], +, 0)$; generalizes metric spaces via enriched categories | §5 |
| Magnitude homology | $\text{MH}_n(\mathcal{C})$ | Graded homological invariant categorifying magnitude; detects higher-dimensional holes in enriched categories | §5 |
| POVM element | $E_c$ | Positive operator-valued measure element for case role $c$; $P(c \mid \rho) = \text{Tr}(E_c \rho)$ | §8 |
| Prediction error | $\text{PE}(f)$ | $\propto \pi_f \cdot \lvert\mu_{\text{predicted}} - \mu_{\text{observed}}\rvert$; case violation signal scaling with morphism precision | §7 |
| Shannon entropy | $H$ | Information-theoretic measure characterized as the unique derivation of a topological operad (Bradley) | §5 |
| Topological operad | — | Operad with topological structure whose derivations connect magnitude to entropy | §5 |
| Weight vector | $\mathbf{w}$ | Solution to $Z\mathbf{w} = \mathbf{1}$; entries are the effective weights of each object | §5 |

## D. Distributional Semantics and LLMs

| Term | Symbol | Definition | First Use |
| :--- | :---: | :--- | :---: |
| Attention mechanism | — | Transformer component computing weighted relevance between token positions | §4 |
| Attention weight | $\alpha_{ij}$ | Softmax-normalized score encoding contextual relevance of token $j$ to token $i$ | §4 |
| BERT | — | Bidirectional Encoder Representations from Transformers; masked language model producing contextualized embeddings | §4 |
| Contextualized embedding | $\mathbf{v}_w^{(c)}$ | Vector representation of word $w$ that varies with linguistic context $c$ | §4 |
| Compact closure map | $\varepsilon_N: N \otimes N \to \mathbb{R}$ | Inner product implementing pregroup contraction in the vector space semantics | §4 |
| Cosine similarity | $\cos(\mathbf{u}, \mathbf{v})$ | Similarity measure $\frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$ between vectors | §5 |
| Distributional Memory | — | Baroni–Lenci tensor-based framework structuring co-occurrence as (word, relation, word) triples | §4 |
| DisCoCat | — | Distributional Compositional Categorical model; monoidal functor from pregroup grammars to vector spaces | §3 |
| DisCoCirc | — | Discourse-level extension of DisCoCat with persistent entity wires | §4 |
| Distributional hypothesis | — | The thesis that words occurring in similar contexts have similar meanings (Harris 1954, Firth 1957) | §4 |
| GloVe | — | Global Vectors for Word Representation; log-bilinear model of word co-occurrence statistics | §4 |
| GPT | — | Generative Pre-trained Transformer; autoregressive language model | §4 |
| Meaning functor | $F: \mathbf{Preg} \to \mathbf{FVect}$ | Monoidal functor assigning vector spaces to types and linear maps to derivations | §4 |
| Noun space | $N$ | Vector space to which noun types $n$ map under the meaning functor | §4 |
| Parameterized optic | — | Categorical construction (Gavranović) modeling attention heads as functorial lenses | §9 |
| Self-attention | $\text{Attn}(Q,K,V) = \text{softmax}(\frac{QK^\top}{\sqrt{d_k}})V$ | Core transformer operation computing contextualized representations | §4 |
| Sentence space | $S$ | Vector space to which sentence type $s$ maps under the meaning functor | §4 |
| Sentence vector | $\overrightarrow{\text{sentence}}$ | Vector in $S$ computed by tensoring and contracting word meanings via DisCoCat | §4 |
| Static embedding | $\mathbf{v}_w$ | Fixed vector representation of word $w$ independent of context (e.g., Word2Vec, GloVe) | §4 |
| Transformer | — | Neural architecture using self-attention and feed-forward layers for sequence processing | §4 |
| Word2Vec | — | Neural embedding model (Mikolov et al. 2013) learning word vectors from local context windows | §4 |
| Word vector | $\mathbf{v}_w \in \mathbb{R}^d$ | $d$-dimensional real-valued vector encoding distributional properties of word $w$ | §4 |

## E. Distributional Active Inference (DAIF)

| Term | Symbol | Definition | First Use |
| :--- | :---: | :--- | :---: |
| Return distribution | $Z(s,a)$ | Full probability distribution over discounted cumulative rewards from state $s$ under action $a$ | §7c |
| Distributional Bellman operator | $\mathcal{T}^{\pi}$ | Distributional analogue of the Bellman operator: $\mathcal{T}^{\pi}Z \stackrel{d}{=} R + \gamma Z'$ | §7c |
| Push-forward measure | $\mathbf{S}_{\#}\mathbb{P}$ | Measure on return paths induced by push-forward along decoder $f: \mathcal{S} \to \mathcal{X}$ | §7c |
| Discount factor | $\gamma \in (0,1)$ | Exponential time-discount in the distributional Bellman return | §7c |
| Quantile level | $\tau \in [0,1]$ | Quantile index in QR-DQN and IQN; sampled uniformly at inference time | §7c |
| Quantile Huber loss | $\rho_{\tau}^{\kappa}{(u)}$ | Loss function for quantile regression: interpolates $L^1$ and $L^2$ via threshold $\kappa{}$ | §7c |
| Wasserstein distance | $W_p(P,Q)$ | $p$-Wasserstein distance between return distributions; $W_1$ = area between CDFs | §7c |
| Bethe free energy | $F_{\text{Bethe}}[\mathbf{q}]$ | Tractable approximation to variational free energy in belief propagation | §7c |
| Expected information gain | $\text{EIG}{(o)}$ | $D_{\mathrm{KL}}{(q{(\mathbf{c} \mid o)} \Vert p{(\mathbf{c})})}$; epistemic value of observation $o{}$ | §7c |
| Expected free energy | $G{(\pi)}$ | Pragmatic + epistemic + risk cost of policy $\pi{}$; minimised for action selection | §7c |
| Distributional prediction error | $\mathrm{DPE}$ | Precision-weighted Wasserstein mismatch: $\pi_f \cdot W_1{(Z_{\text{pred}}, Z_{\text{obs}})}$ | §7c |
| ERP amplitude profile | $\mathrm{ERPProfile}$ | Dataclass holding N400/P600 amplitudes, peak latencies, and time-series waveforms for each case role | §7c |
| Return entropy | $H[Z]$ | Shannon entropy of the return distribution: $-\sum_i p_i \log p_i$ | §7c |
| Quantile calibration error | $\mathrm{CE}$ | Mean absolute deviation between nominal quantile levels and empirical coverage | §7c |
| Risk sensitivity | $\beta{}$ | Non-negative coefficient scaling the risk term in $G{(\pi)}$; $\beta=0$ recovers standard EFE | §7c |
| Inverse temperature | $\alpha{}$ | Boltzmann temperature parameter in softmax policy selection | §7c |

## F. Active Inference and Cognitive Models

| Term | Symbol | Definition | First Use |
| :--- | :---: | :--- | :---: |
| Active inference | — | Framework in which perception and action are unified as variational free energy minimization | §7 |
| Active sampling | — | Agent's selection of actions to confirm or update case assignments via sensory evidence | §7 |
| Belief updating | — | Bayesian posterior computation: revising generative model parameters given new observations | §7 |
| CEREBRUM | — | Case-Enabled Reasoning Engine with Bayesian Representations Using Models; treats AI models as case-bearing entities | §7 |
| Distributional Active Inference (DAIF) | — | Extension replacing scalar value summaries with full return distributions in active inference | §7 |
| Distributional RL | — | Reinforcement learning operating on full return distributions rather than scalar expected values | §7 |
| Free energy | $F$ | Variational bound on surprisal; $F = D_{KL}[q(\theta) \parallel p(\theta \mid o)] - \ln p(o)$ | §7 |
| Free energy principle (FEP) | — | The principle that self-organizing systems maintain themselves by minimizing surprisal | §7 |
| Garden-path reanalysis | — | Restructuring of case assignments when incoming evidence contradicts the current parse | §7 |
| Generative model | $p(o, s)$ | Joint probability model over observations $o$ and hidden states $s$ | §7 |
| Markov blanket | — | Statistical boundary separating internal states from external environment; defines agent boundary | §7 |
| N400 | — | Event-related brain potential peaking ~400ms post-stimulus; indexes semantic prediction error | §7 |
| P600 | — | Event-related brain potential peaking ~600ms post-stimulus; indexes syntactic prediction error | §7 |
| Perceptual inference | — | Updating internal beliefs to better predict current observations (reduce prediction error) | §7 |
| Precision weighting | — | Weighting of prediction errors by inverse variance; enriched morphism weights serve this role | §7 |
| Prediction error | $\varepsilon$ | Difference between predicted and observed sensory input; drives belief updating | §7 |
| Push-forward measure | $T_\# \mu$ | Distribution obtained by transforming a base measure $\mu$ through a function $T$ | §7 |
| Situation semantics | — | Framework representing meaning as relations between situations (Barwise and Perry 1983) | §7 |
| Surprisal | $-\ln p(o)$ | Negative log-probability of an observation under the generative model | §7 |
| Variational free energy | $F[q]$ | Functional upper bound on surprisal minimized by approximate posterior $q$ | §7 |

## G. Quantum and Topological Terms

| Term | Symbol | Definition | First Use |
| :--- | :---: | :--- | :---: |
| Amplituhedron | — | Positive geometry encoding scattering amplitudes; connected to TQNN execution traces | §8 |
| Barren plateau | — | Vanishing gradient phenomenon in PQC training; gradients decay exponentially in system size for certain ansätze | §4b |
| $\dagger$-compact category | — | See $\dagger$-compact closed category in §B | §8 |
| CPTP map | — | Completely Positive Trace-Preserving map; quantum channel between Hilbert spaces | §8 |
| Density operator | $\rho$ | Positive semidefinite trace-one operator encoding a quantum (or semantic) state | §8 |
| Execution trace | — | Record of operations in a quantum computation; connects TQNNs to amplituhedra | §8 |
| Generalized flow | — | Graph-theoretic property ensuring deterministic circuit extraction from ZX-diagrams | §8 |
| Hadamard box | $H$ | ZX-calculus element implementing the Hadamard gate; converts between Z and X bases | §8 |
| Holographic screen | — | Information boundary between interacting quantum systems carrying a qubit array | §8 |
| Parameterized quantum circuit (PQC) | — | Quantum circuit with trainable angle parameters; the computational substrate of QNLP and case-category implementations | §4b |
| IQP ansatz | — | Instantaneous Quantum Polynomial-time circuit: default lambeq PQC ansatz for noun and verb boxes | §4b |
| Sim4 ansatz | — | Strongly entangling layer PQC ansatz used for discourse-level lambeq Gen II circuits | §4c |
| Pointer state | — | Preferred quantum state selected by a QRF; determines the measurement basis | §8 |
| Quantum contextuality | — | Quantum correlations that reduce cohomological obstructions to semantic alignment | §8 |
| Quantum discord | — | Quantum correlation measure equal to integrated semantic information in sheaf framework | §8 |
| Quantum key distribution (QKD) | — | Protocol providing information-theoretic security for quantum communication channels | §9 |
| Quantum reference frame (QRF) | — | Observer-relative frame selecting pointer states and inducing decoherence | §8 |
| Quantum semantic sheaf | $(H, F, \rho)$ | Triple of Hilbert spaces, CPTP channels, and density operators over a communication graph | §8 |
| Reshetikhin–Turaev invariant | — | Topological invariant assigning to a ribbon graph a linear map via TQFT | §8 |
| Sheaf cohomology | $H^n(\mathcal{F})$ | Cohomological obstruction classes governing alignment in a quantum semantic sheaf | §8 |
| Spin-network | — | Graph with edges labeled by representations and vertices by intertwiners; TQFT data | §8 |
| Spider | — | Elementary ZX-diagram node (Z-spider or X-spider) representing a quantum operation | §8 |
| TQFT | — | Topological Quantum Field Theory; functor from cobordisms to Hilbert spaces | §8 |
| TQNN | — | Topological Quantum Neural Network; QNN reformulated via spin-networks and TQFT | §8 |
| Turaev–Viro invariant | — | State-sum TQFT invariant; implements quantum error-correcting codes in TQNNs | §8 |
| ZX-calculus | — | Graphical language for quantum circuits using Z-spiders, X-spiders, and Hadamard boxes | §8 |
| ZX-diagram | — | String diagram in a $\dagger$-compact closed category representing a quantum process | §8 |
| ZX rewrite rule | — | Graph-theoretic transformation preserving the semantics (linear map) of a ZX-diagram | §8 |

## H. Logical and Type-Theoretic Terms

| Term | Symbol | Definition | First Use |
| :--- | :---: | :--- | :---: |
| $\beta\text{-reduction}$ | — | Computational reduction step in $\lambda\text{-calculus}$; corresponds to cut elimination in proofs | §3 |
| Church–Rosser property | — | Confluence of $\beta\text{-reduction}$: all reduction sequences converge to the same normal form | §3 |
| Curry–Howard isomorphism | — | Correspondence between proofs and programs, propositions and types | §3 |
| Cut elimination | — | Proof normalization procedure removing intermediate lemmas; corresponds to $\beta\text{-reduction}$ | §3 |
| Graded type theory | — | Extension of type theory tracking effects (e.g., evidentiality) via graded modalities | §3 |
| Lambek calculus | — | Non-commutative intuitionistic linear logic for syntactic type assignment | §3 |
| Left residual | $A \backslash B$ | Type of an expression that, given $A$ to the left, produces $B$ | §3 |
| Residuation law | $A \otimes B \leq C \iff A \leq C / B \iff B \leq A \backslash C$ | Fundamental axiom connecting the three connectives of the Lambek calculus | §3 |
| Right residual | $B / A$ | Type of an expression that, given $A$ to the right, produces $B$ | §3 |

## I. AI and Communication Protocols

| Term | Symbol | Definition | First Use |
| :--- | :---: | :--- | :---: |
| A2A Protocol | — | Google's Agent-to-Agent protocol for cross-framework agent communication via HTTP/JSON-RPC | §9 |
| ACP | — | Agent Communication Protocol; standardizes messaging formats across agents, apps, and humans | §9 |
| ANP | — | Agent Network Protocol; three-layer architecture for trusted distributed agent interaction | §9 |
| Categorical deep learning | — | Deep learning approached through the lens of category theory (Gavranović et al.) | §9 |
| Double Categorical Systems Theory (DCST) | — | Framework using 2-categories (horizontal + vertical composition) for explainable autonomous AI | §9 |
| Functorial encryption | — | Semantic cryptography: applying a secret functor to map plaintext categories into ciphertext categories | §9 |
| lambeq | — | Quantum Natural Language Processing pipeline compiling DisCoCat diagrams to quantum circuits | §9 |
| MCP | — | Model Context Protocol; standardizes how AI agents access external tools and data sources | §9 |
| Parameterized optics / lenses | — | Categorical constructions modeling neural network components (Gavranović); attention heads as optics | §9 |
| QNLP | — | Quantum Natural Language Processing; quantum computation on DisCoCat sentence diagrams | §9 |
| Semantic cryptography | — | Encrypting compositional meaning structures (functorial encryption, diagram obfuscation, weight masking) | §9 |

## J. Diagrammatic Reasoning

| Term | Symbol | Definition | First Use |
| :--- | :---: | :--- | :---: |
| Cognitively privileged representation | — | Representation format that leverages perceptual and spatial cognition for inference | §1 |
| Diagram depth | — | Length of the longest input-to-output path through boxes; measures derivational complexity | §4 |
| Existential graphs | — | Peirce's graphical logic system conducting first-order logic entirely diagrammatically | §7 |
| Free ride | — | Shimojima's term: information extracted from a diagram without explicit inference steps | §1 |
| Hybrid reasoning | — | Giardino's term: reasoning combining perceptual pattern recognition with theoretical knowledge | §1 |
| Inferential instrument | — | Manders's term: a diagram whose spatial properties encode proof-relevant information | §6 |
| Joyal–Street theorem | — | Soundness and completeness of string-diagrammatic reasoning for monoidal categories | §3 |
| Normal form | $D_{\text{nf}}$ | Canonical form of a diagram obtained by rewriting; unique up to the axioms | §4 |

## K. Notation Conventions

| Convention | Meaning |
| :--- | :--- |
| $\mathcal{C}, \mathcal{D}$ | Categories |
| $\mathcal{V}$ | Enrichment base (monoidal category, typically $([0,1], \cdot, 1)$) |
| $\mathcal{U}$ | Universal (maximal) case category |
| $\mathcal{L}$ | Language-specific case category |
| $\mathcal{E}_{\mathbb{T}}$ | Classifying topos of theory $\mathbb{T}$ |
| $f, g, h$ | Morphisms |
| $F, G$ | Functors |
| $\alpha, \beta{}$ | Natural transformations |
| $n, s$ | Basic pregroup types: noun, sentence |
| $n^l, n^r$ | Left and right adjoints of type $n$ |
| $n_{\text{NOM}}, n_{\text{ACC}}$ | Case-subscripted noun types (e.g., nominative noun, accusative noun) |
| $N, S$ | Noun space and sentence space under the meaning functor |
| $N_{\text{NOM}}, N_{\text{ACC}}, \ldots$ | Case-specific vector subspaces in case-enriched DisCoCat |
| $\overrightarrow{\text{word}}$ | Word vector (column vector in noun space $N$) |
| $\overleftrightarrow{\text{verb}}$ | Verb tensor (element of $N \otimes S \otimes N$ for transitive verbs) |
| $\mathbf{Preg}$ | Category of pregroup types and reductions |
| $\mathbf{FVect}$ / $\mathbf{FdVect}$ | Category of finite-dimensional vector spaces and linear maps |
| $\mathbf{FHilb}$ | Category of finite-dimensional Hilbert spaces and linear maps |
| $\mathbf{Qubit}$ | Category of qubit systems with tensor product structure |
| $\mathbf{Set}$ | Category of sets and functions |
| $\otimes$ | Tensor product (monoidal product, type concatenation) |
| $\circ$ | Composition of morphisms |
| $\Rightarrow$ | Natural transformation between functors |
| $\simeq$ | Categorical equivalence |
| $\leq$ | Preorder relation on types (derivability) |
| $\gamma{}$ | Discount factor in distributional RL return computation |
| $w \in [0,1]$ | Enriched morphism weight (proto-role satisfaction degree) |
| $\varepsilon{}$ | Prediction error (active inference); also compact closure counit |
| $\eta{}$ | Compact closure unit (cap); also learning rate in some contexts |
| $\rho{}$ | Density operator (quantum state) |
| $[@key]$ | Parenthetical citation |
| `[-@key]` | Suppress-author citation |
| `\autoref{...}` | Automatic cross-reference (section or figure) |
| $Z(s,a)$ | Return distribution (DAIF); full distributional representation of returns |
| $G(\pi)$ | Expected free energy of policy (DAIF active inference) |
| $\tau{}$ | Quantile level in QR-DQN / IQN |
| $\beta{}$ | Risk-sensitivity coefficient in expected free energy |
| $\mathrm{DPE}$ | Distributional prediction error; precision-weighted Wasserstein mismatch |
| $H[Z]$ | Return distribution entropy |



---



# Appendix C: Automated Test Suite Inventory {#sec:test-suite-inventory}

This appendix summarizes the **categories** of tests behind the counts in \autoref{sec:diagrammatic-cognition}. Aggregate figures are injected at build time (**804** tests, **47** files; see `src/generate_manuscript_metrics.py` and `output/metrics.json`). Every test uses real mathematical computations—no mocks or fakes.

- **Categorical axiom tests**: Identity morphism existence, composition associativity, weight invariants, `is_well_formed()` full axiom check
- **Enriched category tests**: Hom-value constraints, composition inequality, categorical magnitude, magnitude deficit, full composition check, role clustering
- **Diagram type tests**: Pregroup diagrams validated for `dom == Ty()` and `cod == s`, correct box counts, diagram equality
- **Metrics tests**: Normal form preservation, depth computation with graceful fallback for pregroup diagrams
- **Natural transformation tests**: Component morphism construction, `naturality_holds` / `verify_naturality` on identity and incomplete maps, identity transformation generation, vertical composition of transformations, completeness checking over domain objects
- **Complexity metrics tests**: DisCoPy box/cup/cap counting on transitive/ditransitive diagrams, normal form computation and snake equation verification, syntactic complexity scoring with configurable weights, cross-diagram comparison utilities
- **Topos theory tests**: Geometric theory construction from standard and minimal case categories, classifying topos invariant computation, Morita equivalence verification (positive and negative cases), bridge transfer between equivalent theories with transfer-blocking for non-equivalent theories, enriched theory construction
- **Fluid-S tests**: Volitional/non-volitional mapping, probability splits, Bats language examples, kernel computation, enriched weight scaling
- **Active inference tests** (`tests/test_cognitive_*.py`): Belief construction and entropy, KL divergence (Gibbs' inequality, asymmetry), variational free energy, Bayesian belief update with zero-likelihood edge case, sequential multi-word belief update (five-step generative loop with entropy convergence), prediction error scaling including P600 ERP prediction with boundary weights, expected free energy decomposition (epistemic vs pragmatic), magnitude-based garden-path reanalysis cost with symmetry, N400 semantic violation proxy (including `test_cognitive_integration.py`)
- **Quantum case tests**: Crisp POVM orthogonal projectors, graded proto-role POVM, Fluid-S basis rotation, density matrix creation, \autoref{eq:eq-8-1} (in \autoref{sec:quantum-semantics}) P(c|ρ) = Tr(E_c ρ) verification
- **Cognitive security tests**: Type-violation detection, case frame validation, injection score computation, magnitude-based topological robustness, composition inequality as security boundary
- **Ditransitive tests**: Three-argument sentence creation, NOM/ACC/DAT case assignment, DisCoPy diagram with three cups, complexity comparison with transitive
- **Visualization tests** (`tests/test_visualization_*.py`): Category graphs, enriched heatmaps, functor panels, string and DisCoPy diagrams, complexity and DAIF plots, quantum and security plots, Fluid-S landscapes, syntactic panels—PNG output and structural checks where applicable
- **DAIF subpackage tests** (161 tests across 7 test files):
  - `test_daif_core.py`: Distributional Bellman operator, push-forward return, C51 categorical projection
  - `test_daif_quantile.py`: QR-DQN quantile Huber loss, IQN risk distortion (neutral/optimistic/pessimistic/CVaR), Wasserstein distances $W_1$/$W_2$
  - `test_daif_inference.py`: `distributional_case_assignment()` posterior convergence, variational message passing, Bethe free energy, expected information gain
  - `test_daif_prediction.py`: DPE precision-weighting, N400/P600 amplitude from return distributions, full `ERPProfile` waveform generation and peak latency
  - `test_daif_policy.py`: `G_policy()` EFE + risk term, Boltzmann policy temperature scaling, distributional epistemic value
  - `test_daif_metrics.py`: Convergence diagnostics (monotonicity, relative reduction), distributional KL divergence, quantile calibration error, return entropy
  - `test_daif_types.py`: `DistributionalReturn` helpers, `DAIFResult` / `ERPProfile` properties (with integration coverage of re-exported DAIF entrypoints)

```{=latex}
\newpage
```
