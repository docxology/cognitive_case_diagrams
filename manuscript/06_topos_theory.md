
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
