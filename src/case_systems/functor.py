"""Alignment functors between case categories.

Implements functors that map between typological alignment systems,
preserving categorical structure while reshaping the morphism pattern.
For example, mapping an Accusative system to an Ergative system.

References:
    Polinsky & Preminger (2015) — Case and Grammatical Relations
    Claassen (2025) — Typology of grammatical relations
"""

import logging
from dataclasses import dataclass, field

from .case_category import (
    CaseCategory,
    CaseRole,
    Morphism,
    accusative_alignment,
    ergative_alignment,
    tripartite_alignment,
)

logger = logging.getLogger(__name__)


@dataclass
class AlignmentFunctor:
    """A functor F: C → D mapping between case categories.

    Maps objects (case roles) and morphisms (grammatical relations)
    from a source alignment system to a target alignment system,
    preserving composition and identities.

    Attributes:
        name: Descriptive name of the functor.
        source: Source case category.
        target: Target case category.
        object_map: Mapping from source roles to target roles.
    """

    name: str
    source: CaseCategory
    target: CaseCategory
    object_map: dict[CaseRole, CaseRole] = field(default_factory=dict)

    def map_object(self, role: CaseRole) -> CaseRole:
        """Apply the functor to an object (case role).

        Args:
            role: Source case role.

        Returns:
            Target case role F(role).

        Raises:
            KeyError: If role has no mapping defined.
        """
        if role not in self.object_map:
            raise KeyError(
                f"No mapping defined for {role.name} in functor {self.name}"
            ) from None
        return self.object_map[role]

    def map_morphism(self, morphism: Morphism) -> Morphism:
        """Apply the functor to a morphism.

        F(f: A → B) = F(f): F(A) → F(B)

        Args:
            morphism: Source morphism.

        Returns:
            Target morphism with mapped source and target.
        """
        mapped_source = self.map_object(morphism.source)
        mapped_target = self.map_object(morphism.target)
        return Morphism(
            source=mapped_source,
            target=mapped_target,
            label=f"F({morphism.label})",
        )

    def preserves_identity(self, role: CaseRole) -> bool:
        """Check that F(id_A) = id_{F(A)}.

        Returns:
            True if the functor preserves the identity morphism for role.
        """
        source_id = self.source.identity(role)
        mapped_id = self.map_morphism(source_id)
        target_id = self.target.identity(self.map_object(role))
        preserves = (
            mapped_id.source == target_id.source
            and mapped_id.target == target_id.target
        )
        if not preserves:
            logger.warning(
                "Identity not preserved for %s in functor %s",
                role.name, self.name,
            )
        return preserves

    def preserves_composition(self, f: Morphism, g: Morphism) -> bool:
        """Check that F(g ∘ f) = F(g) ∘ F(f).

        Args:
            f: First morphism.
            g: Second morphism (composable with f).

        Returns:
            True if composition is preserved.
        """
        composed_then_mapped = self.map_morphism(self.source.compose(f, g))
        mapped_then_composed = self.target.compose(
            self.map_morphism(f), self.map_morphism(g)
        )
        preserves = (
            composed_then_mapped.source == mapped_then_composed.source
            and composed_then_mapped.target == mapped_then_composed.target
        )
        if not preserves:
            logger.warning(
                "Composition not preserved for (%s, %s) in functor %s",
                f, g, self.name,
            )
        return preserves

    def is_injective(self) -> bool:
        """Check if the object map is injective (no neutralization).

        Tripartite alignment is injective; Accusative and Ergative are not.
        """
        values = list(self.object_map.values())
        return len(values) == len(set(values))

    def image_roles(self) -> set[CaseRole]:
        """Return the set of target roles in the image of the functor."""
        return set(self.object_map.values())


def accusative_to_ergative_functor() -> AlignmentFunctor:
    """Create a functor from Accusative to Ergative alignment.

    Maps the core argument roles through their respective alignment
    systems to show how S, A, P are grouped differently.
    """
    # Source: Accusative category (S,A → NOM; P → ACC)
    source = CaseCategory(name="AccusativeSystem")
    for role in [CaseRole.S, CaseRole.A, CaseRole.P, CaseRole.NOM, CaseRole.ACC]:
        source.add_role(role)

    # Target: Ergative category (S,P → ABS; A → ERG)
    target = CaseCategory(name="ErgativeSystem")
    for role in [CaseRole.S, CaseRole.A, CaseRole.P, CaseRole.ERG, CaseRole.ABS]:
        target.add_role(role)

    # The functor maps alignment roles, demonstrating neutralization
    # In Accusative: S and A map to NOM. In the functor, we keep core roles
    # the same but map the surface cases showing neutralization.
    # NOM covers both S and A (non-injective), ACC covers P only.
    # In target: ERG covers A only, ABS covers both S and P.
    object_map = {
        CaseRole.S: CaseRole.ABS,    # S → ABS (same as P)
        CaseRole.A: CaseRole.ERG,    # A → ERG (unique)
        CaseRole.P: CaseRole.ABS,    # P → ABS (same as S, non-injective!)
        CaseRole.NOM: CaseRole.ERG,  # Surface NOM → ERG
        CaseRole.ACC: CaseRole.ABS,  # Surface ACC → ABS
    }

    functor = AlignmentFunctor(
        name="Acc→Erg",
        source=source,
        target=target,
        object_map=object_map,
    )
    logger.info("Created accusative-to-ergative functor")
    return functor


def tripartite_functor() -> AlignmentFunctor:
    """Create the tripartite alignment functor (injective).

    S → ABS, A → ERG, P → ACC — no neutralization.
    """
    source = CaseCategory(name="CoreArgs")
    target = CaseCategory(name="TripartiteSystem")
    for role in [CaseRole.S, CaseRole.A, CaseRole.P]:
        source.add_role(role)
    for role in [CaseRole.ABS, CaseRole.ERG, CaseRole.ACC]:
        target.add_role(role)

    tri = tripartite_alignment()
    functor = AlignmentFunctor(
        name="Tripartite",
        source=source,
        target=target,
        object_map=tri,
    )
    logger.info("Created tripartite functor (injective=%s)", functor.is_injective())
    return functor
