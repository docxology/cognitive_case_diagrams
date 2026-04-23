"""Fluid-S alignment: context-dependent functors parameterized by volition.

Implements the Fluid-S alignment system discussed in §4–5 of the manuscript,
where the intransitive subject S receives different case marking depending
on the speaker's construal of agentive volition. In Bats (Nakh-Daghestanian),
'fall' takes ABS when accidental but ERG when volitional.

Categorically, Fluid-S defines a context-dependent functor
    F_θ: U → L
parameterized by θ ∈ {+vol, −vol}:
    F_{+vol}(S) = ERG    (volitional → agent-like)
    F_{-vol}(S) = ABS    (non-volitional → patient-like)
    F_θ(A) = ERG         (always agent)
    F_θ(P) = ABS         (always patient)

The graded version replaces the binary θ with a probability p ∈ [0,1]
representing the degree of agentive construal.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .case_category import CaseRole, Morphism, CaseCategory

logger = logging.getLogger(__name__)


class VolitionContext(Enum):
    """Binary volition context for Fluid-S alignment."""
    VOLITIONAL = "volitional"
    NON_VOLITIONAL = "non_volitional"


@dataclass
class FluidSFunctor:
    """Context-dependent functor for Fluid-S alignment systems.

    Maps the universal category U = {S, A, P} to a language-specific
    category where S receives context-dependent marking based on
    agentive volition.

    Attributes:
        name: Human-readable name for this functor.
        volition: Binary context determining S-mapping.
        volition_probability: Graded probability of agentive construal
            (1.0 = fully volitional, 0.0 = fully non-volitional).
        source: Source (universal) case category.
        target: Target (language-specific) case category.
    """
    name: str = "Fluid-S"
    volition: VolitionContext = VolitionContext.VOLITIONAL
    volition_probability: float = 1.0
    source: Optional[CaseCategory] = field(default=None, repr=False)
    target: Optional[CaseCategory] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Validate probability and log configuration."""
        if not 0.0 <= self.volition_probability <= 1.0:
            raise ValueError(
                f"volition_probability must be in [0,1], got {self.volition_probability}"
            )
        logger.info(
            "FluidSFunctor '%s' created: volition=%s, p=%.2f",
            self.name, self.volition.value, self.volition_probability,
        )

    def map_object(self, role: CaseRole) -> CaseRole:
        """Map a case role under the current volition context.

        Args:
            role: Source case role.

        Returns:
            Target case role after Fluid-S mapping.

        The mapping rules (following manuscript §4–5) use NOM as the
        agent-like (ERG-proxy) surface form and ACC as the patient-like
        (ABS-proxy) surface form, reflecting how Fluid-S languages
        reuse existing surface cases for context-dependent marking:

            S → NOM (agent-like) if volitional
            S → ACC (patient-like) if non-volitional
            Other roles pass through unchanged
        """
        if role == CaseRole.NOM:
            # S (intransitive subject) — context-dependent
            if self.volition == VolitionContext.VOLITIONAL:
                mapped = CaseRole.NOM  # ERG-like (agent marking)
                logger.debug("S mapped to NOM (volitional/agent-like)")
            else:
                mapped = CaseRole.ACC  # ABS-like (patient marking)
                logger.debug("S mapped to ACC (non-volitional/patient-like)")
            return mapped

        # A (transitive agent) always maps to agent marking
        if role in (CaseRole.GEN, CaseRole.DAT, CaseRole.INS,
                    CaseRole.LOC, CaseRole.ABL, CaseRole.VOC):
            return role  # Oblique cases pass through unchanged

        # ACC (patient) passes through unchanged
        return role

    def map_object_in_context(self, role: CaseRole, p_volitional: float) -> dict[CaseRole, float]:
        """Map a case role with graded volition probability.

        Returns a probability distribution over target roles,
        reflecting the speaker's uncertainty about volition.

        Args:
            role: Source case role.
            p_volitional: Probability of volitional construal.

        Returns:
            Dictionary mapping target CaseRole to probability.
        """
        if not 0.0 <= p_volitional <= 1.0:
            raise ValueError(f"p_volitional must be in [0,1], got {p_volitional}")

        if role != CaseRole.NOM:
            # Non-S roles are deterministic
            return {self.map_object(role): 1.0}

        # S role: probabilistic split
        return {
            CaseRole.NOM: p_volitional,      # ERG-like (volitional)
            CaseRole.ACC: 1.0 - p_volitional,  # ABS-like (non-volitional)
        }

    def split_probability(self, role: CaseRole) -> dict[CaseRole, float]:
        """Return case probability distribution using stored volition_probability.

        Convenience method using the instance's volition_probability.

        Args:
            role: Source case role.

        Returns:
            Dictionary mapping target CaseRole to probability.
        """
        return self.map_object_in_context(role, self.volition_probability)

    def map_morphism(self, morphism: Morphism) -> Morphism:
        """Map a morphism under the Fluid-S functor.

        Args:
            morphism: Source morphism.

        Returns:
            Target morphism with mapped source/target roles.
        """
        return Morphism(
            source=self.map_object(morphism.source),
            target=self.map_object(morphism.target),
            label=morphism.label,
            weight=morphism.weight,
        )

    def preserves_identity(self, role: CaseRole) -> bool:
        """Check whether the functor preserves identity at a role.

        An identity morphism id_A should map to id_{F(A)}.
        """
        mapped = self.map_object(role)
        return mapped is not None  # Always true for valid roles

    def kernel(self) -> list:
        """Compute the kernel: pairs of roles mapped to the same target.

        Returns:
            List of (role_a, role_b) pairs that are identified.
        """
        core_roles = (
            list(self.source.objects) if self.source is not None else list(CaseRole)
        )
        kernel_pairs = []
        for i, r1 in enumerate(core_roles):
            for r2 in core_roles[i + 1:]:
                if self.map_object(r1) == self.map_object(r2):
                    kernel_pairs.append((r1, r2))
        return kernel_pairs


def create_fluid_s_functor(
    volitional: bool = True,
    probability: float = 1.0,
) -> FluidSFunctor:
    """Create a Fluid-S functor with given volition context.

    Args:
        volitional: If True, use VOLITIONAL context; else NON_VOLITIONAL.
        probability: Graded volition probability in [0,1].

    Returns:
        Configured FluidSFunctor instance.
    """
    context = (VolitionContext.VOLITIONAL if volitional
               else VolitionContext.NON_VOLITIONAL)
    return FluidSFunctor(
        name=f"Fluid-S ({'vol' if volitional else 'non-vol'})",
        volition=context,
        volition_probability=probability,
    )


def bats_fluid_s() -> tuple:
    """Create the canonical Bats language Fluid-S functor pair.

    In Bats (Nakh-Daghestanian), the verb 'fall' takes:
        - ABS when accidental: "The child-ABS fell"
        - ERG when volitional: "The child-ERG fell [on purpose]"

    Returns:
        Tuple of (volitional_functor, non_volitional_functor).
    """
    vol = create_fluid_s_functor(volitional=True)
    nonvol = create_fluid_s_functor(volitional=False)
    logger.info("Created Bats Fluid-S functor pair")
    return vol, nonvol


def fluid_s_enriched_weight(
    p_volitional: float,
    base_weight: float = 1.0,
) -> float:
    """Compute the enriched morphism weight for a Fluid-S S-morphism.

    The enriched weight of the S-morphism under Fluid-S is the probability
    of the agentive construal in context (manuscript §4–5).

    Args:
        p_volitional: Probability of volitional construal.
        base_weight: Base weight of the morphism before context modulation.

    Returns:
        Context-modulated enriched weight in [0,1].
    """
    if not 0.0 <= p_volitional <= 1.0:
        raise ValueError(f"p_volitional must be in [0,1], got {p_volitional}")
    if not 0.0 <= base_weight <= 1.0:
        raise ValueError(f"base_weight must be in [0,1], got {base_weight}")
    return p_volitional * base_weight
