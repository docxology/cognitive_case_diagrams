"""Metadata synchronization uses real configuration files and hydrated text."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from src.release_metadata import (
    build_release_metadata,
    validate_release_metadata,
    write_release_metadata,
)


@pytest.fixture
def metadata_tree(tmp_path: Path) -> Path:
    (tmp_path / "docs/manuscript").mkdir(parents=True)
    (tmp_path / "output/manuscript").mkdir(parents=True)
    (tmp_path / "output/manuscript/00_abstract.md").write_text(
        "# Abstract {#sec:abstract}\n\nSynthetic method examples.\n"
    )
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nversion="2.4.0"\n[project.urls]\nRepository="https://github.com/example/project"\n'
    )
    config = {
        "paper": {"title": "Example", "version": "2.4.0", "date": "2026-09-07"},
        "publication": {"doi": "10.5281/zenodo.123", "version_doi": "10.5281/zenodo.124"},
        "authors": [
            {
                "name": "Daniel Ari Friedman",
                "orcid": "0000-0001-6232-9096",
                "affiliation": "Active Inference Institute",
                "email": "daniel@activeinference.institute",
            }
        ],
        "keywords": ["synthetic methods"],
    }
    (tmp_path / "docs/manuscript/config.yaml").write_text(yaml.safe_dump(config))
    return tmp_path


def test_metadata_roundtrip_distinguishes_license_and_doi_roles(metadata_tree: Path) -> None:
    data = write_release_metadata(metadata_tree)
    assert validate_release_metadata(metadata_tree) == data
    assert "doi" not in data["citation"]  # The paper DOI is not a software DOI.
    assert data["citation"]["identifiers"][1]["value"] == "10.5281/zenodo.123"
    assert data["citation"]["identifiers"][0]["value"] == "10.5281/zenodo.124"
    assert data["software"]["license"] == "Apache-2.0"
    assert data["publication"]["license"] == "cc-by-4.0"
    assert data["publication"]["publication_type"] == "preprint"
    assert data["citation"]["authors"][0]["given-names"] == "Daniel Ari"
    assert data["publication"]["description"] == "Synthetic method examples."


@pytest.mark.parametrize(
    "section,key,value",
    [
        ("paper", "version", "2.5.0"),
        ("paper", "date", "not-a-date"),
        ("paper", "title", ""),
        ("paper", "title", "${pending_title}"),
        ("publication", "doi", ""),
        ("publication", "version_doi", "10.5281/zenodo.123"),
        ("publication", "version_doi", "not-a-doi"),
    ],
)
def test_ambiguous_or_unresolved_metadata_rejected(
    metadata_tree: Path, section: str, key: str, value: str
) -> None:
    p = metadata_tree / "docs/manuscript/config.yaml"
    data = yaml.safe_load(p.read_text())
    data[section][key] = value
    p.write_text(yaml.safe_dump(data))
    with pytest.raises(ValueError):
        build_release_metadata(metadata_tree)


@pytest.mark.parametrize(
    "authors", [[], [{"name": "Single"}], [{"name": "Two Names", "orcid": "bad"}]]
)
def test_invalid_author_metadata_rejected(metadata_tree: Path, authors: list) -> None:
    p = metadata_tree / "docs/manuscript/config.yaml"
    data = yaml.safe_load(p.read_text())
    data["authors"] = authors
    p.write_text(yaml.safe_dump(data))
    with pytest.raises(ValueError):
        build_release_metadata(metadata_tree)


@pytest.mark.parametrize("abstract", ["", "${unresolved}", "{{UNRESOLVED}}"])
def test_unhydrated_description_cannot_publish(metadata_tree: Path, abstract: str) -> None:
    (metadata_tree / "output/manuscript/00_abstract.md").write_text(abstract)
    with pytest.raises(ValueError, match="hydrated"):
        build_release_metadata(metadata_tree)


def test_noncanonical_repository_rejected(metadata_tree: Path) -> None:
    p = metadata_tree / "pyproject.toml"
    p.write_text(
        p.read_text().replace("https://github.com/example/project", "http://example.com/project")
    )
    with pytest.raises(ValueError, match="GitHub"):
        build_release_metadata(metadata_tree)


@pytest.mark.parametrize("sidecar", ["CITATION.cff", ".zenodo.json"])
def test_stale_sidecar_rejected(metadata_tree: Path, sidecar: str) -> None:
    write_release_metadata(metadata_tree)
    p = metadata_tree / sidecar
    if sidecar.endswith(".json"):
        data = json.loads(p.read_text())
        data["version"] = "0.0.0"
        p.write_text(json.dumps(data))
    else:
        data = yaml.safe_load(p.read_text())
        data["version"] = "0.0.0"
        p.write_text(yaml.safe_dump(data))
    with pytest.raises(ValueError, match="stale"):
        validate_release_metadata(metadata_tree)


def test_optional_author_fields_do_not_create_placeholders(metadata_tree: Path) -> None:
    p = metadata_tree / "docs/manuscript/config.yaml"
    data = yaml.safe_load(p.read_text())
    data["authors"] = [{"name": "Two Names"}]
    p.write_text(yaml.safe_dump(data))
    result = build_release_metadata(metadata_tree)
    assert result["citation"]["authors"] == [{"given-names": "Two", "family-names": "Names"}]


def test_compound_author_name_uses_explicit_parts(metadata_tree: Path) -> None:
    p = metadata_tree / "docs/manuscript/config.yaml"
    config = yaml.safe_load(p.read_text())
    config["authors"] = [{"name": "Ada van Example", "given_names": "Ada", "family_name": "van Example"}]
    p.write_text(yaml.safe_dump(config))
    assert build_release_metadata(metadata_tree)["citation"]["authors"][0]["family-names"] == "van Example"
    del config["authors"][0]["given_names"]
    p.write_text(yaml.safe_dump(config))
    with pytest.raises(ValueError, match="must both be nonempty"):
        build_release_metadata(metadata_tree)
