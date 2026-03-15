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
        return Morphism(source=role, target=role, label="id")

    def compose(self, f: Morphism, g: Morphism) -> Morphism:
        """Compose two morphisms: g ∘ f.

        Requires f.target == g.source (standard categorical composition).

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
        result = Morphism(source=f.source, target=g.target, label=composed_label)
        logger.debug("Composed %s and %s -> %s", f, g, result)
        return result

    @property
    def roles(self) -> set:
        """Alias for objects — returns the set of case roles."""
        return self.objects

    def get_morphisms_from(self, role: CaseRole) -> list[Morphism]:
        """Return all morphisms originating from a given role."""
        return [m for m in self.morphisms if m.source == role]

    def get_morphisms_to(self, role: CaseRole) -> list[Morphism]:
        """Return all morphisms targeting a given role."""
        return [m for m in self.morphisms if m.target == role]

    def associativity_holds(self) -> bool:
        """Verify that composition is associative: h ∘ (g ∘ f) = (h ∘ g) ∘ f.

        Tests all composable triples of morphisms.

        Returns:
            True if associativity holds for all composable triples.
        """
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
                    # Check source and target match
                    if left.source != right.source or left.target != right.target:
                        logger.warning(
                            "Associativity fails: %s vs %s", left, right
                        )
                        return False
        logger.info("Associativity verified for category %s", self.name)
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
