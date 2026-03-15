# Enriched Categories: Magnitude and Quantitative Grading {#sec:enriched-categories}

## Beyond Discrete Categories: Quantitative Grading

The categories introduced in \autoref{sec:case-systems}—with case roles as objects and grammatical relations as morphisms—capture the *qualitative* structure of case systems: which roles exist and how they connect. But linguistic data is fundamentally *quantitative*: some grammatical relations are more probable than others, some role assignments are stronger than others, and distributional similarity is a matter of degree.

To accommodate this quantitative dimension, we move from ordinary categories to **enriched categories**, where hom-sets are not just sets of morphisms but carry additional algebraic structure. The framework of Bradley et al. [-@fritz2021enriched] provides the key construction.

## The $[0,1]$-Enrichment of Case Categories

### Definition

A category $\mathcal{C}$ enriched over the unit interval $([0,1], \cdot, 1)$ assigns to every pair of objects $A, B$ a *hom-value* $\mathcal{C}(A, B) \in [0,1]$ satisfying:

$$\mathcal{C}(A, A) = 1 \quad \text{(Identity)} $$ {#eq:eq-5-1}

$$\mathcal{C}(A, C) \geq \mathcal{C}(A, B) \cdot \mathcal{C}(B, C) \quad \text{(Composition)} $$ {#eq:eq-5-2}

The identity axiom says that every expression is maximally related to itself. The composition inequality says that distributional relatedness composes sub-multiplicatively: if $A$ is 80% related to $B$ and $B$ is 70% related to $C$, then $A$ must be at least $0.8 \times 0.7 = 56\%$ related to $C$.

### Interpreting Hom-Values in Linguistic Context

Bradley et al. [-@fritz2021enriched] interpret hom-values as *conditional probabilities* in a distributional model: $\mathcal{C}(A, B) = P(\text{context} \mid A \text{ and } B \text{ co-occur})$. In our case-theoretic application, we interpret them more broadly:

| Hom-value interpretation | Domain | Example |
| :--- | :--- | :--- |
| Conditional probability | Corpus statistics | P(ACC role \| transitive verb context) |
| Proto-role strength | Semantic typology | Degree of Proto-Agent satisfaction |
| Distributional similarity | Vector semantics | Cosine similarity of case-role embeddings |
| Morphological predictability | Morpholexicology | Reliability of case-marking paradigm |

### Implementation via the EnrichedCategory Class

Our `EnrichedCategory` class implements this structure directly. The constructor takes a list of `CaseRole` objects and a NumPy proximity matrix encoding hom-values:

```python
from src.enriched import EnrichedCategory
from src.case_category import CaseRole
import numpy as np

roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
proximity = np.array([
    [1.00, 0.85, 0.30],  # NOM: high with ACC, low with DAT
    [0.85, 1.00, 0.45],  # ACC: high with NOM, moderate with DAT
    [0.30, 0.45, 1.00],  # DAT: low with NOM, moderate with ACC
])
cat = EnrichedCategory(
    name="English Case Proximity",
    roles=roles,
    proximity_matrix=proximity,
)

# Verify composition inequality: 0.30 >= 0.85 * 0.45 = 0.3825?
# This fails! English NOM-DAT is too distant relative to the chain.
assert not cat.check_composition_inequality(CaseRole.NOM, CaseRole.ACC, CaseRole.DAT)
```

The composition inequality violation here is linguistically meaningful: it tells us that the NOM→ACC→DAT chain overestimates the direct NOM→DAT relatedness, reflecting the typological fact that subject–recipient identity (e.g., in benefactive constructions) is more restricted than the product of agent–patient and patient–recipient proximities. \autoref{fig:enriched-heatmap} shows the distributional relations between case roles as a categorical relation graph.

![Case role distributional relation graph visualizing the enriched hom-values $\mathcal{C}(A,B) \in [0,1]$ among all eight case roles. Strong relations (high distributional co-occurrence, solid edges) cluster into two groups: the **core argument complex** (NOM--ACC--DAT, linked by transitive and transfer morphisms) and the **peripheral complex** (LOC--INS--ABL, linked by spatial and instrumental relations). GEN bridges both clusters via possessive modification. Weak relations (dashed edges) connect VOC to the network---its peripheral isolation reflects the pragmatic rather than syntactic function of direct address. The edge weights in this graph are the hom-values from which the $3 \times 3$ similarity matrix $Z$ ([@eq:eq-5-4]) and categorical magnitude of \autoref{sec:enriched-categories} are computed.](output/figures/enriched_hom_matrix.png){#fig:enriched-heatmap}

## Categorical Magnitude as a Complexity Invariant

A key invariant of enriched categories is their **magnitude**—a numerical quantity that captures the "effective size" of the category, discounting for overlap between objects.

For an enriched category with $n$ objects, let $Z$ be the $n \times n$ matrix with $Z_{ij} = \mathcal{C}(i, j)$. The magnitude is:

$$|\mathcal{C}| = \sum_{i,j} (Z^{-1})_{ij} $$ {#eq:eq-5-3}

when $Z$ is invertible. Magnitude has deep connections to information theory:

- For a *discrete* category (no non-trivial relationships), $|\mathcal{C}| = n$ (the number of objects)
- For a highly connected category, $|\mathcal{C}| < n$ (objects are "redundant")
- Magnitude connects to the diversity measures studied in ecology (species diversity), graph theory (effective graph resistance), and information geometry (Fisher information)

**Worked example.** Consider the minimal 3-case category with objects $\{S, A, P\}$ and hom-values $\mathcal{C}(S,A) = 0.85$ (S and A share agentive contexts), $\mathcal{C}(A,P) = 0.70$ (transitive co-occurrence), $\mathcal{C}(S,P) = 0.40$ (weak S–P overlap). The similarity matrix $Z$ is:

$$Z = \begin{pmatrix} 1.00 & 0.85 & 0.40 \\ 0.85 & 1.00 & 0.70 \\ 0.40 & 0.70 & 1.00 \end{pmatrix}, \quad Z^{-1} \approx \begin{pmatrix} 2.45 & -1.35 & 0.55 \\ -1.35 & 3.00 & -1.80 \\ 0.55 & -1.80 & 2.65 \end{pmatrix} $$ {#eq:eq-5-4}

The magnitude is $|\mathcal{C}| = \sum_{i,j} (Z^{-1})_{ij} \approx 2.45 - 1.35 + 0.55 - 1.35 + 3.00 - 1.80 + 0.55 - 1.80 + 2.65 \approx 2.90$---less than the cardinality 3 of the role inventory. The deficit $3 - 2.90 = 0.10$ is small because these three core arguments are relatively independent (the S–P overlap of 0.40 is the main source of redundancy). By contrast, an accusative alignment—which merges S and A into a single NOM role—would yield a 2-object category with magnitude exactly 2.0, and the deficit $3 - 2.0 = 1.0$ quantifies the information lost by neutralization.

**Scaling to full categories.** Our `EnrichedCategory` implementation computes magnitude for any case category. For the standard 8-case English category with empirically calibrated distributional proximity values, the magnitude is approximately 5.2—the deficit $8 - 5.2 = 2.8$ reflects distributional overlap: NOM and ACC share transitive contexts, DAT and ACC overlap in double-object constructions, and the peripheral cases (VOC, ABL) are relatively independent. This magnitude differential provides a quantitative formalization of Silverstein's [-@silverstein1976hierarchy] case hierarchy: languages with more alignment-based neutralization (lower magnitude) have less relational discriminability, while richer case inventories (higher magnitude) make finer-grained relational distinctions.

Bradley [-@bradley2020entropy] establishes a foundational link between categorical magnitude and information entropy through topological operad derivations. Her result shows that Shannon entropy can be characterized as the unique derivation of a certain topological operad—a categorical structure that also governs the composition of enriched categories. This provides a deep theoretical justification for using magnitude as a measure of linguistic complexity: the magnitude of a case category quantifies how much "information" the case system encodes about relational structure.

Leinster and Shulman [-@leinster2021magnitude] further develop **magnitude homology**, which categorifies magnitude from a scalar invariant to a graded homological invariant—detecting not just the "effective number" of objects but the higher-dimensional "holes" in the distributional landscape. For case categories, magnitude homology can distinguish between two systems with the same magnitude but different topological structure: a category where NOM–ACC–DAT form a tight cluster and all other cases are isolated looks identical in magnitude to one where the clustering is evenly distributed, but their magnitude homology groups differ, revealing that the former has a 1-dimensional "hole" (a missing transitive link) that the latter fills. This finer invariant provides a richer classification of case systems than magnitude alone.

## Enriched Functors, Bradley's Language-as-Category Model, and the LLM Connection

Bradley's [-@bradley2024ipam; -@bradley2025tea] broader program treats natural language itself as an enriched category, where:

- **Objects** are expressions (words, phrases, sentences)
- **Hom-values** encode distributional co-occurrence probabilities
- **Composition** models transitivity of distributional relatedness

This "language as enriched category" perspective has profound implications for case theory:

1. **Case roles emerge from distributional structure**: Rather than being imposed a priori, case distinctions arise from clusters of high hom-values in the enriched language category. Nouns that frequently appear in agent contexts cluster together, forming the "nominative" region of the category.

2. **Alignment types correspond to enriched structure**: Different languages partition the enriched category differently, and these partitions correspond to the alignment types (accusative, ergative, etc.) discussed in \autoref{sec:case-systems}.

3. **Language models are enriched functors**: A neural language model (such as a transformer) can be viewed as an enriched functor from the syntactic category to the semantic category, mapping type-logical derivations to distributional meaning representations while preserving the enriched structure.

The deep connection to modern distributional semantics is this: the static word embeddings of Word2Vec [@mikolov2013efficient] and GloVe [@pennington2014glove] operationalize the enriched hom-values as *cosine similarities* in a learned vector space—$\mathcal{C}(A, B) = \cos(\vec{v}_A, \vec{v}_B)$—while contextualized embeddings from transformers [@devlin2019bert; @vaswani2017attention] compute *dynamic* hom-values that depend on the sentential context. In the enriched-categorical framework, this transition from static to contextualized embeddings corresponds to moving from a *fixed* enriched category (where hom-values are precomputed from corpus statistics) to a *parameterized* enriched category (where hom-values are computed on-the-fly by attention mechanisms). Transformer attention weights $\alpha_{ij}$ are precisely such context-dependent enriched hom-values: they encode how "related" token $i$ is to token $j$ in a given representational layer, satisfying a softmax normalization that parallels the probabilistic interpretation of Bradley et al.'s [-@fritz2021enriched] hom-values as conditional probabilities.

## Connection to Lawvere's Metric Spaces and Generalized Logic

The $[0,1]$-enrichment connects to a deep tradition in categorical algebra. Lawvere showed that metric spaces are categories enriched over $([0, \infty], +, 0)$: the hom-value is the distance between points, the identity axiom says $d(x, x) = 0$, and the composition inequality is the triangle inequality $d(x, z) \leq d(x, y) + d(y, z)$. Our $[0,1]$-enrichment is the multiplicative analogue: hom-values are *similarities* rather than distances, and the composition inequality is sub-multiplicative rather than sub-additive.

This Lawvere-style perspective unifies our case categories with the geometry of distributional semantics: case roles are points in a "similarity space," and morphisms between them are paths weighted by distributional proximity. The magnitude of this space then quantifies the "effective dimensionality" of the case system—how many independent relational distinctions the language makes.
