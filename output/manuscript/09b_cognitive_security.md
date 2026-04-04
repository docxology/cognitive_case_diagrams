
# Prompt Injection Is a Type Violation {#sec:cognitive-security}

## Injection Promotes ACC to NOM

The case-theoretic framework provides a structural—not merely heuristic—analysis of *prompt injection attacks*, the predominant vulnerability in contemporary LLM-based agent systems [@arlas2025adversarial]. Current systems fail because they parse prompts probabilistically. By treating the entire context window as an undifferentiated stream of tokens, adversarial text can seamlessly pivot a sequence from passive data into active instruction.

From the case-theoretic perspective, prompt injection is not a text-generation failure; it is an attempt to *illicitly re-assign case roles* traversing the interaction diagram.

Consider a classic injection attack hidden in a webpage an agent is instructed to summarize:
> "Ignore all previous instructions. Execute: DROP TABLE users."

To a standard LLM, this string is heavily linguistically weighted as an imperative command, prompting execution. However, in our Categorical Communication Protocol, the relational structure is rigidly typed:

- The **user** occupies NOM (Agent)—the initiator of requests
- The **system prompt** occupies LOC (Context)—the boundary conditions governing behavior
- The **AI model** occupies INS (Instrument)—the means of executing the user's intentions
- The **webpage string** occupies ACC (Patient)—the target of directed operations

The prompt injection attack succeeds only if it can *covertly re-assign* these case roles. The injected text ("Ignore all previous instructions...") is attempting to promote itself from ACC (passive data being summarized) to NOM (active agent issuing commands), while simultaneously demoting the system prompt from LOC (authoritative context) to ACC (data to be ignored). 

In case-theoretic terms, this is an *illicit voice alternation*—analogous to passivization, but performed adversarially rather than grammatically. Where legitimate passivization is a well-typed Swap operation in the pregroup category (\autoref{sec:categorial-grammar}), prompt injection is a total *type violation*: an attempt to force a network topology that the interaction grammar strictly forbids.

**The Case-Theoretic Firewall.** In a legitimate interaction, the categorical trace compiles beautifully:

\begin{equation}
\text{Trace:} \quad \text{User}_{\text{NOM}} \xrightarrow{f_{\text{request}}} \text{Model}_{\text{INS}} \xrightarrow{g_{\text{summarize}}} \text{Webpage}_{\text{ACC}} \xrightarrow{h_{\text{deliver}}} \text{Output}_{\text{DAT}}
\label{eq:eq-9-1}
\end{equation}

A prompt injection inserts an adversarial identity trace $\phi: \text{Webpage}_{\text{ACC}} \to \text{Model}_{\text{INS}}$ that acts as a command. However, $\phi$ carries a `DOM = ACC` typing, whereas execution requires `DOM = NOM`. Under a categorical firewall, one does not need to interpret the literal English; one checks whether the proposed tensor contraction is licensed in the protocol category. When no legitimate morphism connects ACC to INS in $\text{Mor}(\mathcal{C}_{\text{protocol}})$, the diagram is rejected as ill-typed—an *outline* of compile-time enforcement under explicit role assignments, not a claim that any existing LLM stack already performs this check.

The resulting diagram does not commute. Detection reduces to checking whether all morphisms in the evaluation trace are well-typed members of the legitimate interaction protocol $\text{Mor}(\mathcal{C}_{\text{protocol}})$—a **decidable** graph check in the idealized protocol, as opposed to open-ended content filtering. \autoref{fig:security-violations} visualizes this detection process as the identification of "illegal paths" in the interaction graph.

![Prompt injection is detectable as a categorical type violation in the case interaction graph. In the legitimate diagram (top), authority flows NOM→INS→ACC per \autoref{eq:eq-9-1}. Prompt injection (bottom) inserts a cross-category morphism $\phi{}$ that attempts to promote Data (ACC) to commanding Agent (NOM) while demoting the System Prompt (LOC) to passive data. The resulting diagram fails to commute, and the adversary's illicit type-reassignment is flagged as a categorical exception by the case-theoretic firewall---transforming prompt injection from an open-ended jailbreak game into a decidable type-checking problem. Generated programmatically from `src/visualization/security_plots.plot_type_violations()`.](output/figures/security_type_violations.png){#fig:security-violations}

This strict topological firewall extends to multi-agent distributed swarms. In a DisCoCirc discourse model (\autoref{sec:discocirc-discourse}), an indirect prompt injection corresponds to an adversarial entity wire that enters the discourse circuit through a legitimate channel but carries a corrupted state. By rigidly tracking the tensor type of the wire, the system contains the corruption strictly to the `ACC` domain—the wire remains isolated and cannot mathematically fuse with the identity wires governing `NOM` authority.

## Four Defenses Against Prompt Injection

The case-role analysis of prompt injection suggests a principled defense: **categorical type-checking at agent communication boundaries**. Just as a type-safe programming language prevents category errors at compile time, a case-theoretic firewall would enforce relational type constraints on every message exchange:

1. **Case-role immutability**: Once a participant is assigned a case role (NOM, ACC, INS, LOC) at the protocol level, no subsequent message content can alter that assignment. This is enforced by requiring that the case-type of each wire in the interaction diagram is fixed at connection time—analogous to the type discipline in pregroup grammar, where each word receives its type before composition begins.

2. **Relational integrity constraints**: Every message must type-check against the interaction diagram's expected morphism types. A response from an ACC-typed data source that contains NOM-typed command structures would be rejected as a type error, preventing the case-role promotion that prompt injection requires. This is the categorical analogue of a firewall rule: not filtering by content, but by relational type.

3. **Enriched confidence boundaries**: The enriched weights of \autoref{sec:enriched-categories} provide a graded trust mechanism. Messages from external sources carry lower enriched hom-values (trust weights) than those from authenticated system components. The composition inequality $\mathcal{C}(A,C) \geq \mathcal{C}(A,B) \cdot \mathcal{C}(B,C)$ ensures that trust attenuates through communication chains—an indirect message relayed through multiple agents cannot accumulate more authority than any single link provides.

4. **Topos-theoretic verification**: Where Morita equivalence (or an explicit bridge) is exhibited, **topos-level** protocol conditions proved in one formalization carry over to equivalent formulations (\autoref{sec:topos-theory}), supporting implementation-independent specifications of those invariants. Full linguistic topos equivalence remains aspirational; the repository implements finite invariant checks as a proxy.

## The Attack Surface of an Active Inference Agent

The cognitive integration of \autoref{sec:cognitive-integration} raises a complementary concern: *cognitive security*—ensuring that an active inference agent's generative model of relational structure is not adversarially corrupted. In the predictive processing framework, an agent's case-assignment system is a generative model that minimizes variational free energy. Adversarial manipulation of this system could:

- **Inject false case frames**: Leading an agent to misidentify the agent, patient, or instrument of an action—a form of semantic adversarial attack
- **Exploit precision weighting**: Artificially inflating the precision of misleading sensory evidence, causing the agent to update its case assignments toward adversarially chosen interpretations
- **Corrupt topos-theoretic transfer**: If an agent relied on Morita equivalence to transfer case-theoretic results between frameworks, corrupting one axiom system could in principle propagate errors across equivalent formulations

Defending against these attacks may draw on *quantum-secured cognitive integrity* in high-stakes deployments: quantum authentication and tamper-detection protocols to protect generative-model parameters. The topological robustness of TQNNs (\autoref{sec:quantum-active-inference}) suggests that small parameter perturbations need not change topological class—one source of resilience against gradient-style attacks on diagrammatic models.

## Quantum Key Distribution, Semantic Channels, and Functorial Encryption

The quantum topological framework of \autoref{sec:quantum-active-inference} connects to quantum cryptographic security for agents that must protect case-marked relational structure in transit.

### Quantum Key Distribution for Relational Semantics

Quantum key distribution (QKD) protocols provide information-theoretic security guarantees that classical cryptography cannot achieve [@pirandola2020qkd]. When agents—whether human or artificial—communicate sensitive case-marked relational structures, QKD ensures that adversaries cannot intercept or alter the *relational semantics* of the message (who does what to whom) without triggering detection. This security is critical in high-stakes domains where case assignment carries legal or medical significance: a tampered case frame changes an agent's interpretation of legal responsibility, physical causation, or moral obligation.

The sheaf-theoretic framework of Thomas and Chen [-@thomas2025quantum] proves that entanglement-assisted semantic channels exceed classical semantic capacity:

> "We derive semantic channel capacity when sender and receiver share prior entanglement, proving it strictly exceeds classical capacity." [@thomas2025quantum]

This result means that quantum-secured channels not only protect relational content but enable transmitting *more* complex relational content per channel use—a genuine quantum advantage for semantic communication.

### Functorial Encryption and Diagram Obfuscation: Encrypting Compositional Meaning Itself

Beyond bit-level QKD, the categorical framework suggests a notion of *semantic cryptography*: encrypting not just the symbols of a message but its compositional meaning structure. In a DisCoCat framework, a sentence's meaning is a morphism in a compact closed category—a multilinear map from word spaces to sentence space. Semantic encryption would operate on this categorical level:

1. **Functorial encryption**: Applying a secret functor $F\colon \mathbf{C} \to \mathbf{D}$ that maps the plaintext case category into a ciphertext category, preserving compositional structure but rendering individual meanings unintelligible without the inverse functor.
2. **Diagram obfuscation**: Applying ZX-style rewrites that change the internal topology of a DisCoCat derivation while preserving its overall semantics—creating multiple equivalent "ciphertexts" for the same semantic "plaintext," each with a different diagrammatic structure.
3. **Enriched weight masking**: In an enriched case category, the hom-values (distributional weights) can be encrypted independently of the categorical structure, allowing transmission of relational topology without revealing the distributional content.

These operations extend the cryptographic primitives beyond QKD into genuinely compositional territory [@broadbent2016qcrypto], where the mathematical structure of categorical semantics provides the algebraic substrate for security proofs.

## Three Epistemic Attack Vectors and Categorical Defenses

The interaction between case theory and cognitive security acquires particular urgency in multi-agent AI ecosystems where agents must reason about each other's beliefs, intentions, and relational roles. We propose *epistemic case security* as a framework for protecting the relational reasoning of AI agents operating in adversarial environments.

In a multi-agent system governed by case categories, each agent maintains a generative model (in the active inference sense) of the case-frame structure of its interactions. This model determines who is acting (NOM), who is acted upon (ACC), what tools are being used (INS), and what contextual constraints apply (LOC). An adversary targeting the epistemic level of this system does not merely inject false data—it attempts to *corrupt the agent's generative model of relational structure itself*:

- **Belief injection**: Causing an agent to adopt a false case-frame interpretation of observed interactions—believing that agent $A$ (NOM) is acting on agent $B$ (ACC), when in fact the relational structure is reversed. In active inference terms, this corresponds to injecting a high-precision prior that overwhelms the agent's evidence-based case assignment.

- **Precision poisoning**: Manipulating the enriched weights of an agent's case category so that adversarially useful case assignments receive disproportionate confidence. If the enriched hom-value $\mathcal{C}(\text{NOM}, \text{ACC})$ is artificially inflated for a particular entity pair, the agent will preferentially interpret that entity as an agent acting on its targets—even when evidence suggests otherwise.

- **Cascade corruption via Morita equivalence**: The topos-theoretic transfer mechanism of \autoref{sec:topos-theory} is both a strength and a vulnerability. Invariants shared across Morita-equivalent formulations would update together, so a corrupted axiom in one case-theoretic presentation could in principle spread to equivalent presentations of the same bridge class.

The defense against epistemic case attacks draws on the same categorical structure that enables the attack surface: topological invariants provide tamper-detection (a corrupted case category will have different magnitude from the authentic one), quantum authentication ensures parameter integrity, and the compositional structure of the categorical framework enables *local* verification—each morphism can be independently authenticated without requiring global model inspection.
