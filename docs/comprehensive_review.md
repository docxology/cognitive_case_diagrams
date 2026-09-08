# Comprehensive review and improvement receipts — 2026-09-07

**Historical initial-review record.** The statements below describe the first local revision and its then-current publication state. Subsequent experiment, MCP, variable-registry, and release work follows the [release workflow](release_workflow.md). Historical receipt paths under `output/review/` are local working evidence and are excluded from public release archives; current publication evidence is supplied with the release.

This working revision replaces overstated scientific claims with explicit method contracts, repairs numerical and validation defects, and rebuilds the manuscript and figures from their sources. It is a local development revision, not a publication or independent certification. Baseline review preceded implementation; checks of the changes are implementation verification.

## 1. Surface map and authority

The selected template-path view resolves to the self-versioned `docxology/cognitive_case_diagrams` checkout. The initial working tree was clean at `ca84b2ce5760335a8dafbb73ff657dfe9685a55b`. No other project was selected or edited, and no commit, push, tag, merge, or external publication was performed. The `ongoing/` local-only policy remains in force.

Reviewed surfaces include all nine source subpackages; shared metrics and hydration writers; tests and orchestration; root and nested guides; all 24 numbered manuscript chapters; cited bibliography entries; all 30 canonical figures; citation/configuration metadata; and final render products. The sibling template repository supplies the rendering and validation engine. Its sources were inspected, not edited. Dependencies, caches, dot-directories, and historical generated guides are not authored documentation surfaces.

The [method contracts](method_contracts.md) state exact implementation scope. The [claim ledger](claim_ledger.md) separates implementation, theory, and empirical claims. The [literature guide](literature_guide.md) records consulted primary sources. The [figure index](manuscript_figure_index.md) and [accessibility descriptions](figure_alt_text.json) bind figures to the paper.

## 2. Findings and implemented corrections

| Lane / severity | Reproduced defect or evidence gap | Resolution |
| :--- | :--- | :--- |
| Methods / critical | Pairwise quantile regression used only corresponding target positions | All current-target pairs with target-averaged Huber gradients; analytic two-point controls |
| Methods / major | Optimistic and pessimistic distortion directions were reversed | Corrected direction, documented curvature convention, and explicitly distinguished the helper from a learned IQN |
| Methods / major | Discrete score quantiles interpolated outcomes absent from the support | Generalized inverse CDF, excluding zero-mass atoms |
| Methods / major | Categorical conversion discarded out-of-support mass | One shared C51-style clipped, mass-splitting projection |
| Methods / major | Equal-length Wasserstein calculations ignored probability-level grids | Integrate the two piecewise-linear reconstructions on a merged grid, with constant tails |
| Methods / major | A converged filter returned the previous belief | Store the current posterior before stopping; record belief and free-energy changes and stop reason |
| Methods / major | Negative or nonfinite probabilities, transitions, and evidence could pass | Shared shape, finiteness, probability, stochastic-matrix, and integer contracts; impossible evidence raises |
| Methods / major | Mutable matrix inputs could leave a stale magnitude inverse | Revalidate and invalidate the cache; pseudoinverse results require both weighting residuals |
| Methods / major | Supplied POVMs/states could be non-Hermitian or otherwise invalid | Validate matrix dimensions, Hermiticity, positivity, completeness, trace, effect bounds, and role support |
| Methods / major | Unknown-role identity could be accepted by a role-policy check | Reject unknown roles and refresh mutable graph adjacency |
| Theory / critical | Presentation counts were presented as Morita equivalence and transfer evidence | Canonical profile-comparison name; deprecated compatibility wrapper; equivalence unknown and transfer unavailable |
| Theory / critical | A dimensionless occupancy score was labelled a Bellman return | Retain legacy API names with exact score formula and explicit non-equivalence to Bellman control |
| Theory / major | Fixed single-factor messages and shared-distribution scores were called general VMP/Bethe inference | Document actual computations; add `factor_consistency_score` alias |
| Theory / major | Raw similarities were treated as a valid enrichment | Preserve the composition counterexample and provide explicit max-product composition closure |
| Theory / major | Cup/cap counts implied magnitude homology or physical decoherence | Mark the score as synthetic and separate it from the cited mathematical constructions |
| Manuscript / critical | Diagrams implied linguistic universals, physiological measurements, quantum interference, and operational security | Rewrite the 24 chapters and captions around supplied types, synthetic examples, assumptions, and required future evidence |
| Visualization / major | Fabricated-looking waveform/probability panels and crowded labels obscured actual data | Plot supplied probabilities, checked free-energy components, and model-unit proxies; improve chart layout and schematic labels |
| Artifacts / critical | Dollar substitution corrupted mathematical delimiters | Substitute only braced identifier tokens; preserve literal inline/display math |
| Artifacts / major | Broad exception fallbacks could publish incomplete scientific metrics | Domain computation errors propagate; no silent empty-dictionary fallback |
| Artifacts / major | Renderer required accessibility text absent from the registry | Author all figure descriptions; propagate and validate them independently of captions |
| Metadata / major | Current files inherited earlier publication identifiers and stronger abstracts | Mark working revision 2.4-dev / software 2.4.0.dev0; clear current DOI and unsupported preferred journal citation |
| Testing / major | One property test generated random matrices it never used and hit a generation timeout | Reproduce the seed successfully, replace unused random setup with explicit invalid diagonals, retain other property tests |
| Documentation / moderate | Large duplicated inventories and unsupported explanations drifted from source | Rebuild source-linked module indexes, concise run instructions, claim boundaries, and review receipts |

Compatibility is preserved where useful through legacy names, but former permissive inputs and incorrect numerical values intentionally change. These differences are listed in the method contracts; this is a development version rather than a patch-release compatibility claim.

## 3. Claim-status rollup

Verified local contracts include the selected executable reductions, finite Bayesian arithmetic, quantile/projection examples, matrix and role-policy validation, and source-to-artifact checks. Their tests demonstrate specific cases and rejection paths, not universal mathematical or empirical validity.

Unsupported claims have been removed or qualified: profile counts deciding Morita equivalence, generic theorem transport, a full local DAIF/Bellman learner, general factor-graph inference, homology from cup counts, measured EEG amplitudes, physical quantum cognition, and enforced agent security. Cognitive advantages and case-labelled authorization remain explicitly proposed research. The canonical matrix is a synthetic candidate with failed composition checks until closure is requested.

The bibliography retains a research library beyond the works cited by this revision. Unused entries are not treated as verified evidence. The earlier Zenodo record returned HTTP 429 during retrieval; its relationship to this working revision is not asserted. The prior DOI is recorded separately in configuration for historical orientation.

## 4. Material risks and boundaries

All numerical examples are synthetic. There is no corpus split, annotation validation, participant sample, EEG calibration, quantum-hardware run, or operational security evaluation. Broad theory-profile comparisons cannot substitute for equivalence witnesses. A role graph is not an authenticated execution boundary, and a pregroup codomain check is not independent grammaticality validation.

The coverage floor applies to combined statement/branch coverage, not to a separate 90% branch-only threshold. Test success does not establish numerical stability for every extreme floating-point input. The selected runtime is recorded below; a multi-version Python matrix was not run. No repository-wide vulnerability or secret scan is claimed.

The current manuscript is maintained as PDF and HTML. Automatic slide exports were disabled because the revised paper does not supply a validated slide design; obsolete renderer-owned slide products are not current deliverables. Historical unprefixed section HTML was moved into `output/review/prior_revision/web/` so it cannot be mistaken for the current article. Automated LLM reviews and translations remain disabled by the author's existing configuration.

Shared template release validation remains red for artifact-path/inventory expectations and rejection of the existing intermediate category symlink. The project checks and successful rendering do not override this failure. The PDF has no structural tagging, so authored figure descriptions and successful browser checks do not establish PDF/UA conformance or a complete accessibility audit.

## 5. Changed artifacts

- Numerical and logical changes: `src/numerics.py`, `src/cognitive/`, `src/daif/`, `src/enriched_cat/`, `src/quantum/`, `src/security/`, `src/topos_theory/`, and the affected case/diagram helpers.
- Figure writers: `src/visualization/`, selected domain orchestrators, and `scripts/generate_diagrams.py`; outputs remain derived from these writers.
- Artifact integrity: `src/manuscript_injection.py`, `src/generate_manuscript_metrics.py`, `src/project_validation.py`, `scripts/inject_variables.py`, `scripts/validate_project.py`, and the locked quality gate.
- Regression and negative controls: method, artifact, quantile, topological-profile, hydration, property, and plotting tests.
- Authored paper and documentation: all numbered chapters, captions, root/module guides, source-linked API indexes, method/claim ledgers, accessibility descriptions, bibliography corrections, `CITATION.cff`, version configuration, and lockfile.

An initial source backup was retained before the rewrite. Current diffs remain reviewable in this checkout. Generated figures and hydrated chapters were regenerated; they were not hand-edited to make checks pass.

## 6. Verification receipts

The source gate used the locked project environment with CPython 3.14.6, NumPy 2.4.4, and DisCoPy 1.2.2. An isolated environment/cache on the internal temporary volume avoided slow external-drive package operations. No dependency or source was installed into the sibling template tree. Rendering used the template's frozen lockfile and rendering dependency group in a separate environment.

| Verification | Observed result | Receipt |
| :--- | :--- | :--- |
| Reproduce original method defects | 15 failing analytic regression cases against the original implementations | [Initial counterexamples](../output/review/receipts/original-counterexamples.log) |
| `uv run python scripts/quality_gate.py --coverage` | Exit 0: Ruff and mypy passed; 1,289 tests passed in 172.95 s | [Complete gate](../output/review/receipts/quality-gate.log) |
| Coverage accounting | 3,759/3,914 statements and 884/1,022 branches covered: 94.06% combined; 86.50% branch-only. The combined 90% floor passed | [Coverage JSON](../output/review/receipts/coverage.json) |
| Coverage rejection control | `uv run coverage report --fail-under=100` exited 2 as intended; real configured floor remains 90% | [Expected rejection](../output/review/receipts/coverage-negative-control.log) |
| Figure generation and hydration | Exit 0; 30 canonical figures, 32 collected metrics, 24 hydrated chapters, zero unresolved metric tokens | [Generation](../output/review/receipts/figure-generation.log), [hydration](../output/review/receipts/hydration.log) |
| `uv run python scripts/validate_project.py` | Exit 0; 24 chapters, 30 figures, 107 bibliography entries, 87 labels; source/output parity, checksums, accessibility descriptions, and references checked | [Artifact gate](../output/review/receipts/artifact-gate.log) |
| Analytic manuscript examples | Source APIs and a NumPy linear solve reproduce the score/return distinction, discrete quantiles, composition counterexample, and Born probability | [Computed examples](../output/review/analytic_checks.json) |
| Template `stage_03_render.py` | Exit 0; current combined PDF and HTML successfully rendered | [Final rendering](../output/review/receipts/render.log) |
| PDF structure and visual inspection | 44 pages, correct title/author, no encryption or JavaScript; every page inspected at 110 dpi, with detailed checks of equations, dense diagrams, and references. After the last bibliography edit, pages 1–43 were byte-identical raster images; changed page 44 was inspected again | [PDF metadata](../output/review/receipts/pdfinfo.txt), [visual receipts](../output/review/visual/), [hash manifest](../output/review/verification.json) |
| HTML/browser interaction | 30 loaded images with descriptions, 113 rendered math elements, no broken internal anchors, keyboard navigation to the DAIF section, no horizontal overflow at 1,440 px or 390 px, zero console/page errors | [Browser checks](../output/review/browser_checks.json), [screenshots](../output/review/visual/) |
| Authored documentation links | 461 local targets across 88 Markdown files exist; HTTP targets and fragment semantics are outside this filesystem check | [Documentation checks](../output/review/documentation_checks.json) |
| Template `stage_04_validate.py` | Exit 1; two critical failures remain. PDF, transmission bookends, figure registry, evidence registry, design overlays, and artifact-manifest checks report pass | [Shared validator](../output/review/receipts/shared-validation.log) |
| Sidecar `python3 scripts/check_signposts.py` | Exit 1; seven missing-link errors outside this project | [Sidecar signposts](../output/review/receipts/sidecar-signposts.log) |
| Sidecar `python3 scripts/validate_agent_prompts.py` | Exit 0; seven prompt files and six skill files checked | [Sidecar prompts](../output/review/receipts/sidecar-prompts.log) |

The shared validator's current blocking output is:

```text
Enabled PDF is not a stable output artifact: .../output/cognitive_case_diagrams_combined.pdf
Missing expected file: ongoing/docxology/cognitive_case_diagrams_combined.pdf
Cannot bind validation report to rendered inputs [PROJECT_LINK_INVALID]: project source has an intermediate symlink: .../template/projects/ongoing/ActiveInference
❌ VALIDATION FAILED - 2 critical issue(s)
```

The actual rendered PDF is `output/pdf/cognitive_case_diagrams_combined.pdf`. The stable-publication inventory and source-containment rules disagree with this local-only checkout's layout. No paths were tracked, no symlinks were altered, and no engine rules were weakened to make validation green. The shared validator also emits noncritical image-path notes despite successfully rendering and checking all 30 figures, and two unsupported-number notes for a supplied matrix entry (`0.85`) and inverse notation (`-1`). Its evidence-registry summary reports pass; the source computations and notation are separately recorded in the analytic receipt.

The sidecar signpost errors concern two absent sibling template examples and five absent `working/` line-set paths. They are outside the selected repository; its documentation pass did not edit those targets. The full failing output is retained. The earlier renderer rejection of missing figure descriptions and malformed math was corrected at the source and followed by a successful complete render. No missing-character, unresolved-reference, or overfull-box warning was found in the final LaTeX build; generic template package/preamble warnings remain in the render log.

The final documentation links and `git diff --check` were checked after recording these receipts. The [verification manifest](../output/review/verification.json) binds the final PDF, HTML, all figure files, and numbered source chapters by SHA-256. This is artifact identification, not a claim of byte-reproducible PDF builds. Browser QA used isolated headless installed Chrome because the preferred browser tools failed to expose a usable session; it does not certify every assistive technology or browser. The renderer removed 24 obsolete tracked slide PDFs after slide generation was disabled; these deletions are visible in the uncommitted diff, and their previous versions remain in Git history.

## 7. Follow-up research and release decisions

A scientific extension needs an independently reviewed formalization or evaluation design: language-specific lexical and alignment evidence, explicit enriched sites/equivalence witnesses for a bridge, correctly specified return dynamics for a distributional learner, controlled human comparisons for diagram benefits, physiological calibration for ERP hypotheses, and authenticated runtime enforcement for security claims. These are separate research projects, not defects hidden by this local green test run.

Before any release, reconcile the shared template's artifact inventory and source-provenance rules with the approved local-only category layout, fix the unrelated sidecar signposts in their owning repositories, and rerun those failing checks without bypasses. Obtain independent subject-matter review, decide which empirical/theoretical claims the release actually makes, and archive that exact validated revision under its own publication metadata. A tagged-PDF workflow and assistive-technology checks are needed before asserting accessible PDF conformance. No publication step was requested or performed here.
