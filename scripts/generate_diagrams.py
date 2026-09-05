#!/usr/bin/env python3
"""Generate all canonical figures for the cognitive_case_diagrams project.

This is the thin orchestrator: it delegates to per-domain sub-scripts or can
be directed at a single domain via ``--domain``.

Domain sub-scripts (also callable independently):
    scripts/generate_category_figures.py   — case categories, alignment, functor
    scripts/generate_discopy_figures.py    — DisCoPy diagrams + complexity
    scripts/generate_cognitive_figures.py  — DAIF, active inference, Fluid-S
    scripts/generate_quantum_figures.py    — quantum POVM, cognitive security
    scripts/generate_syntactic_figures.py  — syntactic case panel
    scripts/generate_category_unpacking_figures.py — pedagogical unpacking panels

Canonical Outputs (30 PNGs total, plus enriched_magnitude.txt):
    Category domain (5):
        case_category_standard.png, case_category_minimal.png,
        composition_triangle.png, alignment_comparison.png, functor_alignment.png
    DisCoPy domain (10):
        discopy_transitive.png, discopy_composition.png, discopy_snake.png,
        discopy_passive.png, discopy_sentence_progression.png,
        discopy_multilingual.png, discopy_ditransitive.png,
        discopy_discocirc_discourse.png, discopy_three_sentence_discourse.png,
        complexity_comparison.png
    String/enriched domain (3):
        string_diagram_discocat.png, discourse_string_diagram.png,
        enriched_hom_matrix.png
    Cognitive/DAIF domain (5):
        active_inference_belief.png, fluid_s_volition_landscape.png,
        daif_belief_trajectory.png, daif_free_energy_convergence.png,
        daif_erp_predictions.png
    Quantum/security domain (3):
        quantum_povm_probabilities.png, security_type_violations.png,
        monoidal_functor_security.png
    Syntactic domain (1):
        syntactic_case_panel.png
    Unpacking domain (3):
        pregroup_reduction_unpacking.png, discocirc_entity_persistence.png,
        snake_equation_unpacking.png

Usage::

    # All domains:
    python scripts/generate_diagrams.py

    # Single domain (use full name or alias):
    python scripts/generate_diagrams.py --domain daif       # alias for cognitive
    python scripts/generate_diagrams.py --domain cognitive
    python scripts/generate_diagrams.py --domain category
    python scripts/generate_diagrams.py --domain discopy
    python scripts/generate_diagrams.py --domain quantum
    python scripts/generate_diagrams.py --domain syntactic
    python scripts/generate_diagrams.py --domain strings    # enriched/string figures
    python scripts/generate_diagrams.py --domain enriched   # alias for strings

    # List available domains:
    python scripts/generate_diagrams.py --list
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path

import matplotlib
if not matplotlib.is_interactive():
    matplotlib.use("Agg")

# Graceful infrastructure import
try:
    from infrastructure.core.logging.utils import get_logger as _get_logger
    logger = _get_logger("generate_diagrams")
    _INFRASTRUCTURE_AVAILABLE = True
except Exception:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger = logging.getLogger("generate_diagrams")
    _INFRASTRUCTURE_AVAILABLE = False

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output" / "figures"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Ensure sub-scripts are importable when invoked from repo root
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


# ── Domain registry ────────────────────────────────────────────────────────

DOMAINS: dict[str, str] = {
    "category": "generate_category_figures",
    "discopy":  "generate_discopy_figures",
    "cognitive": "generate_cognitive_figures",
    "quantum":  "generate_quantum_figures",
    "syntactic": "generate_syntactic_figures",
    "unpacking": "generate_category_unpacking_figures",
    "strings":  "",  # inline handler: _generate_string_enriched()
}

_DOMAIN_ALIASES: dict[str, str] = {
    "daif":     "cognitive",
    "enriched": "strings",
}


# Per-figure failures from the inline "strings" domain, read by run_domain().
# Mirrors the LAST_FAILURES convention the per-domain sub-scripts use, so this
# handler cannot silently drop figures while reporting success either.
STRINGS_LAST_FAILURES: list[str] = []


def _generate_string_enriched(out: Path) -> list[Path]:
    """Generate string diagram and enriched category figures (inline)."""
    STRINGS_LAST_FAILURES.clear()
    from src.diagrams.string_diagram import Sentence
    from src.enriched_cat.enriched import standard_enriched_category
    from src.visualization.string_diagrams import (
        render_discocat_sentence,
        render_discocirc_discourse,
    )
    from src.visualization.enriched_diagrams import render_enriched_heatmap

    out.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    try:
        sent = Sentence.transitive("Alice", "chases", "Bob")
        path = out / "string_diagram_discocat.png"
        render_discocat_sentence(sent, output_path=path)
        outputs.append(path)
        logger.info("  ✓ string_diagram_discocat.png")
    except Exception as exc:
        logger.error("  ✗ string_diagram_discocat.png: %s", exc)
        STRINGS_LAST_FAILURES.append("string_diagram_discocat.png")

    try:
        path = out / "discourse_string_diagram.png"
        render_discocirc_discourse(output_path=path)
        outputs.append(path)
        logger.info("  ✓ discourse_string_diagram.png")
    except Exception as exc:
        logger.error("  ✗ discourse_string_diagram.png: %s", exc)
        STRINGS_LAST_FAILURES.append("discourse_string_diagram.png")

    try:
        cat = standard_enriched_category()
        path = out / "enriched_hom_matrix.png"
        render_enriched_heatmap(cat, output_path=path)
        outputs.append(path)
        # Also write magnitude text file
        mag = cat.magnitude()
        w = cat.weighting()
        txt_path = out / "enriched_magnitude.txt"
        txt_path.write_text(
            f"Enriched Category: {cat.name}\n"
            f"Number of objects: {len(cat.roles)}\n"
            f"Categorical magnitude: {mag:.6f}\n"
            f"Weighting vector: {w.tolist()}\n"
        )
        outputs.append(txt_path)
        logger.info("  ✓ enriched_hom_matrix.png + enriched_magnitude.txt")
    except Exception as exc:
        logger.error("  ✗ enriched figures: %s", exc)
        STRINGS_LAST_FAILURES.append("enriched_hom_matrix.png + enriched_magnitude.txt")

    return outputs


# ── Main dispatcher ─────────────────────────────────────────────────────────

def run_domain(domain: str, out: Path) -> tuple[list[Path], list[str]]:
    """Run a single named domain's figure generation.

    Accepts canonical domain keys *or* their short aliases (e.g. ``"daif"``
    for ``"cognitive"``, ``"enriched"`` for ``"strings"``).

    Args:
        domain: One of the keys in DOMAINS, an alias in _DOMAIN_ALIASES,
                or ``"strings"`` for the inline group.
        out:    Output directory.

    Returns:
        Tuple of (generated file paths, per-figure failure identifiers).
        The failure list is read from the domain module's ``LAST_FAILURES``
        (empty for the "strings" domain, which has no such module) so a
        domain that only partially rendered is not reported as a full
        success.
    """
    # Resolve alias first
    resolved = _DOMAIN_ALIASES.get(domain, domain)

    if resolved == "strings":
        return _generate_string_enriched(out), list(STRINGS_LAST_FAILURES)

    if resolved not in DOMAINS:
        raise ValueError(
            f"Unknown domain '{domain}'. "
            f"Available: {sorted(DOMAINS)} + aliases: {sorted(_DOMAIN_ALIASES)}"
        )

    module_name = DOMAINS[resolved]
    import importlib
    mod = importlib.import_module(module_name)
    paths = mod.run(out)
    failures = list(getattr(mod, "LAST_FAILURES", []))
    return paths, failures


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate canonical figures for the cognitive_case_diagrams project.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    all_domain_choices = list(DOMAINS.keys()) + list(_DOMAIN_ALIASES.keys()) + ["all"]
    parser.add_argument(
        "--domain",
        choices=all_domain_choices,
        default="all",
        metavar="DOMAIN",
        help=(
            "Domain to generate figures for: "
            f"{', '.join(DOMAINS.keys())}, strings; "
            "aliases: daif (=cognitive), enriched (=strings). Default: all"
        ),
    )
    parser.add_argument(
        "--output", type=Path, default=OUTPUT_DIR,
        help="Output directory (default: output/figures)",
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List available domains and aliases, then exit",
    )
    parser.add_argument(
        "--skip-failed", action="store_true",
        help="Continue after domain failures and exit 0 even if some domains failed",
    )
    args = parser.parse_args()

    if args.list:
        print("Available domains:")
        for d in sorted(DOMAINS.keys()) + ["strings"]:
            print(f"  {d}")
        print("Aliases:")
        for alias, target in sorted(_DOMAIN_ALIASES.items()):
            print(f"  {alias}  →  {target}")
        return 0

    out = args.output
    out.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 60)
    logger.info("Cognitive Case Diagrams — Figure Generation Pipeline")
    logger.info("=" * 60)

    if args.domain == "all":
        # "strings" is already a key of DOMAINS; appending it again ran that
        # handler twice and inflated the reported figure total to 35.
        domains_to_run = list(DOMAINS.keys())
    else:
        domains_to_run = [args.domain]

    all_outputs: list[Path] = []
    errors: list[tuple[str, Exception]] = []

    for domain in domains_to_run:
        logger.info("[%s]", domain)
        try:
            paths, failures = run_domain(domain, out)
            all_outputs.extend(paths)
            logger.info("  → %d figure(s) generated", len(paths))
            if failures:
                logger.warning(
                    "  → %d figure(s) in domain '%s' failed to render: %s",
                    len(failures), domain, ", ".join(failures),
                )
                errors.append((
                    domain,
                    RuntimeError(
                        f"{len(failures)} figure(s) failed to render: "
                        f"{', '.join(failures)}"
                    ),
                ))
        except Exception as exc:
            logger.error("  → FAILED: %s", exc)
            errors.append((domain, exc))

    logger.info("=" * 60)
    logger.info("Total: %d figure(s) → %s", len(all_outputs), out)
    for p in all_outputs:
        logger.info("  ✓ %s", p.name)
    if errors:
        logger.warning("%d domain(s) had errors:", len(errors))
        for name, exc in errors:
            logger.warning("  ✗ %s: %s", name, exc)

    # Write figure registry for PDF rendering pipeline
    _write_figure_registry(all_outputs, out)

    logger.info("=" * 60)

    if errors and not args.skip_failed:
        return 1
    return 0


# ``![caption](output/figures/<name>.png){#fig:<label>}`` — captures the image
# filename and the Pandoc label the manuscript actually uses for it.
_FIGURE_LABEL_RE = re.compile(
    r"\]\((?:[^)]*/)?(?P<filename>[\w.-]+\.(?:png|pdf|svg))\)\{#(?P<label>fig:[\w:.-]+)\}"
)


def _manuscript_figure_labels(project_root: Path) -> dict[str, str]:
    """Map figure filename -> the Pandoc label the manuscript assigns it.

    The manuscript is the authority for its own cross-reference labels. Deriving
    them from filenames instead (``fig:` + stem.replace('_','-')``) produced
    ``fig:case-category-standard`` where the manuscript writes ``fig:case-standard``,
    so 20 of 30 labels failed the shared publication gate's
    "Unregistered figure reference" check.
    """
    manuscript_dir = project_root / "docs" / "manuscript"
    if not manuscript_dir.is_dir():
        manuscript_dir = project_root / "manuscript"
    labels: dict[str, str] = {}
    for md in sorted(manuscript_dir.glob("*.md")):
        for m in _FIGURE_LABEL_RE.finditer(md.read_text(encoding="utf-8")):
            labels[m.group("filename")] = m.group("label")
    return labels


def _write_figure_registry(paths: list[Path], out_dir: Path) -> None:
    """Write figure_registry.json consumed by the PDF rendering pipeline."""
    project_root = Path(__file__).resolve().parent.parent
    manuscript_labels = _manuscript_figure_labels(project_root)

    seen: set[str] = set()
    registry: list[dict] = []
    unlabelled: list[str] = []
    for p in paths:
        if p.suffix not in {".png", ".pdf", ".svg"}:
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
        registry.append({
            "filename": p.name,
            # Project-relative: absolute paths embedded the author's home
            # directory in a repo that ships to GitHub and Zenodo.
            "path": str(rel),
            "label": label,
            "generated_by": "scripts/generate_diagrams.py",
        })
    dest = out_dir / "figure_registry.json"
    # Merge with the existing registry instead of replacing it: a
    # ``--domain X`` run regenerates only X's figures, and wholesale
    # replacement would drop the other domains' entries from the manifest the
    # PDF pipeline consumes. Newly rendered figures win on filename clashes.
    existing: dict[str, dict] = {}
    if dest.exists():
        try:
            for entry in json.loads(dest.read_text(encoding="utf-8")):
                filename = entry.get("filename")
                if isinstance(filename, str):
                    existing[filename] = entry
        except (json.JSONDecodeError, AttributeError):
            logger.warning("Existing figure registry unreadable — rebuilding it.")
    merged = {**existing, **{e["filename"]: e for e in registry}}
    merged_list = sorted(merged.values(), key=lambda e: e["filename"])
    dest.write_text(json.dumps(merged_list, indent=2) + "\n", encoding="utf-8")
    logger.info("Wrote figure registry: %s (%d entries)", dest, len(merged_list))
    if unlabelled:
        logger.warning(
            "%d figure(s) carry no manuscript label (supplementary or orphaned): %s",
            len(unlabelled), ", ".join(sorted(unlabelled)),
        )


if __name__ == "__main__":
    sys.exit(main())
