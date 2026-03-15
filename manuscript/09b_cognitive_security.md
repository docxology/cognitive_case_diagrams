
# Cognitive Security: Adversarial Robustness and Type Safety {#sec:cognitive-security}

## Quantum Cryptographic Communications and Semantic Security

The quantum topological framework of \autoref{sec:quantum-active-inference} opens a natural connection to quantum cryptographic communications, with implications for both the security and the semantic integrity of case-structured information transfer.

### Quantum Key Distribution for Relational Semantics

Quantum key distribution (QKD) protocols provide information-theoretic security guarantees that classical cryptography cannot achieve [@pirandola2020qkd]. When case-marked relational structures are communicated between agents—whether human or artificial—QKD ensures that the *relational semantics* of a message (who does what to whom) cannot be intercepted or altered without detection. This is particularly relevant for high-stakes domains where case assignment carries legal or medical significance: a tampered case frame could change an agent's interpretation of responsibility, causation, or obligation.

The sheaf-theoretic framework of Khatri et al. [-@khatri2025quantum] further shows that entanglement-assisted semantic channels strictly exceed classical semantic capacity:

> "We derive semantic channel capacity when sender and receiver share prior entanglement, proving it strictly exceeds classical capacity." [@khatri2025quantum]

This means that quantum-secured channels not only protect relational content but also enable *more* relational content to be communicated per channel use—a genuine quantum advantage for semantic communication.

### Semantic Cryptography: Encrypting Meaning Structures

Beyond bit-level QKD, the categorical framework suggests a notion of *semantic cryptography*: encrypting not just the symbols of a message but its compositional meaning structure. In a DisCoCat framework, a sentence's meaning is a morphism in a compact closed category—a multilinear map from word spaces to sentence space. Semantic encryption would operate on this categorical level:

1. **Functorial encryption**: Applying a secret functor $F\colon \mathbf{C} \to \mathbf{D}$ that maps the plaintext case category into a ciphertext category, preserving compositional structure but rendering individual meanings unintelligible without the inverse functor.
2. **Diagram obfuscation**: Applying ZX-style rewrites that change the internal topology of a DisCoCat derivation while preserving its overall semantics—creating multiple equivalent "ciphertexts" for the same semantic "plaintext," each with a different diagrammatic structure.
3. **Enriched weight masking**: In an enriched case category, the hom-values (distributional weights) can be encrypted independently of the categorical structure, allowing transmission of relational topology without revealing the distributional content.

These operations extend the cryptographic primitives beyond QKD into genuinely compositional territory [@broadbent2016qcrypto], where the mathematical structure of categorical semantics provides the algebraic substrate for security proofs.

## Cognitive Security: Protecting Relational Reasoning

The cognitive integration of \autoref{sec:cognitive-integration} raises a complementary concern: *cognitive security*—ensuring that an active inference agent's generative model of relational structure is not adversarially corrupted. In the predictive processing framework, an agent's case-assignment system is a generative model that minimizes variational free energy. Adversarial manipulation of this system could:

- **Inject false case frames**: Leading an agent to misidentify the agent, patient, or instrument of an action—a form of semantic adversarial attack
- **Exploit precision weighting**: Artificially inflating the precision of misleading sensory evidence, causing the agent to update its case assignments toward adversarially chosen interpretations
- **Corrupt topos-theoretic transfer**: If an agent uses Morita equivalence to transfer case-theoretic results between frameworks, corrupting one framework could propagate errors across all equivalent formulations

Defending against these attacks requires *quantum-secured cognitive integrity*: using quantum authentication and tamper-detection protocols to ensure that the generative model's parameters—the objects, morphisms, and enriched weights of the case category—have not been adversarially modified. The topological robustness of TQNNs (\autoref{sec:quantum-active-inference}) provides a natural resilience mechanism: topological invariants are robust to continuous deformation, so small perturbations to the generative model's parameters cannot change its topological class, providing inherent resistance to gradient-based adversarial attacks.

## Prompt Injection as Adversarial Case-Frame Manipulation

The case-theoretic framework offers a novel structural analysis of *prompt injection attacks*—the predominant vulnerability in contemporary LLM-based agent systems [@arlas2025adversarial]. From the case-theoretic perspective, a prompt injection attack is fundamentally an attempt to *re-assign the case roles* of participants in the human-AI interaction:

In a well-formed agent interaction, the relational structure is:

- The **user** occupies NOM (Agent)—the initiator of requests
- The **system prompt** occupies LOC (Context)—the boundary conditions governing behavior
- The **AI model** occupies INS (Instrument)—the means of executing the user's intentions
- The **tool/API** occupies ACC (Patient)—the target of directed operations
- The **output** occupies DAT (Recipient)—the endpoint of information transfer

A prompt injection attack succeeds by *covertly re-assigning* these case roles. The injected text attempts to promote itself from ACC (passive data being processed) to NOM (active agent issuing commands), while simultaneously demoting the system prompt from LOC (authoritative context) to ACC (data to be overridden). In case-theoretic terms, this is an *illicit voice alternation*—analogous to passivization, but performed adversarially rather than grammatically. Where legitimate passivization is a well-typed Swap operation in the pregroup category (see \autoref{sec:categorial-grammar}), prompt injection is a *type violation*: an attempt to force a case-role permutation that the interaction grammar does not license.

**Formal characterization.** In a legitimate interaction, the following diagram commutes:

$$\text{User}_{\text{NOM}} \xrightarrow{f_{\text{request}}} \text{Model}_{\text{INS}} \xrightarrow{g_{\text{execute}}} \text{Tool}_{\text{ACC}} \xrightarrow{h_{\text{deliver}}} \text{Output}_{\text{DAT}} $$ {#eq:eq-9-1}

where case types are conserved: $\text{cod}(f) = \text{dom}(g)$, etc. A prompt injection inserts an adversarial morphism $\phi: \text{Data}_{\text{ACC}} \to \text{Model}_{\text{INS}}$ with $\text{dom}(\phi) = \text{ACC}$ but $\text{cod}(\phi) = \text{INS}$—a morphism that *does not exist* in the legitimate interaction category because no morphism from ACC to INS is licensed. The resulting diagram does not commute: $h \circ g \circ \phi \neq h \circ g \circ f$, because $\phi$ originates from a different case role than $f$ (ACC instead of NOM). Detection reduces to checking whether all morphisms in the interaction trace are members of the legitimate morphism set $\text{Mor}(\mathcal{C}_{\text{protocol}})$—a categorical type-checking operation that is decidable and compositionally verifiable. \autoref{fig:security-violations} visualizes this detection process as the identification of "illegal paths" in the interaction graph.

![Case-theoretic analysis of prompt injection as a categorical type violation. In the legitimate interaction diagram (top), the flow of authority strictly proceeds from User (NOM) to Model (INS) to Tool (ACC). Prompt injection (bottom) is visualized as the insertion of a cross-category morphism $\phi$ that attempts to promote Data (ACC) to commanding Agent (NOM), while demoting the System Prompt (LOC) to passive data. The resulting diagram fails to commute, and the adversary's type-reassignment is flagged as a categorical exception by the case-theoretic firewall—transforming prompt injection from an open-ended "jailbreak" game into a decidable type-checking problem.](output/figures/security_type_violations.png){#fig:security-violations}

This analysis extends to indirect prompt injection in multi-agent systems, where adversarial content embedded in retrieved documents or tool outputs can manipulate an agent's case-frame interpretation across communication boundaries [@arlas2025adversarial]. In a DisCoCirc discourse model (see \autoref{sec:categorical-semantics}), this corresponds to an adversarial entity wire that enters the discourse circuit through a legitimate channel but carries corrupted state—a coreference attack where the adversary's identity wire is surreptitiously merged with the system's authority wire.

## Case-Theoretic Firewalls for Multi-Agent Communication

The case-role analysis of prompt injection suggests a principled defense: **categorical type-checking at agent communication boundaries**. Just as a type-safe programming language prevents category errors at compile time, a case-theoretic firewall would enforce relational type constraints on every message exchange:

1. **Case-role immutability**: Once a participant is assigned a case role (NOM, ACC, INS, LOC) at the protocol level, no subsequent message content can alter that assignment. This is enforced by requiring that the case-type of each wire in the interaction diagram is fixed at connection time—analogous to the type discipline in pregroup grammar, where each word receives its type before composition begins.

2. **Relational integrity constraints**: Every message must type-check against the interaction diagram's expected morphism types. A response from an ACC-typed data source that contains NOM-typed command structures would be rejected as a type error, preventing the case-role promotion that prompt injection requires. This is the categorical analogue of a firewall rule: not filtering by content, but by relational type.

3. **Enriched confidence boundaries**: The enriched weights of \autoref{sec:enriched-categories} provide a graded trust mechanism. Messages from external sources carry lower enriched hom-values (trust weights) than those from authenticated system components. The composition inequality $\mathcal{C}(A,C) \geq \mathcal{C}(A,B) \cdot \mathcal{C}(B,C)$ ensures that trust attenuates through communication chains—an indirect message relayed through multiple agents cannot accumulate more authority than any single link provides.

4. **Topos-theoretic verification**: Protocol correctness conditions proved in one categorical formulation transfer automatically to all Morita-equivalent formulations (\autoref{sec:topos-theory}), ensuring that security guarantees are implementation-independent. A firewall rule verified for a DisCoCat-style agent communication protocol automatically holds for any quantum circuit implementation of the same protocol.

## Epistemic Case Security in Multi-Agent Systems

The interaction between case theory and cognitive security acquires particular urgency in multi-agent AI ecosystems where agents must reason about each other's beliefs, intentions, and relational roles. We propose *epistemic case security* as a framework for protecting the relational reasoning of AI agents operating in adversarial environments.

In a multi-agent system governed by case categories, each agent maintains a generative model (in the active inference sense) of the case-frame structure of its interactions. This model determines who is acting (NOM), who is acted upon (ACC), what tools are being used (INS), and what contextual constraints apply (LOC). An adversary targeting the epistemic level of this system does not merely inject false data—it attempts to *corrupt the agent's generative model of relational structure itself*:

- **Belief injection**: Causing an agent to adopt a false case-frame interpretation of observed interactions—believing that agent $A$ (NOM) is acting on agent $B$ (ACC), when in fact the relational structure is reversed. In active inference terms, this corresponds to injecting a high-precision prior that overwhelms the agent's evidence-based case assignment.

- **Precision poisoning**: Manipulating the enriched weights of an agent's case category so that adversarially useful case assignments receive disproportionate confidence. If the enriched hom-value $\mathcal{C}(\text{NOM}, \text{ACC})$ is artificially inflated for a particular entity pair, the agent will preferentially interpret that entity as an agent acting on its targets—even when evidence suggests otherwise.

- **Cascade corruption via Morita equivalence**: The topos-theoretic transfer mechanism of \autoref{sec:topos-theory} is both a strength and a vulnerability. Results proved in one framework propagate to all Morita-equivalent frameworks, so a single corrupted axiom in one case-theoretic formulation—say, the distributional framework—could propagate incorrect relational inferences to the typological, type-logical, and enriched frameworks simultaneously.

The defense against epistemic case attacks draws on the same categorical structure that enables the attack surface: topological invariants provide tamper-detection (a corrupted case category will have different magnitude from the authentic one), quantum authentication ensures parameter integrity, and the compositional structure of the categorical framework enables *local* verification—each morphism can be independently authenticated without requiring global model inspection.
