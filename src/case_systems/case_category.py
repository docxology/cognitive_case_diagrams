"""Case category formalization for linguistic case systems.

Implements the categorical structure underlying grammatical case:
- Objects: case roles (NOM, ACC, GEN, DAT, INS, LOC, ABL, VOC)
- Morphisms: grammatical relations (acts_on, receives, etc.)
- Composition: chaining of relational dependencies
- Alignment: functorial mappings between typological systems

References:
    Polinsky & Preminger (2015) — Case and Grammatical Relations
    Dowty (1991) — Thematic proto-roles and argument selection
    Fillmore (1968) — The Case for Case
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class CaseRole(Enum):
    """Linguistic case roles as category objects.

    The standard 8-case system covers the major morphological categories
    attested across typologically diverse languages.
    """

    NOM = "Nominative"
    ACC = "Accusative"
    GEN = "Genitive"
    DAT = "Dative"
    INS = "Instrumental"
    LOC = "Locative"
    ABL = "Ablative"
    VOC = "Vocative"

    # Alignment-specific roles (following Dixon/Comrie notation)
    ERG = "Ergative"
    ABS = "Absolutive"

    # Core argument roles (pre-alignment primitives)
    S = "Sole"      # Sole argument of intransitive
    A = "Agent"     # Agent-like argument of transitive
    P = "Patient"   # Patient-like argument of transitive


_FLOAT_TOLERANCE: float = 1e-9


@dataclass(frozen=True)
class Morphism:
    """A morphism in the case category representing a grammatical relation.

    Attributes:
        source: The source case role.
        target: The target case role.
        label: Human-readable label for the relation.
        weight: Enriched weight in [0,1] encoding proto-role satisfaction.
    """

    source: CaseRole
    target: CaseRole
    label: str
    weight: float = 1.0

    def __post_init__(self) -> None:
        if not (0.0 <= self.weight <= 1.0):
            raise ValueError(
                f"Morphism weight must be in [0,1], got {self.weight} "
                f"for '{self.label}' ({self.source.name} → {self.target.name})"
            )

    def __repr__(self) -> str:
        return f"{self.source.name} --{self.label}(w={self.weight:.2f})--> {self.target.name}"


@dataclass
class CaseCategory:
    """A category of case roles and grammatical relations.

    Implements the categorical axioms:
    - Identity morphisms for each object
    - Associative composition of morphisms
    - Commutativity constraint for consistent relational assignments

    Attributes:
        name: Name of the case system.
        objects: Set of case roles (objects of the category).
        morphisms: List of morphisms (arrows of the category).
    """

    name: str
    objects: set[CaseRole] = field(default_factory=set)
    morphisms: list[Morphism] = field(default_factory=list)

    def add_role(self, role: CaseRole) -> None:
        """Add a case role as an object in the category."""
        self.objects.add(role)
        logger.debug("Added role %s to category %s", role.name, self.name)

    def add_morphism(self, morphism: Morphism) -> None:
        """Add a grammatical relation as a morphism.

        Raises:
            ValueError: If source or target role not in category objects.
        """
        if morphism.source not in self.objects:
            raise ValueError(
                f"Source role {morphism.source.name} not in category {self.name}"
            ) from None
        if morphism.target not in self.objects:
            raise ValueError(
                f"Target role {morphism.target.name} not in category {self.name}"
            ) from None
        self.morphisms.append(morphism)
        logger.debug("Added morphism %s to category %s", morphism, self.name)

    def identity(self, role: CaseRole) -> Morphism:
        """Return the identity morphism for a case role.

        Raises:
            ValueError: If role not in category objects.
        """
        if role not in self.objects:
            raise ValueError(
                f"Role {role.name} not in category {self.name}"
            ) from None
        return Morphism(source=role, target=role, label="id", weight=1.0)

    def compose(self, f: Morphism, g: Morphism) -> Morphism:
        """Compose two morphisms: g ∘ f.

        Requires f.target == g.source (standard categorical composition).
        Enriched weights multiply: ``w(g ∘ f) = w(f) · w(g)`` (manuscript §4–5,
        multiplicative composition over ``[0,1]``).

        Args:
            f: First morphism (applied first).
            g: Second morphism (applied second).

        Returns:
            Composed morphism from f.source to g.target.

        Raises:
            ValueError: If morphisms are not composable.
        """
        if f.target != g.source:
            raise ValueError(
                f"Cannot compose: {f.target.name} != {g.source.name}"
            ) from None
        composed_label = f"{g.label} ∘ {f.label}"
        w = f.weight * g.weight
        result = Morphism(
            source=f.source, target=g.target, label=composed_label, weight=w
        )
        logger.debug("Composed %s and %s -> %s", f, g, result)
        return result

    def get_morphisms_from(self, role: CaseRole) -> list[Morphism]:
        """Return all morphisms originating from a given role."""
        return [m for m in self.morphisms if m.source == role]

    def get_morphisms_to(self, role: CaseRole) -> list[Morphism]:
        """Return all morphisms targeting a given role."""
        return [m for m in self.morphisms if m.target == role]

    def associativity_holds(self, *, weight_tolerance: float | None = None) -> bool:
        """Verify that composition is associative: h ∘ (g ∘ f) = (h ∘ g) ∘ f.

        Tests all composable triples of morphisms.

        Args:
            weight_tolerance: Absolute tolerance on the weight-comparison
                ``|w(h∘(g∘f)) - w((h∘g)∘f)| < tol``. Defaults to the
                module-level ``_FLOAT_TOLERANCE`` (1e-9). Loosen this when
                checking associativity on user-supplied noisy weights.

        Returns:
            True if associativity holds for all composable triples.
        """
        tol = _FLOAT_TOLERANCE if weight_tolerance is None else float(weight_tolerance)
        if tol <= 0:
            raise ValueError(f"weight_tolerance must be > 0, got {tol}")
        for f in self.morphisms:
            for g in self.morphisms:
                if f.target != g.source:
                    continue
                for h in self.morphisms:
                    if g.target != h.source:
                        continue
                    # h ∘ (g ∘ f)
                    gf = self.compose(f, g)
                    left = self.compose(gf, h)
                    # (h ∘ g) ∘ f
                    hg = self.compose(g, h)
                    right = self.compose(f, hg)
                    # Check source, target, and weight match
                    if left.source != right.source or left.target != right.target:
                        logger.warning(
                            "Associativity fails (endpoints): %s vs %s", left, right
                        )
                        return False
                    if not (abs(left.weight - right.weight) < tol):
                        logger.warning(
                            "Associativity fails (weights): %.9f vs %.9f (tol=%.1e)",
                            left.weight, right.weight, tol,
                        )
                        return False
        logger.info("Associativity verified for category %s (tol=%.1e)", self.name, tol)
        return True

    def is_well_formed(self) -> bool:
        """Full categorical axiom check.

        Verifies:
            1. Identity morphisms exist for all objects
            2. Composition is associative
            3. Identity is unit for composition

        Returns:
            True if all categorical axioms hold.
        """
        # Check identity morphisms exist
        for role in self.objects:
            try:
                id_m = self.identity(role)
                if id_m.source != role or id_m.target != role:
                    return False
            except ValueError:
                return False

        # Check associativity
        if not self.associativity_holds():
            return False

        # Check identity is unit: id ∘ f = f and f ∘ id = f
        for f in self.morphisms:
            id_src = self.identity(f.source)
            id_tgt = self.identity(f.target)
            left_unit = self.compose(id_src, f)
            right_unit = self.compose(f, id_tgt)
            if (left_unit.source != f.source or left_unit.target != f.target):
                return False
            if (right_unit.source != f.source or right_unit.target != f.target):
                return False

        logger.info("Category %s is well-formed", self.name)
        return True

    def assess_daif_surprisal(self, observed: Morphism, predicted_weight: float) -> dict[str, float]:
        """Assess DAIF Distributional Prediction Error (DPE) (cf. §7c).
        
        Following Li et al. (2024) and Rabovsky et al. (2025):
        - N400 (heuristic semantic surprise) tracks distance between predicted vs observed scalar enriched weights.
        - P600 (structural geometric discrepancy) triggers forcefully upon foundational topology failure.
        
        Args:
            observed: The observed linguistic relation pattern.
            predicted_weight: The Bayesian prior weight expectation.
            
        Returns: 
            Dictionary of N400 and P600 simulated amplitudes.
        """
        n400_semantic_surprise = abs(predicted_weight - observed.weight)
        
        # P600 triggers geometrically if the fundamental morphism isn't structurally licensed
        structurally_licensed = any(
            m.source == observed.source and m.target == observed.target 
            for m in self.morphisms
        )
        p600_structural_discrepancy = 0.0 if structurally_licensed else 1.0
        
        return {
            "N400_amplitude": n400_semantic_surprise,
            "P600_amplitude": p600_structural_discrepancy
        }


def standard_case_category() -> CaseCategory:
    """Create the standard 8-case category with canonical morphisms.

    Returns a category with NOM, ACC, GEN, DAT, INS, LOC, ABL, VOC
    and the standard grammatical relations between them.
    """
    cat = CaseCategory(name="Standard8Case")
    standard_roles = [
        CaseRole.NOM, CaseRole.ACC, CaseRole.GEN, CaseRole.DAT,
        CaseRole.INS, CaseRole.LOC, CaseRole.ABL, CaseRole.VOC,
    ]
    for role in standard_roles:
        cat.add_role(role)

    # Core transitive relations
    cat.add_morphism(Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on"))
    cat.add_morphism(Morphism(CaseRole.NOM, CaseRole.DAT, "transfers_to"))
    cat.add_morphism(Morphism(CaseRole.ACC, CaseRole.DAT, "received_by"))
    cat.add_morphism(Morphism(CaseRole.NOM, CaseRole.INS, "uses"))
    cat.add_morphism(Morphism(CaseRole.NOM, CaseRole.LOC, "located_at"))
    cat.add_morphism(Morphism(CaseRole.ACC, CaseRole.ABL, "moves_from"))
    cat.add_morphism(Morphism(CaseRole.GEN, CaseRole.NOM, "possesses"))
    cat.add_morphism(Morphism(CaseRole.NOM, CaseRole.VOC, "addresses"))

    logger.info("Created standard 8-case category with %d morphisms", len(cat.morphisms))
    return cat


def minimal_case_category() -> CaseCategory:
    """Create a minimal 3-role transitive case category.

    Agent (NOM), Patient (ACC), Instrument (INS) — illustrating
    basic transitive action structure.
    """
    cat = CaseCategory(name="MinimalTransitive")
    for role in [CaseRole.NOM, CaseRole.ACC, CaseRole.INS]:
        cat.add_role(role)
    cat.add_morphism(Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on"))
    cat.add_morphism(Morphism(CaseRole.NOM, CaseRole.INS, "uses"))
    cat.add_morphism(Morphism(CaseRole.INS, CaseRole.ACC, "applied_to"))
    logger.info("Created minimal transitive case category")
    return cat


def introductory_case_category() -> CaseCategory:
    """Case category for the introduction figure (fig:case-minimal).

    Extends the minimal NOM--INS--ACC transitive triangle with VOC so that
    structurally prohibited morphisms (e.g. VOC→NOM) can be drawn alongside
    licensed edges. Weights on the triangle match the manuscript: legs with
    w=0.9 and w=0.7 compose multiplicatively to 0.63 (see §4–5 enriched
    composition). Theory code should keep using ``minimal_case_category()``.

    Returns:
        Category with objects NOM, ACC, INS, VOC and four licensed morphisms.
    """
    cat = CaseCategory(name="IntroductoryFigure")
    for role in [CaseRole.NOM, CaseRole.ACC, CaseRole.INS, CaseRole.VOC]:
        cat.add_role(role)
    cat.add_morphism(
        Morphism(CaseRole.NOM, CaseRole.ACC, "acts_on", weight=0.63)
    )
    cat.add_morphism(
        Morphism(CaseRole.NOM, CaseRole.INS, "uses", weight=0.9)
    )
    cat.add_morphism(
        Morphism(CaseRole.INS, CaseRole.ACC, "applied_to", weight=0.7)
    )
    cat.add_morphism(
        Morphism(CaseRole.NOM, CaseRole.VOC, "addresses", weight=0.85)
    )
    logger.info("Created introductory case category for manuscript figure")
    return cat


def accusative_alignment() -> dict[CaseRole, CaseRole]:
    """Nominative-Accusative alignment: {S,A} → NOM, P → ACC."""
    return {
        CaseRole.S: CaseRole.NOM,
        CaseRole.A: CaseRole.NOM,
        CaseRole.P: CaseRole.ACC,
    }


def ergative_alignment() -> dict[CaseRole, CaseRole]:
    """Ergative-Absolutive alignment: {S,P} → ABS, A → ERG."""
    return {
        CaseRole.S: CaseRole.ABS,
        CaseRole.P: CaseRole.ABS,
        CaseRole.A: CaseRole.ERG,
    }


def tripartite_alignment() -> dict[CaseRole, CaseRole]:
    """Tripartite alignment: S → ABS, A → ERG, P → ACC (injective)."""
    return {
        CaseRole.S: CaseRole.ABS,
        CaseRole.A: CaseRole.ERG,
        CaseRole.P: CaseRole.ACC,
    }


def active_stative_alignment() -> dict[str, dict[CaseRole, CaseRole]]:
    """Active-Stative alignment: S splits by agentivity.

    In active-stative (split-S) languages, the intransitive subject's
    case depends on whether the predicate is active (agentive) or
    stative (non-agentive):
        S_active → ERG (like A)
        S_stative → ABS (like P)

    Returns:
        Dictionary with 'active' and 'stative' alignment mappings.
    """
    return {
        "active": {
            CaseRole.S: CaseRole.ERG,
            CaseRole.A: CaseRole.ERG,
            CaseRole.P: CaseRole.ABS,
        },
        "stative": {
            CaseRole.S: CaseRole.ABS,
            CaseRole.A: CaseRole.ERG,
            CaseRole.P: CaseRole.ABS,
        },
    }
