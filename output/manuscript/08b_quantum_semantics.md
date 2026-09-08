# Case Labels as Measurement Outcomes {#sec:quantum-semantics}

A positive-operator-valued measure (POVM) is a family of positive semidefinite Hermitian effects $E_c$ that sum to the identity. A density matrix $\rho$ is positive semidefinite and Hermitian with trace one. Under these assumptions,

$$
P(c\mid\rho)=\operatorname{Tr}(E_c\rho),\qquad\sum_cP(c\mid\rho)=1.
$$ {#eq:eq-8-1}

The sum identity follows by linearity of trace. The implementation checks finite entries, dimensions, Hermiticity, positivity, completeness, and density normalization within explicit floating-point tolerances. A symmetric eigenvalue routine alone would not validate Hermiticity, which is checked separately. An individual effect is also required to lie below the identity.

`crisp_case_povm()` constructs orthogonal coordinate projectors. A projective measurement does not guarantee a deterministic outcome for every state: a mixture or superposition can yield several outcomes. The convenience `semantic_state()` constructs a diagonal mixture from supplied nonnegative role weights; it does not create coherence or entanglement.

![Born-rule probabilities for orthogonal projectors and the synthetic diagonal mixture, with computed outcome probabilities 0.8 on NOM, 0.1 on ACC, and 0.1 on DAT. Remaining outcomes have zero probability. These bars are computed traces; they show neither interference fringes nor a continuous semantic-state density.](output/figures/quantum_povm_probabilities.png){#fig:quantum-povm}

`graded_case_povm()` creates diagonal effects from normalized role weights on basis coordinates. `fluid_s_povm()` rotates a two-role measurement according to a supplied context parameter. These are finite mathematical models. Interpreting their outcomes as case assignments is a chosen labeling convention, not a proof that grammatical alignment equals a quantum reference frame.

A general caller can provide a coherent density matrix directly, subject to validation. Demonstrating an interference effect would require a specified state family and measurement whose probabilities depend on off-diagonal components. The canonical figure uses commuting diagonal objects and admits an ordinary classical probability interpretation. No physical quantum advantage or semantic channel-capacity result is established. The seeded completeness check of the canonical example is reported in [@sec:exp-controls].
