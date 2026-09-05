"""Factory functions supplying plot-ready data for quantum/security figures.

All domain logic (POVM construction, violation examples, functor wrapping)
lives here. Scripts remain thin orchestrators.
"""
from __future__ import annotations

from typing import Any


from ..case_systems.case_category import CaseRole
from ..case_systems.functor import MonoidalFunctor, accusative_to_ergative_functor
from ..quantum.quantum_case import CasePOVM, crisp_case_povm, semantic_state
from ..security.cognitive_security import TypeViolation


def make_quantum_povm_example() -> dict[str, Any]:
    """Return POVM, density matrix, and role list for the POVM figure.

    Returns:
        Dict with keys ``roles``, ``povm``, ``state``.
    """
    roles: list[CaseRole] = [
        CaseRole.NOM, CaseRole.ACC, CaseRole.DAT, CaseRole.GEN,
        CaseRole.INS, CaseRole.LOC, CaseRole.ABL, CaseRole.VOC,
    ]
    povm: CasePOVM = crisp_case_povm(roles)
    weights = {CaseRole.NOM: 0.8, CaseRole.ACC: 0.1, CaseRole.DAT: 0.1}
    state = semantic_state(weights, dimension=len(roles), roles=roles)
    return {"roles": roles, "povm": povm, "state": state}


def make_security_violations_example() -> list[TypeViolation]:
    """Return a canonical list of TypeViolation examples for the security figure.

    Returns:
        Three violations spanning critical, moderate, and low severity.
    """
    return [
        TypeViolation(CaseRole.NOM, CaseRole.ACC, "subject_wire", 0.9,
                      "Critical alignment mismatch"),
        TypeViolation(CaseRole.DAT, CaseRole.ACC, "indirect_wire", 0.6,
                      "Case promotion detected"),
        TypeViolation(CaseRole.GEN, CaseRole.LOC, "modifier_wire", 0.4,
                      "Spatial reassignment"),
    ]


def make_monoidal_functor_example() -> MonoidalFunctor:
    """Return a MonoidalFunctor wrapping the accusative-to-ergative alignment.

    Wraps the base AlignmentFunctor in a MonoidalFunctor so that §9b
    tensor-preservation analysis can be visualised.

    Returns:
        MonoidalFunctor with the accusative→ergative object map.
    """
    base = accusative_to_ergative_functor()
    return MonoidalFunctor(
        name=base.name,
        source=base.source,
        target=base.target,
        object_map=base.object_map,
    )
