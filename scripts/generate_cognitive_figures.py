#!/usr/bin/env python3
"""Generate cognitive / active inference figure group.

Thin orchestrator for cognitive-domain figures:
    1. active_inference_belief.png     — Belief distribution bar chart
    2. fluid_s_volition_landscape.png  — Fluid-S functor landscape
    3. daif_belief_trajectory.png      — DAIF sentence parse trajectory
    4. daif_free_energy_convergence.png — DAIF FE decomposition (2-panel)
    5. daif_erp_predictions.png        — N400/P600 ERP predictions (3-panel)

Usage::

    python scripts/generate_cognitive_figures.py
    python scripts/generate_cognitive_figures.py --output /path/to/dir

Can also be imported and called programmatically:
    from scripts.generate_cognitive_figures import run
    paths = run(output_dir)
"""

import argparse
import logging
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("generate_cognitive_figures")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = PROJECT_ROOT / "output" / "figures"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _active_inference_belief(out: Path) -> Path:
    from src.case_systems.case_category import CaseRole
    from src.cognitive.belief import CaseDiagramBelief
    from src.visualization.active_inference_plots import plot_belief_distribution

    belief = CaseDiagramBelief(
        roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
        probabilities=np.array([0.7, 0.2, 0.1]),
    )
    path = out / "active_inference_belief.png"
    plot_belief_distribution(belief, output_path=str(path))
    return path


def _fluid_s(out: Path) -> Path:
    from src.case_systems.fluid_s import bats_fluid_s
    from src.visualization.fluid_s_plots import plot_fluid_s_volition_landscape

    functor = bats_fluid_s()
    verb_names = ["sneeze", "fall", "sleep", "run", "jump"]
    probs = [0.1, 0.2, 0.4, 0.8, 0.9]
    path = out / "fluid_s_volition_landscape.png"
    plot_fluid_s_volition_landscape([functor] * 5, probs, verb_names, output_path=str(path))
    return path


def _daif_figures(out: Path) -> list[Path]:
    from src.case_systems.case_category import CaseRole
    from src.cognitive.belief import CaseDiagramBelief
    from src.cognitive.belief_updating import sequential_belief_update
    from src.daif import (
        distributional_case_assignment,
        distributional_prediction_error,
    )
    from src.visualization.daif_plots import (
        plot_belief_trajectory,
        plot_free_energy_convergence,
        plot_erp_predictions,
    )

    word_labels = ["Der", "Hund", "jagt", "die", "Katze", "schnell"]
    gloss_labels = ["the.NOM", "dog.NOM", "chases", "the.ACC", "cat.ACC", "quickly"]
    roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT, CaseRole.INS]

    prior = CaseDiagramBelief(
        roles=roles,
        probabilities=np.array([0.25, 0.25, 0.25, 0.25]),
        name="daif_prior",
    )
    obs_sequence = [
        np.array([0.45, 0.20, 0.20, 0.15]),
        np.array([0.55, 0.20, 0.15, 0.10]),
        np.array([0.65, 0.20, 0.10, 0.05]),
        np.array([0.70, 0.20, 0.07, 0.03]),
        np.array([0.80, 0.12, 0.05, 0.03]),
        np.array([0.85, 0.08, 0.04, 0.03]),
    ]
    trajectory = sequential_belief_update(prior, obs_sequence)

    path_traj = out / "daif_belief_trajectory.png"
    plot_belief_trajectory(
        trajectory,
        word_labels=word_labels,
        gloss_labels=gloss_labels,
        output_path=str(path_traj),
    )

    # Free energy convergence — accumulate per-word FE trajectories
    all_fe: list[float] = []
    current = prior
    word_boundaries: list[int] = []
    for obs in obs_sequence:
        word_boundaries.append(len(all_fe) + 1)
        result = distributional_case_assignment(current, obs, n_iterations=5)
        current = result.belief
        all_fe.extend(result.fe_trajectory)

    path_fe = out / "daif_free_energy_convergence.png"
    plot_free_energy_convergence(
        all_fe,
        word_boundaries=word_boundaries,
        word_labels=word_labels,
        output_path=str(path_fe),
    )

    # ERP predictions — all 8 case roles
    erp_roles = [
        CaseRole.NOM, CaseRole.ACC, CaseRole.GEN, CaseRole.DAT,
        CaseRole.INS, CaseRole.LOC, CaseRole.ABL, CaseRole.VOC,
    ]
    erp_belief = CaseDiagramBelief(
        roles=erp_roles,
        probabilities=np.array([0.35, 0.25, 0.12, 0.10, 0.07, 0.05, 0.03, 0.03]),
    )
    enriched_weights = [0.95, 0.85, 0.70, 0.60, 0.45, 0.35, 0.20, 0.10]
    erp_errors = [
        distributional_prediction_error(erp_belief, i, w)
        for i, w in enumerate(enriched_weights)
    ]
    path_erp = out / "daif_erp_predictions.png"
    plot_erp_predictions(
        [r.name for r in erp_roles], enriched_weights, erp_errors,
        output_path=str(path_erp),
    )

    return [path_traj, path_fe, path_erp]


def run(out: Path) -> list[Path]:
    """Generate all cognitive/active-inference figures into *out* directory.

    Args:
        out: Directory to write PNG files into.

    Returns:
        List of paths to generated files.
    """
    out.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    steps = [
        ("active_inference_belief",  _active_inference_belief),
        ("fluid_s",                  _fluid_s),
    ]
    for name, fn in steps:
        try:
            path = fn(out)
            outputs.append(path)
            logger.info("  ✓ %s", path.name)
        except Exception as exc:
            logger.error("  ✗ %s: %s", name, exc)

    try:
        paths = _daif_figures(out)
        outputs.extend(paths)
        for p in paths:
            logger.info("  ✓ %s", p.name)
    except Exception as exc:
        logger.error("  ✗ daif_figures: %s", exc)

    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate cognitive / active inference figures."
    )
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT,
        help="Output directory (default: output/figures)"
    )
    args = parser.parse_args()
    outputs = run(args.output)
    logger.info("Generated %d cognitive figures", len(outputs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
