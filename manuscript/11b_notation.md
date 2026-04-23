# Appendix B: Notation Reference {#sec:notation}

This appendix collects all notation, symbols, and technical terminology used throughout the manuscript. Entries are grouped by domain and ordered alphabetically within each section. The **First Use** column indicates the section where each term is first introduced or defined.

**Sections A–K:** A Linguistic Terms; B Category Theory; C Enriched Categories and Magnitude; D Distributional Semantics and LLMs; E Distributional Active Inference (DAIF); F Active Inference and Cognitive Models; G Quantum and Topological Terms; H Logical and Type-Theoretic Terms; I AI and Communication Protocols; J Diagrammatic Reasoning; K Notation Conventions.

Figures that colour-code case roles (category graphs, string diagrams, appendix panels) take those colours from the shared map `CASE_COLORS` in `src/visualization/styles.py` (keys are `CaseRole` names). Captions state the mapping where it matters for reading the diagram.

## Linguistic Terms {#sec:notation-linguistic}

Table: Linguistic terminology and symbols. {#tbl:not-linguistic}

| Term | Symbol | Definition | First Use |
| :------------ | :----: | :-------------------------------------------------------------- | :----: |
| Ablative | ABL | Case role encoding origin, source, or cause | [§2](02_case_systems.md#sec:case-systems) |
| Accusative | ACC | Case role encoding patient, theme, or direct object | [§2](02_case_systems.md#sec:case-systems) |
| Active–Stative alignment | — | Alignment in which the sole argument S splits by agentivity | [§2](02_case_systems.md#sec:case-systems) |
| Agent-like argument | A | The agent-like argument of a transitive clause | [§2](02_case_systems.md#sec:case-systems) |
| Alignment functor | $F: \mathcal{U} \to \mathcal{L}$ | Structure-preserving map from universal to language-specific case category | [§2](02_case_systems.md#sec:case-systems) |
| Alignment type | — | Systematic pattern governing how S, A, P are grouped for case marking | [§2](02_case_systems.md#sec:case-systems) |
| Case category | $\mathcal{C}$ | Small category whose objects are case roles and morphisms are grammatical relations | [§2](02_case_systems.md#sec:case-systems) |
| Case frame | — | The set of case roles activated by a particular verb or predicate | [§2](02_case_systems.md#sec:case-systems) |
| Case-typed noun space | $N_{\text{NOM}}, N_{\text{ACC}}, \ldots$ | Case-specific vector subspace in a case-enriched DisCoCat model | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Categorial grammar | — | Grammar assigning each lexical item an algebraic type encoding combinatory potential | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Contraction | $a^l \cdot a \to 1$ | Pregroup reduction eliminating an adjoint pair | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Dative | DAT | Case role encoding recipient, goal, or beneficiary | [§2](02_case_systems.md#sec:case-systems) |
| Deep case | — | Fillmore's universal semantic primitive (e.g., Agentive, Objective) | [§2](02_case_systems.md#sec:case-systems) |
| Ergative–Absolutive alignment | — | Alignment grouping S = P $\neq$ A | [§2](02_case_systems.md#sec:case-systems) |
| Expansion | $1 \to a \cdot a^l$ | Pregroup expansion introducing an adjoint pair | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Fluid-S | — | Alignment in which S marking varies by context or volition | [§2](02_case_systems.md#sec:case-systems) |
| Fluid-S functor | $F_\theta$ | Context-dependent alignment functor parameterized by a volition feature $\theta$ | [§2](02_case_systems.md#sec:case-systems) |
| Functors (Alignment) | $F_{\text{acc}}, F_{\text{erg}}$ | Alignment functors $\mathcal{U} \to \mathcal{L}_{\text{acc}}$ resp.\ $\mathcal{U} \to \mathcal{L}_{\text{erg}}$ | [§2](02_case_systems.md#sec:case-systems) |
| Language-specific case category | $\mathcal{L}_{\text{acc}}, \mathcal{L}_{\text{erg}}$ | Codomain categories for accusative vs.\ ergative alignment functors | [§2](02_case_systems.md#sec:case-systems) |
| Genitive | GEN | Case role encoding possessor or source | [§2](02_case_systems.md#sec:case-systems) |
| Formal semantics | — | Montague's programme: meaning assigned compositionally via truth-conditional functions | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Grammatical relation | — | Morphism in a case category relating two case roles | [§2](02_case_systems.md#sec:case-systems) |
| Instrumental | INS | Case role encoding instrument or means | [§2](02_case_systems.md#sec:case-systems) |
| Kāraka | — | Pāṇini's system of deep semantic roles in Sanskrit grammar | [§2](02_case_systems.md#sec:case-systems) |
| Left adjoint | $a^l$ | Left adjoint type satisfying $a^l \cdot a \leq 1$ | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Locative | LOC | Case role encoding location or context | [§2](02_case_systems.md#sec:case-systems) |
| Markedness | — | Asymmetry in the formal complexity of paradigmatic oppositions | [§2](02_case_systems.md#sec:case-systems) |
| Monadic semantics | — | Song's extension using monads to model sublexical verb-root decomposition | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Nominative | NOM | Case role encoding agent, experiencer, or intransitive subject | [§2](02_case_systems.md#sec:case-systems) |
| Nominative–Accusative alignment | — | Alignment grouping S = A $\neq$ P | [§2](02_case_systems.md#sec:case-systems) |
| Passivization | — | Syntactic transformation promoting patient to subject position | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Patient-like argument | P | The patient-like argument of a transitive clause | [§2](02_case_systems.md#sec:case-systems) |
| Pregroup grammar | — | Grammar where types have left and right adjoints forming a compact closed category | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Proto-Agent | — | Dowty's cluster of agentive entailments (volition, sentience, causation) | [§2](02_case_systems.md#sec:case-systems) |
| Proto-Patient | — | Dowty's cluster of patient entailments (change of state, causal affectedness) | [§2](02_case_systems.md#sec:case-systems) |
| Right adjoint | $a^r$ | Right adjoint type satisfying $a \cdot a^r \leq 1$ | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Sole argument | S | The sole argument of an intransitive clause | [§2](02_case_systems.md#sec:case-systems) |
| Thematic role | — | Semantic relation between a predicate and its argument (Agent, Patient, Goal, etc.) | [§2](02_case_systems.md#sec:case-systems) |
| Tripartite alignment | — | Alignment in which S $\neq$ A $\neq$ P (all three distinguished) | [§2](02_case_systems.md#sec:case-systems) |
| Verb root decomposition | — | Analysis of a verb's internal causative and result-state layers via a monad | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Vocative | VOC | Case role encoding direct address | [§2](02_case_systems.md#sec:case-systems) |

## Category Theory {#sec:notation-category}

Table: Category theory terminology and symbols. {#tbl:not-category}

| Term | Symbol | Definition | First Use |
| :------------ | :----: | :-------------------------------------------------------------- | :----: |
| Box | — | Node in a string diagram representing a morphism | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Cap | $\eta: 1 \to a^r \otimes a$ | Unit of a compact closure (coevaluation map) | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Category | $\mathcal{C}$ | Collection of objects and morphisms with identity and associative composition | [§2](02_case_systems.md#sec:case-systems) |
| Classifying topos | $\mathcal{E}_{\mathbb{T}}$ | Canonical topos: models of $\mathbb{T}$ in a Grothendieck topos $\mathcal{F}$ correspond to geometric morphisms $\mathcal{F} \to \mathcal{E}_{\mathbb{T}}$ | [§6](06_topos_theory.md#sec:topos-theory) |
| Codomain | $\text{cod}(f)$ | Target object of a morphism $f$ | [§2](02_case_systems.md#sec:case-systems) |
| Commutative diagram | — | Diagram in which all directed paths with the same start and end yield equal composites | [§1](01_introduction.md#sec:introduction) |
| Cobordism | — | Manifold with boundary connecting two lower-dimensional manifolds; domain of TQFT functors | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Compact closed category | — | Monoidal category in which every object has a left and right dual | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Composition | $g \circ f$ | Sequential application of morphisms: first $f$, then $g$ | [§2](02_case_systems.md#sec:case-systems) |
| Cup | $\varepsilon: a \otimes a^r \to 1$ | Counit of a compact closure (evaluation map) | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Diagram | $D$ | DisCoPy representation of a morphism in a monoidal category | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| $\dagger$-compact closed category | — | Compact closed category with a contravariant involutive endofunctor $\dagger$; framework for ZX-calculus | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Domain | $\text{dom}(f)$ | Source object of a morphism $f$ | [§2](02_case_systems.md#sec:case-systems) |
| Fiber bundle | — | Projection $\pi: E \to B$ whose fibers carry role-filler structure; topos-theoretic LoT model | [§6](06_topos_theory.md#sec:topos-theory) |
| Functor | $F: \mathcal{C} \to \mathcal{D}$ | Structure-preserving map between categories | [§2](02_case_systems.md#sec:case-systems) |
| Geometric theory | $\mathbb{T}$ | Theory axiomatized by sequents with finite conjunctions, arbitrary disjunctions, existential quantification | [§6](06_topos_theory.md#sec:topos-theory) |
| Geometric theories (case) | $\mathbb{T}_{\text{typ}}, \mathbb{T}_{\text{log}}, \mathbb{T}_{\text{dist}}, \mathbb{T}_{\text{enr}}$ | Typological, type-logical, distributional (DisCoCat), and enriched case theories (\autoref{sec:topos-theory}) | [§6](06_topos_theory.md#sec:topos-theory) |
| Bridge topos | $\mathcal{E}_{\mathbb{T}_{\text{bridge}}}$ (schematic) | Intermediate classifying topos linking two formalizations in the Morita bridge programme | [§6](06_topos_theory.md#sec:topos-theory) |
| Identity morphism | $\text{id}_A$ | Morphism from $A$ to itself satisfying $f \circ \text{id} = f = \text{id} \circ f$ | [§2](02_case_systems.md#sec:case-systems) |
| Monad | — | Endofunctor with unit and multiplication satisfying associativity and unit laws | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Monoidal category | — | Category with a bifunctor $\otimes$ (tensor product) and unit object $I$ | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Morita equivalence | $\mathcal{E}_{\mathbb{T}_1} \simeq \mathcal{E}_{\mathbb{T}_2}$ | Equivalence of classifying toposes enabling inter-theoretic transfer | [§6](06_topos_theory.md#sec:topos-theory) |
| Morphism | $f: A \to B$ | Arrow between objects in a category; encodes a relation or transformation | [§2](02_case_systems.md#sec:case-systems) |
| Natural transformation | $\alpha: F \Rightarrow G$ | Family of morphisms $\alpha_A: F(A) \to G(A)$ commuting with all morphisms; alignment maps in semantics use $\nu_{\text{acc}}, \nu_{\text{erg}}$; compact-closure cap $\eta_{\mathrm{cc}}$ is distinct from IQN curvature $\eta_{\mathrm{IQN}}$ | [§2](02_case_systems.md#sec:case-systems) |
| Object | $A, B, \ldots$ | Entities in a category; in our framework, case roles | [§2](02_case_systems.md#sec:case-systems) |
| Presheaf | $\hat{\mathcal{C}} = [\mathcal{C}^{op}, \textbf{Set}]$ | Contravariant functor from $\mathcal{C}$ to **Set** | [§6](06_topos_theory.md#sec:topos-theory) |
| Snake equation | $(1 \otimes \varepsilon) \circ (\eta \otimes 1) = 1$ | Zigzag identity: fundamental axiom of compact closed categories | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| String diagram | — | Planar graph faithfully representing morphisms in a monoidal category | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Subobject classifier | $\Omega$ | Object in a topos playing the role of a truth-value object | [§6](06_topos_theory.md#sec:topos-theory) |
| Swap | $\sigma_{A,B}: A \otimes B \to B \otimes A$ | Braiding morphism permuting two objects in a symmetric monoidal category | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Tensor product | $A \otimes B$ | Monoidal product representing parallel composition or concatenation | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Topos | $\mathcal{E}$ | Category with products, exponentials, and a subobject classifier; generalized universe of sets | [§6](06_topos_theory.md#sec:topos-theory) |
| Universal construction | — | Object or morphism characterized by a universal property (product, coproduct, limit) | [§6](06_topos_theory.md#sec:topos-theory) |
| Wire | — | Edge in a string diagram representing a type (object) | [§3](03_categorial_grammar.md#sec:categorial-grammar) |

## Enriched Categories and Magnitude {#sec:notation-enriched}

Table: Enriched categories and magnitude terminology. {#tbl:not-enriched}

| Term | Symbol | Definition | First Use |
| :------------ | :----: | :-------------------------------------------------------------- | :----: |
| Base-change functor | — | Conceptual tower $\mathbf{Bool} \hookrightarrow [0,1] \hookrightarrow \mathbf{R}_{\geq 0}$ showing progressively richer enrichments of grammatical categories (not computationally instantiated; this paper implements only $[0,1]$-enrichment) | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Categorical magnitude | $\lvert X \rvert$ | Sum $\sum_i w_i$ where $(w_1, \ldots, w_n)$ solves $Z \mathbf{w} = \mathbf{1}$; measures effective number of objects | [§5](05_enriched_categories.md#sec:enriched-categories) |
| Composition inequality | $\mathcal{V}(A,B) \cdot \mathcal{V}(B,C) \leq \mathcal{V}(A,C)$ | Enriched analogue of composition on $([0,1], \cdot, 1)$: composite hom-value is at least the product of intermediates | [§5](05_enriched_categories.md#sec:enriched-categories) |
| Enriched category | $\mathcal{V}\text{-Cat}$ | Category whose hom-sets are replaced by objects of a monoidal category $\mathcal{V}$ | [§5](05_enriched_categories.md#sec:enriched-categories) |
| Enriched functor | — | Structure-preserving map between enriched categories respecting hom-values | [§5](05_enriched_categories.md#sec:enriched-categories) |
| Hom-value | $\mathcal{V}(A,B) \in [0,1]$ | Enriched analogue of hom-set; measures degree of relation between objects | [§5](05_enriched_categories.md#sec:enriched-categories) |
| Identity axiom | $\mathcal{V}(A,A) = 1$ | Every object has maximal self-relatedness in the enriched hom (equality, not mere inequality, in our $[0,1]$-convention) | [§5](05_enriched_categories.md#sec:enriched-categories) |
| Similarity matrix | $Z_{ij} = \mathcal{V}(A_i, A_j)$ | Matrix of all pairwise hom-values; used to compute categorical magnitude | [§5](05_enriched_categories.md#sec:enriched-categories) |
| Lawvere metric space | — | Category enriched over $([0,\infty], +, 0)$; generalizes metric spaces via enriched categories | [§5](05_enriched_categories.md#sec:enriched-categories) |
| Magnitude homology | $\text{MH}_n(\mathcal{C})$ | Graded homological invariant categorifying magnitude; detects higher-dimensional holes in enriched categories | [§5](05_enriched_categories.md#sec:enriched-categories) |
| Morphism weight (precision) | $w_f$, $w_k$, $w_c$ | Enriched weights in $[0,1]$; subscript denotes morphism or role in VMP/DPE (\autoref{sec:daif-results}). **Convention**: $w_f$ always refers to the *enriched* hom-value $\mathcal{C}(A,B)$ in the $[0,1]$-enriched category ([§5](05_enriched_categories.md#sec:enriched-categories)), not the unit-weight morphism scalar carried by the `CaseCategory` in [§2](02_case_systems.md#sec:case-systems) — the two number systems are intentionally decoupled in the implementation (see [§5](05_enriched_categories.md#sec:enriched-categories) Architectural note). | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| POVM element | $E_c$ | Positive operator-valued measure element for case role $c$; $P(c \mid \rho) = \text{Tr}(E_c \rho)$ | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Prediction error | $\text{PE}(f)$ | $\propto w_f \cdot \lvert\mu_{\text{predicted}} - \mu_{\text{observed}}\rvert$; case violation signal scaling with morphism weight | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Shannon entropy | $H$ | Information-theoretic measure characterized as the unique derivation of a topological operad (Bradley) | [§5](05_enriched_categories.md#sec:enriched-categories) |
| Topological operad | — | Operad with topological structure whose derivations connect magnitude to entropy | [§5](05_enriched_categories.md#sec:enriched-categories) |
| Weight vector | $\mathbf{w}$ | Solution to $Z\mathbf{w} = \mathbf{1}$; entries are the effective weights of each object | [§5](05_enriched_categories.md#sec:enriched-categories) |

## Distributional Semantics and LLMs {#sec:notation-distributional}

Table: Distributional semantics and LLM terminology. {#tbl:not-distributional}

| Term | Symbol | Definition | First Use |
| :------------ | :----: | :-------------------------------------------------------------- | :----: |
| Attention mechanism | — | Transformer component computing weighted relevance between token positions | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Attention weight | $\alpha_{ij}$ | Softmax-normalized score encoding contextual relevance of token $j$ to token $i$ | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| BERT | — | Bidirectional Encoder Representations from Transformers; masked language model producing contextualized embeddings | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Contextualized embedding | $\mathbf{v}_w^{(c)}$ | Vector representation of word $w$ that varies with linguistic context $c$ | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Compact closure map | $\varepsilon_N: N \otimes N \to \mathbb{R}$ | Inner product implementing pregroup contraction in the vector space semantics | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Cosine similarity | $\cos(\mathbf{u}, \mathbf{v})$ | Similarity measure $\frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$ between vectors | [§5](05_enriched_categories.md#sec:enriched-categories) |
| Distributional Memory | — | Baroni–Lenci tensor-based framework structuring co-occurrence as (word, relation, word) triples | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| DisCoCat | — | Distributional Compositional Categorical model; monoidal functor from pregroup grammars to vector spaces | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| DisCoCirc | — | Discourse-level extension of DisCoCat with persistent entity wires | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Distributional hypothesis | — | The thesis that words occurring in similar contexts have similar meanings (Harris 1954, Firth 1957) | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| GloVe | — | Global Vectors for Word Representation; log-bilinear model of word co-occurrence statistics | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| GPT | — | Generative Pre-trained Transformer; autoregressive language model | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Meaning functor | $F: \mathbf{Preg} \to \mathbf{FVect}$ | Monoidal functor assigning vector spaces to types and linear maps to derivations | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Noun space | $N$ | Vector space to which noun types $n$ map under the meaning functor | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Parameterized optic | — | Categorical construction (Gavranović) modeling attention heads as functorial lenses | [§9](09_ai_implications.md#sec:ai-implications) |
| Self-attention | $\text{Attn}(Q,K,V) = \mathrm{softmax}(\frac{QK^\top}{\sqrt{d_k}})V$ | Core transformer operation computing contextualized representations | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Sentence space | $S$ | Vector space to which sentence type $s$ maps under the meaning functor | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Sentence vector | $\overrightarrow{\text{sentence}}$ | Vector in $S$ computed by tensoring and contracting word meanings via DisCoCat | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Static embedding | $\mathbf{v}_w$ | Fixed vector representation of word $w$ independent of context (e.g., Word2Vec, GloVe) | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Transformer | — | Neural architecture using self-attention and feed-forward layers for sequence processing | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Word2Vec | — | Neural embedding model (Mikolov et al. 2013) learning word vectors from local context windows | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Word vector | $\mathbf{v}_w \in \mathbb{R}^d$ | $d$-dimensional real-valued vector encoding distributional properties of word $w$ | [§4](04_categorical_semantics.md#sec:categorical-semantics) |

## Distributional Active Inference (DAIF) {#sec:notation-daif}

Table: Distributional Active Inference (DAIF) terminology. {#tbl:not-daif}

| Term | Symbol | Definition | First Use |
| :------------ | :----: | :-------------------------------------------------------------- | :----: |
| Return distribution | $Z(s,a)$ | Full probability distribution over discounted cumulative rewards from state $s$ under action $a$ | [§7c](07c_daif_results.md#sec:daif-results) |
| Distributional Bellman operator | $\mathcal{T}^{\pi}$ | Distributional analogue of the Bellman operator: $\mathcal{T}^{\pi}Z \stackrel{d}{=} R + \gamma Z'$ | [§7c](07c_daif_results.md#sec:daif-results) |
| Push-forward measure | $\mathbf{S}_{\#}\mathbb{P}$ | Path-level push-forward of the trajectory measure (composed with decoder $f: \mathcal{S} \to \mathcal{X}$ in \autoref{eq:eq-7-1}); generic push-forward written $T_{\#}\mu$ | [§7c](07c_daif_results.md#sec:daif-results) |
| Discount factor | $\gamma \in (0,1)$ | Exponential time-discount in the distributional Bellman return | [§7c](07c_daif_results.md#sec:daif-results) |
| Quantile level | $\tau \in [0,1]$ | Quantile index in QR-DQN and IQN; sampled uniformly at inference time | [§7c](07c_daif_results.md#sec:daif-results) |
| Quantile Huber loss | $\rho_{\tau}^{\kappa}{(u)}$ | Loss function for quantile regression: interpolates $L^1$ and $L^2$ via threshold $\kappa{}$ | [§7c](07c_daif_results.md#sec:daif-results) |
| Wasserstein distance | $W_p(P,Q)$ | $p$-Wasserstein distance between return distributions; $W_1$ = area between CDFs | [§7c](07c_daif_results.md#sec:daif-results) |
| Bethe free energy | $F_{\text{Bethe}}[\mathbf{q}]$ | Tractable approximation to variational free energy in belief propagation | [§7c](07c_daif_results.md#sec:daif-results) |
| Expected information gain | $\text{EIG}{(o)}$ | $D_{\mathrm{KL}}{(q{(\mathbf{c} \mid o)} \Vert p{(\mathbf{c})})}$; epistemic value of observation $o{}$ | [§7c](07c_daif_results.md#sec:daif-results) |
| Expected free energy | $G{(\pi)}$ | Pragmatic + epistemic + risk cost of policy $\pi{}$; minimised for action selection | [§7c](07c_daif_results.md#sec:daif-results) |
| Distributional prediction error | $\mathrm{DPE}$ | Precision-weighted Wasserstein mismatch: $w_f \cdot W_1{(Z_{\text{pred}}, Z_{\text{obs}})}$ | [§7c](07c_daif_results.md#sec:daif-results) |
| ERP amplitude profile | $\mathrm{ERPProfile}$ | Dataclass holding N400/P600 amplitudes, peak latencies, and time-series waveforms for each case role | [§7c](07c_daif_results.md#sec:daif-results) |
| Return entropy | $H[Z]$ | Shannon entropy of the return distribution: $-\sum_i p_i \log p_i$ | [§7c](07c_daif_results.md#sec:daif-results) |
| Quantile calibration error | $\mathrm{CE}$ | Mean absolute deviation between nominal quantile levels and empirical coverage | [§7c](07c_daif_results.md#sec:daif-results) |
| IQN risk distortion | $\psi_{\mathrm{IQN}}(\tau)$ | Maps quantile levels $\tau{}$; piecewise formulas (neutral, power, tail, CVaR) match `implicit_quantile_network_update()` and the [§7c](07c_daif_results.md#sec:daif-results) table; distinct from $\beta_{\mathrm{risk}}$ in $G(\pi)$ | [§7c](07c_daif_results.md#sec:daif-results) |
| IQN curvature | $\eta_{\mathrm{IQN}}$ | Default $0.71$ in code; not the compact-closure cap $\eta_{\mathrm{cc}}$ | [§7c](07c_daif_results.md#sec:daif-results) |
| CVaR scale | $\alpha_{\mathrm{CVaR}}$ | IQN mode uses $\psi_{\mathrm{IQN}}(\tau)=\tau\cdot\alpha_{\mathrm{CVaR}}$; default $0.25$ in code (distinct from softmax $\alpha_{\mathrm{pol}}$) | [§7c](07c_daif_results.md#sec:daif-results) |
| Risk sensitivity (EFE) | $\beta_{\mathrm{risk}}$ | Non-negative coefficient on $\text{risk}(\pi)$ in $G(\pi)$; $\beta_{\mathrm{risk}}=0$ recovers standard EFE | [§7c](07c_daif_results.md#sec:daif-results) |
| Inverse temperature (policy) | $\alpha_{\mathrm{pol}}$ | Softmax sharpness over policies in $P(\pi)$ | [§7c](07c_daif_results.md#sec:daif-results) |
| Belief precision (VMP) | $\Lambda_{\text{post}}, \Lambda_{\text{prior}}, \Lambda_{\text{lik}}$ | Posterior, prior, and likelihood precision matrices; $\Delta\Lambda$ is their positive update magnitude | [§7c](07c_daif_results.md#sec:daif-results) |
| Violation severity | $S_{\text{violation}}$ | $\in \{0, 0.5, 1.0\}$ in ERP decomposition | [§7c](07c_daif_results.md#sec:daif-results) |
| TD error (quantile) | $\delta_{ij}$ | Temporal-difference residual in QR-DQN (\autoref{eq:eq-7c-qr}) | [§7c](07c_daif_results.md#sec:daif-results) |
| Quantile count (current) | $N$ | Number of current-network quantile levels in QR-DQN (Eq. \ref{eq:eq-7c-qr}); equal to the length of `current_quantiles` passed to `quantile_td_update()` | [§7c](07c_daif_results.md#sec:daif-results) |
| Quantile count (target) | $N'$ | Number of target-network quantile samples in QR-DQN (Eq. \ref{eq:eq-7c-qr}) | [§7c](07c_daif_results.md#sec:daif-results) |
| Huber threshold | $\kappa$ | Cut-point between quadratic and linear regimes of the Huber loss $L_\kappa(u)$ (Eq. \ref{eq:eq-7c-huber}); default $\kappa=1$ in `quantile_td_update()` | [§7c](07c_daif_results.md#sec:daif-results) |
| Atom count (C51) | $N_{\text{atoms}}$ | Number of support atoms $z_i$ in the C51 categorical representation (Eq. \ref{eq:eq-7c-c51}); default $N_{\text{atoms}}=51$ in `categorical_return_distribution()` | [§7c](07c_daif_results.md#sec:daif-results) |
| Support bounds (C51) | $V_{\min},\,V_{\max}$ | Lower and upper endpoints of the atomic support spanned by $\{z_i\}$ in the C51 representation | [§7c](07c_daif_results.md#sec:daif-results) |
| Bin count (entropy) | $N_{\text{bins}}$ | Number of equal-width bins used to discretise the quantile-parameterised return when computing $H[Z]$ (Eq. \ref{eq:eq-7c-entropy}); default $N_{\text{bins}}=50$ in `return_distribution_entropy()` | [§7c](07c_daif_results.md#sec:daif-results) |

## Active Inference and Cognitive Models {#sec:notation-cognitive}

Table: Active inference and cognitive modeling terminology. {#tbl:not-cognitive}

| Term | Symbol | Definition | First Use |
| :------------ | :----: | :-------------------------------------------------------------- | :----: |
| Active inference | — | Framework in which perception and action are unified as variational free energy minimization | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Active sampling | — | Agent's selection of actions to confirm or update case assignments via sensory evidence | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Belief updating | — | Bayesian posterior computation: revising generative model parameters given new observations | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| CEREBRUM | — | Case-Enabled Reasoning Engine with Bayesian Representations for Unified Modeling; treats AI models as case-bearing entities | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Distributional Active Inference (DAIF) | — | Extension replacing scalar value summaries with full return distributions in active inference | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Distributional RL | — | Reinforcement learning operating on full return distributions rather than scalar expected values | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Free energy | $F$ | Variational bound on surprisal; $F = D_{KL}[q(\theta) \parallel p(\theta \mid o)] - \ln p(o)$ | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Free energy principle (FEP) | — | The principle that self-organizing systems maintain themselves by minimizing surprisal | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Garden-path reanalysis | — | Restructuring of case assignments when incoming evidence contradicts the current parse | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Generative model | $p(o, s)$ | Joint probability model over observations $o$ and hidden states $s$ | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Markov blanket | — | Statistical boundary separating internal states from external environment; defines agent boundary | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| N400 | — | Event-related brain potential peaking ~400ms post-stimulus; indexes semantic prediction error | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| P600 | — | Event-related brain potential peaking ~600ms post-stimulus; indexes syntactic prediction error | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Perceptual inference | — | Updating internal beliefs to better predict current observations (reduce prediction error) | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Precision weighting | — | Weighting of prediction errors by inverse variance; enriched morphism weights serve this role | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Prediction error | $\varepsilon$ | Difference between predicted and observed sensory input; drives belief updating | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| ROSE model | — | Murphy's Representation–Operation–Structure–Encoding architecture; cross-frequency phase-amplitude coupling (PAC) linking biolinguistic syntax (slow oscillatory phase) to neuropragmatic inference (fast gamma); the neural-timescale bridge of Pillar 6 | [§1](01_introduction.md#sec:introduction), [§7c](07c_daif_results.md#sec:daif-results) |
| S-HAI | — | Schema-Based Hierarchical Active Inference; dual-level POMDP connecting abstract relational schemas (Level 2: case diagram structure) to sensorimotor surface parsing (Level 1) | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Push-forward (general) | $T_{\#}\mu$ | Image of a measure $\mu$ under a measurable map $T$; DAIF-specific notation in \autoref{sec:notation-daif} | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Situation semantics | — | Framework representing meaning as relations between situations (Barwise and Perry 1983) | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Surprisal | $-\ln p(o)$ | Negative log-probability of an observation under the generative model | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Variational free energy | $F[q]$ | Functional upper bound on surprisal minimized by approximate posterior $q$ | [§7](07_cognitive_integration.md#sec:cognitive-integration) |

## Quantum and Topological Terms {#sec:notation-quantum}

Table: Quantum and topological terminology. {#tbl:not-quantum}

| Term | Symbol | Definition | First Use |
| :------------ | :----: | :-------------------------------------------------------------- | :----: |
| Amplituhedron | — | Positive geometry encoding scattering amplitudes; connected to TQNN execution traces | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Barren plateau | — | Vanishing gradient phenomenon in PQC training; gradients decay exponentially in system size for certain ansätze | [§4b](04b_compact_closure_complexity.md#sec:compact-closure-complexity) |
| $\dagger$-compact category | — | See $\dagger$-compact closed category in [Category Theory](11b_notation.md#sec:notation-category) | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| CPTP map | — | Completely Positive Trace-Preserving map; quantum channel between Hilbert spaces | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Density operator | $\rho$ | Positive semidefinite trace-one operator encoding a quantum (or semantic) state | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Execution trace | — | Record of operations in a quantum computation; connects TQNNs to amplituhedra | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Generalized flow | — | Graph-theoretic property ensuring deterministic circuit extraction from ZX-diagrams | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Hadamard box | $H$ | ZX-calculus element implementing the Hadamard gate; converts between Z and X bases | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Holographic screen | — | Information boundary between interacting quantum systems carrying a qubit array | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Parameterized quantum circuit (PQC) | — | Quantum circuit with trainable angle parameters; the computational substrate of QNLP and case-category implementations | [§4b](04b_compact_closure_complexity.md#sec:compact-closure-complexity) |
| IQP ansatz | — | Instantaneous Quantum Polynomial-time circuit: default lambeq PQC ansatz for noun and verb boxes | [§4b](04b_compact_closure_complexity.md#sec:compact-closure-complexity) |
| Sim4 ansatz | — | Strongly entangling layer PQC ansatz used for discourse-level lambeq Gen II circuits | [§4c](04c_discourse_complexity.md#sec:discocirc-discourse) |
| Pointer state | — | Preferred quantum state selected by a QRF; determines the measurement basis | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Quantum contextuality | — | Quantum correlations that reduce cohomological obstructions to semantic alignment | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Quantum discord | — | Quantum correlation measure equal to integrated semantic information in sheaf framework | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Quantum key distribution (QKD) | — | Protocol providing information-theoretic security for quantum communication channels | [§9](09_ai_implications.md#sec:ai-implications) |
| Quantum reference frame (QRF) | — | Observer-relative frame selecting pointer states and inducing decoherence | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Semantic Hilbert space | $H_v$ | The finite-dimensional semantic Hilbert space carried at vertex $v$ in a quantum semantic sheaf | [§8b](08b_quantum_semantics.md#sec:quantum-semantics) |
| Quantum semantic sheaf | $(H, F, \rho)$ | Triple of Hilbert spaces, CPTP channels, and density operators over a communication graph | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Reshetikhin–Turaev invariant | — | Topological invariant assigning to a ribbon graph a linear map via TQFT | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Sheaf cohomology | $H^n(\mathcal{F})$ | Cohomological obstruction classes governing alignment in a quantum semantic sheaf | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Spin-network | — | Graph with edges labeled by representations and vertices by intertwiners; TQFT data | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Spider | — | Elementary ZX-diagram node (Z-spider or X-spider) representing a quantum operation | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| TQFT | — | Topological Quantum Field Theory; functor from cobordisms to Hilbert spaces | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| TQNN | — | Topological Quantum Neural Network; QNN reformulated via spin-networks and TQFT | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| Turaev–Viro invariant | — | State-sum TQFT invariant; implements quantum error-correcting codes in TQNNs | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| ZX-calculus | — | Graphical language for quantum circuits using Z-spiders, X-spiders, and Hadamard boxes | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| ZX-diagram | — | String diagram in a $\dagger$-compact closed category representing a quantum process | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |
| ZX rewrite rule | — | Graph-theoretic transformation preserving the semantics (linear map) of a ZX-diagram | [§8](08_quantum_active_inference.md#sec:quantum-active-inference) |

## Logical and Type-Theoretic Terms {#sec:notation-logical}

Table: Logical and type-theoretic terminology. {#tbl:not-logical}

| Term | Symbol | Definition | First Use |
| :------------ | :----: | :-------------------------------------------------------------- | :----: |
| $\beta\text{-reduction}$ | — | Computational reduction step in $\lambda\text{-calculus}$; corresponds to cut elimination in proofs | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Church–Rosser property | — | Confluence of $\beta\text{-reduction}$: all reduction sequences converge to the same normal form | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Curry–Howard isomorphism | — | Correspondence between proofs and programs, propositions and types | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Cut elimination | — | Proof normalization procedure removing intermediate lemmas; corresponds to $\beta\text{-reduction}$ | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Graded type theory | — | Extension of type theory tracking effects (e.g., evidentiality) via graded modalities | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Lambek calculus | — | Non-commutative intuitionistic linear logic for syntactic type assignment | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Left residual | $A \backslash B$ | Type of an expression that, given $A$ to the left, produces $B$ | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Residuation law | $A \otimes B \leq C \iff A \leq C / B \iff B \leq A \backslash C$ | Fundamental axiom connecting the three connectives of the Lambek calculus | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Right residual | $B / A$ | Type of an expression that, given $A$ to the right, produces $B$ | [§3](03_categorial_grammar.md#sec:categorial-grammar) |

## AI and Communication Protocols {#sec:notation-ai}

Table: AI and communication protocol terminology. {#tbl:not-ai-protocols}

| Term | Symbol | Definition | First Use |
| :------------ | :----: | :-------------------------------------------------------------- | :----: |
| A2A Protocol | — | Google's Agent-to-Agent protocol for cross-framework agent communication via HTTP/JSON-RPC | [§9](09_ai_implications.md#sec:ai-implications) |
| ACP | — | Agent Communication Protocol; standardizes messaging formats across agents, apps, and humans | [§9](09_ai_implications.md#sec:ai-implications) |
| ANP | — | Agent Network Protocol; three-layer architecture for trusted distributed agent interaction | [§9](09_ai_implications.md#sec:ai-implications) |
| Categorical deep learning | — | Deep learning approached through the lens of category theory (Gavranović et al.) | [§9](09_ai_implications.md#sec:ai-implications) |
| Double Categorical Systems Theory (DCST) | — | Framework using 2-categories (horizontal + vertical composition) for explainable autonomous AI | [§9](09_ai_implications.md#sec:ai-implications) |
| Functorial encryption | — | Semantic cryptography: applying a secret functor to map plaintext categories into ciphertext categories | [§9](09_ai_implications.md#sec:ai-implications) |
| lambeq | — | Quantum Natural Language Processing pipeline compiling DisCoCat diagrams to quantum circuits | [§9](09_ai_implications.md#sec:ai-implications) |
| MCP | — | Model Context Protocol; standardizes how AI agents access external tools and data sources | [§9](09_ai_implications.md#sec:ai-implications) |
| Parameterized optics / lenses | — | Categorical constructions modeling neural network components (Gavranović); attention heads as optics | [§9](09_ai_implications.md#sec:ai-implications) |
| QNLP | — | Quantum Natural Language Processing; quantum computation on DisCoCat sentence diagrams | [§9](09_ai_implications.md#sec:ai-implications) |
| Role variables | $X_{\text{NOM}}, X_{\text{ACC}}, \ldots$ | Agentic components structured by case roles in networked LLM contexts (e.g., active requester policy) | [§9](09_ai_implications.md#sec:ai-implications) |
| Semantic cryptography | — | Encrypting compositional meaning structures (functorial encryption, diagram obfuscation, weight masking) | [§9](09_ai_implications.md#sec:ai-implications) |
| Protocol category | $\mathcal{C}_{\text{protocol}}$ | Category whose morphisms are licensed interaction steps in the case-theoretic firewall (\autoref{sec:cognitive-security}) | [§9b](09b_cognitive_security.md#sec:cognitive-security) |
| Adversarial morphism | $\phi{}$ | Illicit map attempting case-role promotion (e.g. ACC$\to$NOM) in injection attacks | [§9b](09b_cognitive_security.md#sec:cognitive-security) |
| Access Collapse | — | Catastrophic boundary failure where adversarial text traverses from passive data (ACC) to active instruction (NOM) without structural constraint | [§9b](09b_cognitive_security.md#sec:cognitive-security) |
| Case-theoretic firewall | — | Type-checking system enforcing licensed morphism constraints at agent communication boundaries; detects illicit role promotions in $\text{Mor}(\mathcal{C}_{\text{protocol}})$ | [§9b](09b_cognitive_security.md#sec:cognitive-security) |
| Prompt injection | — | Attack illicitly promoting user-supplied data from ACC (patient) to NOM (commanding agent); structurally a type violation in the interaction grammar | [§9b](09b_cognitive_security.md#sec:cognitive-security) |
| Symbolic Isolation | — | Property ensuring ACC-typed data wires cannot fuse with NOM-typed command wires; enforced by the non-cartesian fragment of the monoidal structure | [§9b](09b_cognitive_security.md#sec:cognitive-security) |

## Diagrammatic Reasoning {#sec:notation-diagrammatic}

Table: Diagrammatic reasoning terminology. {#tbl:not-diagrammatic}

| Term | Symbol | Definition | First Use |
| :------------ | :----: | :-------------------------------------------------------------- | :----: |
| Categorical complexity | $\kappa(D)$ | Complexity metric for diagram $D$ derived from box counts, cup counts, and swap depths | [§4b](04b_compact_closure_complexity.md#sec:compact-closure-complexity) |
| Cognitively privileged representation | — | Representation format that leverages perceptual and spatial cognition for inference | [§1](01_introduction.md#sec:introduction) |
| Diagram depth | — | Length of the longest input-to-output path through boxes; measures derivational complexity | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Existential graphs | — | Peirce's graphical logic system conducting first-order logic entirely diagrammatically | [§7](07_cognitive_integration.md#sec:cognitive-integration) |
| Free ride | — | Shimojima's term: information extracted from a diagram without explicit inference steps | [§1](01_introduction.md#sec:introduction) |
| Hybrid reasoning | — | Giardino's term: reasoning combining perceptual pattern recognition with theoretical knowledge | [§1](01_introduction.md#sec:introduction) |
| Inferential instrument | — | Manders's term: a diagram whose spatial properties encode proof-relevant information | [§6](06_topos_theory.md#sec:topos-theory) |
| Joyal–Street theorem | — | Soundness and completeness of string-diagrammatic reasoning for monoidal categories | [§3](03_categorial_grammar.md#sec:categorial-grammar) |
| Normal form | $D_{\text{nf}}$ | Canonical form of a diagram obtained by rewriting; unique up to the axioms | [§4](04_categorical_semantics.md#sec:categorical-semantics) |
| Role colours (figures) | `CASE_COLORS` | `CaseRole` → display colour for generated figures; single source in `src/visualization/styles.py` | [§2](02_case_systems.md#sec:case-systems)–[§4](04_categorical_semantics.md#sec:categorical-semantics), [Appendix A](11_syntactic_sentence_diagrams.md#sec:syntactic-diagrams) |

## Notation Conventions {#sec:notation-conventions}

Table: General mathematical notation and manuscript conventions. {#tbl:not-conventions}

| Convention | Meaning |
| :-------- | :------------------------------------------------------------ |
| $\mathcal{C}, \mathcal{D}$ | Categories |
| $\mathcal{V}$ | Enrichment base (monoidal category, typically $([0,1], \cdot, 1)$) |
| $\mathcal{U}$ | Universal (maximal) case category |
| $\mathcal{L}$ | Language-specific case category |
| $\mathcal{E}_{\mathbb{T}}$ | Classifying topos of theory $\mathbb{T}$ |
| $f, g, h$ | Morphisms |
| $F, G$ | Functors |
| $\alpha{}$, $\beta{}$ | Natural transformations; functorial vertical composition (componentwise along objects) is standard ([§2](02_case_systems.md#sec:case-systems)). In DAIF, $\alpha_{\mathrm{pol}}$ is policy temperature; $\alpha_{\mathrm{CVaR}}$ is CVaR scale; $\beta_{\mathrm{risk}}$ is EFE risk weight; see [§7c](07c_daif_results.md#sec:daif-results) |
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
| $\mathbf{Ent}, \mathbf{Case}$ | Categories for Entities and Case Roles respectively in DisCoCirc discourse extensions |
| $\otimes$ | Tensor product (monoidal product, type concatenation) |
| $\circ$ | Composition of morphisms |
| $\Rightarrow$ | Natural transformation between functors |
| $\simeq$ | Categorical equivalence |
| $\leq$ | Preorder relation on types (derivability) |
| $\gamma{}$ | Discount factor in distributional RL return computation |
| $w \in [0,1]$ | Enriched morphism weight (proto-role satisfaction degree) |
| $\varepsilon$ | Sensory prediction error (active inference); $\varepsilon_n$ also denotes the compact-closure **counit** (cup) on type $n$ |
| $\eta_{\mathrm{cc}}$ | Compact closure **unit** (cap); IQN curvature uses $\eta_{\mathrm{IQN}}$ instead |
| $\epsilon$ | Small numerical floor (e.g.\ KL stabiliser, VMP convergence threshold); not the counit |
| $\rho{}$ | Density operator (quantum state) |
| $[@key]$ | Parenthetical citation |
| `[-@key]` | Suppress-author citation |
| `\autoref` (with `{sec:…}` / `{eq:…}` / `{fig:…}`) | LaTeX/Markdown automatic cross-reference to a labeled target |
| $Z(s,a)$ | Return distribution (DAIF); full distributional representation of returns |
| $G(\pi)$ | Expected free energy of policy (DAIF active inference) |
| $\tau{}$ | Quantile level in QR-DQN / IQN |
| $\psi_{\mathrm{IQN}}(\tau)$ | IQN risk distortion of quantile levels |
| $\beta_{\mathrm{risk}}$ | Risk-sensitivity coefficient in $G(\pi)$ |
| $\alpha_{\mathrm{pol}} \;;\; \alpha_{\mathrm{CVaR}}$ | Policy softmax temperature; CVaR tail level (IQN) |
| $w_f, w_k, w_c$ | Enriched morphism / role weights (precision on PE and VMP) |
| $\mathrm{DPE}$ | Distributional prediction error; precision-weighted Wasserstein mismatch |
| $H[Z]$ | Return distribution entropy |