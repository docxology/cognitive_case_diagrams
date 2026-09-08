"""Textual theory presentations and profile comparison.

No classifying topos, Morita-equivalence witness, or theorem transfer is
constructed. Counts and arities are not topos-theoretic invariants.
"""
from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass, field
from enum import Enum


from ..case_systems.case_category import CaseCategory
from ..enriched_cat.enriched import EnrichedCategory

logger = logging.getLogger(__name__)


class TheoryType(Enum):
    """Types of geometric theories for case systems."""
    TYPOLOGICAL = "typological"
    TYPE_LOGICAL = "type_logical"
    DISTRIBUTIONAL = "distributional"
    ENRICHED = "enriched"


@dataclass
class Axiom:
    """A geometric axiom (sequent) in a case theory.

    Geometric axioms have the form φ ⊢_x ψ, where φ and ψ are
    geometric formulae (finite conjunctions, arbitrary disjunctions,
    existential quantification).

    Attributes:
        name: Human-readable axiom name.
        antecedent: String representation of the antecedent formula φ.
        consequent: String representation of the consequent formula ψ.
        sort_variables: List of sorted variable names.
    """

    name: str
    antecedent: str
    consequent: str
    sort_variables: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        """Format axiom as a sequent."""
        vars_str = ", ".join(self.sort_variables) if self.sort_variables else "∅"
        return f"{self.antecedent} ⊢_{{{vars_str}}} {self.consequent}"


@dataclass
class GeometricTheory:
    """A geometric theory axiomatizing a case-theoretic framework.

    Attributes:
        name: Theory name.
        theory_type: Which framework this theory formalizes.
        sorts: The sorts (types) of the theory.
        relation_symbols: Function/relation symbols with their arities.
        axioms: List of geometric axioms.
    """

    name: str
    theory_type: TheoryType
    sorts: list[str] = field(default_factory=list)
    relation_symbols: dict[str, tuple[str, ...]] = field(default_factory=dict)
    axioms: list[Axiom] = field(default_factory=list)

    def add_sort(self, sort_name: str) -> None:
        """Add a sort to the theory's signature.

        Args:
            sort_name: Name of the sort to add.
        """
        if sort_name not in self.sorts:
            self.sorts.append(sort_name)
            logger.debug("Added sort '%s' to theory %s", sort_name, self.name)

    def add_relation(self, name: str, arity: tuple[str, ...]) -> None:
        """Add a relation symbol to the theory's signature.

        Args:
            name: Relation symbol name.
            arity: Tuple of sort names forming the arity.

        Raises:
            ValueError: If any sort in the arity is not defined.
        """
        for sort in arity:
            if sort not in self.sorts:
                raise ValueError(
                    f"Sort '{sort}' in arity of '{name}' "
                    f"not defined in theory {self.name}"
                )
        self.relation_symbols[name] = arity
        logger.debug(
            "Added relation %s: %s to theory %s",
            name, " × ".join(arity), self.name,
        )

    def add_axiom(self, axiom: Axiom) -> None:
        """Add a geometric axiom to the theory.

        Args:
            axiom: The axiom to add.
        """
        self.axioms.append(axiom)
        logger.debug("Added axiom '%s' to theory %s", axiom.name, self.name)

    def signature_invariant(self) -> tuple[int, int, int]:
        """Count the supplied sorts, relations, and axioms.

        These counts describe the presentation. Adding a redundant axiom
        changes them without changing the theory or its classifying topos.

        Returns:
            Tuple of (num_sorts, num_relations, num_axioms).
        """
        return (len(self.sorts), len(self.relation_symbols), len(self.axioms))

    def arity_spectrum(self) -> list[int]:
        """Compute the sorted list of relation arities.

        The arity spectrum depends on the chosen signature.

        Returns:
            Sorted list of arity lengths.
        """
        return sorted(len(a) for a in self.relation_symbols.values())


@dataclass
class ClassifyingTopos:
    """Legacy-named container for finite presentation statistics.

    This does not construct a classifying topos or its invariants. The
    ``invariants`` field name is retained for compatibility only.

    Attributes:
        theory: The underlying geometric theory.
        invariants: Presentation statistics (not equivalence invariants).
    """

    theory: GeometricTheory
    invariants: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Compute invariants on construction."""
        self._compute_invariants()

    def _compute_invariants(self) -> None:
        """Refresh signature shape, arity spectrum, axiom count, and theory label.

These are presentation statistics; the field name is retained for compatibility.
"""
        self.invariants["signature_shape"] = self.theory.signature_invariant()
        self.invariants["arity_spectrum"] = self.theory.arity_spectrum()
        self.invariants["axiom_count"] = len(self.theory.axioms)
        self.invariants["theory_type"] = self.theory.theory_type.value

        logger.info(
            "Computed presentation profile for %s: "
            "signature=%s, arities=%s",
            self.theory.name,
            self.invariants["signature_shape"],
            self.invariants["arity_spectrum"],
        )


def compare_theory_presentations(
    topos1: ClassifyingTopos,
    topos2: ClassifyingTopos,
) -> tuple[bool, list[str]]:
    """Compare counts in two finite theory presentations.

    Signature counts and arities are presentation-dependent, not Morita
    invariants. A match is neither necessary nor sufficient for equivalence
    of classifying toposes. This function compares no axiom semantics.
    """
    # Recompute because the wrapped theory can be modified after construction.
    topos1._compute_invariants()
    topos2._compute_invariants()
    mismatches: list[str] = []

    # Check arity spectrum
    spec1 = topos1.invariants.get("arity_spectrum", [])
    spec2 = topos2.invariants.get("arity_spectrum", [])
    if spec1 != spec2:
        mismatches.append(
            f"Arity spectra differ: {spec1} vs {spec2}"
        )

    # Compare the full signature shape (num_sorts, num_relations, num_axioms)
    # exactly. The previous `abs(axiom_count1 - axiom_count2) > 2` slack could
    # never fire — every theory this module builds has exactly 2 axioms — so the
    # condition was vacuous, and it ignored the sort and relation counts entirely.
    shape1 = topos1.invariants.get("signature_shape")
    shape2 = topos2.invariants.get("signature_shape")
    if shape1 != shape2:
        mismatches.append(
            f"Signature shapes differ (sorts, relations, axioms): {shape1} vs {shape2}"
        )

    not_ruled_out = len(mismatches) == 0
    logger.info(
        "Presentation comparison %s / %s: %s (%d mismatches)",
        topos1.theory.name, topos2.theory.name,
        "MATCH" if not_ruled_out else "DIFFERENT",
        len(mismatches),
    )
    return not_ruled_out, mismatches


def check_morita_equivalence(
    topos1: ClassifyingTopos, topos2: ClassifyingTopos,
) -> tuple[bool, list[str]]:
    """Deprecated presentation comparator; does not decide Morita equivalence.

    Returns the same pair as ``compare_theory_presentations`` for compatibility.
    Neither Boolean outcome proves or rules out equivalence.
    """
    warnings.warn("check_morita_equivalence only compares presentations; use "
                  "compare_theory_presentations", DeprecationWarning, stacklevel=2)
    return compare_theory_presentations(topos1, topos2)


def build_typological_theory(
    category: CaseCategory,
    alignment_name: str = "typological",
) -> GeometricTheory:
    """Build a geometric theory from a case category (typological formalization).

    Objects become sorts, morphisms become relation symbols, and
    categorical axioms (identity, composition) become geometric axioms.

    Args:
        category: A CaseCategory to formalize.
        alignment_name: Name for the alignment constraint axioms.

    Returns:
        The corresponding geometric theory.
    """
    theory = GeometricTheory(
        name=f"T_{alignment_name}",
        theory_type=TheoryType.TYPOLOGICAL,
    )

    # Add sorts from objects (CaseRole enum members)
    for role in sorted(category.objects, key=lambda r: r.name):
        theory.add_sort(role.name)

    # Add relation symbols from morphisms
    for morph in category.morphisms:
        theory.add_relation(morph.label, (morph.source.name, morph.target.name))

    # Add identity axiom
    theory.add_axiom(Axiom(
        name="identity",
        antecedent="x: CaseRole",
        consequent="∃ id_x: Hom(x, x)",
        sort_variables=["x"],
    ))

    # Add composition axiom
    theory.add_axiom(Axiom(
        name="composition",
        antecedent="f: Hom(A,B) ∧ g: Hom(B,C)",
        consequent="∃ g∘f: Hom(A,C)",
        sort_variables=["A", "B", "C"],
    ))

    logger.info(
        "Built typological theory %s: %d sorts, %d relations, %d axioms",
        theory.name, len(theory.sorts),
        len(theory.relation_symbols), len(theory.axioms),
    )
    return theory


def build_enriched_theory(
    enriched_cat: EnrichedCategory,
) -> GeometricTheory:
    """Build a geometric theory from an enriched case category.

    The enriched structure adds axioms for identity (hom(A,A)=1)
    and composition inequality.

    Args:
        enriched_cat: An EnrichedCategory.

    Returns:
        The corresponding geometric theory.
    """
    theory = GeometricTheory(
        name=f"T_enriched_{enriched_cat.name}",
        theory_type=TheoryType.ENRICHED,
    )

    # Add sorts from roles
    for role in enriched_cat.roles:
        theory.add_sort(role.name)

    # Add hom-value relation (binary) for significant connections
    for i, role_i in enumerate(enriched_cat.roles):
        for j, role_j in enumerate(enriched_cat.roles):
            if i != j and enriched_cat.proximity_matrix[i, j] > 0.1:
                theory.add_relation(
                    f"hom_{role_i.name}_{role_j.name}",
                    (role_i.name, role_j.name),
                )

    # Identity axiom
    theory.add_axiom(Axiom(
        name="enriched_identity",
        antecedent="x: CaseRole",
        consequent="hom(x, x) = 1",
        sort_variables=["x"],
    ))

    # Composition inequality
    theory.add_axiom(Axiom(
        name="composition_inequality",
        antecedent="hom(A,B) = p ∧ hom(B,C) = q",
        consequent="hom(A,C) ≥ p·q",
        sort_variables=["A", "B", "C"],
    ))

    logger.info(
        "Built enriched theory %s: %d sorts, %d relations, %d axioms",
        theory.name, len(theory.sorts),
        len(theory.relation_symbols), len(theory.axioms),
    )
    return theory


def bridge_transfer(
    source_topos: ClassifyingTopos,
    target_topos: ClassifyingTopos,
    property_name: str,
) -> dict[str, object]:
    """Report a requested transfer as unverified; no theorem prover is present.

    Profile matching is exposed for inspection, but never authorizes transfer.
    ``morita_equivalent=None`` means unknown, not disproven.
    """
    match, mismatches = compare_theory_presentations(source_topos, target_topos)
    return {
        "property": property_name,
        "source_theory": source_topos.theory.name,
        "target_theory": target_topos.theory.name,
        "presentation_match": match,
        "morita_equivalent": None,
        "transfer_possible": False,
        "necessary_conditions_only": False,
        "status": "unverified",
        "reason": "No equivalence witness or property translation has been provided",
        "mismatches": mismatches,
    }
