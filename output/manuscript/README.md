# Manuscript sources

The working revision and date are canonical in [config.yaml](config.yaml); prose does not restate them, so a metadata edit cannot drift from the sources. DOI roles are fixed and neutral: the version DOI in `config.yaml` identifies this revision, the concept DOI identifies the series, and the live deposit state is whatever the configured `version_record` link reports at read time. The prior-version DOI is historical metadata only.

These numbered Markdown files are the authored manuscript. `preamble.md`, `references.bib`, and `config.yaml` are auxiliary sources. Figure paths are project-relative `output/figures/...`, as expected by the local template renderer. `${variable}` placeholders are hydrated into `output/manuscript/` from the typed registry in `src/manuscript_variables.py`; never edit the hydrated copies directly.

| Chapter | File |
| :--- | :--- |
| [Abstract](00_abstract.md) | `00_abstract.md` |
| [Introduction: Case, Composition, and the Limits of a Shared Diagram](01_introduction.md) | `01_introduction.md` |
| [Research Questions and Evidence Map](01a_research_questions.md) | `01a_research_questions.md` |
| [Case Systems and Alignment](02_case_systems.md) | `02_case_systems.md` |
| [Case-Role Graphs and Categorical Presentations](02b_case_categories.md) | `02b_case_categories.md` |
| [Categorial Grammar and Executable Reductions](03_categorial_grammar.md) | `03_categorial_grammar.md` |
| [Case Features and Voice Alternation](03b_case_type_logic.md) | `03b_case_type_logic.md` |
| [Compositional Distributional Semantics](04_categorical_semantics.md) | `04_categorical_semantics.md` |
| [Duality Identities and Diagram Complexity](04b_compact_closure_complexity.md) | `04b_compact_closure_complexity.md` |
| [Discourse: Entity Bookkeeping and State-Update Proposals](04c_discourse_complexity.md) | `04c_discourse_complexity.md` |
| [Candidate Similarities and $[0,1]$-Enrichment](05_enriched_categories.md) | `05_enriched_categories.md` |
| [Magnitude, Weightings, and Numerical Sensitivity](05b_magnitude_homology.md) | `05b_magnitude_homology.md` |
| [Topos-Theoretic Bridges: Requirements and Present Scope](06_topos_theory.md) | `06_topos_theory.md` |
| [Bayesian Case-Role Beliefs and Active-Inference Motivation](07_cognitive_integration.md) | `07_cognitive_integration.md` |
| [Cognitive Hypotheses and Testable Comparisons](07b_diagrammatic_cognition.md) | `07b_diagrammatic_cognition.md` |
| [Distributional Utilities and Synthetic Filtering](07c_daif_results.md) | `07c_daif_results.md` |
| [Synthetic Statistical Behavior of the Utilities](07d_synthetic_statistics.md) | `07d_synthetic_statistics.md` |
| [Quantum Diagram Connections and Their Assumptions](08_quantum_active_inference.md) | `08_quantum_active_inference.md` |
| [Case Labels as Measurement Outcomes](08b_quantum_semantics.md) | `08b_quantum_semantics.md` |
| [Proposed Case-Labeled Agent Interfaces](09_ai_implications.md) | `09_ai_implications.md` |
| [Role Policies and the Limits of Type-Based Security](09b_cognitive_security.md) | `09b_cognitive_security.md` |
| [Conclusion](10_conclusion.md) | `10_conclusion.md` |
| [Appendix A: Schematic Construction Panel](11_syntactic_sentence_diagrams.md) | `11_syntactic_sentence_diagrams.md` |
| [Appendix B: Notation and Conventions](11b_notation.md) | `11b_notation.md` |
| [Appendix C: Reproduction and Verification Scope](11c_automated_test_inventory.md) | `11c_automated_test_inventory.md` |

From the project root, run the quality gate with coverage, the synthetic experiment runner, figure generation, `uv run python scripts/inject_variables.py`, and `uv run python scripts/validate_project.py`. Then use the template-root render command in [project README](../../README.md). PDF and HTML are the current manuscript formats; a presentation requires a separate slide design.

Read [method contracts](../method_contracts.md), [claim ledger](../claim_ledger.md), and [review report](../comprehensive_review.md) before restoring or extending claims. A cited construction is not automatically implemented here. Every final PDF must be visually reviewed after rendering.
