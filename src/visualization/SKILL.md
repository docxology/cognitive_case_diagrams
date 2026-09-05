---
name: ccd-visualization
description: Publication figures for cognitive_case_diagrams — case graphs, enriched heatmaps, string/DisCoPy diagrams, complexity plots, active inference and DAIF panels, quantum POVM, security, Fluid-S, syntactic App A panel. Use when generating manuscript figures from src.
---

# `src/visualization/`

## When to use

- Rendering any project figure referenced from manuscript or scripts: category layouts, functor maps, DisCoCat/DisCoCirc diagrams, complexity radars, belief/ERP plots, etc.

## Modules (15 besides `__init__.py`)

- `styles` — palette and typography floors (`FIGURE_DPI` is **300**)  
- `category_diagrams`, `category_diagrams_config` (layout constants only), `enriched_diagrams`, `functor_diagrams`  
- `string_diagrams` — matplotlib-native DisCoCat/DisCoCirc  
- `category_unpacking` — §4 step-by-step unpacking panels  
- `discopy_diagrams` — optional DisCoPy (extra imports when installed)  
- `complexity_plots`, `active_inference_plots`, `daif_plots`  
- `quantum_plots`, `security_plots`, `fluid_s_plots`  
- `syntactic_sentence_diagrams` — Appendix A panel  

Return types differ by module (`Figure` / `str` / `None`) — see [`AGENTS.md`](AGENTS.md).

## Primary imports (always available)

```python
from src.visualization import (
    CASE_COLORS, FONT_SIZE_FLOOR,
    render_case_category, render_enriched_heatmap, render_functor_diagram,
    render_discocat_sentence, render_discourse_diagram,
    plot_belief_distribution, plot_alignment_frame_belief_dynamics,
    plot_erp_predictions, plot_povm_probabilities,
    render_syntactic_panel,
    # ... see __init__.__all__
)
```

Optional: `render_discopy_*`, `get_diagram_metrics` when DisCoPy is installed.

## See also

- [`AGENTS.md`](AGENTS.md) · [`README.md`](README.md) · [`docs/manuscript_figure_index.md`](../../docs/manuscript_figure_index.md)
