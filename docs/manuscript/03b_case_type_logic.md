# Case Subscripts, Passivization, and the Curry–Howard Proof {#sec:case-type-logic}

**Where we are in the argument.** \autoref{sec:categorial-grammar} installed pregroup syntax — cups, caps, and compact closure — as the algebraic backbone of composition. This chapter decorates that backbone with case information: every noun wire picks up a case subscript ($n_{\text{NOM}}$, $n_{\text{ACC}}$, …) so grammatical role becomes a first-class typed structure on wires, and passivization becomes a wire-level swap together with **case relabeling** (\autoref{eq:eq-3-3}/\autoref{eq:eq-3-4}) rather than an exception to the type system — the Curry–Howard image is a proof rewrite of that rearrangement.

Case-marked noun phrases receive compound types that encode both their grammatical role and their combinatory potential. For example, in a nominative–accusative language, the type assignment proceeds as follows (\autoref{tbl:pregroup-types}):

| Expression | Type | Gloss |
| :--- | :--- | :--- |
| "Alice" (subject) | $n_{\text{NOM}}$ | Noun, nominative-marked |
| "the ball" (object) | $n_{\text{ACC}}$ | Noun, accusative-marked |
| "kicks" | $(n_{\text{NOM}} \backslash s) / n_{\text{ACC}}$ | Seeks ACC right, NOM left |
| "to Bob" (recipient) | $(s \backslash s) / n_{\text{DAT}}$ | Modifies sentence via DAT argument |

Table: Case-marked pregroup type assignments for a standard nominative-accusative transitive clause. {#tbl:pregroup-types}

The specific subscripts structurally refine the base noun type $n$ with mandatory continuous case features, mathematically guaranteeing that the transitive verb "kicks" exclusively selects a nominative-marked subject and an accusative-marked object. Any feature mismatch automatically blocks the algebraic derivation, accurately modeling native ungrammaticality.

**Alignment and natural transformations.** Cross-linguistic alignment is modeled functorially in \autoref{sec:case-categories}: alignment types are structure-preserving functors from a universal role category to a language-specific case category, compared via natural transformations when one asks how two alignments cohere on the same underlying argument structure. At the level of case-marked pregroup types (this section), that functorial picture **suggests** treating agreement checks as naturality-style coherence constraints: the morphosyntactic alignment chosen for arguments must remain compatible with the verb's combinatorial requirements so that reductions still factor through the intended case-typed slots. We do not claim a full adjunction between identity and alignment functors in the pregroup category here; the precise categorical status of alignment is anchored in \autoref{sec:case-categories}, while the typed reductions below supply the concrete syntax.

## Syntactic Derivation as Proof, Case Assignment as Type Inference

A deep structural parallel underlies the Lambek calculus: derivations of syntactic types correspond to proofs in intuitionistic logic (via the Curry–Howard isomorphism), and therefore to programs in a typed lambda calculus, as summarized in \autoref{tbl:curry-howard}.

| Syntactic Domain | Logical Domain | Computational Domain |
| :--- | :--- | :--- |
| Types $(A / B, A \backslash B)$ | Propositions | Types |
| Derivations | Proofs | Programs ($\lambda\text{-terms}$) |
| Cut elimination | Proof normalization | $\beta\text{-reduction}$ |
| Commutativity of cuts | Confluence of rewriting | Church–Rosser property |

Table: The Curry–Howard isomorphism connecting syntactic, logical, and computational domains. {#tbl:curry-howard}

This foundational correspondence dictates two critical consequences for our cognitive framework:

1. **Semantic compositionality strictly follows syntactic well-formedness**: A successfully typed derivation automatically guarantees a well-formed geometric meaning representation (specifically, the exact $\lambda\text{-term}$ isolated and extracted directly from the formal proof).
2. **Case assignment reduces to type inference**: Dynamically determining the correct case for a noun phrase in context is computationally equivalent to inferring the type of an unknown variable in a $\lambda\text{-expression}$—thereby grounding case assignment in the well-understood algorithmic landscape of type inference (Hindley-Milner and its extensions).

## Song's Monadic Root Syntax: Sublexical Decomposition via Embedded Monads

Song [-@song2022act; -@song2022blog] significantly extends this categorial framework by deploying a novel **monadic semantics** for root syntax. He successfully models the sublexical decomposition of complex verb roots by embedding specialized monads directly into the base syntactic category. This computational approach captures the deep intuition that a seemingly simple verb like "break" harbors layered internal structure—specifically, an active causative layer tightly coupled to a passive result-state layer—which dynamically dictates subsequent case assignment. The formal monad elegantly encapsulates this tangled lexical complexity within one streamlined categorical construction, empowering the type-logical grammar to process lexical features and syntactic composition simultaneously and uniformly.

This monadic architecture seamlessly interfaces with modern graded type theory. For instance, Asudeh and Giorgolo [-@asudeh2020graded] previously developed a monadic semantics tracking evidentiality, deploying graded computational effects to quantify the shifting epistemic real-world status of various propositions. Our framework extends this exact pattern into the domain of morphological case, where the continuous "grade" attached to any specific morphism formally encodes the statistical strength and validity of that local semantic role assignment.

## Passivization Is a Swap: Voice Alternation as Topological Wire Crossing

Within categorical linguistics, **passivization** emerges as a uniquely revealing topological operation. Traditionally described as a syntactic rule that promotes the patient to subject position while (optionally) demoting the agent to an oblique role, passivization in our framework ceases to be an ad-hoc transformation; instead, it combines (i) a **Swap** morphism $\sigma_{A,B}: A \otimes B \to B \otimes A$ that crosses the noun wires feeding into the verb's pregroup derivation—so *which* noun meets the verb's left vs.\ right adjoint slots reverses relative to the active diagram—and (ii) **updated case features** on those wires: the promoted subject is $n_{\text{NOM}}$, not a carried-over $n_{\text{ACC}}$.

In a pregroup grammar, the active transitive "Alice chases Bob" has the type reduction:

\begin{equation}
n_{\text{NOM}} \cdot (n^r \cdot s \cdot n^l) \cdot n_{\text{ACC}} \to s
\label{eq:eq-3-3}
\end{equation}

For "Bob is chased by Alice," Bob is the grammatical subject ($n_{\text{NOM}}$) and Alice appears in the oblique *by*-phrase ($n_{\text{OBL}}$), with surface order subject--verb--oblique:

\begin{equation}
n_{\text{NOM}} \cdot (n^r \cdot s \cdot n^l) \cdot n_{\text{OBL}} \to s
\label{eq:eq-3-4}
\end{equation}

This is **not** the naive swap of subscripts in \eqref{eq:eq-3-3} (which would incorrectly leave the promoted patient typed as accusative). The DisCoPy `Swap` primitive makes the wire crossing explicit; the case-marked types in \eqref{eq:eq-3-4} match the figure and standard promotion/demotion. The generated passive diagram diverges from its active counterpart through that crossing together with the reassignment of which noun occupies each cup. This transforms abstract syntactic voice alternation into a highly visible, instantly readable topological feature embedded directly within the string diagram.

This diagrammatic transparency exemplifies Shimojima's [-@shimojima1996reasoning] free-ride inference capability. By inspecting the visual topology, a cognitive agent immediately verifies that passivization preserves the verb's inherent argument structure while rearranging its surface realization—a structural fact that typically requires chaining inference steps to algebraically establish within standard linear notation (\autoref{fig:discopy-passive}).

![Passivization as role reassignment in the DisCoPy pregroup diagram for "Bob is chased by Alice" with type $n_{\text{NOM}} \otimes (n^r \otimes s \otimes n^l) \otimes n_{\text{OBL}} \to s$. Bob's $n$ wire contracts into the verb's left adjoint $n^r$ via the left Cup ($n$--$n^r$) — promoting the semantic patient to grammatical subject — while Alice's $n$ wire contracts into the right adjoint $n^l$ via the right Cup ($n^l$--$n$), now demoted to the oblique *by*-phrase. Compare with \autoref{fig:discopy-discocat} (active "Alice chases Bob"), where Alice occupies the left subject slot and Bob the right object slot: the reassignment of *which* noun lands in each Cup is what makes voice alternation a topological swap $\sigma_{n,n}\colon n \otimes n \to n \otimes n$ rather than a lexical substitution. Cup count is unchanged (two, matching the transitive active), so $\kappa(D)$ tracks argument slots rather than surface case marking; per \autoref{eq:eq-4-4} only the box count distinguishes the two diagrams (the passive inserts the "is chased by" box in place of the active "chases" box).](output/figures/discopy_passive.png){#fig:discopy-passive}

Relative to \autoref{eq:eq-4-4}, the passive "Bob is chased by Alice" diagram in \autoref{fig:discopy-passive} has the same cup count as the transitive active and therefore nearly identical $\kappa(D)$; the syntactic reassignment is visible in *which* cup each noun enters, not in the total count of contractions.
