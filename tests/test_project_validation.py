"""Cross-artifact gate positive and adversarial controls using real files.

Every mutation is applied to a byte-for-byte copy of a canonical valid
project tree (see ``tests/fixtures_manuscript.py``) and must fail the gate
with its own diagnostic. Registry and manifest mutations rebind the
variables manifest first so each test isolates exactly one gate.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

pytest_plugins = ("fixtures_manuscript",)

from src.manuscript_injection import render_all_chapters  # noqa: E402
from src.manuscript_variables import write_variables_manifest  # noqa: E402
from src.project_validation import lint_manuscript_equation_labels, validate_project  # noqa: E402


def _metrics(gate_tree: Path) -> dict:
    return json.loads((gate_tree / "output" / "metrics.json").read_text())


def _write_metrics(gate_tree: Path, metrics: dict) -> None:
    (gate_tree / "output" / "metrics.json").write_text(json.dumps(metrics))


def _rebind(gate_tree: Path, metrics: dict | None = None) -> None:
    """Regenerate hydrated chapters and manifest for the given metrics."""
    metrics = metrics if metrics is not None else _metrics(gate_tree)
    render_all_chapters(
        gate_tree / "docs" / "manuscript",
        metrics,
        gate_tree / "output" / "manuscript",
    )
    write_variables_manifest(gate_tree, metrics)


def _append_chapter(gate_tree: Path, addition: str) -> None:
    source = gate_tree / "docs" / "manuscript" / "01_a.md"
    source.write_text(source.read_text() + addition)
    rendered = gate_tree / "output" / "manuscript" / "01_a.md"
    rendered.write_text(rendered.read_text() + addition)


def _rewrite_registry(gate_tree: Path, mutate) -> None:
    path = gate_tree / "output" / "figures" / "figure_registry.json"
    registry = json.loads(path.read_text())
    mutate(registry)
    path.write_text(json.dumps(registry))


#: mutation name -> (expected exception, regex over the diagnostic)
MUTATIONS: dict[str, tuple[type[Exception], str]] = {
    "unknown_token": (ValueError, "Unresolved manuscript token"),
    "duplicate_label": (ValueError, "Duplicate manuscript labels"),
    "stale": (ValueError, "Stale hydrated chapter"),
    "missing_chapter": (ValueError, "Hydrated chapter set differs"),
    "duplicate_bib": (ValueError, "Duplicate bibliography keys"),
    "unresolved_citation": (ValueError, "Unresolved citations"),
    "missing_image": (ValueError, "Missing figure"),
    "checksum": (ValueError, "checksum mismatch"),
    "figure_fingerprint": (ValueError, "Stale figure generation inputs"),
    "stale_environment": (ValueError, "Stale figure generation environment"),
    "missing_environment_fingerprint": (
        ValueError, "Missing figure generation environment fingerprint"),
    "missing_alt": (ValueError, "Missing accessibility text"),
    "stale_alt": (ValueError, "Stale accessibility text"),
    "registry_label": (ValueError, "registry label mismatch"),
    "registry_path": (ValueError, "registry path mismatch"),
    "registry_duplicate": (ValueError, "Duplicate figure registry filenames"),
    "orphan_registry_entry": (ValueError, "Unreferenced registry entries"),
    "figure_count": (ValueError, "Figure count differs from metrics"),
    "stale_auxiliary": (ValueError, "Stale hydrated auxiliary"),
    "unknown_metric_key": (ValueError, "Unregistered manuscript variables"),
    "missing_required_metric": (ValueError, "Required manuscript variables missing"),
    "nonfinite_metric": (ValueError, "coverage_percent"),
    "hard_coded_prose": (ValueError, "Hard-coded manuscript claims"),
    "missing_manifest": (FileNotFoundError, "manuscript_variables.json"),
    "markdown_table": (ValueError, "Malformed markdown table"),
    "missing_receipt": (FileNotFoundError, "quality_receipt.json"),
    "missing_experiments": (FileNotFoundError, "results.json"),
    "stale_manifest": (ValueError, "Manuscript variable manifest is stale"),
    "equation_sequence_gap": (ValueError, "Non-consecutive manuscript equation labels"),
}


def _refresh_receipt(gate_tree: Path) -> None:
    """Re-record the tmp receipt so source edits isolate later gates."""
    from fixtures_manuscript import _create_receipt

    _create_receipt(gate_tree)


_SOURCE_EDIT_MUTATIONS = frozenset(
    {"unknown_token", "duplicate_label", "duplicate_bib",
     "unresolved_citation", "hard_coded_prose", "equation_sequence_gap"}
)


def _apply_mutation(gate_tree: Path, mutation: str) -> None:
    if mutation == "unknown_token":
        _append_chapter(gate_tree, "\n${invented_variable}\n")
    elif mutation == "duplicate_label":
        _append_chapter(gate_tree, "\n{#sec:test}\n")
    elif mutation == "stale":
        rendered = gate_tree / "output" / "manuscript" / "01_a.md"
        rendered.write_text("old text")
    elif mutation == "missing_chapter":
        extra = gate_tree / "output" / "manuscript" / "02_extra.md"
        extra.write_text("extra chapter")
    elif mutation == "duplicate_bib":
        bib = gate_tree / "docs" / "manuscript" / "references.bib"
        bib.write_text(bib.read_text() + "\n@book{ref, title={Again}, year={2026}}")
    elif mutation == "unresolved_citation":
        _append_chapter(gate_tree, "\n[@nowhere]\n")
    elif mutation == "missing_image":
        image = gate_tree / "output" / "figures" / "a.png"
        image.rename(image.with_name("moved.png"))
    elif mutation in (
        "checksum",
        "figure_fingerprint",
        "stale_environment",
        "missing_environment_fingerprint",
        "missing_alt",
        "stale_alt",
        "registry_label",
        "registry_path",
        "registry_duplicate",
        "orphan_registry_entry",
    ):
        registry_mutations = {
            "checksum": lambda r: r[0].update(sha256="0" * 64),
            "figure_fingerprint": lambda r: r[0].update(
                generator_input_fingerprint="stale"
            ),
            "stale_environment": lambda r: r[0].update(
                environment_fingerprint="0" * 64
            ),
            "missing_environment_fingerprint": lambda r: r[0].pop(
                "environment_fingerprint"
            ),
            "missing_alt": lambda r: r[0].update(alt_text=""),
            "stale_alt": lambda r: r[0].update(alt_text="Wrong description"),
            "registry_label": lambda r: r[0].update(label="fig:wrong"),
            "registry_path": lambda r: r[0].update(path="/incorrect.png"),
            "registry_duplicate": lambda r: r.append(dict(r[0])),
            "orphan_registry_entry": lambda r: r.append(
                {**r[0], "filename": "orphan.png"}
            ),
        }
        _rewrite_registry(gate_tree, registry_mutations[mutation])
        _rebind(gate_tree)
    elif mutation == "figure_count":
        metrics = {**_metrics(gate_tree), "total_figures": "7"}
        _write_metrics(gate_tree, metrics)
        _rebind(gate_tree, metrics)
    elif mutation == "stale_auxiliary":
        aux = gate_tree / "output" / "manuscript" / "config.yaml"
        aux.write_text("paper: {}")
    elif mutation == "unknown_metric_key":
        metrics = _metrics(gate_tree)
        metrics["invented_statistic"] = "1"
        _write_metrics(gate_tree, metrics)
    elif mutation == "missing_required_metric":
        metrics = _metrics(gate_tree)
        metrics.pop("total_test_count")
        _write_metrics(gate_tree, metrics)
    elif mutation == "nonfinite_metric":
        metrics = _metrics(gate_tree)
        metrics["coverage_percent"] = "inf"
        _write_metrics(gate_tree, metrics)
    elif mutation == "hard_coded_prose":
        _append_chapter(gate_tree, "\nA supplied weight is 0.8 here.\n")
    elif mutation == "markdown_table":
        _append_chapter(
            gate_tree, "\n| A | B |\n| :--- | :--- |\n| $|Z|$ | c |\n"
        )
    elif mutation == "equation_sequence_gap":
        _append_chapter(gate_tree, "\n$$ {#eq:eq-1-2}\n")
    elif mutation == "missing_manifest":
        (gate_tree / "output" / "manuscript_variables.json").unlink()
    elif mutation == "missing_receipt":
        (gate_tree / "output" / "reports" / "quality_receipt.json").unlink()
    elif mutation == "missing_experiments":
        (gate_tree / "output" / "experiments" / "results.json").unlink()
    elif mutation == "stale_manifest":
        path = gate_tree / "output" / "manuscript_variables.json"
        manifest = json.loads(path.read_text())
        manifest["variables"]["total_test_count"]["value"] = "999"
        path.write_text(json.dumps(manifest))
    else:  # pragma: no cover - table completeness guard
        raise AssertionError(f"unknown mutation {mutation}")

    if mutation in _SOURCE_EDIT_MUTATIONS:
        # Authored sources are fingerprint inputs: refresh the receipt and
        # rebind hydrated/manifest outputs so the intended gate is isolated.
        _refresh_receipt(gate_tree)
        if mutation != "unknown_token":
            _rebind(gate_tree)
        else:
            # Render would reject the invented token; rebind manifest only.
            write_variables_manifest(gate_tree, _metrics(gate_tree))


@pytest.mark.parametrize("mutation", sorted(MUTATIONS))
def test_mutation_is_rejected_with_its_own_diagnostic(
    gate_tree: Path, mutation: str
) -> None:
    expected_type, message = MUTATIONS[mutation]
    _apply_mutation(gate_tree, mutation)
    with pytest.raises(expected_type, match=message):
        validate_project(gate_tree)


def test_valid_artifact_passes_all_gates(gate_tree: Path) -> None:
    result = validate_project(gate_tree)
    assert result["chapters"] == 1
    assert result["figures"] == 1
    assert result["bibliography_entries"] == 1
    assert result["labels"] == 2
    assert "visual review" in result["status"]


def test_markdown_table_lint_flags_unescaped_math_pipe(tmp_path: Path) -> None:
    """The 11b-style defect — a row like ``| $|Z|$ | ... |`` — splits into more
    cells than its header and carries an unescaped pipe inside inline math."""
    from src.project_validation import lint_markdown_tables

    doc = tmp_path / "11b_defect.md"
    doc.write_text(
        "| Symbol | Meaning |\n"
        "| :--- | :--- |\n"
        "| $|Z|$ | cardinality of Z |\n",
        encoding="utf-8",
    )
    findings = lint_markdown_tables(doc.name, doc.read_text(encoding="utf-8"))
    assert findings == [
        f"{doc.name}:3: unescaped '|' inside inline math in a table row",
        f"{doc.name}:3: table row has 4 cells but header row (line 1) has 2",
    ]


def test_markdown_table_lint_accepts_clean_table(tmp_path: Path) -> None:
    """Clean tables, escaped math pipes, and fenced examples produce no findings."""
    from src.project_validation import lint_markdown_tables

    doc = tmp_path / "clean.md"
    doc.write_text(
        "| Symbol | Meaning |\n"
        "| :--- | :--- |\n"
        "| $\\|Z\\|$ | cardinality of Z |\n"
        "| n | element count |\n"
        "\n"
        "```\n| ignored | fenced | example |\n```\n",
        encoding="utf-8",
    )
    assert lint_markdown_tables(doc.name, doc.read_text(encoding="utf-8")) == []


def test_equation_label_lint_flags_sequence_gap_with_file_and_line() -> None:
    """A skipped number inside one chapter is reported at the offending line."""
    sources = {
        "02_case_systems.md": "$$ {#eq:eq-2-1}\n\ntext\n\n$$ {#eq:eq-2-3}\n",
    }
    findings = lint_manuscript_equation_labels(sources)
    assert findings == [
        "02_case_systems.md:5: chapter 2 equation numbers are not a "
        "gap-free sequence starting at 1: found [1, 3]",
    ]


def test_equation_label_lint_requires_sequence_starting_at_one() -> None:
    sources = {"04_categorical_semantics.md": "$$ {#eq:eq-4-2}\n"}
    findings = lint_manuscript_equation_labels(sources)
    assert findings and "found [2]" in findings[0] and findings[0].startswith(
        "04_categorical_semantics.md:1: chapter 4"
    )


def test_equation_label_lint_accepts_gap_free_and_named_labels() -> None:
    """Gap-free per chapter prefix; named labels (and non-numeric suffixes) are exempt."""
    sources = {
        "04_categorical_semantics.md": "$$ {#eq:eq-4-1}\n\n$$ {#eq:eq-4-2}\n",
        "04b_compact_closure_complexity.md": "$$ {#eq:eq-4b-1}\n",
        "07_cognitive_integration.md": "$$ {#eq:variational-bound}\n",
        "07c_daif_results.md": (
            "$$ {#eq:eq-7-1}\n\n$$ {#eq:eq-7c-qr}\n\n$$ {#eq:eq-7c-vmp}\n"
        ),
    }
    assert lint_manuscript_equation_labels(sources) == []


def test_equation_label_lint_judges_chapter_prefixes_independently() -> None:
    """04 and 04b prefixes never compare against each other (the eq-4-1 defect class)."""
    sources = {
        "04_categorical_semantics.md": "$$ {#eq:eq-4-1}\n",
        "04b_compact_closure_complexity.md": "$$ {#eq:eq-4b-1}\n",
    }
    assert lint_manuscript_equation_labels(sources) == []


def test_alt_text_literal_is_caught_by_scanner_after_manifest_rebind(
    gate_tree: Path,
) -> None:
    """Isolate the scanner: rebind manifest so only the alt literal is stale."""
    alt_path = gate_tree / "docs" / "figure_alt_text.json"
    alt_path.write_text(json.dumps({"a.png": "White square fixture at 0.8 mass."}))
    from fixtures_manuscript import _create_receipt

    _create_receipt(gate_tree)
    write_variables_manifest(gate_tree, _metrics(gate_tree))
    with pytest.raises(ValueError, match="Hard-coded figure accessibility claims"):
        validate_project(gate_tree)


def test_no_chapters_is_not_success(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="No numbered"):
        validate_project(tmp_path)
