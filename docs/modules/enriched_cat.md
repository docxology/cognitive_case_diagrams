# enriched_cat: implementation reference

Candidate hom-matrices, explicit multiplicative composition checks, max-product closure, and matrix magnitude. The standard matrix is synthetic and violates composition before closure. Pseudoinverse magnitudes require valid left/right weighting residuals. Threshold clusters are weak connected components, not pairwise-close cliques.

| Source module | Defined entry points |
| :--- | :--- |
| [enriched.py](../../src/enriched_cat/enriched.py) | `EnrichedCategory`, `standard_enriched_category` |

See the [package guide](../../src/enriched_cat/README.md), [method contracts](../method_contracts.md), and [claim ledger](../claim_ledger.md). These describe implementation scope; the manuscript distinguishes implemented examples from proposed extensions.
