# $[0,1]$-Enriched Case Categories: Hom-Values as Distributional Proximity {#sec:enriched-categories}

**Where we are in the argument.** \autoref{sec:case-systems}–\autoref{sec:discocirc-discourse} have been working in a category whose morphisms are Boolean — a relation either exists between two case roles or it does not. This chapter upgrades that to $[0,1]$-enrichment so every pair of roles carries a *graded* hom-value $\mathcal{C}(A, B) \in [0,1]$ — a distributional proximity that doubles as the precision $w_f$ used throughout \autoref{sec:cognitive-integration} / \autoref{sec:daif-results} for prediction-error weighting, and that will feed into the magnitude invariant of \autoref{sec:magnitude-homology} and the topos-theoretic bridge of \autoref{sec:topos-theory}.

## Why Binary Morphisms Are Not Enough

The categories established in \autoref{sec:case-systems}—modeling case roles as objects and grammatical relations as morphisms—capture the *qualitative* topology of case systems: which roles exist and how they connect. However, actual linguistic data is fundamentally *quantitative*: certain grammatical relations are more probable than others, proto-role assignments vary in strength, and distributional similarity is a matter of degree.

To accommodate this quantitative dimension without sacrificing algebraic structure, we advance from ordinary categories to **enriched categories**. In an enriched category, hom-sets carry additional measurable structure rather than functioning as mere discrete sets of morphisms. The framework of Bradley et al. [-@fritz2021enriched] supplies the key formal construction.

## Enriching Over $([0,1],\cdot,1)$: Identity, Sub-Multiplicative Composition, and Four Hom-Value Readings

### The Identity and Composition Axioms for $[0,1]$-Enriched Case Categories

A category $\mathcal{C}$ enriched over the unit interval $([0,1], \cdot, 1)$ assigns to every pair of objects $A, B$ a *hom-value* $\mathcal{C}(A, B) \in [0,1]$ satisfying:

\begin{align}
\mathcal{C}(A, A) &= 1 \quad \text{(Identity)} \label{eq:eq-5-1} \\
\mathcal{C}(A, C) &\geq \mathcal{C}(A, B) \cdot \mathcal{C}(B, C) \quad \text{(Composition)} \label{eq:eq-5-2}
\end{align}

The identity axiom dictates that every linguistic expression remains maximally related to itself. The composition inequality imposes a strict logical boundary, demanding that distributional relatedness inherently composes sub-multiplicatively: if expression $A$ proves 80% related to $B$, and $B$ remains 70% related to $C$, the overarching algebraic structure formally guarantees that $A$ must be at least $0.8 \times 0.7 = 56\%$ related to $C$.

### Four Linguistic Readings of the Hom-Value: Probability, Proto-Role, Similarity, Predictability

Bradley et al. [-@fritz2021enriched] originally interpret these numerical hom-values strictly as empirical *conditional probabilities* measured within a massive distributional model: $\mathcal{C}(A, B) = P(\text{context} \mid A \text{ and } B \text{ co-occur})$. Within our customized case-theoretic application, we actively broaden this interpretation to capture deep grammatical phenomena (\autoref{tbl:hom-value-interpretations}):

| Hom-value interpretation | Domain | Example |
| :--- | :--- | :--- |
| Conditional probability | Corpus statistics | $P(\text{ACC role} \mid \text{transitive verb context})$ |
| Proto-role strength | Semantic typology | Degree of Proto-Agent satisfaction |
| Distributional similarity | Vector semantics | Cosine similarity of case-role embeddings |
| Morphological predictability | Morpholexicology | Reliability of case-marking paradigm |

Table: Four linguistic interpretations of hom-values in $[0,1]$-enriched case categories. {#tbl:hom-value-interpretations}

### When the Composition Inequality Fails: A Worked English NOM–ACC–DAT Example

**Architectural note — two decoupled number systems.** The enriched hom-value $\mathcal{C}(A,B) \in [0,1]$ defined here is *not* the same scalar as the morphism weight $w_f \in [0,1]$ that appears on every `Morphism` in the `CaseCategory` of \autoref{sec:case-systems}. The `CaseCategory` assigns $w_f = 1.0$ to every structurally present morphism (it encodes *admissibility* — a binary question dressed as a real to support multiplicative composition along chains, per Eq. \ref{eq:eq-2-1}), whereas the `EnrichedCategory` assigns a *graded distributional proximity* between every pair of roles including non-adjacent ones. The two number systems serve different purposes and are intentionally decoupled in the implementation: `src/case_systems/case_category.py::standard_case_category` ships unit-weight morphisms, while `src/enriched_cat/enriched.py::standard_enriched_category` ships the full $8 \times 8$ proximity matrix $Z$. When a prediction-error formula in \autoref{sec:cognitive-integration} or \autoref{sec:daif-results} references a "weight" $w_f = \mathcal{C}(A,B)$, the referent is the *enriched* hom-value — never the morphism weight in the case category.

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

The composition inequality violation here is linguistically meaningful: it tells us that the NOM→ACC→DAT chain overestimates the direct NOM→DAT relatedness, reflecting the typological fact that subject–recipient identity (e.g., in benefactive constructions) is more restricted than the product of agent–patient and patient–recipient proximities. \autoref{fig:enriched-heatmap} shows the pairwise hom-values $\mathcal{C}(A,B) \in [0,1]$ between case roles as an annotated heatmap of the proximity matrix.

**Slavic syncretism as an empirical anchor for high hom-values.** The fourth row of \autoref{tbl:hom-value-interpretations} — *morphological predictability* — is most cleanly calibrated against Slavic case morphology. Where a paradigm collapses two morphological cells into one form, the morphological-predictability hom-value approaches its upper bound:

- **Russian masculine animate ACC = GEN** (e.g. *brata*, *čeloveka*) ⇒ $\mathcal{C}(\text{ACC}, \text{GEN}) \approx 1$ for that declension class.
- **Russian neuter NOM = ACC** (e.g. *okno* "window" identical in subject and direct-object position) ⇒ $\mathcal{C}(\text{NOM}, \text{ACC}) \approx 1$ for that paradigm.
- **Serbian/BCS dative–locative singular merger** in many declensions (e.g. *gradu* serves both *prema gradu* "toward-DAT the city" and *u gradu* "in-LOC the city") ⇒ $\mathcal{C}(\text{DAT}, \text{LOC}) \approx 1$.

These are not modelling choices: they are *observed* identifications of morphological cells, supplying directly-measurable upper bounds on the enriched hom-values for the corresponding role pairs. They co-exist with low hom-values for the same role pairs under the *distributional* or *proto-role* readings of \autoref{tbl:hom-value-interpretations} — a useful reminder that the four interpretations are projections of a richer multi-channel proximity, not competing definitions.

![Core and peripheral argument complexes emerge from enriched distributional hom-values. Annotated heatmap of the $8 \times 8$ matrix with entries $\mathcal{C}(A_i,A_j) \in [0,1]$ (YlOrRd scale; numeric labels in each cell). High-proximity blocks reveal the **core argument complex** (NOM--ACC--DAT: transitive and transfer morphisms) and the **peripheral complex** (LOC--INS--ABL: spatial and instrumental relations). GEN shows elevated proximity to both blocks via possessive modification; VOC shows high proximity to NOM (0.70, reflecting nominative-vocative morphological syncretism in many IE languages) but low proximity to the spatial-instrumental periphery (INS=0.20, LOC=0.15, ABL=0.15), reflecting its pragmatic rather than referential function. These hom-values assemble the similarity matrix $Z$ used for categorical magnitude in \autoref{sec:magnitude-homology} (\autoref{eq:eq-5-3}), with axioms \autoref{eq:eq-5-1}–\autoref{eq:eq-5-2}. Generated programmatically from `src.visualization.enriched_diagrams.render_enriched_heatmap()` applied to `EnrichedCategory` data (see `scripts/generate_diagrams.py`).](output/figures/enriched_hom_matrix.png){#fig:enriched-heatmap}
