"""Figure registry writer: the canonical manifest behind PDF/HTML rendering.

Extracted verbatim from ``scripts/generate_diagrams.py`` (wave: figure-registry
extraction) so release-critical registry logic lives under ``src/`` coverage.
The registry is consumed by ``src.project_validation`` (fingerprint, path,
alt-text, and per-figure hash checks) and by the PDF rendering pipeline.

Contract preserved from the script-era writer:
- entries carry exactly ``filename, path, label, alt_text, generated_by,
  generator_input_fingerprint, sha256, provenance`` in that key order,
- the list is sorted by ``filename`` and serialized as
  ``json.dumps(entries, indent=2) + "\\n"`` — byte-stable so downstream
  byte-compatibility comparisons stay meaningful,
- merge semantics: existing entries are preserved, a newly rendered figure
  wins its filename clash, an unreadable existing registry is rebuilt only
  when the caller explicitly allows it (diagnostic runs),
- labels are the manuscript's own ``{#fig:...}`` assignments; unlabelled
  figures keep a derived slug and are reported, never silently dropped,
- ``generator_input_fingerprint`` is ``quality_input_fingerprint``'s combined
  digest, bound at write time and re-verified after the manifest is built so
  a mid-run source edit fails the run instead of shipping stale bindings.

Atomicity note: ``src.release_validation.write_json_atomic`` serializes with
``sort_keys=True``, which would reorder entry keys and break the byte-format
contract above. This module therefore performs the same crash-safe
temporary-file + fsync + replace sequence while emitting the exact legacy
bytes.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import tempfile
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

FIGURE_LABEL_RE = re.compile(
    r"\]\((?:[^)]*/)?(?P<filename>[\w.-]+\.(?:png|pdf|svg))\)\{#(?P<label>fig:[\w:.-]+)\}"
)

REGISTRY_FILENAME = "figure_registry.json"
_IMAGE_SUFFIXES = frozenset({".png", ".pdf", ".svg"})
_ENTRY_KEYS = (
    "filename",
    "path",
    "label",
    "alt_text",
    "generated_by",
    "generator_input_fingerprint",
    "sha256",
    "provenance",
)


def manuscript_figure_labels(project_root: Path) -> dict[str, str]:
    """Map figure filename -> the Pandoc label the manuscript assigns it.

    The manuscript is the authority for its own cross-reference labels.
    Deriving them from filenames instead (``fig:`` + stem.replace('_','-'))
    produced ``fig:case-category-standard`` where the manuscript writes
    ``fig:case-standard``, so 20 of 30 labels failed the shared publication
    gate's "Unregistered figure reference" check.
    """
    manuscript_dir = project_root / "docs" / "manuscript"
    if not manuscript_dir.is_dir():
        manuscript_dir = project_root / "manuscript"
    labels: dict[str, str] = {}
    for md in sorted(manuscript_dir.glob("*.md")):
        for m in FIGURE_LABEL_RE.finditer(md.read_text(encoding="utf-8")):
            labels[m.group("filename")] = m.group("label")
    return labels


def _load_existing(dest: Path, *, allow_rebuild: bool) -> dict[str, dict]:
    """Return the existing registry keyed by filename, honouring A6 policy."""
    if not dest.exists():
        return {}
    try:
        loaded = json.loads(dest.read_text(encoding="utf-8"))
        existing: dict[str, dict] = {}
        for entry in loaded:
            filename = entry.get("filename")
            if isinstance(filename, str):
                existing[filename] = entry
        return existing
    except (json.JSONDecodeError, AttributeError, TypeError):
        if not allow_rebuild:
            raise ValueError(
                f"Existing figure registry is unreadable: {dest}; "
                "rebuilding requires the diagnostic (skip-failed) mode"
            ) from None
        logger.warning("Existing figure registry unreadable — rebuilding it.")
        return {}


def _fingerprint(project_root: Path) -> str:
    from src.release_validation import quality_input_fingerprint

    return quality_input_fingerprint(project_root)["sha256"]


def _registry_bytes(entries: list[dict]) -> bytes:
    return (json.dumps(entries, indent=2) + "\n").encode("utf-8")


def write_figure_registry(
    paths: list[Path],
    out_dir: Path,
    project_root: Path,
    *,
    expected_fingerprint: str | None = None,
    allow_rebuild: bool = False,
) -> dict[str, Any]:
    """Write ``figure_registry.json`` for the rendered figures and return a summary.

    ``paths`` are the figures produced by the current run (any suffix; non-image
    members are skipped). Existing registry entries are preserved and merged
    with the new ones (newer wins). ``expected_fingerprint`` is the quality
    input fingerprint captured before figure generation; when provided and the
    live fingerprint disagrees — before or after the manifest is built — the
    run fails rather than shipping a stale binding. ``allow_rebuild`` permits
    rebuilding an unreadable existing registry (diagnostic mode only).
    """
    dest = out_dir / REGISTRY_FILENAME
    # CONFINEMENT: the registry must land inside the project's output tree.
    # Both sides are resolved so host mount aliases (/tmp -> /private/tmp)
    # compare consistently; a symlinked out_dir whose target leaves the
    # project output subtree is refused here rather than resolved away.
    output_root = (project_root / "output").resolve()
    resolved_out_dir = out_dir.resolve()
    if resolved_out_dir != output_root and output_root not in resolved_out_dir.parents:
        raise ValueError(
            f"Registry output directory escapes the project output tree: {out_dir}"
        )
    # WITHIN-SUBTREE REFUSALS: the destination itself or any intermediate
    # between out_dir and dest must not be a symlink.
    guarded = [dest, *reversed(dest.parents)]
    stop = out_dir.resolve()
    if any(
        candidate.is_symlink()
        for candidate in guarded
        if candidate == stop or stop in candidate.parents or candidate == dest
    ):
        raise ValueError(f"Refusing to replace a linked registry destination: {dest}")

    fingerprint = _fingerprint(project_root)
    if expected_fingerprint is not None and expected_fingerprint != fingerprint:
        raise ValueError(
            "Figure generation inputs changed during the run "
            f"(before {expected_fingerprint[:12]}, after {fingerprint[:12]})"
        )

    manuscript_labels = manuscript_figure_labels(project_root)
    alt_texts = json.loads((project_root / "docs" / "figure_alt_text.json").read_text(encoding="utf-8"))

    existing = _load_existing(dest, allow_rebuild=allow_rebuild)
    seen: set[str] = set()
    registry: list[dict] = []
    unlabelled: list[str] = []
    for p in paths:
        if p.suffix not in _IMAGE_SUFFIXES:
            continue
        if p.name in seen:
            continue
        seen.add(p.name)
        label = manuscript_labels.get(p.name)
        if label is None:
            # Not referenced by the manuscript — keep the derived slug so the
            # entry still round-trips, and say so rather than failing silently.
            label = f"fig:{p.stem.replace('_', '-')}"
            unlabelled.append(p.name)
        try:
            rel = p.resolve().relative_to(project_root)
        except ValueError:
            rel = p
        entry = {
            "filename": p.name,
            # Project-relative: absolute paths embedded the author's home
            # directory in a repo that ships to GitHub and Zenodo.
            "path": str(rel),
            "label": label,
            "alt_text": alt_texts.get(p.name, ""),
            "generated_by": "scripts/generate_diagrams.py",
            "generator_input_fingerprint": fingerprint,
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            "provenance": "synthetic input or explicitly constructed diagram; see source and manuscript caption",
        }
        assert tuple(entry) == _ENTRY_KEYS, "registry entry key order is a byte contract"
        registry.append(entry)

    merged = {**existing, **{e["filename"]: e for e in registry}}
    merged_list = sorted(merged.values(), key=lambda e: e["filename"])

    # Post-build re-verification: a source edit that landed while the manifest
    # was being assembled must fail the run, not ship a stale binding.
    post = _fingerprint(project_root)
    if post != fingerprint:
        raise ValueError(
            "Figure generation inputs changed during the run "
            f"({fingerprint[:12]} -> {post[:12]}); registry not written"
        )

    payload = _registry_bytes(merged_list)
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="wb", dir=out_dir, delete=False
    ) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        except BaseException:
            temporary.unlink()
            raise
    try:
        temporary.chmod(0o644)  # These are public project evidence artifacts.
        temporary.replace(dest)
    finally:
        temporary.unlink(missing_ok=True)

    logger.info("Wrote figure registry: %s (%d entries)", dest, len(merged_list))
    if unlabelled:
        logger.warning(
            "%d figure(s) carry no manuscript label (supplementary or orphaned): %s",
            len(unlabelled), ", ".join(sorted(unlabelled)),
        )
    return {
        "written": len(registry),
        "merged": len(merged_list),
        "unlabelled": sorted(unlabelled),
        "fingerprint": fingerprint,
        "path": dest,
    }
