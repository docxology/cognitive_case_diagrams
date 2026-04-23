#!/usr/bin/env python3
"""Generate cognitive / active inference figure group.

Thin orchestrator for cognitive-domain figures:
    1. active_inference_belief.png     — Scalar alignment-frame trajectory (3-panel)
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
if not matplotlib.is_interactive():
    matplotlib.use("Agg")

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
    from src.cognitive.figure_data import make_belief_trajectory_data
    from src.visualization.active_inference_plots import (
        plot_alignment_frame_belief_dynamics,
    )

    data = make_belief_trajectory_data()
    path = out / "active_inference_belief.png"
    plot_alignment_frame_belief_dynamics(
        data["prior"],
        data["trajectory"],
        data["obs_sequence"],
        evidence_labels=data["evidence_labels"],
        output_path=str(path),
    )
    return path


def _fluid_s(out: Path) -> Path:
    from src.cognitive.figure_data import make_fluid_s_landscape_data
    from src.visualization.fluid_s_plots import plot_fluid_s_volition_landscape

    data = make_fluid_s_landscape_data()
    path = out / "fluid_s_volition_landscape.png"
    plot_fluid_s_volition_landscape(
        data["functors"], data["probs"], data["verb_names"], output_path=str(path)
    )
    return path


def _daif_figures(out: Path) -> list[Path]:
    from src.cognitive.figure_data import (
        make_daif_belief_trajectory_data,
        make_erp_prediction_data,
        make_free_energy_convergence_data,
    )
    from src.visualization.daif_plots import (
        plot_belief_trajectory,
        plot_erp_predictions,
        plot_free_energy_convergence,
    )

    traj_data = make_daif_belief_trajectory_data()
    path_traj = out / "daif_belief_trajectory.png"
    plot_belief_trajectory(
        traj_data["trajectory"],
        word_labels=traj_data["word_labels"],
        gloss_labels=traj_data["gloss_labels"],
        output_path=str(path_traj),
    )

    fe_data = make_free_energy_convergence_data()
    path_fe = out / "daif_free_energy_convergence.png"
    plot_free_energy_convergence(
        fe_data["all_fe"],
        word_boundaries=fe_data["word_boundaries"],
        word_labels=fe_data["word_labels"],
        kl_trajectory=fe_data.get("all_kl"),
        loglik_trajectory=fe_data.get("all_loglik"),
        output_path=str(path_fe),
    )

    erp_data = make_erp_prediction_data()
    path_erp = out / "daif_erp_predictions.png"
    plot_erp_predictions(
        erp_data["role_names"],
        erp_data["enriched_weights"],
        erp_data["erp_errors"],
        n400_amplitudes=erp_data.get("n400_amplitudes"),
        p600_amplitudes=erp_data.get("p600_amplitudes"),
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
