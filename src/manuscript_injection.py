"""Manuscript ``${variable}`` injection (standalone implementation).

Reads the metrics produced by :mod:`src.generate_manuscript_metrics` and
performs ``${variable}`` substitution in every numbered manuscript chapter
under ``docs/manuscript/``, writing rendered copies to ``output/manuscript/``.

Only braced identifier tokens are substituted; mathematical dollar delimiters
and bare dollar-prefixed names are preserved. Unknown tokens reject the entire
hydration before any chapter is written.
"""

from __future__ import annotations

import logging
import re
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

# Match only ``${identifier}`` tokens that ``string.Template.safe_substitute`` would
# substitute — same pattern as ``projects/template/src/template/inject_metrics.py``
# (avoids false positives on LaTeX-like ``${...}`` spans).
_UNRESOLVED_VAR_RE = re.compile(r"\$\{([_a-zA-Z][_a-zA-Z0-9]*)\}")

_CHAPTER_PATTERN = re.compile(r"^\d")


def resolve_manuscript_dir(project_root: Path) -> Path:
    """Return the directory holding the numbered manuscript chapters.

    Mirrors ``infrastructure.core.project_paths.resolve_source_manuscript_dir``
    without importing it, so standalone checkouts resolve identically:
    ``docs/manuscript/`` is canonical, ``manuscript/`` is the legacy fallback
    retained for pre-relocation trees.
    """
    canonical = project_root / "docs" / "manuscript"
    if any(canonical.glob("[0-9]*.md")):
        return canonical
    legacy = project_root / "manuscript"
    if any(legacy.glob("[0-9]*.md")):
        return legacy
    return canonical


def render_all_chapters(
    manuscript_dir: Path, metrics: dict, output_dir: Path
) -> list[Path]:
    """Process all numbered chapter files and copy ancillary files."""
    chapters = sorted(manuscript_dir.glob("[0-9]*.md"))
    if not chapters:
        raise ValueError("No numbered manuscript chapters")
    rendered_chapters = {
        item.name: substitute_variables(item.read_text(encoding="utf-8"), metrics)
        for item in chapters
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for item in sorted(manuscript_dir.iterdir()):
        if item.is_dir():
            continue

        if _CHAPTER_PATTERN.match(item.name) and item.suffix == ".md":
            # Numbered chapter — apply substitution
            rendered = rendered_chapters[item.name]

            dest = output_dir / item.name
            dest.write_text(rendered, encoding="utf-8")
            written.append(dest)

        else:
            # Ancillary file — copy verbatim
            dest = output_dir / item.name
            shutil.copy2(item, dest)
            written.append(dest)

    return written


def substitute_variables(text: str, metrics: dict) -> str:
    """Replace braced identifiers exactly and reject missing or nested tokens."""
    missing = set(_UNRESOLVED_VAR_RE.findall(text)) - set(metrics)
    if missing:
        raise ValueError(f"Unresolved manuscript variables: {sorted(missing)}")
    rendered = _UNRESOLVED_VAR_RE.sub(lambda match: str(metrics[match[1]]), text)
    if _UNRESOLVED_VAR_RE.search(rendered):
        raise ValueError("Injected values contain unresolved manuscript variables")
    return rendered


def count_unresolved_variables(rendered_dir: Path) -> int:
    """Report unresolved ``${identifier}`` tokens in rendered numbered chapters.

    Warns once per affected file (sorted, unique token names) and returns the
    total number of unresolved occurrences across all chapters.
    """
    unresolved_total = 0
    for out_file in sorted(rendered_dir.glob("[0-9]*.md")):
        content = out_file.read_text(encoding="utf-8")
        remaining = _UNRESOLVED_VAR_RE.findall(content)
        if remaining:
            logger.warning(
                f"  {out_file.name}: unresolved: "
                + ", ".join(f"${{{t}}}" for t in sorted(set(remaining)))
            )
            unresolved_total += len(remaining)
    return unresolved_total
