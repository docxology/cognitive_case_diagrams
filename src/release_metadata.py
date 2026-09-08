"""Derive citation and deposit metadata from versioned manuscript configuration.

The software keeps Apache-2.0. The publication deposit keeps the existing
paper series' CC-BY-4.0 license. A concept DOI identifies the series; a reserved
version DOI identifies the exact forthcoming deposit, never an existing result.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from src.release_validation import write_json_atomic

try:
    import tomllib
except ImportError:  # Python 3.10
    import tomli as tomllib  # type: ignore[no-redef]


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
    pattern = r"10\.5281/zenodo\.\d+"
    if (
        not re.fullmatch(pattern, concept)
        or not re.fullmatch(pattern, specific)
        or concept == specific
    ):
        raise ValueError("Distinct concept and reserved version Zenodo DOIs are required")
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
        "license": "Apache-2.0",
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
        "license": "Apache-2.0",
        "related_identifiers": [
            {"identifier": specific, "relation": "isSupplementTo", "scheme": "doi"}
        ],
    }
    manuscript = {
        **shared,
        "upload_type": "publication",
        "publication_type": "preprint",
        "license": "cc-by-4.0",
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
        raise ValueError("CITATION.cff is stale; regenerate release metadata")
    if json.loads((root / ".zenodo.json").read_text()) != expected["software"]:
        raise ValueError(".zenodo.json is stale; regenerate release metadata")
    return expected
