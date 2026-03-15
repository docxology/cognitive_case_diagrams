
# Appendix: Active Inference, Quantum, and Type-Theoretic Notation

## E. Active Inference and Cognitive Models

| Term | Symbol | Definition | First Use |
| :--- | :---: | :--- | :---: |
| Active inference | — | Framework in which perception and action are unified as variational free energy minimization | §7 |
| Active sampling | — | Agent's selection of actions to confirm or update case assignments via sensory evidence | §7 |
| Belief updating | — | Bayesian posterior computation: revising generative model parameters given new observations | §7 |
| CEREBRUM | — | Case-Enabled Reasoning Engine with Bayesian Representations Using Models; treats AI models as case-bearing entities | §7 |
| Distributional Active Inference (DAIF) | — | Extension replacing scalar value summaries with full return distributions in active inference | §7 |
| Distributional RL | — | Reinforcement learning operating on full return distributions rather than scalar expected values | §7 |
| Free energy | $F$ | Variational bound on surprisal; $F = D_{KL}[q(\theta) \parallel p(\theta \mid o)] - \ln p(o)$ | §7 |
| Free energy principle (FEP) | — | The principle that self-organizing systems maintain themselves by minimizing surprisal | §7 |
| Garden-path reanalysis | — | Restructuring of case assignments when incoming evidence contradicts the current parse | §7 |
| Generative model | $p(o, s)$ | Joint probability model over observations $o$ and hidden states $s$ | §7 |
| Markov blanket | — | Statistical boundary separating internal states from external environment; defines agent boundary | §7 |
| N400 | — | Event-related brain potential peaking ~400ms post-stimulus; indexes semantic prediction error | §7 |
| P600 | — | Event-related brain potential peaking ~600ms post-stimulus; indexes syntactic prediction error | §7 |
| Perceptual inference | — | Updating internal beliefs to better predict current observations (reduce prediction error) | §7 |
| Precision weighting | — | Weighting of prediction errors by inverse variance; enriched morphism weights serve this role | §7 |
| Prediction error | $\varepsilon$ | Difference between predicted and observed sensory input; drives belief updating | §7 |
| Push-forward measure | $T_\# \mu$ | Distribution obtained by transforming a base measure $\mu$ through a function $T$ | §7 |
| Situation semantics | — | Framework representing meaning as relations between situations (Barwise and Perry 1983) | §7 |
| Surprisal | $-\ln p(o)$ | Negative log-probability of an observation under the generative model | §7 |
| Variational free energy | $F[q]$ | Functional upper bound on surprisal minimized by approximate posterior $q$ | §7 |

## F. Quantum and Topological Terms

| Term | Symbol | Definition | First Use |
| :--- | :---: | :--- | :---: |
| Amplituhedron | — | Positive geometry encoding scattering amplitudes; connected to TQNN execution traces | §8 |
| $\dagger$-compact category | — | See $\dagger$-compact closed category in §B | §8 |
| CPTP map | — | Completely Positive Trace-Preserving map; quantum channel between Hilbert spaces | §8 |
| Density operator | $\rho$ | Positive semidefinite trace-one operator encoding a quantum (or semantic) state | §8 |
| Execution trace | — | Record of operations in a quantum computation; connects TQNNs to amplituhedra | §8 |
| Generalized flow | — | Graph-theoretic property ensuring deterministic circuit extraction from ZX-diagrams | §8 |
| Hadamard box | $H$ | ZX-calculus element implementing the Hadamard gate; converts between Z and X bases | §8 |
| Holographic screen | — | Information boundary between interacting quantum systems carrying a qubit array | §8 |
| Pointer state | — | Preferred quantum state selected by a QRF; determines the measurement basis | §8 |
| Quantum contextuality | — | Quantum correlations that reduce cohomological obstructions to semantic alignment | §8 |
| Quantum discord | — | Quantum correlation measure equal to integrated semantic information in sheaf framework | §8 |
| Quantum key distribution (QKD) | — | Protocol providing information-theoretic security for quantum communication channels | §9 |
| Quantum reference frame (QRF) | — | Observer-relative frame selecting pointer states and inducing decoherence | §8 |
| Quantum semantic sheaf | $(H, F, \rho)$ | Triple of Hilbert spaces, CPTP channels, and density operators over a communication graph | §8 |
| Reshetikhin–Turaev invariant | — | Topological invariant assigning to a ribbon graph a linear map via TQFT | §8 |
| Sheaf cohomology | $H^n(\mathcal{F})$ | Cohomological obstruction classes governing alignment in a quantum semantic sheaf | §8 |
| Spin-network | — | Graph with edges labeled by representations and vertices by intertwiners; TQFT data | §8 |
| Spider | — | Elementary ZX-diagram node (Z-spider or X-spider) representing a quantum operation | §8 |
| TQFT | — | Topological Quantum Field Theory; functor from cobordisms to Hilbert spaces | §8 |
| TQNN | — | Topological Quantum Neural Network; QNN reformulated via spin-networks and TQFT | §8 |
| Turaev–Viro invariant | — | State-sum TQFT invariant; implements quantum error-correcting codes in TQNNs | §8 |
| ZX-calculus | — | Graphical language for quantum circuits using Z-spiders, X-spiders, and Hadamard boxes | §8 |
| ZX-diagram | — | String diagram in a $\dagger$-compact closed category representing a quantum process | §8 |
| ZX rewrite rule | — | Graph-theoretic transformation preserving the semantics (linear map) of a ZX-diagram | §8 |

## G. Logical and Type-Theoretic Terms

| Term | Symbol | Definition | First Use |
| :--- | :---: | :--- | :---: |
| $\beta$-reduction | — | Computational reduction step in $\lambda$-calculus; corresponds to cut elimination in proofs | §3 |
| Church–Rosser property | — | Confluence of $\beta$-reduction: all reduction sequences converge to the same normal form | §3 |
| Curry–Howard isomorphism | — | Correspondence between proofs and programs, propositions and types | §3 |
| Cut elimination | — | Proof normalization procedure removing intermediate lemmas; corresponds to $\beta$-reduction | §3 |
| Graded type theory | — | Extension of type theory tracking effects (e.g., evidentiality) via graded modalities | §3 |
| Lambek calculus | — | Non-commutative intuitionistic linear logic for syntactic type assignment | §3 |
| Left residual | $A \backslash B$ | Type of an expression that, given $A$ to the left, produces $B$ | §3 |
| Residuation law | $A \otimes B \leq C \iff A \leq C / B \iff B \leq A \backslash C$ | Fundamental axiom connecting the three connectives of the Lambek calculus | §3 |
| Right residual | $B / A$ | Type of an expression that, given $A$ to the right, produces $B$ | §3 |
