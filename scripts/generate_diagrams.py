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

Canonical Outputs (26 total):
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
    Cognitive domain (5):
        active_inference_belief.png, fluid_s_volition_landscape.png,
        daif_belief_trajectory.png, daif_free_energy_convergence.png,
        daif_erp_predictions.png
    Quantum/security domain (2):
        quantum_povm_probabilities.png, security_type_violations.png
    Syntactic domain (1):
        syntactic_case_panel.png

Usage::

    # All domains:
    python scripts/generate_diagrams.py

    # Single domain:
    python scripts/generate_diagrams.py --domain daif
    python scripts/generate_diagrams.py --domain category
    python scripts/generate_diagrams.py --domain discopy
    python scripts/generate_diagrams.py --domain quantum
    python scripts/generate_diagrams.py --domain syntactic

    # List available domains:
    python scripts/generate_diagrams.py --list
"""

import argparse
import logging
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("generate_diagrams")

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
}

# String/enriched figures don't yet have a dedicated sub-script;
# handled inline below for backward compatibility.


def _generate_string_enriched(out: Path) -> list[Path]:
    """Generate string diagram and enriched category figures (inline)."""
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

    try:
        path = out / "discourse_string_diagram.png"
        render_discocirc_discourse(output_path=path)
        outputs.append(path)
        logger.info("  ✓ discourse_string_diagram.png")
    except Exception as exc:
        logger.error("  ✗ discourse_string_diagram.png: %s", exc)

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

    return outputs


# ── Main dispatcher ─────────────────────────────────────────────────────────

def run_domain(domain: str, out: Path) -> list[Path]:
    """Run a single named domain's figure generation.

    Args:
        domain: One of the keys in DOMAINS, or ``"strings"`` for the inline group.
        out:    Output directory.

    Returns:
        List of generated file paths.
    """
    if domain == "strings":
        return _generate_string_enriched(out)

    if domain not in DOMAINS:
        raise ValueError(f"Unknown domain '{domain}'. Available: {sorted(DOMAINS)}")

    module_name = DOMAINS[domain]
    import importlib
    mod = importlib.import_module(module_name)
    return mod.run(out)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate canonical figures for the cognitive_case_diagrams project.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--domain",
        choices=list(DOMAINS.keys()) + ["strings", "all"],
        default="all",
        metavar="DOMAIN",
        help=(
            "Domain to generate figures for: "
            f"{', '.join(DOMAINS.keys())}, strings, all (default: all)"
        ),
    )
    parser.add_argument(
        "--output", type=Path, default=OUTPUT_DIR,
        help="Output directory (default: output/figures)",
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List available domains and exit",
    )
    args = parser.parse_args()

    if args.list:
        print("Available domains:")
        for d in sorted(list(DOMAINS.keys()) + ["strings"]):
            print(f"  {d}")
        return 0

    out = args.output
    out.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 60)
    logger.info("Cognitive Case Diagrams — Figure Generation Pipeline")
    logger.info("=" * 60)

    if args.domain == "all":
        domains_to_run = list(DOMAINS.keys()) + ["strings"]
    else:
        domains_to_run = [args.domain]

    all_outputs: list[Path] = []
    errors: list[tuple[str, Exception]] = []

    for domain in domains_to_run:
        logger.info("[%s]", domain)
        try:
            paths = run_domain(domain, out)
            all_outputs.extend(paths)
            logger.info("  → %d figure(s) generated", len(paths))
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
    logger.info("=" * 60)

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
