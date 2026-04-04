
# From Phrase Structure to Type Algebra {#sec:categorial-grammar}

## Each Word Is Its Own Grammar Rule

Traditional generative grammar computes sentence structure using top-down phrase-structure rules that recursively combine constituents. Categorial grammar perfectly inverts this perspective: rather than specifying abstract construction rules, it assigns each lexical item a dedicated *type* that rigorously encodes its combinatory potential. For example, a transitive verb like "chases" is not loosely defined as "a word requiring a subject and object," but specifically assigned the algebraic type $(n \backslash s) / n$—an active function that categorically demands a noun to its right (the object) and a noun to its left (the subject) to yield a complete sentence.

## Lambek's Residuation Law: Consuming and Producing Types in Linear Order

Lambek [-@lambek1958mathematics] laid the algebraic foundations by introducing a *residuated* structure on syntactic types. He defined two binary operations—the left residual $\backslash$ and the right residual $/$—derived from the multiplicative connective $\otimes$ (concatenation). The fundamental axiom governing this system is the residuation law:

\begin{equation}
A \otimes B \leq C \quad \iff \quad A \leq C / B \quad \iff \quad B \leq A \backslash C
\label{eq:eq-3-1}
\end{equation}

This law brilliantly captures the fundamental duality of syntax: a verb of type $(n \backslash s) / n$ actively *consumes* available noun arguments to *produce* a well-formed sentence. The resulting **Lambek calculus** operates as a non-commutative intuitionistic linear logic—non-commutative because strict word order dictates meaning, and linear because the derivation logically consumes each lexical resource exactly once.

### Pregroups Unlock Compact Closure: The Bridge to DisCoCat String Diagrams

Lambek [-@lambek2004fine] later simplified the framework to **pregroup grammars**, where each type $a$ has a left adjoint $a^l$ and a right adjoint $a^r$ satisfying:

\begin{equation}
a^l \cdot a \leq 1 \leq a \cdot a^l \qquad a \cdot a^r \leq 1 \leq a^r \cdot a
\label{eq:eq-3-2}
\end{equation}

Coecke, Sadrzadeh, and Clark revolutionized this formal structuralism in 2010 with the **DisCoCat** (Distributional Compositional Categorical) model [-@coecke2010mathematical]. DisCoCat mathematically unifies categorial grammar with distributional semantics by defining strong monoidal functors mapping pregroup grammars directly into vector spaces. As Duneau emphasizes, this approach "allows the meaning of a sentence to be computed as a function of both the distributional meaning of the words involved, as well as its grammatical form" [-@duneau2021parsing]. By proving that pregroups and finite-dimensional vector spaces both behave as rigid monoidal categories, DisCoCat allows us to compute whole-sentence vector meanings linearly from constituent word vectors.

In this system, grammaticality literally reduces to algebraic verification: checking whether a sequence of types maps to the sentence type $s$ via strict *contraction* ($a^l \cdot a \to 1$) and *expansion* ($1 \to a \cdot a^l$) operations. This specific reformulation unlocks the DisCoCat framework (\autoref{sec:categorical-semantics}) because pregroups function as **compact closed categories**, natively supporting a powerful, computationally sound diagrammatic calculus. When a derivation is ill-typed, contractions fail to close: there is no valid reduction to $s$. \autoref{sec:cognitive-security} develops the security reading of that failure mode—typed interaction boundaries and prompt injection as illicit role reassignment.

## Cups, Caps, and Joyal–Street: How Wires Prove Grammaticality

The pivotal connection between categorial grammar and visualization comes from Joyal and Street [-@joyalstreet1991geometry], who proved that morphisms in monoidal categories can be faithfully represented as *string diagrams*—planar graphs where:

- **Wires** represent types (objects of the category)
- **Boxes** represent words or operations (morphisms)
- **Vertical composition** represents sequential application
- **Horizontal juxtaposition** represents the tensor product (concatenation)
- **Cups and caps** represent the contraction/expansion of a pregroup

\autoref{fig:string-diagram} surveys three syntactic structures side by side (progression from intransitive to passive); \autoref{fig:native-discocat} shows the same transitive sentence rendered by our native matplotlib pipeline—a direct computational output confirming word-box layout, wire routing, and cup-contraction geometry independently of DisCoPy.

![Native matplotlib rendering cross-validates DisCoPy pregroup geometry. String diagram for "Alice chases Bob" generated via `src.visualization.string_diagrams.render_discocat_sentence()` without the DisCoPy library. Three Word boxes carry pregroup types: $n$ (Alice, **blue** = NOM), $n^r \otimes s \otimes n^l$ (chases, **neutral**), and $n$ (Bob, **red** = ACC). Dashed arcs trace cup connections from noun wires to the verb's adjoint slots, rendering $\varepsilon: n^r \otimes n \to 1$ and $\varepsilon: n^l \otimes n \to 1$ as paired ligatures. This confirms that our visualization pipeline correctly reconstructs pregroup string-diagram geometry using only case-role metadata from `src.case_systems.case_category`, cross-validating the DisCoPy canonical output in \autoref{fig:discopy-transitive}.](output/figures/string_diagram_discocat.png){#fig:native-discocat}

![Sentence complexity increases monotonically from intransitive to passive. A 1×3 DisCoPy pregroup grammar visualization: Panel (a) intransitive "Bob runs" (NOM, 1 cup); Panel (b) transitive "Alice chases Bob" (NOM+ACC, 2 cups); Panel (c) passive "Bob is-chased" (patient promoted to subject via reduced pregroup type). Cup count directly reflects verb valency per \autoref{eq:eq-4-4}.](output/figures/discopy_sentence_progression.png){#fig:string-diagram}

![Type-logical structure is invariant under surface word-order permutation. Pregroup derivations for "SUBJ chases OBJ" across three typologically diverse languages: English (SVO), Latin (inflected, free order), and Japanese (agglutinative, SOV). Each renders an identical type reduction $n \otimes (n^r \otimes s \otimes n^l) \otimes n \to s$, confirming the central claim of categorial grammar: syntactic universals reside in the type algebra, not in linear word order.](output/figures/discopy_multilingual.png){#fig:multilingual-isomorphism}

This result—the soundness and completeness of string-diagrammatic reasoning—formally guarantees that any topological conclusion drawn visually from the diagram is algebraically valid: the diagram is not a heuristic but a rigorous proof instrument.

This profound visual transparency instantiates exactly the "free ride" phenomenon identified by Shimojima [-@shimojima1996reasoning]: a single diagram simultaneously exposes the syntactic derivation, the deep argument structure, and the compositional flow of semantic meaning—entirely eliminating the need for sequential, explicit inference steps.

**Concrete derivation in DisCoPy.** The type reduction for "Alice chases Bob" is computationally verified using the DisCoPy library's `discopy.rigid` module:

```python
from discopy.rigid import Ty, Box, Cup, Id
n, s = Ty('n'), Ty('s')
alice = Box('Alice', Ty(), n)
chases = Box('chases', Ty(), n.r @ s @ n.l)
bob  = Box('Bob',  Ty(), n)
words = alice @ chases @ bob          # n ⊗ (n.r ⊗ s ⊗ n.l) ⊗ n
cups  = Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
diagram = words >> cups               # reduces to s
assert diagram.cod == s               # type-checks: sentence type
```

The two `Cup` operations successfully contract $n$ with $n^r$ (resolving the subject–verb link) and $n^l$ with $n$ (resolving the verb–object link). This topological reduction collapses the five-wire tensor product into a single, valid sentence wire $s$. Consequently, the assertion `diagram.cod == s` constitutes a direct, machine-processable proof of grammaticality.

**From pregroup types to graded types.** The standard pregroup derivation produces a rigid, binary grammaticality judgment: the final codomain of the fully contracted tensor product either matches the sentence type $s$ (grammatical) or fails (ill-formed). However, we can *grade* this binary verdict by replacing the underlying Boolean algebra $\{0,1\}$ with the continuous unit interval $[0,1]$. This substitution yields a graded type theory where type judgments carry continuous confidence weights rather than truth values. Asudeh and Giorgolo [-@asudeh2020graded] developed this approach using a monadic semantics that wraps base types inside a computational effect tracking epistemic uncertainty—an idea whose categorical content is precisely a change of enrichment base.

Mapped into our framework, this operation corresponds exactly to the $[0,1]$-enrichment detailed in \autoref{sec:enriched-categories}: the enriched scalar weight on any specific morphism $f: A \to B$ quantifies the systemic confidence that the categorical case assignment $A \to B$ remains well-typed. From there, categorical magnitude aggregates these sparse, local confidence scores into a robust global complexity measure evaluating the entire syntactic derivation. Ultimately, the systematic progression from rigid pregroup strings, through graded types, into fully enriched case categories operates mathematically as a strict cascade of base-change functors ($\mathbf{Bool} \hookrightarrow [0,1] \hookrightarrow \mathbf{R}_{\geq 0}$)—where each successive level grants greater representational nuance while demanding higher computational complexity.

![Direct DisCoPy machine output confirms pregroup type reduction to sentence wire $s$. Three Word boxes carry types $n$ (Alice), $n^r \otimes s \otimes n^l$ (chases), and $n$ (Bob). Two Cup contractions $\varepsilon\colon n^r \otimes n \to 1$ and $\varepsilon\colon n^l \otimes n \to 1$ cancel adjoint pairs, reducing the five-wire tensor product to the single sentence wire $s$. Unlike the schematic progression in \autoref{fig:string-diagram}, this is the *direct computational output* confirming `diagram.cod == s`. By the Curry--Howard correspondence, this diagram simultaneously constitutes a syntactic derivation, a proof of well-typedness, and (under the meaning functor of \autoref{sec:categorical-semantics}) a compositional semantic computation. Our extension decorates $n$-typed wires with functorial states $S: \mathbf{Ent} \to \mathbf{Case}$, tracking role assignments across discourse boundaries via **DisCoCirc entity wires**.](output/figures/discopy_transitive.png){#fig:discopy-transitive}
