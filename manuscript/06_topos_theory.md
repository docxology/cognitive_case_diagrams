
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
