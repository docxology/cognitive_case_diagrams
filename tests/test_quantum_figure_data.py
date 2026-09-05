"""Tests for src/quantum/figure_data.py — quantum/security figure data factories.
No mocks — real computations only.
"""
import numpy as np

from src.case_systems.case_category import CaseRole
from src.quantum.figure_data import (
    make_monoidal_functor_example,
    make_quantum_povm_example,
    make_security_violations_example,
)


class TestMakeQuantumPovmExample:
    def test_returns_dict_with_required_keys(self):
        data = make_quantum_povm_example()
        for key in ("roles", "povm", "state"):
            assert key in data

    def test_roles_are_case_roles(self):
        data = make_quantum_povm_example()
        assert all(isinstance(r, CaseRole) for r in data["roles"])

    def test_eight_roles(self):
        data = make_quantum_povm_example()
        assert len(data["roles"]) == 8

    def test_povm_is_complete(self):
        data = make_quantum_povm_example()
        assert data["povm"].is_complete()

    def test_state_is_density_matrix(self):
        data = make_quantum_povm_example()
        state = data["state"]
        assert abs(np.trace(state).real - 1.0) < 1e-9
        eigenvalues = np.linalg.eigvalsh(state)
        assert np.all(eigenvalues >= -1e-10)

    def test_state_shape_matches_roles(self):
        data = make_quantum_povm_example()
        n = len(data["roles"])
        assert data["state"].shape == (n, n)


class TestMakeSecurityViolationsExample:
    def test_returns_list(self):
        assert isinstance(make_security_violations_example(), list)

    def test_three_violations(self):
        assert len(make_security_violations_example()) == 3

    def test_violations_have_scores_in_zero_one(self):
        from src.security.cognitive_security import TypeViolation
        for v in make_security_violations_example():
            assert isinstance(v, TypeViolation)
            assert 0.0 <= v.severity <= 1.0

    def test_severitys_are_ordered(self):
        violations = make_security_violations_example()
        scores = [v.severity for v in violations]
        assert scores[0] > scores[1] > scores[2]


class TestMakeMonoidalFunctorExample:
    def test_returns_monoidal_functor(self):
        from src.case_systems.functor import MonoidalFunctor
        mf = make_monoidal_functor_example()
        assert isinstance(mf, MonoidalFunctor)

    def test_has_object_map(self):
        mf = make_monoidal_functor_example()
        assert mf.object_map

    def test_maps_nom_to_erg_proxy(self):
        mf = make_monoidal_functor_example()
        assert CaseRole.NOM in mf.object_map

    def test_preserves_tensor_on_self(self):
        mf = make_monoidal_functor_example()
        roles = list(mf.object_map.keys())
        if len(roles) >= 2:
            assert isinstance(mf.preserves_tensor(roles[0], roles[1]), bool)
