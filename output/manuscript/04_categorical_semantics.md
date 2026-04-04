
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
