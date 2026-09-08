"""Contract tests for the extracted figure-registry writer.

Real tmp trees with real PNG bytes (Pillow); no mocks. The byte-compatibility
test embeds the base-commit writer algorithm verbatim as the reference and
requires the extracted module to produce byte-identical output on identical
inputs — the A1-A6 acceptance line for the extraction.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from PIL import Image

from src.visualization.figure_registry import (
    manuscript_figure_labels,
    write_figure_registry,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def make_png(path: Path) -> None:
    Image.new("RGB", (4, 4), color=(200, 100, 50)).save(path)


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    """Minimal authored tree: manuscript, alt texts, and one src byte."""
    root = tmp_path / "proj"
    (root / "docs" / "manuscript").mkdir(parents=True)
    for required in ("src", "scripts", "tests", "docs", "skills"):
        (root / required).mkdir(exist_ok=True)
    (root / "pyproject.toml").write_text('[project]\nname = "fixture"\nversion = "0.0.0"\n', encoding="utf-8")
    (root / "uv.lock").write_text("", encoding="utf-8")
    (root / "src" / "module.py").write_text("value = 1\n", encoding="utf-8")
    (root / "docs" / "manuscript" / "01_chapter.md").write_text(
        "![Case category](output/figures/case_standard.png){#fig:case-standard}\n",
        encoding="utf-8",
    )
    (root / "docs" / "figure_alt_text.json").write_text(
        json.dumps({"case_standard.png": "A case category graph."}), encoding="utf-8"
    )
    return root


def make_figures(root: Path, *names: str) -> list[Path]:
    out = root / "output" / "figures"
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    for name in names:
        p = out / name
        make_png(p)
        paths.append(p)
    return paths


def test_manuscript_label_is_authoritative_over_slug(project: Path) -> None:
    labels = manuscript_figure_labels(project)
    assert labels["case_standard.png"] == "fig:case-standard"


def test_unlabelled_figure_falls_back_to_slug(project: Path) -> None:
    paths = make_figures(project, "case_standard.png", "orphan_bonus.png")
    summary = write_figure_registry(paths, project / "output" / "figures", project)
    registry = {e["filename"]: e for e in json.loads(
        (project / "output" / "figures" / "figure_registry.json").read_text(encoding="utf-8"))}
    assert registry["case_standard.png"]["label"] == "fig:case-standard"
    assert registry["orphan_bonus.png"]["label"] == "fig:orphan-bonus"
    assert summary["unlabelled"] == ["orphan_bonus.png"]


def test_alt_text_binding_and_empty_fallback(project: Path) -> None:
    paths = make_figures(project, "case_standard.png", "orphan_bonus.png")
    write_figure_registry(paths, project / "output" / "figures", project)
    registry = {e["filename"]: e for e in json.loads(
        (project / "output" / "figures" / "figure_registry.json").read_text(encoding="utf-8"))}
    assert registry["case_standard.png"]["alt_text"] == "A case category graph."
    assert registry["orphan_bonus.png"]["alt_text"] == ""


def test_sha256_binds_rendered_bytes(project: Path) -> None:
    (paths,) = [make_figures(project, "case_standard.png")]
    write_figure_registry(paths, project / "output" / "figures", project)
    entry = json.loads((project / "output" / "figures" / "figure_registry.json").read_text())[0]
    assert entry["sha256"] == hashlib.sha256(paths[0].read_bytes()).hexdigest()


def test_non_image_suffix_is_skipped(project: Path) -> None:
    out = project / "output" / "figures"
    out.mkdir(parents=True)
    make_png(out / "kept.png")
    stray = out / "notes.txt"
    stray.write_text("not a figure", encoding="utf-8")
    summary = write_figure_registry([out / "kept.png", stray], out, project)
    assert summary["written"] == 1


def test_merge_preserves_unrelated_entries_and_newer_wins(project: Path) -> None:
    out = project / "output" / "figures"
    paths = make_figures(project, "case_standard.png")
    write_figure_registry(paths, out, project)
    # A prior registry entry from another domain must survive a partial run.
    dest = out / "figure_registry.json"
    prior = json.loads(dest.read_text(encoding="utf-8"))
    prior.append({
        "filename": "from_other_domain.png", "path": "output/figures/from_other_domain.png",
        "label": "fig:from-other-domain", "alt_text": "", "generated_by": "scripts/generate_diagrams.py",
        "generator_input_fingerprint": prior[0]["generator_input_fingerprint"],
        "sha256": "0" * 64, "provenance": "prior",
    })
    dest.write_text(json.dumps(prior, indent=2) + "\n", encoding="utf-8")
    # Re-render the same figure with changed bytes: newer wins the clash.
    make_png(paths[0])
    write_figure_registry(paths, out, project)
    merged = {e["filename"]: e for e in json.loads(dest.read_text(encoding="utf-8"))}
    assert set(merged) == {"case_standard.png", "from_other_domain.png"}
    assert merged["case_standard.png"]["sha256"] == hashlib.sha256(paths[0].read_bytes()).hexdigest()
    assert merged["from_other_domain.png"]["provenance"] == "prior"


def test_ordering_and_deterministic_bytes(project: Path) -> None:
    out = project / "output" / "figures"
    paths = make_figures(project, "zulu.png", "alpha.png", "mike.png")
    first = write_figure_registry(paths, out, project)
    first_bytes = first["path"].read_bytes()
    second = write_figure_registry(paths, out, project)
    assert second["path"].read_bytes() == first_bytes
    entries = json.loads(first_bytes.decode("utf-8"))
    assert [e["filename"] for e in entries] == sorted(e["filename"] for e in entries)
    assert first_bytes.endswith(b"\n")


def test_stale_generation_fingerprint_is_rejected(project: Path) -> None:
    paths = make_figures(project, "case_standard.png")
    stale = "0" * 64
    with pytest.raises(ValueError, match="changed during the run"):
        write_figure_registry(paths, project / "output" / "figures", project,
                              expected_fingerprint=stale)


def test_corrupt_registry_fail_closed_and_diagnostic_rebuild(project: Path) -> None:
    out = project / "output" / "figures"
    paths = make_figures(project, "case_standard.png")
    write_figure_registry(paths, out, project)
    dest = out / "figure_registry.json"
    dest.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="unreadable"):
        write_figure_registry(paths, out, project)
    summary = write_figure_registry(paths, out, project, allow_rebuild=True)
    assert summary["merged"] == 1
    json.loads(dest.read_text(encoding="utf-8"))


def test_atomic_write_refuses_linked_destination(project: Path) -> None:
    out = project / "output" / "figures"
    paths = make_figures(project, "case_standard.png")
    write_figure_registry(paths, out, project)
    dest = out / "figure_registry.json"
    dest.unlink()
    link_target = project / "elsewhere.json"
    link_target.write_text("{}", encoding="utf-8")
    dest.symlink_to(link_target)
    with pytest.raises(ValueError, match="linked registry destination"):
        write_figure_registry(paths, out, project)


def test_byte_compatibility_with_base_writer(project: Path) -> None:
    """The extracted module must emit the base-commit writer's exact bytes."""
    import re

    out = project / "output" / "figures"
    paths = make_figures(project, "case_standard.png", "extra_plate.png")
    write_figure_registry(paths, out, project)
    produced = (out / "figure_registry.json").read_text(encoding="utf-8")

    # --- reference implementation: base 9382dde scripts/generate_diagrams.py:251-336, verbatim ---
    _FIGURE_LABEL_RE = re.compile(
        r"\]\((?:[^)]*/)?(?P<filename>[\w.-]+\.(?:png|pdf|svg))\)\{#(?P<label>fig:[\w:.-]+)\}"
    )

    def _manuscript_figure_labels(project_root: Path) -> dict[str, str]:
        manuscript_dir = project_root / "docs" / "manuscript"
        if not manuscript_dir.is_dir():
            manuscript_dir = project_root / "manuscript"
        labels: dict[str, str] = {}
        for md in sorted(manuscript_dir.glob("*.md")):
            for m in _FIGURE_LABEL_RE.finditer(md.read_text(encoding="utf-8")):
                labels[m.group("filename")] = m.group("label")
        return labels

    def reference_bytes(paths: list[Path], out_dir: Path) -> bytes:
        import hashlib as hl

        project_root = project
        manuscript_labels = _manuscript_figure_labels(project_root)
        alt_texts = json.loads((project_root / "docs" / "figure_alt_text.json").read_text())
        from src.release_validation import quality_input_fingerprint

        generation_inputs = quality_input_fingerprint(project_root)["sha256"]
        seen: set[str] = set()
        registry: list[dict] = []
        for p in paths:
            if p.suffix not in {".png", ".pdf", ".svg"}:
                continue
            if p.name in seen:
                continue
            seen.add(p.name)
            label = manuscript_labels.get(p.name)
            if label is None:
                label = f"fig:{p.stem.replace('_', '-')}"
            try:
                rel = p.resolve().relative_to(project_root)
            except ValueError:
                rel = p
            registry.append({
                "filename": p.name,
                "path": str(rel),
                "label": label,
                "alt_text": alt_texts.get(p.name, ""),
                "generated_by": "scripts/generate_diagrams.py",
                "generator_input_fingerprint": generation_inputs,
                "sha256": hl.sha256(p.read_bytes()).hexdigest(),
                "provenance": "synthetic input or explicitly constructed diagram; see source and manuscript caption",
            })
        dest = out_dir / "figure_registry.json"
        existing: dict[str, dict] = {}
        if dest.exists():
            for entry in json.loads(dest.read_text(encoding="utf-8")):
                existing[entry.get("filename")] = entry
        merged = {**existing, **{e["filename"]: e for e in registry}}
        merged_list = sorted(merged.values(), key=lambda e: e["filename"])
        return (json.dumps(merged_list, indent=2) + "\n").encode("utf-8")

    assert produced.encode("utf-8") == reference_bytes(paths, out)


def test_output_directory_symlink_escape_is_refused(project: Path, tmp_path: Path) -> None:
    """A symlinked out_dir whose target leaves the project output tree is refused."""
    paths = make_figures(project, "case_standard.png")
    outside = tmp_path / "outside-esc"
    outside.mkdir()
    out_link = project / "output" / "linked"
    out_link.symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="escapes the project output tree"):
        write_figure_registry(paths, out_link, project)
    # Nothing may be written outside: the seeded directory stays byte-empty.
    assert list(outside.iterdir()) == []


def test_mount_alias_ancestor_above_out_dir_is_allowed(project: Path, tmp_path: Path) -> None:
    """A symlinked ancestor ABOVE out_dir that resolves inside output is fine."""
    alias = tmp_path / "alias-in"
    alias.symlink_to(project / "output", target_is_directory=True)
    out_dir = alias / "figures-alias"
    paths = make_figures(project, "case_standard.png")
    summary = write_figure_registry(paths, out_dir, project)
    assert summary["merged"] == 1
    landed = project / "output" / "figures-alias" / "figure_registry.json"
    assert json.loads(landed.read_text(encoding="utf-8"))[0]["filename"] == "case_standard.png"
