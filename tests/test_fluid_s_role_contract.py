"""P1-08 acceptance controls: Fluid-S S-role contract + docstring reconciliation."""
import numpy as np
import pytest

from src.case_systems.case_category import CaseRole
from src.case_systems.fluid_s import (
    VolitionContext,
    bats_fluid_s,
    create_fluid_s_functor,
    fluid_s_enriched_weight,
)
from src.quantum.quantum_case import fluid_s_povm  # noqa: E501


class TestMapObjectSRoute:
    def test_volitional_s_maps_to_nom(self):
        f = create_fluid_s_functor(volitional=True)
        assert f.map_object(CaseRole.S) == CaseRole.NOM

    def test_non_volitional_s_maps_to_acc(self):
        f = create_fluid_s_functor(volitional=False)
        assert f.map_object(CaseRole.S) == CaseRole.ACC

    def test_nom_proxy_unchanged(self):
        assert create_fluid_s_functor(volitional=True).map_object(CaseRole.NOM) == CaseRole.NOM
        assert create_fluid_s_functor(volitional=False).map_object(CaseRole.NOM) == CaseRole.ACC

    def test_a_and_p_pass_through(self):
        for ctx in (VolitionContext.VOLITIONAL, VolitionContext.NON_VOLITIONAL):
            f = create_fluid_s_functor(volitional=ctx == VolitionContext.VOLITIONAL)
            assert f.map_object(CaseRole.A) == CaseRole.A
            assert f.map_object(CaseRole.P) == CaseRole.P

    def test_obliques_pass_through(self):
        f = create_fluid_s_functor(volitional=True)
        for role in (CaseRole.GEN, CaseRole.DAT, CaseRole.INS,
                     CaseRole.LOC, CaseRole.ABL, CaseRole.VOC):
            assert f.map_object(role) == role
        assert f.map_object(CaseRole.ACC) == CaseRole.ACC


class TestGradedSplitS:
    @pytest.mark.parametrize("p", [0.0, 0.3, 0.5, 1.0])
    def test_s_graded_split(self, p):
        f = create_fluid_s_functor(probability=p)
        dist = f.map_object_in_context(CaseRole.S, p)
        assert dist == {CaseRole.NOM: p, CaseRole.ACC: 1.0 - p}
        assert sum(dist.values()) == pytest.approx(1.0)

    def test_split_probability_s_uses_stored_field(self):
        f = create_fluid_s_functor(probability=0.3)
        assert f.split_probability(CaseRole.S) == {CaseRole.NOM: 0.3, CaseRole.ACC: 0.7}

    def test_nom_split_unchanged(self):
        f = create_fluid_s_functor(probability=0.3)
        assert f.map_object_in_context(CaseRole.NOM, 0.3) == {CaseRole.NOM: 0.3, CaseRole.ACC: 0.7}

    def test_boundary_p_zero(self):
        assert create_fluid_s_functor(probability=0.0).map_object_in_context(CaseRole.S, 0.0) \
            == {CaseRole.NOM: 0.0, CaseRole.ACC: 1.0}

    def test_boundary_p_one(self):
        assert create_fluid_s_functor(probability=1.0).map_object_in_context(CaseRole.S, 1.0) \
            == {CaseRole.NOM: 1.0, CaseRole.ACC: 0.0}

    def test_invalid_p_raises(self):
        f = create_fluid_s_functor()
        with pytest.raises(ValueError, match="p_volitional"):
            f.map_object_in_context(CaseRole.S, 1.5)


class TestNonSDeterministic:
    def test_non_s_roles_deterministic(self):
        f = create_fluid_s_functor(probability=0.5)
        for role in (CaseRole.A, CaseRole.P, CaseRole.ACC, CaseRole.GEN,
                     CaseRole.DAT, CaseRole.INS, CaseRole.LOC, CaseRole.ABL,
                     CaseRole.VOC, CaseRole.ERG, CaseRole.ABS):
            dist = f.map_object_in_context(role, 0.5)
            assert dist == {f.map_object(role): 1.0}


class TestUnchangedSurfaces:
    def test_create_fluid_s_functor_entry_points(self):
        vol = create_fluid_s_functor(volitional=True)
        nonvol = create_fluid_s_functor(volitional=False)
        assert vol.volition == VolitionContext.VOLITIONAL
        assert nonvol.volition == VolitionContext.NON_VOLITIONAL
        with pytest.raises(ValueError, match="volition_probability"):
            create_fluid_s_functor(probability=1.5)

    def test_bats_pair(self):
        vol, nonvol = bats_fluid_s()
        assert vol.volition == VolitionContext.VOLITIONAL
        assert nonvol.volition == VolitionContext.NON_VOLITIONAL

    def test_enriched_weight_exact(self):
        assert fluid_s_enriched_weight(0.3, 1.0) == 0.3
        with pytest.raises(ValueError):
            fluid_s_enriched_weight(1.5, 1.0)

    def test_fluid_s_povm_untouched(self):
        # Quantum-study surface: analytic identity must remain byte-identical.
        povm = fluid_s_povm(p_volitional=0.5)
        assert float(np.linalg.norm(
            povm.elements[CaseRole.NOM] @ povm.elements[CaseRole.ACC])) < 1e-12
        rho = np.diag([0.7 + 0j, 0.3 + 0j])
        assert abs(float(np.real(np.trace(
            povm.elements[CaseRole.NOM] @ rho))) - 0.5) < 1e-12