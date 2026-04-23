"""Data-generation functions for cognitive/DAIF manuscript figures.

Each function returns a plain dict of arrays/values ready for the
corresponding visualization call. Keeping data construction here (src/)
rather than in scripts/ upholds the thin-orchestrator pattern and makes
the data directly testable.
"""
from __future__ import annotations

import logging
from typing import Any

import numpy as np

from ..case_systems.case_category import CaseRole
from ..case_systems.fluid_s import bats_fluid_s, create_fluid_s_functor
from ..cognitive.belief import CaseDiagramBelief
from ..cognitive.belief_updating import sequential_belief_update
from ..daif import (
    distributional_case_assignment,
    distributional_prediction_error,
    n400_from_return_distribution,
    p600_from_precision_update,
    push_forward_return,
)

logger = logging.getLogger(__name__)


def make_belief_trajectory_data() -> dict[str, Any]:
    """Return prior, trajectory, obs_sequence, and labels for the alignment-frame figure.

    Returns:
        dict with keys: prior, trajectory, obs_sequence, evidence_labels
    """
    prior = CaseDiagramBelief(
        roles=[CaseRole.NOM, CaseRole.ERG],
        probabilities=np.array([0.5, 0.5]),
        name="alignment_frames",
    )
    obs_sequence = [
        np.array([0.58, 0.42]),
        np.array([0.62, 0.38]),
        np.array([0.88, 0.12]),
        np.array([0.91, 0.09]),
        np.array([0.95, 0.05]),
    ]
    trajectory = sequential_belief_update(prior, obs_sequence)
    return {
        "prior": prior,
        "trajectory": trajectory,
        "obs_sequence": obs_sequence,
        "evidence_labels": ["Det", "N", "V", "Acc", "Adv"],
    }


def make_fluid_s_landscape_data() -> dict[str, Any]:
    """Return functors, probabilities, and verb names for the Fluid-S landscape figure.

    Returns:
        dict with keys: vol_functor, nonvol_functor, functors, probs, verb_names
    """
    vol_functor, nonvol_functor = bats_fluid_s()
    verb_names = [
        "sneeze", "fall (acc.)", "sleep", "shiver",
        "trip", "walk", "fall (vol.)", "run", "jump", "fight",
    ]
    probs = [0.10, 0.15, 0.25, 0.30, 0.20, 0.55, 0.75, 0.80, 0.90, 0.95]
    functors = [
        create_fluid_s_functor(volitional=(p >= 0.5), probability=p)
        for p in probs
    ]
    return {
        "vol_functor": vol_functor,
        "nonvol_functor": nonvol_functor,
        "functors": functors,
        "probs": probs,
        "verb_names": verb_names,
    }


def make_daif_belief_trajectory_data() -> dict[str, Any]:
    """Return belief trajectory data for the DAIF sentence parse figure.

    Returns:
        dict with keys: trajectory, word_labels, gloss_labels
    """
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
    return {
        "trajectory": trajectory,
        "word_labels": ["Der", "Hund", "jagt", "die", "Katze", "schnell"],
        "gloss_labels": ["the.NOM", "dog.NOM", "chases", "the.ACC", "cat.ACC", "quickly"],
    }


def make_free_energy_convergence_data() -> dict[str, Any]:
    """Return free-energy convergence data for the DAIF FE figure.

    Runs distributional_case_assignment for each observation in the trajectory
    and accumulates the per-word FE sequences along with the per-iteration
    KL(q_posterior ‖ q_pushed) and expected log-likelihood terms so that
    the figure can plot the *true* decomposition F = KL − E_q[log p(o|s)]
    instead of a synthetic envelope.

    Returns:
        dict with keys: all_fe, all_kl, all_loglik, word_boundaries, word_labels
    """
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
    word_labels = ["Der", "Hund", "jagt", "die", "Katze", "schnell"]

    all_fe: list[float] = []
    all_kl: list[float] = []
    all_loglik: list[float] = []
    current = prior
    word_boundaries: list[int] = []
    for obs in obs_sequence:
        word_boundaries.append(len(all_fe) + 1)
        result = distributional_case_assignment(current, obs, n_iterations=5)
        current = result.belief
        all_fe.extend(result.fe_trajectory)
        all_kl.extend(result.diagnostics.get("kl_trajectory", []))
        all_loglik.extend(result.diagnostics.get("loglik_trajectory", []))

    return {
        "all_fe": all_fe,
        "all_kl": all_kl,
        "all_loglik": all_loglik,
        "word_boundaries": word_boundaries,
        "word_labels": word_labels,
    }


def make_erp_prediction_data() -> dict[str, Any]:
    """Return ERP prediction data (N400/P600) for the DAIF ERP figure.

    Computes per-role distributional prediction error (DPE), N400 amplitude
    via ``n400_from_return_distribution``, and P600 amplitude via
    ``p600_from_precision_update``, so that the figure can plot the *real*
    model predictions rather than ad-hoc scalings of mean(PE).

    Returns:
        dict with keys: role_names, enriched_weights, erp_errors,
            n400_amplitudes, p600_amplitudes
    """
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

    # Real N400 / P600 amplitudes via the manuscript Eqs. (7c-n400, 7c-p600).
    n = len(enriched_weights)
    T_id = np.eye(n)
    R = np.array(enriched_weights, dtype=np.float64)
    ret = push_forward_return(erp_belief, T_id, R, gamma=0.9, n_quantiles=51)
    baseline_return = float(np.mean(R))
    # Severity sweeps mild→strong across roles so the scatter shows real variation.
    severities = np.linspace(0.25, 1.0, n)
    n400_amplitudes = [
        n400_from_return_distribution(
            ret, baseline_return=baseline_return,
            precision=w, violation_severity=float(s),
        )
        for w, s in zip(enriched_weights, severities)
    ]
    p600_amplitudes = [
        p600_from_precision_update(
            prior_precision=1.0,
            posterior_precision=1.0 + w,
            dpe=dpe,
            scaling=1.0,
            violation_severity=float(s),
        )
        for w, dpe, s in zip(enriched_weights, erp_errors, severities)
    ]

    return {
        "role_names": [r.name for r in erp_roles],
        "enriched_weights": enriched_weights,
        "erp_errors": erp_errors,
        "n400_amplitudes": n400_amplitudes,
        "p600_amplitudes": p600_amplitudes,
    }
