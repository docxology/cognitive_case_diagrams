# Architecture and data flow

This is a set of small mathematical examples, not a single trained inference pipeline. `case_systems` provides shared role objects. `diagrams`, `enriched_cat`, `topos_theory`, `cognitive`, `daif`, `quantum`, and `security` implement distinct constructions; `visualization` renders them. The exact import graph is determined by source, including local imports in figure-data helpers. It is not the previously claimed strictly enforced package DAG.

Synthetic fixture writers feed plotting functions. Domain scripts invoke those writers. `generate_diagrams.py` records generated paths, manuscript labels, and SHA-256 hashes. Coverage and source inspection feed `generate_manuscript_metrics.py`. Injection substitutes braced metrics into numbered chapters; artifact validation verifies parity before rendering. The separate template engine consumes `output/manuscript/` and `output/figures/`.

Canonical sources are source code, tests, manuscript chapters, bibliography, and configuration. Outputs are derived and must be regenerated after a relevant source change. A passing structural artifact gate is distinct from a successful renderer and a visual PDF review.

See [API index](api_reference.md), [extension guide](extension_guide.md), and [method contracts](method_contracts.md).

## Package map

Generated on 2026-11-12 from the `import` statements under `src/`. An arrow from A to B means code in A imports B; arrows already implied by a longer path are left out, so the picture shows layering rather than every edge. It shows 14 of the package's 24 top-level parts: the largest ones that import or are imported by others.

```mermaid
flowchart TB
    accTitle: Internal dependency map of the src package in cognitive_case_diagrams
    accDescr: Generated from import statements in src. Each box is a subpackage or module of the package; an arrow from A to B means code in A imports B; arrows already implied by a longer path are omitted. Most-imported: case_systems, enriched_cat, cognitive.
    n_visualization["visualization/"]
    n_experiments["experiments/"]
    n_integrations["integrations/"]
    n_daif["daif/"]
    n_diagrams["diagrams/"]
    n_case_systems["case_systems/"]
    n_manuscript_variables["manuscript_variables.py"]
    n_generate_manuscript_metrics["generate_manuscript_metrics.py"]
    n_cognitive["cognitive/"]
    n_aggregation["aggregation/"]
    n_quantum["quantum/"]
    n_enriched_cat["enriched_cat/"]
    n_evidence_status["evidence_status.py"]
    n_release_bundle["release_bundle.py"]
    n_daif --> n_cognitive
    n_experiments --> n_cognitive
    n_experiments --> n_aggregation
    n_quantum --> n_case_systems
    n_visualization --> n_cognitive
    n_diagrams --> n_case_systems
    n_experiments --> n_quantum
    n_manuscript_variables --> n_experiments
    n_visualization --> n_diagrams
    n_cognitive --> n_enriched_cat
    n_cognitive --> n_daif
    n_enriched_cat --> n_case_systems
    n_evidence_status --> n_experiments
    n_evidence_status --> n_release_bundle
    n_generate_manuscript_metrics --> n_manuscript_variables
    n_generate_manuscript_metrics --> n_visualization
    n_integrations --> n_evidence_status
    n_visualization --> n_quantum
```
