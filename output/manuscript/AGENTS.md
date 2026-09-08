# Manuscript agent guidance

Follow [project](../../AGENTS.md) and [documentation](../AGENTS.md) guidance. The [chapter map](README.md) inventories the numbered sources. Configuration is authoritative for working version, date, authors, DOI fields, and publication status; prose quotes them only through injection.

Use Markdown headings with stable identifiers and Pandoc references such as `[@sec:case-systems]`. Use labelled Markdown figures with paths under `output/figures/`, relative to the project root because this renderer resolves resources there. Do not hand-edit injected output. Braced `${identifier}` tokens are reserved for registry variables; mathematical dollar delimiters remain literal.

## Variable injection is the only channel for quantities

Every quantitative claim in prose, tables, equations, and figure captions comes from the typed registry in `src/manuscript_variables.py` (units, formats, provenance, descriptions) via strict `${identifier}` substitution. Provenance classes: the source-bound quality receipt for passing-test and coverage claims; the seeded experiments runner output for the synthetic statistics of `07d`; direct computation from public `src` APIs on canonical inputs declared in the collectors; `config.yaml`/`pyproject` for metadata; and collection counters for structural counts. A collection count and a passing receipt are different claims and must be worded differently.

Structural mathematical constants (the integers in unit/singular definitions and indexed symbols), section labels, and citation keys are not variables — but any configurable weight (for example the `kappa(D)` coefficients), example input, result, count, version, date, or caption quantity is. A negative-control scan flags unbacked numeric literals in prose and captions, and decimal or larger literals inside mathematics; keep equations symbolic or inject their configurable values.

Equations may state definitions, established mathematics, or implemented formulas, but their status must be explicit. Do not pretend every theoretical equation is implemented. Keep raw candidate matrices distinct from valid enrichment, profile comparisons distinct from Morita equivalence, score utilities distinct from Bellman returns, and proxies distinct from measurements. Verify primary citations for substantive literature claims.

Keep figure typography readable at final PDF size, with source labels using the project's 16-point floor. Captions identify synthetic inputs and operational limits, and must distinguish synthetic replication uncertainty from empirical evidence. Do not fabricate intervals, physiological units, empirical comparisons, or proof evidence. Inspect all final pages for clipping, unresolved references, incorrect math, and caption/figure disagreement.

No manuscript content subfolders are present. Generated figures, rendered output, dependency trees, caches, and dot-directories are outside the authored documentation tree.
