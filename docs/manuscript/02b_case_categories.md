# Case-Role Graphs and Categorical Presentations {#sec:case-categories}

The Python `CaseCategory` stores a finite role set and a list of labelled arrows. An arrow has source, target, label, and a weight in $[0,1]$. Identity arrows and composite arrows can be constructed. For composable $f:A\to B$ and $g:B\to C$, the implementation multiplies weights:

$$
w(g\circ f)=w(g)w(f).
$$ {#eq:eq-2-1}

This gives a useful presentation of relational paths. The stored generator list need not contain every composite. Endpoint and weight checks therefore should not be described as a complete implementation of arbitrary hom-sets and their equations. `is_well_formed()` checks the stored representation; it does not prove that a proposed linguistic analysis is adequate.

![The standard synthetic role graph. Its arrows are explicit modeling choices; their presence is not a measured grammatical universal.](output/figures/case_category_standard.png){#fig:case-standard}

An alignment map assigns source labels to target labels. The two common groupings of S, A, and P differ as maps on named arguments, even when their unlabelled quotient sets have the same cardinality. In particular, NOM alone cannot determine whether a source argument was S or A, so an accusative-to-ergative mapping cannot generally recover the original argument from its surface case.

![Comparison of schematic alignment maps. The grouped labels illustrate which distinctions are retained or lost; the figure is not an equivalence proof between language grammars.](output/figures/alignment_comparison.png){#fig:alignment}

`AlignmentFunctor` is a lightweight object/arrow mapping helper. Its identity and composition predicates compare endpoints and weights; they do not verify all target-hom membership or labelled-arrow equations. Some alignment factories contain only objects, so tests over their stored nonidentity arrows can be vacuous. A mathematical functor claim requires an explicit source and target category and preservation of their defining relations.

![A composition triangle showing the source, intermediate, and target of a selected path. Equality of two paths is an additional relation to establish, not a consequence of drawing a triangle.](output/figures/composition_triangle.png){#fig:composition}

For actual functors $F,G:C\to D$, a natural transformation requires components $\eta_A:F(A)\to G(A)$ with

$$
G(f)\circ\eta_A=\eta_B\circ F(f).
$$ {#eq:eq-2-2}

The natural-transformation helper checks its supplied components and finite source arrows using the project's representation. This is useful for examples, but neither a dative alternation nor a cross-linguistic correspondence becomes a natural transformation without the required maps and equations.
