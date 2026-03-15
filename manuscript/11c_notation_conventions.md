# Appendix: AI Protocols, Diagrammatic Reasoning, and Notation Conventions

## H. AI and Communication Protocols

| Term | Symbol | Definition | First Use |
| :--- | :---: | :--- | :---: |
| A2A Protocol | — | Google's Agent-to-Agent protocol for cross-framework agent communication via HTTP/JSON-RPC | §9 |
| ACP | — | Agent Communication Protocol; standardizes messaging formats across agents, apps, and humans | §9 |
| ANP | — | Agent Network Protocol; three-layer architecture for trusted distributed agent interaction | §9 |
| Categorical deep learning | — | Deep learning approached through the lens of category theory (Gavranović et al.) | §9 |
| Double Categorical Systems Theory (DCST) | — | Framework using 2-categories (horizontal + vertical composition) for explainable autonomous AI | §9 |
| Functorial encryption | — | Semantic cryptography: applying a secret functor to map plaintext categories into ciphertext categories | §9 |
| lambeq | — | Quantum Natural Language Processing pipeline compiling DisCoCat diagrams to quantum circuits | §9 |
| MCP | — | Model Context Protocol; standardizes how AI agents access external tools and data sources | §9 |
| Parameterized optics / lenses | — | Categorical constructions modeling neural network components (Gavranović); attention heads as optics | §9 |
| QNLP | — | Quantum Natural Language Processing; quantum computation on DisCoCat sentence diagrams | §9 |
| Semantic cryptography | — | Encrypting compositional meaning structures (functorial encryption, diagram obfuscation, weight masking) | §9 |

## I. Diagrammatic Reasoning

| Term | Symbol | Definition | First Use |
| :--- | :---: | :--- | :---: |
| Cognitively privileged representation | — | Representation format that leverages perceptual and spatial cognition for inference | §1 |
| Diagram depth | — | Length of the longest input-to-output path through boxes; measures derivational complexity | §4 |
| Existential graphs | — | Peirce's graphical logic system conducting first-order logic entirely diagrammatically | §7 |
| Free ride | — | Shimojima's term: information extracted from a diagram without explicit inference steps | §1 |
| Hybrid reasoning | — | Giardino's term: reasoning combining perceptual pattern recognition with theoretical knowledge | §1 |
| Inferential instrument | — | Manders's term: a diagram whose spatial properties encode proof-relevant information | §6 |
| Joyal–Street theorem | — | Soundness and completeness of string-diagrammatic reasoning for monoidal categories | §3 |
| Normal form | $D_{\text{nf}}$ | Canonical form of a diagram obtained by rewriting; unique up to the axioms | §4 |

## J. Notation Conventions

| Convention | Meaning |
| :--- | :--- |
| $\mathcal{C}, \mathcal{D}$ | Categories |
| $\mathcal{V}$ | Enrichment base (monoidal category, typically $([0,1], \cdot, 1)$) |
| $\mathcal{U}$ | Universal (maximal) case category |
| $\mathcal{L}$ | Language-specific case category |
| $\mathcal{E}_{\mathbb{T}}$ | Classifying topos of theory $\mathbb{T}$ |
| $f, g, h$ | Morphisms |
| $F, G$ | Functors |
| $\alpha, \beta$ | Natural transformations |
| $n, s$ | Basic pregroup types: noun, sentence |
| $n^l, n^r$ | Left and right adjoints of type $n$ |
| $n_{\text{NOM}}, n_{\text{ACC}}$ | Case-subscripted noun types (e.g., nominative noun, accusative noun) |
| $N, S$ | Noun space and sentence space under the meaning functor |
| $N_{\text{NOM}}, N_{\text{ACC}}, \ldots$ | Case-specific vector subspaces in case-enriched DisCoCat |
| $\overrightarrow{\text{word}}$ | Word vector (column vector in noun space $N$) |
| $\overleftrightarrow{\text{verb}}$ | Verb tensor (element of $N \otimes S \otimes N$ for transitive verbs) |
| $\mathbf{Preg}$ | Category of pregroup types and reductions |
| $\mathbf{FVect}$ / $\mathbf{FdVect}$ | Category of finite-dimensional vector spaces and linear maps |
| $\mathbf{FHilb}$ | Category of finite-dimensional Hilbert spaces and linear maps |
| $\mathbf{Qubit}$ | Category of qubit systems with tensor product structure |
| $\mathbf{Set}$ | Category of sets and functions |
| $\otimes$ | Tensor product (monoidal product, type concatenation) |
| $\circ$ | Composition of morphisms |
| $\Rightarrow$ | Natural transformation between functors |
| $\simeq$ | Categorical equivalence |
| $\leq$ | Preorder relation on types (derivability) |
| $\gamma$ | Discount factor in distributional RL return computation |
| $w \in [0,1]$ | Enriched morphism weight (proto-role satisfaction degree) |
| $\varepsilon$ | Prediction error (active inference); also compact closure counit |
| $\eta$ | Compact closure unit (cap); also learning rate in some contexts |
| $\rho$ | Density operator (quantum state) |
| $[@key]$ | Parenthetical citation |
| `[-@key]` | Suppress-author citation |
| `\autoref{...}` | Automatic cross-reference (section or figure) |
