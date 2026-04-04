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
