# src/ — Scientific Source Code

All scientific business logic for the `cognitive_case_diagrams` project lives here, organized by manuscript section.

## Quick Import

```python
from src import (
    CaseRole, CaseCategory,
    standard_case_category, minimal_case_category, introductory_case_category,
    EnrichedCategory, standard_enriched_category,
    CaseDiagramBelief, CasePOVM, CaseFrameValidator,
)
from src.case_systems import FluidSFunctor, AlignmentFunctor
from src.visualization import (
    plot_belief_distribution,
    plot_alignment_frame_belief_dynamics,
    plot_povm_probabilities,
)
```

## Package Map

| Package | § | Purpose | Key Classes |
|---------|---|---------|-------------|
| [`case_systems/`](case_systems/) | §2 | Case theory, alignment, Fluid-S | `CaseRole`, `CaseCategory`, `AlignmentFunctor`, `FluidSFunctor` |
| [`diagrams/`](diagrams/) | §3–§4c | String diagrams, complexity, discourse | `Sentence`, `Discourse`, `DitransitiveSentence` |
| [`enriched_cat/`](enriched_cat/) | §5 | Enriched categories | `EnrichedCategory`, `standard_enriched_category` |
| [`topos_theory/`](topos_theory/) | §6 | Morita equivalence | `GeometricTheory`, `ClassifyingTopos` |
| [`cognitive/`](cognitive/) | §7 | Scalar active inference | `CaseDiagramBelief`, `variational_free_energy` |
| [`daif/`](daif/) | §7c | Distributional active inference | `DistributionalReturn`, `DAIFResult`, `ERPProfile` |
| [`quantum/`](quantum/) | §8 | POVM case assignment | `CasePOVM`, `case_probability` |
| [`security/`](security/) | §9b | Type violation detection | `TypeViolation`, `CaseFrameValidator` |
| [`visualization/`](visualization/) | All | Figure generation (30 publication figures) | `styles` + 14 renderer modules |

[`generate_manuscript_metrics.py`](generate_manuscript_metrics.py) writes `output/metrics.json` for manuscript `${variable}` injection (test counts, `daif` module counts).

Agent-oriented descriptors: [`SKILL.md`](SKILL.md) (hub) and one [`SKILL.md`](case_systems/SKILL.md) per subpackage.

See [`AGENTS.md`](AGENTS.md) for the full architecture guide and design principles.
