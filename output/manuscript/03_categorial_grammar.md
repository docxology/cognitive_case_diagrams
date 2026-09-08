# Categorial Grammar and Executable Reductions {#sec:categorial-grammar}

Categorial grammars associate lexical expressions with types that determine how they combine. In a pregroup presentation, a noun type $n$ has left and right adjoints. Ordered reductions use $n^l n\leq 1$ and $n n^r\leq 1$, together with the corresponding expansion inequalities [@coecke2010mathematical]. These are directional operations; arbitrary wire exchange is not an axiom of a nonsymmetric pregroup.

For the hand-assigned types of “Alice chases Bob,” the reduction is

$$
n\,(n^r s n^l)\,n\longrightarrow s.
$$ {#eq:eq-3-2}

The implementation builds words and cups with DisCoPy. The assertion below verifies the codomain of this specified derivation. It does not discover lexical types or establish grammaticality independently of them.

```python
from discopy.rigid import Ty, Box, Cup, Id
n, s = Ty("n"), Ty("s")
words = (Box("Alice", Ty(), n)
         @ Box("chases", Ty(), n.r @ s @ n.l)
         @ Box("Bob", Ty(), n))
diagram = words >> (Cup(n, n.r) @ Id(s) @ Cup(n.l, n))
assert diagram.cod == s
```

![Native rendering of the transitive example. Case colors are supplied metadata; the drawing is a schematic companion to the executable DisCoPy construction.](output/figures/string_diagram_discocat.png){#fig:native-discocat}

![Intransitive, transitive, and passive examples with explicitly assigned lexical types. Cup counts describe these constructions rather than a universal complexity scale for voice.](output/figures/discopy_sentence_progression.png){#fig:string-diagram}

![Lexical substitutions in a shared normalized diagram template. Language labels do not imply that the displayed order is each language's surface order or that the code implements those languages' grammars.](output/figures/discopy_multilingual.png){#fig:multilingual-isomorphism}

String diagrams represent equations within a specified categorical calculus. A drawing is a proof only when the allowed rewrites and interpretation have been established. Visual similarity alone does not prove a linguistic universal, semantic equivalence, or independence from word order.

![A larger executable DisCoPy example using assigned modifier and argument types. Successful contraction checks the supplied type sequence.](output/figures/discopy_transitive.png){#fig:discopy-transitive}

![Pedagogical unpacking of the transitive reduction: lexical types, juxtaposition, cup contraction, and the remaining sentence output. The reduced output type is $s$; the semantic sentence morphism is not thereby erased.](output/figures/pregroup_reduction_unpacking.png){#fig:pregroup-unpacking}
