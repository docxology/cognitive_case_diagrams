# Candidate Similarities and $[0,1]$-Enrichment {#sec:enriched-categories}

For enrichment over the ordered monoid $([0,1],\cdot,1)$, a finite hom-matrix $Z$ must satisfy

$$
Z_{ii}=1,\qquad Z_{ik}\geq Z_{ij}Z_{jk}\quad\text{for every }i,j,k.
$$ {#eq:eq-5-2}

The inequality follows the order convention used here. Symmetry is optional. Normalized conditional probabilities, cosine similarities, and attention weights do not generally satisfy these axioms. They are candidate inputs requiring separate justification.

The standard 8-role matrix in `src/enriched_cat/enriched.py` is hand-selected and fails some composition inequalities. For example, its NOM-to-DAT value is 0.45, whereas the NOM-to-ACC-to-DAT product is 0.85 × 0.55 = 0.4675. The failure is retained as a useful counterexample; the matrix is not described as an English estimate or a valid enriched category merely because its entries lie in $[0,1]$.

![Synthetic candidate similarity matrix. Read entries as selected numerical examples. The raw matrix fails composition closure; neither its colors nor its linguistic labels provide empirical provenance.](output/figures/enriched_hom_matrix.png){#fig:enriched-heatmap}

`composition_closure()` computes the maximum path product using a Floyd–Warshall update $Z_{ik}\leftarrow\max(Z_{ik},Z_{ij}Z_{jk})$. It returns a new matrix and leaves the raw input intact. With entries at most one and unit diagonals, cycles cannot improve a path product beyond a cycle-free representative. The resulting finite closure satisfies the multiplicative path inequalities up to the stated numerical tolerance.

```python
from src.enriched_cat.enriched import standard_enriched_category
candidate = standard_enriched_category()
closed = candidate.composition_closure()
assert not closed.full_composition_check()["violations"]
```

Closure is a mathematical operation, not statistical validation. It raises selected similarities and can alter their interpretation, spectrum, magnitude, and clusters. Both raw and closed matrices should be retained in empirical work. Bradley, Terilla, and Vlassopoulos construct enriched structure from suitable text-extension probabilities [@bradley2021enriched]; this does not identify the present role matrix with their construction.
