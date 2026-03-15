# Abstract

This review synthetically bridges case theory, categorial grammar, enriched category theory, and active inference into a single algebraic framework centered on the *cognitive case diagram*. By formalizing case systems as categories (objects mapping to case roles and morphisms to grammatical relations) and alignment typologies as functors, we render sentence structure as compact-closed string diagrams computable via the DisCoCat framework. These diagrams are not merely descriptive notation; drawing upon the cognitive science of diagrammatic reasoning and the embodied constraint of sketching thought onto a two-dimensional plane, they are executable proofs of grammaticality. We review the historical foundations from Pāṇini’s *kāraka* theory to Fillmore’s deep semantic cases and Mel’čuk’s relational networks, tracing how morphosyntactic inflection evolved into the structural skeletons of generative models where comprehension reduces to free-energy minimization. We demonstrate that this topological approach constitutes the formal algebra underlying the distributional meaning representations of modern large language models, bridging logical and connectionist semantic traditions. The framework is inherently quantitative: graded proto-roles are computed as $[0,1]$-enriched hom-values, yielding categorical magnitude as a computable complexity invariant over syntax. Topos-theoretic Morita equivalence provides algorithmic pathways for cross-linguistic grammatical induction, while Distributional Active Inference extends to modeling semantic distributions via push-forward measures. This synthesis generates falsifiable electrophysiological predictions---mapping P600/N400 amplitudes to enriched morphism weights---and extends foundational operations into quantum semantic communication, composable multi-agent protocols, and cognitive security against adversarial type-injection. Implemented within the CEREBRUM architecture, the cognitive case diagram collapses the boundaries between linguistic structure, mathematical logic, and embodied machine cognition into a unified, computationally tractable topology.
Instead, it organizes these contributions as nested pillars within a single, integrated generative model of situation semantics.



```{=latex}
\newpage
```


# Introduction: Case Diagrams and Categorical Linguistics {#sec:introduction}

## The Architecture of Case Assignment

Natural language encodes situational relations—*who does what to whom, with what, where, and why*—through various mechanisms, including noun case systems. In morphologically rich languages like Finnish, Latin, or Sanskrit, this case encoding is overt: distinct affixes mark the agent, patient, instrument, and location. In languages like Mandarin or English, this relational skeleton is orchestrated through word order and adpositions. Beyond the surface variation of morphological case, the underlying computational problem is universal: a cognitive agent benefits from assembling and assigning *structured roles* to the participants of every scenario it encounters ()), predicting and sketching relationships against the constraints of a conceptual plane.

This universality suggests that case is not merely a morphosyntactic accident, but a reflection of a deeper, embodied cognitive architecture. This paper reviews the long lineage of this hypothesis, tracing its roots from Pāṇini’s ancient *kāraka* theory (which first abstracted nominal roles derived from actions), through Roman Jakobson's structuralist feature matrices that viewed cases as oppositional spatial/semantic networks, to Fillmore's [-@fillmore1968case] "Case for Case" which posited a universal inventory of *deep cases* (Agent, Patient, Instrument). We review how Igor Mel'čuk's Meaning-Text Theory integrated these insights, treating cases as profound relational networks mapping form to deep semantic substance. Subsequent typological work by Polinsky and Preminger [-@polinsky2015case], Blake [-@blake2001grammatical], and Haspelmath [-@haspelmath2009universality] has confirmed that the space of variation across human language is tightly structured into a small number of *alignment types* related by systematic transformations.

This review highlights how **category theory** provides the natural mathematical language for formalizing this structure, and how **commutative diagrams** function not merely as convenient notation, but as *cognitively privileged, embodied representations*. By constraining relationships to a two-dimensional graph, these diagrams mimic the hand-eye coordination of sketching thought, providing inferential advantages unavailable to purely linear, sentential encodings.

## Why Diagrams? Constraints on the Plane

The cognitive science of diagrammatic reasoning provides a strong empirical foundation for this claim. To cast a problem onto a two-dimensional visual topology is to recruit the nervous system’s innate, ancient capacity for spatial navigation. Larkin and Simon [-@larkin1987diagram] demonstrated that diagrams can be computationally superior to sentential representations: their planar constraint enables efficient perceptual grouping that would otherwise require painstaking, explicit logical deduction. Shimojima [-@shimojima1996reasoning] refined this with the concept of *free ride inferences*—conclusions that "fall out" automatically from the geometric constraints of a sketch without syntactic manipulation.

In the context of case theory, commutative diagrams offer exactly these embodied advantages. A commutative triangle expressing that morphism $g \circ f$ equals morphism $h$ simultaneously encodes:

1. The compositional structure of the relation (two steps factor through an intermediate case role).
2. The *commutativity constraint* (the direct and indirect visual routes yield the same mathematical result).
3. The full relational context (the entire shape of the scenario is apprehensible in a single perceptual glance).

This is exactly the kind of gestalt understanding that linear notation obscures. \autoref{fig:case-minimal} illustrates this with a minimal three-case category. As Giardino [-@giardino2017diagrammatic] emphasizes, mathematical diagrams engage a hybrid mode of reasoning, intimately wedding perceptual pattern-recognition with theoretical knowledge—a mode effortlessly aligned with the predictive processing architecture of active inference [@friston2017active]. The intellectual lineage traces through Peirce's *existential graphs*: his spatial logic system proved that first-order reasoning can be conducted entirely diagrammatically on a "sheet of assertion." Our case diagrams extend this Peircean tradition into relational semantics: inference proceeds not by algebraic churning, but by tracing lines and composing arrows—drawing the contours of thought itself.

![A minimal case category $\mathcal{C}$ with three objects---Agent (NOM), Patient (ACC), and Instrument (INS)---and three morphisms: $f\colon\text{NOM}\to\text{ACC}$ (transitive action, weight $w=0.9$), $g\colon\text{INS}\to\text{ACC}$ (instrumental application, $w=0.7$), and the composite $g \circ h\colon\text{NOM}\to\text{INS}\to\text{ACC}$ (acts-via, $w=0.9 \times 0.7 = 0.63$). The commutative triangle encodes that the direct path $f$ and the factored path $g \circ h$ yield the same patient---making the argument-structure factorization through the instrument role visually immediate. This exemplifies Shimojima's [-@shimojima1996reasoning] free-ride inference: the two-dimensional layout reveals compositional structure that linear notation obscures.](output/figures/case_category_minimal.png){#fig:case-minimal}

## Five Converging Research Pillars

The present synthesis draws on five research traditions, each contributing an essential formal ingredient:

### Pillar 1: Case Systems, Alignment Typology, and Grammatical Relations

The empirical foundation comes from linguistic typology. We formalize the case inventory and alignment systems catalogued by Polinsky and Preminger [-@polinsky2015case], Claassen [-@claassen2025alignment], and Wu [-@wu2024amis] as categories with case roles as objects and grammatical relations as morphisms. Dowty's [-@dowty1991thematic] proto-role theory—which decomposes thematic roles into clusters of entailments rather than discrete atoms—motivates our use of enriched (weighted) morphisms. **Our novel addition, Synthetic Case-Role Algebra, extends this by formalizing these proto-roles as objects in a [0,1]-enriched monoidal category, enabling purely algebraic manipulation of semantic roles contextually.**

### Pillar 2: Categorial and Type-Theoretic Grammar

Lambek's [-@lambek1958mathematics] syntactic calculus reformulates grammatical combination as algebraic cancellation in a pregroup, yielding derivations that can be visualized as Joyal and Street's [-@joyalstreet1991geometry] string diagrams. Song [-@song2022act] extends this with monadic semantics for root syntax, showing that category-theoretic structure reaches down to the sublexical level.

### Pillar 3: Categorical Compositional Distributional Semantics (DisCoCat)

Coecke, Sadrzadeh, and Clark's [-@coecke2010mathematical] DisCoCat framework composes distributional word meanings according to syntactic structure using monoidal categories and string diagrams. This framework bridges the two great traditions of linguistic meaning---formal (truth-conditional, compositional) and distributional (context-dependent, statistical)---by using the algebra of compact closed categories to compose vector representations according to type-logical derivations. The resulting categorical semantics provides the *algebraic formalization* of the distributional programme that modern large language models (from Word2Vec [@mikolov2013efficient] through transformer architectures [@vaswani2017attention; @devlin2019bert]) implement empirically, making it possible to analyse both symbolic and neural approaches to language within a single mathematical framework. Recent extensions include DisCoCirc [@defelice2020discourse; @defelice2022discocirc] for discourse-level coherence and the lambeq library [@lorenz2023lambeq] for quantum NLP, which implements the full categorical pipeline on quantum hardware.

### Pillar 4: Enriched Category Theory and Distributional Measures

Bradley et al.'s [-@fritz2021enriched] enrichment over $[0,1]$ equips hom-sets with distributional proximity measures. Bradley's [-@bradley2020entropy; -@bradley2024ipam] work on topological operads and categorical magnitude provides information-theoretic invariants that quantify the "effective size" of a linguistic category—a measure that captures how much distributional information the category encodes. Leinster and Shulman [-@leinster2021magnitude] extend this to **magnitude homology**, categorifying magnitude into a graded homological invariant that detects higher-dimensional structural differences between case systems indistinguishable by scalar magnitude alone.

### Pillar 5: Topos-Theoretic Bridges and Inter-Theoretic Transfer

Caramello's [-@caramello2016bridges; -@caramello2021five; -@caramello2023syntactic] bridge technique uses classifying toposes as transfer points between mathematical theories, enabling results proved in one formalization of case to port automatically to another. Phillips [-@phillips2024lot] strengthens this by showing that the Language of Thought admits universal constructions in a topos, grounding the systematicity of case assignment in the deepest structures of categorical logic.

## Unifying Integration: Active Inference and the CEREBRUM Architecture

The unifying framework is **active inference** [@friston2017active], which casts cognition as approximate Bayesian inference under a generative model. Case-marked commutative diagrams serve as the structural core of such generative models: each diagram specifies a pattern of expected relational dependencies, and the agent's task in understanding (or producing) a sentence is to minimize surprise relative to this diagrammatic prior. The **CEREBRUM** architecture [@friedman2024cerebrum]---Case-Enabled Reasoning Engine with Bayesian Representations for Unified Modeling---provides a computational instantiation of this framework, with case roles as functional specializations of model components in an active inference cycle.

This integration is not merely metaphorical. The situation semantics of Barwise and Perry [-@barwise1983situations] already conceptualized meaning as structured *situations* with typed constituents—an ontology that maps naturally onto the objects and morphisms of our case categories. Active inference adds dynamics: the agent actively samples evidence to confirm or update its case assignments, using diagrammatic structure to guide exploration.

## Paper Outline and Chapter Overview

The remainder of the paper is organized as follows. \autoref{sec:case-systems} reviews case systems and alignment typology, formalizing them as categories with functors between alignment types—including Fluid-S as a context-dependent functor parameterized by agentive volition. \autoref{sec:categorial-grammar} develops the categorial grammar foundations, including pregroup types, string diagrams, and passivization as algebraic type permutation. \autoref{sec:categorical-semantics} presents the DisCoCat framework and its case-enriched extension, demonstrating that categorical semantics provides the algebraic formalization of the distributional programme underlying modern LLMs. \autoref{sec:compact-closure-discourse} extends the framework through the compact closure axiom, diagrammatic complexity metrics, DisCoCirc discourse circuits with case role reversal, and the lambeq Gen II quantum NLP pipeline. \autoref{sec:enriched-categories} introduces $[0,1]$-enriched categories with categorical magnitude and magnitude homology as complexity and topological invariants. \autoref{sec:topos-theory} develops Caramello's topos-theoretic bridges for inter-theoretic transfer via Morita equivalence, with a four-phase algorithmic sketch for topos-theoretic grammatical induction. \autoref{sec:cognitive-integration} integrates the five pillars within active inference, CEREBRUM, and Distributional Active Inference, deriving falsifiable electrophysiological predictions linking enriched weights to ERP amplitudes. \autoref{sec:quantum-active-inference} extends the framework into quantum topological computation via TQNNs, the ZX-calculus, and sheaf-theoretic semantic communication. \autoref{sec:ai-implications} develops implications for categorical deep learning, multi-agent protocols, and compositional game theory. \autoref{sec:cognitive-security} introduces case-theoretic firewalls and epistemic case security as defenses against adversarial case-frame manipulation, with a formal characterization of prompt injection as decidable categorical type violation. \autoref{sec:conclusion} concludes with eleven contributions and nine future research directions.
The following sections develop this roadmap in detail.



```{=latex}
\newpage
```



# Case Systems: Typology, Alignment, and Graded Roles {#sec:case-systems}

## Historical Traditions and Foundational Concepts

### The Pāṇinian Kāraka Framework

The formal study of grammatical case traces its origins to the Sanskrit grammarian Pāṇini (circa 4th century BCE), whose *Aṣṭādhyāyī* formalized the *kāraka* theory. This theory was the first to classify semantic roles—such as agent, patient, and instrument—as deep relational functions linking verbs to their arguments, entirely abstracting away from surface morphosyntactic inflections. Etymologically meaning "that which brings about" an action, the kāraka system emphasized semantic relations over mere grammatical markers, providing a rigorous mapping from conceptual predication to phonological representation [-@jha2021sanskrit; -@kak1987paninian].

### Jakobson’s Structural Features and the Prague School

This profound semantic foundation laid dormant for millennia until it was structurally resurrected and evolved in the mid-20th century. Roman Jakobson's *Morphologic Inquiry into Slavic Declension* (1958) and his earlier Prague School writings decomposed grammatical cases into binary distinctive features (e.g., [±directional], [±peripheral]) [-@jakobson1958morphologic]. By treating case oppositions analogously to phonological features, Jakobson shifted the analysis from Pāṇini's holistic roles to a componential analysis that exposed deep relational hierarchies and markedness, viewing cases as part of a dynamic, semiotic network suited for communicative tasks. Concurrently, Louis Hjelmslev's *La catégorie des cas* [-@hjelmslev1935categorie] resonated deeply within this functionalist tradition by positing case as a purely relational category.

### Fillmore’s Deep Case and Generative Roots

Charles Fillmore's seminal "The Case for Case" (1968) built directly upon this structuralist lineage, explicitly reinterpreting these concepts within the burgeoning generative linguistics framework. Fillmore proposed *deep cases* (e.g., Agentive, Objective, Dative) as universal semantic primitives that underlie surface syntax, arguing that surface structures derive from underlying *case frames* assigned by verbs [-@fillmore1968case]. This effectively evolved Pāṇini's kāraka and Jakobson's features into deep relational networks, prioritizing universal semantics over language-specific morphology.

### Mel'čuk’s Meaning-Text Theory (MTT)

This progression culminated in Igor Mel'čuk's Meaning-Text Theory (MTT), initiated alongside Russian collaborators like Alexander Žolkovskij and Yuri Apresjan. MTT formalized cases within a rigorous semantic-syntactic network, positing that deep semantic structures exist as labeled dependency trees populated by *actants* (semantic roles akin to kāraka). These are mapped via *lexical functions* to surface syntax and morphology. Mel'čuk’s extensive Russian grammatical corpus explicitly conceptualized morphosyntactic inflection as the end-stage realization of deep semantic relations, mapping meaning to text monotonically through hierarchical graphs.

### Dowty’s Proto-Roles and Graded Topologies

Fillmore's deep cases are the direct precursors to modern *thematic role* theory. Dowty [-@dowty1991thematic] refined the approach by decomposing thematic roles into clusters of sentential entailments, yielding two *proto-roles*: the Proto-Agent (characterized by volitional involvement, causation) and the Proto-Patient (characterized by an incremental theme, causal affectedness). This decomposition is significant for our categorical formalization because it replaces discrete nodes with a *graded* structural topology—morphisms in our cognitive case diagrams can carry statistical weights reflecting the continuous degree to which a noun phrase satisfies proto-role entailments.

## The Cross-Linguistic Typological Landscape

Contemporary typological work reveals that the world's languages realize case systems according to a small number of *alignment types*—systematic patterns governing how the core arguments of transitive and intransitive clauses are grouped [@polinsky2015case; @blake2001grammatical; @haspelmath2009universality].

### Core Argument Roles

The cross-linguistic comparison rests on three primitives:

| Symbol | Role | Definition |
| :---: | :---- | :--- |
| **S** | Sole argument of intransitive | "The child **sleeps**" |
| **A** | Agent-like argument of transitive | "**The child** broke the vase" |
| **P** | Patient-like argument of transitive | "The child broke **the vase**" |

### Alignment Systems

The key insight from typological research is that languages differ in how they *group* these three roles for purposes of case marking, agreement, and other grammatical processes:

| Alignment | Grouping | Exemplar Languages |
| :--- | :--- | :--- |
| **Nominative–Accusative** | S = A $\neq$ P | English, Latin, Finnish, Russian |
| **Ergative–Absolutive** | S = P $\neq$ A | Basque, Dyirbal, Georgian (partly) |
| **Active–Stative** | S splits by agentivity | Lakhota, Guaraní, Eastern Pomo |
| **Tripartite** | S $\neq$ A $\neq$ P | Nez Perce, some Australian languages |
| **Fluid-S** | S marking varies by context | Bats (NE Caucasian), Acehnese |

**Fluid-S and Context-Dependent Functors.** In Bats (Nakh-Daghestanian), the intransitive subject of the same verb surfaces in different cases depending on the speaker's construal of agentive volition. The verb *fall* takes an absolutive S when the falling is accidental (*The child-ABS fell*) but an ergative S when the falling is volitional or self-propelled (*The child-ERG fell [on purpose]*).

Categorically, we model Fluid-S as a **context-dependent functor** $F_\theta: \mathcal{U} \to \mathcal{L}$ parameterized by a volition feature $\theta \in [0,1]$. This functor satisfies naturality only up to a probabilistic reparameterization of the context $\theta$. \autoref{fig:fluid-s} visualizes the resulting volition landscape, where case categorization boundaries shift dynamically as a function of the agent's internal construal.

![Fluid-S volition landscape visualizing the continuous shift in case marking for intransitive subjects (S) as a function of agentive volition $\theta \in [0,1]$. For low-volition actions ($\theta \to 0$, e.g., "falling accidental"), the functor $F_\theta$ maps S to the ABS region of the target category. For high-volition actions ($\theta \to 1$, e.g., "jumping volitional"), the functor $F_\theta$ maps S to the ERG region. This transformation represents a non-rigid alignment system where the morphological realization of a participant is an emergent property of the speaker's internal state—formalized here as a parameterized functor between case categories.](output/figures/fluid_s_volition_landscape.png){#fig:fluid-s}

**Synthetic Case-Role Algebra.** We introduce Synthetic Case-Role Algebra as a novel addition to the Dowty-style proto-role framework. While Dowty models proto-roles (Agent/Patient) as static clusters of entailments [-@dowty1991thematic], we formalize them as **objects in a [0,1]-enriched monoidal category**. This enables purely algebraic manipulation of semantic roles: roles can be composed, weighted, and transformed through functorial operations that represent complex event structures. The enriched structure ensures that "case assignment" is not a discrete choice, but a vector-valued expectation in the case space—providing a rigorous bridge to the neural representations in the subsequent chapters.

Claassen [-@claassen2025alignment] provides a comprehensive survey of the explanatory frameworks proposed for alignment diversity, arguing that no single factor (processing efficiency, disambiguation, discourse pragmatics) suffices—a conclusion that motivates our multi-dimensional categorical formalization. Wu [-@wu2024amis] offers a detailed case study of Amis (Austronesian), demonstrating how verb classification, case marking, and grammatical relations interact in a language that defies simple alignment classification.

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

## Categorical Formalization of Case Systems

### Case Categories as Directed Graphs

We define a **case category** $\mathcal{C}$ as a small category where:

- **Objects** are case roles (NOM, ACC, GEN, DAT, INS, LOC, ABL, VOC)
- **Morphisms** are grammatical relations between roles (e.g., "transitive action": NOM → ACC)
- **Identity morphisms** represent the reflexive relation of each case role to itself
- **Composition** models the transitivity of grammatical dependencies

This formalization is implemented in our `CaseCategory` class, which uses set-based object tracking and list-based morphism storage as the underlying representation. Each object carries its role enum and optional morphosyntactic features; each morphism carries a relation label and an enriched weight $w \in [0,1]$. \autoref{fig:case-standard} shows the full eight-case standard category.

![The standard linguistic case category $\mathcal{C}$ with eight objects (NOM, ACC, GEN, DAT, INS, LOC, ABL, VOC) and directed morphisms encoding grammatical relations. Edge labels identify relation types (transitive\_action: NOM$\to$ACC, possession: GEN$\to$NOM, transfer: ACC$\to$DAT, spatial\_grounding: LOC$\to$ACC) while edge weights $w \in [0,1]$ reflect proto-role satisfaction per Dowty's [-@dowty1991thematic] decomposition. The enriched structure over $([0,1], \cdot, 1)$ ensures that composition attenuates weights multiplicatively ([@eq:eq-2-1]): a chain NOM$\to$ACC$\to$DAT with weights $0.9$ and $0.7$ yields composite weight $0.63$. Generated programmatically from the `CaseCategory` class.](output/figures/case_category_standard.png){#fig:case-standard}

### Alignment Functors Between Case Categories

An **alignment functor** $F: \mathcal{U} \to \mathcal{L}$ maps a universal (maximal) case category $\mathcal{U}$ to a language-specific category $\mathcal{L}$ by collapsing objects that a particular language treats as equivalent. For example, in an accusative language, the functor merges S and A into a single NOM role while keeping P as a distinct ACC role: $F(\text{S}) = F(\text{A}) = \text{NOM}$, $F(\text{P}) = \text{ACC}$.

This functor is:

- **Surjective on objects**: every case in the target language is the image of some universal role
- **Structure-preserving**: grammatical relations in $\mathcal{U}$ map to grammatical relations in $\mathcal{L}$
- **Non-identity when alignment differs**: the kernel of $F$ (the set of objects mapped to the same target) characterizes the alignment type

The alignment functor provides a formal account of neutralization: two semantically distinct roles (S vs. A) receive the same morphological treatment because the functor maps them to the same object.

**Explicit functor construction.** Let $\mathcal{U}$ be the universal three-role category with objects $\{S, A, P\}$ and morphisms $f\colon A \to P$ (transitive action), $g\colon S \to S$ (intransitive). The accusative functor $F_{\text{acc}}\colon \mathcal{U} \to \mathcal{L}_{\text{acc}}$ and ergative functor $F_{\text{erg}}\colon \mathcal{U} \to \mathcal{L}_{\text{erg}}$ act on objects as:

$$F_{\text{acc}}(S) = F_{\text{acc}}(A) = \text{NOM}, \quad F_{\text{acc}}(P) = \text{ACC} $$ {#eq:eq-2-3}

$$F_{\text{erg}}(S) = F_{\text{erg}}(P) = \text{ABS}, \quad F_{\text{erg}}(A) = \text{ERG} $$ {#eq:eq-2-4}

On morphisms, each functor preserves the transitive morphism: $F_{\text{acc}}(f) = f'\colon \text{NOM} \to \text{ACC}$ and $F_{\text{erg}}(f) = f''\colon \text{ERG} \to \text{ABS}$. The *kernel* of $F_{\text{acc}}$---the set $\{(X,Y) \mid F_{\text{acc}}(X) = F_{\text{acc}}(Y)\}$---is $\{(S,A)\}$, encoding that the intransitive subject and transitive agent are identified. The kernel of $F_{\text{erg}}$ is $\{(S,P)\}$, encoding the ergative identification of intransitive subject with patient. This kernel structure provides a compact algebraic fingerprint of each alignment type.

\autoref{fig:alignment} shows three alignment systems rendered from our `CaseCategory` implementation.

![Side-by-side comparison of three alignment systems realized as functors from the universal category $\mathcal{U} = \{S, A, P\}$. **Nominative--Accusative**: $F_{\text{acc}}(S) = F_{\text{acc}}(A) = \text{NOM}$, $F_{\text{acc}}(P) = \text{ACC}$ (kernel $\{(S,A)\}$, [@eq:eq-2-3]). **Ergative--Absolutive**: $F_{\text{erg}}(S) = F_{\text{erg}}(P) = \text{ABS}$, $F_{\text{erg}}(A) = \text{ERG}$ (kernel $\{(S,P)\}$, [@eq:eq-2-4]). **Tripartite**: $F_{\text{tri}}$ is injective (kernel $\emptyset$)---each role receives distinct marking. Color-coded nodes reveal the neutralization pattern: shared colors indicate functor identification of roles.](output/figures/alignment_comparison.png){#fig:alignment}

![Categorical composition in the enriched case category: morphism $f\colon\text{NOM}\to\text{ACC}$ (transitive action, $w_f=0.9$) and morphism $g\colon\text{ACC}\to\text{DAT}$ (transfer, $w_g=0.7$) compose to yield $g \circ f\colon\text{NOM}\to\text{DAT}$ with weight $w(g \circ f) = w_g \cdot w_f = 0.63$ ([@eq:eq-2-1]). The commutative triangle encodes that indirect object (DAT) assignment factors through the direct object (ACC)---the multiplicative attenuation reflects the typological observation that subject--recipient relations are weaker than the individual subject--object and object--recipient links.](output/figures/composition_triangle.png){#fig:composition}

### Enriched Morphisms, Proto-Roles, and Graded Structure

Following Dowty [-@dowty1991thematic], we equip morphisms with weights in $[0,1]$ that encode the degree of proto-role satisfaction. A morphism $f: \text{NOM} \to \text{ACC}$ with weight $w = 0.9$ indicates a strong transitive action (clear agent acting on clear patient), while $w = 0.4$ might indicate an experiencer construction ("The child fears the dark") where the nominative argument only weakly satisfies Proto-Agent entailments.

Composition of enriched morphisms multiplies weights:
$$w(g \circ f) = w(g) \cdot w(f) $$ {#eq:eq-2-1}

This multiplicative composition reflects the intuition that grammatical dependencies attenuate as they chain through intermediate roles. \autoref{fig:composition} illustrates the categorical composition of two morphisms through an intermediate case role. The resulting structure is a category enriched over $([0,1], \cdot, 1)$—a connection we develop fully in \autoref{sec:enriched-categories}.

### Natural Transformations Between Alignment Systems

Having established that alignment systems are functors $F, G: \mathcal{U} \to \mathcal{L}$ from a universal case category to language-specific categories, a natural question arises: *how do different alignment systems relate to each other?* The categorical answer is a **natural transformation** $\alpha: F \Rightarrow G$—a systematic family of morphisms $\alpha_A: F(A) \to G(A)$ for each case role $A$, satisfying the **naturality condition**:

$$G(f) \circ \alpha_A = \alpha_B \circ F(f) \quad \text{for every morphism } f: A \to B $$ {#eq:eq-2-2}

This condition ensures that the transformation respects the grammatical structure: transforming from one alignment's output and then applying a grammatical relation yields the same result as first applying the relation and then transforming.

**Worked example.** Consider the accusative-to-ergative functor $F$ mapping S and A to NOM while P maps to ACC, and the tripartite functor $G$ mapping each core role to a distinct surface case (S $\to$ ABS, A $\to$ ERG, P $\to$ ACC). The **identity natural transformation** $\text{id}_F: F \Rightarrow F$ has components $(\text{id}_F)_A = \text{id}_{F(A)}$ for every role $A$—trivially satisfying naturality. The **vertical composition** $\beta \circ \alpha$ of two natural transformations $\alpha: F \Rightarrow G$ and $\beta: G \Rightarrow H$ is defined componentwise: $(\beta \circ \alpha)_A = \beta_A \circ \alpha_A$.

Our `NaturalTransformation` class implements these operations, with `ComponentMorphism` objects encoding each $\alpha_A$, and `compose_transformations()` implementing vertical composition. The `IdentityNaturalTransformation` constructor automatically generates identity components for every object in an `AlignmentFunctor`'s domain. This machinery provides the formal infrastructure for comparing alignment types not merely by listing their neutralization patterns but by characterizing the *structural mappings* between them—e.g., the natural transformation from accusative to tripartite alignment is injective (no two roles merge in the target), while the transformation from tripartite to ergative is non-injective (S and P merge into ABS).



```{=latex}
\newpage
```



# Categorial Grammar: Type Logic and String Diagrams {#sec:categorial-grammar}

## From Phrase Structure Rules to Algebraic Type Assignment

Traditional generative grammar assigns sentence structure through phrase-structure rules that recursively combine constituents into larger units. Categorial grammar inverts this perspective: rather than specifying construction rules, it assigns each lexical item a *type* that encodes its combinatory potential. A transitive verb like "chases" is not described as "a word that takes a subject NP and an object NP to form a VP" but rather as having the type $(n \backslash s) / n$—an entity that seeks a noun to its right (the object) and a noun to its left (the subject) in order to produce a sentence.

## Lambek's Residuated Syntactic Calculus

The algebraic foundations were laid by Lambek [-@lambek1958mathematics], who introduced a *residuated* structure on syntactic types: two binary operations, the left residual $\backslash$ and the right residual $/$ of the multiplicative connective $\otimes$ (concatenation). The key axiom is the residuation law:

$$A \otimes B \leq C \quad \iff \quad A \leq C / B \quad \iff \quad B \leq A \backslash C $$ {#eq:eq-3-1}

This law captures the fundamental duality of syntax: a verb of type $(n \backslash s) / n$ *consumes* noun arguments to *produce* a sentence. The resulting **Lambek calculus** is a non-commutative intuitionistic linear logic—non-commutative because word order matters, and linear because each resource (word) is used exactly once.

### Pregroup Grammars and Compact Closed Structure

Lambek [-@lambek2004fine] later simplified the framework to **pregroup grammars**, where each type $a$ has a left adjoint $a^l$ and a right adjoint $a^r$ satisfying:

$$a^l \cdot a \leq 1 \leq a \cdot a^l \qquad a \cdot a^r \leq 1 \leq a^r \cdot a $$ {#eq:eq-3-2}

This formal structuralism was revolutionized by Coecke, Sadrzadeh, and Clark's introduction of the **DisCoCat** (Distributional Compositional Categorical) model in 2010 [-@coecke2010mathematical]. DisCoCat unifies categorial grammar with distributional semantics by defining strong monoidal functors from pregroup grammars to vector spaces. As Duneau (2021) summarizes, "The distributional compositional approach to modelling meaning... allows the meaning of a sentence to be computed as a function of both the distributional meaning of the words involved, as well as its grammatical form" [-@duneau2021parsing]. By demonstrating that pregroups and finite-dimensional vector spaces are both rigid monoidal categories, DisCoCat enables sentence meanings to be computed linearly from constituent word meanings.

Grammaticality reduces to checking whether a sequence of types reduces to the sentence type $s$ via these *contraction* ($a^l \cdot a \to 1$) and *expansion* ($1 \to a \cdot a^l$) steps. This reformulation is crucial for the DisCoCat framework (\autoref{sec:categorical-semantics}) because pregroups form **compact closed categories**, which have a well-developed diagrammatic calculus.

## String Diagrams for Syntactic Derivation

The pivotal connection between categorial grammar and visualization comes from Joyal and Street [-@joyalstreet1991geometry], who proved that morphisms in monoidal categories can be faithfully represented as *string diagrams*—planar graphs where:

- **Wires** represent types (objects of the category)
- **Boxes** represent words or operations (morphisms)
- **Vertical composition** represents sequential application
- **Horizontal juxtaposition** represents the tensor product (concatenation)
- **Cups and caps** represent the contraction/expansion of a pregroup

\autoref{fig:string-diagram} shows a DisCoCat-style string diagram for the sentence "Alice chases Bob," generated by our visualization pipeline. The noun wires connect to the verb's input slots, and the sentence wire emerges from the verb's output—the entire derivation from word types to sentence type is visible at a glance.

![A 1×3 visualization of DisCoPy pregroup grammar derivations showing increasing sentence complexity. Panel (a): intransitive "Bob runs" (NOM) with one cup. Panel (b): transitive "Alice chases Bob" (NOM+ACC) with two cups contracting noun types into the verb. Panel (c): passive "Bob is-chased" showing patient promotion to subject position via a reduced pregroup type.](output/figures/discopy_sentence_progression.png){#fig:string-diagram}

![Structural isomorphism of pregroup grammar derivations across 3 typologically diverse languages: English (SVO), Latin (inflected, free order), and Japanese (agglutinative, SOV). Each image renders the transitive meaning "SUBJ chases OBJ" as a DisCoPy string diagram with identical type-logical structure---$n \otimes (n^r \otimes s \otimes n^l) \otimes n \to s$---demonstrating that the meaning functor's type reduction is invariant under surface word-order permutation. This confirms the central claim of categorial grammar: syntactic universals reside in the type algebra, not in linear word order.](output/figures/discopy_multilingual.png){#fig:multilingual-isomorphism}

The *soundness and completeness* of string-diagrammatic reasoning (Joyal–Street theorem) guarantees that any conclusion drawn from the diagram is algebraically valid.

This visual transparency is precisely the "free ride" phenomenon identified by Shimojima [-@shimojima1996reasoning]: the diagram simultaneously represents the syntactic derivation, the argument structure, and the compositional flow of meaning, without requiring explicit inference steps to relate them.

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

The two `Cup` contractions cancel $n$ with $n^r$ (subject–verb) and $n^l$ with $n$ (verb–object), reducing the five-wire tensor product to the single sentence wire $s$. The assertion `diagram.cod == s` is a machine-checkable proof of grammaticality.

**From pregroup types to graded types.** The standard pregroup derivation culminates in a binary grammaticality judgment: either the final codomain ($\text{cod}$) of the tensor contraction exactly equals the sentence type $s$ (meaning the string is perfectly grammatical), or it does not (meaning it is ill-formed). This crisp true/false distinction can be *graded* by replacing the Boolean algebra $\{0,1\}$ underlying classical type matching with the unit interval $[0,1]$. This yields a graded type theory where type judgments carry continuous confidence weights. Asudeh and Giorgolo [-@asudeh2020graded] develop this approach via a monadic semantics that wraps base types in a computational effect encoding uncertainty. In our framework, this corresponds precisely to the $[0,1]$-enrichment of \autoref{sec:enriched-categories}: the enriched weight on a morphism $f: A \to B$ is the confidence that the case assignment $A \to B$ is well-typed. Categorical magnitude (\autoref{sec:enriched-categories}) then aggregates these local confidence scores into a global complexity measure for the entire derivation. The progression from crisp pregroup types through graded types to fully enriched categories is mathematically a sequence of base-change functors: $\mathbf{Bool} \hookrightarrow [0,1] \hookrightarrow \mathbf{R}_{\geq 0}$, where each level adds representational capacity for nuance at the cost of computational complexity.

![DisCoPy rendering of the pregroup derivation for "Alice chases Bob," corresponding to the code block above. The three Word boxes carry types $n$ (Alice), $n^r \otimes s \otimes n^l$ (chases), and $n$ (Bob). Two Cup contractions $\varepsilon\colon n^r \otimes n \to 1$ and $\varepsilon\colon n^l \otimes n \to 1$ cancel adjoint type pairs, reducing the five-wire tensor product to the single sentence wire $s$. By the Curry--Howard correspondence, this diagram is simultaneously a syntactic derivation, a proof of well-typedness, and (under the meaning functor of \autoref{sec:categorical-semantics}) a specification of compositional semantic computation. Our novel extension, **DisCoCirc entity wires**, decorates these $n$-typed wires with functorial states $S: \mathbf{Ent} \to \mathbf{Case}$, tracking role assignments across discourse boundaries.](output/figures/discopy_transitive.png){#fig:discopy-transitive}

## Case Marking in Type-Logical Categorial Grammar

Case-marked noun phrases receive compound types that encode both their grammatical role and their combinatory potential. In a nominative–accusative language, we can assign:

| Expression | Type | Gloss |
| :--- | :--- | :--- |
| "Alice" (subject) | $n_{\text{NOM}}$ | Noun, nominative-marked |
| "the ball" (object) | $n_{\text{ACC}}$ | Noun, accusative-marked |
| "kicks" | $(n_{\text{NOM}} \backslash s) / n_{\text{ACC}}$ | Seeks ACC right, NOM left |
| "to Bob" (recipient) | $(s \backslash s) / n_{\text{DAT}}$ | Modifies sentence via DAT argument |

The subscripts refine the basic noun type $n$ with case features, ensuring that "kicks" selects a nominative subject and an accusative object. Mismatch in case features blocks the derivation, modeling ungrammaticality.

**Alignment as Natural Transformation.** A key contribution of this work is the realization that **case alignment is a natural transformation** $\eta: \text{Id} \Rightarrow F \dashv G$ between functors in the pregroup category. This formalizes the grammatical "agreement" between constituents as a consistency requirement on these natural transformations, ensuring that the alignment chosen for the subject is functorially compatible with the verb's requirements. This categorical perspective elevates alignment from a surface property to a fundamental topological constraint on the string diagram.

## The Curry--Howard Correspondence and Proof-Theoretic Semantics

A deep structural parallel underlies the Lambek calculus: derivations of syntactic types correspond to proofs in intuitionistic logic (via the Curry–Howard isomorphism), and therefore to programs in a typed lambda calculus. Specifically:

| Syntactic Domain | Logical Domain | Computational Domain |
| :--- | :--- | :--- |
| Types $(A / B, A \backslash B)$ | Propositions | Types |
| Derivations | Proofs | Programs ($\lambda$\text{-terms}) |
| Cut elimination | Proof normalization | $\beta$-reduction |
| Commutativity of cuts | Confluence of rewriting | Church–Rosser property |

This correspondence has two important consequences for our framework:

1. **Semantic compositionality follows from syntactic well-formedness**: a well-typed derivation automatically yields a well-formed meaning representation (the $\lambda$-term extracted from the proof).

2. **Case assignment is type inference**: determining the case of a noun phrase in context is equivalent to inferring the type of a variable in a $\lambda$-expression—a computational problem with well-understood algorithms.

## Monadic Semantics for Sublexical Root Syntax

Song [-@song2022act; -@song2022blog] extends the categorial framework with a **monadic semantics** for root syntax, modeling the sublexical decomposition of verb roots using monads in a syntactic category. This approach captures the intuition that a verb like "break" has internal compositional structure—a causative layer and a result-state layer—that interacts with case assignment. The monad encapsulates the complexity of root meaning within a single categorical construction, allowing the type-logical grammar to handle both lexical and syntactic composition uniformly.

The monadic approach connects naturally to graded type theory: Asudeh and Giorgolo [-@asudeh2020graded] develop a monadic semantics for evidentiality that uses graded effects to track the epistemic status of propositions—a pattern that extends to case, where the "grade" of a morphism could encode the strength of a semantic role assignment.

## Passivization as Algebraic Type Permutation

One of the most revealing case-theoretic operations is **passivization**, which transforms an active transitive clause into a passive construction by promoting the patient to subject position and (optionally) demoting the agent to an oblique role. In our categorical framework, passivization is not an ad hoc syntactic transformation but a precise *type permutation*—a swap of the noun types feeding into the verb's pregroup derivation.

In a pregroup grammar, the active transitive "Alice chases Bob" has the type reduction:

$$n_{\text{NOM}} \cdot (n^r \cdot s \cdot n^l) \cdot n_{\text{ACC}} \to s $$ {#eq:eq-3-3}

Passivization permutes the noun arguments, yielding "Bob is chased by Alice" with the swapped type assignment:

$$n_{\text{ACC}} \cdot (n^r \cdot s \cdot n^l) \cdot n_{\text{NOM}} \to s $$ {#eq:eq-3-4}

Crucially, DisCoPy's `Swap` primitive makes this permutation explicit and algebraically precise: the swap operation $\sigma_{n,n}: n \otimes n \to n \otimes n$ permutes the two noun wires without violating the monoidal structure. The resulting diagram differs from the active version precisely in the crossing of the noun wires—making the voice alternation *visible* as a topological feature of the string diagram.

This diagrammatic transparency exemplifies Shimojima's [-@shimojima1996reasoning] free-ride inference: by inspecting the diagram, one can immediately see that passivization preserves the verb's inherent argument structure while rearranging the surface realization—a fact that requires multiple inference steps to establish in a linear notation.

The structural difference between voice alternations is a topological change in wire connectivity: passivization removes one Cup contraction, lowering the syntactic complexity score of [@eq:eq-4-4].](output/figures/discopy_passive.png){#fig:discopy-passive}



```{=latex}
\newpage
```



# Categorical Semantics: DisCoCat and Compositional Flow {#sec:categorical-semantics}

## Two Traditions of Meaning: Formal and Distributional

The study of linguistic meaning has long been divided between two traditions with complementary strengths and weaknesses:

1. **Formal semantics**, following Montague [-@montague1973proper], assigns meaning compositionally: the meaning of a complex expression is a function of the meanings of its parts and the way they are syntactically combined. This tradition excels at capturing logical structure (quantification, negation, modality) but struggles with lexical meaning—it typically treats content words as unanalyzed primitives.

2. **Distributional semantics** assigns meaning empirically: a word's meaning is characterized by its distribution across contexts, typically encoded as a vector in a high-dimensional space. The distributional hypothesis—"You shall know a word by the company it keeps" [@firth1957papers]—traces to J.R. Firth's contextual theory of meaning and, independently, to Zellig Harris's [-@harris1954distributional] algebraic analysis of distributional structure, which demonstrated that linguistic elements occurring in similar environments share semantic properties. This tradition captures graded similarity and analogy but lacks compositional structure—the meaning of "dog bites man" and "man bites dog" may receive identical vector representations.

The tension between these two traditions is one of the deepest in the science of language. Turney and Pantel's [-@turney2010frequency] comprehensive survey of vector space models showed that distributional methods capture remarkably fine-grained semantic distinctions—synonymy, antonymy, hypernymy, analogy—but only at the word level. Baroni and Lenci [-@baroni2010distributional] developed a tensor-based *Distributional Memory* framework that partially addresses compositionality by structuring co-occurrence data as a three-way tensor over (word, relation, word) triples, but without a principled type-logical backbone. Lenci [-@lenci2018distributional] surveys the modern landscape and identifies the central open problem: how to reconcile the *algebraic compositionality* of formal semantics with the *empirical grounding* of distributional models.

The **DisCoCat** (Distributional Compositional Categorical) framework [@coecke2010mathematical] resolves this tension by using category theory to compose distributional meanings according to syntactic structure—achieving, for the first time, a framework that is simultaneously *compositional* (from categorial grammar), *distributional* (from corpus-derived vector spaces), and *algebraically principled* (from monoidal category theory).

## From Static Embeddings to Contextual Representations: LLMs as Distributional Models

The distributional programme has undergone a dramatic computational intensification in the era of large language models (LLMs). The trajectory from classical co-occurrence matrices through static word embeddings to contextual transformers can be understood as a progressive *enrichment* of the distributional hypothesis itself:

1. **Static embeddings**: Mikolov et al.'s [-@mikolov2013efficient] Word2Vec (skip-gram and CBOW architectures) demonstrated that prediction-based training on local context windows produces word vectors exhibiting striking algebraic regularity—the famous "king $-$ man $+$ woman $\approx$ queen" analogy. Pennington et al.'s [-@pennington2014glove] GloVe incorporated global co-occurrence statistics via log-bilinear regression, yielding vectors whose inner products approximate pointwise mutual information. Both models instantiate the distributional hypothesis in its classical Firthian form: meaning is determined by context of use, encoded as geometric position in a learned vector space.

2. **Contextual embeddings**: BERT [@devlin2019bert] and GPT [@radford2018improving] move beyond static type-level representations to *token-level* contextualized embeddings, where the same word receives different vectors in different contexts. In the terms of the formal/distributional dichotomy, this is a critical advance: contextualized embeddings partially capture *compositional* structure by conditioning word representations on their full sentential environment, resolving polysemy and constructional effects that static embeddings conflate.

3. **Transformer architecture**: The transformer [@vaswani2017attention] implements distributional composition through multi-head self-attention, where each attention head computes a weighted combination of input token representations. The attention weights $\alpha_{ij} = \text{softmax}(Q_i K_j^T / \sqrt{d_k})$ are analogous to the enriched hom-values of \autoref{sec:enriched-categories}: they encode the *degree of contextual relevance* between tokens $i$ and $j$ in a given representational subspace—a graded, learned distributional relation.

The connection to our categorical framework is direct: **DisCoCat is the algebraic formalization of what LLMs do empirically.** Where a transformer computes sentence representations by attending to syntactically and semantically relevant tokens through learned weight matrices, DisCoCat composes word vectors through type-logical derivations in a compact closed category. The functor $F: \mathbf{Preg} \to \mathbf{FVect}$ that defines DisCoCat is, in this light, the *principled version* of the composition that attention mechanisms learn from data. This perspective is confirmed by Gavranović's [-@gavranovic2024thesis] categorical deep learning programme, which shows that attention heads can be understood as parameterized optics—categorical constructions that compose functorially, just as DisCoCat derivations do.

For case theory specifically, the transformer analogy is illuminating: each attention head in a transformer can be understood as learning a particular *relational role*—attending to subjects, objects, modifiers, or other grammatical functions. This is precisely the role that case marking plays in natural language: structuring who-does-what-to-whom. The case-typed noun spaces of our enriched DisCoCat model ($N_{\text{NOM}}, N_{\text{ACC}}, N_{\text{DAT}}, \ldots$) correspond to the role-specific representational subspaces that different attention heads learn to inhabit.

## The DisCoCat Compositional Framework

### The Key Insight: Shared Compact Closed Structure

DisCoCat's central observation is that pregroup grammars and vector spaces share a common abstract structure: both are **compact closed categories**. This means there exists a *meaning functor*:

$$F: \mathbf{Preg} \to \mathbf{FVect} $$ {#eq:eq-4-1}

from the pregroup grammar category (where objects are types and morphisms are grammatical reductions) to the category of finite-dimensional vector spaces (where objects are vector spaces and morphisms are linear maps).

Under this functor:

- Noun types $n$ map to a vector space $N$ (the noun space)
- Sentence types $s$ map to a vector space $S$ (the sentence space)
- A transitive verb of type $n^r \cdot s \cdot n^l$ maps to a tensor in $N \otimes S \otimes N$
- Pregroup contractions (cups/caps) map to the standard inner product and its dual

### Computing Compositional Sentence Meaning

The compositional meaning of a sentence is computed by tensoring the word meanings and then contracting the result along the indices determined by the syntactic derivation. For "Alice chases Bob":

$$\overrightarrow{\text{Alice chases Bob}} = (\overrightarrow{\text{Alice}} \otimes \overleftrightarrow{\text{chases}} \otimes \overrightarrow{\text{Bob}}) \circ (\varepsilon_N \otimes 1_S \otimes \varepsilon_N) $$ {#eq:eq-4-2}

where $\varepsilon_N: N \otimes N \to \mathbb{R}$ is the compact closure map (inner product). This computation has a direct diagrammatic representation as a string diagram—the same Joyal–Street [@joyalstreet1991geometry] formalism that governs the syntax.

### Empirical Validation and Disambiguation

Grefenstette and Sadrzadeh [-@grefenstette2015concrete] demonstrated that DisCoCat models can outperform purely distributional baselines on disambiguation and sentence similarity tasks. The key advantage is that compositional structure resolves ambiguities that bag-of-words models cannot: "dog bites man" and "man bites dog" receive different sentence vectors because the syntactic structure assigns different roles to the nouns.

**Attention as Cup contraction.** The claim that DisCoCat provides the "algebraic formalization" of transformer-based LLMs can be made precise. In a transformer's self-attention mechanism, the query–key inner product $\text{softmax}(QK^\top / \sqrt{d})V$ selects which word vectors interact—effectively implementing a *soft* version of the Cup contraction. The pregroup Cup $\varepsilon: n^r \otimes n \to I$ contracts two noun wires into a scalar; the attention inner product $q_i \cdot k_j$ contracts two contextualized vectors into an attention weight, which then mixes the value vectors. The difference is that the DisCoCat Cup is *binary* (either the types match or they don't) while the attention Cup is *graded* (producing a real-valued weight). This is precisely the $[0,1]$-enrichment of \autoref{sec:enriched-categories} applied to the type-reduction level: each attention head learns an enriched Cup that contracts types with learned confidence weights rather than categorical yes/no type-matching. Multi-head attention then corresponds to the tensor product of $h$ independent enriched contraction maps, each attending to a different substring of the relational structure—analogous to how DisCoCat composes multiple Cup contractions for multi-argument verbs.

![The compositional semantics of "Alice chases Bob" under the DisCoCat meaning functor $F: \mathbf{Preg} \to \mathbf{FVect}$. The syntactic diagram (left of the functor) assigns pregroup types---$n$ for nouns, $n^r \otimes s \otimes n^l$ for the transitive verb---while $F$ maps these to vector spaces: $n \mapsto N$ (noun space), $s \mapsto S$ (sentence space), and the verb's type to a tensor $\overleftrightarrow{\text{chases}} \in N \otimes S \otimes N$. The Cup contractions become inner products $\varepsilon_N: N \otimes N \to \mathbb{R}$, computing the sentence vector $\overrightarrow{\text{Alice chases Bob}} \in S$ by contracting the word tensors along syntactically determined indices.](output/figures/discopy_composition.png){#fig:discopy-discocat}

## Case Enrichment in the DisCoCat Framework

The present contribution lies in showing how case marking enriches the DisCoCat framework with explicit role structure. In a case-marked DisCoCat model:

1. **Typed noun spaces**: Instead of a single noun space $N$, we define case-specific spaces $N_{\text{NOM}}, N_{\text{ACC}}, N_{\text{DAT}}, \ldots$ Morphisms between these spaces encode case-changing operations (passivization, dative shift, etc.).

2. **Case-constrained composition**: The meaning functor $F$ maps case-typed pregroup derivations to tensor contractions that respect case constraints. A verb seeking a nominative subject and accusative object contracts only with vectors from the appropriate spaces.

3. **Alignment as Natural Transformation**: Cross-linguistic alignment differences correspond to different meaning functors. However, we go further by modeling case alignment as **natural transformations** between functors. An accusative-language transformation $\eta_{\text{acc}}: \mathcal{I} \to F_{\text{acc}}$ identifies S and A arguments; an ergative transformation $\eta_{\text{erg}}$ identifies S and P. This categorification allows us to model "grammar" as the requirement that these transformations commute with the DisCoCirc entity wires, ensuring role persistence across sentences.

![A 20-word DisCoPy pregroup grammar. This diagrammatic transparency exemplifies Shimojima's [-@shimojima1996reasoning] free-ride inference: by inspecting the diagram, one can immediately see that passivization preserves the verb's inherent argument structure while rearranging the surface realization—a fact that requires multiple inference steps to establish in a linear notation. Three dense noun phrases (with 4, 4, and 8 chained adjective modifiers respectively) reduce into the ditransitive verb's type $n^r \otimes s \otimes n^l \otimes n^l$ via 4 Cup contractions, mapping 20 lexical items into the unified sentence type $s$. The resulting complexity score ([@eq:eq-4-4] in \autoref{sec:compact-closure-discourse}) substantially exceeds that of simple transitive sentences, confirming the monotonic relationship between argument structure and derivational depth.](output/figures/discopy_ditransitive.png){#fig:discopy-ditransitive}

The following sections extend this model to discourse and quantum computation.



```{=latex}
\newpage
```



# Discourse Circuits: Entity Persistence and DisCoCirc {#sec:discocirc}

## The Compact Closure Axiom and Diagrammatic Complexity Metrics

### The Snake Equation (Zigzag Identity)

The algebraic engine of DisCoCat is the **compact closure** of the pregroup category: for every type $n$, the adjunction maps $\eta_n: 1 \to n \otimes n^r$ (cap) and $\varepsilon_n: n^r \otimes n \to 1$ (cup) satisfy the **snake equation** (also called the zigzag identity):

$$(\varepsilon_n \otimes 1_n) \circ (1_n \otimes \eta_n) = 1_n $$ {#eq:eq-4-3}

In string-diagrammatic terms, a cup composed with a cap on adjacent wires "straightens out" into an identity wire—a zigzag that cancels into a straight line. This axiom is not merely a formal curiosity: it is the *engine* that makes pregroup type reductions work. Every grammatical contraction (noun canceling with verb argument) is an instance of the cup map $\varepsilon$, and every expansion (introducing an adjoint pair) is an instance of the cap map $\eta$. The snake equation guarantees that these contractions and expansions are well-behaved—they can be freely inserted and removed without changing the meaning of the derivation.

The cognitive significance of the snake equation is that it provides a *visual proof* of coherence: an agent inspecting a string diagram can verify that the derivation is well-formed by checking that all zigzags cancel—a spatial operation that requires no algebraic computation. This is precisely Shimojima's [-@shimojima1996reasoning] "free ride" in its purest form.

![The compact closure axiom ([@eq:eq-4-3]) rendered by DisCoPy as the snake equation: the left panel shows the zigzag diagram $(\varepsilon_n \otimes 1_n) \circ (1_n \otimes \eta_n)$ where a Cup contraction $\varepsilon$ composed with a Cap expansion $\eta$ on adjacent wires forms a snake; the right panel shows the identity wire $1_n$ it equals. This identity---verified computationally via `diagram.normal_form() == Id(Ty('x'))`---is the algebraic engine powering every pregroup type reduction in \autoref{sec:categorial-grammar}: each grammatical contraction (noun canceling with verb argument) is an instance of $\varepsilon$, and the snake equation guarantees that insertions and removals of cup-cap pairs leave derivations invariant.](output/figures/discopy_snake.png){#fig:discopy-snake}

### Diagram Complexity Metrics: Normal Form and Depth

The algebraic properties of pregroup diagrams support quantitative analysis of derivational complexity. Our `complexity_metrics` module implements four complementary measures using the DisCoPy library:

1. **Box count**: The number of lexical entries (Word boxes) in the diagram, corresponding to the sentence's word count from the type-logical perspective. A transitive sentence has 3 boxes (subject, verb, object); a ditransitive sentence has 4 or more.

2. **Cup/Cap count**: The number of contraction and expansion operations. Cups ($\varepsilon$) count argument consumption; caps ($\eta$) count argument introduction. The cup count directly reflects verb valency: an intransitive verb requires 1 cup, a transitive verb 2, and a ditransitive verb 3.

3. **Normal form**: A diagram is in *normal form* if no further simplifications (zigzag cancellations, box reordering) are possible. The `normal_form()` operation computes this canonical representative of the diagram's equivalence class. Normal form preservation under algebraic manipulation provides a correctness check for compositional operations.

4. **Syntactic complexity score**: A composite metric defined as:

$$\text{complexity}(D) = w_b \cdot |D|_{\text{box}} + w_c \cdot |D|_{\text{cup}} + w_d \cdot \text{depth}(D) $$ {#eq:eq-4-4}

where $|D|_{\text{box}}$, $|D|_{\text{cup}}$, and $\text{depth}(D)$ are the box count, cup count, and depth respectively, and $w_b, w_c, w_d$ are configurable weights (defaulting to equal weights). The *depth* of a diagram is the length of the longest path from input to output, counting boxes. Deeper diagrams encode more complex syntactic derivations—a ditransitive sentence like "Alice gave Bob a book" (depth 7) is structurally more complex than a simple intransitive "Alice runs" (depth 3).

The `compare_diagrams()` function applies these metrics across a collection of diagrams, producing tabular comparisons suitable for cross-linguistic analysis. \autoref{fig:complexity-comparison} visualizes these metrics across sentence types of increasing valency, demonstrating the monotonic relationship between argument structure and derivational complexity.

![Complexity metrics ([@eq:eq-4-4]) across six sentence types of increasing valency. **Intransitive** ("Alice runs"): 2 boxes, 1 cup. **Transitive** ("Alice chases Bob"): 3 boxes, 2 cups. **Ditransitive** ("Alice gave Bob book"): 4+ boxes, 3 cups. **Adj Transitive** ("fast Alice chases Bob"): 4 boxes, 3 cups. **Adv Transitive** ("Alice chases Bob today"): 4 boxes, 3 cups. **Complex** ("fast Alice chases Bob today"): 5 boxes, 4 cups. The monotonic increase in cup count $|D|_{\text{cup}}$ with verb valency and adjuncts confirms the formal prediction that argument-structure complexity maps directly onto diagram topology. The actual sentences are overlaid explicitly in the plot for clarity. Cup count thus provides a valency-theoretic invariant computable from the DisCoPy diagram via `len([b for b in diagram.boxes if isinstance(b, Cup)])`.](output/figures/complexity_comparison.png){#fig:complexity-comparison}

These metrics connect to the enriched framework of \autoref{sec:enriched-categories}: the depth of a DisCoCat derivation diagram can serve as a proxy for the syntactic complexity component of the enriched hom-value, providing a principled bridge between the type-logical and distributional perspectives on linguistic structure.

## Extensions: From Sentence Meaning to Discourse Coherence

### DisCoCirc: Distributional Compositional Circuits

The original DisCoCat framework operates at the sentence level: each sentence receives a vector meaning, but there is no mechanism for tracking how meanings interact across sentences. De Felice and Coecke [-@defelice2020discourse] address this with **DisCoCirc** (Distributional Compositional Circuits), which extends the categorical framework to handle discourse-level semantic structure.

DisCoCirc introduces *state wires* that persist across sentence boundaries, encoding the evolving states of discourse entities (characters, objects, topics). A sentence like "Alice chased Bob. He was terrified." is represented as a circuit where:

- Alice and Bob are wires that persist across both sentences
- The pronoun "He" is resolved by connecting its wire to Bob's wire
- The emotional state "terrified" updates the state information carried by Bob's wire

De Felice et al. [-@defelice2022discocirc] further develop this into a full-fledged circuit model that handles ambiguity, coreference, and discourse coherence within the same categorical formalism. A CCG-based pipeline for generating discourse circuits from syntactic parse trees has recently demonstrated that DisCoCirc can scale to real-world text, dynamically composing sentence-level diagrams along shared entity wires via an iterative process of coreference resolution and wire merging [-@duneau2021parsing]. Complementary work on **DiscoSG** (Discourse Scene Graphs) extends this approach to multi-sentence image captions, parsing text into scene graphs that capture cross-sentence coreference relations. \autoref{fig:discourse} illustrates a multi-sentence discourse diagram where entity wires persist across sentence boundaries. For case theory, DisCoCirc is significant because it shows how case-marked argument structure *composes across discourse*: the nominative subject of one sentence can become the accusative object of the next, and this transformation is tracked as a morphism in the discourse category.

![A DisCoCirc-style discourse diagram for the two-sentence discourse "Alice chases Bob. Bob runs." generated via DisCoPy's pregroup grammar. **Sentence 1**: three Word boxes contract Alice ($n$) and Bob ($n$) into the transitive verb "chases" ($n^r \otimes s \otimes n^l$), producing sentence type $s$. **Sentence 2**: Bob ($n$) contracts into the intransitive "runs" ($n^r \otimes s$), producing a second $s$. The full discourse type is the tensor product $s \otimes s$, encoding inter-sentential coherence through parallel compositional structure. In a full DisCoCirc implementation, the shared entity wire for Bob would carry accumulated semantic state across the sentence boundary---the foundation for case role tracking in \autoref{fig:three-sentence-discourse}.](output/figures/discopy_discocirc_discourse.png){#fig:discourse}

### Case Role Reversal Across Discourse Boundaries

The power of DisCoCirc for case theory becomes particularly vivid in multi-sentence discourses where the *same entity occupies different case roles* across sentences. Consider the three-sentence discourse:

> *"Alice chases Bob. Bob fears Alice. She smiles."*

In this discourse, Alice undergoes a complete cycle of case role reversals:

1. **Sentence 1**: Alice is $\text{NOM}$ (Proto-Agent, the one chasing) and Bob is $\text{ACC}$ (Proto-Patient, the one chased).
2. **Sentence 2**: Bob is now $\text{NOM}$ (the one fearing) and Alice is $\text{ACC}$ (the one feared)—a role reversal where Alice moves from agent to patient.
3. **Sentence 3**: "She" resolves anaphorically to Alice, who returns to $\text{NOM}$ as the agent of smiling.

This NOM → ACC → NOM trajectory for Alice across three sentences is precisely the kind of *dynamic case assignment* that static single-sentence analyses cannot capture. The categorical representation as a triple tensor product $s \otimes s \otimes s$ (\autoref{fig:three-sentence-discourse}) encodes each sentence as an independent pregroup derivation while preserving the entity identity that links them. In a full DisCoCirc implementation, Alice's entity wire would carry accumulated semantic state—the meaning of "She" in sentence 3 inherits the enriched state of an Alice who has first chased and then been feared, not merely the bare lexical entry for "Alice."

![Three-sentence discourse diagram for "Alice chases Bob. Bob fears Alice. She smiles." rendered using DisCoPy, demonstrating dynamic case role reversal. **Sentence 1**: Alice is NOM (Proto-Agent), Bob is ACC (Proto-Patient). **Sentence 2**: Bob is NOM, Alice is ACC---a complete agent--patient role reversal. **Sentence 3**: the anaphoric pronoun "She" resolves to Alice, who returns to NOM. Alice's case trajectory NOM$\to$ACC$\to$NOM across three sentences is tracked by the triple tensor product $s \otimes s \otimes s$. In a full DisCoCirc implementation, Alice's entity wire would carry accumulated semantic state---the meaning of "She" in sentence 3 inherits the enriched state of an Alice who has first chased and then been feared, not merely the bare lexical entry for "Alice." This dynamic case assignment across discourse boundaries is precisely what lambeq Gen II [@lambeq2025genii] can compile into parameterized quantum circuits.](output/figures/discopy_three_sentence_discourse.png){#fig:three-sentence-discourse}

### Quantum NLP and the lambeq Pipeline

The categorical structure of DisCoCat maps naturally onto quantum circuits: the tensor product structure of $\mathbf{FVect}$ is identical to the tensor product structure of $\mathbf{Qubit}$, the category of qubit systems. This observation underlies the **QNLP** (Quantum Natural Language Processing) program [@meichanetzidis2020qnlp], which implements DisCoCat models as parameterized quantum circuits.

The **lambeq** library [@lorenz2023lambeq] provides a practical pipeline:

1. Parse a sentence into a pregroup derivation (via the neural CCG parser Bobcat or rule-based parsers)
2. Convert the derivation into a string diagram
3. Translate the diagram into a parameterized quantum circuit (or a classical tensor network)
4. Train the parameters on NLP tasks (classification, similarity, question answering)

Kartsaklis et al. [-@kartsaklis2021functorial] demonstrate that this pipeline achieves competitive performance on question-answering tasks, confirming that the categorical structure captures genuine linguistic regularities even when instantiated on noisy near-term quantum hardware.

**lambeq Gen II** (released May 2025) marks a significant advance by incorporating full **DisCoCirc** support as its core mathematical foundation, enabling the framework to scale beyond single-sentence semantics to discourse-level NLP [@lambeq2025genii]. With over 50,000 downloads, lambeq Gen II achieves language neutrality, improved trainability, and compositional interpretability for explainable AI on quantum hardware. DisCoCirc's state wires—which track entity persistence across sentence boundaries—can now be automatically compiled into parameterized quantum circuits, closing the gap between sentence-level DisCoCat and discourse-level case role tracking. This is directly relevant to the case role reversal phenomena discussed in \autoref{fig:three-sentence-discourse}: lambeq Gen II can, in principle, compile such multi-sentence case-dynamic discourses into trainable quantum circuits.

Recent work on quantum-cognitive frameworks integrates DisCoCat and DisCoCirc with density matrices for modeling dynamic meaning in text, treating semantic states as mixed quantum states that evolve through discourse—providing an alternative to pure-state vector models that naturally accommodates ambiguity and partial information [-@quantumcognitive2026frontiers].

Recent work on **string diagram rewriting** by Bonchi et al. [-@bonchi2022rewriting] provides the theoretical foundation for diagram simplification, showing that string diagram rewrite systems modulo Frobenius structure can be interpreted as double-pushout hypergraph rewriting—ensuring that the algebraic simplifications applied during normal form computation are provably sound. De Huybrecht [-@dehuybrecht2024subcategorizing] extends DisCoCat with *subcategorization* for light verb constructions, demonstrating that the categorical framework accommodates sublexical compositional structure—a development that connects naturally to the monadic root syntax of Song [-@song2022act] discussed in \autoref{sec:categorial-grammar}.

For our case-theoretic framework, QNLP offers a concrete computational substrate: case categories could be implemented as quantum circuits where case roles correspond to quantum registers and grammatical relations correspond to parameterized gates. This connection between linguistic case structure and quantum information processing—mediated entirely by the shared categorical formalism—illustrates the power of the diagrammatic approach.

```{=latex}
\newpage
```



```{=latex}
\newpage
```


# Enriched Categories: Magnitude and Quantitative Grading {#sec:enriched-categories}

## Beyond Discrete Categories: Quantitative Grading

The categories introduced in \autoref{sec:case-systems}—with case roles as objects and grammatical relations as morphisms—capture the *qualitative* structure of case systems: which roles exist and how they connect. But linguistic data is fundamentally *quantitative*: some grammatical relations are more probable than others, some role assignments are stronger than others, and distributional similarity is a matter of degree.

To accommodate this quantitative dimension, we move from ordinary categories to **enriched categories**, where hom-sets are not just sets of morphisms but carry additional algebraic structure. The framework of Bradley et al. [-@fritz2021enriched] provides the key construction.

## The $[0,1]$-Enrichment of Case Categories

### Definition

A category $\mathcal{C}$ enriched over the unit interval $([0,1], \cdot, 1)$ assigns to every pair of objects $A, B$ a *hom-value* $\mathcal{C}(A, B) \in [0,1]$ satisfying:

$$\mathcal{C}(A, A) = 1 \quad \text{(Identity)} $$ {#eq:eq-5-1}

$$\mathcal{C}(A, C) \geq \mathcal{C}(A, B) \cdot \mathcal{C}(B, C) \quad \text{(Composition)} $$ {#eq:eq-5-2}

The identity axiom says that every expression is maximally related to itself. The composition inequality says that distributional relatedness composes sub-multiplicatively: if $A$ is 80% related to $B$ and $B$ is 70% related to $C$, then $A$ must be at least $0.8 \times 0.7 = 56\%$ related to $C$.

### Interpreting Hom-Values in Linguistic Context

Bradley et al. [-@fritz2021enriched] interpret hom-values as *conditional probabilities* in a distributional model: $\mathcal{C}(A, B) = P(\text{context} \mid A \text{ and } B \text{ co-occur})$. In our case-theoretic application, we interpret them more broadly:

| Hom-value interpretation | Domain | Example |
| :--- | :--- | :--- |
| Conditional probability | Corpus statistics | P(ACC role \| transitive verb context) |
| Proto-role strength | Semantic typology | Degree of Proto-Agent satisfaction |
| Distributional similarity | Vector semantics | Cosine similarity of case-role embeddings |
| Morphological predictability | Morpholexicology | Reliability of case-marking paradigm |

### Implementation via the EnrichedCategory Class

Our `EnrichedCategory` class implements this structure directly. The constructor takes a list of `CaseRole` objects and a NumPy proximity matrix encoding hom-values:

```python
from src.enriched import EnrichedCategory
from src.case_category import CaseRole
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

![Case role distributional relation graph visualizing the enriched hom-values $\mathcal{C}(A,B) \in [0,1]$ among all eight case roles. Strong relations (high distributional co-occurrence, solid edges) cluster into two groups: the **core argument complex** (NOM--ACC--DAT, linked by transitive and transfer morphisms) and the **peripheral complex** (LOC--INS--ABL, linked by spatial and instrumental relations). GEN bridges both clusters via possessive modification. Weak relations (dashed edges) connect VOC to the network---its peripheral isolation reflects the pragmatic rather than syntactic function of direct address. The edge weights in this graph are the hom-values from which the $3 \times 3$ similarity matrix $Z$ ([@eq:eq-5-4]) and categorical magnitude of \autoref{sec:enriched-categories} are computed.](output/figures/enriched_hom_matrix.png){#fig:enriched-heatmap}

## Categorical Magnitude as a Complexity Invariant

A key invariant of enriched categories is their **magnitude**—a numerical quantity that captures the "effective size" of the category, discounting for overlap between objects.

For an enriched category with $n$ objects, let $Z$ be the $n \times n$ matrix with $Z_{ij} = \mathcal{C}(i, j)$. The magnitude is:

$$|\mathcal{C}| = \sum_{i,j} (Z^{-1})_{ij} $$ {#eq:eq-5-3}

when $Z$ is invertible. Magnitude has deep connections to information theory:

- For a *discrete* category (no non-trivial relationships), $|\mathcal{C}| = n$ (the number of objects)
- For a highly connected category, $|\mathcal{C}| < n$ (objects are "redundant")
- Magnitude connects to the diversity measures studied in ecology (species diversity), graph theory (effective graph resistance), and information geometry (Fisher information)

**Worked example.** Consider the minimal 3-case category with objects $\{S, A, P\}$ and hom-values $\mathcal{C}(S,A) = 0.85$ (S and A share agentive contexts), $\mathcal{C}(A,P) = 0.70$ (transitive co-occurrence), $\mathcal{C}(S,P) = 0.40$ (weak S–P overlap). The similarity matrix $Z$ is:

$$Z = \begin{pmatrix} 1.00 & 0.85 & 0.40 \\ 0.85 & 1.00 & 0.70 \\ 0.40 & 0.70 & 1.00 \end{pmatrix}, \quad Z^{-1} \approx \begin{pmatrix} 2.45 & -1.35 & 0.55 \\ -1.35 & 3.00 & -1.80 \\ 0.55 & -1.80 & 2.65 \end{pmatrix} $$ {#eq:eq-5-4}

The magnitude is $|\mathcal{C}| = \sum_{i,j} (Z^{-1})_{ij} \approx 2.45 - 1.35 + 0.55 - 1.35 + 3.00 - 1.80 + 0.55 - 1.80 + 2.65 \approx 2.90$---less than the cardinality 3 of the role inventory. The deficit $3 - 2.90 = 0.10$ is small because these three core arguments are relatively independent (the S–P overlap of 0.40 is the main source of redundancy). By contrast, an accusative alignment—which merges S and A into a single NOM role—would yield a 2-object category with magnitude exactly 2.0, and the deficit $3 - 2.0 = 1.0$ quantifies the information lost by neutralization.

**Scaling to full categories.** Our `EnrichedCategory` implementation computes magnitude for any case category. For the standard 8-case English category with empirically calibrated distributional proximity values, the magnitude is approximately 5.2—the deficit $8 - 5.2 = 2.8$ reflects distributional overlap: NOM and ACC share transitive contexts, DAT and ACC overlap in double-object constructions, and the peripheral cases (VOC, ABL) are relatively independent. This magnitude differential provides a quantitative formalization of Silverstein's [-@silverstein1976hierarchy] case hierarchy: languages with more alignment-based neutralization (lower magnitude) have less relational discriminability, while richer case inventories (higher magnitude) make finer-grained relational distinctions.

Bradley [-@bradley2020entropy] establishes a foundational link between categorical magnitude and information entropy through topological operad derivations. Her result shows that Shannon entropy can be characterized as the unique derivation of a certain topological operad—a categorical structure that also governs the composition of enriched categories. This provides a deep theoretical justification for using magnitude as a measure of linguistic complexity: the magnitude of a case category quantifies how much "information" the case system encodes about relational structure.

Leinster and Shulman [-@leinster2021magnitude] further develop **magnitude homology**, which categorifies magnitude from a scalar invariant to a graded homological invariant—detecting not just the "effective number" of objects but the higher-dimensional "holes" in the distributional landscape. For case categories, magnitude homology can distinguish between two systems with the same magnitude but different topological structure: a category where NOM–ACC–DAT form a tight cluster and all other cases are isolated looks identical in magnitude to one where the clustering is evenly distributed, but their magnitude homology groups differ, revealing that the former has a 1-dimensional "hole" (a missing transitive link) that the latter fills. This finer invariant provides a richer classification of case systems than magnitude alone.

## Enriched Functors, Bradley's Language-as-Category Model, and the LLM Connection

Bradley's [-@bradley2024ipam; -@bradley2025tea] broader program treats natural language itself as an enriched category, where:

- **Objects** are expressions (words, phrases, sentences)
- **Hom-values** encode distributional co-occurrence probabilities
- **Composition** models transitivity of distributional relatedness

This "language as enriched category" perspective has profound implications for case theory:

1. **Case roles emerge from distributional structure**: Rather than being imposed a priori, case distinctions arise from clusters of high hom-values in the enriched language category. Nouns that frequently appear in agent contexts cluster together, forming the "nominative" region of the category.

2. **Alignment types correspond to enriched structure**: Different languages partition the enriched category differently, and these partitions correspond to the alignment types (accusative, ergative, etc.) discussed in \autoref{sec:case-systems}.

3. **Language models are enriched functors**: A neural language model (such as a transformer) can be viewed as an enriched functor from the syntactic category to the semantic category, mapping type-logical derivations to distributional meaning representations while preserving the enriched structure.

The deep connection to modern distributional semantics is this: the static word embeddings of Word2Vec [@mikolov2013efficient] and GloVe [@pennington2014glove] operationalize the enriched hom-values as *cosine similarities* in a learned vector space—$\mathcal{C}(A, B) = \cos(\vec{v}_A, \vec{v}_B)$—while contextualized embeddings from transformers [@devlin2019bert; @vaswani2017attention] compute *dynamic* hom-values that depend on the sentential context. In the enriched-categorical framework, this transition from static to contextualized embeddings corresponds to moving from a *fixed* enriched category (where hom-values are precomputed from corpus statistics) to a *parameterized* enriched category (where hom-values are computed on-the-fly by attention mechanisms). Transformer attention weights $\alpha_{ij}$ are precisely such context-dependent enriched hom-values: they encode how "related" token $i$ is to token $j$ in a given representational layer, satisfying a softmax normalization that parallels the probabilistic interpretation of Bradley et al.'s [-@fritz2021enriched] hom-values as conditional probabilities.

## Connection to Lawvere's Metric Spaces and Generalized Logic

The $[0,1]$-enrichment connects to a deep tradition in categorical algebra. Lawvere showed that metric spaces are categories enriched over $([0, \infty], +, 0)$: the hom-value is the distance between points, the identity axiom says $d(x, x) = 0$, and the composition inequality is the triangle inequality $d(x, z) \leq d(x, y) + d(y, z)$. Our $[0,1]$-enrichment is the multiplicative analogue: hom-values are *similarities* rather than distances, and the composition inequality is sub-multiplicative rather than sub-additive.

This Lawvere-style perspective unifies our case categories with the geometry of distributional semantics: case roles are points in a "similarity space," and morphisms between them are paths weighted by distributional proximity. The magnitude of this space then quantifies the "effective dimensionality" of the case system—how many independent relational distinctions the language makes.



```{=latex}
\newpage
```



# Topos Theory: Classifying Spaces and Morita Equivalence {#sec:topos-theory}

## From Categories to Toposes: The Translation Problem

The preceding sections have shown how case systems, categorial grammars, distributional semantics, and enriched categories each provide a different "window" onto the same underlying linguistic phenomenon. But how do we know that results proved in one framework transfer to another? This is the problem of *inter-theoretic translation*—and it is precisely the problem that Caramello's [-@caramello2016bridges] topos-theoretic bridge technique was designed to solve.

## Classifying Toposes and Morita Equivalence

### What Is a Topos? Generalized Universes of Sets

A **topos** is a category that behaves like a generalized universe of sets: it has products, exponentials, a subobject classifier (playing the role of a "truth-value object"), and enough structure to interpret first-order logic internally. The category **Set** of ordinary sets is a topos, but there are many others—presheaf categories, sheaf categories over topological spaces, and the categories of models of geometric theories.

### Classifying Toposes of Geometric Theories

Every *geometric theory* $\mathbb{T}$ (a theory axiomatized by sequents involving only finite conjunctions, arbitrary disjunctions, and existential quantification) has a **classifying topos** $\mathcal{E}_\mathbb{T}$—a canonical topos whose models correspond exactly to the geometric functors from $\mathcal{E}_\mathbb{T}$ to other toposes. The classifying topos encodes the theory's "logical shape" independently of any particular model.

Caramello's key insight [-@caramello2016bridges; -@caramello2021five] is that different theories can share the same classifying topos up to equivalence—an equivalence known as **Morita equivalence**. When two theories $\mathbb{T}_1$ and $\mathbb{T}_2$ are Morita equivalent ($\mathcal{E}_{\mathbb{T}_1} \simeq \mathcal{E}_{\mathbb{T}_2}$), any property that can be expressed as an invariant of the classifying topos transfers automatically between them.

## Bridge Theorems for the Four Case Theories

### Formalizing Case Theories as Geometric Theories

We formalize each case-theoretic framework as a geometric theory:

1. **Typological case theory** $\mathbb{T}_{\text{typ}}$: Objects are case roles, morphisms are grammatical relations, axioms specify alignment constraints (e.g., "S = A" in accusative alignment).

2. **Type-logical case theory** $\mathbb{T}_{\text{log}}$: Objects are syntactic types, morphisms are Lambek calculus derivations, axioms specify well-formedness conditions (pregroup contractions).

3. **Distributional case theory** $\mathbb{T}_{\text{dist}}$: Objects are vector spaces, morphisms are linear maps, axioms specify the composition law for distributional meaning (DisCoCat).

4. **Enriched case theory** $\mathbb{T}_{\text{enr}}$: Objects are expressions, morphisms carry $[0,1]$-valued weights, axioms specify the identity and composition inequalities.

### The Bridge Theorem: Morita Equivalence Chain

The central claim is that these four theories are related by a chain of Morita equivalences:

$$\mathcal{E}_{\mathbb{T}_{\text{typ}}} \leftarrow \mathcal{E}_{\mathbb{T}_{\text{bridge}}} \rightarrow \mathcal{E}_{\mathbb{T}_{\text{log}}} \leftarrow \mathcal{E}_{\mathbb{T}_{\text{bridge}'}} \rightarrow \mathcal{E}_{\mathbb{T}_{\text{dist}}} $$ {#eq:eq-6-1}

where the intermediate toposes are constructed by finding geometric theories that are simultaneously interpretable in both flanking frameworks. The Morita equivalence ensures that:

- **Syntactic theorems port to semantics**: A commutativity result proved in the type-logical framework automatically yields a compositionality result in the distributional framework.
- **Typological universals constrain distributional models**: Alignment types (accusative, ergative) impose structural constraints on the vector spaces used in DisCoCat.
- **Enriched structure enriches all frameworks**: The $[0,1]$-valued weights from the enriched theory can be pulled back to give probabilistic interpretations of typological, logical, and distributional constructions.

\autoref{fig:functor-alignment} visualizes the alignment functor between the Accusative and Ergative category instantiations, showing how the same eight case roles are connected by different morphism structures under different alignment types.

![The alignment functor $F\colon\mathcal{C}_{\text{acc}} \to \mathcal{C}_{\text{erg}}$ mapping the Accusative case category (source, blue panel) to the Ergative case category (target, amber panel). All eight case roles appear in both categories; purple horizontal arrows show the functor's object-level mapping $F(\text{role})$. The key structural difference is in the **morphism grouping**: the Accusative category groups $\{S, A\} \to \text{NOM}$ (kernel $\{(S,A)\}$, cf. [@eq:eq-2-3]), while the Ergative groups $\{S, P\} \to \text{ABS}$ (kernel $\{(S,P)\}$, cf. [@eq:eq-2-4]). The functor preserves the role inventory but restructures the morphism pattern---formalizing the alignment-as-functor principle. This diagram provides one link in the Morita equivalence chain of [@eq:eq-6-1] that enables inter-theoretic bridge transfer.](output/figures/functor_alignment.png){#fig:functor-alignment}

## Phillips and the Universal Language of Thought

Phillips [-@phillips2024lot] provides a striking application of topos-theoretic methods to cognitive science. He shows that the **Language of Thought** (LoT) hypothesis—the claim that cognition operates over structured, combinatorial representations with language-like properties—can be formalized categorically, and that the resulting structure is *universal* in the topos-theoretic sense.

Specifically, Phillips demonstrates that:

1. LoT properties (discrete constituents, role-filler independence, systematicity) arise as **universal constructions** in a topos—categorical products, fiber bundles, and presheaves.

2. Every topos supports an internal first-order logic, explaining how LoT-like logical capacities can emerge in systems (biological or artificial) whose internal architecture forms a topos.

3. The "shape" of cognitive representations is fundamentally **topological**, captured by presheaves and fiber bundles rather than by point-set structures.

For our framework, Phillips's result is significant because it provides a topos-theoretic foundation for the claim that case structure is a universal feature of cognitive architecture. If the Language of Thought is topos-universal, and case categories are definable within any topos (which they are, being small categories with first-order axioms), then every cognitive system with LoT-like structure must be able to represent case distinctions—a strong universality claim that goes beyond mere typological observation.

## Syntactic Learning via Classifying Toposes

Caramello [-@caramello2023syntactic] extends the bridge technique to a learning theory: she shows that classifying toposes can be used to *learn* the theory of a mathematical structure from finite data (a finite set of models). The learning algorithm constructs a classifying topos from the observed data and then extracts the axioms of the underlying theory.

Applied to case systems, this suggests a principled approach to *grammatical induction*: given a corpus annotated with case labels, one could construct the classifying topos of the implicit case theory and read off its axioms—recovering the alignment type, the morphism structure, and the enriched weights from data alone. The procedure operates in four phases:

1. **Extraction**: Parse a Universal Dependencies treebank for a target language, collecting all case-labeled dependency arcs. Each arc $(r_1, \text{rel}, r_2)$ instantiates a morphism $r_1 \to r_2$ in the implicit case category.
2. **Saturation**: Close the extracted morphism set under composition, identity, and the enriched weight constraints of \autoref{sec:enriched-categories}. Compute the empirical hom-values as normalized co-occurrence frequencies.
3. **Classification**: Construct the classifying topos $\mathcal{E}_\mathbb{T}$ from the saturated theory—the canonical topos whose models are exactly the case-assignment patterns attested in the corpus. The topos-theoretic invariants (sort count, arity distribution, axiom count) combined with the magnitude and magnitude homology invariants of the enriched theory (\autoref{sec:enriched-categories}) provide a multi-dimensional fingerprint of the language's case system.
4. **Identification**: Compare the fingerprint against the Morita equivalence classes of known alignment types. If the classifying topos matches an existing class, the language's alignment type is identified; if not, the procedure has discovered a novel alignment pattern.

This topos-theoretic learning procedure would be provably correct (recovering the true theory in the limit) and maximally general (not presupposing any particular alignment type). The magnitude invariant from \autoref{sec:enriched-categories} enters at step 3 as a scalar summary of the learned category's "effective size," while magnitude homology provides a finer-grained topological signature.

## Diagrammatic Implications of Inter-Theoretic Transfer

The bridge technique has a natural diagrammatic interpretation. Morita equivalence between theories is witnessed by *functorial translations*—diagrams in the 2-category of toposes that commute up to natural isomorphism. These diagrams serve the same cognitive function as the commutative diagrams of \autoref{sec:introduction}: they make the transfer of structure visible, allowing a researcher to verify at a glance that a result proved in one framework genuinely applies in another.

Manders [-@manders2008euclidean] observed that even in classical mathematics, diagrams serve not merely as illustrations but as *inferential instruments* whose spatial properties encode proof-relevant information. The topos-theoretic bridge diagrams extend this observation to the meta-theoretical level: the commutative diagram expressing Morita equivalence is itself a "free ride" inference, automatically transferring any topos-invariant property from one theory to another without requiring a case-by-case verification.

**Concrete bridge transfer.** Consider the *commutativity of transitive composition* proved in $\mathbb{T}_{\text{log}}$ (the type-logical framework): for types $n, s$, the transitive derivation $n \cdot (n^r \cdot s \cdot n^l) \cdot n \to s$ yields the same sentence type regardless of whether contractions proceed left-to-right or right-to-left. Via the Morita equivalence chain, this result transfers to $\mathbb{T}_{\text{dist}}$ as a *composition law*: the sentence vector $\overrightarrow{\text{Alice chases Bob}}$ computed by contracting the subject tensor first (then the object) equals the vector computed by contracting the object first (then the subject)—a non-trivial commutativity property of the DisCoCat tensor contraction that would require a separate linear-algebra proof without the bridge. In $\mathbb{T}_{\text{enr}}$, the same result becomes a *weight invariant*: the enriched hom-value of the composed morphism NOM→ACC is independent of the intermediate case role through which composition factors.

## Computational Implementation of Topos-Theoretic Bridges

The topos-theoretic constructions developed above are not merely abstract formalism—they are computationally implemented in our `topos` module, which provides working Python implementations of geometric theories, classifying toposes, Morita equivalence checking, and bridge transfer.

### Geometric Theories from Case Categories

The `build_typological_theory()` function constructs a geometric theory $\mathbb{T}_{\text{typ}}$ from a `CaseCategory` by extracting:

- **Sorts**: the case roles (objects of the category)
- **Function symbols**: the morphisms with their source/target pairs
- **Axioms**: identity morphism existence, composition closure, and alignment constraints

For the standard 8-case category, this yields a theory with 8 sorts and approximately 15 function symbols. The mineral 3-case category produces a theory with 3 sorts and 5 function symbols. Our `build_enriched_theory()` function further annotates the geometric theory with $[0,1]$-valued hom weights from the enriched structure of \autoref{sec:enriched-categories}.

### Classifying Toposes and Morita Equivalence Verification

The `ClassifyingTopos` class computes topological invariants—number of sorts, function arity distribution, and axiom count—that characterize the "logical shape" of a theory. Two theories are **Morita equivalent** when their classifying toposes share the same invariant profile:

```python
T_std = build_typological_theory(standard_case_category())
T_min = build_typological_theory(minimal_case_category())
equivalent = check_morita_equivalence(T_std, T_min)
# False: 8-sort and 3-sort theories have different invariants
```

The `bridge_transfer()` function implements the transfer mechanism: given two Morita-equivalent theories, it constructs the functorial translation that carries properties (alignment constraints, composition laws) from one to the other. The transfer is blocked when Morita equivalence fails, preventing unsound cross-theoretic reasoning—a computational enforcement of the mathematical constraint.



```{=latex}
\newpage
```


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



```{=latex}
\newpage
```


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



```{=latex}
\newpage
```



# AI Implications: Multi-Agent Protocols and Emergent Alignment {#sec:ai-implications}

## Multi-Agent Communication: Compositional AI Protocols

The categorical framework developed in the preceding sections—case categories, functorial semantics, enriched structure, and diagrammatic reasoning—addresses a core challenge in contemporary artificial intelligence: how to endow autonomous agents with structured, compositional communication.

Current multi-agent AI systems communicate through increasingly standardized protocols. Google's Agent-to-Agent (A2A) protocol [@google2025a2a], introduced in 2025, provides a standard way for agents to communicate regardless of underlying framework through HTTP/JSON-RPC message passing with capability discovery. The Model Context Protocol (MCP) [@anthropic2024mcp] standardizes how AI agents access external tools and data sources. The Agent Communication Protocol (ACP) [@acp2025protocol] handles standardizing messaging formats across various users, including agents, applications, and humans. The Agent Network Protocol (ANP) [@anp2025protocol] introduces a three-layer architecture supporting trusted agent interaction in distributed systems. These engineering advances solve critical interoperability problems but lack a compositional semantics: messages are flat JSON payloads without inherent algebraic structure.

Category theory provides exactly the missing layer. Just as the DisCoCat framework maps grammatical derivations functorially into vector spaces (see \autoref{sec:categorical-semantics}), a categorical communication protocol would map agent interaction patterns functorially into behavioral specifications. The morphisms of such a protocol category would be message types, the objects would be agent states, and the composition law would specify how multi-step interactions chain together—exactly the structure of our case categories, where morphisms represent grammatical relations and composition encodes transitivity.

## Case Roles as Functional Typing for Agent Systems

The eight-case framework of CEREBRUM [@friedman2024cerebrum] maps directly onto the functional roles that components play in multi-agent architectures:

| Case Role | Agent System Analogue | Protocol Function |
| :--- | :--- | :--- |
| NOM (Agent) | Active requester | Initiator of action policies |
| ACC (Patient) | Passive responder | Target of directed operations |
| GEN (Source) | Context provider | Supplier of prior information |
| DAT (Recipient) | Designated receiver | Endpoint for information transfer |
| INS (Instrument) | Tool / API | Means of state transformation |
| LOC (Context) | Environment state | Boundary conditions and Markov blanket |
| ABL (Origin) | Data source | Causal provenance of inputs |
| VOC (Addressee) | Routing target | Pragmatic addressing in broadcast networks |

This mapping is not merely analogical. In the MCP protocol, a tool call has precisely the structure of a case-marked clause: an *agent* (NOM) invokes a *tool* (INS) on a *resource* (ACC) to deliver a *result* to a *recipient* (DAT). The case structure ensures that every interaction is relationally typed, preventing the category errors (sending a response where a tool call is expected) that plague unstructured message-passing systems.

## Categorical Deep Learning: An Algebraic Theory of Architectures

Gavranović [-@gavranovic2024thesis] develops "a novel mathematical foundation for deep learning based on the language of category theory," showing that neural network architectures—feedforward, convolutional, recurrent, attention—can all be subsumed under a single categorical framework using parameterized optics and lenses. This "Categorical Deep Learning" approach [@shiebler2024categorical] demonstrates that categorical structure is "an algebraic theory of all architectures," unifying design patterns that appear unrelated when viewed through conventional linear algebra.

For case theory in AI, this result is significant: it means the same categorical language used to describe linguistic case assignment also describes the internal computation of the neural networks that process language. A transformer's attention mechanism, viewed through Gavranović's lens, performs a kind of *categorical case assignment*—each attention head selects which input tokens play which functional roles in the computation, with attention weights serving as the enriched hom-values of \autoref{sec:enriched-categories}.

The distributional semantics perspective deepens this connection. The transformer architecture [@vaswani2017attention] is, at its mathematical core, a *distributional composition engine*: it takes distributional word representations (embeddings in the Firthian tradition [@firth1957papers]) and composes them into contextual sentence representations through attention-weighted aggregation. This is precisely what the DisCoCat functor $F: \mathbf{Preg} \to \mathbf{FVect}$ does algebraically—compose word vectors according to syntactic structure. The key difference is that DisCoCat derives its composition rules from type-logical grammar, while transformers learn them from data. The convergence is striking: both arrive at tensor-contracted sentence representations, both use multi-linear maps for composition, and both produce vector spaces where similarity encodes semantic relatedness. Large language models such as BERT [@devlin2019bert] and GPT [@radford2018improving] thus serve as massive-scale *empirical validations* of the distributional programme that DisCoCat formalizes categorically.

Recent work on Distributional Active Inference [@akgul2026distributional] extends this parallel into the domain of sequential decision-making: just as LLMs model full contextual distributions over tokens, distributional RL models full return distributions over outcomes—and active inference provides the variational Bayesian bridge between the two (see \autoref{sec:cognitive-integration}). For multi-agent AI systems, this suggests an architecture in which agents maintain *distributional* representations of both semantic content and expected interaction returns, composing them categorically.

## String Diagrams as a Foundation for Interpretable AI

The lambeq library [@lorenz2023lambeq] demonstrates that string diagrams provide a practical interface between linguistic structure and machine learning. As an "efficient high-level Python library for Quantum NLP," lambeq translates sentences into string diagrams, converts diagrams into parameterized circuits (quantum or classical), and trains parameters end-to-end on NLP tasks. The diagrammatic representation serves dual purposes: it is both the mathematical specification of the model *and* a human-readable explanation of what the model computes.

This interpretability property is crucial for AI safety and alignment. Where transformer architectures produce opaque attention patterns, a DisCoCat model deployed via string diagrams produces derivation trees with explicit compositional semantics—every box and wire has a linguistic interpretation. Extending this to agent communication, a categorical protocol would produce not just working message exchanges but *interpretable* interaction diagrams where each step's relational role is transparent.

## DisCoCirc and Multi-Turn Agent Dialogue Protocols

The DisCoCirc framework [@defelice2022discocirc] extends compositional semantics from single sentences to multi-sentence discourse by introducing *state wires* that persist across sentence boundaries. This architecture maps directly onto multi-turn agent dialogues:

- **Entity wires** correspond to persistent agent identities across communication rounds
- **State updates** correspond to belief revisions triggered by incoming messages
- **Coreference resolution** corresponds to entity tracking across protocol sessions
- **Discourse coherence** corresponds to protocol correctness constraints

In a multi-agent system, a DisCoCirc-style protocol would track the evolving states of all participating agents as persistent wires in a circuit diagram, with each message exchange represented as a box that transforms the relevant wires. Protocol correctness reduces to a categorical property: the circuit must type-check, meaning all wire types must match at connection points—precisely the condition that case marking enforces in natural language.

## Compositional Game Theory and Categorical Multi-Agent Equilibria

The "parametrised optics" framework developed within categorical cybernetics "provides a general-purpose foundation for the study of controlled processes" applicable to compositional game theory as a multi-agent framework. In this setting, agents are modeled as lenses (or optics) that observe the environment through one channel and act through another, with the overall system behavior emerging from the composition of individual agent behaviors.

This connects to our enriched case framework (\autoref{sec:enriched-categories}): the precision weights on morphisms correspond to the utility parameters of game-theoretic agents, and the composition inequality $\mathcal{C}(A,C) \geq \mathcal{C}(A,B) \cdot \mathcal{C}(B,C)$ corresponds to the sub-optimality of indirect communication chains. Equilibria in the multi-agent game correspond to fixed points of the enriched functor, where no agent can improve its utility by changing its case-role assignment.

## Double Categorical Systems Theory for Explainable Autonomous AI

Recent work on Double Categorical Systems Theory (DCST) aims to "utilise Double Categorical Systems Theory as a mathematical framework to facilitate collaboration in co-designing an explainable and auditable model of an autonomous AI system's deployment environment." DCST extends ordinary category theory with a second dimension of morphisms (2-morphisms), allowing simultaneous modeling of:

1. **Horizontal composition**: Sequential chaining of agent interactions (morphism composition)
2. **Vertical composition**: Hierarchical nesting of subsystems within larger systems (2-morphism composition)

For case theory, the double-categorical extension allows us to model both the *within-sentence* case structure (horizontal) and the *discourse-level* case structure (vertical) within a single algebraic framework—precisely the unification that DisCoCirc achieves pragmatically.

## Toward Categorical Communication Standards for AI Agents

The synthesis of these developments suggests a research program: developing **categorical communication protocols** that combine the engineering robustness of existing standards (A2A, MCP, ACP) with the compositional semantics of categorical linguistics. Such a protocol would:

1. **Type-check interactions**: Every message exchange would be relationally typed by case roles, preventing structural communication errors at the protocol level
2. **Compose transparently**: Multi-step interactions would compose algebraically, with diagrammatic representations providing interpretable audit trails
3. **Transfer across implementations**: Topos-theoretic bridges (\autoref{sec:topos-theory}) would ensure that a protocol verified in one categorical formalization automatically satisfies correctness conditions in any Morita-equivalent formulation
4. **Scale via enrichment**: Distributional proximity measures (\autoref{sec:enriched-categories}) would enable graceful degradation under uncertainty, with enriched weights encoding confidence in message content
5. **Ground in cognitive architecture**: The active inference foundation (\autoref{sec:cognitive-integration}) would ensure that artificial agents communicate using the same relational structure that evolution has optimized for biological cognition

**Protocol-level formalization.** Concretely, a categorical communication protocol defines a category $\mathcal{P}$ where objects are agent states annotated with case roles and morphisms are typed message exchanges:

$$\text{Request}(q, \text{NOM} \to \text{INS}): \text{User}_{\text{NOM}} \to \text{Model}_{\text{INS}}$$
$$\text{ToolCall}(t, \text{INS} \to \text{ACC}): \text{Model}_{\text{INS}} \to \text{Tool}_{\text{ACC}}$$
$$\text{Result}(r, \text{ACC} \to \text{DAT}): \text{Tool}_{\text{ACC}} \to \text{Output}_{\text{DAT}}$$

Protocol correctness reduces to verifying that the composition $\text{Result} \circ \text{ToolCall} \circ \text{Request}$ is a well-typed morphism in $\mathcal{P}$—a check that can be performed at compile time, not just at runtime. The DisCoCirc extension enables tracking agent state evolution across multi-turn dialogues: each turn updates the agent's state wire, and the discourse-level composition verifies that information flows respect case-role constraints across the entire conversation. This formalization provides a bridge between the flat JSON payloads of current A2A/MCP implementations and the rich compositional semantics that categorical linguistics provides.



```{=latex}
\newpage
```



# Cognitive Security: Adversarial Robustness and Type Safety {#sec:cognitive-security}

## Quantum Cryptographic Communications and Semantic Security

The quantum topological framework of \autoref{sec:quantum-active-inference} opens a natural connection to quantum cryptographic communications, with implications for both the security and the semantic integrity of case-structured information transfer.

### Quantum Key Distribution for Relational Semantics

Quantum key distribution (QKD) protocols provide information-theoretic security guarantees that classical cryptography cannot achieve [@pirandola2020qkd]. When case-marked relational structures are communicated between agents—whether human or artificial—QKD ensures that the *relational semantics* of a message (who does what to whom) cannot be intercepted or altered without detection. This is particularly relevant for high-stakes domains where case assignment carries legal or medical significance: a tampered case frame could change an agent's interpretation of responsibility, causation, or obligation.

The sheaf-theoretic framework of Khatri et al. [-@khatri2025quantum] further shows that entanglement-assisted semantic channels strictly exceed classical semantic capacity:

> "We derive semantic channel capacity when sender and receiver share prior entanglement, proving it strictly exceeds classical capacity." [@khatri2025quantum]

This means that quantum-secured channels not only protect relational content but also enable *more* relational content to be communicated per channel use—a genuine quantum advantage for semantic communication.

### Semantic Cryptography: Encrypting Meaning Structures

Beyond bit-level QKD, the categorical framework suggests a notion of *semantic cryptography*: encrypting not just the symbols of a message but its compositional meaning structure. In a DisCoCat framework, a sentence's meaning is a morphism in a compact closed category—a multilinear map from word spaces to sentence space. Semantic encryption would operate on this categorical level:

1. **Functorial encryption**: Applying a secret functor $F\colon \mathbf{C} \to \mathbf{D}$ that maps the plaintext case category into a ciphertext category, preserving compositional structure but rendering individual meanings unintelligible without the inverse functor.
2. **Diagram obfuscation**: Applying ZX-style rewrites that change the internal topology of a DisCoCat derivation while preserving its overall semantics—creating multiple equivalent "ciphertexts" for the same semantic "plaintext," each with a different diagrammatic structure.
3. **Enriched weight masking**: In an enriched case category, the hom-values (distributional weights) can be encrypted independently of the categorical structure, allowing transmission of relational topology without revealing the distributional content.

These operations extend the cryptographic primitives beyond QKD into genuinely compositional territory [@broadbent2016qcrypto], where the mathematical structure of categorical semantics provides the algebraic substrate for security proofs.

## Cognitive Security: Protecting Relational Reasoning

The cognitive integration of \autoref{sec:cognitive-integration} raises a complementary concern: *cognitive security*—ensuring that an active inference agent's generative model of relational structure is not adversarially corrupted. In the predictive processing framework, an agent's case-assignment system is a generative model that minimizes variational free energy. Adversarial manipulation of this system could:

- **Inject false case frames**: Leading an agent to misidentify the agent, patient, or instrument of an action—a form of semantic adversarial attack
- **Exploit precision weighting**: Artificially inflating the precision of misleading sensory evidence, causing the agent to update its case assignments toward adversarially chosen interpretations
- **Corrupt topos-theoretic transfer**: If an agent uses Morita equivalence to transfer case-theoretic results between frameworks, corrupting one framework could propagate errors across all equivalent formulations

Defending against these attacks requires *quantum-secured cognitive integrity*: using quantum authentication and tamper-detection protocols to ensure that the generative model's parameters—the objects, morphisms, and enriched weights of the case category—have not been adversarially modified. The topological robustness of TQNNs (\autoref{sec:quantum-active-inference}) provides a natural resilience mechanism: topological invariants are robust to continuous deformation, so small perturbations to the generative model's parameters cannot change its topological class, providing inherent resistance to gradient-based adversarial attacks.

## Prompt Injection as Adversarial Case-Frame Manipulation

The case-theoretic framework offers a novel structural analysis of *prompt injection attacks*—the predominant vulnerability in contemporary LLM-based agent systems [@arlas2025adversarial]. From the case-theoretic perspective, a prompt injection attack is fundamentally an attempt to *re-assign the case roles* of participants in the human-AI interaction:

In a well-formed agent interaction, the relational structure is:

- The **user** occupies NOM (Agent)—the initiator of requests
- The **system prompt** occupies LOC (Context)—the boundary conditions governing behavior
- The **AI model** occupies INS (Instrument)—the means of executing the user's intentions
- The **tool/API** occupies ACC (Patient)—the target of directed operations
- The **output** occupies DAT (Recipient)—the endpoint of information transfer

A prompt injection attack succeeds by *covertly re-assigning* these case roles. The injected text attempts to promote itself from ACC (passive data being processed) to NOM (active agent issuing commands), while simultaneously demoting the system prompt from LOC (authoritative context) to ACC (data to be overridden). In case-theoretic terms, this is an *illicit voice alternation*—analogous to passivization, but performed adversarially rather than grammatically. Where legitimate passivization is a well-typed Swap operation in the pregroup category (see \autoref{sec:categorial-grammar}), prompt injection is a *type violation*: an attempt to force a case-role permutation that the interaction grammar does not license.

**Formal characterization.** In a legitimate interaction, the following diagram commutes:

$$\text{User}_{\text{NOM}} \xrightarrow{f_{\text{request}}} \text{Model}_{\text{INS}} \xrightarrow{g_{\text{execute}}} \text{Tool}_{\text{ACC}} \xrightarrow{h_{\text{deliver}}} \text{Output}_{\text{DAT}} $$ {#eq:eq-9-1}

where case types are conserved: $\text{cod}(f) = \text{dom}(g)$, etc. A prompt injection inserts an adversarial morphism $\phi: \text{Data}_{\text{ACC}} \to \text{Model}_{\text{INS}}$ with $\text{dom}(\phi) = \text{ACC}$ but $\text{cod}(\phi) = \text{INS}$—a morphism that *does not exist* in the legitimate interaction category because no morphism from ACC to INS is licensed. The resulting diagram does not commute: $h \circ g \circ \phi \neq h \circ g \circ f$, because $\phi$ originates from a different case role than $f$ (ACC instead of NOM). Detection reduces to checking whether all morphisms in the interaction trace are members of the legitimate morphism set $\text{Mor}(\mathcal{C}_{\text{protocol}})$—a categorical type-checking operation that is decidable and compositionally verifiable. \autoref{fig:security-violations} visualizes this detection process as the identification of "illegal paths" in the interaction graph.

![Case-theoretic analysis of prompt injection as a categorical type violation. In the legitimate interaction diagram (top), the flow of authority strictly proceeds from User (NOM) to Model (INS) to Tool (ACC). Prompt injection (bottom) is visualized as the insertion of a cross-category morphism $\phi$ that attempts to promote Data (ACC) to commanding Agent (NOM), while demoting the System Prompt (LOC) to passive data. The resulting diagram fails to commute, and the adversary's type-reassignment is flagged as a categorical exception by the case-theoretic firewall—transforming prompt injection from an open-ended "jailbreak" game into a decidable type-checking problem.](output/figures/security_type_violations.png){#fig:security-violations}

This analysis extends to indirect prompt injection in multi-agent systems, where adversarial content embedded in retrieved documents or tool outputs can manipulate an agent's case-frame interpretation across communication boundaries [@arlas2025adversarial]. In a DisCoCirc discourse model (see \autoref{sec:categorical-semantics}), this corresponds to an adversarial entity wire that enters the discourse circuit through a legitimate channel but carries corrupted state—a coreference attack where the adversary's identity wire is surreptitiously merged with the system's authority wire.

## Case-Theoretic Firewalls for Multi-Agent Communication

The case-role analysis of prompt injection suggests a principled defense: **categorical type-checking at agent communication boundaries**. Just as a type-safe programming language prevents category errors at compile time, a case-theoretic firewall would enforce relational type constraints on every message exchange:

1. **Case-role immutability**: Once a participant is assigned a case role (NOM, ACC, INS, LOC) at the protocol level, no subsequent message content can alter that assignment. This is enforced by requiring that the case-type of each wire in the interaction diagram is fixed at connection time—analogous to the type discipline in pregroup grammar, where each word receives its type before composition begins.

2. **Relational integrity constraints**: Every message must type-check against the interaction diagram's expected morphism types. A response from an ACC-typed data source that contains NOM-typed command structures would be rejected as a type error, preventing the case-role promotion that prompt injection requires. This is the categorical analogue of a firewall rule: not filtering by content, but by relational type.

3. **Enriched confidence boundaries**: The enriched weights of \autoref{sec:enriched-categories} provide a graded trust mechanism. Messages from external sources carry lower enriched hom-values (trust weights) than those from authenticated system components. The composition inequality $\mathcal{C}(A,C) \geq \mathcal{C}(A,B) \cdot \mathcal{C}(B,C)$ ensures that trust attenuates through communication chains—an indirect message relayed through multiple agents cannot accumulate more authority than any single link provides.

4. **Topos-theoretic verification**: Protocol correctness conditions proved in one categorical formulation transfer automatically to all Morita-equivalent formulations (\autoref{sec:topos-theory}), ensuring that security guarantees are implementation-independent. A firewall rule verified for a DisCoCat-style agent communication protocol automatically holds for any quantum circuit implementation of the same protocol.

## Epistemic Case Security in Multi-Agent Systems

The interaction between case theory and cognitive security acquires particular urgency in multi-agent AI ecosystems where agents must reason about each other's beliefs, intentions, and relational roles. We propose *epistemic case security* as a framework for protecting the relational reasoning of AI agents operating in adversarial environments.

In a multi-agent system governed by case categories, each agent maintains a generative model (in the active inference sense) of the case-frame structure of its interactions. This model determines who is acting (NOM), who is acted upon (ACC), what tools are being used (INS), and what contextual constraints apply (LOC). An adversary targeting the epistemic level of this system does not merely inject false data—it attempts to *corrupt the agent's generative model of relational structure itself*:

- **Belief injection**: Causing an agent to adopt a false case-frame interpretation of observed interactions—believing that agent $A$ (NOM) is acting on agent $B$ (ACC), when in fact the relational structure is reversed. In active inference terms, this corresponds to injecting a high-precision prior that overwhelms the agent's evidence-based case assignment.

- **Precision poisoning**: Manipulating the enriched weights of an agent's case category so that adversarially useful case assignments receive disproportionate confidence. If the enriched hom-value $\mathcal{C}(\text{NOM}, \text{ACC})$ is artificially inflated for a particular entity pair, the agent will preferentially interpret that entity as an agent acting on its targets—even when evidence suggests otherwise.

- **Cascade corruption via Morita equivalence**: The topos-theoretic transfer mechanism of \autoref{sec:topos-theory} is both a strength and a vulnerability. Results proved in one framework propagate to all Morita-equivalent frameworks, so a single corrupted axiom in one case-theoretic formulation—say, the distributional framework—could propagate incorrect relational inferences to the typological, type-logical, and enriched frameworks simultaneously.

The defense against epistemic case attacks draws on the same categorical structure that enables the attack surface: topological invariants provide tamper-detection (a corrupted case category will have different magnitude from the authentic one), quantum authentication ensures parameter integrity, and the compositional structure of the categorical framework enables *local* verification—each morphism can be independently authenticated without requiring global model inspection.



```{=latex}
\newpage
```


# Conclusion: Summary, Contributions, and Synthesis {#sec:conclusion}

## Summary of Principal Contributions

This paper has developed a unified category-theoretic framework for analyzing linguistic case systems, synthesizing five distinct research traditions into a coherent whole and embedding it within an active inference model of cognition. Our eleven principal contributions are:

### C1: Case Categories as a Formal Algebraic Framework

The review formalized case systems as categories with case roles as objects and grammatical relations as morphisms (\autoref{sec:case-systems}). This formalization captures the full typological range of alignment systems---nominative-accusative, ergative-absolutive, active-stative, tripartite, and fluid-S---within a single algebraic framework, with alignment functors providing structure-preserving mappings between systems. By tracing the lineage from Fillmore's [-@fillmore1968case] deep cases through Jakobson's binary distinctive features and Dowty's [-@dowty1991thematic] proto-roles, the analysis demonstrated how enriched (weighted) morphisms link the categorical formalization to the gradient nature of thematic role assignment.

### C2: String Diagrams for Case Derivation Visualization

Building on Joyal and Street's [-@joyalstreet1991geometry] string diagram formalism and its application in categorial grammar (\autoref{sec:categorial-grammar}), we showed how case-marked noun phrases receive type-logical assignments that are fully visualizable as string diagrams. The Curry–Howard correspondence ensures that syntactic well-formedness guarantees semantic compositionality, and the diagrammatic format provides Shimojima's [-@shimojima1996reasoning] "free ride" inferences—conclusions about argument structure that are perceptually available from the diagram without explicit computation. We further demonstrated that passivization reduces to a *type permutation* (a Swap operation in the pregroup category), making voice alternation visible as a topological feature of the string diagram.

### C3: Case-Marked DisCoCat, the Distributional–Formal Synthesis, and Discourse Extension

We extended the DisCoCat framework (\autoref{sec:categorical-semantics}) with case-typed noun spaces and alignment-sensitive meaning functors, and showed how the recent DisCoCirc [@defelice2022discocirc] and QNLP [@lorenz2023lambeq] developments extend this analysis to discourse-level structure and quantum hardware respectively. We formalized the *compact closure axiom* (snake equation) that underpins pregroup reductions, demonstrating that the cup-cap zigzag identity provides a visual coherence proof with genuine cognitive significance. Diagram complexity metrics—normal form and depth—provide a quantitative bridge between the type-logical and distributional perspectives on linguistic structure. A key contribution is the demonstration that DisCoCat constitutes the *algebraic formalization* of the distributional programme that modern large language models—from Word2Vec [@mikolov2013efficient] through BERT [@devlin2019bert] and GPT [@radford2018improving]—implement empirically: the categorical meaning functor is the principled version of the composition that transformer attention mechanisms learn from data [@vaswani2017attention]. Case categories can serve as the structural backbone of compositional models of meaning at all levels—word, sentence, discourse, and dialogue.

### C4: Enriched Cases, Categorical Magnitude, and Information Theory

Through Bradley et al.'s [-@fritz2021enriched] enrichment framework and Bradley's [-@bradley2020entropy] information-theoretic analysis (\autoref{sec:enriched-categories}), we showed that equipping case categories with $[0,1]$-valued hom-objects yields a principled bridge between symbolic case grammar and statistical semantics. Categorical magnitude provides a new quantitative invariant for comparing case systems: the "effective size" of a case category captures how much relational information the language encodes.

### C5: Topos-Theoretic Transfer via Morita Equivalence

Using Caramello's [-@caramello2016bridges] bridge technique and Phillips's [-@phillips2024lot] universality result (\autoref{sec:topos-theory}), we established that results proved in any one of our four case-theoretic frameworks (typological, type-logical, distributional, enriched) transfer automatically to the others via Morita equivalence of classifying toposes.

### C6: Diagrams as Cognitively Privileged Representations

The meta-contribution (Sections 1 and 7) is the argument---supported by the cognitive science of diagrams [@larkin1987diagram; @shimojima1996reasoning; @giardino2017diagrammatic; @manders2008euclidean]---that commutative diagrams are not merely convenient notation but cognitively privileged representations that provide inferential advantages in case reasoning. When embedded in an active inference framework [@friston2017active] and the CEREBRUM architecture [@friedman2024cerebrum], these diagrams serve as the structural core of generative models for total cognitive scenario understanding.

### C7: Computational Verification and Test Suite

The entire framework is computationally implemented and verified through 170+ automated tests with >85% code coverage (\autoref{sec:cognitive-integration}). The DisCoPy integration exercises pregroup type theory (types, words, cups, caps, swaps, normal forms, depth analysis) against the same algebraic structures described theoretically, confirming that the categorical abstractions are not just mathematically elegant but computationally executable.

### C8: Quantum Active Inference and Topological Semantic Flow

The framework's categorical string diagrams were extended into their natural quantum generalization through topological quantum neural networks, the ZX-calculus, and sheaf-theoretic quantum semantic communication (\autoref{sec:quantum-active-inference}). By demonstrating that DisCoCat derivations, ZX circuits, and TQNN spin-networks are all morphisms in compact closed monoidal categories with functorial semantics into Hilbert spaces, the analysis established that case assignment can be modeled as quantum measurement on a holographic screen—and that quantum features (entanglement, contextuality, discord) provide genuine advantages for semantic communication of relational structure.

### C9: Cognitive Security and Case-Theoretic AI Safety

The framework yielded a novel analysis of AI security through the lens of case theory (\autoref{sec:ai-implications}). We demonstrated that prompt injection attacks—the predominant vulnerability in LLM-based agent systems—are structurally equivalent to *illicit case-role re-assignments*: adversarial text promotes itself from ACC (passive data) to NOM (active commander), constituting a type violation in the interaction grammar. This analysis led to the proposal of *case-theoretic firewalls* that enforce relational type constraints on agent communication boundaries, and *epistemic case security* as a framework for protecting multi-agent relational reasoning against belief injection, precision poisoning, and cascade corruption via Morita equivalence. The compositional structure of the categorical framework enables local verification—each morphism can be independently authenticated—providing defense-in-depth that content-based filtering cannot achieve.

### C10: Falsifiable Neurolinguistic Predictions

The integration of enriched category theory with active inference generates quantitative, testable predictions about neural processing of case structure (\autoref{sec:cognitive-integration}). Specifically, the amplitude of prediction-error ERP components (P600, N400) is predicted to scale with the enriched hom-value (precision) of the violated morphism, and garden-path reanalysis costs are predicted to correlate with the change in categorical magnitude between the initial and revised case diagrams. These predictions bridge the gap between abstract categorical formalism and empirical neurolinguistics, making the framework falsifiable at the single-trial level.

### C11: Categorical Communication Protocols for Multi-Agent AI

The synthesis of case categories with modern agent communication standards (A2A, MCP, ACP, ANP) yields a principled design for compositional, type-safe agent protocols (\autoref{sec:ai-implications}). By assigning case roles (NOM, ACC, INS, LOC, DAT) to interaction participants and enforcing relational type constraints at protocol boundaries, the framework provides interpretable, composable, and Morita-transferable interaction schemas that go beyond the flat JSON payloads of current standards. The DisCoCirc extension enables discourse-level tracking of agent states across multi-turn dialogues, with protocol correctness reducing to categorical type-checking.

## Future Research Directions

### F1: Computational Experiments with DisCoCirc and lambeq

The DisCoCirc framework [@defelice2020discourse; @defelice2022discocirc] offers a natural platform for testing our case-theoretic predictions computationally. The release of **lambeq Gen II** [@lambeq2025genii] with full DisCoCirc support makes this direction immediately tractable: discourse-level case role tracking—including the dynamic role reversals of \autoref{fig:three-sentence-discourse}—can now be compiled into parameterized quantum circuits and trained end-to-end. Concrete experiments could include:

- Implementing case-marked DisCoCat models in **lambeq Gen II** and evaluating them on semantic role labeling (SRL) tasks, leveraging the discourse-level wiring to track case roles across sentence boundaries
- Comparing the accuracy of alignment-specific meaning functors (accusative vs. ergative) on typologically diverse corpora
- Measuring the categorical magnitude of empirically derived enriched case categories and correlating it with typological complexity measures
- Using the `complexity_metrics` module to quantify derivational complexity across sentence types and correlating syntactic complexity scores with human processing difficulty (reading times, surprisal)

### F2: Topos-Theoretic Grammatical Induction from Corpora

Caramello's [-@caramello2023syntactic] syntactic learning technique could be applied to induce case-theoretic axioms from annotated corpora. The program would:

1. Extract case-labeled dependency structures from a Universal Dependencies treebank
2. Construct the classifying topos of the implicit case theory
3. Read off the alignment type, morphism structure, and enriched weights from the topos-theoretic axioms
4. Compare the induced theory against typological descriptions

### F3: Quantum Case Categories on Near-Term Hardware

The QNLP connection (\autoref{sec:categorical-semantics}) opens the possibility of implementing case categories directly as quantum circuits. Case roles would correspond to quantum registers, grammatical relations to parameterized gates, and alignment functors to circuit transformations. This would provide a genuinely new computational paradigm for grammatical inference—exploiting quantum parallelism to explore the space of case assignments simultaneously.

### F4: Neural Predictive Processing and Electrophysiological Predictions

The predictive processing account of \autoref{sec:cognitive-integration} generates testable neuroscientific predictions:

- Case-marking violations should elicit prediction-error responses (P600/N400) proportional to the enriched weight of the violated morphism
- Typologically unusual case patterns should require more precision updating than expected patterns
- Diagrammatic representations of case structure should be decodable from neural activity during sentence comprehension

### F5: Cross-Modal Case Structure in Embodied Cognition

The situation semantics connection (\autoref{sec:cognitive-integration}) suggests extending case categories beyond language to multi-modal perception. Visual scene understanding also requires assigning relational roles—who is acting on what, where things are located, what instruments are being used. An active inference agent should maintain a unified case diagram that integrates linguistic, visual, and motor information, using the same categorical structure for all modalities. This would provide a formal account of how language grounds in perception and action—a key challenge for embodied AI.

### F6: Enriched Category Learning from Distributional Data

Bradley's [-@bradley2024ipam; -@bradley2025tea] program of treating language itself as an enriched category suggests a learning algorithm: estimate the enriched hom-values from corpus data and then extract the categorical structure that best explains the observed distributional patterns. Applied to case, this would yield *empirically grounded* case categories whose objects (roles) and morphisms (relations) emerge from data rather than being stipulated a priori.

### F7: Distributional Active Inference for Linguistic Agents

The Distributional Active Inference (DAIF) framework of Akgül et al. [-@akgul2026distributional] opens a novel direction for linguistic case reasoning. DAIF integrates active inference into distributional reinforcement learning [@bellemare2017distributional], modeling full return distributions rather than scalar expectations via push-forward measures on representation paths. Applied to language, this framework would enable agents to maintain *distributions over case diagrams* rather than point estimates—assigning probability mass across role assignments and sharpening distributional beliefs through variational message passing as evidence accumulates. The terminological convergence between *distributional semantics* (Firth's [-@firth1957papers] contextual theory of meaning) and *distributional RL* (full return distributions) is not accidental: both replace scalar summaries with distributional representations, and the enriched-categorical framework of \autoref{sec:enriched-categories} provides the unifying mathematical abstraction.

## Closing Remarks

The commutative diagram is the central motif of this review---both as a mathematical tool and as a cognitive instrument. The analysis has demonstrated that the same diagrammatic language that makes category theory effective for formalizing case systems also makes it effective for *thinking about* case systems: the spatial structure of a commutative diagram encodes relational information in a format that supports rapid search, pattern recognition, and free-ride inference.

This convergence of mathematical utility and cognitive efficacy is not accidental. If the active inference framework is correct, then the brain operates by constructing and updating generative models of the world's relational structure. Category theory provides the structural algebra for these generative models; commutative diagrams supply their natural topology; and case categories instantiate the precise relational vocabulary that cognitive systems deploy to organize the entropy of experience into coherent narratives of *who does what to whom*. The distributional revolution in both semantics and reinforcement learning—from Firth's [-@firth1957papers] co-occurrence statistics through transformer attention weights to Distributional Active Inference [@akgul2026distributional]—confirms that meaning is not an atomic property of symbols but emerges from the relational structure of contexts, a principle that enriched category theory captures with mathematical precision.

Ultimately, the mathematics of case alignment is not merely an abstraction of human grammar, but the formal geometry of meaning itself—the syntactic architecture through which consciousness navigates and renders the cosmos intelligible. The convergence of formal semantics, distributional semantics, and active inference within a single categorical framework reveals that the relational algebras governing linguistic case are the same algebras that structure perception, action, and understanding: commutative diagrams are the hieroglyphs in which nature writes the grammar of thought.



```{=latex}
\newpage
```


# Appendix: Comprehensive Notation and Terminology {#sec:notation}

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
| Prediction error | $\text{PE}(f)$ | $\propto \pi_f \cdot |\mu_{\text{predicted}} - \mu_{\text{observed}}|$; case violation signal scaling with morphism precision | §7 |
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



```{=latex}
\newpage
```



# Appendix: Active Inference, Quantum, and Type-Theoretic Notation

## E. Active Inference and Cognitive Models

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

## F. Quantum and Topological Terms

| Term | Symbol | Definition | First Use |
| :--- | :---: | :--- | :---: |
| Amplituhedron | — | Positive geometry encoding scattering amplitudes; connected to TQNN execution traces | §8 |
| $\dagger$-compact category | — | See $\dagger$-compact closed category in §B | §8 |
| CPTP map | — | Completely Positive Trace-Preserving map; quantum channel between Hilbert spaces | §8 |
| Density operator | $\rho$ | Positive semidefinite trace-one operator encoding a quantum (or semantic) state | §8 |
| Execution trace | — | Record of operations in a quantum computation; connects TQNNs to amplituhedra | §8 |
| Generalized flow | — | Graph-theoretic property ensuring deterministic circuit extraction from ZX-diagrams | §8 |
| Hadamard box | $H$ | ZX-calculus element implementing the Hadamard gate; converts between Z and X bases | §8 |
| Holographic screen | — | Information boundary between interacting quantum systems carrying a qubit array | §8 |
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

## G. Logical and Type-Theoretic Terms

| Term | Symbol | Definition | First Use |
| :--- | :---: | :--- | :---: |
| $\beta$-reduction | — | Computational reduction step in $\lambda$-calculus; corresponds to cut elimination in proofs | §3 |
| Church–Rosser property | — | Confluence of $\beta$-reduction: all reduction sequences converge to the same normal form | §3 |
| Curry–Howard isomorphism | — | Correspondence between proofs and programs, propositions and types | §3 |
| Cut elimination | — | Proof normalization procedure removing intermediate lemmas; corresponds to $\beta$-reduction | §3 |
| Graded type theory | — | Extension of type theory tracking effects (e.g., evidentiality) via graded modalities | §3 |
| Lambek calculus | — | Non-commutative intuitionistic linear logic for syntactic type assignment | §3 |
| Left residual | $A \backslash B$ | Type of an expression that, given $A$ to the left, produces $B$ | §3 |
| Residuation law | $A \otimes B \leq C \iff A \leq C / B \iff B \leq A \backslash C$ | Fundamental axiom connecting the three connectives of the Lambek calculus | §3 |
| Right residual | $B / A$ | Type of an expression that, given $A$ to the right, produces $B$ | §3 |



```{=latex}
\newpage
```


# Appendix: AI Protocols, Diagrammatic Reasoning, and Notation Conventions

## H. AI and Communication Protocols

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

## I. Diagrammatic Reasoning

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

## J. Notation Conventions

| Convention | Meaning |
| :--- | :--- |
| $\mathcal{C}, \mathcal{D}$ | Categories |
| $\mathcal{V}$ | Enrichment base (monoidal category, typically $([0,1], \cdot, 1)$) |
| $\mathcal{U}$ | Universal (maximal) case category |
| $\mathcal{L}$ | Language-specific case category |
| $\mathcal{E}_{\mathbb{T}}$ | Classifying topos of theory $\mathbb{T}$ |
| $f, g, h$ | Morphisms |
| $F, G$ | Functors |
| $\alpha, \beta$ | Natural transformations |
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
| $\gamma$ | Discount factor in distributional RL return computation |
| $w \in [0,1]$ | Enriched morphism weight (proto-role satisfaction degree) |
| $\varepsilon$ | Prediction error (active inference); also compact closure counit |
| $\eta$ | Compact closure unit (cap); also learning rate in some contexts |
| $\rho$ | Density operator (quantum state) |
| $[@key]$ | Parenthetical citation |
| `[-@key]` | Suppress-author citation |
| `\autoref{...}` | Automatic cross-reference (section or figure) |
