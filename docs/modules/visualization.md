# visualization: implementation reference

Source-generated diagrams and synthetic numerical plots. Captions, labels, units, and provenance must agree with the data. Never create arbitrary confidence bands, empirical comparisons, or physical interpretations from synthetic scores. DisCoPy is a required project dependency; schematic native drawings are not independent proofs.

| Source module | Defined entry points |
| :--- | :--- |
| [active_inference_plots.py](../../src/visualization/active_inference_plots.py) | `plot_alignment_frame_belief_dynamics`, `plot_belief_distribution` |
| [category_diagrams.py](../../src/visualization/category_diagrams.py) | `render_case_category`, `render_alignment_comparison`, `render_composition_triangle` |
| [category_diagrams_config.py](../../src/visualization/category_diagrams_config.py) | Shared constants / internal helpers |
| [category_unpacking.py](../../src/visualization/category_unpacking.py) | `render_pregroup_reduction_unpacking`, `render_discocirc_entity_persistence`, `render_snake_equation_unpacking` |
| [complexity_plots.py](../../src/visualization/complexity_plots.py) | `render_complexity_comparison`, `render_normal_form_comparison`, `render_syntactic_complexity_radar` |
| [daif_plots.py](../../src/visualization/daif_plots.py) | `plot_belief_trajectory`, `plot_free_energy_convergence`, `plot_erp_predictions` |
| [discopy_diagrams.py](../../src/visualization/discopy_diagrams.py) | `render_discopy_transitive`, `render_discopy_composition`, `render_discopy_snake`, `render_discopy_passive`, `render_discopy_sentence_progression`, `render_discopy_multilingual`, `render_discopy_ditransitive`, `render_discopy_discocirc_discourse`, `render_discopy_three_sentence_discourse`, `get_diagram_metrics` |
| [enriched_diagrams.py](../../src/visualization/enriched_diagrams.py) | `render_enriched_heatmap`, `write_magnitude_report` |
| [fluid_s_plots.py](../../src/visualization/fluid_s_plots.py) | `plot_fluid_s_volition_landscape` |
| [functor_diagrams.py](../../src/visualization/functor_diagrams.py) | `render_functor_diagram` |
| [quantum_plots.py](../../src/visualization/quantum_plots.py) | `plot_povm_probabilities` |
| [security_plots.py](../../src/visualization/security_plots.py) | `plot_type_violations`, `plot_case_interaction_graph`, `plot_monoidal_functor_security` |
| [string_diagrams.py](../../src/visualization/string_diagrams.py) | `render_discocat_sentence`, `render_discourse_diagram`, `render_discocirc_discourse`, `render_three_sentence_discourse` |
| [styles.py](../../src/visualization/styles.py) | `mathtext_safe_arrows` |
| [syntactic_sentence_diagrams.py](../../src/visualization/syntactic_sentence_diagrams.py) | `render_syntactic_panel` |

See the [package guide](../../src/visualization/README.md), [method contracts](../method_contracts.md), and [claim ledger](../claim_ledger.md). These describe implementation scope; the manuscript distinguishes implemented examples from proposed extensions.
