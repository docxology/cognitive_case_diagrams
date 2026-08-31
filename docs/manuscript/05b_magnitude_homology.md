# Magnitude and Magnitude Homology: Effective Role Count, Lawvere Similarity Spaces, and Language as Enriched Category {#sec:magnitude-homology}

**Where we are in the argument.** \autoref{sec:enriched-categories} introduced $[0,1]$-enrichment so that the case category carries a full distributional-proximity matrix. This chapter extracts the principal quantitative invariant of that matrix — Leinster's *magnitude* $|\mathcal{C}| = \sum_{i,j} (Z^{-1})_{ij}$ — which gives a single-number answer to "how many effectively distinct case roles does the language use?" ($|\mathcal{C}| \approx 2.50$ for the standard eight-case system), and which will serve as the N400 magnitude-change proxy in \autoref{sec:diagrammatic-cognition} and as a cognitive-security invariant in \autoref{sec:cognitive-security}.

A central mathematical invariant unique to enriched categories is their **magnitude**—a numerical quantity capturing the "effective size" of the category by discounting distributional overlap between objects.

For an enriched category with $n$ objects, let $Z$ be the $n \times n$ similarity matrix where $Z_{ij} = \mathcal{C}(i, j)$. The categorical magnitude is:

\begin{equation}
|\mathcal{C}| = \sum_{i,j} (Z^{-1})_{ij}
\label{eq:eq-5-3}
\end{equation}

assuming $Z$ is invertible. This magnitude metric connects to information theory:

- For a *discrete* category (no non-trivial relationships), $|\mathcal{C}| = n$ (the number of objects)
- For a highly connected category, $|\mathcal{C}| < n$ (objects are "redundant")
- Magnitude connects to the diversity measures studied in ecology (species diversity), graph theory (effective graph resistance), and information geometry (Fisher information)

**Worked example.** Consider the minimal 3-case category with objects $\{S, A, P\}$ and hom-values $\mathcal{C}(S,A) = 0.85$ (S and A share agentive contexts), $\mathcal{C}(A,P) = 0.70$ (transitive co-occurrence), $\mathcal{C}(S,P) = 0.40$ (weak S–P overlap). The similarity matrix $Z$ is:

\begin{equation}
Z = \begin{pmatrix} 1.00 & 0.85 & 0.40 \\ 0.85 & 1.00 & 0.70 \\ 0.40 & 0.70 & 1.00 \end{pmatrix}, \quad Z^{-1} \approx \begin{pmatrix} 4.93 & -5.51 & 1.88 \\ -5.51 & 8.12 & -3.48 \\ 1.88 & -3.48 & 2.68 \end{pmatrix}
\label{eq:eq-5-4}
\end{equation}

The magnitude is $|\mathcal{C}| = \sum_{i,j} (Z^{-1})_{ij} \approx 4.93 - 5.51 + 1.88 - 5.51 + 8.12 - 3.48 + 1.88 - 3.48 + 2.68 \approx 1.52$---substantially less than the cardinality 3 of the role inventory. The deficit $3 - 1.52 = 1.48$ is substantial—approximately 49% of the cardinality—reflecting that S and A share dense agentive contexts ($w = 0.85$) and A and P share transitive co-occurrence contexts ($w = 0.70$), making the proto-role system considerably redundant. By contrast, an accusative alignment—which merges S and A into a single NOM role—would yield a 2-object category with magnitude exactly 2.0, and the deficit $3 - 2.0 = 1.0$ quantifies the information lost by neutralization.

**Scaling to full categories.** Our `EnrichedCategory` implementation computes magnitude for any case category. For the standard 8-case English category with empirically calibrated distributional proximity values, the magnitude is approximately 2.50—the deficit $8 - 2.50 = 5.50$ reflects substantial distributional overlap: NOM and ACC share transitive contexts ($w = 0.85$), DAT and ACC overlap in double-object constructions ($w = 0.55$), GEN and NOM co-occur in possessive constructions ($w = 0.60$), and even peripheral cases such as VOC overlap with NOM ($w = 0.70$). Only 2.50 of the 8 case roles encode genuinely independent relational distinctions. This magnitude differential provides a quantitative formalization of Silverstein's [-@silverstein1976hierarchy] case hierarchy: languages with more alignment-based neutralization (lower magnitude) have less relational discriminability, while richer case inventories (higher magnitude) make finer-grained relational distinctions.

Bradley [-@bradley2021entropy] established a link connecting categorical magnitude to classical information entropy via topological operad derivations. Her result proves that Shannon entropy acts as the unique algebraic derivation of a specific topological operad—a categorical structure governing the composition of enriched categories. This supplies theoretical justification for magnitude as a measurable geometric invariant quantifying linguistic complexity: the magnitude of any case category quantifies how much irreducible "information" that case system encodes regarding relational meaning.

Leinster and Shulman [-@leinster2021magnitude] further develop **magnitude homology**, which categorifies magnitude from a scalar invariant to a graded homological invariant—detecting not just the "effective number" of objects but the higher-dimensional "holes" in the distributional landscape. For case categories, magnitude homology can distinguish between two systems with the same magnitude but different topological structure: a category where NOM–ACC–DAT form a tight cluster and all other cases are isolated looks identical in magnitude to one where the clustering is evenly distributed, but their magnitude homology groups differ, revealing that the former has a 1-dimensional "hole" (a missing transitive link) that the latter fills. This finer invariant provides a richer classification of case systems than magnitude alone. Bradley and Vigneaux [-@bradleyvigneaux2025magnitude] realize this programme on natural language by building categories of texts enriched from language-model next-token probabilities and computing magnitude and magnitude homology for associated metric spaces of texts—a concrete large-scale application of Leinster--Shulman theory beyond finite toy examples.

However, that LM-enriched construction exposes a vulnerability relevant to our cognitive synthesis: if magnitude homology computations are ported into non-classical environments, such as lambeq Gen II's Parameterized Quantum Circuits (\autoref{sec:quantum-active-inference}), the inherent environmental quantum noise (decoherence) acts as a non-trivial topological perturbation. Unless error-correction syndromes explicitly preserve the sequence of homology groups, the invariant may technically fail to commute. Thus, comparing the 1-dimensional "holes" of classical case-frames against their quantum algorithmic analogues must be approached with mathematical caution, respecting the shear forces introduced by measurement non-commutativity.

## Language as Enriched Category: Transformer Attention Weights Are Context-Dependent Hom-Values

Bradley's [-@bradley2024ipam; -@bradley2025tea] broader program treats natural language itself as an enriched category, where:

- **Objects** are expressions (words, phrases, sentences)
- **Hom-values** encode distributional co-occurrence probabilities
- **Composition** models transitivity of distributional relatedness

This "language as enriched category" perspective has profound implications for case theory:

1. **Case roles emerge from distributional structure**: Rather than being imposed a priori, case distinctions arise from clusters of high hom-values in the enriched language category. Nouns that frequently appear in agent contexts cluster together, forming the "nominative" region of the category.

2. **Alignment types correspond to enriched structure**: Different languages partition the enriched category differently, and these partitions correspond to the alignment types (accusative, ergative, etc.) discussed in \autoref{sec:case-systems}.

3. **Language models are enriched functors**: A neural language model (such as a transformer) can be viewed as an enriched functor from the syntactic category to the semantic category, mapping type-logical derivations to distributional meaning representations while preserving the enriched structure.

The deep connection to modern distributional semantics is this: static embeddings operationalize hom-values as cosine similarity in a learned space, while contextualized transformers [@devlin2019bert; @vaswani2017attention] compute *dynamic* hom-values from sentential context—a move from a fixed enriched category to a parameterized one. The attention-as-enriched-cup analogy (developed in \autoref{sec:categorical-semantics}) carries the same intuition here: layer-wise weights grade how strongly tokens couple, alongside Bradley et al.'s [-@fritz2021enriched] probabilistic reading of hom-objects.

## Lawvere's Insight: Case Categories Are Similarity Spaces

The $[0,1]$-enrichment connects to a deep tradition in categorical algebra. Lawvere showed that metric spaces are categories enriched over $([0, \infty], +, 0)$: the hom-value is the distance between points, the identity axiom says $d(x, x) = 0$, and the composition inequality is the triangle inequality $d(x, z) \leq d(x, y) + d(y, z)$. Our $[0,1]$-enrichment is the multiplicative analogue: hom-values are *similarities* rather than distances, and the composition inequality is sub-multiplicative rather than sub-additive. The inequality *direction reverses* between the two settings because the monoidal structure reverses: in the additive metric setting we want small composites (triangle inequality is an upper bound on distance), whereas for multiplicative similarity we want large composites (so the natural inequality is the lower bound $\mathcal{C}(A,C) \ge \mathcal{C}(A,B)\cdot\mathcal{C}(B,C)$, equivalently the upper-bound form used in the \autoref{sec:notation} notation appendix).

**When is magnitude defined?** Leinster's magnitude requires the similarity matrix $Z$ to be invertible. For the standard eight-case category (\autoref{tbl:eight-cases}) $Z$ has condition number $\approx 9.5$ and magnitude is well-defined ($|C| \approx 2.50$, deficit $5.50$). For degenerate categories where roles are distributional clones (e.g. $Z$ has repeated rows), $Z$ becomes singular; the implementation in `src/enriched_cat/enriched.py` falls back to a Moore–Penrose pseudo-inverse with a logged warning, which yields a best-least-squares approximate magnitude but not the exact Leinster magnitude (which is simply undefined in that case).

**Distributional-semantics embedding into $[0,1]$.** A word-embedding model instantiates the enriched category via the explicit map $\mathcal{C}(w, w') = \bigl(\cos(v_w, v_{w'}) + 1\bigr) / 2 \in [0,1]$, where $v_w, v_{w'}$ are the model's vector representations and $\cos$ is cosine similarity. This is the concrete choice that allows a pretrained transformer or word2vec model to be read as a $[0,1]$-enriched functor.

This Lawvere-style perspective unifies our case categories with the geometry of distributional semantics: case roles are points in a "similarity space," and morphisms between them are paths weighted by distributional proximity. The magnitude of this space then quantifies the "effective dimensionality" of the case system—how many independent relational distinctions the language makes.
