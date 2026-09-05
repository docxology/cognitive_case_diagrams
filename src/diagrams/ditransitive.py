"""Ditransitive sentence support with three-argument verbs.

Extends the string diagram framework with proper ditransitive support:
    - DitransitiveSentence: subject + verb + direct_obj + indirect_obj
    - DisCoPy integration for three-argument verb diagrams
    - Case assignment: NOM → ACC → DAT

Example: "Alice gave Bob a book"
    - Alice: NOM (agent)
    - book: ACC (theme)
    - Bob: DAT (recipient)
"""

import logging
from dataclasses import dataclass, field
from typing import Any

from ..case_systems.case_category import CaseRole
from .string_diagram import Wire, Box, Sentence, N, S

logger = logging.getLogger(__name__)


@dataclass
class DitransitiveSentence:
    """A sentence with a three-argument verb (subject + 2 objects).

    Extends the Sentence model for ditransitive constructions like
    "Alice gave Bob a book" where three NPs receive case marking:
        - Agent (NOM): Alice
        - Theme (ACC): a book
        - Recipient (DAT): Bob

    Attributes:
        subject: Agent noun phrase.
        verb: Ditransitive verb.
        direct_object: Theme/patient noun phrase.
        indirect_object: Recipient/goal noun phrase.
        sentence: Underlying Sentence object.
    """
    subject: str
    verb: str
    direct_object: str
    indirect_object: str
    sentence: Sentence = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Build the sentence structure with case assignments."""
        text = f"{self.subject} {self.verb} {self.indirect_object} {self.direct_object}"
        self.sentence = Sentence(text=text)

        # Add nouns with case assignments
        self.sentence.add_noun(self.subject, CaseRole.NOM)
        self.sentence.add_noun(self.indirect_object, CaseRole.DAT)
        self.sentence.add_noun(self.direct_object, CaseRole.ACC)

        # Add verb box
        subj_wire = Wire(wire_type=N, entity=self.subject, case_role=CaseRole.NOM)
        io_wire = Wire(wire_type=N, entity=self.indirect_object, case_role=CaseRole.DAT)
        do_wire = Wire(wire_type=N, entity=self.direct_object, case_role=CaseRole.ACC)
        sent_wire = Wire(wire_type=S)
        verb_box = Box(
            name=self.verb,
            dom=[subj_wire, io_wire, do_wire],
            cod=[sent_wire],
        )
        self.sentence.boxes.append(verb_box)

        logger.info(
            "DitransitiveSentence: '%s' (NOM=%s, DAT=%s, ACC=%s)",
            text, self.subject, self.indirect_object, self.direct_object,
        )

    @property
    def text(self) -> str:
        """Full text of the sentence."""
        return self.sentence.text

    @property
    def case_assignments(self) -> dict:
        """Dictionary of entity → CaseRole assignments."""
        return self.sentence.case_assignments

    @property
    def num_boxes(self) -> int:
        """Number of boxes (3 nouns + 1 verb = 4)."""
        return self.sentence.num_boxes

    @property
    def num_arguments(self) -> int:
        """Number of verb arguments (always 3 for ditransitive)."""
        return 3

    @property
    def codomain_type(self) -> str:
        """Codomain type of the sentence."""
        return self.sentence.codomain_type


def create_ditransitive(
    subject: str,
    verb: str,
    indirect_object: str,
    direct_object: str,
) -> DitransitiveSentence:
    """Factory function for creating a ditransitive sentence.

    Args:
        subject: Agent (NOM).
        verb: Ditransitive verb.
        indirect_object: Recipient (DAT).
        direct_object: Theme (ACC).

    Returns:
        DitransitiveSentence instance.
    """
    return DitransitiveSentence(
        subject=subject,
        verb=verb,
        direct_object=direct_object,
        indirect_object=indirect_object,
    )


def create_discopy_ditransitive(
    subject: str,
    verb: str,
    indirect_object: str,
    direct_object: str,
) -> Any:
    """Create a DisCoPy ditransitive diagram.

    Type structure:
        subject: n
        verb: n.r @ s @ n.l @ n.l
        indirect_object: n
        direct_object: n

    Requires discopy.

    Args:
        subject: Agent name.
        verb: Verb string.
        indirect_object: Recipient name.
        direct_object: Theme name.

    Returns:
        DisCoPy Diagram reducing to type 's'.
    """
    from discopy.rigid import Ty, Box as DBox, Cup, Id

    n = Ty('n')
    s = Ty('s')

    # Word boxes
    subj_box = DBox(subject, Ty(), n)
    verb_box = DBox(verb, Ty(), n.r @ s @ n.l @ n.l)
    io_box = DBox(indirect_object, Ty(), n)
    do_box = DBox(direct_object, Ty(), n)

    # Tensor product of all words
    words = subj_box @ verb_box @ io_box @ do_box

    # Contract: subject with verb's left adjoint
    cups = Cup(n, n.r) @ Id(s @ n.l @ n.l @ n @ n)
    # Contract: indirect object with verb's first right adjoint
    cups2 = Id(s @ n.l) @ Cup(n.l, n) @ Id(n)
    # Contract: direct object with verb's second right adjoint
    cups3 = Id(s) @ Cup(n.l, n)

    diagram = words >> cups >> cups2 >> cups3
    logger.info("DisCoPy ditransitive diagram: %s %s %s %s → s",
                subject, verb, indirect_object, direct_object)
    return diagram
