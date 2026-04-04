# visualization/ — Publication figures

**13** Python modules (plus `__init__.py`) implement manuscript figures. Re-exported names live in [`__init__.py`](__init__.py) (`__all__`); optional DisCoPy symbols are appended only when `discopy` imports succeed.

## Quick import

```python
from src.visualization import (
    render_case_category,
    plot_belief_distribution,
    plot_belief_trajectory,
    render_syntactic_panel,
)
```

## Module map (actual public entrypoints)

| Module | Primary API | Manuscript / output |
|--------|-------------|---------------------|
| `styles.py` | `CASE_COLORS`, `FONT_SIZE_FLOOR`, `FIGURE_DPI`, … | Used by all renderers |
| `category_diagrams.py` | `render_case_category`, `render_alignment_comparison`, `render_composition_triangle` | §2 PNGs |
| `enriched_diagrams.py` | `render_enriched_heatmap` | `enriched_hom_matrix.png` |
| `functor_diagrams.py` | `render_functor_diagram` | `functor_alignment.png` |
| `string_diagrams.py` | `render_discocat_sentence`, `render_discourse_diagram`, `render_discocirc_discourse`, `render_three_sentence_discourse` | Native string diagrams |
| `discopy_diagrams.py` | `render_discopy_*`, `get_diagram_metrics` | DisCoPy PNGs (optional dep.) |
| `complexity_plots.py` | `render_complexity_comparison`, `render_syntactic_complexity_radar` | `complexity_comparison.png`, radar |
| `active_inference_plots.py` | `plot_belief_distribution` | `active_inference_belief.png` |
| `daif_plots.py` | `plot_belief_trajectory`, `plot_free_energy_convergence`, `plot_erp_predictions` | DAIF §7c PNGs |
| `quantum_plots.py` | `plot_povm_probabilities` | `quantum_povm_probabilities.png` |
| `security_plots.py` | `plot_type_violations` | `security_type_violations.png` |
| `fluid_s_plots.py` | `plot_fluid_s_volition_landscape` | `fluid_s_volition_landscape.png` |
| `syntactic_sentence_diagrams.py` | `render_syntactic_panel` | `syntactic_case_panel.png` |

Full figure list: [`docs/manuscript_figure_index.md`](../../docs/manuscript_figure_index.md). Details: [`AGENTS.md`](AGENTS.md); [`SKILL.md`](SKILL.md) for agent routing.

## Contract

Render/plot functions typically accept `output_path: str | None`, write via `savefig(..., dpi=FIGURE_DPI)` from `styles`, and return the path string (see each docstring).
