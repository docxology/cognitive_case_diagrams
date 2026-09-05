# visualization/ — Publication figures

**15** Python modules (plus `__init__.py`) implement manuscript figures — confirm with `ls src/visualization/*.py`. Re-exported names live in [`__init__.py`](__init__.py) (`__all__`); optional DisCoPy symbols are appended only when `discopy` imports succeed.

## Quick import

```python
from src.visualization import (
    render_case_category,
    plot_belief_distribution,
    plot_alignment_frame_belief_dynamics,
    plot_belief_trajectory,
    render_syntactic_panel,
)
```

## Module map (actual public entrypoints)

| Module | Primary API | Manuscript / output |
|--------|-------------|---------------------|
| `styles.py` | `CASE_COLORS`, `FONT_SIZE_FLOOR`, `FIGURE_DPI` (300), `DEFAULT_FIGSIZE`, `mathtext_safe_arrows` | Used by all renderers |
| `category_diagrams.py` | `render_case_category`, `render_alignment_comparison`, `render_composition_triangle` | §2 PNGs |
| `category_diagrams_config.py` | `CASE_MINIMAL_NODE_POSITIONS`, `CASE_MINIMAL_EDGE_LABEL_PREFIX`, `CASE_MINIMAL_LICENSED_CONNECTIONSTYLE` | Layout constants for `fig:case-minimal`; no renderers |
| `category_unpacking.py` | `render_pregroup_reduction_unpacking`, `render_discocirc_entity_persistence`, `render_snake_equation_unpacking` | §4 unpacking panels |
| `enriched_diagrams.py` | `render_enriched_heatmap` | `enriched_hom_matrix.png` |
| `functor_diagrams.py` | `render_functor_diagram` | `functor_alignment.png` |
| `string_diagrams.py` | `render_discocat_sentence`, `render_discourse_diagram`, `render_discocirc_discourse`, `render_three_sentence_discourse` | Native string diagrams |
| `discopy_diagrams.py` | `render_discopy_*`, `get_diagram_metrics` | DisCoPy PNGs (optional dep.) |
| `complexity_plots.py` | `render_complexity_comparison`, `render_syntactic_complexity_radar` | `complexity_comparison.png`, radar |
| `active_inference_plots.py` | `plot_belief_distribution`, `plot_alignment_frame_belief_dynamics` | `active_inference_belief.png` |
| `daif_plots.py` | `plot_belief_trajectory`, `plot_free_energy_convergence`, `plot_erp_predictions` | DAIF §7c PNGs |
| `quantum_plots.py` | `plot_povm_probabilities` | `quantum_povm_probabilities.png` |
| `security_plots.py` | `plot_case_interaction_graph`, `plot_monoidal_functor_security`, `plot_type_violations` | `security_type_violations.png` (from `plot_case_interaction_graph`), `monoidal_functor_security.png` (from `plot_monoidal_functor_security`); `plot_type_violations` ships no committed figure |
| `fluid_s_plots.py` | `plot_fluid_s_volition_landscape` | `fluid_s_volition_landscape.png` |
| `syntactic_sentence_diagrams.py` | `render_syntactic_panel` | `syntactic_case_panel.png` |

Full figure list: [`docs/manuscript_figure_index.md`](../../docs/manuscript_figure_index.md). Details: [`AGENTS.md`](AGENTS.md); [`SKILL.md`](SKILL.md) for agent routing.

## Contract

Render/plot functions accept `output_path: str | None` and write via
`savefig(..., dpi=FIGURE_DPI)` from `styles`. The **return type is not uniform** —
three conventions coexist, so check the annotation before consuming a result:

| Convention | Returns | Functions |
|------------|---------|-----------|
| Figure-returning | `matplotlib.figure.Figure` | all of `category_diagrams`, `enriched_diagrams`, `functor_diagrams`, `string_diagrams` |
| Path-returning | `str` (the written path, or `""` on an empty-input guard) | `category_unpacking`, `complexity_plots`, `active_inference_plots`, `daif_plots`, `quantum_plots`, `security_plots`, `fluid_s_plots`, `syntactic_sentence_diagrams` |
| Side-effect only | `None` | every `render_discopy_*` in `discopy_diagrams` (`get_diagram_metrics` returns `dict`) |

Re-derive the split with `inspect.signature(fn).return_annotation` rather than trusting this table after a refactor.
