
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
