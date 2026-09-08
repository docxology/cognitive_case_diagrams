# Release workflow

The release is a coupled set of source, synthetic experiment results, figures, hydrated manuscript, PDF, web article, software distributions, and provenance. Edit source writers first. Rebuild any dependent artifacts after changing their inputs.

## Canonical inputs and evidence

| Artifact | Authoritative writer or input | Rejection conditions |
| :--- | :--- | :--- |
| Package version and dependencies | `pyproject.toml`, `uv.lock` | Stable software and paper versions differ; lock cannot resolve |
| Paper identity, author, date and DOI roles | `docs/manuscript/config.yaml` | Missing or equal concept/version DOIs; unresolved title or abstract |
| Test and coverage receipt | `scripts/quality_gate.py --coverage`, `src/release_validation.py` | Failed check, insufficient coverage, empty suite, changed source, changed JUnit or coverage JSON |
| Synthetic results | `src/experiments`, `scripts/run_experiments.py` | Invalid configuration, nonfinite result, failed analytic control, stale source evidence |
| Figures | `src/visualization`, `scripts/generate_diagrams.py` | Generator failure, missing image, checksum/label/alt-text mismatch |
| Manuscript variables | `src/manuscript_variables.py`, `scripts/inject_variables.py` | Missing/stale evidence, unresolved variables, forbidden literal claims |
| Citation and deposit metadata | `src/release_metadata.py`, `scripts/build_release.py --metadata-only` | Sidecars differ from canonical configuration and hydrated abstract |
| Visual inspection | `src/publication_review.py` | Uninspected page or figure, failed browser observation, changed source or artifact bytes |
| Reproducibility archive | `src/release_bundle.py`, `scripts/build_release.py` | Unsafe paths, symlinks, private derived paths, duplicate files, changed bytes, mismatched hashes |

Quality receipts are local execution records, not signed attestations. Visual review records describe completed reviewer observations; their validator checks completeness and freshness, not aesthetic or scientific truth. The public receipt fields include test totals, line and branch coverage, an input fingerprint, a timestamp, and the suite command. The original JUnit and coverage files remain necessary to validate that receipt locally.

## Build order

From the project root:

```bash
uv sync --frozen --extra mcp
uv run python scripts/quality_gate.py --coverage
uv run python scripts/run_experiments.py
uv run python scripts/generate_diagrams.py
uv run python scripts/inject_variables.py
uv run python scripts/validate_project.py
uv run python scripts/build_release.py --metadata-only
uv build --no-sources
uv run python scripts/evidence_status.py
```

Render through the sibling template engine using the commands in the project README. Inspect every final PDF page and every figure; check PDF identity/metadata, web images, internal links, browser console, keyboard navigation, and narrow viewport behavior. Record only observations actually completed through `record_publication_review`. The record binds the current publication bytes and tested source. A late change invalidates it.

Then run `uv run python scripts/build_release.py`. The builder requires current quality, artifact, metadata, and visual evidence. It rejects skipped tests so the optional MCP integration must execute in the release environment. Install the built wheel in a clean environment outside the checkout and exercise the installed MCP stdio server with a real SDK client before publication.

The archive is deterministic for the same file bytes, configured publication date, and compression runtime. Building it twice and comparing SHA-256 values checks archive assembly; it does not establish byte-identical PDF generation across operating systems or dependency versions. The internal manifest records every selected file's size and digest. Verification also reconstructs embedded quality evidence from the archived source and test data, and streams payloads under size and count bounds. Cache directories, environment files, local review logs, and prior release archives are excluded.

## GitHub and Zenodo

Reserve the new Zenodo version DOI before final manuscript rendering. A reserved DOI is not a published record. Preserve the manuscript series' concept DOI and its existing publication license; do not assign the manuscript DOI to the software as though it were a software deposit.

Commit and push only the selected project's intended source and tracked deliverables. Verify the remote commit and CI result. Create the matching GitHub tag/release with wheel, source distribution, rendered paper, reproducibility archive, and validation/checksum evidence. Replace inherited files only in the new Zenodo draft, upload the final paper and declared supplementary publication artifacts, update metadata from the generated publication payload, and publish. Verify the published record, exact version DOI, and uploaded-file checksums through the API.

The root `.zenodo.json` describes the software for GitHub/Zenodo integration. The generated `zenodo-publication.json` describes the separately licensed manuscript deposit. They intentionally have different upload types and licenses. Public release notes must report actual remote outcomes and any remaining shared-engine limitations.

## Shared engine boundary

This checkout resolves through a category symlink in the template workspace. The shared engine's provenance checker currently expects a different external-project boundary, while its stable inventory omits these explicitly ignored PDF/HTML outputs. Those checks must not be reported as passing without a successful run. The standalone project gate uses the resolved project root and explicit artifact hashes; it does not rewrite workspace symlinks or weaken the shared engine's policy.
