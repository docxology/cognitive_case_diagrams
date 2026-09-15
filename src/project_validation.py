"""Fail-closed cross-artifact checks for the authored and hydrated manuscript.

Checks declared links and provenance, not linguistic validity or visual quality.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from PIL import Image
from src.manuscript_variables import scan_hard_coded_claims, validate_metrics, validate_variables_manifest
from src.release_validation import StaleEvidenceError, quality_input_fingerprint
from src.visualization.figure_registry import environment_fingerprint

FIGURE = re.compile(r'!\[([^\n]*)\]\(([^)]+)\)\{#(fig:[\w:.-]+)\}')
LABEL = re.compile(r'\{#([\w:.-]+)\}')
REFERENCE = re.compile(r'(?<![\w@])@([\w][\w:.-]*)')
TOKEN = re.compile(r'\$\{[A-Za-z_]\w*\}')
BIB_KEY = re.compile(r'^@(?!comment\b|preamble\b|string\b)\w+\s*\{\s*([^,\s]+)\s*,', re.M | re.I)

MATH_SPAN = re.compile(r'(?<!\\)\$([^$]+)(?<!\\)\$')
UNESCAPED_PIPE = re.compile(r'(?<!\\)\|')
EQ_NUMBERED = re.compile(r'eq:eq-(\w+)-(\d+)')


def _table_cells(row: str) -> list[str]:
    """Split a stripped pipe-table row on unescaped '|' boundary pipes."""
    inner = row[1:]
    if inner.endswith('|'):
        inner = inner[:-1]
    return re.split(r'(?<!\\)\|', inner)


def lint_markdown_tables(name: str, text: str) -> list[str]:
    """Return ``name:line`` findings for malformed pipe tables in *text*.

    Pure string scanning: every pipe-table row must carry the same cell
    count as its header row, and inline math (``$...$``) inside a row must
    escape any literal ``|`` — an unescaped one silently splits the cell
    (e.g. ``| $|Z|$ | x |`` parses four cells against a three-cell header).
    Fenced code blocks are skipped.
    """
    findings: list[str] = []
    in_fence = False
    header_cells: int | None = None
    header_line = 0
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith('```'):
            in_fence = not in_fence
            header_cells = None
            continue
        if in_fence:
            continue
        stripped = line.strip()
        if not stripped.startswith('|'):
            header_cells = None
            continue
        for span in MATH_SPAN.findall(stripped):
            if UNESCAPED_PIPE.search(span):
                findings.append(
                    f'{name}:{lineno}: unescaped \'|\' inside inline math in a table row'
                )
        cell_count = len(_table_cells(stripped))
        if header_cells is None:
            header_cells = cell_count
            header_line = lineno
        elif cell_count != header_cells:
            findings.append(
                f'{name}:{lineno}: table row has {cell_count} cells but header row '
                f'(line {header_line}) has {header_cells}'
            )
    return findings


def _lint_manuscript_tables(root: Path, sources: dict[str, str]) -> None:
    """Raise when authored chapters or the README carry malformed pipe tables."""
    findings: list[str] = []
    for name, text in sources.items():
        findings.extend(lint_markdown_tables(f'docs/manuscript/{name}', text))
    readme = root / 'README.md'
    if readme.is_file():
        findings.extend(lint_markdown_tables('README.md', readme.read_text(encoding='utf-8')))
    if findings:
        raise ValueError('Malformed markdown table: ' + '; '.join(findings))


def lint_manuscript_equation_labels(sources: dict[str, str]) -> list[str]:
    """Return ``name:line`` findings for non-consecutive numbered eq labels.

    Numbered labels (``eq:eq-<chapter>-<k>``) must form a gap-free sequence
    starting at 1 within each file for their chapter prefix; named labels
    are exempt here (they are still covered by the duplicate-label check).
    """
    numbered: dict[tuple[str, str], list[tuple[int, int]]] = {}
    for name, text in sources.items():
        for lineno, line in enumerate(text.splitlines(), start=1):
            for label in LABEL.findall(line):
                match = EQ_NUMBERED.fullmatch(label)
                if match:
                    numbered.setdefault((name, match[1]), []).append((int(match[2]), lineno))
    findings: list[str] = []
    for (name, prefix), entries in sorted(numbered.items()):
        ordered = sorted(entries)
        expected = list(range(1, len(ordered) + 1))
        if [number for number, _ in ordered] == expected:
            continue
        bad_line = next(
            lineno for (number, lineno), want in zip(ordered, expected) if number != want
        )
        findings.append(
            f'{name}:{bad_line}: chapter {prefix} equation numbers are not a '
            f'gap-free sequence starting at 1: found {[n for n, _ in ordered]}'
        )
    return findings


def validate_project(root: Path) -> dict:
    """Raise ValueError on missing, stale, malformed, or unresolved artifacts."""
    source = root / 'docs/manuscript'
    chapters = sorted(source.glob('[0-9]*.md'))
    if not chapters:
        raise ValueError('No numbered manuscript chapters')
    sources = {p.name: p.read_text(encoding='utf-8') for p in chapters}
    _lint_manuscript_tables(root, sources)
    metrics = json.loads((root / 'output/metrics.json').read_text())
    validate_metrics(metrics)
    findings = scan_hard_coded_claims(sources)
    if findings:
        raise ValueError('Hard-coded manuscript claims: ' + '; '.join(findings))
    validate_variables_manifest(root, metrics)
    figure_inputs = quality_input_fingerprint(root)['sha256']
    hydrated = root / 'output/manuscript'
    if {p.name for p in hydrated.glob('[0-9]*.md')} != set(sources):
        raise ValueError('Hydrated chapter set differs from source')
    for name, text in sources.items():
        expected = TOKEN.sub(lambda m: str(metrics.get(m[0][2:-1], m[0])), text)
        if TOKEN.search(expected):
            raise ValueError(f'Unresolved manuscript token in {name}')
        if (hydrated / name).read_text(encoding='utf-8') != expected:
            raise StaleEvidenceError(f'Stale hydrated chapter: {name}')
    text = '\n'.join(sources.values())
    labels = LABEL.findall(text)
    seen: dict[str, tuple[str, int]] = {}
    duplicates: list[str] = []
    for name, chapter in sources.items():
        for lineno, line in enumerate(chapter.splitlines(), start=1):
            for label in LABEL.findall(line):
                first = seen.setdefault(label, (name, lineno))
                if first != (name, lineno):
                    duplicates.append(
                        f'{name}:{lineno} repeats {label} (first defined at {first[0]}:{first[1]})'
                    )
    if duplicates:
        raise ValueError('Duplicate manuscript labels: ' + '; '.join(duplicates))
    eq_findings = lint_manuscript_equation_labels(sources)
    if eq_findings:
        raise ValueError('Non-consecutive manuscript equation labels: ' + '; '.join(eq_findings))
    bib = BIB_KEY.findall((source / 'references.bib').read_text(encoding='utf-8'))
    if len(bib) != len(set(bib)):
        raise ValueError('Duplicate bibliography keys')
    # Ignore fenced source examples before looking for prose references.
    prose = re.sub(r'```.*?```', '', text, flags=re.S)
    unknown = set(REFERENCE.findall(prose)) - set(labels) - set(bib)
    if unknown:
        raise ValueError(f'Unresolved citations or cross-references: {sorted(unknown)}')
    alt_texts = json.loads((root / 'docs/figure_alt_text.json').read_text())
    alt_findings = scan_hard_coded_claims(alt_texts)
    if alt_findings:
        raise ValueError('Hard-coded figure accessibility claims: ' + '; '.join(alt_findings))
    entries = json.loads((root / 'output/figures/figure_registry.json').read_text())
    registry = {entry['filename']: entry for entry in entries}
    if len(registry) != len(entries):
        raise ValueError('Duplicate figure registry filenames')
    figures = FIGURE.findall(text)
    if not figures:
        raise ValueError('Manuscript contains no labelled figures')
    referenced = set()
    for caption, relative, label in figures:
        if not caption.strip():
            raise ValueError(f'Empty figure caption: {label}')
        image = root / relative
        if not image.resolve().is_relative_to(root.resolve()):
            raise ValueError(f'Figure escapes project: {relative}')
        if not image.is_file():
            raise ValueError(f'Missing figure: {relative}')
        entry = registry.get(image.name)
        if entry is None or entry.get('label') != label:
            raise ValueError(f'Figure registry label mismatch: {label}')
        if entry.get('generator_input_fingerprint') != figure_inputs:
            raise StaleEvidenceError(f'Stale figure generation inputs: {relative}')
        if 'environment_fingerprint' not in entry:
            raise StaleEvidenceError(f'Missing figure generation environment fingerprint: {relative}')
        if entry['environment_fingerprint'] != environment_fingerprint():
            raise StaleEvidenceError(f'Stale figure generation environment: {relative}')
        if Path(entry.get('path', '')).is_absolute() or (root / entry.get('path', '')).resolve() != image.resolve():
            raise ValueError(f'Figure registry path mismatch: {relative}')
        alt = entry.get('alt_text')
        if not isinstance(alt, str) or not alt.strip():
            raise ValueError(f'Missing accessibility text: {relative}')
        if alt != alt_texts.get(image.name):
            raise StaleEvidenceError(f'Stale accessibility text: {relative}')
        digest = hashlib.sha256(image.read_bytes()).hexdigest()
        if entry.get('sha256') != digest:
            raise ValueError(f'Figure checksum mismatch: {relative}')
        with Image.open(image) as png:
            png.verify()
        referenced.add(image.name)
    if referenced != set(registry):
        raise ValueError(f'Unreferenced registry entries: {sorted(set(registry) - referenced)}')
    if int(metrics['total_figures']) != len(referenced):
        raise ValueError('Figure count differs from metrics')
    for auxiliary in ('references.bib', 'config.yaml', 'preamble.md'):
        if (source / auxiliary).read_bytes() != (hydrated / auxiliary).read_bytes():
            raise StaleEvidenceError(f'Stale hydrated auxiliary: {auxiliary}')
    return {'chapters': len(chapters), 'figures': len(referenced),
            'bibliography_entries': len(bib), 'labels': len(labels),
            'status': 'structural checks passed; visual review remains separate'}
