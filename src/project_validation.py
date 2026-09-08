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

FIGURE = re.compile(r'!\[([^\n]*)\]\(([^)]+)\)\{#(fig:[\w:.-]+)\}')
LABEL = re.compile(r'\{#([\w:.-]+)\}')
REFERENCE = re.compile(r'(?<![\w@])@([\w][\w:.-]*)')
TOKEN = re.compile(r'\$\{[A-Za-z_]\w*\}')
BIB_KEY = re.compile(r'^@(?!comment\b|preamble\b|string\b)\w+\s*\{\s*([^,\s]+)\s*,', re.M | re.I)


def validate_project(root: Path) -> dict:
    """Raise ValueError on missing, stale, malformed, or unresolved artifacts."""
    source = root / 'docs/manuscript'
    chapters = sorted(source.glob('[0-9]*.md'))
    if not chapters:
        raise ValueError('No numbered manuscript chapters')
    sources = {p.name: p.read_text(encoding='utf-8') for p in chapters}
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
    if len(labels) != len(set(labels)):
        raise ValueError('Duplicate manuscript labels')
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
