# 🤖 AGENTS.md — manuscript/

## Overview

The `manuscript/` directory contains the complete research manuscript *Compositional Approaches to Linguistic Case for Cognitive Modeling* (`config.yaml` title) in Pandoc-compatible Markdown. The manuscript is rendered to PDF via the pipeline using `scripts/03_render_pdf.py`.

## File Inventory

| File | Section | Content |
|------|---------|---------|
| `config.yaml` | — | Paper metadata (title, author, ORCID, keywords, LLM settings) |
| `preamble.md` | — | Pandoc build configuration, include order, LaTeX options |
| `references.bib` | — | BibTeX bibliography (100+ entries) |
| `00_abstract.md` | Abstract | Core thesis, 5 pillars, key contributions |
| `01_introduction.md` | §1 | Case as cognitive problem, diagram privilege, research map |
| `01a_research_questions.md` | §1a | Explicit research questions and scope |
| `02_case_systems.md` | §2 | Historical traditions (Pāṇini→Fillmore), cross-linguistic typology |
| `02b_case_categories.md` | §2b | Categorical formalization, objects/morphisms, graded enrichment |
| `03_categorial_grammar.md` | §3 | Lambek calculus, pregroup grammar, string diagrams |
| `03b_case_type_logic.md` | §3b | Case marking, Curry–Howard correspondence, passivization |
| `04_categorical_semantics.md` | §4 | DisCoCat, commutative and non-commutative compositional semantics |
| `04b_compact_closure_complexity.md` | §4b | Snake equation, cup/cap metrics, syntactic complexity score (labels `eq-4-3`, `eq-4-4`) |
| `04c_discourse_complexity.md` | §4c | DisCoCirc discourse, dynamic case reversal, lambeq Gen II QNLP, trainability |
| `05_enriched_categories.md` | §5 | [0,1]-enrichment as continuous distributional proximity |
| `05b_magnitude_homology.md` | §5b | Categorical magnitude, redundancy, and transformer attention mapping |
| `06_topos_theory.md` | §6 | Geometric theories, classifying toposes, Morita equivalence |
| `07_cognitive_integration.md` | §7 | Active inference process theory and the generative loop |
| `07b_computational_verification.md` | §7b | Diagrammatic reasoning evidence, ERP predictions; test summary (inventory in App C) |
| `07c_daif_results.md` | §7c | Distributional Active Inference (DAIF) quantitative results: push-forward/C51, quantile TD/IQN, VMP/Bethe FE/EIG, G_policy, ERPProfile/DPE, convergence metrics, and CEREBRUM 8-case functional table |
| `08_quantum_active_inference.md` | §8 | TQNN, ZX-calculus, spin-networks |
| `08b_quantum_semantics.md` | §8b | Semantic sheaves, POVM case assignment on quantum hardware |
| `09_ai_implications.md` | §9 | Compositional agents, case typing, categorical deep learning |
| `09b_cognitive_security.md` | §9b | Adversarial injection, case-theoretic firewalls, type checking |
| `10_conclusion.md` | §10 | 11 principal contributions, future directions |
| `11_syntactic_sentence_diagrams.md` | App A | Syntactic trees + pregroup types for 8 case constructions |
| `11b_notation.md` | App B | Complete notation reference (sections A–K: linguistic, category theory, enriched, distributional, DAIF, active inference, quantum, logical, AI protocols, diagrammatic, conventions) |
| `11c_automated_test_inventory.md` | App C | Per-category automated test inventory (uses manuscript variable injection for counts) |

## Authorship

**Daniel Ari Friedman**  
ORCID: 0000-0001-6232-9096  
Active Inference Institute  
Version 2.3 (2026)

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

### Section Cross-References
```markdown
As established in \autoref{sec:categorical-semantics}...
```

## Key Equations by Section

| Section | Equation | Label |
|---------|----------|-------|
| §4 | DisCoCat sentence type: `n·s·n⁻¹` | `\label{eq:discocat-type}` |
| §5 | Composition inequality: `C(A,C) ≥ C(A,B)·C(B,C)` | `\label{eq:comp-ineq}` |
| §5 | Categorical magnitude: `|C| = Σᵢⱼ (Z⁻¹)ᵢⱼ` | `\label{eq:magnitude}` |
| §7 | Variational FE: `F = E_q[log q − log p]` | `\label{eq:free-energy}` |
| §7c.1 | Push-forward Bellman: $\int_{\mathcal{S}^{\mathbb{N}_+}} R \circ f \, d(\mathbf{S}_{\#} \mathbb{P})$ | `\label{eq:eq-7-1}` |
| §7c.2 | QR-DQN Huber loss: $\mathcal{L}_{\text{QR}}(\theta) = \frac{1}{NN'}\sum_{ij} \rho_{\tau_i}^{\kappa}(\delta_{ij})$ | `\label{eq:eq-7c-qr}` |
| §7c.3 | VMP update: $q^{(t+1)}(c_k) \propto q^{(t)}(c_k) \cdot \exp(\mathbb{E}[\log p(o|c_k)])$ | `\label{eq:eq-7c-vmp}` |
| §7c.3 | Bethe FE: $F_{\text{Bethe}} = -\sum_k q(c_k)\log p(c_k) + \sum_k q\log q - \sum_{t,k} q\log p(o_t|c_k)$ | `\label{eq:eq-7c-bethe}` |
| §7c.4 | EFE + risk: $G(\pi) = -\mathbb{E}[\log p(o)] + D_{\text{KL}}(q(s|\pi)\|p(s)) + \beta\cdot\text{risk}$ | `\label{eq:eq-7c-g}` |
| §7c.5 | DPE: $\mathrm{DPE}(o,q) = \pi_f \cdot W_1(Z_{\text{pred}}, Z_{\text{obs}})$ | `\label{eq:eq-7c-dpe}` |
| §7c.6 | Return entropy: $H[Z] = -\sum_i p_i \log p_i$ | `\label{eq:eq-7c-entropy}` |
| §8 | Quantum case: `P(c\|ρ) = Tr(E_c ρ)` | `\label{eq:eq-8-1}` |

## Bibliography Statistics

- **80+ BibTeX entries**
- Timespan: 1935 (Hjelmslev) — 2026 (PQC trainability)
- Key 2024 additions: `rad2024trainability`, `letcher2024tight`
- Key frameworks: DisCoCat (Coecke), DisCoCirc (Coecke-de Felice), lambeq (Kartsaklis)

## Rendering

```bash
# Validate manuscript markdown (from repository root)
uv run python -m infrastructure.validation.cli markdown projects/cognitive_case_diagrams/manuscript/
```

## Editing Guidelines

1. **Never break equation labels** — keep `\label{eq:...}` / `\autoref{eq:...}` pairs consistent
2. **Keep notation consistent** — always check `11b_notation.md` before introducing a new symbol
3. **Cite generously** — use `[@key]` for all claims that have literature backing
4. **Test citations** — run PDF render after adding new `references.bib` entries to verify
5. **Figure captions** — must exactly describe what is visually shown (verified in §7 during prior audit)
