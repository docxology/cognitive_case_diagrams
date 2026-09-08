"""Derive citation and deposit metadata from versioned manuscript configuration.

Code is distributed under the license declared in ``pyproject.toml``; the
publication deposit keeps the paper series' CC-BY-4.0 license policy. A
concept DOI identifies the series; a reserved version DOI identifies the
exact forthcoming deposit, never an existing result. Software deposit
records are version-scoped facts: a deposit DOI belongs to exactly one
release version and is never reassigned to a later version.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from src.release_validation import StaleEvidenceError, write_json_atomic

try:
    import tomllib
except ImportError:  # Python 3.10
    import tomli as tomllib  # type: ignore[no-redef]

ZENODO_DOI_PATTERN = r"10\.5281/zenodo\.\d+"
ZENODO_RECORD_PATTERN = r"https://zenodo\.org/records/\d+"
# Documented series policy (module docstring): the separately licensed
# manuscript deposit retains CC-BY-4.0. A config declaring anything else is
# a deliberate policy change and must fail the build instead of silently
# emitting the old license.
MANUSCRIPT_LICENSE_POLICY = "CC-BY-4.0"
# Factual component summary for the software deposit description. Every
# component exists in the repository; no capability beyond the claim ledger.
SOFTWARE_COMPONENTS_SUMMARY = (
    "executable case-role graphs, pregroup reductions, tensor contractions, "
    "synthetic similarity matrices, Bayesian belief filtering, quantile "
    "utilities, POVM measurement models, seeded synthetic studies, and a "
    "reproducibility archive"
)
# Version-scoped record of software deposits that exist remotely (verified
# against the Zenodo API captures of 2026-09-08; the concept families of the
# software and the manuscript are distinct). A record is historical once the
# working version moves past it; the working version's own deposit DOI is
# never self-assigned into CITATION.cff, whose identifiers carry only the
# manuscript DOIs.
SOFTWARE_DEPOSIT_RECORDS: dict[str, dict[str, str]] = {
    "2.4.0": {
        "version_doi": "10.5281/zenodo.22655342",
        "concept_doi": "10.5281/zenodo.22655341",
    },
}


def validate_publication_identifiers(publication: Any) -> None:
    """Reject malformed or colliding publication DOI/record identifiers.

    Empty values are skipped (optional keys are handled by their own
    consumers); every nonempty DOI must be a Zenodo DOI, the record URL
    must point at zenodo.org, and the concept, version, and prior-version
    DOIs must be pairwise distinct when present.
    """
    doi_values: dict[str, str] = {}
    for key in ("doi", "version_doi", "prior_version_doi"):
        value = str(publication.get(key) or "").strip()
        if value and not re.fullmatch(ZENODO_DOI_PATTERN, value):
            raise ValueError(
                f"publication.{key} must be a Zenodo DOI of the form "
                f"10.5281/zenodo.<digits>, got {value!r}"
            )
        if value:
            doi_values[key] = value
    record = str(publication.get("version_record") or "").strip()
    if record and not re.fullmatch(ZENODO_RECORD_PATTERN, record):
        raise ValueError(
            "publication.version_record must be a Zenodo record URL of the "
            f"form https://zenodo.org/records/<digits>, got {record!r}"
        )
    if len(set(doi_values.values())) != len(doi_values):
        colliding = sorted(
            key
            for key, value in doi_values.items()
            if sum(1 for other in doi_values.values() if other == value) > 1
        )
        raise ValueError(f"Publication DOI roles must be distinct: {colliding}")


def _software_deposit_facts(version: str) -> dict[str, Any]:
    """Validate deposit records and split current from historical facts."""
    for record_version, record in SOFTWARE_DEPOSIT_RECORDS.items():
        for key in ("version_doi", "concept_doi"):
            value = str(record.get(key) or "")
            if not re.fullmatch(ZENODO_DOI_PATTERN, value):
                raise ValueError(
                    f"Software deposit record {record_version}: {key} must be "
                    f"a Zenodo DOI, got {value!r}"
                )
        if record["version_doi"] == record["concept_doi"]:
            raise ValueError(f"Software deposit record {record_version} is self-colliding")
    current = SOFTWARE_DEPOSIT_RECORDS.get(version)
    historical = {
        record_version: dict(record)
        for record_version, record in SOFTWARE_DEPOSIT_RECORDS.items()
        if record_version != version
    }
    return {"current": dict(current) if current else None, "historical": historical}


def build_release_metadata(project_root: Path) -> dict[str, Any]:
    """Build consistent CFF/software/publication metadata or reject ambiguous inputs."""
    root = project_root.resolve(strict=True)
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    config = yaml.safe_load((root / "docs/manuscript/config.yaml").read_text())
    paper, publication = config["paper"], config["publication"]
    version = str(project["version"])
    if not re.fullmatch(r"\d+\.\d+\.\d+", version) or str(paper["version"]) != version:
        raise ValueError("Software and paper must declare the same stable semantic version")
    day = str(paper["date"])
    date.fromisoformat(day)
    concept = publication.get("doi", "")
    specific = publication.get("version_doi", "")
    if not concept or not specific:
        raise ValueError("Concept and version Zenodo DOIs are required for release metadata")
    validate_publication_identifiers(publication)
    software_license = str(project.get("license", "")).strip()
    if not software_license:
        raise ValueError("pyproject [project] license is required for software deposit metadata")
    config_license = str((config.get("metadata") or {}).get("license", "")).strip()
    if config_license.upper() != MANUSCRIPT_LICENSE_POLICY:
        raise ValueError(
            f"Manuscript deposit license policy is {MANUSCRIPT_LICENSE_POLICY}; "
            f"config declares {config_license!r} - deliberate policy change required"
        )
    manuscript_license = config_license.lower()
    repository = project["urls"]["Repository"].removesuffix(".git")
    if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("Release repository must be a canonical GitHub HTTPS URL")
    title = str(paper["title"]).strip()
    if not title or "${" in title:
        raise ValueError("Release title is empty or unresolved")
    abstract_path = root / "output/manuscript/00_abstract.md"
    abstract = abstract_path.read_text()
    abstract = re.sub(r"^#+[^\n]*\n", "", abstract, flags=re.M).strip()
    abstract = re.sub(r"\{#[\w:.-]+\}", "", abstract)
    if not abstract or "${" in abstract or "{{" in abstract:
        raise ValueError("Release description requires a fully hydrated abstract")
    cff_authors = []
    creators = []
    for author in config["authors"]:
        name = author["name"].strip()
        if len(name.split()) < 2:
            raise ValueError("Author needs explicit given/family names for citation metadata")
        if "given_names" in author or "family_name" in author:
            given, family = author.get("given_names"), author.get("family_name")
            if not isinstance(given, str) or not given.strip() or not isinstance(family, str) or not family.strip():
                raise ValueError("Explicit author given_names and family_name must both be nonempty")
            given, family = given.strip(), family.strip()
        else:
            given, family = name.rsplit(" ", 1)  # Legacy config; use explicit fields for compound family names.
        cff_author = {"given-names": given, "family-names": family}
        creator = {"name": f"{family}, {given}"}
        if author.get("orcid"):
            orcid = author["orcid"].removeprefix("https://orcid.org/")
            if not re.fullmatch(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]", orcid):
                raise ValueError("Invalid author ORCID syntax")
            cff_author["orcid"] = f"https://orcid.org/{orcid}"
            creator["orcid"] = orcid
        if author.get("affiliation"):
            cff_author["affiliation"] = author["affiliation"]
            creator["affiliation"] = author["affiliation"]
        if author.get("email"):
            cff_author["email"] = author["email"]
        cff_authors.append(cff_author)
        creators.append(creator)
    if not creators:
        raise ValueError("At least one author is required")
    keywords = config.get("keywords", [])
    release_url = f"{repository}/releases/tag/v{version}"
    cff = {
        "cff-version": "1.2.0",
        "message": "Cite the exact software release and manuscript version used.",
        "title": title,
        "abstract": abstract,
        "type": "software",
        "authors": cff_authors,
        "version": version,
        "date-released": day,
        "license": software_license,
        "repository-code": repository,
        "url": release_url,
        "keywords": keywords,
        "identifiers": [
            {"type": "doi", "value": specific, "description": "Associated manuscript version"},
            {"type": "doi", "value": concept, "description": "Associated manuscript series"}
        ],
    }
    shared = {
        "title": title,
        "description": abstract,
        "creators": creators,
        "version": version,
        "publication_date": day,
        "access_right": "open",
        "keywords": keywords,
    }
    software = {
        **shared,
        "upload_type": "software",
        "license": software_license,
        "description": (
            f"Software accompanying the article '{title}' (working revision {version}): "
            f"{SOFTWARE_COMPONENTS_SUMMARY}. Code is distributed under {software_license}; "
            "the article text carries the separate manuscript deposit's "
            f"{manuscript_license} license."
        ),
        "related_identifiers": [
            {"identifier": specific, "relation": "isSupplementTo", "scheme": "doi"}
        ],
    }
    manuscript = {
        **shared,
        "upload_type": "publication",
        "publication_type": "preprint",
        "license": manuscript_license,
        "related_identifiers": [
            {"identifier": release_url, "relation": "isSupplementTo", "scheme": "url"}
        ],
    }
    return {
        "version": version,
        "date": day,
        "concept_doi": concept,
        "version_doi": specific,
        "github_release_url": release_url,
        "citation": cff,
        "software": software,
        "publication": manuscript,
        "software_deposits": _software_deposit_facts(version),
    }


def write_release_metadata(project_root: Path) -> dict[str, Any]:
    """Regenerate metadata sidecars; never submit a deposit or claim its completion."""
    root = project_root.resolve(strict=True)
    metadata = build_release_metadata(root)
    (root / "CITATION.cff").write_text(
        yaml.safe_dump(metadata["citation"], sort_keys=False, allow_unicode=True)
    )
    write_json_atomic(root / ".zenodo.json", metadata["software"])
    return metadata


def validate_release_metadata(project_root: Path) -> dict[str, Any]:
    """Ensure checked-in citation/Zenodo sidecars match their canonical writers."""
    root = project_root.resolve(strict=True)
    expected = build_release_metadata(root)
    if yaml.safe_load((root / "CITATION.cff").read_text()) != expected["citation"]:
        raise StaleEvidenceError("CITATION.cff is stale; regenerate release metadata")
    if json.loads((root / ".zenodo.json").read_text()) != expected["software"]:
        raise StaleEvidenceError(".zenodo.json is stale; regenerate release metadata")
    return expected
