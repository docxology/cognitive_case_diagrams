# AGENTS.md — src/visualization/

## Overview

Publication-quality matplotlib figures for *Compositional Approaches to Linguistic Case for Cognitive Modeling* ([`manuscript/config.yaml`](../../manuscript/config.yaml) `paper.title`). Orchestrator: [`scripts/generate_diagrams.py`](../../scripts/generate_diagrams.py). Inventory: [`docs/manuscript_figure_index.md`](../../docs/manuscript_figure_index.md).

**Public surface:** import from `src.visualization` — names are listed in [`__init__.py`](__init__.py) `__all__`. When `discopy` is installed, DisCoPy render helpers are also exported.

**Style:** use constants from [`styles.py`](styles.py) (`FONT_SIZE_FLOOR`, `FIGURE_DPI`, `CASE_COLORS`, …). Do not hardcode a single font face in new code; prefer `fontfamily="sans-serif"` so headless CI can resolve the stack (see project `tests/conftest.py`). For titles or NetworkX labels that include Unicode arrows, checkmarks, or composition (`→`, `✓`, `∘`, …), run them through `mathtext_safe_arrows()` so mathtext supplies glyphs when Helvetica is first in the stack. DisCoPy renders use `_glyph_safe_rc()` in [`discopy_diagrams.py`](discopy_diagrams.py) to prefer DejaVu during `draw`.

## Module inventory (actual filenames)

| Module | Key entrypoints | Notes |
|--------|-----------------|--------|
| `styles.py` | Typography and colour constants | ADR-003: label floor 16pt |
| `category_diagrams.py` | `render_case_category` (`extra_prohibited`, `figsize`, `node_positions`, `edge_label_prefix`, `licensed_connectionstyle`), `render_alignment_comparison`, `render_composition_triangle` | NetworkX `DiGraph` + matplotlib; licensed edges use `arrowstyle="-|>"` and `arrowsize=24` (prohibited dashed: 18); optional fixed layout and per-edge `connectionstyle`; caption note on arrow direction and Mor(𝒞); default prohibited edges only if both roles exist |
| `enriched_diagrams.py` | `render_enriched_heatmap` | Proximity / graph |
| `functor_diagrams.py` | `render_functor_diagram` | Dual-panel functor |
| `string_diagrams.py` | `render_discocat_sentence`, `render_discourse_diagram`, `render_discocirc_discourse`, `render_three_sentence_discourse` | No DisCoPy required |
| `discopy_diagrams.py` | `render_discopy_transitive`, …, `get_diagram_metrics` | Optional `discopy` |
| `complexity_plots.py` | `render_complexity_comparison`, `render_syntactic_complexity_radar` | Bar / radar |
| `active_inference_plots.py` | `plot_belief_distribution` | Scalar `CaseDiagramBelief` |
| `daif_plots.py` | `plot_belief_trajectory`, `plot_free_energy_convergence`, `plot_erp_predictions` | Uses `daif` + `cognitive` |
| `quantum_plots.py` | `plot_povm_probabilities` | 2D density matrix required |
| `security_plots.py` | `plot_type_violations` | |
| `fluid_s_plots.py` | `plot_fluid_s_volition_landscape` | |
| `syntactic_sentence_diagrams.py` | `render_syntactic_panel` | Appendix A eight-panel |

## Patterns

- **Return value:** most functions return `str` path after `savefig`, or `""` on empty guard inputs (see per-module docstrings).
- **Tests:** `tests/test_visualization_*.py` mirror modules; no mocks.
- **New figure:** implement in the module matching manuscript §, export in `__init__.py`, wire `generate_diagrams.py` / domain script, add test, add `output/figures/...` reference + `{#fig:...}` in manuscript, update `docs/manuscript_figure_index.md`.

## Quantum POVM gotcha

`plot_povm_probabilities(povm, density_matrix, ...)` requires a **2D** complex density matrix (`np.ndarray` shape `(n,n)`), not a 1D state vector. Pure states: `rho = np.outer(v, v.conj())`.

## Native string diagrams (`string_diagrams.py`)

Case-role fill colours follow `CASE_COLORS`; there is no separate axes legend on these figures. Manuscript captions carry the reading (e.g. wire labels and role names on discourse plots).

## See also

- [`README.md`](README.md) — quick module map  
- [`docs/api_reference.md`](../../docs/api_reference.md) — prose API (if present for visualization section)
