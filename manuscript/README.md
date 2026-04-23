# manuscript/ — Research Manuscript

Research manuscript for *Cognitive Diagrams: Reviewing Categorical Accounts of Linguistic Case* (v2.3, 2026-04-22, [open-access version on Zenodo (record 19695260)](https://doi.org/10.5281/zenodo.19695260)); see [`config.yaml`](config.yaml) for canonical metadata (`paper.version`, authors, keywords).

Section files open with an `#` title and section anchor. `preamble.md` supplies LaTeX package declarations (geometry, hyperref, etc.) for Pandoc rendering; edition/version tracked in `config.yaml`. Figures use paths such as `output/figures/...` **relative to** `projects/cognitive_case_diagrams/` (see [`AGENTS.md`](AGENTS.md) — Figure path roots).

## Quick Reference

| Action | Command |
|--------|---------|
| Refresh metrics + inject `${…}` | From `projects/cognitive_case_diagrams/`: `uv run pytest tests/ --cov=src --cov-report=json` then `uv run python -m src.generate_manuscript_metrics` then `uv run python scripts/inject_variables.py` (writes `output/manuscript/` for PDF stage) |
| Render PDF | `uv run python scripts/03_render_pdf.py --project cognitive_case_diagrams` (prefers `output/manuscript/` when present) |
| Validate Markdown | From repo root: `uv run python -m infrastructure.validation.cli markdown projects/cognitive_case_diagrams/manuscript/` |
| Check citations | `grep -r '??' manuscript/` |

## Chapter Map

Section titles below link to the chapter file's `{#sec:…}` anchor; the rendered PDF resolves the same anchor through `\autoref{sec:…}`, so the link text and the in-text cross-reference share a single source of truth.

| Section | One-Line Summary |
|---------|------------------|
| [Abstract](00_abstract.md) | Category theory + active inference unifies case systems |
| [Introduction](01_introduction.md#sec:introduction) | Case assignment is the universal cognitive problem |
| [Research Questions and Manuscript Navigation](01a_research_questions.md#sec:research-questions) | Research questions and scope |
| [Case Systems](02_case_systems.md#sec:case-systems) | From Pāṇini to cross-linguistic alignment typology |
| [Case Categories](02b_case_categories.md#sec:case-categories) | Case as categories: objects, morphisms, and graded functors |
| [Categorial Grammar](03_categorial_grammar.md#sec:categorial-grammar) | Lambek calculus and string diagrams for phrase structure |
| [Case Subscripts, Passivization, and the Curry–Howard Proof](03b_case_type_logic.md#sec:case-type-logic) | Case syntax, Curry–Howard proofs, and passivization |
| [Categorical Distributional Semantics (DisCoCat)](04_categorical_semantics.md#sec:categorical-semantics) | Compact closed categories for compositional vector semantics |
| [Compact Closure: Snake Equation, Valency, and Four Complexity Metrics](04b_compact_closure_complexity.md#sec:compact-closure-complexity) | Snake equation, diagram metrics, complexity score |
| [Beyond the Sentence: DisCoCirc Discourse](04c_discourse_complexity.md#sec:discocirc-discourse) | DisCoCirc discourse, QNLP, dynamic case reversal, trainability |
| [$[0,1]$-Enriched Case Categories](05_enriched_categories.md#sec:enriched-categories) | $[0,1]$-enrichment = distributional proximity; hom-value interpretation table |
| [Magnitude and Magnitude Homology](05b_magnitude_homology.md#sec:magnitude-homology) | Categorical magnitude evaluates effective role redundancy |
| [Topos-Theoretic Bridges](06_topos_theory.md#sec:topos-theory) | Morita equivalence translates between case theories |
| [Active Inference as a Process Theory of Case](07_cognitive_integration.md#sec:cognitive-integration) | Active inference process theory of generative language |
| [Diagrams as Cognitively Privileged Representations](07b_diagrammatic_cognition.md#sec:diagrammatic-cognition) | Diagrammatic cognition, ERP predictions, six-strand synthesis (five formal layers + ROSE interface); test counts + pointer to [Appendix C](11c_automated_test_inventory.md#sec:test-suite-inventory) |
| [Distributional Active Inference (DAIF)](07c_daif_results.md#sec:daif-results) | DAIF metrics; CEREBRUM design-principles and eight-case tables |
| [Topological Quantum Neural Networks and ZX-Calculus](08_quantum_active_inference.md#sec:quantum-active-inference) | TQNNs and ZX-calculus as the quantum diagram foundation |
| [Quantum Meaning Spaces: POVM Case Assignment](08b_quantum_semantics.md#sec:quantum-semantics) | Sheaves and POVM case assignment on quantum hardware |
| [Categorical Communication Protocols](09_ai_implications.md#sec:ai-implications) | Compositional AI agents and categorical deep learning |
| [Prompt Injection as Categorical Type Violation](09b_cognitive_security.md#sec:cognitive-security) | Prompt injection as decidable type violation |
| [Conclusion](10_conclusion.md#sec:conclusion) | Principal contributions and future directions |
| [Appendix A — Syntactic and Semantic Case Assignment Diagrams](11_syntactic_sentence_diagrams.md#sec:syntactic-diagrams) | Panel index table; syntactic trees + pregroup types for the appendix constructions |
| [Appendix B — Notation Reference](11b_notation.md#sec:notation) | Notation reference: topic headings carry stable `#sec:notation-*` anchors |
| [Appendix C — Automated Test Suite Inventory](11c_automated_test_inventory.md#sec:test-suite-inventory) | Full automated test suite inventory |

## Suggested Reading Paths

The manuscript is designed so readers can enter at the section most relevant to their background and follow a coherent arc:

| Audience | Recommended path |
|----------|------------------|
| **Linguists & typologists** | [Introduction](01_introduction.md#sec:introduction) → [Case Systems](02_case_systems.md#sec:case-systems) → [Case Categories](02b_case_categories.md#sec:case-categories) → [Categorial Grammar](03_categorial_grammar.md#sec:categorial-grammar) → [Categorical Semantics](04_categorical_semantics.md#sec:categorical-semantics) |
| **Category theorists** | [Introduction](01_introduction.md#sec:introduction) → [Enriched Categories](05_enriched_categories.md#sec:enriched-categories) → [Magnitude Homology](05b_magnitude_homology.md#sec:magnitude-homology) → [Topos Theory](06_topos_theory.md#sec:topos-theory) |
| **Cognitive scientists & neuroscientists** | [Introduction](01_introduction.md#sec:introduction) → [Active Inference as a Process Theory of Case](07_cognitive_integration.md#sec:cognitive-integration) → [Diagrammatic Cognition](07b_diagrammatic_cognition.md#sec:diagrammatic-cognition) → [DAIF Results](07c_daif_results.md#sec:daif-results) |
| **AI safety & alignment researchers** | [Categorical Communication Protocols](09_ai_implications.md#sec:ai-implications) → [Cognitive Security](09b_cognitive_security.md#sec:cognitive-security) → [Topos Theory](06_topos_theory.md#sec:topos-theory) (for Morita-stable invariants) |

## Configuration

`config.yaml` controls paper metadata, author info, and LLM review settings.  
See [`AGENTS.md`](AGENTS.md) for the full editing guide.
