#!/usr/bin/env python3
"""Manuscript variable injection script for cognitive_case_diagrams.

Reads ``output/metrics.json`` produced by ``generate_manuscript_metrics.py``
and performs ``${variable}`` substitution in every numbered manuscript chapter
under ``docs/manuscript/``, writing rendered copies to ``output/manuscript/``.

The monorepo render stage (``scripts/pipeline/stage_03_render.py`` at the
template root) automatically renders from ``output/manuscript/`` when that
directory contains ``.md`` files.

Thin orchestrator: substitution logic lives in
``src/manuscript_injection.py`` (standalone fallback) or the template
monorepo's ``projects.template.src.template.inject_metrics`` (used
automatically when the monorepo is available).

Usage:
    python scripts/inject_variables.py
    python scripts/inject_variables.py --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Resolve project paths
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
_REPO_ROOT = _PROJECT_ROOT.parent.parent

# Add paths for imports
sys.path.insert(0, str(_REPO_ROOT))
sys.path.insert(0, str(_PROJECT_ROOT))

# The template monorepo's ``infrastructure`` package is only importable when this
# project is reached through the monorepo checkout. Standalone runs fall back to
# stdlib logging — same pattern as ``scripts/generate_diagrams.py``.
try:
    from infrastructure.core.logging.utils import get_logger, log_success
    from infrastructure.core.logging.pipeline_logging import log_header
except ImportError:  # pragma: no cover - exercised only outside the monorepo
    import logging

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)

    def log_success(message: str, lg: "logging.Logger") -> None:
        lg.info(f"✅ {message}")

    def log_header(title: str, lg: "logging.Logger") -> None:
        lg.info(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


from src.generate_manuscript_metrics import collect_metrics, write_metrics
from src.manuscript_injection import (
    count_unresolved_variables,
    resolve_manuscript_dir,
)

# Prefer the template monorepo's inject_metrics infrastructure when available;
# standalone checkouts delegate to the equivalent src/ implementation.
try:
    from projects.template.src.template.inject_metrics import (
        render_all_chapters,
    )
except ImportError:
    from src.manuscript_injection import render_all_chapters


logger = get_logger(__name__)


def main() -> int:
    """Execute manuscript variable injection."""
    parser = argparse.ArgumentParser(
        description="Inject pipeline metrics into manuscript templates"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show metrics but don't write files",
    )
    args = parser.parse_args()

    manuscript_dir = resolve_manuscript_dir(_PROJECT_ROOT)
    output_dir = _PROJECT_ROOT / "output"
    rendered_dir = output_dir / "manuscript"
    metrics_path = output_dir / "metrics.json"

    log_header("MANUSCRIPT VARIABLE INJECTION", logger)

    chapters = sorted(manuscript_dir.glob("[0-9]*.md"))
    if not chapters:
        logger.error(
            f"No numbered manuscript chapters under {manuscript_dir} — "
            "refusing to render an empty manuscript."
        )
        return 1
    logger.info(f"Manuscript source: {manuscript_dir} ({len(chapters)} chapters)")

    # Step 1: Collect metrics
    logger.info("Collecting metrics from project structure...")
    metrics = collect_metrics(_PROJECT_ROOT)
    logger.info(f"Collected {len(metrics)} variables:")
    for key in sorted(metrics.keys()):
        logger.info(f"  ${{{key}}} = {metrics[key]}")

    if args.dry_run:
        logger.info(
            f"[DRY RUN] Would write {metrics_path} and inject into "
            f"{len(chapters)} chapters under {manuscript_dir}"
        )
        return 0

    # Step 2: Write metrics.json
    write_metrics(metrics, metrics_path)
    logger.info(f"Wrote metrics to {metrics_path}")

    # Step 3: Render all chapters with substitution
    logger.info(f"Injecting variables into manuscript → {rendered_dir}")
    written = render_all_chapters(manuscript_dir, metrics, rendered_dir)
    logger.info(f"Wrote {len(written)} files to {rendered_dir}")

    # Step 4: Verify no unresolved ${...} in critical files
    rendered_chapters = sorted(rendered_dir.glob("[0-9]*.md"))
    if len(rendered_chapters) != len(chapters):
        logger.error(
            f"Rendered {len(rendered_chapters)} chapters into {rendered_dir} but "
            f"{len(chapters)} were expected from {manuscript_dir} — refusing to "
            "report success on a partial render."
        )
        return 1

    unresolved_total = count_unresolved_variables(rendered_dir)
    if unresolved_total:
        logger.error(f"{unresolved_total} unresolved variable(s) remain — pipeline cannot proceed")
        return 1
    else:
        log_success("All template variables resolved successfully", logger)

    log_success(
        f"Variable injection complete: {len(metrics)} variables across {len(written)} files",
        logger,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
