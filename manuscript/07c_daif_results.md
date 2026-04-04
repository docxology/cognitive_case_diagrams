# DAIF: The Convergence of Distributional Semantics and RL {#sec:daif-results}

A remarkable convergence has emerged between *distributional semantics* in linguistics and *distributional reinforcement learning* in machine learning, mediated by active inference. Akgül et al. [-@akgul2026distributional] parameterize this in **Distributional Active Inference (DAIF)**, which embeds active inference within the distributional RL framework of Bellemare, Dabney, and Munos [-@bellemare2017distributional]. Where classical RL optimises *expected* returns (scalar values), distributional RL models the *full distribution* of returns—a shift from point estimates to distributional representations that parallels the shift from symbolic to distributional semantics in linguistics. Crucially, as recent convergences demonstrate, estimating full distributions over discounted returns substantially enhances sample efficiency and buffers aleatoric uncertainty, factors essential for biological plausibility during rapid linguistic parsing.

The terminological collision between "distributional" in distributional semantics and "distributional" in distributional RL is not mere homonymy—it reflects a deep structural parallel. In both domains, the core computational move is the same: **replacing scalar summaries with full distributional representations.** In linguistics, this means contextualizing word identities via probability distributions (Firth's [-@firth1957papers] company-keeping principle). In reinforcement learning, it replaces expected-value estimates with quantile-approximated return distributions. In active inference, it replaces point estimates of states with variational posterior distributions. The enriched-categorical framework of \autoref{sec:enriched-categories} provides the unifying abstraction: all three are instances of $[0,1]$-enriched categories where hom-values encode distributional proximity rather than rigid identity.

This section presents the complete implementation and quantitative results of the `src/daif/` subpackage—${daif_modules_word} modules, ${daif_symbols} public symbols, ${daif_tests} automated tests—covering six major computational contributions: push-forward returns (\autoref{sec:daif-pushforward}), quantile TD and implicit quantile networks (\autoref{sec:daif-quantile}), variational message passing and Bethe free energy (\autoref{sec:daif-vmp}), policy selection and expected free energy (\autoref{sec:daif-policy}), unifying ERP amplitude profiles (\autoref{sec:daif-erp}), and convergence diagnostics (\autoref{sec:daif-metrics}).

## Push-Forward Returns and the Distributional Bellman Operator {#sec:daif-pushforward}

The formal architecture of DAIF proceeds through three stages: (1) reconstructing active inference via variational Bayesian inference on a controlled Markov process; (2) defining a *push-forward* operation that iteratively maps latent-space trajectories to return distributions; and (3) deriving a temporal-difference quantile-matching algorithm that achieves active inference's sample-efficiency advantages within a model-free computational architecture. This permits far-sighted parsing without explicit transition modeling:

\begin{equation}
\mathbb{E}\left[\sum_{t=0}^{\infty} \gamma^t R(x_t, a_t) \mid x_0, a_0\right] = \int_{\mathcal{S}^{\mathbb{N}_+}} R \circ f \, d(\mathbf{S}_{\#} \mathbb{P}_{x_0, a_0}^{P_\pi})
\label{eq:eq-7-1}
\end{equation}

where $\mathbf{S}_{\#}$ denotes the push-forward measure on representation paths, $f: \mathcal{S} \to \mathcal{X}$ is the stochastic decoder, and $\gamma \in (0,1)$ is the discount factor. The `push_forward_return()` function in `src/daif/core.py` computes this via an atomised categorical projection over $N_{\mathrm{atoms}}$ support points $\{z_i\}_{i=1}^{N_{\text{atoms}}}$ spanning $[V_{\min}, V_{\max}]$—the C51 architecture of Bellemare et al. [-@bellemare2017distributional]:

\begin{equation}
Z(s,a) = \sum_{i=1}^{N_{\text{atoms}}} p_i(s,a) \cdot \delta_{z_i}
\label{eq:eq-7c-c51}
\end{equation}

where $p_i(s,a)$ is the probability assigned to support point $z_i$ and $\delta$ is the Dirac delta mass. The distributional Bellman operator $\mathcal{T}^{\pi}$ then maps return distributions forward:

\begin{equation}
\mathcal{T}^{\pi} Z(s,a) \stackrel{d}{=} R(s,a) + \gamma Z(S', A'), \quad S' \sim P(\cdot|s,a), \; A' \sim \pi(\cdot|S')
\label{eq:eq-7c-bellman}
\end{equation}

For case-theoretic reasoning, DAIF implies a computational architecture in which case assignment operates distributionally at every level: the agent maintains not a single case diagram but a *distribution over case diagrams*, weighted by their posterior probability given the observed linguistic evidence. This distributional perspective on case assignment aligns naturally with the graded proto-role structure of Dowty [-@dowty1991thematic]: a noun phrase distributes probability mass across case roles, with the distribution sharpening as more evidence accumulates.

## Quantile Temporal Difference and Implicit Quantile Networks {#sec:daif-quantile}

Rather than representing the return distribution as a fixed categorical support (C51), the Quantile Regression DQN (QR-DQN) approach represents it as a uniform mixture of $N$ Dirac masses, one at each quantile level $\tau_i = (2i-1)/2N$. The `quantile_td_update()` function implements the Huber quantile loss:

\begin{equation}
\mathcal{L}_{\text{QR}}(\theta) = \frac{1}{N N'} \sum_{i=1}^{N} \sum_{j=1}^{N'} \rho_{\tau_i}^{\kappa}\!\left(\delta_{ij}\right)
\label{eq:eq-7c-qr}
\end{equation}

where $\delta_{ij} = r + \gamma z_j' - z_i$ is the temporal-difference error, and the Huber quantile loss $\rho_{\tau}^{\kappa}$ is:

\begin{equation}
\rho_{\tau}^{\kappa}(u) = |\tau - \mathbf{1}[u < 0]| \cdot \mathcal{L}_{\kappa}(u), \quad \mathcal{L}_{\kappa}(u) = \begin{cases} \frac{1}{2}u^2 & |u| \leq \kappa \\ \kappa(|u| - \frac{\kappa}{2}) & \text{otherwise} \end{cases}
\label{eq:eq-7c-huber}
\end{equation}

The **Implicit Quantile Network** extension (`implicit_quantile_network_update()` in `src/daif/quantile.py`) samples quantile levels $\tau \sim U[0,1]$ at inference time, enabling risk-distorted policy selection via four modes:

| Mode | Distortion $\beta{}(\tau{})$ | Semantic Role |
| :--- | :--- | :--- |
| **neutral** | $\beta{}(\tau{}) = \tau{}$ | Standard expected-value maximisation |
| **optimistic** | $\beta{}(\tau{}) = \tau{}^{1/(1+\eta{})}$ | Prefers high-return tails; suits exploratory parsers |
| **pessimistic** | $\beta{}(\tau{}) = \tau{}^{1+\eta{}}$ | Over-weights low-return tails; conservative case disambiguation |
| **CVaR** | $\beta{}(\tau{}) = \min(\tau{}/\alpha{}, 1)$ | Conditional Value-at-Risk at level $\alpha{}$; risk-averse comprehension |

The `wasserstein_return_distance()` function computes both $W_1$ (absolute area between CDFs) and $W_2$ (squared area) distances between return distributions, providing a principled metric for comparing case-assignment belief states across sentence positions.

## Variational Message Passing and Bethe Free Energy {#sec:daif-vmp}

The `variational_message_passing()` function in `src/daif/inference.py` implements iterative belief refinement over the case-role posterior $q(\mathbf{c} \mid \mathbf{o})$. Starting from a uniform prior over $K$ case roles, each observation $o_t$ (an incoming morphologically marked word) triggers a VMP update:

\begin{equation}
q^{(t+1)}(c_k) \propto q^{(t)}(c_k) \cdot \exp\!\bigl(\mathbb{E}_{q^{(t)}_{-k}}\!\bigl[\log p(o_t \mid c_k)\bigr]\bigr)
\label{eq:eq-7c-vmp}
\end{equation}

followed by renormalisation. The algorithm returns log-beliefs, final probabilities, and iteration count. Convergence is declared when $\|q^{(t+1)} - q^{(t)}\|_1 < \epsilon = 10^{-6}$.

The **Bethe free energy** provides a tractable lower-bound approximation to the variational free energy:

\begin{equation}
F_{\text{Bethe}}[\mathbf{q}] = \underbrace{-\sum_k q(c_k) \log p(c_k)}_{\text{prior fit}} + \underbrace{\sum_k q(c_k) \log q(c_k)}_{\text{belief entropy}} - \underbrace{\sum_t \sum_k q(c_k) \log p(o_t \mid c_k)}_{\text{likelihood}}
\label{eq:eq-7c-bethe}
\end{equation}

`bethe_free_energy()` in `src/daif/inference.py` computes this quantity for any belief distribution and observation set. The **expected information gain** (`expected_information_gain()`) measures the KL divergence between posterior and prior:

\begin{equation}
\text{EIG}(o) = D_{\mathrm{KL}}\bigl(q(\mathbf{c} \mid o) \;\|\; p(\mathbf{c})\bigr)
\label{eq:eq-7c-eig}
\end{equation}

\autoref{fig:daif-free-energy} visualises the Bethe free energy landscape over six sequential word arrivals in the sentence *"Der Hund jagt die Katze schnell"*: variational free energy decreases with each belief update cycle, and the KL decomposition shows the balance between model complexity ($D_{\mathrm{KL}}(q\|p)$) and data fit ($-\mathbb{E}_q[\log p(o|s)]$).

![Variational free energy decreases monotonically with each word arrival during distributional case assignment. **Left**: variational free energy $F[q]$ over DAIF iterations with vertical dashed lines marking word arrivals; each word triggers a new belief update cycle. **Right**: KL divergence decomposition showing $D_{\mathrm{KL}}(q\|p)$ (model complexity) versus $-\mathbb{E}_q[\log p(o|s)]$ (data fit accuracy), demonstrating the balance between parsimony and fidelity during case inference. Generated programmatically from `src.visualization.daif_plots.plot_free_energy_convergence()` (curves from `DAIFResult` produced by `src/daif/inference.py`).](output/figures/daif_free_energy_convergence.png){#fig:daif-free-energy}

\autoref{fig:daif-belief-trajectory} illustrates the full belief trajectory: starting from uniform prior over NOM, ACC, DAT, INS, the posterior sharpens monotonically as each morphologically marked word supplies evidence. The determiner *Der* signals nominative; the transitive verb *jagt* activates a valency frame expecting an accusative object; the accusative article *die* confirms NOM=Hund, ACC=Katze. Entropy $H[q]$ (centre panel) drops steeply at the second word—the most informative item in this parse.

![Case-role posterior sharpens from uniform prior as German morphology supplies evidence. DAIF belief trajectory during sequential disambiguation of *"Der Hund jagt die Katze schnell."* **Top**: stacked area showing P(NOM), P(ACC), P(DAT), P(INS) evolution over six words with German morphological glosses. **Middle**: entropy $H[q]$ with annotated steepest drop marking the most informative word. **Bottom**: push-forward return distribution as a quantile fan chart (10th--90th percentile) showing distributional uncertainty narrowing as the parse progresses. Generated programmatically from `src.visualization.daif_plots.plot_belief_trajectory()` (beliefs from `src/daif/` inference and `push_forward_return()` in `core.py`).](output/figures/daif_belief_trajectory.png){#fig:daif-belief-trajectory}

## Policy Selection and Expected Free Energy {#sec:daif-policy}

Active inference selects actions (here: next-word predictions or syntactic commitments) by minimising *expected free energy* $G{(\pi)}$, which decomposes into a pragmatic term (instrumental value) and an epistemic term (information gain):

\begin{equation}
G(\pi) = \underbrace{-\mathbb{E}_{q(o|\pi)}[\log p(o)]}_{\text{pragmatic value}} + \underbrace{D_{\mathrm{KL}}(q(s|\pi) \| p(s))}_{\text{epistemic value}} + \beta \cdot \text{risk}(\pi)
\label{eq:eq-7c-g}
\end{equation}

where $\beta \geq 0$ is the risk-sensitivity parameter. The `G_policy()` function in `src/daif/policy.py` computes this for any policy $\pi{}$ given a current belief state. Policy selection follows a Boltzmann (softmax) distribution over negative EFE:

\begin{equation}
P(\pi) = \frac{\exp(-\alpha \cdot G(\pi))}{\sum_{\pi'} \exp(-\alpha \cdot G(\pi'))}
\label{eq:eq-7c-softmax}
\end{equation}

where $\alpha > 0$ is the inverse temperature. `softmax_policy_selection()` implements this across an array of candidate policies; `distributional_epistemic_value()` returns the epistemic component alone, enabling decomposition of the policy gradient.

For case-theoretic reasoning, this means the agent selects the case assignment (NOM/ACC/DAT/etc.) that simultaneously minimises surprise (fits the observed morphological evidence), maximises information gain (resolves ambiguity fastest), and respects risk sensitivity (avoids high-variance parses in pessimistic mode). This provides a principled, Bayes-optimal account of why certain parse strategies are preferred cross-linguistically—they minimise expected free energy under the agent's generative model.

## ERP Amplitude Profiles from Distributional Prediction Error {#sec:daif-erp}

The `distributional_prediction_error()` function (`src/daif/prediction.py`) computes the precision-weighted mismatch between the observed return distribution and the predicted distribution:

\begin{equation}
\mathrm{DPE}(o, q) = \pi_f \cdot W_1(Z_{\text{predicted}}, Z_{\text{observed}})
\label{eq:eq-7c-dpe}
\end{equation}

where $\pi_f = \mathcal{C}(A,B) \in [0,1]$ is the enriched morphism weight (precision) of the violated case morphism (matching \autoref{eq:pe-precision-error} in \autoref{sec:diagrammatic-cognition}) and $W_1$ is the Wasserstein-1 distance. This yields direct predictions for psycholinguistic ERP components:

\begin{align}
\mathrm{N400}(c) &= \mathrm{DPE}_{\text{semantic}} \cdot \pi_c \cdot S_{\text{violation}} \label{eq:eq-7c-n400} \\
\mathrm{P600}(c) &= \mathrm{DPE}_{\text{structural}} \cdot (1-\pi_c) \cdot S_{\text{violation}} \label{eq:eq-7c-p600}
\end{align}

where $S_{\text{violation}} \in \{0, 0.5, 1.0\}$ encodes violation severity (congruent / mild / strong) and $\pi_c$ is the enriched weight of the case morphism in question. This dual decomposition directly mirrors the empirical finding of Li and Futrell [-@li2023decomposition; -@li2024shallow], who show that surprisal decomposes into a *heuristic* component tracking N400 and a *discrepancy* component tracking P600—precisely the semantic vs. structural split captured by $\mathrm{DPE}_{\text{semantic}}$ and $\mathrm{DPE}_{\text{structural}}$ above. The `erp_amplitude_profile()` function generates a complete `ERPProfile` dataclass containing:

- **N400 amplitude** (µV) and **peak latency** (ms) for each case role
- **P600 amplitude** (µV) and **peak latency** (ms) for each case role
- **Time-series waveforms** sampled at 1 kHz over a 1000 ms epoch

\autoref{fig:daif-erp-predictions} demonstrates predicted ERP amplitudes across all eight case roles under three violation conditions. A key result: because VOC→NOM is the most structurally inadmissible transition (morphism weight $\approx 0$), it elicits the largest P600; while the GEN→ACC semantic mismatch, with moderate morphism weight, elicits a pronounced N400 but attenuated P600.

![Distributional prediction error predicts graded N400/P600 amplitudes across all eight case roles. **Left**: simulated ERP waveforms for three violation conditions---congruent (NOM→NOM), mild (ACC→NOM), and strong (VOC→NOM)---showing component timing and amplitude scaling per \autoref{eq:eq-7c-n400}--\autoref{eq:eq-7c-p600}. **Middle**: scatter of enriched weight $\pi{}$ versus distributional prediction error (DPE, \autoref{eq:eq-7c-dpe}) for all roles, with regression line and $R^2$. **Right**: predicted versus literature-typical N400/P600 amplitudes. VOC→NOM (weight $\approx 0$) elicits the largest P600; GEN→ACC (moderate weight) elicits a pronounced N400 but attenuated P600. Generated programmatically from `src.visualization.daif_plots.plot_erp_predictions()` (amplitudes from `erp_amplitude_profile()` and related APIs in `src/daif/prediction.py`).](output/figures/daif_erp_predictions.png){#fig:daif-erp-predictions}

## Convergence Diagnostics and Distributional Metrics {#sec:daif-metrics}

The `src/daif/metrics.py` module provides four diagnostic tools for verifying DAIF model behaviour:

**Convergence diagnostics** (`convergence_diagnostics()`) assess whether a free-energy trajectory $\{F^{(t)}\}_{t=0}^{T}$ is well-behaved. Given the free energy sequence produced by VMP, the diagnostics return:

| Metric | Formula | Interpretation |
| :--- | :--- | :--- |
| `is_monotone` | $\forall t: F^{(t+1)} \leq F^{(t)}$ | FE decreasing at every step |
| `relative_reduction` | $(F^{(0)} - F^{(T)}) / \lvert F^{(0)}\rvert$ | Fraction of initial FE eliminated |
| `converged` | $\lvert F^{(T)} - F^{(T-1)}\rvert < \epsilon$ | Reached stable minimum |
| `final_value` | $F^{(T)}$ | Absolute FE at convergence |

**Distributional KL divergence** (`distributional_kl()`) computes the KL divergence between two discrete return distributions:

\begin{equation}
D_{\mathrm{KL}}(P \| Q) = \sum_{i} P(z_i) \log \frac{P(z_i)}{Q(z_i) + \epsilon}
\label{eq:eq-7c-dkl}
\end{equation}

with $\epsilon = 10^{-10}$ for numerical stability. Verified properties: $D_{\mathrm{KL}}(P\|Q) \geq 0$ (Gibbs' inequality), $D_{\mathrm{KL}}(P\|P) = 0$, asymmetry $D_{\mathrm{KL}}(P\|Q) \neq D_{\mathrm{KL}}(Q\|P)$ in general.

**Quantile coverage** (`quantile_coverage()`) measures calibration error—the mean absolute deviation between nominal quantile levels and empirical coverage frequencies:

\begin{equation}
\mathrm{CE} = \frac{1}{N} \sum_{i=1}^{N} \left| \tau_i - \hat{F}(z_{\tau_i}) \right|
\label{eq:eq-7c-ce}
\end{equation}

A perfectly calibrated distributional model achieves $\mathrm{CE} = 0$; the DAIF implementation yields $\mathrm{CE} < 0.01$ on all test cases evaluated in `test_daif_metrics.py`.

**Return distribution entropy** (`return_distribution_entropy()`) quantifies uncertainty in the distributional belief:

\begin{equation}
H[Z] = -\sum_{i=1}^{N_{\text{atoms}}} p_i \log p_i
\label{eq:eq-7c-entropy}
\end{equation}

This links directly to the belief trajectory in \autoref{fig:daif-belief-trajectory}: entropy decreases monotonically as the distributional belief sharpens, providing a scalar summary of parse certainty.

## CEREBRUM: Eight Cases as Functional Specializations {#sec:cerebrum}

### Architecture and Design Principles

The **CEREBRUM** framework [@friedman2024cerebrum; @cerebrum2024github]—Case-Enabled Reasoning Engine with Bayesian Representations for Unified Modeling—provides a computational architecture that implements the categorical case framework within an active inference engine. CEREBRUM instantiates the view of Vasil et al. [-@vasil2020world] that human communication is itself active inference: a process of jointly constructing and refining generative models of shared relational structure.

CEREBRUM's key design principles:

| Principle | Implementation |
| :--- | :--- |
| **Cases as functional roles** | Model components carry case markings that determine their computational role in the inference cycle |
| **Morphisms as message passing** | Grammatical relations are implemented as message-passing channels between components |
| **Enriched weights as precision** | The $[0,1]$ weights on morphisms correspond to precision parameters in the variational inference scheme |
| **Alignment as model selection** | Different alignment types correspond to different generative model architectures, selected by Bayesian model comparison |
| **Diagrams as generative models** | Commutative diagrams serve as the structural specification of the generative model |
| **DAIF as distributional layer** | The `src/daif/` subpackage provides the distributional RL layer: full return distributions replace point estimates throughout the generative cycle |

### Case Roles as Functional Specializations in CEREBRUM

CEREBRUM deploys the eight traditional cases as functional specializations, each with a DAIF-level extension:

| Case | CEREBRUM Function | Active Inference Role | DAIF Extension |
| :--- | :--- | :--- | :--- |
| NOM | Primary driver / agent | Source of action policies | Softmax policy over $G{(\pi)}$; highest epistemic value |
| ACC | Primary target / patient | Object of predictions | Predicted distribution $Z_{\text{acc}}$; error-driven update |
| GEN | Source / possessor | Provider of priors | Prior return distribution $p(Z)$ |
| DAT | Recipient / goal | Target of information transfer | EIG maximised toward DAT state |
| INS | Instrument / means | Tool for state transformation | IQN risk distortion (neutral mode) |
| LOC | Context / environment | Markov blanket boundary | Bethe FE boundary conditions |
| ABL | Origin / cause | Source of causal influence | Push-forward source measure $\mathbb{P}_{x_0,a_0}$ |
| VOC | Addressee | Pragmatic pointer | Lowest epistemic weight; largest P600 on violation |
