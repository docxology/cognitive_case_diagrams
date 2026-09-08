"""Machine-readable evidence-status report over the canonical validators.

``ccd-evidence-status`` composes the project's fail-closed validators into
one read-only, per-stage status report. It never generates artifacts, never
writes files, and never touches the network; it only reports the state of
evidence that already exists on disk. The report is deterministic for a
given tree state: no wall-clock fields are emitted, so consumers can digest
the document byte-stably.

Stages and the validators they reuse (no receipt logic is duplicated):

- quality:       ``src.release_validation.validate_quality_receipt``
- experiments:   ``src.experiments.validate_experiment_results``
- manuscript:    ``src.project_validation.validate_project``
- metadata:      ``src.release_metadata.validate_release_metadata``
- visual_review: ``src.publication_review.validate_publication_review``
- release:       ``src.release_bundle.verify_release_archive`` plus the
  release record set under ``output/releases/v<version>/``

Each stage reports one of four states:

- ``missing``: the derived evidence artifact is absent,
- ``stale``: the validator raised ``StaleEvidenceError`` — the evidence was
  produced from, or binds, different inputs than the ones currently on disk,
- ``invalid``: the evidence exists but was rejected for any other reason
  (malformed, failed checks, inconsistent records); every unexpected
  validator escape also maps here with sanitized detail,
- ``validated``: the canonical validator accepted the evidence.

``overall`` is ``validated`` only when every stage is validated, and the
process exits 0 only in that case; mid-pipeline checkouts are expected to
exit 1. The release stage requires the archive to verify AND a three-way
binding: the current quality input fingerprint, the fingerprint embedded in
the archived quality receipt, and ``release-validation.json``'s ``source``
must agree. Archive record corruption (digest or publication-payload
mismatch) is ``invalid``, not ``stale``. The MCP capability summary keeps
its coarser ``stale_or_invalid`` vocabulary and consumes this module's
mapping so the two surfaces cannot drift.

Artifact lookup is fixed to the version declared in ``pyproject.toml``;
release directories are never auto-discovered, so leftover or partially
written candidate versions cannot produce a false pass.
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:  # Python 3.10
    import tomli as tomllib  # type: ignore[no-redef]

from src.release_validation import StaleEvidenceError

SCHEMA = "ccd-evidence-status-v1"
OVERALL_VALIDATED = "validated"
OVERALL_INCOMPLETE = "incomplete"
OVERALL_ERROR = "error"
EXIT_SUCCESS = 0
EXIT_INCOMPLETE = 1

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _declared_version(root: Path) -> str:
    """Return the declared package version, or ``unknown`` when undeclared."""
    try:
        with (root / "pyproject.toml").open("rb") as handle:
            return str(tomllib.load(handle)["project"]["version"])
    except (OSError, KeyError, tomllib.TOMLDecodeError):
        return "unknown"


def _clean(detail: str, root: Path) -> str:
    """Scrub the project-root prefix so reports expose no local layout."""
    return str(detail).replace(str(root), "<project>")


def quality_stage(root: Path) -> dict[str, Any]:
    """Report the source-bound quality receipt through its own validator."""
    from src.release_validation import QUALITY_RECEIPT, validate_quality_receipt

    artifact = QUALITY_RECEIPT.as_posix()
    try:
        receipt = validate_quality_receipt(root)
    except FileNotFoundError as exc:
        return {"state": "missing", "artifact": artifact, "detail": _clean(str(exc), root)}
    except StaleEvidenceError as exc:
        return {"state": "stale", "artifact": artifact, "detail": _clean(str(exc), root)}
    except Exception as exc:  # fail-closed: every validator escape is invalid
        return {"state": "invalid", "artifact": artifact, "detail": _clean(str(exc), root)}
    skipped = int(receipt.get("pytest_skipped") or 0)
    detail = (
        f"quality gate passed: {receipt.get('pytest_passed')} tests, "
        f"{receipt.get('coverage_percent')}% line-and-branch coverage"
    )
    if skipped:
        detail += f"; {skipped} skipped (release assembly rejects skipped tests)"
    return {
        "state": "validated",
        "artifact": artifact,
        "detail": detail,
        "skipped": skipped,
    }


def _stage_experiments(root: Path) -> dict[str, Any]:
    """Report synthetic experiment results through their fail-closed verdict."""
    from src.experiments import DEFAULT_RESULTS_PATH, validate_experiment_results

    artifact = DEFAULT_RESULTS_PATH
    path = root / artifact
    if not path.is_file():
        detail = "Synthetic experiment results have not been generated"
        return {"state": "missing", "artifact": artifact, "detail": detail, "errors": [detail]}
    try:
        results = json.loads(path.read_text(encoding="utf-8"))
        verdict = validate_experiment_results(results, root)
    except FileNotFoundError as exc:
        return {"state": "missing", "artifact": artifact, "detail": _clean(str(exc), root), "errors": []}
    except StaleEvidenceError as exc:
        detail = _clean(str(exc), root)
        return {"state": "stale", "artifact": artifact, "detail": detail, "errors": [detail]}
    except Exception as exc:  # fail-closed: every validator escape is invalid
        detail = _clean(str(exc), root)
        return {"state": "invalid", "artifact": artifact, "detail": detail, "errors": [detail]}
    if verdict.get("valid") is True:
        detail = "synthetic study results match their recorded provenance"
        return {"state": "validated", "artifact": artifact, "detail": detail, "errors": []}
    errors = list(verdict.get("errors", []))
    state = "stale" if verdict.get("stale") else "invalid"
    joined = "; ".join(errors) if errors else "experiment evidence rejected"
    return {"state": state, "artifact": artifact, "detail": _clean(joined, root), "errors": errors}


def _stage_manuscript(root: Path) -> dict[str, Any]:
    """Report the hydrated manuscript and figures through the artifact gate."""
    from src.project_validation import validate_project

    artifact = "output/manuscript"
    if not (root / artifact).is_dir():
        detail = "Hydrated manuscript has not been generated"
        return {"state": "missing", "artifact": artifact, "detail": detail}
    try:
        structure = validate_project(root)
    except FileNotFoundError as exc:
        return {"state": "missing", "artifact": artifact, "detail": _clean(str(exc), root)}
    except StaleEvidenceError as exc:
        return {"state": "stale", "artifact": artifact, "detail": _clean(str(exc), root)}
    except Exception as exc:  # fail-closed: every validator escape is invalid
        return {"state": "invalid", "artifact": artifact, "detail": _clean(str(exc), root)}
    detail = (
        f"{structure.get('chapters')} chapters, {structure.get('figures')} figures: "
        f"{structure.get('status', 'structural checks passed')}"
    )
    return {"state": "validated", "artifact": artifact, "detail": detail}


def _stage_metadata(root: Path) -> dict[str, Any]:
    """Report citation and deposit sidecars through the metadata validator."""
    from src.release_metadata import validate_release_metadata

    artifact = "CITATION.cff"
    absent = [name for name in ("CITATION.cff", ".zenodo.json") if not (root / name).is_file()]
    if absent:
        detail = f"Release metadata sidecars not generated: {', '.join(absent)}"
        return {"state": "missing", "artifact": artifact, "detail": detail}
    try:
        metadata = validate_release_metadata(root)
    except FileNotFoundError as exc:
        return {"state": "missing", "artifact": artifact, "detail": _clean(str(exc), root)}
    except StaleEvidenceError as exc:
        return {"state": "stale", "artifact": artifact, "detail": _clean(str(exc), root)}
    except Exception as exc:  # fail-closed: every validator escape is invalid
        return {"state": "invalid", "artifact": artifact, "detail": _clean(str(exc), root)}
    detail = f"citation and deposit sidecars match configuration for version {metadata.get('version')}"
    return {"state": "validated", "artifact": artifact, "detail": detail}


def _stage_visual_review(root: Path) -> dict[str, Any]:
    """Report the recorded visual inspection through its own validator."""
    from src.publication_review import REVIEW_PATH, validate_publication_review

    artifact = REVIEW_PATH.as_posix()
    rendered = (
        "output/pdf/cognitive_case_diagrams_combined.pdf",
        "output/web/index.html",
    )
    absent = [name for name in rendered if not (root / name).is_file()]
    if absent:
        detail = f"Rendered publication artifacts are absent: {', '.join(absent)}"
        return {"state": "missing", "artifact": artifact, "detail": detail}
    try:
        review = validate_publication_review(root)
    except FileNotFoundError as exc:
        return {"state": "missing", "artifact": artifact, "detail": _clean(str(exc), root)}
    except StaleEvidenceError as exc:
        return {"state": "stale", "artifact": artifact, "detail": _clean(str(exc), root)}
    except Exception as exc:  # fail-closed: every validator escape is invalid
        return {"state": "invalid", "artifact": artifact, "detail": _clean(str(exc), root)}
    observations = review["observations"]
    detail = (
        f"inspection record validated: {observations['pdf_page_count']} pages, "
        f"{len(observations['inspected_figures'])} figures, "
        f"{len(observations['browser_checks'])} browser checks"
    )
    return {"state": "validated", "artifact": artifact, "detail": detail}


def _stage_release(root: Path, version: str) -> dict[str, Any]:
    """Report the reproducibility archive and its bound release records.

    ``validated`` requires the archive to verify through
    ``verify_release_archive`` AND a three-way fingerprint binding: the
    current quality input fingerprint, the fingerprint inside the archived
    quality receipt, and ``release-validation.json``'s ``source`` must all
    agree. A digest or publication-payload disagreement is record
    corruption (``invalid``), while a binding mismatch is ``stale``.
    """
    from src.release_bundle import verify_release_archive
    from src.release_metadata import validate_release_metadata
    from src.release_validation import QUALITY_RECEIPT, quality_input_fingerprint

    artifact = f"output/releases/v{version}"
    if version == "unknown":
        detail = "Release version is not declared in pyproject.toml"
        return {"state": "invalid", "artifact": "pyproject.toml", "detail": detail}
    zip_relative = f"{artifact}/cognitive_case_diagrams-{version}-reproducibility.zip"
    validation_relative = f"{artifact}/release-validation.json"
    publication_relative = f"{artifact}/zenodo-publication.json"
    zip_path = root / zip_relative
    validation_path = root / validation_relative
    publication_path = root / publication_relative
    for path, name in (
        (zip_path, zip_relative),
        (validation_path, validation_relative),
        (publication_path, publication_relative),
    ):
        if not path.is_file():
            detail = f"Release evidence artifact is absent: {name}"
            return {"state": "missing", "artifact": artifact, "detail": detail}
    try:
        current = quality_input_fingerprint(root)["sha256"]
    except Exception as exc:  # fail-closed: the binding cannot be evaluated
        detail = _clean(f"Current quality inputs could not be fingerprinted: {exc}", root)
        return {"state": "invalid", "artifact": artifact, "detail": detail}
    try:
        manifest = verify_release_archive(zip_path)
        with zipfile.ZipFile(zip_path) as bundle:
            receipt_member = QUALITY_RECEIPT.as_posix()
            if receipt_member in bundle.namelist():
                archived = json.loads(bundle.read(receipt_member)).get("inputs", {}).get("sha256")
            else:
                archived = None
        validation = json.loads(validation_path.read_text(encoding="utf-8"))
        if validation.get("schema") != "ccd-release-v1" or validation.get("status") != "passed":
            raise ValueError("Release validation record is unsupported or nonpassing")
        if validation.get("archive_sha256") != manifest["archive_sha256"]:
            raise ValueError("Release validation record disagrees with the archive digest")
        try:
            publication = validate_release_metadata(root)["publication"]
        except StaleEvidenceError as exc:
            detail = f"Release publication payload cannot be regenerated: {exc}"
            raise StaleEvidenceError(detail) from exc
        expected = (json.dumps(publication, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
        if publication_path.read_bytes() != expected:
            raise ValueError("zenodo-publication.json differs from the regenerated payload")
        recorded = validation.get("source")
        if not (current == archived == recorded):
            detail = (
                "Release archive does not bind the current source: current "
                f"{str(current)[:12]}, archived {str(archived)[:12]}, recorded {str(recorded)[:12]}"
            )
            raise StaleEvidenceError(detail)
    except StaleEvidenceError as exc:
        return {"state": "stale", "artifact": artifact, "detail": _clean(str(exc), root)}
    except Exception as exc:  # fail-closed: every validator escape is invalid
        return {"state": "invalid", "artifact": artifact, "detail": _clean(str(exc), root)}
    detail = f"{len(manifest['files'])} archived files verified with source binding confirmed"
    return {
        "state": "validated",
        "artifact": artifact,
        "detail": detail,
        "archive_sha256": manifest["archive_sha256"],
    }


def collect_evidence_status(project_root: Path) -> dict[str, Any]:
    """Collect the per-stage evidence report; read-only, fail-closed, deterministic."""
    root = project_root.resolve(strict=True)
    version = _declared_version(root)
    evidence = {
        "quality": quality_stage(root),
        "experiments": _stage_experiments(root),
        "manuscript": _stage_manuscript(root),
        "metadata": _stage_metadata(root),
        "visual_review": _stage_visual_review(root),
        "release": _stage_release(root, version),
    }
    overall = (
        OVERALL_VALIDATED
        if all(stage["state"] == "validated" for stage in evidence.values())
        else OVERALL_INCOMPLETE
    )
    return {
        "schema": SCHEMA,
        "version": version,
        "overall": overall,
        "exit_code": EXIT_SUCCESS if overall == OVERALL_VALIDATED else EXIT_INCOMPLETE,
        "evidence": evidence,
    }


def main(argv: list[str] | None = None) -> int:
    """Console entry point: print the evidence-status report as JSON."""
    parser = argparse.ArgumentParser(
        prog="ccd-evidence-status",
        description=(
            "Report machine-readable evidence status (read-only; no generation, "
            "no network). Exits 0 only when every evidence stage is validated."
        ),
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Project whose evidence is reported (default: the current directory)",
    )
    args = parser.parse_args(argv)
    attempted = (args.project_root or Path.cwd()).resolve()
    try:
        report = collect_evidence_status(args.project_root or Path.cwd())
    except (OSError, ValueError) as exc:
        detail = _clean(str(exc), attempted)
        if args.project_root is not None:
            detail = detail.replace(str(args.project_root), "<project>")
        envelope = {"schema": SCHEMA, "overall": OVERALL_ERROR, "detail": detail}
        print(json.dumps(envelope), file=sys.stderr)
        return EXIT_INCOMPLETE
    print(json.dumps(report, indent=2, sort_keys=True))
    return int(report["exit_code"])


if __name__ == "__main__":
    sys.exit(main())
