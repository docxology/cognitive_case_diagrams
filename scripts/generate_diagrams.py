#!/usr/bin/env python3
"""Generate all canonical figures for the cognitive_case_diagrams project.

This is the thin orchestrator script that produces all 9+ canonical outputs
to the project output/figures/ directory. It imports computation from
projects/cognitive_case_diagrams/src/ and utilities from infrastructure/.

Canonical Outputs:
    1. case_category_standard.png    — Standard 8-case category
    2. case_category_minimal.png     — Minimal 3-role category
    3. composition_triangle.png      — Morphism composition diagram
    4. alignment_comparison.png      — Accusative/Ergative/Tripartite
    5. string_diagram_discocat.png   — DisCoCat sentence diagram
    6. enriched_hom_matrix.png       — [0,1]-enriched heatmap
    7. enriched_magnitude.txt        — Magnitude computation results
    8. discourse_string_diagram.png  — DisCoCirc 2-sentence discourse
    9. functor_alignment.png         — Alignment functor diagram

DisCoPy Outputs (optional, requires discopy):
   10. discopy_transitive.png        — DisCoPy transitive diagram
   11. discopy_composition.png       — DisCoPy composition & normal form
   12. discopy_snake.png             — Compact closure snake equations
   13. discopy_passive.png           — Passive voice type permutation
   14. discopy_sentence_progression.png — Intransitive/Transitive/Passive
   15. discopy_multilingual.png      — 6-language structural isomorphism
   16. discopy_ditransitive.png      — Ditransitive diagram
   17. discopy_discocirc_discourse.png    — DisCoPy discourse
   18. discopy_three_sentence_discourse.png — Role reversal
"""

import logging
import sys
from pathlib import Path

# Force non-interactive backend before any matplotlib/discopy imports
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("generate_diagrams")

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output" / "figures"

# Ensure project root is on sys.path so `from src.xxx` imports work
# when invoked from repo root by the pipeline orchestrator
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def ensure_output_dir() -> Path:
    """Create the output directory if it doesn't exist."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("Output directory: %s", OUTPUT_DIR)
    return OUTPUT_DIR


def generate_category_figures(out: Path) -> list[Path]:
    """Generate case category diagrams."""
    from src.case_systems.case_category import standard_case_category, minimal_case_category
    from src.visualization.category_diagrams import (
        render_case_category,
        render_alignment_comparison,
        render_composition_triangle,
    )

    outputs = []

    # 1. Standard 8-case category
    path = out / "case_category_standard.png"
    render_case_category(standard_case_category(), output_path=path)
    outputs.append(path)

    # 2. Minimal 3-role category
    path = out / "case_category_minimal.png"
    render_case_category(minimal_case_category(), output_path=path)
    outputs.append(path)

    # 3. Composition triangle
    path = out / "composition_triangle.png"
    render_composition_triangle(output_path=path)
    outputs.append(path)

    # 4. Alignment comparison
    path = out / "alignment_comparison.png"
    render_alignment_comparison(output_path=path)
    outputs.append(path)

    return outputs


def generate_string_figures(out: Path) -> list[Path]:
    """Generate string diagram figures."""
    from src.diagrams.string_diagram import Sentence, Discourse
    from src.visualization.string_diagrams import (
        render_discocat_sentence,
        render_discocirc_discourse,
        render_three_sentence_discourse,
    )

    outputs = []

    # 5. DisCoCat sentence
    sent = Sentence.transitive("Alice", "chases", "Bob")
    path = out / "string_diagram_discocat.png"
    render_discocat_sentence(sent, output_path=path)
    outputs.append(path)

    # 8. DisCoCirc 2-sentence discourse
    path = out / "discourse_string_diagram.png"
    render_discocirc_discourse(output_path=path)
    outputs.append(path)

    return outputs


def generate_enriched_figures(out: Path) -> list[Path]:
    """Generate enriched category figures and data."""
    from src.enriched_cat.enriched import standard_enriched_category
    from src.visualization.enriched_diagrams import render_enriched_heatmap

    outputs = []

    # 6. Enriched hom-value heatmap
    cat = standard_enriched_category()
    path = out / "enriched_hom_matrix.png"
    render_enriched_heatmap(cat, output_path=path)
    outputs.append(path)

    # 7. Magnitude computation text file
    mag = cat.magnitude()
    w = cat.weighting()
    path = out / "enriched_magnitude.txt"
    with open(path, "w") as f:
        f.write(f"Enriched Category: {cat.name}\n")
        f.write(f"Number of objects: {len(cat.roles)}\n")
        f.write(f"Categorical magnitude: {mag:.6f}\n")
        f.write(f"Weighting vector: {w.tolist()}\n")
    outputs.append(path)

    return outputs


def generate_functor_figures(out: Path) -> list[Path]:
    """Generate functor diagram figures."""
    from src.case_systems.functor import accusative_to_ergative_functor
    from src.visualization.functor_diagrams import render_functor_diagram

    outputs = []

    # 9. Functor alignment
    path = out / "functor_alignment.png"
    render_functor_diagram(accusative_to_ergative_functor(), output_path=path)
    outputs.append(path)

    return outputs


def generate_discopy_figures(out: Path) -> list[Path]:
    """Generate DisCoPy-based figures (optional)."""
    try:
        from src.visualization.discopy_diagrams import (
            render_discopy_transitive,
            render_discopy_composition,
            render_discopy_snake,
            render_discopy_passive,
            render_discopy_sentence_progression,
            render_discopy_multilingual,
            render_discopy_ditransitive,
            render_discopy_discocirc_discourse,
            render_discopy_three_sentence_discourse,
        )
    except ImportError:
        logger.warning("discopy not installed — skipping DisCoPy figures")
        return []

    outputs = []

    figures = [
        ("discopy_transitive.png", render_discopy_transitive),
        ("discopy_composition.png", render_discopy_composition),
        ("discopy_snake.png", render_discopy_snake),
        ("discopy_passive.png", render_discopy_passive),
        ("discopy_sentence_progression.png", render_discopy_sentence_progression),
        ("discopy_multilingual.png", render_discopy_multilingual),
        ("discopy_ditransitive.png", render_discopy_ditransitive),
        ("discopy_discocirc_discourse.png", render_discopy_discocirc_discourse),
        ("discopy_three_sentence_discourse.png", render_discopy_three_sentence_discourse),
    ]

    for fname, render_fn in figures:
        path = out / fname
        try:
            render_fn(output_path=path)
            outputs.append(path)
        except Exception as exc:
            logger.error("Failed to generate %s: %s", fname, exc)

    return outputs


def generate_complexity_figures(out: Path) -> list[Path]:
    """Generate complexity comparison figures from the complexity_metrics module."""
    try:
        from src.visualization.complexity_plots import (
            render_complexity_comparison,
        )
        from src.diagrams.complexity_metrics import compare_diagrams
        from discopy.rigid import Ty, Box, Cup, Id
    except ImportError:
        logger.warning("discopy not installed — skipping complexity figures")
        return []

    outputs = []

    # Build representative diagrams for comparison using discopy.rigid
    n = Ty('n')
    s = Ty('s')

    diagrams = []
    sentences = []
    try:
        # Intransitive: "Alice runs"
        intrans = Box("Alice", Ty(), n) @ Box("runs", Ty(), n.r @ s) >> Cup(n, n.r) @ Id(s)
        diagrams.append(("Intransitive", intrans))
        sentences.append("Alice runs")

        # Transitive: "Alice chases Bob"
        trans = (
            Box("Alice", Ty(), n)
            @ Box("chases", Ty(), n.r @ s @ n.l)
            @ Box("Bob", Ty(), n)
            >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
        )
        diagrams.append(("Transitive", trans))
        sentences.append("Alice chases Bob")

        # Ditransitive: "Alice gave Bob book"
        ditrans = (
            Box("Alice", Ty(), n)
            @ Box("gave", Ty(), n.r @ s @ n.l @ n.l)
            @ Box("Bob", Ty(), n)
            @ Box("book", Ty(), n)
        )
        ditrans = ditrans >> Cup(n, n.r) @ Id(s @ n.l @ n.l @ n @ n)
        ditrans = ditrans >> Id(s @ n.l) @ Cup(n.l, n) @ Id(n)
        ditrans = ditrans >> Id(s) @ Cup(n.l, n)
        diagrams.append(("Ditransitive", ditrans))
        sentences.append("Alice gave Bob book")

        # Adjective Transitive: "fast Alice chases Bob"
        fast = Box("fast", Ty(), n @ n.l)
        alice = Box("Alice", Ty(), n)
        chases = Box("chases", Ty(), n.r @ s @ n.l)
        bob = Box("Bob", Ty(), n)
        adj_trans = (fast @ alice @ chases @ bob)
        adj_trans = adj_trans >> Id(n) @ Cup(n.l, n) @ Id(n.r @ s @ n.l @ n)
        adj_trans = adj_trans >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
        diagrams.append(("Adj Transitive", adj_trans))
        sentences.append("fast Alice chases Bob")

        # Adverb Transitive: "Alice chases Bob today"
        today = Box("today", Ty(), s.r @ s)
        adv_trans = (alice @ chases @ bob @ today)
        adv_trans = adv_trans >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n) @ Id(s.r @ s)
        adv_trans = adv_trans >> Cup(s, s.r) @ Id(s)
        diagrams.append(("Adv Transitive", adv_trans))
        sentences.append("Alice chases Bob today")

        # Complex: "fast Alice chases Bob today"
        complex_s = (fast @ alice @ chases @ bob @ today)
        complex_s = complex_s >> Id(n) @ Cup(n.l, n) @ Id(n.r @ s @ n.l @ n @ s.r @ s)
        complex_s = complex_s >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n) @ Id(s.r @ s)
        complex_s = complex_s >> Cup(s, s.r) @ Id(s)
        diagrams.append(("Complex", complex_s))
        sentences.append("fast Alice chases Bob today")

        metrics_list = compare_diagrams(diagrams)

        # Unpack metrics into separate lists for render_complexity_comparison
        labels = [m.name for m in metrics_list]
        box_counts = [m.box_count for m in metrics_list]
        word_counts = [m.word_count for m in metrics_list]
        cup_counts = [m.cup_count for m in metrics_list]

        path = out / "complexity_comparison.png"
        render_complexity_comparison(labels, box_counts, word_counts, cup_counts, sentences, output_path=str(path))
        outputs.append(path)
    except Exception as exc:
        logger.error("Failed to generate complexity_comparison.png: %s", exc)

    return outputs


def generate_active_inference_figures(out: Path) -> list[Path]:
    """Generate Active Inference belief distribution figures."""
    import numpy as np
    from src.cognitive.active_inference import CaseDiagramBelief
    from src.case_systems.case_category import CaseRole
    from src.visualization.active_inference_plots import plot_belief_distribution

    outputs = []
    
    belief = CaseDiagramBelief(
        roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
        probabilities=np.array([0.7, 0.2, 0.1]),
    )
    
    path = out / "active_inference_belief.png"
    plot_belief_distribution(belief, output_path=str(path))
    outputs.append(path)
    
    return outputs


def generate_quantum_figures(out: Path) -> list[Path]:
    """Generate Quantum Case POVM figures."""
    import numpy as np
    from src.quantum.quantum_case import crisp_case_povm, semantic_state
    from src.visualization.quantum_plots import plot_povm_probabilities
    from src.case_systems.case_category import CaseRole

    outputs = []
    
    roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT, CaseRole.GEN, 
             CaseRole.INS, CaseRole.LOC, CaseRole.ABL, CaseRole.VOC]
    povm = crisp_case_povm(roles)
    
    weights = {CaseRole.NOM: 0.8, CaseRole.ACC: 0.1, CaseRole.DAT: 0.1}
    state = semantic_state(weights, dimension=len(roles), roles=roles)
    
    path = out / "quantum_povm_probabilities.png"
    plot_povm_probabilities(povm, state, output_path=str(path))
    outputs.append(path)
    
    return outputs


def generate_security_figures(out: Path) -> list[Path]:
    """Generate Cognitive Security violation figures."""
    from src.security.cognitive_security import TypeViolation
    from src.case_systems.case_category import CaseRole
    from src.visualization.security_plots import plot_type_violations

    outputs = []
    
    violations = [
        TypeViolation(CaseRole.NOM, CaseRole.ACC, "subject_wire", 0.9, "Critcal alignment mismatch"),
        TypeViolation(CaseRole.DAT, CaseRole.ACC, "indirect_wire", 0.6, "Case promotion detected"),
        TypeViolation(CaseRole.GEN, CaseRole.LOC, "modifier_wire", 0.4, "Spatial reassignment"),
    ]
    
    path = out / "security_type_violations.png"
    plot_type_violations(violations, output_path=str(path))
    outputs.append(path)
    
    return outputs


def generate_fluid_s_figures(out: Path) -> list[Path]:
    """Generate Fluid-S volition landscape figures."""
    from src.case_systems.fluid_s import bats_fluid_s
    from src.visualization.fluid_s_plots import plot_fluid_s_volition_landscape

    outputs = []
    
    functor = bats_fluid_s()
    
    verb_names = ["sneeze", "fall", "sleep", "run", "jump"]
    probs = [0.1, 0.2, 0.4, 0.8, 0.9]
    
    path = out / "fluid_s_volition_landscape.png"
    plot_fluid_s_volition_landscape([functor]*5, probs, verb_names, output_path=str(path))
    outputs.append(path)
    
    return outputs


def main() -> int:
    """Main entry point for the diagram generation pipeline."""
    logger.info("=" * 60)
    logger.info("Cognitive Case Diagrams — Figure Generation Pipeline")
    logger.info("=" * 60)

    out = ensure_output_dir()
    all_outputs = []
    errors = []

    # Generate core figures (always available)
    for name, gen_fn in [
        ("Category diagrams", generate_category_figures),
        ("String diagrams", generate_string_figures),
        ("Enriched diagrams", generate_enriched_figures),
        ("Functor diagrams", generate_functor_figures),
        ("DisCoPy diagrams", generate_discopy_figures),
        ("Complexity figures", generate_complexity_figures),
        ("Active Inference figures", generate_active_inference_figures),
        ("Quantum figures", generate_quantum_figures),
        ("Security figures", generate_security_figures),
        ("Fluid-S figures", generate_fluid_s_figures),
    ]:
        try:
            outputs = gen_fn(out)
            logger.info("  %s: %d figures generated", name, len(outputs))
            all_outputs.extend(outputs)
        except Exception as exc:
            logger.error("  %s: FAILED — %s", name, exc)
            errors.append((name, exc))

    # Summary
    logger.info("=" * 60)
    logger.info("Generated %d figures to %s", len(all_outputs), out)
    for path in all_outputs:
        logger.info("  ✓ %s", path.name)
    if errors:
        logger.warning("  %d generation steps had errors", len(errors))
        for name, exc in errors:
            logger.warning("  ✗ %s: %s", name, exc)
    logger.info("=" * 60)

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
