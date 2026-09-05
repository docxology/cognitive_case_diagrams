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
├── __init__.py                    # 27 exported symbols (+ 10 optional DisCoPy names)
├── styles.py                      # CASE_COLORS, FONT_SIZE_FLOOR, typography constants
├── category_diagrams.py           # Case category directed graphs (§2)
├── category_diagrams_config.py    # CASE_MINIMAL_* layout constants for Figure 2
├── category_unpacking.py          # Pedagogical unpacking companions (§3, §4b, §4c)
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
| `FONT_SIZE_FLOOR` | `int` | Minimum font size = 16 (ADR-003) |
| `FONT_SIZE_LABEL` / `FONT_SIZE_TITLE` / `FONT_SIZE_ANNOTATION` | `int` | 16 / 20 / 14 |
| `FIGURE_DPI` | `int` | 300 — export resolution |
| `DEFAULT_FIGSIZE` | `tuple[int, int]` | (10, 8); `WIDE_FIGSIZE`, `POLAR_FIGSIZE`, `DISCOPY_*_FIGSIZE` etc. cover the other shapes |

Only `CASE_COLORS` and `FONT_SIZE_FLOOR` are re-exported from the package
`__init__.py`; the rest are imported from `.styles` directly. The full constant
table, including the colour and threshold groups, lives in
`src/visualization/AGENTS.md`. All other visualization modules import these
constants rather than hardcoding values.

### `category_diagrams.py` — Case Category Graphs (§2)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `render_case_category(category, output_path=None, …)` | Directed graph of a `CaseCategory` (layout overridable via `node_positions`, `edge_label_prefix`, …) | Fig 1, Fig 2 |
| `render_alignment_comparison(output_path=None)` | Side-by-side accusative / ergative / tripartite comparison | Fig 4 |
| `render_composition_triangle(output_path=None)` | Composition triangle with weights | Fig 5 |

### `functor_diagrams.py` — Alignment Functor Mappings (§2)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `render_functor_diagram(functor, output_path=None, title=None)` | Object/morphism mapping visualization | Fig 3 |

### `string_diagrams.py` — DisCoCat/DisCoCirc (§3–4)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `render_discocat_sentence(sentence, output_path=None, title=None)` | Single-sentence string diagram | Fig 20 |
| `render_discourse_diagram(discourse, output_path=None, title=None)` | Multi-sentence discourse circuit | — (no committed figure) |
| `render_discocirc_discourse(output_path=None)` | DisCoCirc-style entity persistence | Fig 21 |
| `render_three_sentence_discourse(output_path=None)` | Three-sentence discourse progression | — (no committed figure) |

### `discopy_diagrams.py` — DisCoPy Rendering (§3–4, optional)

All nine renderers take `output_path=None` and return `None` (they write the PNG themselves).

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `render_discopy_transitive(output_path=None)` | Transitive sentence via DisCoPy | Fig 6 |
| `render_discopy_composition(output_path=None)` | DisCoCat meaning composition | Fig 7 |
| `render_discopy_snake(output_path=None)` | Snake equation (compact closure) | Fig 8 |
| `render_discopy_passive(output_path=None)` | Passive voice transformation | Fig 9 |
| `render_discopy_ditransitive(output_path=None)` | Three-argument verb | Fig 10 |
| `render_discopy_multilingual(output_path=None)` | Cross-linguistic comparison | Fig 11 |
| `render_discopy_sentence_progression(output_path=None)` | Sentence-by-sentence progression | Fig 6b |
| `render_discopy_discocirc_discourse(output_path=None)` | DisCoCirc via DisCoPy | Fig 13 |
| `render_discopy_three_sentence_discourse(output_path=None)` | Three-sentence DisCoPy tensor | Fig 14 |
| `get_diagram_metrics(diagram)` | Complexity metrics from a DisCoPy diagram (`→ dict`) | — |

> **Note**: `discopy` is an optional dependency. These functions are only available when `discopy` is installed. The `__init__.py` handles this via try/except.

### `complexity_plots.py` — Complexity Visualization (§9)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `render_syntactic_complexity_radar(labels, metrics, output_path)` | Radar chart of complexity dimensions | — (no committed figure) |
| `render_complexity_comparison(labels, box_counts, word_counts, cup_counts, sentences, output_path)` | Bar chart comparing constructions | Fig 12 |
| `render_normal_form_comparison(labels, original_counts, normal_form_counts, output_path)` | Normal-form reduction comparison | — (no committed figure) |

### `enriched_diagrams.py` — Enriched Heatmaps (§5)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `render_enriched_heatmap(enriched, output_path=None)` | 8×8 proximity matrix heatmap | Fig 15 |

### `active_inference_plots.py` — Scalar Belief (§7)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `plot_belief_distribution(belief, title=…, output_path=None)` | Bar chart of case role probabilities (snapshot) | — (diagnostics only) |
| `plot_alignment_frame_belief_dynamics(prior, trajectory, observation_sequence, …)` | 3-panel: P(frame), H(q), per-step F[q] + running-min envelope vs. evidence step | Fig 17 (`active_inference_belief.png`, §7) |

### `daif_plots.py` — DAIF Panels (§7c)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `plot_belief_trajectory(trajectory, word_labels=None, …, output_path=None)` | Word-by-word belief evolution: stacked P(role), H[q], uncertainty fan | Fig 17b |
| `plot_free_energy_convergence(fe_trajectory, …, kl_trajectory=None, loglik_trajectory=None, output_path=None)` | Measured free energy vs. iteration, plus the KL / log-likelihood decomposition | Fig 17c |
| `plot_erp_predictions(role_names, enriched_weights, prediction_errors, n400_amplitudes=None, p600_amplitudes=None, …)` | 3-panel: illustrative ERP waveforms, weight-vs-DPE scatter, predicted-vs-literature N400/P600 bars | Fig 17d |

Each takes the measured trajectories/arrays directly, not a `DAIFResult`. This is the
largest visualization module (~23 KB), rendering the DAIF multi-panel figures.

### `quantum_plots.py` — POVM Visualization (§8)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `plot_povm_probabilities(povm, density_matrix, title=…, output_path=None)` | Bar chart of case probabilities Tr(E_c ρ) | Fig 18 |

### `security_plots.py` — Security visualization (§9b)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `plot_case_interaction_graph(output_path=None)` | Two-panel case interaction graph: legitimate NOM→INS→ACC→DAT trace vs. the illicit ACC→INS injection arc | Fig 19 (`security_type_violations.png`) |
| `plot_monoidal_functor_security(functor, title=…, output_path=None)` | Monoidal-functor object map + tensor-preservation grid | Fig 19b |
| `plot_type_violations(violations, title=…, output_path=None)` | Type violation severity bar chart | — (no committed figure) |

> **Note**: `plot_case_interaction_graph` is not re-exported from the package
> `__init__.py`; import it from `src.visualization.security_plots` (as
> `scripts/generate_quantum_figures.py` does).

### `fluid_s_plots.py` — Fluid-S Visualization (§2b)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `plot_fluid_s_volition_landscape(…, output_path=None)` | 2D volition × proto-agentivity heatmap of P(ERG) with the functor decision boundary and Bats verb exemplars | Fig 16 |

### `syntactic_sentence_diagrams.py` — Construction Panel (App A)

| Function | Description | Figures |
| -------- | ----------- | ------- |
| `render_syntactic_panel(output_path=None, panels=None)` | Eight-construction panel with pregroup types | Fig 22 |

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

Render functions own their own figure and saving — pass `output_path`, do not pass
an `Axes`.

```python
from src.case_systems import standard_case_category
from src.enriched_cat import standard_enriched_category
from src.visualization import (
    render_case_category,
    render_enriched_heatmap,
    CASE_COLORS,
)

# 1. Render a case category (writes the PNG at FIGURE_DPI, returns the Figure)
cat = standard_case_category()
fig = render_case_category(cat, output_path="output/figures/case_category_standard.png")

# 2. Render the enriched hom-proximity heatmap
enriched = standard_enriched_category()
fig = render_enriched_heatmap(enriched, output_path="output/figures/enriched_hom_matrix.png")

# 3. Colours are shared across every renderer
print(CASE_COLORS["NOM"])
```

Return types differ by module: the `render_*` category/string-diagram functions
return a `matplotlib.figure.Figure`, the `plot_*` and panel functions return the
output path as `str`, and the optional `render_discopy_*` functions return `None`.

---

## Related Documentation

- **Generated figures**: [manuscript_figure_index.md](../manuscript_figure_index.md) — all 30 figures (original 27 plus three pedagogical unpacking companions for §3 / §4b / §4c)
- **Extension guide**: [extension_guide.md](../extension_guide.md) — adding new figures
- **All upstream modules**: [`case_systems`](case_systems.md), [`cognitive`](cognitive.md), [`daif`](daif.md), [`diagrams`](diagrams.md), [`enriched_cat`](enriched_cat.md), [`quantum`](quantum.md), [`security`](security.md)
- **ADR-003**: Font size ≥ 16pt — [AGENTS.md](../AGENTS.md)

---

*Last updated: 2026-04-22. Source of truth: `src/visualization/__init__.py` (27 exported symbols, plus 10 additional optional DisCoPy names surfaced when `discopy` is installed).*
