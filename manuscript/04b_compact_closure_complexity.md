
# Compact Closure and Diagram Complexity: Snake Equation and Valency Metrics {#sec:compact-closure-complexity}

## The Snake Equation Powers Every Pregroup Contraction

### The Snake Equation (Zigzag Identity)

The essential algebraic engine driving DisCoCat is the strict **compact closure** of the governing pregroup category. For every lexical type $n$, the corresponding adjunction maps—$\eta_n: 1 \to n \otimes n^r$ (the cap expansion) and $\varepsilon_n: n^r \otimes n \to 1$ (the cup contraction)—must mathematically satisfy the fundamental **snake equation** (also known as the topological zigzag identity):

\begin{equation}
(\varepsilon_n \otimes 1_n) \circ (1_n \otimes \eta_n) = 1_n
\label{eq:eq-4-3}
\end{equation}

Translated into intuitive string-diagrammatic terms, a cup geometrically composed with a cap bridging adjacent wires immediately "straightens out" into a solid identity wire—a topological zigzag seamlessly canceling into a continuous straight line. This foundational axiom is not merely a geometric curiosity: it physically functions as the *engine* powering every valid pregroup type reduction. Every recorded grammatical contraction (e.g., a noun canceling against an active verb argument slot) constitutes a direct instance of the cup map $\varepsilon{}$, and every grammatical expansion instantiates the cap map $\eta{}$. The continuous snake equation algebraically guarantees that these interwoven contractions and expansions remain globally well-behaved—ensuring they can be freely inserted and removed without ever altering the final semantic meaning of the derivation.

Cognitively, the snake equation provides an immediate *visual proof* of coherence. A cognitive agent inspecting a string diagram can verify well-formedness by confirming that all zigzags cancel—a purely spatial operation requiring no sequential algebraic computation, and thus instantiating Shimojima's [-@shimojima1996reasoning] free-ride inference in its most direct form.

![The snake equation is the algebraic engine powering every pregroup type reduction. The compact closure axiom (\autoref{eq:eq-4-3}) rendered by DisCoPy: **left panel** shows the zigzag $(\varepsilon_n \otimes 1_n) \circ (1_n \otimes \eta_n)$ where a Cup $\varepsilon{}$ composed with a Cap $\eta{}$ forms a snake; **right panel** shows the identity wire $1_n$ it equals. Verified computationally via `diagram.normal_form() == Id(Ty('x'))`. Each pregroup contraction (noun canceling with verb argument) is an instance of $\varepsilon{}$; the snake equation guarantees that cup-cap pair insertions and removals leave derivations invariant (cf. \autoref{sec:categorial-grammar}).](output/figures/discopy_snake.png){#fig:discopy-snake}

### Four Metrics Quantify Derivational Complexity

The algebraic properties of pregroup diagrams support quantitative analysis of derivational complexity. Our `complexity_metrics` module implements four complementary measures using the DisCoPy library:

1. **Box count**: The number of lexical entries (Word boxes) in the diagram, corresponding to the sentence's word count from the type-logical perspective. A transitive sentence has 3 boxes (subject, verb, object); a ditransitive sentence has 4 or more.

2. **Cup/Cap count**: The number of contraction and expansion operations. Cups (denoted $\varepsilon{}$) count argument consumption; caps (denoted $\eta{}$) count argument introduction. The cup count directly reflects verb valency: an intransitive verb requires 1 cup, a transitive verb 2, and a ditransitive verb 3.

3. **Normal form**: A diagram is in *normal form* if no further simplifications (zigzag cancellations, box reordering) are possible. The `normal_form()` operation computes this canonical representative of the diagram's equivalence class. Normal form preservation under algebraic manipulation provides a correctness check for compositional operations.

4. **Syntactic complexity score**: A composite metric defined as:

\begin{equation}
\text{complexity}(D) = w_b \cdot |D|_{\text{box}} + w_c \cdot |D|_{\text{cup}} + w_d \cdot \text{depth}(D)
\label{eq:eq-4-4}
\end{equation}

where $|D|_{\text{box}}$, $|D|_{\text{cup}}$, and $\text{depth}(D)$ are the box count, cup count, and depth respectively, and $w_b, w_c, w_d$ are configurable weights (defaulting to equal weights). The *depth* of a diagram is the length of the longest path from input to output, counting boxes. Deeper diagrams encode more complex syntactic derivations—a ditransitive sentence like "Alice gave Bob a book" (depth 7) is structurally more complex than a simple intransitive "Alice runs" (depth 3).

The `compare_diagrams()` function applies these metrics across a collection of diagrams, producing tabular comparisons suitable for cross-linguistic analysis. \autoref{fig:complexity-comparison} visualizes these metrics across sentence types of increasing valency, demonstrating the monotonic relationship between argument structure and derivational complexity.

![Argument-structure complexity maps monotonically onto diagram topology. Complexity metrics (\autoref{eq:eq-4-4}) plotted across ten sentence types of increasing valency: from intransitive "Alice runs" (2 boxes, 1 cup) through transitive (3 boxes, 2 cups), ditransitive (4 boxes, 3 cups), and adjunct-stacked constructions up to "fast Alice gave Bob book quickly" (8 boxes, 4 cups). Cup count $|D|_{\text{cup}}$ increases monotonically with verb valency and adjunct stacking, confirming that argument-structure complexity is a topological invariant of the diagram. Actual sentences are overlaid in the plot; cup count is computable from the DisCoPy diagram via `len([b for b in diagram.boxes if isinstance(b, Cup)])`.](output/figures/complexity_comparison.png){#fig:complexity-comparison}

These metrics connect naturally to the enriched framework of \autoref{sec:enriched-categories}: diagram depth serves as a syntactic complexity proxy that can be incorporated into the enriched hom-value, providing a principled bridge between type-logical derivation cost and distributional semantic distance. Discourse-level persistence of entity wires (DisCoCirc) is developed in \autoref{sec:discocirc-discourse}. For multi-agent security, when tracking networks isolate an adversarial identity wire (a prompt injection) covertly attempting to merge with an ongoing command wire across communication boundaries, the circuit topology can flag the type violation before execution (\autoref{sec:cognitive-security}).
