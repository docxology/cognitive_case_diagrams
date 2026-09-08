# Duality Identities and Diagram Complexity {#sec:compact-closure-complexity}

Cups and caps satisfy snake identities in the appropriate category with duals. A wire bent through a matching evaluation and coevaluation is equal to its identity morphism. The project constructs both sides and checks normal forms with DisCoPy; this is an executable algebraic example, not a new theorem.

![Executable snake-equation diagrams and the identity wire. Equality is tested within the selected DisCoPy calculus.](output/figures/discopy_snake.png){#fig:discopy-snake}

![Stepwise illustration of a snake identity. The allowed categorical equation licenses straightening the wire; geometric resemblance alone would not.](output/figures/snake_equation_unpacking.png){#fig:snake-unpacking}

The complexity utilities report box count, cup count, cap count, depth, width, and normal-form size. The configurable score used by the examples is

$$
\kappa(D)=${complexity_weight_words}N_{\mathrm{lex}}+${complexity_weight_cups}N_{\mathrm{cup}}+${complexity_weight_caps}N_{\mathrm{cap}}+${complexity_weight_depth}\,d(D).
$$ {#eq:eq-4-4}

Here `count_words` counts every non-Cup/non-Cap box; in diagrams containing a Swap, this is broader than a linguistic word count. The four coefficients are the declared defaults of `syntactic_complexity_score()` in the source, injected at build time; they are chosen weights, not a fitted psycholinguistic model. DisCoPy depth and width describe a particular representation and do not directly determine qubit count, hardware depth, processing time, or cognitive difficulty without an explicit compilation or measurement model.

![Complexity measurements for the generator's selected diagrams. Scores depend on the assigned lexical decomposition and the injected weights. The collection is illustrative rather than a benchmark sampled from a language.](output/figures/complexity_comparison.png){#fig:complexity-comparison}

The legacy `compute_pqc_decoherence_proxy()` derives a synthetic decoherence-rate field from a caller-supplied noise baseline, excess cups over caps, and an unsourced exponential amplification factor; the container also carries this section's base complexity score as its base field. Despite legacy field names, it computes neither topological homology nor a physical decoherence rate. No physical or security conclusion in this manuscript relies on that score.
