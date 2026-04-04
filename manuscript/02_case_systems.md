
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
