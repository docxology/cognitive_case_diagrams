# API index

Source signatures and local package guides are authoritative. This inventory lists public definitions, not a promise that every legacy name implements its namesake theory. See [method contracts](method_contracts.md). Each package's boundary paragraph lives canonically in its [module guide](modules/README.md); the sections below link to it instead of copying it.

## case_systems

Boundary statement: see the [module guide](modules/case_systems.md) (canonical).

| Module | Definitions |
| :--- | :--- |
| [case_category.py](../src/case_systems/case_category.py) | `CaseRole`, `Morphism`, `CaseCategory`, `standard_case_category`, `minimal_case_category`, `introductory_case_category`, `accusative_alignment`, `ergative_alignment`, `tripartite_alignment`, `active_stative_alignment` |
| [fluid_s.py](../src/case_systems/fluid_s.py) | `VolitionContext`, `FluidSFunctor`, `create_fluid_s_functor`, `bats_fluid_s`, `fluid_s_enriched_weight` |
| [functor.py](../src/case_systems/functor.py) | `AlignmentFunctor`, `accusative_to_ergative_functor`, `tripartite_functor`, `MonoidalFunctor` |
| [natural_transformation.py](../src/case_systems/natural_transformation.py) | `ComponentMorphism`, `NaturalTransformation`, `IdentityNaturalTransformation`, `compose_transformations` |

## diagrams

Boundary statement: see the [module guide](modules/diagrams.md) (canonical).

| Module | Definitions |
| :--- | :--- |
| [complexity_examples.py](../src/diagrams/complexity_examples.py) | `build_complexity_examples` |
| [complexity_metrics.py](../src/diagrams/complexity_metrics.py) | `DiagramMetrics`, `count_boxes`, `count_words`, `count_cups`, `count_caps`, `diagram_depth`, `diagram_width`, `compute_normal_form`, `is_in_normal_form`, `diagrams_equal`, `analyze_diagram`, `syntactic_complexity_score`, `compare_diagrams`, `MagnitudeHomologyMetrics`, `compute_pqc_decoherence_proxy` |
| [ditransitive.py](../src/diagrams/ditransitive.py) | `DitransitiveSentence`, `create_ditransitive`, `create_discopy_ditransitive` |
| [string_diagram.py](../src/diagrams/string_diagram.py) | `AtomicType`, `Wire`, `Box`, `Sentence`, `Discourse`, `create_discopy_transitive`, `create_discopy_complex_transitive`, `create_discopy_intransitive`, `create_discopy_passive`, `create_discopy_snake_equation`, `create_discopy_composition`, `create_discopy_multilingual`, `create_word_diagram_transitive`, `create_word_diagram_intransitive`, `create_swap_passive`, `create_word_diagram_ditransitive`, `create_tensor_semantics` |

## enriched_cat

Boundary statement: see the [module guide](modules/enriched_cat.md) (canonical).

| Module | Definitions |
| :--- | :--- |
| [enriched.py](../src/enriched_cat/enriched.py) | `EnrichedCategory`, `standard_enriched_category` |

## topos_theory

Boundary statement: see the [module guide](modules/topos_theory.md) (canonical).

| Module | Definitions |
| :--- | :--- |
| [topos.py](../src/topos_theory/topos.py) | `TheoryType`, `Axiom`, `GeometricTheory`, `ClassifyingTopos`, `compare_theory_presentations`, `check_morita_equivalence`, `build_typological_theory`, `build_enriched_theory`, `bridge_transfer` |

## cognitive

Boundary statement: see the [module guide](modules/cognitive.md) (canonical).

| Module | Definitions |
| :--- | :--- |
| [action_selection.py](../src/cognitive/action_selection.py) | `expected_free_energy` |
| [belief.py](../src/cognitive/belief.py) | `CaseDiagramBelief` |
| [belief_updating.py](../src/cognitive/belief_updating.py) | `update_belief`, `sequential_belief_update` |
| [figure_data.py](../src/cognitive/figure_data.py) | `make_belief_trajectory_data`, `make_fluid_s_landscape_data`, `make_daif_belief_trajectory_data`, `make_free_energy_convergence_data`, `make_erp_prediction_data` |
| [free_energy.py](../src/cognitive/free_energy.py) | `kl_divergence`, `variational_free_energy` |
| [prediction_error.py](../src/cognitive/prediction_error.py) | `prediction_error`, `p600_amplitude_ratio` |
| [reanalysis.py](../src/cognitive/reanalysis.py) | `magnitude_reanalysis_cost`, `n400_amplitude_proxy` |

## daif

Boundary statement: see the [module guide](modules/daif.md) (canonical).

| Module | Definitions |
| :--- | :--- |
| [core.py](../src/daif/core.py) | `push_forward_return`, `distributional_bellman_operator`, `categorical_return_distribution` |
| [inference.py](../src/daif/inference.py) | `distributional_case_assignment`, `variational_message_passing`, `bethe_free_energy`, `expected_information_gain` |
| [metrics.py](../src/daif/metrics.py) | `convergence_diagnostics`, `distributional_kl`, `quantile_coverage`, `return_distribution_entropy` |
| [policy.py](../src/daif/policy.py) | `G_policy`, `softmax_policy_selection`, `distributional_epistemic_value` |
| [prediction.py](../src/daif/prediction.py) | `distributional_prediction_error`, `wasserstein_prediction_error`, `n400_from_return_distribution`, `p600_from_precision_update`, `erp_amplitude_profile` |
| [quantile.py](../src/daif/quantile.py) | `quantile_td_update`, `implicit_quantile_network_update`, `wasserstein_return_distance` |
| [types.py](../src/daif/types.py) | `DistributionalReturn`, `DAIFResult`, `ERPProfile` |

## quantum

Boundary statement: see the [module guide](modules/quantum.md) (canonical).

| Module | Definitions |
| :--- | :--- |
| [figure_data.py](../src/quantum/figure_data.py) | `make_quantum_povm_example`, `make_security_violations_example`, `make_monoidal_functor_example` |
| [quantum_case.py](../src/quantum/quantum_case.py) | `CasePOVM`, `case_probability`, `crisp_case_povm`, `graded_case_povm`, `fluid_s_povm`, `semantic_state` |

## security

Boundary statement: see the [module guide](modules/security.md) (canonical).

| Module | Definitions |
| :--- | :--- |
| [cognitive_security.py](../src/security/cognitive_security.py) | `TypeViolation`, `CaseFrameValidator`, `detect_type_violation`, `injection_score`, `topological_robustness`, `semantic_integrity_check` |

## visualization

Boundary statement: see the [module guide](modules/visualization.md) (canonical).

| Module | Definitions |
| :--- | :--- |
| [active_inference_plots.py](../src/visualization/active_inference_plots.py) | `plot_alignment_frame_belief_dynamics`, `plot_belief_distribution` |
| [category_diagrams.py](../src/visualization/category_diagrams.py) | `render_case_category`, `render_alignment_comparison`, `render_composition_triangle` |
| [category_diagrams_config.py](../src/visualization/category_diagrams_config.py) | Shared constants / internal helpers |
| [category_unpacking.py](../src/visualization/category_unpacking.py) | `render_pregroup_reduction_unpacking`, `render_discocirc_entity_persistence`, `render_snake_equation_unpacking` |
| [complexity_plots.py](../src/visualization/complexity_plots.py) | `render_complexity_comparison`, `render_normal_form_comparison`, `render_syntactic_complexity_radar` |
| [daif_plots.py](../src/visualization/daif_plots.py) | `plot_belief_trajectory`, `plot_free_energy_convergence`, `plot_erp_predictions` |
| [discopy_diagrams.py](../src/visualization/discopy_diagrams.py) | `render_discopy_transitive`, `render_discopy_composition`, `render_discopy_snake`, `render_discopy_passive`, `render_discopy_sentence_progression`, `render_discopy_multilingual`, `render_discopy_ditransitive`, `render_discopy_discocirc_discourse`, `render_discopy_three_sentence_discourse`, `get_diagram_metrics` |
| [enriched_diagrams.py](../src/visualization/enriched_diagrams.py) | `render_enriched_heatmap`, `write_magnitude_report` |
| [fluid_s_plots.py](../src/visualization/fluid_s_plots.py) | `plot_fluid_s_volition_landscape` |
| [functor_diagrams.py](../src/visualization/functor_diagrams.py) | `render_functor_diagram` |
| [quantum_plots.py](../src/visualization/quantum_plots.py) | `plot_povm_probabilities` |
| [security_plots.py](../src/visualization/security_plots.py) | `plot_type_violations`, `plot_case_interaction_graph`, `plot_monoidal_functor_security` |
| [string_diagrams.py](../src/visualization/string_diagrams.py) | `render_discocat_sentence`, `render_discourse_diagram`, `render_discocirc_discourse`, `render_three_sentence_discourse` |
| [styles.py](../src/visualization/styles.py) | `mathtext_safe_arrows` |
| [syntactic_sentence_diagrams.py](../src/visualization/syntactic_sentence_diagrams.py) | `render_syntactic_panel` |

## Manuscript helpers

`src.generate_manuscript_metrics.collect_metrics()` collects test counts and scientific example metrics; `write_metrics()` serializes them. `src.manuscript_injection.render_all_chapters()` substitutes only braced identifiers and preserves mathematical dollar delimiters. `src.project_validation.validate_project()` verifies hydrated text, citations, labels, image integrity, and registry checksums. See the scripts guide for execution order.

`src.manuscript_variables` is the typed registry for manuscript ``${variable}`` injection: `VariableSpec` entries define which identifiers exist, each with unit, display format, provenance class, and a description of what the number measures. The contract is fail-closed — an unregistered token fails injection, and a registered required variable without a finite, format-conformant value fails collection, as does a nonfinite value, an unknown unit, or a boolean-valued experiment metric. `src.web_correction` is the source-owned, idempotent post-render correction that injects one project-owned override block into every HTML file under `output/web/` so the code-block surface and scroll behavior survive pandoc's transparent-`.sourceCode` stylesheet; it runs after the render stage and before validation or browser checks, every re-render removes its marker, and a later HTML correction invalidates previously recorded browser acceptance.
