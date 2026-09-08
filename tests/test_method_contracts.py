"""Analytic counterexamples for the scientific contracts (real computations)."""

import numpy as np
import pytest

from src.case_systems import CaseRole
from src.cognitive import CaseDiagramBelief, update_belief, variational_free_energy
from src.daif import (
    DistributionalReturn, distributional_case_assignment,
    quantile_td_update, implicit_quantile_network_update,
    wasserstein_return_distance,
)
from src.daif.core import _single_bellman_step, categorical_return_distribution
from src.topos_theory.topos import (
    Axiom, ClassifyingTopos, GeometricTheory, TheoryType, bridge_transfer,
)
from src.quantum import CasePOVM, case_probability
from src.security import detect_type_violation
from src.case_systems import minimal_case_category
from src.enriched_cat import EnrichedCategory


def belief(probabilities):
    return CaseDiagramBelief(list(CaseRole)[:len(probabilities)], np.array(probabilities))


@pytest.mark.parametrize("q", [np.array([1.1, -0.1]), np.array([[0.5], [0.5]])])
def test_free_energy_rejects_invalid_probability_vectors(q):
    with pytest.raises(ValueError):
        variational_free_energy(q, np.zeros_like(q), np.zeros_like(q))


def test_negative_likelihood_cannot_hide_under_zero_prior_mass():
    with pytest.raises(ValueError):
        update_belief(belief([1., 0.]), np.array([1., -1.]))


def test_quantile_td_uses_all_target_samples():
    # tau=.25: gradients +.25 and -.75; mean=-.25. tau=.75: mean=+.25.
    updated = quantile_td_update(np.zeros(2), np.array([-2., 2.]), learning_rate=1.)
    np.testing.assert_allclose(updated, [-0.25, 0.25])


def test_optimistic_distortion_targets_higher_returns():
    q = np.zeros(3)
    tau = np.array([.25, .5, .75])
    args = (q, tau, np.array([-2., 0., 2.]), tau)
    optimistic = implicit_quantile_network_update(*args, risk_distortion="optimistic")
    neutral = implicit_quantile_network_update(*args)
    pessimistic = implicit_quantile_network_update(*args, risk_distortion="pessimistic")
    assert np.all(optimistic > neutral)
    assert np.all(pessimistic < neutral)


def test_discrete_quantiles_do_not_invent_intermediate_outcomes():
    result = _single_bellman_step(np.array([.5, .5]), np.eye(2), np.array([0., 10.]), 0., 4)
    np.testing.assert_array_equal(result.quantiles, [0., 0., 10., 10.])


def test_wasserstein_compares_levels_even_when_grid_lengths_match():
    a = DistributionalReturn(0., 1., np.array([0., 1.]), np.array([.1, .2]))
    b = DistributionalReturn(0., 1., np.array([0., 1.]), np.array([.8, .9]))
    assert wasserstein_return_distance(a, b) > .5


def test_categorical_method_agrees_with_c51_projection_and_clips_mass():
    d = DistributionalReturn(0., 1., np.array([-20., .5, 20.]), np.array([1/6, .5, 5/6]))
    _, expected = categorical_return_distribution(d, 0., 1., 3)
    np.testing.assert_allclose(d.to_categorical(0., 1., 3), expected)


def test_converged_belief_matches_the_last_recorded_update():
    result = distributional_case_assignment(belief([.5, .5]), np.array([.8, .2]),
                                          np.eye(2), convergence_threshold=1., n_iterations=5)
    # The second update is proportional to the squared likelihood.
    np.testing.assert_allclose(result.belief.probabilities, [16/17, 1/17])


def test_negative_transition_entries_rejected_even_with_unit_row_sums():
    with pytest.raises(ValueError):
        distributional_case_assignment(belief([.5, .5]), np.ones(2),
                                      np.array([[2., -1.], [-1., 2.]]))


def test_matching_presentation_counts_never_authorize_theorem_transfer():
    # Same counts, incompatible axioms: every element satisfies P vs no element does.
    a = GeometricTheory("all", TheoryType.TYPOLOGICAL)
    b = GeometricTheory("none", TheoryType.TYPOLOGICAL)
    for t in (a, b):
        t.add_sort("S")
        t.add_relation("P", ("S",))
    a.add_axiom(Axiom("rule", "true", "P(x)"))
    b.add_axiom(Axiom("rule", "P(x)", "false"))
    result = bridge_transfer(ClassifyingTopos(a), ClassifyingTopos(b), "all_P")
    assert result["transfer_possible"] is False
    assert result["morita_equivalent"] is None


def test_unknown_role_identity_is_not_licensed():
    assert detect_type_violation(minimal_case_category(), CaseRole.ERG, CaseRole.ERG) is not None


def test_povm_rejects_nonhermitian_effects_even_if_they_sum_to_identity():
    a = np.array([[.5, 1.], [0., .5]])
    with pytest.raises(ValueError):
        CasePOVM([CaseRole.NOM, CaseRole.ACC],
                 {CaseRole.NOM: a, CaseRole.ACC: np.eye(2) - a})


def test_born_rule_rejects_unnormalized_density():
    with pytest.raises(ValueError):
        case_probability(np.eye(2), np.eye(2))


def test_magnitude_recomputes_after_matrix_mutation():
    c = EnrichedCategory("example", [CaseRole.NOM, CaseRole.ACC], np.eye(2))
    assert c.magnitude() == pytest.approx(2.)
    c.proximity_matrix[:] = [[1., .5], [.5, 1.]]
    assert c.magnitude() == pytest.approx(4/3)


def test_enrichment_closure_is_explicit_and_preserves_raw_input():
    from src.enriched_cat import standard_enriched_category
    candidate = standard_enriched_category()
    raw = candidate.proximity_matrix.copy()
    assert candidate.full_composition_check()['violations']
    closed = candidate.composition_closure()
    assert not closed.full_composition_check()['violations']
    np.testing.assert_array_equal(candidate.proximity_matrix, raw)
    assert np.all(closed.proximity_matrix >= raw)
    np.testing.assert_allclose(closed.composition_closure().proximity_matrix,
                               closed.proximity_matrix)


def test_singular_magnitude_requires_valid_weightings():
    c = EnrichedCategory('duplicate', list(CaseRole)[:2], np.ones((2, 2)))
    assert c.magnitude() == pytest.approx(1.)
    # Inconsistent row equations: w1+w2=1 and w1+w2+w3=1 with w2+w3=1.
    z = np.array([[1.,1.,0.], [1.,1.,1.], [0.,0.,1.]])
    c = EnrichedCategory('undefined', list(CaseRole)[:3], z)
    with pytest.raises(ValueError, match='undefined'):
        c.magnitude()


@pytest.mark.parametrize('values', [[], [[.5,.5]], [np.nan, 1], [np.inf, 0], [-.1,1.1], [.2,.2]])
def test_probability_validation_rejects_malformed_inputs(values):
    from src.numerics import probability_vector
    with pytest.raises(ValueError):
        probability_vector(values)


@pytest.mark.parametrize('count', [True, 2.5, 0, np.nan])
def test_integer_counts_reject_coercion(count):
    from src.numerics import positive_integer
    with pytest.raises(ValueError):
        positive_integer(count, 'count')


@pytest.mark.parametrize('q,tau', [([1,0],[.25,.75]), ([0,1],[.5,.5]),
                                  ([0,1],[0,.9]), ([0,1],[.2,1]), ([0,1],[.5])])
def test_invalid_quantile_grids(q,tau):
    from src.numerics import quantile_grid
    with pytest.raises(ValueError):
        quantile_grid(q,tau)


def test_weighted_quantiles_drop_zero_mass_and_respect_atoms():
    from src.numerics import weighted_quantiles
    np.testing.assert_array_equal(weighted_quantiles([0,5,10], [.5,0,.5], [.25,.5,.75]), [0,0,10])
    for support, probs, levels in [([0],[.5,.5],[.5]), ([0],[1],[0])]:
        with pytest.raises(ValueError):
            weighted_quantiles(support, probs, levels)


def test_factor_score_rejects_negative_factors_and_nonbinary_graph():
    from src.daif import factor_consistency_score
    with pytest.raises(ValueError):
        factor_consistency_score(belief([.5,.5]), [np.array([-1,2])], np.ones((2,1)))
    with pytest.raises(ValueError):
        factor_consistency_score(belief([.5,.5]), [np.ones(2)], np.full((2,1), .5))


def test_information_gain_matches_binary_channel_mutual_information():
    from src.daif import expected_information_gain
    contributions = expected_information_gain(belief([.5,.5]), np.eye(2))
    np.testing.assert_allclose(contributions, np.log(2)/2)


def test_plot_rejects_invented_free_energy_components(tmp_path):
    from src.visualization.daif_plots import plot_free_energy_convergence
    with pytest.raises(ValueError, match='sum'):
        plot_free_energy_convergence([1,2], kl_trajectory=[.5,.5],
                                     loglik_trajectory=[-.5,-.5], output_path=str(tmp_path/'bad.png'))
    assert not (tmp_path/'bad.png').exists()
