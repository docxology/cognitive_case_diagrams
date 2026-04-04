# manuscript/ — Research Manuscript

Research manuscript for *Compositional Approaches to Linguistic Case for Cognitive Modeling* (v2.3, 2026); see `config.yaml` for canonical metadata.

## Quick Reference

| Action | Command |
|--------|---------|
| Render PDF | After promoting to `projects/cognitive_case_diagrams/`: `uv run python scripts/03_render_pdf.py --project cognitive_case_diagrams` |
| Validate Markdown | From repo root: `uv run python -m infrastructure.validation.cli markdown projects/cognitive_case_diagrams/manuscript/` |
| Check citations | `grep -r '??' manuscript/` |

## Chapter Map

| File | § | One-Line Summary |
|------|---|-----------------|
| `00_abstract.md` | — | Category theory + active inference unifies case systems |
| `01_introduction.md` | §1 | Case assignment is the universal cognitive problem |
| `01a_research_questions.md` | §1a | Research questions and scope |
| `02_case_systems.md` | §2 | From Pāṇini to cross-linguistic alignment typology |
| `02b_case_categories.md` | §2b | Case as categories: objects, morphisms, and graded functors |
| `03_categorial_grammar.md` | §3 | Lambek calculus and string diagrams for phrase structure |
| `03b_case_type_logic.md` | §3b | Case syntax, Curry–Howard proofs, and passivization |
| `04_categorical_semantics.md` | §4 | DisCoCat: compact closed categories for NLP |
| `04b_compact_closure_complexity.md` | §4b | Snake equation, diagram metrics, complexity score |
| `04c_discourse_complexity.md` | §4c | DisCoCirc discourse, QNLP, dynamic case reversal, trainability |
| `05_enriched_categories.md` | §5 | [0,1]-enrichment = distributional proximity |
| `05b_magnitude_homology.md` | §5b | Categorical magnitude evaluates effective role redundancy |
| `06_topos_theory.md` | §6 | Morita equivalence translates between case theories |
| `07_cognitive_integration.md` | §7 | Active inference process theory of generative language |
| `07b_computational_verification.md` | §7b | Diagrammatic cognition, ERP predictions; test counts + pointer to App C |
| `07c_daif_results.md` | §7c | DAIF and CEREBRUM: Distributional Active Inference results |
| `08_quantum_active_inference.md` | §8 | TQNNs and ZX-calculus as the quantum diagram foundation |
| `08b_quantum_semantics.md` | §8b | Sheaves and POVM case assignment on quantum hardware |
| `09_ai_implications.md` | §9 | Compositional AI agents and categorical deep learning |
| `09b_cognitive_security.md` | §9b | Prompt injection as decidable type violation |
| `10_conclusion.md` | §10 | 11 contributions + future directions |
| `11_syntactic_sentence_diagrams.md` | App A | Syntactic trees + pregroup types for 8 case constructions |
| `11b_notation.md` | App B | Complete notation reference (sections A–K) |
| `11c_automated_test_inventory.md` | App C | Full automated test suite inventory |

## Configuration

`config.yaml` controls paper metadata, author info, and LLM review settings.  
See [`AGENTS.md`](AGENTS.md) for the full editing guide.
