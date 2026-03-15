"""Natural transformations between alignment functors.

Implements natural transformations α: F ⇒ G between alignment functors,
providing the categorical infrastructure for comparing different
cross-linguistic alignment mappings.

A natural transformation consists of component morphisms α_A: F(A) → G(A)
for each object A, satisfying the naturality condition:
    G(f) ∘ α_A = α_B ∘ F(f)
for every morphism f: A → B.

References:
    Mac Lane (1971) — Categories for the Working Mathematician
    Caramello (2016) — Theories, Sites, Toposes
"""

import logging
from dataclasses import dataclass, field

from .case_category import CaseRole, Morphism, CaseCategory
from .functor import AlignmentFunctor

logger = logging.getLogger(__name__)


@dataclass
class ComponentMorphism:
    """A component morphism α_A: F(A) → G(A) of a natural transformation.

    Attributes:
        object_name: The object A this component is defined on.
        source_image: F(A) — image of A under source functor.
        target_image: G(A) — image of A under target functor.
    """

    object_name: CaseRole
    source_image: CaseRole
    target_image: CaseRole

    def as_morphism(self) -> Morphism:
        """Return the corresponding morphism F(A) → G(A)."""
        return Morphism(
            source=self.source_image,
            target=self.target_image,
            label=f"α_{self.object_name.name}",
        )


@dataclass
class NaturalTransformation:
    """A natural transformation α: F ⇒ G between alignment functors.

    Attributes:
        name: Descriptive name for this transformation.
        source_functor: The source functor F.
        target_functor: The target functor G.
        components: Mapping from each CaseRole to its ComponentMorphism.
    """

    name: str
    source_functor: AlignmentFunctor
    target_functor: AlignmentFunctor
    components: dict[CaseRole, ComponentMorphism] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate that source and target functors share source categories."""
        if (self.source_functor.source.name !=
                self.target_functor.source.name):
            logger.warning(
                "Source functors have different source categories: %s vs %s",
                self.source_functor.source.name,
                self.target_functor.source.name,
            )

    def set_component(self, role: CaseRole, component: ComponentMorphism) -> None:
        """Set the component morphism α_A for object A.

        Args:
            role: The case role (object) this component is for.
            component: The component morphism data.

        Raises:
            ValueError: If role is not in the source functor's object map.
        """
        if role not in self.source_functor.object_map:
            raise ValueError(
                f"Role {role.name} not in source functor's object map"
            )
        if role not in self.target_functor.object_map:
            raise ValueError(
                f"Role {role.name} not in target functor's object map"
            )

        f_image = self.source_functor.object_map[role]
        g_image = self.target_functor.object_map[role]

        if component.source_image != f_image:
            raise ValueError(
                f"Component source {component.source_image.name} != "
                f"F({role.name}) = {f_image.name}"
            )
        if component.target_image != g_image:
            raise ValueError(
                f"Component target {component.target_image.name} != "
                f"G({role.name}) = {g_image.name}"
            )

        self.components[role] = component
        logger.debug(
            "Set component α_%s: %s → %s",
            role.name, f_image.name, g_image.name,
        )

    def is_complete(self) -> bool:
        """Check if components are defined for all objects in the source category.

        Returns:
            True if every object in the shared source category has a component.
        """
        source_objects = set(self.source_functor.object_map.keys())
        defined = set(self.components.keys())
        complete = source_objects <= defined
        if not complete:
            missing = {r.name for r in source_objects - defined}
            logger.warning(
                "Natural transformation %s missing components for: %s",
                self.name, missing,
            )
        return complete

    def component_morphisms(self) -> list[Morphism]:
        """Return all component morphisms as a list.

        Returns:
            List of Morphism objects representing each component.
        """
        return [comp.as_morphism() for comp in self.components.values()]

    def image_roles(self) -> set[CaseRole]:
        """Return the set of all target images in the components."""
        return {comp.target_image for comp in self.components.values()}


@dataclass
class IdentityNaturalTransformation(NaturalTransformation):
    """The identity natural transformation id_F: F ⇒ F.

    Each component α_A is the identity morphism on F(A).
    """

    def __init__(self, functor: AlignmentFunctor) -> None:
        """Create the identity natural transformation on a functor.

        Args:
            functor: The functor F for which id_F is constructed.
        """
        super().__init__(
            name=f"id_{functor.name}",
            source_functor=functor,
            target_functor=functor,
        )
        # Set identity components for every object in the functor
        for role, image in functor.object_map.items():
            self.components[role] = ComponentMorphism(
                object_name=role,
                source_image=image,
                target_image=image,
            )
        logger.info("Created identity natural transformation on %s", functor.name)


def compose_transformations(
    alpha: NaturalTransformation,
    beta: NaturalTransformation,
) -> NaturalTransformation:
    """Vertical composition of natural transformations: β ∘ α: F ⇒ H.

    Given α: F ⇒ G and β: G ⇒ H, the composite (β ∘ α)_A = β_A ∘ α_A.

    Args:
        alpha: Natural transformation F ⇒ G.
        beta: Natural transformation G ⇒ H.

    Returns:
        The composite natural transformation F ⇒ H.

    Raises:
        ValueError: If alpha's target functor differs from beta's source functor.
    """
    if alpha.target_functor.name != beta.source_functor.name:
        raise ValueError(
            f"Cannot compose: α target functor ({alpha.target_functor.name}) "
            f"!= β source functor ({beta.source_functor.name})"
        )

    composite = NaturalTransformation(
        name=f"{beta.name}∘{alpha.name}",
        source_functor=alpha.source_functor,
        target_functor=beta.target_functor,
    )

    for role in alpha.components:
        if role in beta.components:
            alpha_comp = alpha.components[role]
            beta_comp = beta.components[role]
            composite.components[role] = ComponentMorphism(
                object_name=role,
                source_image=alpha_comp.source_image,
                target_image=beta_comp.target_image,
            )

    logger.info(
        "Composed natural transformations: %s ∘ %s → %s",
        beta.name, alpha.name, composite.name,
    )
    return composite
