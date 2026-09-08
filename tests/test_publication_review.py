"""Inspection receipts must fail on missing pages and changed publication bytes."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.publication_review import (
    BROWSER_CHECKS,
    REVIEW_PATH,
    publication_fingerprint,
    record_publication_review,
    validate_publication_review,
)


@pytest.fixture
def review_tree(tmp_path: Path) -> Path:
    files = {
        "src/example.py": "value = 1",
        "scripts/run.py": "print(1)",
        "tests/test_example.py": "assert 1",
        "pyproject.toml": "[project]",
        "uv.lock": "version = 1",
        "docs/manuscript/01_a.md": "# Fixture",
        "docs/figure_alt_text.json": '{}',
        "output/manuscript/01_a.md": "# Fixture",
        "output/web/index.html": "<p>Fixture</p>",
        "output/pdf/cognitive_case_diagrams_combined.pdf": None,
        "output/figures/figure_registry.json": '[{"filename":"a.png"}]',
        "output/figures/a.png": "Image bytes are opaque to the receipt",
        "output/metrics.json": '{}',
        "output/manuscript_variables.json": '{}',
        "output/experiments/results.json": '{}',
    }
    for name, text in files.items():
        if text is None:
            continue
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    (tmp_path / "output/pdf").mkdir(parents=True, exist_ok=True)
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.pyplot as plt

    with PdfPages(tmp_path / "output/pdf/cognitive_case_diagrams_combined.pdf") as pdf:
        for _ in range(2):
            figure = plt.figure()
            pdf.savefig(figure)
            plt.close(figure)
    return tmp_path
def observations() -> dict:
    return {
        "pdf_page_count": 2,
        "inspected_pdf_pages": [1, 2],
        "inspected_figures": ["a.png"],
        "browser_checks": dict.fromkeys(BROWSER_CHECKS, True),
        "pdf_metadata_checked": True,
        "reviewer": "Test fixture; no actual visual inspection claimed",
        "method": "Receipt validation test using opaque fixture bytes",
        "limitations": "Receipt authenticity is outside the automated check",
    }


def test_roundtrip_binds_every_artifact(review_tree: Path) -> None:
    receipt = record_publication_review(review_tree, **observations())
    assert validate_publication_review(review_tree) == receipt
    assert len(receipt["inputs"]["sha256"]) == 64


@pytest.mark.parametrize("field,value", [
    ("pdf_page_count", True), ("pdf_page_count", 0),
    ("inspected_pdf_pages", [1]), ("inspected_pdf_pages", [1, 1]),
    ("inspected_figures", []), ("inspected_figures", ["a.png", "a.png"]),
    ("browser_checks", {}), ("browser_checks", dict.fromkeys(BROWSER_CHECKS, False)),
    ("pdf_metadata_checked", False), ("reviewer", ""), ("method", None),
    ("limitations", ""),
])
def test_incomplete_inspection_rejected(review_tree: Path, field: str, value: object) -> None:
    data = observations()
    data[field] = value
    with pytest.raises(ValueError):
        record_publication_review(review_tree, **data)
    assert not (review_tree / REVIEW_PATH).exists()


@pytest.mark.parametrize("name", [
    "src/example.py", "docs/manuscript/01_a.md", "output/manuscript/01_a.md",
    "output/web/index.html", "output/figures/a.png", "output/experiments/results.json",
    "output/pdf/cognitive_case_diagrams_combined.pdf",
])
def test_late_changes_invalidate_inspection(review_tree: Path, name: str) -> None:
    record_publication_review(review_tree, **observations())
    path = review_tree / name
    if path.suffix == ".pdf":
        path.write_bytes(path.read_bytes() + b"\nchanged")
    else:
        path.write_text(path.read_text() + "\nchanged")
    with pytest.raises(ValueError, match="stale"):
        validate_publication_review(review_tree)


def test_malformed_receipt_rejected(review_tree: Path) -> None:
    path = review_tree / REVIEW_PATH
    path.parent.mkdir()
    path.write_text(json.dumps({"schema": "forged"}))
    with pytest.raises(ValueError, match="Unsupported"):
        validate_publication_review(review_tree)


def test_missing_directory_rejected(review_tree: Path) -> None:
    (review_tree / "output/manuscript").rename(review_tree / "output/old")
    with pytest.raises(ValueError, match="Missing"):
        publication_fingerprint(review_tree)


def test_linked_artifact_rejected(review_tree: Path) -> None:
    path = review_tree / "output/figures/a.png"
    path.rename(path.with_suffix(".old"))
    path.symlink_to(path.with_suffix(".old"))
    with pytest.raises(ValueError, match="Linked"):
        publication_fingerprint(review_tree)


def test_tampered_observations_rejected(review_tree: Path) -> None:
    receipt = record_publication_review(review_tree, **observations())
    receipt["observations"]["browser_checks"] = {}
    (review_tree / REVIEW_PATH).write_text(json.dumps(receipt))
    with pytest.raises(ValueError, match="browser"):
        validate_publication_review(review_tree)


def test_declared_page_count_must_match_derived_bytes(review_tree: Path) -> None:
    """Positive: declared == derived passes; negative: N-1/N+1 are rejected."""
    for wrong in (1, 3):
        data = observations()
        data["pdf_page_count"] = wrong
        data["inspected_pdf_pages"] = list(range(1, wrong + 1))
        with pytest.raises(ValueError, match="does not match the 2 pages"):
            record_publication_review(review_tree, **data)


def test_truncated_pdf_is_rejected(review_tree: Path) -> None:
    pdf = review_tree / "output/pdf/cognitive_case_diagrams_combined.pdf"
    pdf.write_bytes(pdf.read_bytes()[: len(pdf.read_bytes()) // 2])
    with pytest.raises(ValueError, match="page tree|trailer|catalog"):
        record_publication_review(review_tree, **observations())
