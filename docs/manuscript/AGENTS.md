# 🤖 AGENTS.md — docs/manuscript/

## Overview

The `docs/manuscript/` directory contains the complete research manuscript *Cognitive Diagrams: Reviewing Categorical Accounts of Linguistic Case* (`config.yaml` `paper.title`) in Pandoc-compatible Markdown. Current edition: **v2.3**, dated **2026-04-22**, [open-access version on Zenodo (record 19695260)](https://doi.org/10.5281/zenodo.19695260). The manuscript is rendered to PDF by the template monorepo's pipeline stage `scripts/pipeline/stage_03_render.py`, run from the template root with `--project ongoing/ActiveInference/cognitive_case_diagrams`.

## File Inventory

Section titles below link to the chapter file via its `{#sec:…}` anchor; the manuscript renderer resolves those anchors with `\autoref{sec:…}` so the same labels work in PDF cross-references and in editor previews.

| Section | Content |
|---------|---------|
| [`config.yaml`](config.yaml) | Paper metadata (title, author, ORCID, keywords, LLM settings) |
| [`preamble.md`](preamble.md) | LaTeX package declarations (geometry, hyperref, etc.) for Pandoc rendering |
| [`references.bib`](references.bib) | BibTeX bibliography (count derived live from `references.bib`; see `docs/literature_guide.md`) |
| [Abstract](00_abstract.md) | Core thesis; six intro strands (five formal layers + neuro interface); key contributions |
| [Introduction](01_introduction.md#sec:introduction) | Case as cognitive problem, diagram privilege, research map |
| [Research Questions and Manuscript Navigation](01a_research_questions.md#sec:research-questions) | Explicit research questions and scope |
| [Case Systems: From Pāṇinian Kāraka to Cross-Linguistic Alignment Typology](02_case_systems.md#sec:case-systems) | Historical traditions (Pāṇini→Fillmore), cross-linguistic typology |
| [Case Categories: Roles as Objects, Relations as Morphisms, Alignment as Functors](02b_case_categories.md#sec:case-categories) | Categorical formalization, objects/morphisms, graded enrichment |
| [Categorial Grammar: Syntax as Algebraic Composition and Proof](03_categorial_grammar.md#sec:categorial-grammar) | Lambek calculus, pregroup grammar, string diagrams |
| [Case Subscripts, Passivization, and the Curry–Howard Proof](03b_case_type_logic.md#sec:case-type-logic) | Case marking, Curry–Howard correspondence, passivization |
| [Categorical Distributional Semantics (DisCoCat)](04_categorical_semantics.md#sec:categorical-semantics) | DisCoCat, commutative and non-commutative compositional semantics |
| [Compact Closure: Snake Equation, Valency, and Four Complexity Metrics](04b_compact_closure_complexity.md#sec:compact-closure-complexity) | Snake equation, cup/cap metrics, syntactic complexity score (`eq:eq-4-3`, `eq:eq-4-4`) |
| [Beyond the Sentence: State Wires Accumulate Semantic History Across Discourse](04c_discourse_complexity.md#sec:discocirc-discourse) | DisCoCirc discourse, dynamic case reversal, lambeq Gen II QNLP, trainability |
| [$[0,1]$-Enriched Case Categories](05_enriched_categories.md#sec:enriched-categories) | $[0,1]$-enrichment as continuous distributional proximity; hom-value interpretations (`tbl:hom-value-interpretations`) |
| [Magnitude and Magnitude Homology](05b_magnitude_homology.md#sec:magnitude-homology) | Categorical magnitude, redundancy, and transformer attention mapping |
| [Topos-Theoretic Bridges](06_topos_theory.md#sec:topos-theory) | Geometric theories, classifying toposes, Morita equivalence |
| [Active Inference as a Process Theory of Case](07_cognitive_integration.md#sec:cognitive-integration) | Active inference process theory and the generative loop |
| [Diagrams as Cognitively Privileged Representations](07b_diagrammatic_cognition.md#sec:diagrammatic-cognition) | Diagrammatic reasoning evidence, ERP predictions; test summary (inventory in [Appendix C](11c_automated_test_inventory.md#sec:test-suite-inventory)) |
| [Distributional Active Inference (DAIF)](07c_daif_results.md#sec:daif-results) | DAIF quantitative results (push-forward/C51, quantile TD/IQN, VMP/Bethe FE/EIG, `G_policy`, ERPProfile/DPE, convergence metrics); CEREBRUM design principles (`tbl:cerebrum-principles`) and eight-case DAIF table (`tbl:cerebrum-daif`) |
| [Topological Quantum Neural Networks and ZX-Calculus](08_quantum_active_inference.md#sec:quantum-active-inference) | TQNN, ZX-calculus, spin-networks |
| [Quantum Meaning Spaces: POVM Case Assignment](08b_quantum_semantics.md#sec:quantum-semantics) | Semantic sheaves, POVM case assignment on quantum hardware |
| [Categorical Communication Protocols](09_ai_implications.md#sec:ai-implications) | Compositional agents, case typing, categorical deep learning |
| [Prompt Injection as Categorical Type Violation](09b_cognitive_security.md#sec:cognitive-security) | Adversarial injection, case-theoretic firewalls, type checking |
| [Conclusion](10_conclusion.md#sec:conclusion) | Principal contributions and future directions |
| [Appendix A — Syntactic and Semantic Case Assignment Diagrams](11_syntactic_sentence_diagrams.md#sec:syntactic-diagrams) | Panel index table (`tbl:appendix-syntactic-constructions`); syntactic trees + pregroup types for the appendix constructions |
| [Appendix B — Notation Reference](11b_notation.md#sec:notation) | Notation reference: topic headings carry stable `#sec:notation-*` anchors |
| [Appendix C — Automated Test Suite Inventory](11c_automated_test_inventory.md#sec:test-suite-inventory) | Per-category automated test inventory (uses manuscript variable injection for counts) |

## Authorship

**Daniel Ari Friedman**  
ORCID: 0000-0001-6232-9096  
Active Inference Institute  
Email: daniel@activeinference.institute  
Version **2.3** · Date **2026-04-22** · Journal: *Active Inference Journal* (2026) · [Zenodo open access](https://doi.org/10.5281/zenodo.19695260)

## Pandoc Conventions

### Citations
Use `[@author_year]` format. All references must be in `references.bib`.

```markdown
...as shown by [@coecke2010mathematical] and [@fritz2021enriched].
```

### Display Equations
Use `\begin{equation}...\label{eq:label}...\end{equation}` blocks for numbered equations:

```markdown
\begin{equation}
P(c \mid \rho) = \text{Tr}(E_c \rho)
\label{eq:quantum-case}
\end{equation}
```

### Figure References
```markdown
![Case category structure with 8 objects (NOM, ACC, GEN, DAT, INS, LOC, ABL, VOC) and governing morphisms.](output/figures/case_category_standard.png){#fig:case-standard}
```

**Figure path roots (important for editors).** Image paths like `output/figures/...png` are **project-root–relative** — that is, relative to the project root that holds `src/`, `docs/`, `scripts/`, and `output/` — not relative to the individual `docs/manuscript/*.md` file. Pandoc and the PDF renderer add `--resource-path` entries for the manuscript directory and for `output/figures/`; the template’s `infrastructure/rendering/_pdf_figure_paths.py` rewrites `output/figures/` and related prefixes for XeLaTeX. If a Markdown preview shows a broken image, set the working tree to the project root or add that folder (and `output/figures/`) as a preview resource root.

### Section Cross-References
```markdown
As established in \autoref{sec:categorical-semantics}...
```

### Tables
Prefer **pipe tables** with a `Table:` caption and `{#tbl:label}` on the caption line (Pandoc). When the PDF needs **fixed column widths** (e.g. a narrow label column), use an `{=latex}` fenced block with a `booktabs` `tabular` environment, `\caption{...}`, and `\label{tbl:...}`—same naming pattern as pipe captions.

### Inline math in pipe tables (XeLaTeX)
Pipe tables are rendered to LaTeX `longtable` cells. Pandoc turns `$...$` into `\(...\)`. Some patterns drop the closing `\)` in the `.tex` output, which yields `! LaTeX Error: Bad math environment delimiter` / `Missing $ inserted` in `_xelatex_stdout.log`.

- Avoid bare Greek immediately before a cell boundary `|` (e.g. end a column with `$\eta_{\mathrm{cc}}$` or `$\phi{}$`, not `$\eta$` / `$\phi$` right before `|`).
- Avoid `$\beta \circ \alpha$` (or similar) immediately followed by `(` (e.g. `(§2)`), or immediately followed by `)`—parentheses adjoining the math span are a frequent trigger.
- Prefer disambiguators (`$\eta_{\mathrm{cc}}$`, `$\phi{}$`), prose instead of a fragile formula, or a single math span without those adjacencies.

## Key Equations by Section

The "Source" column links to the manuscript file holding the cited `\label{eq:…}` anchor. The active inference narrative in [Active Inference as a Process Theory of Case](07_cognitive_integration.md#sec:cognitive-integration) (scalar beliefs, variational FE prose) does not introduce a dedicated equation label; numbered DAIF equations live in [`07c_daif_results.md`](07c_daif_results.md#sec:daif-results).

| Source | Equation | Label |
|--------|----------|-------|
| [Case Categories](02b_case_categories.md#sec:case-categories) | Enriched weight composition: $w(g \circ f) = w(g) \cdot w(f)$ | `eq:eq-2-1` |
| [Case Categories](02b_case_categories.md#sec:case-categories) | Naturality condition: $G(f) \circ \alpha_A = \alpha_B \circ F(f)$ | `eq:eq-2-2` |
| [Categorical Semantics](04_categorical_semantics.md#sec:categorical-semantics) | Meaning functor $F: \mathbf{Preg} \to \mathbf{FVect}$ | `eq:eq-4-1` |
| [Categorical Semantics](04_categorical_semantics.md#sec:categorical-semantics) | Compositional sentence meaning (tensor + cups) | `eq:eq-4-2` |
| [Compact Closure & Complexity](04b_compact_closure_complexity.md#sec:compact-closure-complexity) | Snake equation: $(\varepsilon_n \otimes 1_n) \circ (1_n \otimes \eta_n) = 1_n$ | `eq:eq-4-3` |
| [Compact Closure & Complexity](04b_compact_closure_complexity.md#sec:compact-closure-complexity) | Syntactic complexity: $\text{complexity}(D) = w_w\lvert D\rvert_\text{words} + w_c\lvert D\rvert_\text{cup} + w_a\lvert D\rvert_\text{cap} + w_d \cdot \text{depth}(D)$ | `eq:eq-4-4` |
| [Enriched Categories](05_enriched_categories.md#sec:enriched-categories) | $[0,1]$ composition inequality | `eq:eq-5-2` |
| [Magnitude Homology](05b_magnitude_homology.md#sec:magnitude-homology) | Categorical magnitude $\lvert\mathcal{C}\rvert = \sum_{i,j}(Z^{-1})_{ij}$ | `eq:eq-5-3` |
| [Diagrammatic Cognition](07b_diagrammatic_cognition.md#sec:diagrammatic-cognition) | Precision-weighted PE: $\text{PE}(f) \propto w_f \cdot \lvert\mu_\text{predicted} - \mu_\text{observed}\rvert$ | `eq:pe-precision-error` |
| [DAIF: Push-Forward](07c_daif_results.md#sec:daif-pushforward) | Push-forward Bellman: $\int_{\mathcal{S}^{\mathbb{N}_+}} R \circ f \, d(\mathbf{S}_{\#} \mathbb{P})$ | `eq:eq-7-1` |
| [DAIF: Quantile TD](07c_daif_results.md#sec:daif-quantile) | QR-DQN Huber loss: $\mathcal{L}_{\text{QR}}(\theta) = \frac{1}{NN'}\sum_{ij} \rho_{\tau_i}^{\kappa}(\delta_{ij})$ | `eq:eq-7c-qr` |
| [DAIF: VMP](07c_daif_results.md#sec:daif-vmp) | VMP update: $q^{(t+1)}(c_k) \propto q^{(t)}(c_k) \cdot \exp\!\bigl(w_k \cdot o_k\bigr)$ | `eq:eq-7c-vmp` |
| [DAIF: VMP](07c_daif_results.md#sec:daif-vmp) | Bethe FE: $F_{\text{Bethe}} = -\sum_k q(c_k)\log p(c_k) + \sum_k q\log q - \sum_{t,k} q\log p(o_t\mid c_k)$ | `eq:eq-7c-bethe` |
| [DAIF: Policy](07c_daif_results.md#sec:daif-policy) | Four-term EFE: $G(\pi) = \mathcal{A} - \mathcal{E} - \gamma\mathcal{P} + \beta_{\mathrm{risk}}\mathcal{R}$ — ambiguity, epistemic value, pragmatic value, risk | `eq:eq-7c-g` |
| [DAIF: ERP](07c_daif_results.md#sec:daif-erp) | DPE: $\mathrm{DPE}(o,q) = w_f \cdot W_1(Z_{\text{pred}}, Z_{\text{obs}})$ | `eq:eq-7c-dpe` |
| [DAIF: Metrics](07c_daif_results.md#sec:daif-metrics) | Return entropy: $H[Z] = -\sum_i p_i \log p_i$ | `eq:eq-7c-entropy` |
| [Quantum Semantics](08b_quantum_semantics.md#sec:quantum-semantics) | Quantum case: $P(c\mid\rho) = \mathrm{Tr}(E_c \rho)$ | `eq:eq-8-1` |
| [Cognitive Security](09b_cognitive_security.md#sec:cognitive-security) | Protocol trace: $\text{User}_\text{NOM} \xrightarrow{f} \text{Model}_\text{INS} \xrightarrow{g} \text{Webpage}_\text{ACC} \xrightarrow{h} \text{Output}_\text{DAT}$ | `eq:eq-9-1` |

## Bibliography Statistics

- BibTeX entries: count derived live from [`references.bib`](references.bib) (rebuilt on each render). Avoid quoting a fixed total here; use `grep -cE '^@[a-zA-Z]+\{' references.bib` to obtain the current value.
- Timespan: 1935 (Hjelmslev) — present (most recent: PQC trainability and protocol-typing additions).
- Key frameworks: DisCoCat (Coecke), DisCoCirc (Coecke–de Felice), lambeq (Kartsaklis).

## Rendering

```bash
# Validate manuscript markdown.
# The infrastructure package ships with the template monorepo, not with this
# project, so run this from the template root and point it at the project.
uv run python -m infrastructure.validation.cli markdown \
  projects/ongoing/ActiveInference/cognitive_case_diagrams/docs/manuscript/
```

## Editing Guidelines

1. **Never break equation labels** — keep each `\label{eq:…}` paired with a matching `\autoref{eq:…}` to the same equation id
2. **Keep notation consistent** — always check `11b_notation.md` before introducing a new symbol
3. **Cite generously** — use `[@key]` for all claims that have literature backing
4. **Test citations** — run PDF render after adding new `references.bib` entries to verify
5. **Figure captions** — must exactly describe what is visually shown (audited end-to-end across [Active Inference as a Process Theory of Case](07_cognitive_integration.md#sec:cognitive-integration), [Diagrammatic Cognition](07b_diagrammatic_cognition.md#sec:diagrammatic-cognition), and [DAIF Results](07c_daif_results.md#sec:daif-results))
