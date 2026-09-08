# Release metadata contract

Scope of `src/release_metadata.py`: derive `CITATION.cff`, the software
deposit descriptor (`.zenodo.json`), and the manuscript deposit payload
(`zenodo-publication.json`) from `pyproject.toml` and
`docs/manuscript/config.yaml`; validate publication identifiers; and report
version-scoped software-deposit facts. The module never performs network
I/O and never submits a deposit or claims a deposit's completion.

## Identifier validation

| Field | Rule when nonempty |
| :--- | :--- |
| `publication.doi` | `10.5281/zenodo.<digits>`; distinct from every other role |
| `publication.version_doi` | `10.5281/zenodo.<digits>`; distinct from every other role; required nonempty at build time |
| `publication.prior_version_doi` | `10.5281/zenodo.<digits>`; optional; distinct from every other role |
| `publication.version_record` | `https://zenodo.org/records/<digits>` |

Violations raise `ValueError` at build time and at metric collection
(`generate_manuscript_metrics._read_publication_metadata` calls the same
validator), so a malformed value can never reach hydrated manuscript prose.
Empty optional values pass; an empty concept or version DOI fails the
release build.

## License sourcing and policy

| Artifact | License source | Emitted form |
| :--- | :--- | :--- |
| `CITATION.cff` `license` | `pyproject.toml` `[project] license` | SPDX token as declared (e.g. `Apache-2.0`) |
| `.zenodo.json` `license` | `pyproject.toml` `[project] license` | same value |
| `zenodo-publication.json` `license` | `config.yaml` `metadata.license` | lowercase (e.g. `cc-by-4.0`) |

The manuscript series license policy is `CC-BY-4.0` (documented in the
module docstring). A config declaring any other license raises
`ValueError` with `deliberate policy change required` — silent re-emission
of the old license under a changed config is the defect this prevents.
A missing `pyproject` license is rejected.

## Identity distinctness

The software and manuscript deposits are intentionally different records:
different `upload_type`, different license roles, and different
descriptions. The software description states that the record accompanies
the article, names the article title and working revision, summarizes the
factual software components, and states both license roles. It does not
reprint the article abstract. The software and manuscript concept-DOI
families are distinct (verified 2026-09-08: software concept
`10.5281/zenodo.22655341`, manuscript concept `10.5281/zenodo.19695259`).

`CITATION.cff` `identifiers` carry only the manuscript DOIs (version and
series). The software deposit's own DOI is never self-assigned into
`CITATION.cff`, and a historical deposit DOI is never reassigned to a
later version.

## Software deposit facts

`SOFTWARE_DEPOSIT_RECORDS` maps release versions to their verified
deposits (currently `2.4.0` → version `10.5281/zenodo.22655342`, concept
`10.5281/zenodo.22655341`). `build_release_metadata` validates every
record (Zenodo DOI pattern, no self-collision), reports the working
version's own record under `software_deposits.current` (`None` when no
deposit has been minted for that version yet — absence is never invented),
and moves every other record to `software_deposits.historical`. Release
notes and provenance consumers quote these facts from the emitted
metadata; pilot or scratch observations never enter them.

## Determinism and network guarantee

`build_release_metadata` and `validate_release_metadata` read only
declared files under the project root. Tests enforce the zero-network
guarantee with a socket guard, and `validate_release_metadata` remains a
pure regeneration-parity check against the canonical writers.
