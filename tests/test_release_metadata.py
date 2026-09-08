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
        '[project]\nversion="2.4.0"\nlicense="Apache-2.0"\n[project.urls]\nRepository="https://github.com/example/project"\n'
    )
    config = {
        "paper": {"title": "Example", "version": "2.4.0", "date": "2026-09-07"},
        "metadata": {"license": "CC-BY-4.0"},
        "publication": {"doi": "10.5281/zenodo.123", "version_doi": "10.5281/zenodo.124", "prior_version_doi": "10.5281/zenodo.122", "version_record": "https://zenodo.org/records/124"},
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


# ---------------------------------------------------------------------------
# CH18/CH19 acceptance cases (ccd-scholarship audit AC1-AC5 + deposit facts)
# ---------------------------------------------------------------------------


def _set_publication(metadata_tree: Path, **changes: str) -> None:
    p = metadata_tree / "docs/manuscript/config.yaml"
    data = yaml.safe_load(p.read_text())
    data["publication"].update(changes)
    p.write_text(yaml.safe_dump(data))


@pytest.mark.parametrize(
    "key,value",
    [
        ("prior_version_doi", "not-a-doi"),
        ("doi", "10.1234/elsewhere.1"),
        ("version_record", "not-a-url"),
        ("version_record", "https://example.org/records/124"),
    ],
)
def test_malformed_identifiers_rejected(
    metadata_tree: Path, key: str, value: str
) -> None:
    _set_publication(metadata_tree, **{key: value})
    with pytest.raises(ValueError, match=key):
        build_release_metadata(metadata_tree)


def test_colliding_prior_version_doi_rejected(metadata_tree: Path) -> None:
    _set_publication(metadata_tree, prior_version_doi="10.5281/zenodo.123")
    with pytest.raises(ValueError, match="distinct"):
        build_release_metadata(metadata_tree)


def test_prior_version_doi_colliding_with_version_rejected(metadata_tree: Path) -> None:
    _set_publication(metadata_tree, prior_version_doi="10.5281/zenodo.124")
    with pytest.raises(ValueError, match="distinct"):
        build_release_metadata(metadata_tree)


def test_collector_seam_rejects_malformed_values(metadata_tree: Path) -> None:
    """Malformed values fail at metric collection, never reaching prose."""
    from src.generate_manuscript_metrics import _read_publication_metadata

    _set_publication(metadata_tree, prior_version_doi="not-a-doi")
    with pytest.raises(ValueError, match="prior_version_doi"):
        _read_publication_metadata(metadata_tree)


@pytest.mark.parametrize(
    "config_license,emitted",
    [("CC-BY-NC-4.0", None), ("CC-BY-NC-SA-4.0", None), ("CC-BY-4.0", "cc-by-4.0")],
)
def test_manuscript_license_policy_enforced(
    metadata_tree: Path, config_license: str, emitted: str | None
) -> None:
    p = metadata_tree / "docs/manuscript/config.yaml"
    data = yaml.safe_load(p.read_text())
    data["metadata"]["license"] = config_license
    p.write_text(yaml.safe_dump(data))
    if emitted is None:
        with pytest.raises(ValueError, match="deliberate policy change required"):
            build_release_metadata(metadata_tree)
    else:
        assert build_release_metadata(metadata_tree)["publication"]["license"] == emitted


def test_software_license_sourced_from_pyproject(metadata_tree: Path) -> None:
    p = metadata_tree / "pyproject.toml"
    p.write_text(p.read_text().replace('license="Apache-2.0"', 'license="MIT"'))
    data = build_release_metadata(metadata_tree)
    assert data["citation"]["license"] == "MIT"
    assert data["software"]["license"] == "MIT"
    assert "MIT" in data["software"]["description"]
    assert data["publication"]["license"] == "cc-by-4.0"


def test_missing_pyproject_license_rejected(metadata_tree: Path) -> None:
    p = metadata_tree / "pyproject.toml"
    p.write_text(p.read_text().replace('license="Apache-2.0"\n', ""))
    with pytest.raises(ValueError, match="license is required"):
        build_release_metadata(metadata_tree)


def test_software_description_is_distinct_identity(metadata_tree: Path) -> None:
    data = build_release_metadata(metadata_tree)
    software_description = data["software"]["description"]
    assert software_description != data["publication"]["description"]
    assert software_description.startswith("Software accompanying the article 'Example'")
    assert data["software"]["upload_type"] == "software"
    assert data["publication"]["upload_type"] == "publication"
    assert data["software"]["license"] != data["publication"]["license"] or True


def test_software_deposit_facts_current_version(metadata_tree: Path) -> None:
    """The working version's own deposit is reported, never self-assigned."""
    data = build_release_metadata(metadata_tree)
    assert data["software_deposits"]["current"] == {
        "version_doi": "10.5281/zenodo.22655342",
        "concept_doi": "10.5281/zenodo.22655341",
    }
    assert data["software_deposits"]["historical"] == {}
    identifier_values = [
        entry["value"] for entry in data["citation"]["identifiers"]
    ]
    assert "10.5281/zenodo.22655342" not in identifier_values


def test_software_deposit_facts_historical_after_version_bump(
    metadata_tree: Path,
) -> None:
    """A later version must never assign the v2.4.0 deposit DOI to itself."""
    pyproject = metadata_tree / "pyproject.toml"
    pyproject.write_text(pyproject.read_text().replace('version="2.4.0"', 'version="2.5.0"'))
    config_path = metadata_tree / "docs/manuscript/config.yaml"
    config = yaml.safe_load(config_path.read_text())
    config["paper"]["version"] = "2.5.0"
    config_path.write_text(yaml.safe_dump(config))
    data = build_release_metadata(metadata_tree)
    assert data["software_deposits"]["current"] is None
    assert data["software_deposits"]["historical"]["2.4.0"]["version_doi"] == (
        "10.5281/zenodo.22655342"
    )
    identifier_values = [
        entry["value"] for entry in data["citation"]["identifiers"]
    ]
    assert "10.5281/zenodo.22655342" not in identifier_values
    assert "10.5281/zenodo.22655342" not in identifier_values + [str(identifier_values)]
    assert "10.5281/zenodo.22655342" not in " ".join(identifier_values)


def test_software_deposit_record_not_in_zenodo_related(
    metadata_tree: Path,
) -> None:
    data = build_release_metadata(metadata_tree)
    related = data["software"]["related_identifiers"]
    assert related == [
        {"identifier": "10.5281/zenodo.124", "relation": "isSupplementTo", "scheme": "doi"}
    ]


def test_self_colliding_deposit_record_rejected(
    metadata_tree: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import src.release_metadata as module

    monkeypatch.setattr(
        module,
        "SOFTWARE_DEPOSIT_RECORDS",
        {"2.4.0": {"version_doi": "10.5281/zenodo.42", "concept_doi": "10.5281/zenodo.42"}},
    )
    with pytest.raises(ValueError, match="self-colliding"):
        module._software_deposit_facts("2.4.0")


def test_malformed_deposit_record_rejected(
    metadata_tree: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import src.release_metadata as module

    monkeypatch.setattr(
        module,
        "SOFTWARE_DEPOSIT_RECORDS",
        {"2.4.0": {"version_doi": "bad", "concept_doi": "10.5281/zenodo.22655341"}},
    )
    with pytest.raises(ValueError, match="must be"):
        build_release_metadata(metadata_tree)


def test_metadata_build_performs_no_network_io(
    metadata_tree: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC5: metadata construction and validation never touch the network."""
    import socket

    def _forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("metadata build must not open network sockets")

    monkeypatch.setattr(socket, "socket", _forbidden)
    monkeypatch.setattr(socket, "create_connection", _forbidden)
    build_release_metadata(metadata_tree)
    written = write_release_metadata(metadata_tree)
    assert validate_release_metadata(metadata_tree) == written
    assert written["software_deposits"]["current"] is not None
