# Compositional Distributional Semantics {#sec:categorical-semantics}

A typed grammatical derivation can guide a semantic calculation. In the DisCoCat construction, a suitable interpretation maps grammatical types to semantic spaces and the derivation to a composition map [@coecke2010mathematical]. This separates the choice of a grammar from the choice of lexical representations.

## An explicit tensor contraction {#sec:discocat-meaning-functor}

Let $a_i$ and $b_k$ represent the two noun vectors and $V_{ijk}$ a transitive verb tensor, with the middle index ranging over sentence features. The example calculation is

$$
m_j=\sum_{i,k}a_i V_{ijk} b_k.
$$ {#eq:eq-4-2}

The source helper `create_tensor_semantics()` constructs deterministic example tensors and evaluates their contraction. These are generated representations, not pretrained embeddings or estimates from a corpus. Exchanging the arguments changes the result when the selected tensor is sensitive to that exchange; the formalism does not guarantee every tensor will distinguish them.

![Word tensor product followed by grammatical contraction in the transitive example. The diagram shows how assigned types determine the slots used by semantic evaluation.](output/figures/discopy_composition.png){#fig:discopy-discocat}

![A ditransitive example with three explicitly supplied argument slots. Recipient and theme labels are metadata unless refined noun objects are introduced.](output/figures/discopy_ditransitive.png){#fig:discopy-ditransitive}

The diagrams make dependency on argument position inspectable. This is a representational advantage, not a measured interpretability result. Tensor entries can still be opaque, high-dimensional, or poorly estimated. Similarly, transformer attention is not automatically a functor or an enriched hom-matrix; such an identification needs domains, codomains, and law-preserving maps. A useful empirical comparison would train alternative composition models on the same data and test argument reversal and generalization on held-out constructions.
