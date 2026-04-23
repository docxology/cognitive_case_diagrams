"""Visualization subpackage for publication-quality figure generation.

Modules:
    styles: Color palette and typography constants
    category_diagrams: Case category directed graphs
    enriched_diagrams: [0,1]-enriched heatmaps
    functor_diagrams: Alignment functor mappings
    string_diagrams: DisCoCat/DisCoCirc renderers (matplotlib-native)
    discopy_diagrams: DisCoPy diagram rendering (optional dependency)
    complexity_plots: Complexity and normal-form comparison charts, radar plots
    active_inference_plots: Scalar beliefs — bar snapshot + alignment-frame dynamics (§7)
    daif_plots: Distributional active inference panels (§7c)
    quantum_plots: Case POVM probabilities
    security_plots: Type violation analysis
    fluid_s_plots: Contextual volition alignment
    syntactic_sentence_diagrams: Eight-construction syntactic + pregroup panel (App A)
    category_unpacking: Multi-panel pedagogical unpackings of key category-theoretic
        constructions (pregroup reduction, DisCoCirc entity persistence, snake equation)
"""

from __future__ import annotations

from .styles import CASE_COLORS, FONT_SIZE_FLOOR
from .category_diagrams import (
    render_case_category,
    render_alignment_comparison,
    render_composition_triangle,
)
from .enriched_diagrams import render_enriched_heatmap
from .functor_diagrams import render_functor_diagram
from .string_diagrams import (
    render_discocat_sentence,
    render_discourse_diagram,
    render_discocirc_discourse,
    render_three_sentence_discourse,
)
from .complexity_plots import (
    render_syntactic_complexity_radar,
    render_complexity_comparison,
    render_normal_form_comparison,
)
from .active_inference_plots import (
    plot_belief_distribution,
    plot_alignment_frame_belief_dynamics,
)
from .daif_plots import (
    plot_belief_trajectory,
    plot_free_energy_convergence,
    plot_erp_predictions,
)
from .quantum_plots import plot_povm_probabilities
from .security_plots import plot_type_violations, plot_monoidal_functor_security
from .fluid_s_plots import plot_fluid_s_volition_landscape
from .syntactic_sentence_diagrams import render_syntactic_panel
from .category_unpacking import (
    render_pregroup_reduction_unpacking,
    render_discocirc_entity_persistence,
    render_snake_equation_unpacking,
)

__all__ = [
    "CASE_COLORS",
    "FONT_SIZE_FLOOR",
    "render_case_category",
    "render_alignment_comparison",
    "render_composition_triangle",
    "render_enriched_heatmap",
    "render_functor_diagram",
    "render_discocat_sentence",
    "render_discourse_diagram",
    "render_discocirc_discourse",
    "render_three_sentence_discourse",
    "render_syntactic_complexity_radar",
    "render_complexity_comparison",
    "render_normal_form_comparison",
    "plot_belief_distribution",
    "plot_alignment_frame_belief_dynamics",
    "plot_belief_trajectory",
    "plot_free_energy_convergence",
    "plot_erp_predictions",
    "plot_povm_probabilities",
    "plot_type_violations",
    "plot_monoidal_functor_security",
    "plot_fluid_s_volition_landscape",
    "render_syntactic_panel",
    "render_pregroup_reduction_unpacking",
    "render_discocirc_entity_persistence",
    "render_snake_equation_unpacking",
]

try:
    from .discopy_diagrams import (
        render_discopy_transitive,
        render_discopy_composition,
        render_discopy_snake,
        render_discopy_passive,
        render_discopy_sentence_progression,
        render_discopy_multilingual,
        render_discopy_ditransitive,
        render_discopy_discocirc_discourse,
        render_discopy_three_sentence_discourse,
        get_diagram_metrics,
    )
except ImportError:  # pragma: no cover
    pass
else:
    __all__.extend(
        [
            "render_discopy_transitive",
            "render_discopy_composition",
            "render_discopy_snake",
            "render_discopy_passive",
            "render_discopy_sentence_progression",
            "render_discopy_multilingual",
            "render_discopy_ditransitive",
            "render_discopy_discocirc_discourse",
            "render_discopy_three_sentence_discourse",
            "get_diagram_metrics",
        ]
    )
