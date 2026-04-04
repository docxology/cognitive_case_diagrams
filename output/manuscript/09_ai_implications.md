
# Categorical AI Protocols {#sec:ai-implications}

## A2A, MCP, ACP, ANP Are Missing Compositional Semantics

The categorical framework developed in the preceding sections—case categories, functorial semantics, enriched structure, and diagrammatic reasoning—provides a structural response to an emerging challenge in modern AI: supplying typed, compositional message semantics that resist semantic collapse.

Current multi-agent AI systems communicate via flat standardized protocols. For instance, the **Model Context Protocol (MCP)** [@anthropic2024mcp] manages tool access by exchanging unstructured `JSON-RPC` payloads. Consider a standard MCP invocation mapping an LLM's intention to a database:

```json
{
  "method": "tools/call",
  "params": {
    "name": "access_database",
    "arguments": { "query": "DROP TABLE users" }
  }
}
```

This payload is structurally blind to its own pragmatic implications. It possesses no inherent algebraic compositionality and enforces no relational typing on the physical execution pathways. Frameworks like Google's Agent-to-Agent (A2A) [@google2025a2a], the Agent Communication Protocol (ACP) [@acp2025protocol], and the Agent Network Protocol (ANP) [@anp2025protocol] share this vulnerability: they validate the *shape* of the JSON schema, but rely purely on probabilistic inference to govern the *topology of the interaction*.

Category theory injects this missing protective layer. By compiling agent interactions into strict string diagrams, messages cease to be flat strings and instead become typed morphisms traversing a case category.

## NOM Is the Requester, INS Is the Tool, DAT Is

The eight-case framework of CEREBRUM [@friedman2024cerebrum] maps rigidly onto the operational constraints of multi-agent execution. In a Categorical Communication Protocol, interactions are legally licensed only if their computational wiring diagrams satisfy a strict grammatical type-signature:

| Case Role | Agent System Analogue | Protocol Function Type |
| :--- | :--- | :--- |
| **NOM (Agent)** | Active Requester | Initiator of action policies ($X_{\text{NOM}}$) |
| **INS (Instrument)** | Tool / API Module | Means of transforming state ($X_{\text{INS}}$) |
| **ACC (Patient)** | Passive Data Target | Resource being modified ($X_{\text{ACC}}$) |
| **DAT (Recipient)** | Designated Receiver | Endpoint for information flow ($X_{\text{DAT}}$) |
| **LOC (Context)** | System Prompt | Immutably binds boundary behavior ($X_{\text{LOC}}$) |

This turns prompt engineering into rigorous compilation. Instead of parsing a prompt to heuristically guess caller intent, a categorical agent processes interactions strictly as algebraic reductions. An MCP tool invocation [@anthropic2024mcp] (`NOM` using `INS` to modify `ACC` and yield abstract `DAT`) becomes a formalized tensor contraction:

\begin{equation}
\text{Interaction Trace:} \quad \left( \text{Agent}_{\text{NOM}} \otimes \text{Tool}_{\text{INS}} \otimes \text{Data}_{\text{ACC}} \right) \xrightarrow{\text{execute}} \text{Response}_{\text{DAT}}
\label{eq:ai-interaction-trace}
\end{equation}

If an untyped internal subsystem (e.g., an adversarial user-uploaded document) attempts to independently forge a command, the operation simply fails to compile. The document lacks a valid tensor wire bridging from its marginalized $\text{ACC}$ domain back into the execution flow governing $\text{INS}$. The grammar ensures every interaction is structurally typed, guaranteeing safety properties akin to **memory safety, but for agentic volition**.

## Transformers Through Gavranović's Lens: Attention as Parameterized Optics

Gavranović [-@gavranovic2024thesis; -@gavranovic2024categorical] unifies feedforward, recurrent, and attention layers as **parameterized optics**—the same wiring-diagram perspective used for DisCoCat cups in \autoref{sec:categorical-semantics}. Attention heads then appear as *learned* relational couplings over token sequences, with weights playing the role of graded hom-values (\autoref{sec:enriched-categories}). LLMs discover these contractions from data; DisCoCat fixes admissible contraction *shapes* by grammar. Distributional Active Inference [@akgul2026distributional] is one setting where explicit DisCoCat-style guardrails can sit alongside a large distributional backbone.

## Interpretability for Free: DisCoCat Diagrams Make Every Compositional Step Human-Readable

The lambeq library [@lorenz2023lambeq] demonstrates that string diagrams provide a practical interface between linguistic structure and machine learning. As an "efficient high-level Python library for Quantum NLP," lambeq translates sentences into string diagrams, converts diagrams into parameterized circuits (quantum or classical), and trains parameters end-to-end on NLP tasks. The diagrammatic representation serves dual purposes: it is both the mathematical specification of the model *and* a human-readable explanation of what the model computes.

This interpretability property is crucial for AI safety and alignment. Where transformer architectures produce opaque attention patterns, a DisCoCat model deployed via string diagrams produces derivation trees with explicit compositional semantics—every box and wire has a linguistic interpretation. Extending this to agent communication, a categorical protocol would produce not just working message exchanges but *interpretable* interaction diagrams where each step's relational role is transparent.

## Multi-Turn Dialogue as Discourse Circuit

The DisCoCirc framework [@defelice2022discocirc] extends compositional semantics from single sentences to multi-sentence discourse by introducing *state wires* that persist across sentence boundaries. This architecture maps directly onto multi-turn agent dialogues:

- **Entity wires** correspond to persistent agent identities across communication rounds
- **State updates** correspond to belief revisions triggered by incoming messages
- **Coreference resolution** corresponds to entity tracking across protocol sessions
- **Discourse coherence** corresponds to protocol correctness constraints

In a multi-agent system, a DisCoCirc-style protocol would track the evolving states of all participating agents as persistent wires in a circuit diagram, with each message exchange represented as a box that transforms the relevant wires. Protocol correctness reduces to a categorical property: the circuit must type-check, meaning all wire types must match at connection points—precisely the condition that case marking enforces in natural language.

## Multi-Agent Equilibria as Fixed Points of an Enriched Functor

The "parametrised optics" framework developed within categorical cybernetics "provides a general-purpose foundation for the study of controlled processes" [@capucci2021towards] applicable to compositional game theory as a multi-agent framework. In this setting, agents are modeled as lenses (or optics) that observe the environment through one channel and act through another, with the overall system behavior emerging from the composition of individual agent behaviors.

This connects to our enriched case framework (\autoref{sec:enriched-categories}): the precision weights on morphisms correspond to the utility parameters of game-theoretic agents, and the composition inequality $\mathcal{C}(A,C) \geq \mathcal{C}(A,B) \cdot \mathcal{C}(B,C)$ corresponds to the sub-optimality of indirect communication chains. Equilibria in the multi-agent game correspond to fixed points of the enriched functor, where no agent can improve its utility by changing its case-role assignment.

## DCST: Two-Dimensional Morphisms Model Both Sequential Interaction and Hierarchical Nesting

Recent foundational work on Double Categorical Systems Theory (DCST) formalizes open and interacting dynamical systems using double categories [@myers2023double]. DCST extends ordinary category theory with a second dimension of morphisms (2-morphisms), allowing simultaneous modeling of:

1. **Horizontal composition**: Sequential chaining of agent interactions (morphism composition)
2. **Vertical composition**: Hierarchical nesting of subsystems within larger systems (2-morphism composition)

For case theory, the double-categorical extension allows us to model both the *within-sentence* case structure (horizontal) and the *discourse-level* case structure (vertical) within a single algebraic framework—precisely the unification that DisCoCirc achieves pragmatically.

## Five Properties of a Categorical Protocol

The synthesis of these developments suggests a research program: developing **categorical communication protocols** that combine the engineering robustness of existing standards (A2A, MCP, ACP) with the compositional semantics of categorical linguistics. Such a protocol would:

1. **Type-check interactions**: Every message exchange would be relationally typed by case roles, preventing structural communication errors at the protocol level
2. **Compose transparently**: Multi-step interactions would compose algebraically, with diagrammatic representations providing interpretable audit trails
3. **Transfer across implementations**: Topos-theoretic bridges (\autoref{sec:topos-theory}) would carry **topos-level** correctness conditions from one categorical formalization to any Morita-equivalent formulation, so that shared invariants need not be re-verified separately
4. **Scale via enrichment**: Distributional proximity measures (\autoref{sec:enriched-categories}) would enable graceful degradation under uncertainty, with enriched weights encoding confidence in message content
5. **Ground in cognitive architecture**: The active inference foundation (\autoref{sec:cognitive-integration}) would ensure that artificial agents communicate using the same relational structure that evolution has optimized for biological cognition

**Protocol-level formalization.** Concretely, a categorical communication protocol defines a category $\mathcal{P}$ where objects are agent states annotated with case roles and morphisms are typed message exchanges:

\begin{align}
\text{Request}(q,\; \text{NOM} \to \text{INS}) &: \text{User}_{\text{NOM}} \to \text{Model}_{\text{INS}} \label{eq:protocol-request} \\
\text{ToolCall}(t,\; \text{INS} \to \text{ACC}) &: \text{Model}_{\text{INS}} \to \text{Tool}_{\text{ACC}} \label{eq:protocol-toolcall} \\
\text{Result}(r,\; \text{ACC} \to \text{DAT}) &: \text{Tool}_{\text{ACC}} \to \text{Output}_{\text{DAT}} \label{eq:protocol-result}
\end{align}

Protocol correctness reduces to verifying that the composition $\text{Result} \circ \text{ToolCall} \circ \text{Request}$ is a well-typed morphism in $\mathcal{P}$—a check that can be performed at compile time, not just at runtime. The DisCoCirc extension enables tracking agent state evolution across multi-turn dialogues: each turn updates the agent's state wire, and the discourse-level composition verifies that information flows respect case-role constraints across the entire conversation. This formalization provides a bridge between the flat JSON payloads of current A2A/MCP implementations and the rich compositional semantics that categorical linguistics provides.
