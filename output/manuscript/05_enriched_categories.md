# $[0,1]$-Enriched Case Categories: Hom-Values as Distributional Proximity, Magnitude as Complexity {#sec:enriched-categories}

## Why Binary Morphisms Are Not Enough

The categories established in \autoref{sec:case-systems}—modeling case roles as objects and grammatical relations as morphisms—capture the *qualitative* topology of case systems: which roles exist and how they connect. However, actual linguistic data is fundamentally *quantitative*: certain grammatical relations are more probable than others, proto-role assignments vary in strength, and distributional similarity is a matter of degree.

To accommodate this quantitative dimension without sacrificing algebraic structure, we advance from ordinary categories to **enriched categories**. In an enriched category, hom-sets carry additional measurable structure rather than functioning as mere discrete sets of morphisms. The framework of Bradley et al. [-@fritz2021enriched] supplies the key formal construction.

## Enriching Over $([0,1],\cdot,1)$

### Hom-Values as Graded Distributional Proximity: Four Linguistic Interpretations

A category $\mathcal{C}$ enriched over the unit interval $([0,1], \cdot, 1)$ assigns to every pair of objects $A, B$ a *hom-value* $\mathcal{C}(A, B) \in [0,1]$ satisfying:

\begin{align}
\mathcal{C}(A, A) &= 1 \quad \text{(Identity)} \label{eq:eq-5-1} \\
\mathcal{C}(A, C) &\geq \mathcal{C}(A, B) \cdot \mathcal{C}(B, C) \quad \text{(Composition)} \label{eq:eq-5-2}
\end{align}

The identity axiom physically dictates that every distinct linguistic expression remains perfectly and maximally related to itself. The composition inequality imposes a strict logical boundary, demanding that distributional relatedness inherently composes sub-multiplicatively: if expression $A$ proves 80% related to $B$, and $B$ remains 70% related to $C$, the overarching algebraic structure formally guarantees that $A$ must be at least $0.8 \times 0.7 = 56\%$ related to $C$.

### Conditional Probability, Proto-Role Strength, Cosine Similarity

Bradley et al. [-@fritz2021enriched] originally interpret these numerical hom-values strictly as empirical *conditional probabilities* measured within a massive distributional model: $\mathcal{C}(A, B) = P(\text{context} \mid A \text{ and } B \text{ co-occur})$. Within our customized case-theoretic application, we actively broaden this interpretation to capture deep grammatical phenomena:

| Hom-value interpretation | Domain | Example |
| :--- | :--- | :--- |
| Conditional probability | Corpus statistics | P(ACC role \| transitive verb context) |
| Proto-role strength | Semantic typology | Degree of Proto-Agent satisfaction |
| Distributional similarity | Vector semantics | Cosine similarity of case-role embeddings |
| Morphological predictability | Morpholexicology | Reliability of case-marking paradigm |

### When Composition Inequality Fails

Our `EnrichedCategory` class implements this structure directly. The constructor takes a list of `CaseRole` objects and a NumPy proximity matrix encoding hom-values:

```python
from src.enriched_cat.enriched import EnrichedCategory
from src.case_systems.case_category import CaseRole
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

![Core and peripheral argument complexes emerge from enriched distributional hom-values. Relation graph visualizing $\mathcal{C}(A,B) \in [0,1]$ among all eight case roles. Strong relations (solid edges) cluster into two groups: the **core argument complex** (NOM--ACC--DAT, linked by transitive and transfer morphisms) and the **peripheral complex** (LOC--INS--ABL, linked by spatial and instrumental relations). GEN bridges both via possessive modification. Weak relations (dashed edges) connect VOC---its peripheral isolation reflects the pragmatic rather than syntactic function of direct address. These hom-values yield the similarity matrix $Z$ (\autoref{eq:eq-5-4}) and categorical magnitude of \autoref{sec:enriched-categories}. Generated programmatically from the `EnrichedCategory` class.](output/figures/enriched_hom_matrix.png){#fig:enriched-heatmap}
