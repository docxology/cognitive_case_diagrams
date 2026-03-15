"""Visualization subpackage for publication-quality figure generation.

Modules:
    styles: Color palette and typography constants
    category_diagrams: Case category directed graphs
    enriched_diagrams: [0,1]-enriched heatmaps
    functor_diagrams: Alignment functor mappings
    string_diagrams: DisCoCat/DisCoCirc renderers
    discopy_diagrams: Real DisCoPy diagram rendering (optional)
    complexity_plots: Diagram complexity comparison charts
    active_inference_plots: Belief distributions and Free Energy
    quantum_plots: Case POVM probabilities
    security_plots: Type violation analysis
    fluid_s_plots: Contextual volition alignment
"""

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
from .complexity_plots import render_syntactic_complexity_radar
from .active_inference_plots import plot_belief_distribution
from .quantum_plots import plot_povm_probabilities
from .security_plots import plot_type_violations
from .fluid_s_plots import plot_fluid_s_volition_landscape

# Optional DisCoPy-based rendering
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
except ImportError:
    pass

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
    "plot_belief_distribution",
    "plot_povm_probabilities",
    "plot_type_violations",
    "plot_fluid_s_volition_landscape",
]
