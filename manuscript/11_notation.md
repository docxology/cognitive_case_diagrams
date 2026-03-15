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
