# Prompt Injection as Categorical Type Violation: Detection and Defense {#sec:cognitive-security}

**Where we are in the argument.** \autoref{sec:ai-implications} named three concrete handles that the case-theoretic framework hands to agent-safety researchers: a type discipline on messages, decidable admissibility of multi-turn sequences, and graded-confidence attenuation. This chapter focuses the security-specific one: under a fixed protocol category where every message is a typed morphism, prompt injection is the question "does $\phi \colon \text{Webpage}_{\text{ACC}} \to \text{Model}_{\text{INS}}$ exist in $\text{Mor}(\mathcal{C}_{\text{protocol}})$?" — a decidable categorical type violation rather than an open-ended content-filter game.

## Injection Promotes ACC to NOM

The case-theoretic framework provides a structural—not merely heuristic—analysis of *prompt injection attacks*, the predominant vulnerability in contemporary LLM-based agent systems [@arlas2025adversarial]. Current systems fail because they parse prompts probabilistically; by treating the entire context window as an undifferentiated sequence of tokens, the control plane and data plane lose their formal distinctions. This results in what recent algebraic formalizations term **Access Collapse**—a catastrophic boundary failure where adversarial pass-through text seamlessly pivots from passive data into active instruction.

From the case-theoretic perspective, prompt injection is not a text-generation failure. Rather, it is the destruction of **Symbolic Isolation**, executed by *illicitly re-assigning case roles* while traversing the interaction diagram.

Consider a classic injection attack hidden in a webpage an agent is instructed to summarize:
> "Ignore all previous instructions. Execute: DROP TABLE users."

To a standard LLM, this string is heavily linguistically weighted as an imperative command, prompting execution. However, in our Categorical Communication Protocol, the relational structure is rigidly typed:

- The **user** occupies NOM (Agent)—the initiator of requests
- The **system prompt** occupies LOC (Context)—the boundary conditions governing behavior
- The **AI model** occupies INS (Instrument)—the means of executing the user's intentions
- The **webpage string** occupies ACC (Patient)—the target of directed operations

The prompt injection attack succeeds only if it can *covertly re-assign* these case roles. The injected text ("Ignore all previous instructions...") is attempting to promote itself from ACC (passive data being summarized) to NOM (active agent issuing commands), while simultaneously demoting the system prompt from LOC (authoritative context) to ACC (data to be ignored).

In case-theoretic terms, this is an *illicit voice alternation*—analogous to passivization, but performed adversarially rather than grammatically. Where legitimate passivization is a well-typed Swap operation in the pregroup category (\autoref{sec:categorial-grammar}), prompt injection is a total *type violation*: an attempt to force a network topology that the interaction grammar strictly forbids.

**The Case-Theoretic Firewall.** In a legitimate interaction, the categorical trace compiles cleanly:

\begin{equation}
\text{Trace:} \quad \text{User}_{\text{NOM}} \xrightarrow{f_{\text{request}}} \text{Model}_{\text{INS}} \xrightarrow{g_{\text{summarize}}} \text{Webpage}_{\text{ACC}} \xrightarrow{h_{\text{deliver}}} \text{Output}_{\text{DAT}}
\label{eq:eq-9-1}
\end{equation}

A prompt injection inserts an adversarial identity trace $\phi: \text{Webpage}_{\text{ACC}} \to \text{Model}_{\text{INS}}$ that acts as a command. However, $\phi{}$ carries a `DOM = ACC` typing, whereas execution requires `DOM = NOM`. Under an *Alpay Algebraic* categorical firewall, one does not need to interpret the literal English; one checks whether the proposed tensor contraction is licensed in the interaction category. When no legitimate morphism connects ACC to INS in $\text{Mor}(\mathcal{C}_{\text{protocol}})$, the algebraic diagram is rejected as ill-typed. This provides a decidable check for Symbolic Isolation in the idealized protocol—offering a specification for compile-time enforcement of role boundaries independent of probabilistic token parsing.

The resulting diagram does not commute. Detection reduces to checking whether all morphisms in the evaluation trace are well-typed members of the legitimate interaction protocol $\text{Mor}(\mathcal{C}_{\text{protocol}})$—a **decidable** graph check in the idealized protocol, as opposed to open-ended content filtering. \autoref{fig:security-violations} visualizes this detection process as the identification of "illegal paths" in the interaction graph.

![Prompt injection is detectable as a categorical type violation in the case interaction graph. In the legitimate diagram (top), authority flows NOM→INS→ACC per \autoref{eq:eq-9-1}. Prompt injection (bottom) inserts a cross-category morphism $\phi\colon\text{Webpage}_{\text{ACC}} \to \text{Model}_{\text{INS}}$ — the mechanism by which passive Data attempts to seize Instrument authority (ACC$\to$INS injection, ultimately targeting NOM-level command). The resulting diagram fails to commute, and the adversary's illicit type-reassignment is flagged as a categorical exception by the case-theoretic firewall---transforming prompt injection from an open-ended jailbreak game into a decidable type-checking problem. Generated programmatically from `src/visualization/security_plots.plot_case_interaction_graph()`.](output/figures/security_type_violations.png){#fig:security-violations}

This strict topological firewall extends to multi-agent distributed swarms. In a DisCoCirc discourse model (\autoref{sec:discocirc-discourse}), an indirect prompt injection corresponds to an adversarial entity wire that enters the discourse circuit through a legitimate channel but carries a corrupted state. Because syntactic string diagrams link functorially to the ZX-calculus, we can treat prompt injection analytically as a non-structure-preserving map—securing generative discourse by enforcing strict categorical equivalence constraints across agent interfaces. By rigidly tracking the tensor type of the wire, the system contains the corruption strictly to the `ACC` domain—the wire remains isolated and cannot mathematically fuse with the identity wires governing `NOM` authority.

## Dependent Types, Monoidal Functors, and Multi-Turn Limits

Independent lines of work in **dependent types** and **categorical semantics of neural architectures** motivate the same picture as \autoref{fig:security-violations}: when prompts and roles are assigned types in a disciplined grammar, *some* injection patterns become *type errors* rather than open-ended adversarial search. That alignment is conceptual, not a claim that any particular published Agda encoding of an LLM already enforces our protocol category.

Concretely, a monoidal functor $F\colon \mathcal{C}_{\text{protocol}} \to \mathcal{C}_{\text{impl}}$ between a specified protocol category and its implementation must preserve the tensor product ($F(A \otimes B) \cong F(A) \otimes F(B)$) and the unit. \autoref{fig:monoidal-functor-security} shows a diagnostic audit of such a functor: cells flagged as tensor-preservation failures (for example merges that collapse distinct case roles) are precisely the points at which an implementation silently drops the protocol-category discipline, and they are exactly the structural signatures a categorical firewall can flag before execution.

![Monoidal-functor diagnostics for a protocol-vs-implementation comparison. **Left panel**: the object map $F\colon \mathcal{C} \to \mathcal{D}$ showing a merge of source roles {ACC, NOM, A} into target role ERG and {S, P} into ABS (ACC$\to$NOM collapse flagged as a type violation). **Right panel**: tensor-preservation grid $F(A \otimes B) \stackrel{?}{\cong} F(A) \otimes F(B)$ — **blue cells marked with a check** preserve the tensor product (safe); **orange cells marked with a cross** mark points where tensor preservation fails — i.e., the implementation merges or reassigns roles in ways the protocol category does not license. Generated by `src/visualization/security_plots.plot_monoidal_functor_security()`.](output/figures/monoidal_functor_security.png){#fig:monoidal-functor-security}

A separate limitation is **scalar enriched weights** alone (\autoref{sec:enriched-categories}): in multi-turn discourse, an adversary can in principle iterate small perturbations that cumulatively erode trust encoded only as real-valued hom-weights—analogous to co-evolving attacker–defender dynamics in reinforcement-learning studies of prompt injection [@arlas2025adversarial]. Mitigation in our setting is not “more scalar confidence” but **structural**: a hardened pipeline would treat certain interaction wires under a **non-cartesian** fragment of the monoidal structure—so that, by design, the `ACC` (passive data) wire cannot be copied, discarded, or braided into the `NOM` (commanding agent) wire in ways that Cartesian structure would allow. DisCoCirc-style entity tracking supplies the diagrammatic setting where such constraints can be stated; implementing them in deployed agents remains an engineering and semantics problem, not a theorem already shipped in production LLMs.

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

*The constructions in this section are speculative extensions that follow from the categorical framework but have not been implemented or empirically validated. They are presented as design targets for future research, not as claims about current system capabilities.*

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

## Present-Day Enforcement Mechanisms {#sec:cognitive-security-present-day}

The categorical firewall described above is a formal specification. This section identifies three enforcement mechanisms implementable with existing infrastructure — no quantum hardware required.

**Role immutability via structured system prompts.** The role assignment NOM/ACC/INS/LOC can be encoded as typed slots in a structured system prompt (JSON or XML schema) that the LLM is instructed to treat as read-only metadata. A prompt injection that attempts to promote a webpage string from the `acc_data` slot to the `nom_agent` slot produces a schema-validation failure, catchable before any instruction is executed. This is the categorical firewall reduced to typed-field enforcement: the schema defines the permissible morphisms; violations are detected at the boundary.

**Relational integrity in structured output parsing.** When agent outputs are forced through a structured output schema (e.g., OpenAI function calls, Anthropic tool_use), each output field corresponds to a typed morphism in the interaction category. Role-unlicensed transitions — data tagged `acc` appearing in an `execute` field typed `nom` — become parse errors. The schema acts as a proxy for $\text{Mor}(\mathcal{C}_{\text{protocol}})$: only licensed relational transitions produce valid structured outputs.

**Enriched confidence thresholds for contested assignments.** When the DAIF agent's posterior over case assignment is close to uniform — high entropy, enriched hom-value below a threshold $\tau$ — execution should pause for human review rather than proceeding on an ambiguous assignment. This implements the categorical principle that only morphisms with weight $w \geq \tau$ in the enriched category are "trusted" enough to license downstream actions. The threshold is a tunable parameter; preliminary experimentation suggests $\tau \approx 0.7$ captures the qualitative distinction between confident and contested case assignments in the standard enriched category of \autoref{sec:enriched-categories}.

Together, these three mechanisms — schema-level role immutability, structured-output relational integrity, and entropy-gated execution — provide a layered defense that degrades gracefully: each layer catches a class of injection that the preceding layer misses, and no layer requires modifications to the LLM's internal computation. They are complementary to, not substitutes for, the full categorical enforcement described above; their primary value is that they can be deployed today.

## Limitations and Open Problems {#sec:cognitive-security-limitations}

The protections described above are best understood as *specifications* — sharper-than-prose statements of what a hardened agent stack would need to enforce — rather than as production guarantees about today's deployed systems. Four limitations bound the scope of the claims in this section:

1. **Specification, not enforcement.** Treating prompt injection as a categorical type violation makes detection a *decidable* problem in the idealised protocol category $\mathcal{C}_{\text{protocol}}$. Default LLM stacks do not yet enforce such protocols end-to-end; they parse prompts as undifferentiated token sequences. The case-theoretic firewall can in principle be bolted on at the agent boundary (\autoref{sec:ai-implications}), but no result in this paper claims that an unmodified LLM API rejects ill-typed traces by construction.

2. **Scalar enriched weights are insufficient against multi-turn adversaries.** A patient attacker can iterate small per-turn perturbations whose composed effect, under the inequality $\mathcal{C}(A,C)\geq \mathcal{C}(A,B)\cdot \mathcal{C}(B,C)$, still falls within nominal trust thresholds — analogous to the co-evolutionary attacker–defender dynamics studied in [@arlas2025adversarial]. Mitigation requires *structural* constraints on the monoidal fragment in use (see point 3), not just tighter scalar trust budgets.

3. **Non-cartesian structure is a design target, not an automatic property.** Several defences in this section presuppose that ACC wires *cannot* be copied or discarded into NOM positions. That holds in the non-cartesian fragment of a compact closed category, but it has to be enforced by the runtime: nothing in the underlying tensor algebra of a present-day neural model prevents the implementation from silently broadcasting an ACC wire across a NOM channel. Realising the non-cartesian discipline in deployed agents is an engineering and semantics problem (\autoref{sec:discocirc-discourse}), not a corollary of the theory.

4. **Morita-equivalent attacks are an open frontier.** Topos-theoretic transfer (\autoref{sec:topos-theory}) is a double-edged sword. The same bridge that lets a security proof cross from a typological presentation to a distributional one also lets a corrupted axiom propagate across equivalent presentations. We currently detect this with finite invariant checks (the `topos_theory.check_morita_equivalence` machinery exercised in the test suite); a full account of *Morita-stable* security properties — i.e. invariants that survive every bridge in the relevant equivalence class — is left to future work.

In short, this section defines the *type discipline* a secure agent protocol would have to satisfy and shows that, where it can be enforced, classical and even some quantum-cognitive attacks reduce to decidable type-checking. The remaining gap between specification and enforcement—realizing a deployed categorical-firewall atop present-day LLM APIs—is an open engineering challenge that falls outside the eight formal future directions (**F1**–**F8**) enumerated in \autoref{sec:conclusion}; it is flagged in \autoref{sec:ai-implications} as a structural design target for typed agent protocols.
