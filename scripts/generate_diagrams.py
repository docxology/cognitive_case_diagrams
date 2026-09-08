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
    scripts/generate_string_figures.py     — string diagrams + enriched hom heatmap
    scripts/generate_category_unpacking_figures.py — pedagogical unpacking panels

Canonical outputs (see the domain registry and generated figure manifest):
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
import logging
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
except ImportError:
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
    "strings": "generate_string_figures",
    "experiments": "generate_experiment_figures",
}

_DOMAIN_ALIASES: dict[str, str] = {
    "daif":     "cognitive",
    "enriched": "strings",
    "category_unpacking": "unpacking",
}


# ── Main dispatcher ─────────────────────────────────────────────────────────

def run_domain(domain: str, out: Path) -> tuple[list[Path], list[str]]:
    """Run a single named domain's figure generation.

    Accepts canonical domain keys *or* their short aliases (e.g. ``"daif"``
    for ``"cognitive"``, ``"enriched"`` for ``"strings"``).

    Args:
        domain: One of the keys in DOMAINS or an alias in _DOMAIN_ALIASES.
        out:    Output directory.

    Returns:
        Tuple of (generated file paths, per-figure failure identifiers).
        The failure list is read from the domain module's ``LAST_FAILURES``
        so a domain that only partially rendered is not reported as a full
        success.
    """
    # Resolve alias first
    resolved = _DOMAIN_ALIASES.get(domain, domain)

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
            f"{', '.join(DOMAINS.keys())}; "
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
        for d in sorted(DOMAINS.keys()):
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

    # Write figure registry for PDF rendering pipeline. Extracted to
    # src/visualization/figure_registry.py so the release-critical writer is
    # under src coverage; A5 guards the generation window, A6 rebuilds only in
    # diagnostic mode. Per-domain failures above do not block the manifest —
    # downstream gates (project_validation) reject stale/orphaned entries.
    from src.release_validation import quality_input_fingerprint
    from src.visualization.figure_registry import write_figure_registry

    try:
        write_figure_registry(
            all_outputs, out, PROJECT_ROOT,
            expected_fingerprint=quality_input_fingerprint(PROJECT_ROOT)["sha256"],
            allow_rebuild=args.skip_failed,
        )
    except ValueError as exc:
        logger.error("Figure registry not written: %s", exc)
        return 1

    logger.info("=" * 60)


if __name__ == "__main__":
    sys.exit(main())
