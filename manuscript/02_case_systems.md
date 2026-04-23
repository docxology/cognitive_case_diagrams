# Case Systems: From Pāṇinian Kāraka to Cross-Linguistic Alignment Typology {#sec:case-systems}

**Where we are in the argument.** \autoref{sec:introduction} stated the central claim — that commutative diagrams are cognitively privileged because they encode algebra, distribution, and inference at once, with case as the pivot. Before we formalise case as a category in \autoref{sec:case-categories}, this chapter surveys the linguistic input the formalism must cover: five analytical traditions (Pāṇinian $k\bar{a}raka$, Fillmorean deep case, Jakobsonian features, Mel'čukian dependency, Haspelmathian typology) and the five alignment typologies (nominative-accusative, ergative-absolutive, tripartite, active-stative, fluid-S) on which cross-linguistic variation converges.

## Five Analytical Traditions That Shaped the Modern Theory of Case

### The Pāṇinian Kāraka Framework

The formal study of grammatical case originates with Pāṇini (circa 4th century BCE), whose *Aṣṭādhyāyī*—a grammar of approximately 4,000 rules that predates Euclid—formalized the *kāraka* theory. This framework first classified semantic roles—agent, patient, instrument, and others—as deep relational functions linking verbs to their arguments, abstracting away from surface morphosyntactic inflections. Etymologically meaning "that which brings about" an action, the kāraka system establishes a rigorous mapping from conceptual predication to phonological realization [-@jha2021sanskrit; -@kak1987paninian].

### Jakobson’s Structural Features and the Prague School

This profound semantic foundation lay predominantly dormant until structural linguists resurrected it in the mid-20th century. Roman Jakobson's *Morphologic Inquiry into Slavic Declension* (1958) decomposed grammatical cases into binary distinctive features (e.g., [±directional], [±peripheral]) [-@jakobson1958morphologic]. By treating case oppositions analogously to phonological features, Jakobson shifted the field from Pāṇini's holistic roles to a componential analysis that exposes deep relational hierarchies and markedness. Concurrently, Louis Hjelmslev's *La catégorie des cas* [-@hjelmslev1935categorie] reinforced this functionalist tradition by formalizing case as a purely relational category within a dynamic semiotic network.

To make Jakobson's componential analysis tangible, consider the six-case singular paradigm of the Russian masculine inanimate noun *stol* "table": NOM *stol* / ACC *stol* / GEN *stolá* / DAT *stolú* / INS *stolóm* / PREP (LOC) *stolé*. The same root surfaces in six morphological guises whose contrasts Jakobson decomposes along the binary features `[±directional]` (the dative singles out goal-directed cases) and `[±peripheral]` (the instrumental and locative push out from the core argument cases). Serbian/BCS *prijatelj* "friend" runs a parallel paradigm but adds an overt vocative *prijatelju!* "friend!", giving a seven-way contrast that exercises the entire eight-role inventory we adopt in \autoref{tbl:eight-cases} (with the ablative absorbed into Slavic genitive-of-source and the prepositional/locative). These overt morphological contrasts will reappear in \autoref{sec:case-categories} as concrete witnesses for the alignment functor and in \autoref{sec:enriched-categories} as a calibration source for $[0,1]$-enriched hom-values. Slavic languages — with their dense nominal morphology, productive derivation, and unambiguous case suffixes — are also a natural stress-test candidate for the Distributional Active Inference framework developed in \autoref{sec:daif-results}; the limitations discussion in \autoref{sec:daif-limitations} returns to this point explicitly, noting that a Russian or Serbian/BCS sentence would deliver an information-theoretically sharper drop in posterior entropy than the German example currently shipped.

### Fillmore’s Deep Case and Generative Roots

Charles Fillmore's seminal "The Case for Case" (1968) built directly upon this structuralist lineage, explicitly translating these concepts into the burgeoning generative linguistics framework. Fillmore proposed *deep cases* (e.g., Agentive, Objective, Dative) as universal semantic primitives underlying surface syntax. Crucially, he argued that verbs assign underlying *case frames* which subsequently generate surface structures [-@fillmore1968case]. This evolution transformed Pāṇini's kāraka into deep relational networks, permanently prioritizing universal semantics over language-specific morphology.

### Mel'čuk's Meaning-Text Theory (MTT)

A distinct but parallel formalization emerged with Aleksandr Žolkovskij and Igor Mel'čuk's Meaning-Text Theory (MTT) [@zolkovskij1965possible; @melcuk1981meaning; @melcuk1988dependency]. Developed initially in Moscow, MTT models natural language as a rigorous, many-to-many correspondence between meanings (deep semantic representations) and texts (surface-phonological representations). The transition from meaning to text unfolds across a multi-level synthesis process: Deep Semantics, Deep-Syntactic, Surface-Syntactic, Morphological, and Phonological. At the deep-syntactic level, meaning is represented via *dependency trees* linking lexical units through dependency relations. The nodes are populated by *actants*—semantic roles closely aligning with thematic grids but strictly language-specific in their surface realization.

Crucially, MTT establishes that grammatical case is not directly semantic, but rather a final surface-morphological phenomenon governed by syntactic linearization and dependency constraints. *Lexical functions* map actants to surface structures, explicitly demonstrating that morphosyntactic inflection serves merely as the end-stage formal realization of deep semantic relations. By monotonically mapping meaning to text via hierarchical dependency graphs, MTT provided an exhaustive synthesis that presages our modern categorical formalizations mapping conceptual structures to syntactic types.

### Dowty’s Proto-Roles and Graded Topologies

Where MTT models the *mapping* from deep semantic roles to surface morphology via hierarchical dependency graphs, Dowty's contribution is to decompose the deep roles themselves into continuous, gradient primitives. Fillmore's deep cases serve as the direct precursors to modern *thematic role* theory. Dowty [-@dowty1991thematic] refined this paradigm by decomposing thematic roles into clusters of sentential entailments, yielding two *proto-roles*: the Proto-Agent (characterized by volitional involvement and causation) and the Proto-Patient (characterized by incremental themes and causal affectedness). This decomposition proves critical for our categorical formalization: it replaces discrete, named roles with a *graded* structural topology where role assignment is a matter of degree rather than kind. Consequently, morphisms in our cognitive case diagrams carry continuous weights $w \in [0,1]$ representing the degree to which a noun phrase satisfies proto-role entailments—a design choice that yields the enriched category structure developed formally in \autoref{sec:enriched-categories}.

## Alignment Typology: How Languages Group S, A, and P

Contemporary typological work reveals that the world's languages realize case systems according to a small number of *alignment types*—systematic patterns governing how the core arguments of transitive and intransitive clauses are grouped [@polinsky2015case; @blake2001grammatical; @haspelmath2009universality].

### The Three Core Argument Primitives: S, A, P

The cross-linguistic comparison rests on three primitives:

| Symbol | Role | Definition |
| :---: | :---- | :--- |
| **S** | Sole argument of intransitive | "The child **sleeps**" |
| **A** | Agent-like argument of transitive | "**The child** broke the vase" |
| **P** | Patient-like argument of transitive | "The child broke **the vase**" |

Table: The three core argument primitives used in cross-linguistic case typology. {#tbl:s-a-p}

### The Five Cross-Linguistic Alignment Types

The key insight from typological research is that languages differ in how they *group* these three roles for purposes of case marking, agreement, and other grammatical processes:

| Alignment | Grouping | Exemplar Languages |
| :--- | :--- | :--- |
| **Nominative–Accusative** | S = A $\neq$ P | English, Latin, Finnish, Russian |
| **Ergative–Absolutive** | S = P $\neq$ A | Basque, Dyirbal, Georgian (partly) |
| **Active–Stative** | S splits by agentivity | Lakhota, Guaraní, Eastern Pomo |
| **Tripartite** | S $\neq$ A $\neq$ P | Nez Perce, some Australian languages |
| **Fluid-S** | S marking varies by context | Bats (NE Caucasian), Acehnese |

Table: Five alignment types and their grouping of the three core argument primitives. {#tbl:alignment-types}

**Slavic case morphology as a stress-test for the formalism.** Russian (six cases) and Serbian/BCS (seven cases including a productive vocative) sit firmly in the nominative-accusative column of \autoref{tbl:alignment-types}, yet their nominal paradigms exercise the *full* eight-role inventory of \autoref{tbl:eight-cases} in ways that English's collapsed paradigm hides. Two animacy-conditioned syncretisms in Russian masculine singular illustrate the point precisely:

- **Inanimate masculine — NOM = ACC syncretism.** *stol* "table" surfaces identically in subject and direct-object position (NOM *stol* / ACC *stol*; *Stol stoit* "the table stands" vs. *Vižu stol* "I see the table"). The surface-realisation functor $M\colon\mathcal{C}_{\text{grammatical}} \to \mathcal{C}_{\text{morphological}}$ identifies $\{\text{NOM},\text{ACC}\}$ for this declension class — a *partial* kernel that coexists with full distinguishability for feminine and neuter paradigms.
- **Animate masculine — ACC = GEN syncretism.** *brat* "brother" takes ACC = GEN *brata* (*Vižu brata* "I see the brother", same form as the genitive *bez brata* "without the brother"). The morphology overtly licenses the canonical formalism's claim that the surface functor neutralises distinct grammatical objects on a *paradigm-by-paradigm* basis, not globally.

Serbian/BCS replicates the same animacy split (*čovek* / *čoveka* parallel to *brat* / *brata*) and adds a productive vocative (*prijatelju!* "friend!", *bože!* "God!") that English lacks entirely. These are exactly the empirical witnesses the alignment functor of \autoref{sec:case-categories} predicts: where English shows a single inflectionless noun, Slavic morphology exposes a non-trivial kernel structure on a per-declension-class basis, supplying ready-made cross-linguistic targets for the categorical apparatus we develop next.

**Fluid-S and Context-Dependent Functors.** In Bats (Nakh-Daghestanian), the intransitive subject of a single verb surfaces in different cases strictly depending on the speaker's internal construal of agentive volition. For example, the verb *fall* assigns an absolutive S when the action is accidental (*The child-ABS fell*), but assigns an ergative S when the action is volitional (*The child-ERG fell [on purpose]*).

Categorically, we model Fluid-S as a **context-dependent functor** $F_\theta: \mathcal{U} \to \mathcal{L}$ parameterized by a continuous volition feature $\theta \in [0,1]$. \autoref{fig:fluid-s} visualizes the resulting volition landscape: case categorization boundaries shift dynamically as a direct function of the agent's internal construal, satisfying naturality only up to a probabilistic reparameterization of $\theta$.

![Fluid-S alignment is a continuous mapping, not a binary switch. The context-dependent functor $F_\theta: \mathcal{U} \to \mathcal{L}$ is rendered as a 2D decision surface with volitional control $\theta \in [0,1]$ on the x-axis and proto-agentivity [@dowty1991thematic] on the y-axis. Color intensity represents $P(\text{ERG} \mid \theta, \text{agentivity})$, computed via a logistic boundary. Nakh-Daghestanian verb exemplars (Bats language) are overlaid at their typologically attested coordinates: low-volition actions (sneeze, accidental fall) cluster in the ABS region; high-volition actions (jump, fight) occupy the ERG region. The dashed curve marks the functor decision boundary where $F_\theta(S)$ transitions from ABS to ERG. Generated programmatically from `src.visualization.fluid_s_plots.plot_fluid_s_volition_landscape()`.](output/figures/fluid_s_volition_landscape.png){#fig:fluid-s}

**Synthetic Case-Role Algebra.** We introduce Synthetic Case-Role Algebra as a novel, computational upgrade to the Dowty-style proto-role framework. Where Dowty modeled proto-roles as static clusters of entailments [-@dowty1991thematic], we formalize them as **objects in a $[0,1]$-enriched monoidal category** with tensor product over role compositions. This advancement enables purely algebraic manipulation of semantic roles: composition, weighting, and transformation of roles proceed through functorial operations representing complex event structures such as causativization, serial verb constructions, and argument-structure alternations. Crucially, this enriched structure demonstrates that "case assignment" is not a discrete binary choice but a vector-valued expectation in continuous case space—providing the mathematical bridge between the symbolic traditions of formal grammar and the statistical representations of modern neural language models (\autoref{sec:categorical-semantics}).

Claassen [-@claassen2019alignment] surveys the explanatory frameworks proposed for alignment diversity, arguing that no single factor (processing efficiency, disambiguation, discourse pragmatics) suffices—a conclusion that motivates our multi-dimensional categorical formalization. Wu [-@wu2024amis] offers a detailed case study of Amis (Austronesian), demonstrating how verb classification, case marking, and grammatical relations interact in a language that defies simple alignment classification.

Beyond the three core arguments, languages distinguish a rich inventory of oblique cases. Our formalization follows the CEREBRUM framework [@friedman2024cerebrum] in adopting eight fundamental cases (\autoref{tbl:eight-cases}):

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

Table: Eight fundamental case roles adopted from the CEREBRUM framework [@friedman2024cerebrum]. {#tbl:eight-cases}

While historically used merely to diagram sentences, this exact eight-role inventory is what enables the **Categorical AI Protocol** introduced in \autoref{sec:ai-implications}. By rigidly mapping artificial agent capabilities to corresponding grammatical cases—e.g., treating an API as strictly `INS`, passive data strictly as `ACC`, and system context rigidly as `LOC`—the cognitive case diagram enforces computational boundary constraints that formally constrain prompt injection attacks through explicit role typing (\autoref{sec:cognitive-security}).
