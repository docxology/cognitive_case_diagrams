"""Bind recorded human/agent visual inspection to the exact publication bytes.

This is an inspection record, not an automated judgment of scientific validity
or accessibility certification. Reviewers must actually inspect the pages and
figures and operate the rendered web article before recording these observations.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.release_validation import StaleEvidenceError, file_sha256, quality_input_fingerprint, write_json_atomic

REVIEW_PATH = Path("output/reports/publication_review.json")
BROWSER_CHECKS = frozenset(
    {"images_loaded", "internal_links_resolved", "console_clean", "keyboard_navigation", "narrow_viewport"}
)


def publication_fingerprint(project_root: Path) -> dict[str, Any]:
    """Hash source, hydrated chapters, registry, figures and final render artifacts."""
    root = project_root.resolve(strict=True)
    paths = [
        root / "output/pdf/cognitive_case_diagrams_combined.pdf",
        root / "output/web/index.html",
        root / "output/figures/figure_registry.json",
        root / "output/metrics.json",
        root / "output/manuscript_variables.json",
        root / "output/experiments/results.json",
        root / "docs/figure_alt_text.json",
    ]
    for name in ("docs/manuscript", "output/manuscript", "output/web", "output/figures"):
        directory = root / name
        if directory.is_symlink() or not directory.is_dir():
            raise ValueError(f"Missing or linked publication directory: {name}")
        paths.extend(
            p for p in directory.rglob("*")
            if p.is_file() and not any(part.startswith(".") for part in p.relative_to(directory).parts)
        )
    files = {}
    for path in sorted(set(paths)):
        relative = path.relative_to(root)
        if any((root / Path(*relative.parts[:i])).is_symlink() for i in range(1, len(relative.parts) + 1)):
            raise ValueError(f"Linked publication input: {relative}")
        files[relative.as_posix()] = file_sha256(path)
    inputs = {"quality_source": quality_input_fingerprint(root)["sha256"], "files": files}
    digest = hashlib.sha256(json.dumps(inputs, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {**inputs, "sha256": digest}


def _validate_observations(root: Path, observations: Mapping[str, Any]) -> None:
    count = observations.get("pdf_page_count")
    pages = observations.get("inspected_pdf_pages", [])
    if type(count) is not int or count <= 0 or pages != list(range(1, count + 1)):
        raise ValueError("Every PDF page must have a recorded visual inspection")
    registry = json.loads((root / "output/figures/figure_registry.json").read_text())
    expected = sorted(entry["filename"] for entry in registry)
    if not expected or observations.get("inspected_figures") != expected:
        raise ValueError("Every registered figure must have a recorded visual inspection")
    checks = observations.get("browser_checks", {})
    if set(checks) != BROWSER_CHECKS or any(value is not True for value in checks.values()):
        raise ValueError("All declared browser checks must have passing observations")
    if observations.get("pdf_metadata_checked") is not True:
        raise ValueError("PDF identity and metadata inspection is required")
    for name in ("reviewer", "method", "limitations"):
        if not isinstance(observations.get(name), str) or not observations[name].strip():
            raise ValueError(f"Inspection provenance requires {name}")


def record_publication_review(
    project_root: Path,
    *,
    pdf_page_count: int,
    inspected_pdf_pages: Sequence[int],
    inspected_figures: Sequence[str],
    browser_checks: Mapping[str, bool],
    pdf_metadata_checked: bool,
    reviewer: str,
    method: str,
    limitations: str,
) -> dict[str, Any]:
    """Record completed inspections, rejecting incomplete or failed check lists."""
    root = project_root.resolve(strict=True)
    observations = {
        "pdf_page_count": pdf_page_count,
        "inspected_pdf_pages": list(inspected_pdf_pages),
        "inspected_figures": sorted(inspected_figures),
        "browser_checks": dict(browser_checks),
        "pdf_metadata_checked": pdf_metadata_checked,
        "reviewer": reviewer,
        "method": method,
        "limitations": limitations,
    }
    _validate_observations(root, observations)
    receipt = {
        "schema": "ccd-publication-review-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "inputs": publication_fingerprint(root),
        "observations": observations,
    }
    write_json_atomic(root / REVIEW_PATH, receipt)
    return receipt


def validate_publication_review(project_root: Path) -> dict[str, Any]:
    """Reject absent, incomplete or stale inspection records before release."""
    root = project_root.resolve(strict=True)
    receipt = json.loads((root / REVIEW_PATH).read_text())
    if not isinstance(receipt, dict) or receipt.get("schema") != "ccd-publication-review-v1":
        raise ValueError("Unsupported publication review record")
    _validate_observations(root, receipt["observations"])
    if receipt.get("inputs") != publication_fingerprint(root):
        raise StaleEvidenceError("Publication review is stale for the current source or artifacts")
    return receipt
