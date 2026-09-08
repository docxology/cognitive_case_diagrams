#!/usr/bin/env python3
"""Validate the project and assemble a source/data/manuscript release archive."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from xml.etree.ElementTree import ParseError

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.project_validation import validate_project
from src.publication_review import validate_publication_review
from src.release_bundle import build_release_archive
from src.release_metadata import validate_release_metadata, write_release_metadata
from src.release_validation import validate_quality_receipt, write_json_atomic


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--metadata-only",
        action="store_true",
        help="Regenerate citation/deposit sidecars from canonical configuration",
    )
    parser.add_argument(
        "--output", type=Path, help="Release directory (default: output/releases/vVERSION)"
    )
    args = parser.parse_args()
    try:
        if args.metadata_only:
            metadata = write_release_metadata(ROOT)
            print(f"Metadata regenerated for {metadata['version']}; nothing published")
            return 0
        quality = validate_quality_receipt(ROOT)
        if quality["pytest_skipped"]:
            raise ValueError(
                "Release gate requires all configured tests, including MCP, to execute"
            )
        structure = validate_project(ROOT)
        review = validate_publication_review(ROOT)
        metadata = validate_release_metadata(ROOT)
        required = [
            ROOT / "output/pdf/cognitive_case_diagrams_combined.pdf",
            ROOT / "output/web/index.html",
            ROOT / "output/experiments/results.json",
            ROOT / "SKILL.md",
        ]
        if any(not p.is_file() for p in required):
            raise ValueError(
                "Release requires PDF, HTML, experiment results, and installable skill"
            )
        destination = (
            args.output or ROOT / "output/releases" / f"v{metadata['version']}"
        ).resolve()
        archive = destination / f"cognitive_case_diagrams-{metadata['version']}-reproducibility.zip"
        manifest = build_release_archive(
            ROOT, archive, version=metadata["version"], publication_date=metadata["date"]
        )
        if (validate_quality_receipt(ROOT) != quality or validate_publication_review(ROOT) != review
                or validate_release_metadata(ROOT) != metadata):
            raise ValueError("Release inputs changed during assembly; discard and rebuild the candidate")
        write_json_atomic(destination / "zenodo-publication.json", metadata["publication"])
        write_json_atomic(
            destination / "release-validation.json",
            {
                "schema": "ccd-release-v1",
                "status": "passed",
                "source": quality["quality_input_fingerprint"],
                "tests_passed": quality["pytest_passed"],
                "coverage_percent": quality["coverage_percent"],
                "structure": structure,
                "publication_review_fingerprint": review["inputs"]["sha256"],
                "review_limitations": review["observations"]["limitations"],
                "archive_sha256": manifest["archive_sha256"],
                "version": metadata["version"],
                "concept_doi": metadata["concept_doi"],
                "version_doi": metadata["version_doi"],
                "publication_status": "prepared; remote verification required",
            },
        )
        print(f"Validated release archive: {archive.name} ({len(manifest['files'])} files)")
        print(f"SHA-256: {manifest['archive_sha256']}")
        return 0
    except (OSError, ValueError, KeyError, yaml.YAMLError, ParseError) as exc:
        print(f"Release assembly failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
