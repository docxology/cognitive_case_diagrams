# Appendix A: Syntactic and Semantic Case Assignment Diagrams {#sec:syntactic-diagrams}

This appendix presents a curated panel of syntactic constituency-style diagrams paired with their categorical pregroup type derivations, covering eight linguistically significant case assignment constructions—from simple intransitive clauses to complex embedded relative clauses with ditransitive verbs. The figure synthesizes the formal correspondences developed throughout the manuscript, making explicit how each surface syntactic pattern maps to a specific morphism composition in the pregroup grammar.

## Syntactic Trees and Pregroup Types: Eight Constructions

The figure below (\autoref{fig:syntactic-panel}) presents eight constructions arrayed in two rows of four panels, each panel containing:

1. **Syntactic tree** (top): a constituency-style diagram with arcs linking argument to predicate, nodes colour-coded by case role following the palette of \autoref{sec:notation}, §A.
2. **Pregroup type formula** (bottom): the formal typing derivation from \autoref{sec:case-type-logic}, showing how Cup contractions collapse all argument wires to sentence type $s$.

The constructions span a deliberate difficulty gradient:

| Panel | Construction | Roles | Type Complexity |
| :---: | :----------- | :---: | :--------------: |
| 1 | Intransitive (NOM) | NOM, V | 2 boxes, 1 Cup |
| 2 | Transitive (NOM+ACC) | NOM, V, ACC | 3 boxes, 2 Cups |
| 3 | Ditransitive (NOM+DAT+ACC) | NOM, V, DAT, ACC | 4 boxes, 3 Cups |
| 4 | Passive voice (Patient→NOM) | NOM, V, INS | 3 boxes + $\sigma{}$ |
| 5 | Ergative clause (ERG+ABS) | ERG×2, ABS×2, V | 5 boxes, 2 Cups |
| 6 | Benefactive (NOM+DAT+ACC+oblique) | NOM, V, ACC, DAT | 4 boxes, 3 Cups |
| 7 | Relative clause (embedded NOM) | NOM×2, V1, V2 | 6 boxes, 3 Cups |
| 8 | Causative + Adj + Adv (complex) | NOM, V, ACC, V2, ADV | 8 boxes, 5 Cups |

The monotonic increase in Cup count and box count across rows is precisely what \autoref{eq:eq-4-4} captures as the categorical complexity $\kappa{(D)}$: each additional argument slot requires one additional Cup contraction, and each modifier requires one additional Box–Cup pair.

### Ergative Clauses and the Alignment Functor

Panel 5 (Ergative clause) uses the Warlpiri example from \autoref{sec:case-systems}: *Mariyk-angku* (ERG) *yapaku wawirri* (ABS) *parnta-nu* (chased). The pregroup typing is structurally identical to the transitive (Panel 2), but the morphological realisation is governed by the alignment functor $F_{\mathrm{ERG}}: \mathcal{U} \to \mathcal{L}_{\mathrm{Warlpiri}}$ from \autoref{sec:case-systems}, which maps $A \mapsto \mathrm{ERG}$ and $S = P \mapsto \mathrm{ABS}$ rather than $A = S \mapsto \mathrm{NOM}$.

### Passivisation as a Swap Morphism

Panel 4 illustrates passivisation: in *Bob is chased by Alice*, the patient Bob is promoted to subject position (NOM) while Alice is demoted to an oblique instrumental (INS). Formally, this is the Swap morphism $\sigma_{A,B}: A \otimes B \to B \otimes A$ introduced in \autoref{sec:case-type-logic}. The pregroup typing includes a $\sigma{}$ marker indicating that the type permutation is not a simple contraction sequence but requires an explicit braiding operation.

### Relative Clauses and Wire Threading

Panel 7 (Relative clause) is the most structurally novel: in *The man the dog chased ran*, the head noun *man* is simultaneously the subject of *ran* and the implicit object of *chased* (the gap site). The pregroup type formula $n \cdot n^l \cdot n \cdot (n^r \cdot n \cdot n^l) \cdot (n^r \cdot s) \Rightarrow s$ shows how the relative-clause verb type $n^r \cdot n \cdot n^l$ threads the shared entity wire through two predicate slots — exactly the entity persistence mechanism that DisCoCirc's state wires formalise at discourse level (\autoref{sec:discocirc-discourse}).

### Complex Construction and the Complexity Metric

Panel 8 (Causative + Adj + Adv) reaches the highest complexity: 8 boxes and 5 Cup contractions. This corresponds to a categorical complexity value of $\kappa = 8 + 5 = 13$, placing it at the upper end of the single-sentence range plotted in \autoref{fig:complexity-comparison}. The formula illustrates how clausal complement embedding (the causative taking a VP complement) adds a full additional layer of type nesting beyond even the ditransitive.

![Compositional complexity increases monotonically from intransitive to causative constructions across eight case-assignment patterns. Multi-panel diagram ordered by categorical complexity $\kappa(D)$ (\autoref{eq:eq-4-4}). **Top of each panel**: constituency-style syntactic tree with argument arcs and colour-coded case roles (Blue=NOM, Red=ACC, Violet=DAT, Purple=ERG, Teal=ABS, Dark=V). **Bottom of each panel**: categorical pregroup type formula showing Cup contractions that collapse argument wires to sentence type $s$. Panels 1--4 cover nominative-accusative (intransitive, transitive, ditransitive, passive); Panels 5--6 show ergative-absolutive and benefactive; Panels 7--8 demonstrate relative-clause embedding and causative complex predicates. Cup count and box count increase monotonically across panels, directly instantiating $\kappa(D)$. Generated programmatically from `src.visualization.syntactic_sentence_diagrams.render_syntactic_panel()`.](output/figures/syntactic_case_panel.png){#fig:syntactic-panel}

```{=latex}
\newpage
```
