# Module: `visualization` — Publication-Quality Figure Generation

> **Package**: `src.visualization`
> **Manuscript**: All sections (cross-cutting)
> **Dependencies**: `case_systems`, `cognitive`, `daif`, `enriched_cat`, `quantum`, `security`, `diagrams`
> **Test files**: `tests/test_visualization*.py`
> **Optional dependency**: `discopy` (for `discopy_diagrams.py`)

---

## Purpose

The `visualization` package generates all **30 publication-quality figures** in the manuscript (original 27 plus three pedagogical unpacking companions added for §3 / §4b / §4c; authoritative live count in `output/metrics.json::total_figures`). It is a cross-cutting module that imports from every other `src/` package to render mathematical structures as visual diagrams. All figures adhere to:

- **16pt minimum font size** (ADR-003)
- **Consistent color palette** via `styles.py`
- **Matplotlib-native** rendering (no external diagram tools required except optional `discopy`)

---

## Architecture

```text
visualization/
├── __init__.py                    # 28 exported symbols (+ optional discopy)
├── styles.py                      # CASE_COLORS, FONT_SIZE_FLOOR, typography constants
├── category_diagrams.py           # Case category directed graphs (§2)
├── functor_diagrams.py            # Alignment functor mappings (§2)
├── string_diagrams.py             # DisCoCat/DisCoCirc native renderers (§3–4)
├── discopy_diagrams.py            # DisCoPy diagram rendering (§3–4, optional)
├── complexity_plots.py            # Complexity radar + comparison charts (§9)
├── enriched_diagrams.py           # [0,1]-enriched heatmaps (§5)
├── active_inference_plots.py      # Scalar belief distributions (§7)
├── daif_plots.py                  # DAIF multi-panel visualizations (§7c)
├── quantum_plots.py               # Case POVM probabilities (§8)
├── security_plots.py              # Type violation analysis (§9b)
├── fluid_s_plots.py               # Contextual volition landscape (§2b)
└── syntactic_sentence_diagrams.py # Eight-construction syntactic panel (App A)
```

### Dependency Position

```text
All other src/ packages → visualization
```

`visualization` is the **terminal node** of the dependency DAG — it imports from everything else but nothing imports from it. This is by design: figure generation is a downstream consumer of all computational modules.

---

## Module Reference

### `styles.py` — Design System

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `CASE_COLORS` | `dict[str, str]` | Color assignments for each case role (NOM=#4C72B0, etc.) |
| `FONT_SIZE_FLOOR` | `int` | Minimum font size = 16pt (ADR-003) |

All other visualization modules import these constants for consistency.

### `category_diagrams.py` — Case Category Graphs (§2)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `render_case_category(cat, ax)` | Directed graph of a CaseCategory | Fig 1 |
| `render_alignment_comparison(alignments, ax)` | Side-by-side alignment comparison | Fig 2 |
| `render_composition_triangle(cat, f, g, ax)` | Composition triangle with weights | Fig 3 |

### `functor_diagrams.py` — Alignment Functor Mappings (§2)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `render_functor_diagram(functor, ax)` | Object/morphism mapping visualization | Fig 4–5 |

### `string_diagrams.py` — DisCoCat/DisCoCirc (§3–4)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `render_discocat_sentence(sentence, ax)` | Single-sentence string diagram | Fig 6 |
| `render_discourse_diagram(discourse, ax)` | Multi-sentence discourse circuit | Fig 10 |
| `render_discocirc_discourse(discourse, ax)` | DisCoCirc-style entity persistence | Fig 11 |
| `render_three_sentence_discourse(discourse, ax)` | Three-sentence discourse progression | Fig 12 |

### `discopy_diagrams.py` — DisCoPy Rendering (§3–4, optional)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `render_discopy_transitive(ax)` | Transitive sentence via DisCoPy | Fig 7 |
| `render_discopy_composition(ax)` | Functor composition diagram | Fig 8 |
| `render_discopy_snake(ax)` | Snake equation (compact closure) | Fig 9 |
| `render_discopy_passive(ax)` | Passive voice transformation | Fig 13 |
| `render_discopy_sentence_progression(ax)` | Sentence-by-sentence progression | — |
| `render_discopy_multilingual(ax)` | Cross-linguistic comparison | — |
| `render_discopy_ditransitive(ax)` | Three-argument verb | — |
| `render_discopy_discocirc_discourse(ax)` | DisCoCirc via DisCoPy | — |
| `get_diagram_metrics(diagram)` | Complexity metrics from DisCoPy | — |

> **Note**: `discopy` is an optional dependency. These functions are only available when `discopy` is installed. The `__init__.py` handles this via try/except.

### `complexity_plots.py` — Complexity Visualization (§9)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `render_syntactic_complexity_radar(metrics, ax)` | Radar chart of complexity dimensions | Fig 14 |
| `render_complexity_comparison(metrics_list, ax)` | Bar chart comparing constructions | Fig 15 |
| `render_normal_form_comparison(before, after, ax)` | Normal-form reduction comparison | Fig 16 |

### `enriched_diagrams.py` — Enriched Heatmaps (§5)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `render_enriched_heatmap(enriched_cat, ax)` | 8×8 proximity matrix heatmap | Fig 17 |

### `active_inference_plots.py` — Scalar Belief (§7)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `plot_belief_distribution(belief, …)` | Bar chart of case role probabilities (snapshot) | Diagnostics |
| `plot_alignment_frame_belief_dynamics(prior, trajectory, observation_sequence, …)` | 3-panel: P(frame), H(q), per-step F[q] + running-min envelope vs. evidence step | `active_inference_belief.png` (§7) |

### `daif_plots.py` — DAIF Panels (§7c)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `plot_belief_trajectory(result, ax)` | Belief evolution over VMP iterations | Fig 19 |
| `plot_free_energy_convergence(result, ax)` | Free energy vs. iteration | Fig 20 |
| `plot_erp_predictions(erp_profile, ax)` | N400/P600/LPC waveform panel | Fig 21 |

This is among the largest visualization modules (~23 KB), rendering the DAIF multi-panel figures.

### `quantum_plots.py` — POVM Visualization (§8)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `plot_povm_probabilities(povm, rho, ax)` | Bar chart of case probabilities | Fig 24 |

### `security_plots.py` — Security visualization (§9b)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `plot_type_violations(violations, ax)` | Type violation severity chart | Fig 25 |

### `fluid_s_plots.py` — Fluid-S Visualization (§2b)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `plot_fluid_s_volition_landscape(ax)` | 3D volition probability surface | Fig 26 |

### `syntactic_sentence_diagrams.py` — Construction Panel (App A)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `render_syntactic_panel(ax)` | Eight-construction panel with pregroup types | Fig 22 |

### `category_unpacking.py` — Pedagogical Unpacking Companions (§3, §4b, §4c)

Native-matplotlib multi-panel companions to the raw DisCoPy figures, each *unpacking* a central category-theoretic construction into pedagogical stages (raw types → parallel tensor → cups applied → normal form, etc.). All three are pure matplotlib (no DisCoPy dependency), colour-coded by case role, and render identically in every environment.

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `render_pregroup_reduction_unpacking(output_path=None, *, subject="Alice", verb="chases", obj="Bob")` | Four-panel pregroup-reduction walkthrough: raw word types, parallel tensor $\otimes$, cup contractions $\varepsilon_n$, normal-form sentence wire $s$ | Fig 23 (`pregroup_reduction_unpacking.png`; §3, §4) |
| `render_discocirc_entity_persistence(output_path=None)` | Three sentence panels plus a role-history ribbon tracking Alice (NOM→ACC→NOM) and Bob (ACC→NOM) across the canonical three-sentence DisCoCirc discourse | Fig 24 (`discocirc_entity_persistence.png`; §4c) |
| `render_snake_equation_unpacking(output_path=None)` | Three-panel visual derivation of the compact-closure snake equation $(\varepsilon_n \otimes 1_n) \circ (1_n \otimes \eta_n) = 1_n$ with explicit η (cap) and ε (cup) labels and an axiom recap | Fig 25 (`snake_equation_unpacking.png`; §4b) |

> **Design note:** These companions complement — rather than replace — the raw DisCoPy outputs (`discopy_transitive.png`, `discopy_snake.png`, `discopy_three_sentence_discourse.png`). The DisCoPy figures remain the *authoritative* type-theoretic proofs; the unpacking companions provide pedagogical decomposition for readers meeting pregroup reduction, the snake equation, or DisCoCirc entity persistence for the first time. See manuscript §3, §4b, §4c for the cross-references.

---

## Usage Examples

```python
import matplotlib.pyplot as plt
from src.case_systems import standard_case_category
from src.enriched_cat import standard_enriched_category
from src.visualization import (
    render_case_category,
    render_enriched_heatmap,
    plot_belief_distribution,
    CASE_COLORS,
)

# 1. Render a case category
fig, ax = plt.subplots(figsize=(10, 8))
cat = standard_case_category()
render_case_category(cat, ax)
plt.savefig("case_category.png", dpi=300, bbox_inches="tight")

# 2. Render enriched heatmap
fig, ax = plt.subplots(figsize=(8, 8))
enriched = standard_enriched_category()
render_enriched_heatmap(enriched, ax)
plt.savefig("enriched_heatmap.png", dpi=300, bbox_inches="tight")
```

---

## Related Documentation

- **Generated figures**: [manuscript_figure_index.md](../manuscript_figure_index.md) — all 30 figures (original 27 plus three pedagogical unpacking companions for §3 / §4b / §4c)
- **Extension guide**: [extension_guide.md](../extension_guide.md) — adding new figures
- **All upstream modules**: [`case_systems`](case_systems.md), [`cognitive`](cognitive.md), [`daif`](daif.md), [`diagrams`](diagrams.md), [`enriched_cat`](enriched_cat.md), [`quantum`](quantum.md), [`security`](security.md)
- **ADR-003**: Font size ≥ 16pt — [AGENTS.md](../AGENTS.md)

---

*Last updated: 2026-04-22. Source of truth: `src/visualization/__init__.py` (28 exported symbols, plus 10 additional optional DisCoPy renderers surfaced when `discopy` is installed).*
