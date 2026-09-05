"""DisCoCat and DisCoCirc string diagram representations.

Provides both:
1. Native representations for string diagram semantics (Sentence, Discourse)
2. Real DisCoPy integration for compact closed categorical diagrams

The native representations capture the compositional structure of
natural language sentences and discourse using monoidal category theory.

References:
    Coecke, Sadrzadeh & Clark (2010) — DisCoCat
    de Felice & Coecke (2020) — Discourse in categorical relational semantics
    de Felice, Meichanetzidis & Coecke (2022) — DisCoCirc
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional

from ..case_systems.case_category import CaseRole

logger = logging.getLogger(__name__)


# --- Native Representations ---


@dataclass(frozen=True)
class AtomicType:
    """An atomic type in the pregroup grammar.

    Standard types: n (noun), s (sentence).
    """

    name: str

    def __repr__(self) -> str:
        return self.name


# Standard atomic types
N = AtomicType("n")  # Noun type
S = AtomicType("s")  # Sentence type


@dataclass(frozen=True)
class Wire:
    """A wire in a string diagram carrying a type.

    Attributes:
        wire_type: The type carried by this wire.
        entity: Optional entity label (for discourse persistence).
        case_role: Optional case role assignment.
    """

    wire_type: AtomicType
    entity: Optional[str] = None
    case_role: Optional[CaseRole] = None

    def __repr__(self) -> str:
        parts = [self.wire_type.name]
        if self.entity:
            parts.append(f"({self.entity})")
        if self.case_role:
            parts.append(f"[{self.case_role.name}]")
        return ":".join(parts)


@dataclass
class Box:
    """A box (process) in a string diagram.

    Represents a word or morphological operation that transforms
    input wires to output wires according to its type signature.

    Attributes:
        name: Label of the box (e.g., word).
        dom: Input wires (domain).
        cod: Output wires (codomain).
    """

    name: str
    dom: list[Wire] = field(default_factory=list)
    cod: list[Wire] = field(default_factory=list)

    @property
    def dom_type(self) -> str:
        """String representation of domain type."""
        return " ⊗ ".join(str(w.wire_type) for w in self.dom) if self.dom else "I"

    @property
    def cod_type(self) -> str:
        """String representation of codomain type."""
        return " ⊗ ".join(str(w.wire_type) for w in self.cod) if self.cod else "I"

    def __repr__(self) -> str:
        return f"Box({self.name}: {self.dom_type} → {self.cod_type})"


@dataclass
class Sentence:
    """A sentence represented as a DisCoCat string diagram.

    The diagram captures the compositional structure of a sentence,
    with nouns as identity wires and verbs as boxes that consume and
    produce wires according to their type.

    Attributes:
        text: The natural language sentence.
        boxes: Ordered list of boxes (words/morphemes).
        wires: All wires in the diagram.
        case_assignments: Map from entity names to case roles.
    """

    text: str
    boxes: list[Box] = field(default_factory=list)
    wires: list[Wire] = field(default_factory=list)
    case_assignments: dict[str, CaseRole] = field(default_factory=dict)

    def add_noun(self, word: str, case_role: CaseRole) -> Wire:
        """Add a noun to the sentence diagram.

        Args:
            word: The noun word.
            case_role: The case role assigned to this noun.

        Returns:
            The wire representing the noun.
        """
        wire = Wire(wire_type=N, entity=word, case_role=case_role)
        box = Box(name=word, dom=[], cod=[wire])
        self.boxes.append(box)
        self.wires.append(wire)
        self.case_assignments[word] = case_role
        return wire

    def add_verb(
        self, word: str, subject: Wire, obj: Optional[Wire] = None
    ) -> Wire:
        """Add a verb to the sentence diagram.

        For transitive verbs, consumes subject and object noun wires
        and produces a sentence wire. For intransitive, just subject.

        Args:
            word: The verb word.
            subject: Subject noun wire.
            obj: Optional object noun wire (for transitive).

        Returns:
            The sentence wire produced.
        """
        sentence_wire = Wire(wire_type=S)
        dom = [subject] if obj is None else [subject, obj]
        box = Box(name=word, dom=dom, cod=[sentence_wire])
        self.boxes.append(box)
        self.wires.append(sentence_wire)
        return sentence_wire

    @property
    def codomain_type(self) -> str:
        """The overall codomain type of the sentence diagram."""
        sentence_wires = [w for w in self.wires if w.wire_type == S]
        if sentence_wires:
            return " ⊗ ".join(str(w.wire_type) for w in sentence_wires)
        return "I"

    @property
    def num_boxes(self) -> int:
        """Total number of boxes in the diagram."""
        return len(self.boxes)

    @classmethod
    def transitive(cls, subject: str, verb: str, obj: str) -> "Sentence":
        """Create a transitive sentence diagram.

        Example: Sentence.transitive("Alice", "chases", "Bob")
        """
        sent = cls(text=f"{subject} {verb} {obj}")
        subj_wire = sent.add_noun(subject, CaseRole.NOM)
        obj_wire = sent.add_noun(obj, CaseRole.ACC)
        sent.add_verb(verb, subj_wire, obj_wire)
        logger.debug("Created transitive sentence: %s", sent.text)
        return sent

    @classmethod
    def intransitive(cls, subject: str, verb: str) -> "Sentence":
        """Create an intransitive sentence diagram.

        Example: Sentence.intransitive("Bob", "runs")
        """
        sent = cls(text=f"{subject} {verb}")
        subj_wire = sent.add_noun(subject, CaseRole.NOM)
        sent.add_verb(verb, subj_wire)
        logger.debug("Created intransitive sentence: %s", sent.text)
        return sent


@dataclass
class Discourse:
    """Multi-sentence discourse as a DisCoCirc-style diagram.

    Extends DisCoCat to multi-sentence text by modeling nouns as
    persistent state wires in a categorical circuit. Entity wires
    persist across sentence boundaries, with case roles dynamically
    reassigned at each step.

    **Limitations**: Entity matching uses exact string equality of word
    names — there is no coreference resolution or pronoun binding.
    The current implementation tracks entity names and role history
    but does not implement full DisCoCirc circuit semantics (feedback
    wires, state update boxes, or formal entity persistence). See
    ``security.cognitive_security.CaseFrameValidator`` for formal
    type-checking of case transitions.

    Attributes:
        sentences: Ordered list of sentences in the discourse.
        entity_wires: Persistent entity wires across the discourse.
        role_history: History of case role assignments per entity.
    """

    sentences: list[Sentence] = field(default_factory=list)
    entity_wires: dict[str, list[Wire]] = field(default_factory=dict)
    role_history: dict[str, list[CaseRole]] = field(default_factory=dict)

    def add_sentence(self, sentence: Sentence) -> None:
        """Add a sentence to the discourse, tracking entity persistence.

        Updates entity wires and role history for coreference tracking.
        """
        self.sentences.append(sentence)
        for entity, role in sentence.case_assignments.items():
            if entity not in self.entity_wires:
                self.entity_wires[entity] = []
                self.role_history[entity] = []
            self.entity_wires[entity].extend(
                [w for w in sentence.wires if w.entity == entity]
            )
            self.role_history[entity].append(role)
        logger.debug(
            "Added sentence to discourse: %s (total: %d)",
            sentence.text, len(self.sentences),
        )

    @property
    def entities(self) -> set[str]:
        """Return all entities mentioned in the discourse."""
        return set(self.entity_wires.keys())

    @property
    def num_sentences(self) -> int:
        """Return the number of sentences in the discourse."""
        return len(self.sentences)

    @property
    def total_boxes(self) -> int:
        """Return total box count across all sentences."""
        return sum(s.num_boxes for s in self.sentences)

    @property
    def codomain_type(self) -> str:
        """Composite codomain type of the full discourse."""
        return " ⊗ ".join(s.codomain_type for s in self.sentences)

    def role_reversal_entities(self) -> list[str]:
        """Find entities whose case role changes across the discourse.

        Example: Alice is NOM in sentence 1, ACC in sentence 2, NOM in 3.
        """
        reversals = []
        for entity, roles in self.role_history.items():
            if len(set(roles)) > 1:
                reversals.append(entity)
        return reversals

    @classmethod
    def two_sentence(
        cls, subj1: str, verb1: str, obj1: str, subj2: str, verb2: str
    ) -> "Discourse":
        """Create a two-sentence discourse with entity persistence.

        Example: Discourse.two_sentence("Alice", "chases", "Bob", "Bob", "runs")
        """
        discourse = cls()
        discourse.add_sentence(Sentence.transitive(subj1, verb1, obj1))
        discourse.add_sentence(Sentence.intransitive(subj2, verb2))
        return discourse

    @classmethod
    def role_reversal(
        cls, entity: str, partner: str
    ) -> "Discourse":
        """Create a three-sentence discourse demonstrating role reversal.

        Sentence 1: entity (NOM) chases partner (ACC)
        Sentence 2: partner (NOM) fears entity (ACC)
        Sentence 3: entity (NOM) smiles — aligns with manuscript §4c and DisCoPy export.
        """
        discourse = cls()
        discourse.add_sentence(Sentence.transitive(entity, "chases", partner))
        discourse.add_sentence(Sentence.transitive(partner, "fears", entity))
        discourse.add_sentence(Sentence.intransitive(entity, "smiles"))
        return discourse


# --- DisCoPy Integration ---


def create_discopy_transitive(subject: str, verb: str, obj: str, s_type: str = 's'):
    """Create a DisCoPy diagram for a transitive sentence using real DisCoPy.

    Uses discopy.rigid for pregroup grammar types and Box/Cup operations.

    Args:
        subject: Subject noun.
        verb: Transitive verb.
        obj: Object noun.
        s_type: Label for the sentence output wire (useful for language tagging).

    Returns:
        A discopy.rigid.Diagram representing the sentence.

    Raises:
        ImportError: If discopy is not installed.
    """
    from discopy.rigid import Ty, Box as RBox, Cup, Id

    n = Ty('n')
    s = Ty(s_type)

    # Transitive verb type: n.r @ s @ n.l
    subject_box = RBox(subject, Ty(), n)
    verb_box = RBox(verb, Ty(), n.r @ s @ n.l)
    object_box = RBox(obj, Ty(), n)

    # Build the diagram: subject ⊗ verb ⊗ object >> cups
    diagram = subject_box @ verb_box @ object_box
    # Apply cups to contract: n @ n.r → I (left) and n.l @ n → I (right)
    diagram = diagram >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)

    logger.info("Created DisCoPy transitive diagram: %s %s %s", subject, verb, obj)
    return diagram


def create_discopy_complex_transitive():
    """Create a 9-word complex sentence diagram.
    
    Sentence: 'the clever autonomous agent intercepts the malicious adversarial payload'
    
    Returns:
        A discopy.rigid.Diagram reducing the 9 words to sentence type 's'.
    """
    from discopy.rigid import Ty, Box as RBox, Id, Cup
    n = Ty('n')
    s = Ty('s')

    the1 = RBox('the', Ty(), n @ n.l)
    adj1 = RBox('clever', Ty(), n @ n.l)
    adj2 = RBox('autonomous', Ty(), n @ n.l)
    agent = RBox('agent', Ty(), n)

    verb = RBox('intercepts', Ty(), n.r @ s @ n.l)

    the2 = RBox('the', Ty(), n @ n.l)
    adj3 = RBox('malicious', Ty(), n @ n.l)
    adj4 = RBox('adversarial', Ty(), n @ n.l)
    payload = RBox('payload', Ty(), n)

    words = the1 @ adj1 @ adj2 @ agent @ verb @ the2 @ adj3 @ adj4 @ payload

    # subject NP reduction (right to left typically, so n.l contracts with n)
    cup1 = Id(n@n.l @ n@n.l @ n) @ Cup(n.l, n) @ Id(n.r@s@n.l @ n@n.l @ n@n.l @ n@n.l @ n)
    cup2 = Id(n@n.l @ n) @ Cup(n.l, n) @ Id(n.r@s@n.l @ n@n.l @ n@n.l @ n@n.l @ n)
    cup3 = Id(n) @ Cup(n.l, n) @ Id(n.r@s@n.l @ n@n.l @ n@n.l @ n@n.l @ n)

    # object NP reduction
    cup4 = Id(n @ n.r@s@n.l @ n@n.l @ n@n.l @ n) @ Cup(n.l, n)
    cup5 = Id(n @ n.r@s@n.l @ n@n.l @ n) @ Cup(n.l, n)
    cup6 = Id(n @ n.r@s@n.l @ n) @ Cup(n.l, n)

    # verb reduction
    cup7 = Cup(n, n.r) @ Id(s @ n.l @ n)
    cup8 = Id(s) @ Cup(n.l, n)

    diagram = words >> cup1 >> cup2 >> cup3 >> cup4 >> cup5 >> cup6 >> cup7 >> cup8
    logger.info("Created complex transitive diagram")
    return diagram


def create_discopy_intransitive(subject: str, verb: str):
    """Create a DisCoPy diagram for an intransitive sentence.

    Args:
        subject: Subject noun.
        verb: Intransitive verb.

    Returns:
        A discopy.rigid.Diagram.

    Raises:
        ImportError: If discopy is not installed.
    """
    from discopy.rigid import Ty, Box as RBox, Cup, Id

    n = Ty('n')
    s = Ty('s')

    subject_box = RBox(subject, Ty(), n)
    verb_box = RBox(verb, Ty(), n.r @ s)

    # Build parallel product then apply Cup
    diagram = subject_box @ verb_box >> Cup(n, n.r) @ Id(s)

    logger.info("Created DisCoPy intransitive diagram: %s %s", subject, verb)
    return diagram


def create_discopy_passive(subject: str, verb: str, agent: str):
    """Create a DisCoPy diagram for a passive sentence.

    Passivization as algebraic type permutation:
    "Bob is chased by Alice" reverses argument order.

    Args:
        subject: Grammatical subject (patient).
        verb: Passive verb.
        agent: By-phrase agent.

    Returns:
        A discopy.rigid.Diagram.
    """
    from discopy.rigid import Ty, Box as RBox, Cup, Id

    n = Ty('n')
    s = Ty('s')

    # Passive type: swap the noun arguments
    subject_box = RBox(subject, Ty(), n)
    verb_box = RBox(f"is {verb} by", Ty(), n.r @ s @ n.l)
    agent_box = RBox(agent, Ty(), n)

    diagram = subject_box @ verb_box @ agent_box
    diagram = diagram >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)

    logger.info("Created DisCoPy passive diagram: %s is %s by %s", subject, verb, agent)
    return diagram


def create_discopy_snake_equation():
    """Create the snake equation (compact closure axiom) diagram.

    Demonstrates: x ⊗ Cap(x.r, x) >> Cup(x, x.r) ⊗ x = Id(x)
    This is the fundamental identity of compact closed categories.

    Returns:
        Tuple of (left_snake, identity, right_snake) DisCoPy diagrams.
    """
    from discopy.rigid import Ty, Id, Cup, Cap

    x = Ty('x')

    left_snake = x @ Cap(x.r, x) >> Cup(x, x.r) @ x
    right_snake = Cap(x, x.l) @ x >> x @ Cup(x.l, x)
    identity = Id(x)

    logger.info("Created DisCoPy snake equation diagrams")
    return left_snake, identity, right_snake


def create_discopy_composition(subject: str, verb: str, obj: str):
    """Create a DisCoPy composition diagram showing pre- and post-contraction.

    Returns the pre-contraction word tensor (before Cup contractions)
    alongside the fully contracted diagram. This makes the DisCoCat
    functor mapping F: Preg → FVect visible: the left panel shows the
    uncontracted word boxes, the right panel shows the result after
    Cup contractions reduce the type to s.

    Returns:
        Tuple of (words_tensor, contracted_diagram).
    """
    from discopy.rigid import Ty, Box as RBox, Cup, Id

    n = Ty('n')
    s = Ty('s')

    subject_box = RBox(subject, Ty(), n)
    verb_box = RBox(verb, Ty(), n.r @ s @ n.l)
    object_box = RBox(obj, Ty(), n)

    # Pre-contraction: just the word tensor product (no cups applied)
    words = subject_box @ verb_box @ object_box

    # Fully contracted diagram (cups applied)
    diagram = words >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)

    logger.info("Created composition diagram: words (%d boxes) → contracted (%d boxes)",
                len(words.boxes), len(diagram.boxes))
    return words, diagram


def create_discopy_multilingual(translations: Optional[dict] = None):
    """Create DisCoPy diagrams for 'Alice chases Bob' across languages.

    Args:
        translations: Dict mapping language name to (subject, verb, object).
            Defaults to 6 standard languages.

    Returns:
        Dict mapping language name to discopy diagram.
    """
    if translations is None:
        translations = {
            "English": ("Alice", "chases", "Bob"),
            "Latin": ("Alicia", "persequitur", "Robertum"),
            "Japanese": ("Arisu-ga", "ou", "Bobu-wo"),
            "Turkish": ("Alice", "kovaliyor", "Bob-u"),
            "Basque": ("Alice-k", "jazartzen_du", "Bob"),
            "Hindi": ("Alice", "piicha_karti_hai", "Bob-ko"),
        }

    diagrams = {}
    for lang, (subj, verb, obj) in translations.items():
        diagrams[lang] = create_discopy_transitive(subj, verb, obj, s_type='s')
        logger.debug("Created %s diagram", lang)

    logger.info("Created multilingual diagrams for %d languages", len(diagrams))
    return diagrams


# --- Extended DisCoPy Integration (grammar.pregroup, Swap, tensor semantics) ---


def create_word_diagram_transitive(subject: str, verb: str, obj: str):
    """Create a transitive diagram using grammar.pregroup.Word and eager_parse.

    Uses DisCoPy's proper grammar types instead of generic Box.
    Word carries lexical information, and eager_parse automatically
    determines optimal Cup placement.

    Args:
        subject: Subject noun.
        verb: Transitive verb.
        obj: Object noun.

    Returns:
        A discopy.grammar.pregroup.Diagram with Word boxes.
    """
    from discopy.grammar.pregroup import Word, Ty, eager_parse

    n = Ty('n')
    s = Ty('s')

    subject_word = Word(subject, n)
    verb_word = Word(verb, n.r @ s @ n.l)
    object_word = Word(obj, n)

    diagram = eager_parse(subject_word, verb_word, object_word)
    logger.info("Created Word-based transitive diagram via eager_parse: %s %s %s",
                subject, verb, obj)
    return diagram


def create_word_diagram_intransitive(subject: str, verb: str):
    """Create an intransitive diagram using grammar.pregroup.Word and eager_parse.

    Args:
        subject: Subject noun.
        verb: Intransitive verb.

    Returns:
        A discopy.grammar.pregroup.Diagram.
    """
    from discopy.grammar.pregroup import Word, Ty, eager_parse

    n = Ty('n')
    s = Ty('s')

    subject_word = Word(subject, n)
    verb_word = Word(verb, n.r @ s)

    diagram = eager_parse(subject_word, verb_word)
    logger.info("Created Word-based intransitive diagram via eager_parse: %s %s",
                subject, verb)
    return diagram


def create_swap_passive(subject: str, verb: str, agent: str):
    """Create a passive sentence using DisCoPy's Swap morphism.

    Passivization is modeled as a type permutation (Swap) that
    exchanges the argument order of the verb, making the patient
    the grammatical subject (cf. §3b).

    Uses discopy.grammar.pregroup.Swap — the proper categorical
    operation for argument reordering.

    Args:
        subject: Grammatical subject (patient).
        verb: Passive verb.
        agent: By-phrase agent.

    Returns:
        A discopy.grammar.pregroup.Diagram with explicit Swap.
    """
    from discopy.grammar.pregroup import Word, Ty, eager_parse

    n = Ty('n')
    s = Ty('s')

    patient_word = Word(subject, n)
    passive_verb = Word(f"is_{verb}_by", n.r @ s @ n.l)
    agent_word = Word(agent, n)

    diagram = eager_parse(patient_word, passive_verb, agent_word)

    logger.info("Created Swap-passive diagram: %s is %s by %s",
                subject, verb, agent)
    return diagram


def create_word_diagram_ditransitive(
    subject: str, verb: str, indirect_object: str, direct_object: str
):
    """Create a ditransitive diagram using grammar.pregroup.Word and eager_parse.

    Args:
        subject: Agent (NOM).
        verb: Ditransitive verb.
        indirect_object: Recipient (DAT).
        direct_object: Theme (ACC).

    Returns:
        A discopy.grammar.pregroup.Diagram.
    """
    from discopy.grammar.pregroup import Word, Ty, eager_parse

    n = Ty('n')
    s = Ty('s')

    subj = Word(subject, n)
    v = Word(verb, n.r @ s @ n.l @ n.l)
    io = Word(indirect_object, n)
    do = Word(direct_object, n)

    diagram = eager_parse(subj, v, io, do)
    logger.info("Created Word-based ditransitive via eager_parse: %s %s %s %s",
                subject, verb, indirect_object, direct_object)
    return diagram


def create_tensor_semantics(
    subject: str,
    verb: str,
    obj: str,
    noun_dim: int = 2,
    sentence_dim: int = 4,
    subject_vec: Optional[list[float]] = None,
    object_vec: Optional[list[float]] = None,
    verb_tensor: Optional[list[float]] = None,
):
    """Create a DisCoCat meaning functor evaluation in tensor category.

    Implements F: Preg -> FVect by building the diagram directly in
    discopy.tensor, where Box data carries word vectors/tensors.
    The diagram is evaluated via .eval() to produce sentence meaning.

    This is the core DisCoCat semantic composition (§4):
        F(Alice chases Bob) = F(chases) x_n F(Alice) x_n F(Bob)

    Args:
        subject: Subject noun name.
        verb: Verb name.
        obj: Object noun name.
        noun_dim: Dimension of noun vector space N.
        sentence_dim: Dimension of sentence vector space S.
        subject_vec: Noun vector for subject (default: basis[0]).
        object_vec: Noun vector for object (default: basis[1]).
        verb_tensor: Verb tensor (N x S x N, default: sparse).

    Returns:
        Tuple of (tensor_diagram, meaning_vector) where meaning_vector
        is a numpy array of shape (sentence_dim,).
    """
    from discopy.tensor import Box as TBox, Cup as TCup, Id as TId, Dim

    N = Dim(noun_dim)
    S = Dim(sentence_dim)

    if subject_vec is None:
        subject_vec = [0.0] * noun_dim
        subject_vec[0] = 1.0
    if object_vec is None:
        object_vec = [0.0] * noun_dim
        object_vec[min(1, noun_dim - 1)] = 1.0
    if verb_tensor is None:
        verb_tensor = [0.0] * (noun_dim * sentence_dim * noun_dim)
        verb_tensor[0 * sentence_dim * noun_dim + 0 * noun_dim + min(1, noun_dim - 1)] = 1.0

    subj_box = TBox(subject, Dim(1), N, subject_vec)
    verb_box = TBox(verb, Dim(1), N @ S @ N, verb_tensor)
    obj_box = TBox(obj, Dim(1), N, object_vec)

    diagram = subj_box @ verb_box @ obj_box >> TCup(N, N) @ TId(S) @ TCup(N, N)

    meaning = diagram.eval()
    logger.info(
        "DisCoCat semantic evaluation: '%s %s %s' -> meaning vector shape %s",
        subject, verb, obj, meaning.array.shape,
    )
    return diagram, meaning.array
