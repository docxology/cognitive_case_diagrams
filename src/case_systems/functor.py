"""Alignment functors between case categories.

Implements functors that map between typological alignment systems,
preserving categorical structure while reshaping the morphism pattern.
For example, mapping an Accusative system to an Ergative system.

References:
    Polinsky & Preminger (2015) — Case and Grammatical Relations
    Claassen (2025) — Typology of grammatical relations
"""
from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field

from .case_category import (
    CaseCategory,
    CaseRole,
    Morphism,
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
            weight=morphism.weight,
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
        struct_ok = (
            composed_then_mapped.source == mapped_then_composed.source
            and composed_then_mapped.target == mapped_then_composed.target
        )
        weight_ok = math.isclose(
            composed_then_mapped.weight,
            mapped_then_composed.weight,
            rel_tol=1e-9,
            abs_tol=1e-9,
        )
        preserves = struct_ok and weight_ok
        if not preserves:
            logger.warning(
                "Composition not preserved for (%s, %s) in functor %s "
                "(struct_ok=%s weight_ok=%s weights %s vs %s)",
                f,
                g,
                self.name,
                struct_ok,
                weight_ok,
                composed_then_mapped.weight,
                mapped_then_composed.weight,
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


@dataclass
class MonoidalFunctor(AlignmentFunctor):
    """Monoidal functor for tensor-preservation checks on case-alignment maps (cf. §9b).

    Under a **Categorical Communication Protocol**, non-cartesian tensor structure can be
    specified so that disallowed wire manipulations (e.g., merging roles that must stay
    distinct) are detectable. This class implements **specification-level** tensor checks
    aligned with the case-theoretic analysis of prompt injection in
    ``docs/manuscript/09b_cognitive_security.md``; it does **not** secure a deployed LLM API
    by itself. Multi-turn context attacks remain an open systems problem; see empirical
    motivation in adversarial LLM-agent work (e.g. ARLAS 2025, cited in §9b).

    Use :meth:`preserves_tensor` to test whether ``F`` preserves tensor structure for
    role pairs; collapsing distinct roles models the kind of illicit ACC/NOM merge
    discussed in §9b.
    """
    
    def preserves_tensor(self, role_a: CaseRole, role_b: CaseRole) -> bool:
        """Check that F(A ⊗ B) ≅ F(A) ⊗ F(B) for a pair of roles.

        Tensor preservation requires:
        1. Both roles are in the functor's domain.
        2. Distinct roles map to distinct images (no tensor collapse).
        3. If a morphism A→B exists in the source, F(A)→F(B) exists in the target.

        In pregroup grammars, wires cannot be arbitrarily copied or deleted.
        A tensor collapse (two distinct roles mapping to the same image)
        represents loss of structural information — e.g., an adversary
        merging ACC (data) with NOM (authority).

        Args:
            role_a: First role in the tensor product.
            role_b: Second role in the tensor product.

        Returns:
            True if tensor structure is preserved for this pair.
        """
        try:
            fa = self.map_object(role_a)
            fb = self.map_object(role_b)
        except KeyError:
            logger.warning(
                "Tensor preservation: unmapped role(s) %s, %s in functor %s",
                role_a.name, role_b.name, self.name,
            )
            return False

        # Distinct inputs mapping to the same output collapses tensor factors
        if role_a != role_b and fa == fb:
            logger.warning(
                "Tensor preservation fails: %s ⊗ %s collapses to %s ⊗ %s "
                "under functor %s — distinct roles merged",
                role_a.name, role_b.name, fa.name, fb.name, self.name,
            )
            return False

        # Check morphism structure is preserved between the pair
        source_morphisms = self.source.get_morphisms_from(role_a)
        for m in source_morphisms:
            if m.target == role_b:
                target_morphisms = self.target.get_morphisms_from(fa)
                if not any(tm.target == fb for tm in target_morphisms):
                    logger.warning(
                        "Tensor preservation fails: morphism %s→%s exists "
                        "but F(%s)→F(%s) missing in target under functor %s",
                        role_a.name, role_b.name,
                        fa.name, fb.name, self.name,
                    )
                    return False

        logger.debug(
            "Tensor %s ⊗ %s preserved under functor %s",
            role_a.name, role_b.name, self.name,
        )
        return True
