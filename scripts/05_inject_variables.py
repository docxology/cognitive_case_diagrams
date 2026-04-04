#!/usr/bin/env python3
"""Manuscript variable injection script for cognitive_case_diagrams.

Reads ``output/metrics.json`` produced by ``generate_manuscript_metrics.py``
and performs ``${variable}`` substitution in every numbered manuscript chapter,
writing rendered copies to ``output/manuscript/``.

The pipeline hook in ``scripts/03_render_pdf.py`` automatically renders
from ``output/manuscript/`` when that directory contains ``.md`` files.

Usage:
    python scripts/05_inject_variables.py
    python scripts/05_inject_variables.py --dry-run
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

from infrastructure.core.logging.utils import get_logger, log_success
from infrastructure.core.logging.pipeline_logging import log_header
from src.generate_manuscript_metrics import collect_metrics, write_metrics

# Use the template's inject_metrics infrastructure if available,
# otherwise fall back to a local implementation
try:
    from projects.template.src.template.inject_metrics import (
        render_all_chapters,
    )
except ImportError:
    # Fallback: local implementation matching the template pattern
    import re
    import shutil
    from string import Template

    _CHAPTER_PATTERN = re.compile(r"^\d")

    def render_all_chapters(
        manuscript_dir: Path, metrics: dict, output_dir: Path
    ) -> list[Path]:
        """Process all numbered chapter files and copy ancillary files."""
        output_dir.mkdir(parents=True, exist_ok=True)
        written: list[Path] = []

        for item in sorted(manuscript_dir.iterdir()):
            if item.is_dir():
                continue

            if _CHAPTER_PATTERN.match(item.name) and item.suffix == ".md":
                # Numbered chapter — apply substitution
                source_text = item.read_text(encoding="utf-8")
                rendered = Template(source_text).safe_substitute(metrics)

                dest = output_dir / item.name
                dest.write_text(rendered, encoding="utf-8")
                written.append(dest)

                # Warn about unresolved tokens
                remaining = re.findall(r"\$\{([^}]+)\}", rendered)
                if remaining:
                    logger.warning(
                        f"{item.name}: {len(remaining)} unresolved: "
                        + ", ".join(f"${{{t}}}" for t in sorted(set(remaining)))
                    )
            else:
                # Ancillary file — copy verbatim
                dest = output_dir / item.name
                shutil.copy2(item, dest)
                written.append(dest)

        return written


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

    manuscript_dir = _PROJECT_ROOT / "manuscript"
    output_dir = _PROJECT_ROOT / "output"
    rendered_dir = output_dir / "manuscript"
    metrics_path = output_dir / "metrics.json"

    log_header("MANUSCRIPT VARIABLE INJECTION", logger)

    # Step 1: Collect metrics
    logger.info("Collecting metrics from project structure...")
    metrics = collect_metrics(_PROJECT_ROOT)
    logger.info(f"Collected {len(metrics)} variables:")
    for key in sorted(metrics.keys()):
        logger.info(f"  ${{{key}}} = {metrics[key]}")

    # Step 2: Write metrics.json
    write_metrics(metrics, metrics_path)
    logger.info(f"Wrote metrics to {metrics_path}")

    if args.dry_run:
        logger.info("[DRY RUN] Would inject into manuscript files")
        return 0

    # Step 3: Render all chapters with substitution
    logger.info(f"Injecting variables into manuscript → {rendered_dir}")
    written = render_all_chapters(manuscript_dir, metrics, rendered_dir)
    logger.info(f"Wrote {len(written)} files to {rendered_dir}")

    # Step 4: Verify no unresolved ${...} in critical files
    import re

    unresolved_total = 0
    for out_file in sorted(rendered_dir.glob("[0-9]*.md")):
        content = out_file.read_text(encoding="utf-8")
        remaining = re.findall(r"\$\{(\w+)\}", content)
        if remaining:
            logger.warning(
                f"  {out_file.name}: unresolved: "
                + ", ".join(f"${{{t}}}" for t in sorted(set(remaining)))
            )
            unresolved_total += len(remaining)

    if unresolved_total:
        logger.warning(f"{unresolved_total} unresolved variable(s) remain")
    else:
        log_success("All template variables resolved successfully", logger)

    log_success(
        f"Variable injection complete: {len(metrics)} variables across {len(written)} files",
        logger,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
