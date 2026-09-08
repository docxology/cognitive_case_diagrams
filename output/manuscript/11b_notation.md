# Appendix B: Notation and Conventions {#sec:notation}

## Linguistic labels {#sec:notation-linguistic}

S, A, and P denote the argument primitives defined in [@sec:case-systems]. NOM, ACC, GEN, DAT, INS, LOC, ABL, VOC, ERG, and ABS are case labels used in the examples. Their interpretation depends on the language or modeling context. Case color is redundant with a written label; it does not encode evidence strength.

## Algebra and probabilities {#sec:notation-categorical}

| Symbol | Meaning here |
| :--- | :--- |
| $A,B,C$ | Objects or specified role labels |
| $f:A\to B$ | A typed arrow; its exact semantics must be supplied |
| $g\circ f$ | First $f$, then $g$ |
| $\otimes$ | Monoidal product in a specified category |
| $n,s,n^l,n^r$ | Noun, sentence, and adjoint types |
| $Z_{ij}$ | Candidate or verified hom-value, distinguished in context |
| $|Z|$ | Weighting/coweighting sum when defined |
| $q,p,L,T$ | Posterior, prior, likelihood, row-stochastic transition matrix |
| $F$ | Variational free energy for a specified fixed model |
| $G$ | Caller-defined policy score in the compatibility API |
| $\tau,Q(\tau)$ | Quantile probability level and value |
| $E_c,\rho$ | POVM effect and density matrix |
| $W_p$ | Wasserstein distance of order $p$ under a stated reconstruction |

Table: Symbols used in the mathematical and computational examples. {#tbl:notation}

Natural logarithms give entropy and KL in nats. Similarity weights and synthetic scores are dimensionless unless a scale is explicitly supplied. Variances have squared score units. ERP-inspired amplitudes are uncalibrated model units; waveform time coordinates are milliseconds. `return`, `Bellman`, `Bethe`, `MonoidalFunctor`, and `ClassifyingTopos` in legacy APIs do not override the narrower operational definitions in the text.
