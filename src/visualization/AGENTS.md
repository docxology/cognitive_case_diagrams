# AGENTS.md — src/visualization/

## Overview

Publication-quality matplotlib figures for *Cognitive Diagrams: Reviewing Categorical Accounts of Linguistic Case* ([`docs/manuscript/config.yaml`](../../docs/manuscript/config.yaml) `paper.title`). Orchestrator: [`scripts/generate_diagrams.py`](../../scripts/generate_diagrams.py). Inventory: [`docs/manuscript_figure_index.md`](../../docs/manuscript_figure_index.md).

**Public surface:** import from `src.visualization` — names are listed in [`__init__.py`](__init__.py) `__all__`. When `discopy` is installed, DisCoPy render helpers are also exported.

**Style:** use constants from [`styles.py`](styles.py) (`FONT_SIZE_FLOOR`, `FIGURE_DPI`, `CASE_COLORS`, …). Do not hardcode a single font face in new code; prefer `fontfamily="sans-serif"` so headless CI can resolve the stack (see project `tests/conftest.py`). For titles or NetworkX labels that include Unicode arrows, checkmarks, or composition (`→`, `✓`, `∘`, …), run them through `mathtext_safe_arrows()` so mathtext supplies glyphs when Helvetica is first in the stack. DisCoPy renders use `_glyph_safe_rc()` in [`discopy_diagrams.py`](discopy_diagrams.py) to prefer DejaVu during `draw`.

## Module inventory

### `styles.py`

Constants and helpers for consistent visual styling.

| Export | Type | Description |
|--------|------|-------------|
| `FONT_SIZE_FLOOR` | `int` (16) | Minimum font size for accessibility |
| `FONT_SIZE_TITLE` | `int` (20) | Title font size |
| `FONT_SIZE_LABEL` | `int` (16) | Axis label font size |
| `FONT_SIZE_ANNOTATION` | `int` (14) | Annotation font size |
| `CASE_COLORS` | `dict[str, str]` | Hex palette for 13 case roles (NOM–P) |
| `FIGURE_DPI` | `int` (300) | Publication-quality DPI |
| `DEFAULT_FIGSIZE` | `tuple` | `(10, 8)` default figure size |
| `WIDE_FIGSIZE` | `tuple` | `(14, 8)` wide layout |
| `COMPARISON_FIGSIZE` | `tuple` | `(16, 6)` side-by-side panels |
| `POLAR_FIGSIZE` | `tuple` | `(8, 8)` radar/polar charts |
| `NARROW_FIGSIZE` | `tuple` | `(9, 6)` two-column comparison bars |
| `SQUARE_FIGSIZE` | `tuple` | `(8, 6)` single compact charts |
| `DISCOPY_SINGLE_FIGSIZE` | `tuple` | `(10, 5)` single DisCoPy sentence |
| `DISCOPY_WIDE_FIGSIZE` | `tuple` | `(16, 6)` wide DisCoPy sentence |
| `DISCOPY_DISCOURSE_FIGSIZE` | `tuple` | `(22, 6)` multi-sentence discourse |
| `COLOR_EDGE`, `COLOR_TEXT`, … | `str` | Semantic colour tokens |
| `COLOR_SEVERITY_HIGH/MED/LOW` | `str` | Severity tier colours (§9b) |
| `SEVERITY_HIGH_THRESHOLD` | `float` (0.8) | Severity colour cutoff |
| `SEVERITY_MED_THRESHOLD` | `float` (0.5) | Severity colour cutoff |
| `BAR_ALPHA`, `BAR_WIDTH_*` | `float` | Bar chart layout constants |
| `GRID_ALPHA`, `LINE_WIDTH_*`, `MARKER_SIZE` | `float` | Axis/grid constants |
| `HEATMAP_TEXT_PIVOT` | `float` (0.6) | White-text threshold for heatmaps |
| `FLUID_S_AGENT_THRESHOLD` | `float` (0.5) | Fluid-S decision boundary |
| `mathtext_safe_arrows(text) -> str` | function | Replace Unicode symbols with mathtext |

### `category_diagrams.py`

NetworkX `DiGraph` + matplotlib renderings of case categories as directed graphs.

| Function | Signature | Description |
|----------|-----------|-------------|
| `render_case_category` | `(category, output_path=None, title=None, show_admissibility=True, extra_prohibited=None, figsize=None, node_positions=None, edge_label_prefix=None, licensed_connectionstyle=None) -> Figure` | Render a `CaseCategory` as a directed graph with licensed (solid) and prohibited (dashed) edges |
| `render_alignment_comparison` | `(output_path=None) -> Figure` | Side-by-side comparison of alignment typologies (categories are built internally) |
| `render_composition_triangle` | `(output_path=None) -> Figure` | Morphism composition triangle diagram (category fixed internally) |

Layout constants for `fig:case-minimal` live in
[`category_diagrams_config.py`](category_diagrams_config.py)
(`CASE_MINIMAL_NODE_POSITIONS`, `CASE_MINIMAL_EDGE_LABEL_PREFIX`,
`CASE_MINIMAL_LICENSED_CONNECTIONSTYLE`); pass them through the matching
`render_case_category` keywords.

### `enriched_diagrams.py`

Heatmap visualization for enriched category proximity matrices.

| Function | Signature | Description |
|----------|-----------|-------------|
| `render_enriched_heatmap` | `(enriched, output_path=None, title=None) -> Figure` | Annotated heatmap of `[0,1]`-valued hom-weights |

### `functor_diagrams.py`

Dual-panel functor mapping diagrams.

| Function | Signature | Description |
|----------|-----------|-------------|
| `render_functor_diagram` | `(functor, output_path=None, title=None) -> Figure` | Single-Axes dual-panel layout; dashed `FancyArrowPatch` from `functor.object_map`, staggered targets |

### `string_diagrams.py`

Native matplotlib string diagram renderings (no DisCoPy dependency).

| Function | Signature | Description |
|----------|-----------|-------------|
| `render_discocat_sentence` | `(sentence, output_path=None, title=None) -> Figure` | DisCoCat-style sentence as box/wire diagram |
| `render_discourse_diagram` | `(discourse, output_path=None, title=None) -> Figure` | Multi-sentence discourse with entity wires |
| `render_discocirc_discourse` | `(output_path=None) -> Figure` | DisCoCirc-style discourse with persistent entity state wires (discourse fixed internally) |
| `render_three_sentence_discourse` | `(output_path=None) -> Figure` | Three-sentence Alice/Bob canonical example |

### `discopy_diagrams.py`

Optional DisCoPy-based diagram renderings (requires `discopy`).

| Function | Signature | Description |
|----------|-----------|-------------|
These render for side effect only — every `render_discopy_*` returns `None`.

| Function | Signature | Description |
|----------|-----------|-------------|
| `render_discopy_transitive` | `(output_path=None) -> None` | Transitive sentence diagram |
| `render_discopy_composition` | `(subject='Alice', verb='chases', obj='Bob', output_path=None) -> None` | Morphism composition diagram |
| `render_discopy_snake` | `(output_path=None) -> None` | Snake equation (compact closure) |
| `render_discopy_passive` | `(output_path=None) -> None` | Passivization as swap morphism |
| `render_discopy_sentence_progression` | `(output_path=None) -> None` | Progressive sentence type build-up |
| `render_discopy_multilingual` | `(output_path=None) -> None` | Cross-linguistic type comparison |
| `render_discopy_ditransitive` | `(output_path=None) -> None` | Ditransitive (DAT) sentence diagram |
| `render_discopy_discocirc_discourse` | `(output_path=None) -> None` | DisCoPy DisCoCirc discourse rendering |
| `render_discopy_three_sentence_discourse` | `(output_path=None) -> None` | Three-sentence DisCoPy discourse |
| `get_diagram_metrics` | `(diagram) -> dict` | Extract box/cup/cap counts and complexity score |

### `complexity_plots.py`

Bar charts and radar plots for diagram complexity metrics.

| Function | Signature | Description |
|----------|-----------|-------------|
| `render_complexity_comparison` | `(labels, box_counts, word_counts, cup_counts, sentences, output_path) -> str` | Grouped bar chart comparing construction complexities |
| `render_normal_form_comparison` | `(labels, original_counts, normal_form_counts, output_path) -> str` | Normal-form vs raw complexity comparison |
| `render_syntactic_complexity_radar` | `(labels, metrics, output_path) -> str` | Radar plot of multi-axis complexity scores |

### `active_inference_plots.py`

Scalar belief and alignment dynamics plots for §7.

| Function | Signature | Description |
|----------|-----------|-------------|
| `plot_belief_distribution` | `(belief, title=…, output_path=None) -> str` | Bar chart of case role belief probabilities |
| `plot_alignment_frame_belief_dynamics` | `(prior, trajectory, observation_sequence, *, frame_labels=None, evidence_labels=None, figsize=(14, 11), title=…, output_path=None) -> str` | Multi-frame belief dynamics over sentence processing |

### `daif_plots.py`

Distributional Active Inference result plots for §7c.

| Function | Signature | Description |
|----------|-----------|-------------|
| `plot_belief_trajectory` | `(trajectory, word_labels=None, gloss_labels=None, title=…, figsize=(14, 12), output_path=None) -> str` | Distributional belief evolution over parsing steps |
| `plot_free_energy_convergence` | `(fe_trajectory, word_boundaries=None, word_labels=None, kl_trajectory=None, loglik_trajectory=None, title=…, figsize=(16, 7), output_path=None) -> str` | Free energy convergence curve |
| `plot_erp_predictions` | `(role_names, enriched_weights, prediction_errors, n400_amplitudes=None, p600_amplitudes=None, title=…, figsize=(18, 7), output_path=None) -> str` | P600/N400 ERP amplitude predictions |

### `quantum_plots.py`

Quantum semantics visualizations for §8b.

| Function | Signature | Description |
|----------|-----------|-------------|
| `plot_povm_probabilities` | `(povm, density_matrix, title=…, output_path=None) -> str` | Case assignment probabilities from POVM measurement; requires 2D complex density matrix |

### `security_plots.py`

Cognitive security visualizations for §9b.

| Function | Signature | Description |
|----------|-----------|-------------|
| `plot_case_interaction_graph` | `(output_path=None) -> str` | Two-panel case interaction graph: legitimate NOM→INS→ACC→DAT trace vs. an ACC→INS injection arc. **This is the function that produces `security_type_violations.png`** (see `scripts/generate_quantum_figures.py`) |
| `plot_monoidal_functor_security` | `(functor, title=…, output_path=None) -> str` | `MonoidalFunctor` tensor-preservation check; produces `monoidal_functor_security.png` |
| `plot_type_violations` | `(violations, title=…, output_path=None) -> str` | Type violation severity bar chart. Public API, but **no committed figure is generated from it** — do not cite it as the source of `security_type_violations.png` |

`plot_case_interaction_graph` is not re-exported in `__init__.py` `__all__`; import
it from `security_plots` directly, as the generator script does.

### `fluid_s_plots.py`

Fluid-S alignment system visualization.

| Function | Signature | Description |
|----------|-----------|-------------|
| `plot_fluid_s_volition_landscape` | `(functors=None, probabilities=None, verb_names=None, title=…, output_path=None) -> str` | 2D volition landscape with ergative/absolutive decision boundary |

### `syntactic_sentence_diagrams.py`

Appendix A panel figures: syntactic trees and pregroup derivations.

| Function | Signature | Description |
|----------|-----------|-------------|
| `render_syntactic_panel` | `(output_path=None, panels=None) -> str` | Eight-panel grid of tree + type derivation pairs |

### `category_unpacking.py`

Step-by-step "unpacking" panels for §4 categorical machinery.

| Function | Signature | Description |
|----------|-----------|-------------|
| `render_pregroup_reduction_unpacking` | `(output_path=None, *, subject='Alice', verb='chases', obj='Bob') -> str` | Pregroup reduction, contraction by contraction |
| `render_discocirc_entity_persistence` | `(output_path=None) -> str` | Entity-wire persistence across a DisCoCirc discourse |
| `render_snake_equation_unpacking` | `(output_path=None) -> str` | Snake equation unpacked into its cup/cap steps |

### `category_diagrams_config.py`

Layout constants only — no renderers. Exports `CASE_MINIMAL_NODE_POSITIONS`,
`CASE_MINIMAL_EDGE_LABEL_PREFIX` and `CASE_MINIMAL_LICENSED_CONNECTIONSTYLE`, fed
to the matching `render_case_category` keywords for `fig:case-minimal`.

## Patterns

- **Return value: not uniform.** Three conventions coexist —
  `category_diagrams`, `enriched_diagrams`, `functor_diagrams` and
  `string_diagrams` return a `matplotlib.figure.Figure`; the plot/panel modules
  return the written path as `str` (or `""` on an empty-input guard); every
  `render_discopy_*` returns `None` and writes for side effect
  (`get_diagram_metrics` returns `dict`). Check
  `inspect.signature(fn).return_annotation` before consuming a result.
- **Tests:** `tests/test_visualization_*.py` mirror modules; no mocks.
- **New figure:** implement in the module matching manuscript §, export in `__init__.py`, wire `generate_diagrams.py` / domain script, add test, add `output/figures/...` reference + `{#fig:...}` in manuscript, update `docs/manuscript_figure_index.md`.

## Quantum POVM gotcha

`plot_povm_probabilities(povm, density_matrix, ...)` requires a **2D** complex density matrix (`np.ndarray` shape `(n,n)`), not a 1D state vector. Pure states: `rho = np.outer(v, v.conj())`.

## Native string diagrams (`string_diagrams.py`)

Case-role fill colours follow `CASE_COLORS`; there is no separate axes legend on these figures. Manuscript captions carry the reading (e.g. wire labels and role names on discourse plots).

## See also

- [`README.md`](README.md) — quick module map
- [`docs/api_reference.md`](../../docs/api_reference.md) — prose API (if present for visualization section)
