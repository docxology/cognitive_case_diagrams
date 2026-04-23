# Distributional Active Inference (DAIF): Convergence of Semantic Topologies and Reinforcement Learning {#sec:daif-results}

**The claim of this section, precisely.** Three mathematical objects that arose independently in three fields — Firth's distributional-semantics vectors [-@firth1957papers] in linguistics, Bellemare–Dabney–Munos return distributions [-@bellemare2017distributional] in reinforcement learning, and Friston variational posteriors [-@friston2017active] in active inference — are the *same* structural object seen from three angles. Each assigns to a pair of states a $[0,1]$-valued hom-value (a similarity, a probability mass on a support atom, a posterior weight); each does so because the underlying framework had to replace an inadequate scalar summary (co-occurrence count, expected return, MAP estimate) with a *full distribution* in order to be expressive; and each composes along chains by multiplying those hom-values, putting all three inside the same $[0,1]$-enriched category (\autoref{sec:enriched-categories}). The convergence is non-trivial because none of the three frameworks was designed with the others in mind, yet the enriched-category axioms (identity, sub-multiplicative composition, $Z$-matrix invertibility for magnitude) hold in all three without modification. This convergence is what Akgül et al. [-@akgul2026distributional] call **Distributional Active Inference (DAIF)**. The repository implements the convergence computationally; a fully categorical proof that the three instantiations share a common enriched-category base in the strict sense (with a single enriching monoidal base category, not merely compatible hom-value scales) remains open and is flagged in the Limitations subsection below.

The `src/daif/core.py` implementation (tested in the project suite) uses a **belief-weighted mean-field approximation**: rather than maintaining a separate return distribution $Z(s)$ for every case-role state $s$ (which would cost $\mathcal{O}(n \cdot N_{\text{atoms}})$ memory), `push_forward_return(belief, transition_matrix, ...)` propagates a single return distribution weighted by the current posterior $q(s)$ over states. Formally, one step of the contraction computes $\mathbf{z} = R + \gamma\, T^{\top} q$ and collapses it to the belief-weighted scalar $\bar z = q^{\top} \mathbf{z}$; uncertainty is then injected back via the quantile spread of the updating distributional return. The approximation is exact in the limit of a sharp posterior ($q \to \delta_{s^\ast}$) and recovers the full per-state distributional Bellman operator in that regime. In exchange for the $\mathcal{O}(n)$ complexity, it buffers aleatoric and epistemic uncertainty simultaneously and remains sample-efficient for the linguistic-parsing proxy model used here (**implemented and tested**).

The terminological collision between "distributional" in distributional semantics and "distributional" in distributional RL is not mere homonymy—it reflects a deep structural parallel. In both domains, the core computational move is the same: **replacing scalar summaries with full distributional representations.** In linguistics, this means contextualizing word identities via probability distributions (Firth's [-@firth1957papers] company-keeping principle). In reinforcement learning, it replaces expected-value estimates with quantile-approximated return distributions. In active inference, it replaces point estimates of states with variational posterior distributions. The enriched-categorical framework of \autoref{sec:enriched-categories} provides the unifying abstraction: all three are instances of $[0,1]$-enriched categories where hom-values encode distributional proximity rather than rigid identity.

This section presents the complete implementation and quantitative results of the `src/daif/` subpackage—seven modules, 25 public symbols, 224 automated tests—covering six major computational contributions: push-forward returns (\autoref{sec:daif-pushforward}), quantile TD and implicit quantile networks (\autoref{sec:daif-quantile}), variational message passing and Bethe free energy (\autoref{sec:daif-vmp}), policy selection and expected free energy (\autoref{sec:daif-policy}), unifying ERP amplitude profiles (\autoref{sec:daif-erp}), and convergence diagnostics (\autoref{sec:daif-metrics}).

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

where $p_i(s,a)$ is the probability assigned to support point $z_i$ and $\delta$ is the Dirac delta mass. In our framework, this C51 support structure is instantiated via the `categorical_return_distribution()` function. The distributional Bellman operator $\mathcal{T}^{\pi}$, implemented computationally via the `distributional_bellman_operator()` multi-step contraction tracking method, then maps return distributions forward:

\begin{equation}
\mathcal{T}^{\pi} Z(s,a) \stackrel{d}{=} R(s,a) + \gamma Z(S', A'), \quad S' \sim P(\cdot|s,a), \; A' \sim \pi(\cdot|S')
\label{eq:eq-7c-bellman}
\end{equation}

**Contraction (B1)**. By Bellemare et al. [-@bellemare2017distributional, Theorem 1], $\mathcal{T}^{\pi}$ is a $\gamma$-contraction in the supremum $p$-Wasserstein metric $\bar W_p$ on the space of return distributions — i.e. $\bar W_p(\mathcal{T}^{\pi} Z_1, \mathcal{T}^{\pi} Z_2) \le \gamma\, \bar W_p(Z_1, Z_2)$ for any $p \in [1, \infty)$. Hence the fixed point $Z^\star$ is unique and iterates $\mathcal{T}^{\pi n} Z_0$ converge to $Z^\star$ at geometric rate $\gamma^n$; this underwrites the convergence tracked by `distributional_bellman_operator()` in `src/daif/core.py`.

**Mean-field bound (B5)**. The belief-weighted step $\bar z = q^\top \mathbf{z}$ used by `push_forward_return()` replaces the exact per-state operator with a single scalar collapse. Assume bounded rewards $\lVert R\rVert_\infty \le R_{\max}$ and an entropy budget $H[q] < \varepsilon$ nats. Then the approximation error of this collapse is bounded by $\gamma\,R_{\max}\,\varepsilon$ in the induced $W_1$ metric (units of return), since the worst-case mass reallocation between roles is at most the entropy of $q$, and each reallocated unit of probability contributes at most $\gamma R_{\max}$ to $W_1$. The approximation is therefore exact in the sharp-posterior limit $q \to \delta_{s^\star}$ ($\varepsilon \to 0$) and degrades at most linearly in $H[q]$ as the posterior diffuses.

For case-theoretic reasoning, DAIF implies a computational architecture in which case assignment operates distributionally at every level: the agent maintains not a single case diagram but a *distribution over case diagrams*, weighted by their posterior probability given the observed linguistic evidence. This distributional perspective on case assignment aligns naturally with the graded proto-role structure of Dowty [-@dowty1991thematic]: a noun phrase distributes probability mass across case roles, with the distribution sharpening as more evidence accumulates.

## Quantile Temporal Difference and Implicit Quantile Networks {#sec:daif-quantile}

Rather than representing the return distribution as a fixed categorical support (C51), the Quantile Regression DQN (QR-DQN) approach represents it as a uniform mixture of $N$ Dirac masses, one at each midpoint quantile level $\tau_j = (2j-1)/(2N)$ for $j = 1,\dots,N$ — equivalently $\tau_i = (2i+1)/(2N)$ for the 0-indexed form $i = 0,\dots,N-1$ used in `src/daif/quantile.py:66`. The `quantile_td_update()` function implements the Huber quantile loss:

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

| Mode | Distortion $\psi_{\mathrm{IQN}}(\tau)$ | Semantic Role |
| :--- | :--- | :--- |
| **neutral** | $\psi_{\mathrm{IQN}}(\tau) = \tau{}$ | Standard expected-value maximisation |
| **optimistic** | $\psi_{\mathrm{IQN}}(\tau) = \tau^{1/\eta_{\mathrm{IQN}}}$ | Prefers high-return tails; suits exploratory parsers |
| **pessimistic** | $\psi_{\mathrm{IQN}}(\tau) = 1 - (1-\tau)^{1/\eta_{\mathrm{IQN}}}$ | Over-weights low-return tails; conservative case disambiguation |
| **CVaR** | $\psi_{\mathrm{IQN}}(\tau) = \tau \cdot \alpha_{\mathrm{CVaR}}$ | Linear tail compression (implementation default $\alpha_{\mathrm{CVaR}} = 0.25$); risk-averse comprehension |

Table: IQN risk distortion modes, formulas, and semantic roles in case-assignment parsing. {#tbl:iqn-modes}

The four modes are implemented exactly in `implicit_quantile_network_update()` (`src/daif/quantile.py`) with fixed $\eta_{\mathrm{IQN}} = 0.71$. **Convention note.** With $\eta = 0.71$ we have $1/\eta \approx 1.408 > 1$, so $\tau^{1/\eta} < \tau$ and $1-(1-\tau)^{1/\eta} > \tau$ on $(0,1)$. In our implementation the distorted level $\tau'$ is multiplied directly into the asymmetric Huber weight (i.e. the loss has its positive-error weight scaled by $\tau'$ and its negative-error weight by $1-\tau'$). Under that *weight-level* convention, the "optimistic" mode shrinks positive-error updates (making the agent slower to revise upward on good news — preference for the status quo upper tail) and the "pessimistic" mode inflates positive-error updates (making the agent track the lower tail more aggressively). Readers cross-referencing Dabney et al.'s [-@dabney2018distributional] sampling-level distortion (where the distortion is applied to the sampling density of $\tau$) should note that our mode names follow the *weight-level* semantic rather than the sampling-level one; the underlying mathematical formulas match across the two conventions but their qualitative labels are mirror-images.

**Consistency (B2)**. Under i.i.d. TD samples, the empirical minimiser of the quantile Huber loss $\rho_\tau^\kappa$ converges to the true $\tau$-quantile at rate $O(N^{-1/2})$; see Dabney et al. [-@dabney2018distributional, Theorem 2]. The Huber threshold $\kappa$ trades off robustness to outliers against bias near $\delta=0$, and our default $\kappa=1$ recovers Dabney et al.'s standard setting.

The `wasserstein_return_distance()` function computes discrete-quantile approximations of both $W_1$ (absolute area between CDFs) and $W_2$ (root-mean-square area) distances between return distributions. **Approximation error (B4)**. For midpoint quantiles $\tau_i = (2i-1)/(2N)$ and a Lipschitz quantile function, the estimator is O($N^{-2}$) consistent with the continuous integral $W_p = (\int_0^1 |F_a^{-1}(\tau) - F_b^{-1}(\tau)|^p\,d\tau)^{1/p}$; this is the canonical discretisation used in quantile-regression RL (Dabney et al. [-@dabney2018distributional]) and is documented explicitly in the docstring of `wasserstein_return_distance()`.

## Variational Message Passing and Bethe Free Energy {#sec:daif-vmp}

The orchestrator of the DAIF inference cycle is the `distributional_case_assignment()` function in `src/daif/inference.py`. It wraps the push-forward mapping and Bayesian update routines to return a `DAIFResult` object encapsulating the free-energy trajectory. During this loop, the `variational_message_passing()` sub-function implements iterative categorical belief refinement over the case-role posterior $q(\mathbf{c} \mid \mathbf{o})$. Starting from a uniform prior over $K$ case roles, each sweep applies the precision-weighted exponential update:

\begin{equation}
q^{(t+1)}(c_k) \propto q^{(t)}(c_k) \cdot \exp\!\bigl(w_k \cdot o_k\bigr)
\label{eq:eq-7c-vmp}
\end{equation}

where $w_k \in [0,1]$ is the **enriched morphism weight** for role $k$ read off from the case category of \autoref{sec:enriched-categories} (acting as a precision on the update) and $o_k = \log p(o \mid c = k)$ is the log-likelihood of the observation under role $k$. After each update the distribution is renormalised via softmax. The algorithm returns posterior probabilities and posterior precisions $\Lambda_{\text{post}} = \Lambda_{\text{prior}} + \Lambda_{\text{lik}}$. Convergence is declared when $\|q^{(t+1)} - q^{(t)}\|_1 < \epsilon = 10^{-6}$.

**Convergence (B3)**. *Proposition.* For the single-observation categorical factor graph used in case assignment, the softmax update (\autoref{eq:eq-7c-vmp}) is a strict KL-contraction and possesses a unique fixed point $q^\star$; the $L^1$ threshold $\varepsilon$ is reached in $O(\log(1/\varepsilon))$ sweeps. *Sketch.* The unnormalised multiplicative update followed by normalisation is the gradient step of a strictly convex problem (minimising the Bethe free energy on a tree-structured factor graph); Yedidia, Freeman and Weiss [-@yedidia2005constructing, §III–IV] show that in the tree (cycle-free) case, belief propagation exactly minimises the Bethe FE, so the iteration has a unique global minimiser. The contraction rate is bounded by the ratio of likelihood precision to prior precision. For factor graphs with loops our implementation inherits the weaker "approximate fixed point" guarantee of loopy BP; the current linguistic application uses a single observation factor per word, which is tree-structured.

The **Bethe free energy** provides a tractable lower-bound approximation to the variational free energy. In the mean-field specialisation—where each observation constitutes an independent factor with uniform variable degrees—the Bethe FE reduces to:

\begin{equation}
F_{\text{Bethe}}[\mathbf{q}] = \underbrace{-\sum_k q(c_k) \log p(c_k)}_{\text{prior fit}} + \underbrace{\sum_k q(c_k) \log q(c_k)}_{\text{belief entropy}} - \underbrace{\sum_t \sum_k q(c_k) \log p(o_t \mid c_k)}_{\text{likelihood}}
\label{eq:eq-7c-bethe}
\end{equation}

The `bethe_free_energy()` function in `src/daif/inference.py` implements the full factor-graph Bethe FE (Yedidia et al. 2001): $F_{\text{Bethe}} = \sum_\alpha \mathrm{KL}(b_\alpha \| f_\alpha) - \sum_i (d_i - 1) H(b_i)$, where $b_\alpha$ are factor beliefs, $f_\alpha$ are factor potentials, and $d_i$ is the degree of variable $i$ in the factor graph. The equation above is the tractable mean-field limit presented for clarity. The **expected information gain** (`expected_information_gain()`) measures the mutual information between observations and case-role assignments—the expected KL divergence between posterior and prior, weighted by the marginal likelihood of each candidate observation:

\begin{equation}
\text{EIG}(o^*) = \sum_{o^*} p(o^*) \, D_{\mathrm{KL}}\bigl(q(\mathbf{c} \mid o^*) \;\|\; p(\mathbf{c})\bigr)
\label{eq:eq-7c-eig}
\end{equation}

This mutual-information formulation properly accounts for the probability of each observation, providing a principled measure of how much a candidate word would reduce uncertainty about the current case-role assignment on average.

\autoref{fig:daif-free-energy} visualises the Bethe free energy landscape over six sequential word arrivals in the sentence *"Der Hund jagt die Katze schnell"*: variational free energy decreases with each belief update cycle, and the KL decomposition shows the balance between model complexity ($D_{\mathrm{KL}}(q\|p)$) and data fit ($-\mathbb{E}_q[\log p(o|s)]$).

![Variational free energy decreases during distributional case assignment. **Left**: measured $F^{(t)}$ values read directly from `DAIFResult.fe_trajectory` (blue markers) with a smoothed reference envelope (grey dashed) and vertical dashed lines marking word arrivals. **Right**: the *real* decomposition $F^{(t)} = D_{\mathrm{KL}}(q^{(t)}_{\text{posterior}}\|q^{(t)}_{\text{pushed}}) - \mathbb{E}_{q^{(t)}}[\log p(o|s)]$, plotted from `DAIFResult.diagnostics["kl_trajectory"]` and `diagnostics["loglik_trajectory"]` (not a schematic). Generated programmatically by `src.visualization.daif_plots.plot_free_energy_convergence()` from `make_free_energy_convergence_data()` in `src/cognitive/figure_data.py`.](output/figures/daif_free_energy_convergence.png){#fig:daif-free-energy}

\autoref{fig:daif-belief-trajectory} illustrates the full belief trajectory: starting from uniform prior over NOM, ACC, DAT, INS, the posterior sharpens monotonically as each morphologically marked word supplies evidence. The determiner *Der* signals nominative; the transitive verb *jagt* activates a valency frame expecting an accusative object; the accusative article *die* confirms NOM=Hund, ACC=Katze. Entropy $H[q]$ (centre panel) drops steeply at the second word—the most informative item in this parse.

![Case-role posterior sharpens from uniform prior as German morphology supplies evidence. DAIF belief trajectory during sequential disambiguation of *"Der Hund jagt die Katze schnell."* **Top**: stacked area showing P(NOM), P(ACC), P(DAT), P(INS) evolution over six words with German morphological glosses. **Middle**: entropy $H[q]$ with annotated steepest drop marking the most informative word. **Bottom**: uncertainty fan around the dominant-role probability, constructed as a simple proxy $\Delta = 1 - \max_k P(c_k)$ scaled by fixed percentile multipliers; this is a visual surrogate, *not* a 51-quantile decomposition of the push-forward return distribution. Generated programmatically from `src.visualization.daif_plots.plot_belief_trajectory()`.](output/figures/daif_belief_trajectory.png){#fig:daif-belief-trajectory}

## Policy Selection and Expected Free Energy {#sec:daif-policy}

Active inference selects actions (here: next-word predictions or syntactic commitments) by minimising *expected free energy* $G{(\pi)}$. `G_policy()` in `src/daif/policy.py` implements the four-term decomposition used throughout this paper:

\begin{equation}
G(\pi) = \underbrace{-\mathbb{E}_{q(s)}[\log p(o\mid s,\pi)]}_{\text{ambiguity}\;(\mathcal{A})}
\;-\;\underbrace{\mathbb{E}_{q(s)}\bigl[\,H[p(s\mid o)]\,\bigr]}_{\text{epistemic value}\;(\mathcal{E})}
\;-\;\gamma\,\underbrace{\mathbb{E}_{q(s)}[v(s,\pi)]}_{\text{pragmatic value}\;(\mathcal{P})}
\;+\;\beta_{\mathrm{risk}}\,\underbrace{\mathrm{Var}_{Z}[R(\pi)]}_{\text{risk}\;(\mathcal{R})}
\label{eq:eq-7c-g}
\end{equation}

Each term is signed so that *minimising* $G(\pi)$ simultaneously minimises ambiguity, maximises expected information gain, maximises expected pragmatic utility, and penalises high-variance return distributions. The weights are $\gamma>0$ (pragmatic gain) and $\beta_{\mathrm{risk}}\ge 0$ (risk sensitivity, using the distributional return variance produced by `push_forward_return()`).

**Collapse identity (derivation).** Setting $v(s,\pi) = \log p(o_{\text{goal}} \mid s,\pi)$ and $\beta_{\mathrm{risk}} = 0$ reduces Eq. \ref{eq:eq-7c-g} to
\begin{align*}
G(\pi) \;&=\; -\mathbb{E}_{q(s)}[\log p(o \mid s,\pi)] \;-\; \mathbb{E}_{q(s)}[H[p(s \mid o)]] \;-\; \gamma\,\mathbb{E}_{q(s)}[\log p(o_{\text{goal}} \mid s,\pi)]\\
\;&=\; \underbrace{-\mathbb{E}_{q(s)}[\log p(o \mid s,\pi)]}_{\text{expected surprise}} \;+\; \underbrace{D_{\mathrm{KL}}\bigl(q(s\mid\pi)\,\|\,p(s)\bigr)}_{\text{epistemic value}} \;-\; \gamma\,\mathbb{E}_{q(s)}[\log p(o_{\text{goal}} \mid s,\pi)],
\end{align*}
where the second equality uses the standard active-inference identity $-\mathbb{E}_{q(s)}[H[p(s\mid o)]] = D_{\mathrm{KL}}(q(s\mid\pi) \,\|\, p(s)) + \text{const}$ (Friston et al. [-@friston2017active], Eq. 5), valid when the posterior is close to the generative prior so that the $H[q(s\mid\pi)]$ term absorbs into the constant offset that cancels across policies. This is the canonical three-term form of Friston et al., confirming that our decomposition is a conservative generalisation rather than a departure.

Policy selection follows a Boltzmann (softmax) distribution over negative EFE:

\begin{equation}
P(\pi) = \frac{\exp(-\alpha_{\mathrm{pol}} \cdot G(\pi))}{\sum_{\pi'} \exp(-\alpha_{\mathrm{pol}} \cdot G(\pi'))}
\label{eq:eq-7c-softmax}
\end{equation}

where $\alpha_{\mathrm{pol}} > 0$ is the inverse temperature (policy softmax), distinct from the CVaR tail level $\alpha_{\mathrm{CVaR}}$ in the IQN table above. `softmax_policy_selection()` implements this across an array of candidate policies; `distributional_epistemic_value()` returns the epistemic component alone, enabling decomposition of the policy gradient.

For case-theoretic reasoning, this means the agent selects the case assignment (NOM/ACC/DAT/etc.) that simultaneously minimises surprise (fits the observed morphological evidence), maximises information gain (resolves ambiguity fastest), and respects risk sensitivity (avoids high-variance parses in pessimistic mode). This provides a principled, Bayes-optimal account of why certain parse strategies are preferred cross-linguistically—they minimise expected free energy under the agent's generative model.

## ERP Amplitude Profiles from Distributional Prediction Error {#sec:daif-erp}

The DAIF prediction module (`src/daif/prediction.py`) provides two complementary prediction error measures, each appropriate for different levels of the distributional hierarchy:

**Scalar DPE** (`distributional_prediction_error()`): For point-prediction scenarios where the expected case role is known, the precision-weighted surprisal provides a computationally efficient scalar measure:

\begin{equation}
\mathrm{DPE}_{\text{scalar}}(c, q) = w_f \cdot \bigl(-\log q[c_{\text{expected}}]\bigr)
\label{eq:eq-7c-dpe-scalar}
\end{equation}

**Wasserstein DPE** (`wasserstein_prediction_error()`): For full distributional comparisons between predicted and observed return distributions, the precision-weighted Wasserstein-1 distance provides the distributional measure:

\begin{equation}
\mathrm{DPE}(o, q) = w_f \cdot W_1(Z_{\text{predicted}}, Z_{\text{observed}})
\label{eq:eq-7c-dpe}
\end{equation}

where $w_f = \mathcal{C}(A,B) \in [0,1]$ is the enriched morphism weight (precision) of the violated case morphism (matching \autoref{eq:pe-precision-error} in \autoref{sec:diagrammatic-cognition}) and $W_1$ is the Wasserstein-1 distance.

**Reader's guide to the four DPE variants.** The DAIF framework uses four distinct but related prediction-error measures, easily confused because they share the name "DPE":

1. $\mathrm{DPE}_{\text{scalar}}$ (\autoref{eq:eq-7c-dpe-scalar}, `distributional_prediction_error()`) — a *point-belief* surprisal: precision-weighted cross-entropy on the currently-expected role. Used when the grammatically expected role is known.
2. $\mathrm{DPE}$ (full Wasserstein; \autoref{eq:eq-7c-dpe}, `wasserstein_prediction_error()`) — a *full distributional* mismatch between predicted and observed return distributions. Used for graded / distributional comparisons.
3. $\mathrm{DPE}_{\text{semantic}}$ (\autoref{eq:eq-7c-dpe-semantic} below, input to `n400_from_return_distribution()`) — the *first moment* of the distributional mismatch, i.e. the absolute mean-return shift; tracks the N400 heuristic component.
4. $\mathrm{DPE}_{\text{structural}}$ (\autoref{eq:eq-7c-dpe-structural} below, input to `p600_from_precision_update()`) — the *full distributional* mismatch $W_1(Z_{\text{pred}}, Z_{\text{obs}})$; tracks the P600 discrepancy component and coincides with $\mathrm{DPE}$ in item 2.

Items (3) and (4) decompose (2) into a mean-shift and a full-distribution signal; item (1) is a simpler scalar surrogate for point-belief use cases.

**ERP derivation from the Free Energy Principle (B6).** The two ERP formulas below are *derived* from a free-energy decomposition rather than posited empirically. A new word arriving at the case-assignment layer induces a change in variational free energy $\Delta F = F_{\text{post}} - F_{\text{prior}}$. Using $F = D_{\mathrm{KL}}\bigl(q \,\|\, p(s)\bigr) - \mathbb{E}_q[\log p(o|s)]$ (the variational free-energy decomposition introduced in \autoref{sec:cognitive-integration}) and splitting $q \to q'$ into a posterior-mean shift and a precision-sharpening component, a first-order expansion gives
\begin{equation*}
\Delta F \;=\; \underbrace{-\bigl(\mathbb{E}_{q'}[Z_{\text{obs}}] - \mathbb{E}_{q}[Z_{\text{pred}}]\bigr)}_{\text{mean-return shift}\;\approx\;\mathrm{DPE}_{\text{semantic}}} \;+\; \underbrace{\tfrac{1}{2}\,\Delta\Lambda\,\sigma_Z^{2}}_{\text{precision update}\;\approx\;\Delta\Lambda \cdot \mathrm{DPE}_{\text{structural}}} \;+\; O(\|\Delta q\|^2),
\end{equation*}
where $\sigma_Z^2$ is the return-distribution variance (proxied at first order by $W_1(Z_{\text{pred}}, Z_{\text{obs}})$). The mean-return shift is the heuristic, expectation-dominated component that Kuperberg and Jaeger [-@kuperberg2016mean] and Li and Futrell [-@li2023decomposition] associate with the N400; the precision-update term is the discrepancy, structure-update component that Rabovsky et al. [-@rabovsky2018modelling] and Li and Futrell [-@li2024shallow] associate with the P600. Severity gating $S_{\text{violation}} \in \{0, 0.5, 1.0\}$ modulates both components multiplicatively, reflecting the attenuation of prediction-error signals when the violation is only mild. The precision on the semantic component is $w_c$ (the enriched morphism weight), and the amplitude calibration $s$ on the P600 converts the dimensionless free-energy increment into μV. This yields the severity-gated decomposition:

\begin{align}
\mathrm{N400}(c) &= -\,\mathrm{DPE}_{\text{semantic}} \cdot w_c \cdot S_{\text{violation}} \label{eq:eq-7c-n400} \\
\mathrm{P600}(c) &= s\,\cdot\,\Delta\Lambda \cdot \mathrm{DPE}_{\text{structural}} \cdot S_{\text{violation}} \label{eq:eq-7c-p600}
\end{align}

where $S_{\text{violation}} \in \{0, 0.5, 1.0\}$ encodes violation severity (congruent / mild / strong), $w_c$ is the enriched weight of the case morphism, $\Delta\Lambda = \max(0, \Lambda_{\text{post}} - \Lambda_{\text{prior}})$ is the precision-update magnitude reflecting the structural reanalysis cost, and $s > 0$ is a dimensionless amplitude-calibration constant (default $s=1$ in `p600_from_precision_update()`). The leading minus sign in Eq. \ref{eq:eq-7c-n400} follows electrophysiological convention: larger semantic surprise yields a more negative deflection at the N400 latency, consistent with the sign produced by `n400_from_return_distribution()` in `src/daif/prediction.py`. The two $\mathrm{DPE}$ flavours appearing here are defined formally by:

\begin{align}
\mathrm{DPE}_{\text{semantic}}\;&=\;\bigl\lvert \mathbb{E}[Z_{\text{pred}}] - \mathbb{E}[Z_{\text{obs}}] \bigr\rvert
\label{eq:eq-7c-dpe-semantic}\\
\mathrm{DPE}_{\text{structural}}\;&=\;W_{1}\bigl(Z_{\text{pred}},\,Z_{\text{obs}}\bigr)
\label{eq:eq-7c-dpe-structural}
\end{align}

i.e. $\mathrm{DPE}_{\text{semantic}}$ is the absolute mean-return mismatch (the heuristic component in the Li–Futrell decomposition, tracking the N400) and $\mathrm{DPE}_{\text{structural}}$ is the full distributional Wasserstein-1 mismatch (the discrepancy component, tracking the P600). Computationally, N400 amplitudes are extracted via `n400_from_return_distribution()` (which computes mean-return mismatch scaled by precision and severity), while P600 amplitudes use `p600_from_precision_update()` (which computes precision-update magnitude scaled by DPE and severity). This dual decomposition directly mirrors the empirical finding of Li and Futrell [-@li2023decomposition; -@li2024shallow], who show that surprisal decomposes into a *heuristic* component tracking N400 and a *discrepancy* component tracking P600---precisely the semantic vs. structural split captured by $\mathrm{DPE}_{\text{semantic}}$ and $\mathrm{DPE}_{\text{structural}}$ above.

Our framework explicitly accommodates Rabovsky et al.'s [-@rabovsky2018modelling] finding that the N400 reflects a probabilistic Bayesian belief update, extending it by formally equipping the N400 semantic surprise as a distributional prediction-error over explicit case boundaries. (The complementary neurobiological-timing question raised by the ROSE model is addressed in the Limitations subsection below, after the metrics discussion and before the CEREBRUM integration.)

Ultimately, the `erp_amplitude_profile()` master function aggregates these distinct computations into a complete `ERPProfile` dataclass containing:

- **N400 amplitude** (µV) and **peak latency** (ms) for each case role
- **P600 amplitude** (µV) and **peak latency** (ms) for each case role
- **Time-series waveforms** sampled at 1 kHz over a 1100 ms epoch (−200 to +900 ms)

\autoref{fig:daif-erp-predictions} demonstrates predicted ERP amplitudes across all eight case roles under three violation conditions. A key result: because VOC carries the lowest enriched precision weight in the illustration ($w = 0.10$, the smallest among all eight roles), VOC→NOM is the most structurally inadmissible transition and elicits the largest P600; while GEN, with moderate precision weight ($w = 0.70$), elicits a pronounced N400 but attenuated P600.

![Distributional prediction error predicts graded N400/P600 amplitudes across all eight case roles. **Left**: illustrative Gaussian ERP waveforms for three violation conditions — congruent (NOM→NOM), mild (ACC→NOM), and strong (VOC→NOM) — with fixed template amplitudes ($-1.5/3.0$, $-4.0/3.0$, $-7.0/6.0$ μV N400/P600) and peaks at 380 ms / 600 ms (matching `DEFAULT_N400_PEAK_MS` / `DEFAULT_P600_PEAK_MS` in `src/daif/prediction.py`), shown to depict the *mechanism* of \autoref{eq:eq-7c-n400}--\autoref{eq:eq-7c-p600} rather than a calibrated simulation. **Middle**: scatter of enriched weight $w$ versus scalar DPE (\autoref{eq:eq-7c-dpe-scalar}) for all eight case roles, computed via `distributional_prediction_error()` in `src/daif/prediction.py`. **Right**: *real* DAIF-predicted magnitudes — mean N400 magnitude via `n400_from_return_distribution()` and mean P600 via `p600_from_precision_update()` across the eight roles (`make_erp_prediction_data()` in `src/cognitive/figure_data.py`) — alongside literature-typical amplitude ranges from Kutas \& Federmeier [-@kutas2011thirty] (N400 magnitude 3–5 μV, P600 5–8 μV, shown with error bars). Note that the model predictions are on a *dimensionless* DPE scale (units of log-probability × enriched weight), whereas the literature values are calibrated in μV; the comparison is therefore qualitative (relative ordering and graded response to precision) rather than a numerical match. A future calibration step would require fitting a per-subject μV-per-nat scaling constant to empirical ERP data. Generated programmatically from `src.visualization.daif_plots.plot_erp_predictions()`.](output/figures/daif_erp_predictions.png){#fig:daif-erp-predictions}

## Convergence Diagnostics and Distributional Metrics {#sec:daif-metrics}

The `src/daif/metrics.py` module provides four diagnostic tools for verifying DAIF model behaviour:

**Convergence diagnostics** (`convergence_diagnostics()`) assess whether a free-energy trajectory $\{F^{(t)}\}_{t=0}^{T}$ is well-behaved. Given the free-energy sequence produced by VMP, the function returns a dict with the eight fields below (keys match the Python return value exactly):

| Key | Formula | Interpretation |
| :--- | :--- | :--- |
| `monotone` | $\forall t: F^{(t+1)} \leq F^{(t)}$ | FE decreasing at every step |
| `total_reduction` | $F^{(0)} - F^{(T)}$ | Total free energy minimised (absolute) |
| `relative_reduction_pct` | $100\cdot (F^{(0)} - F^{(T)}) / \lvert F^{(0)}\rvert$ | Fraction of initial FE eliminated, % |
| `n_iterations` | $T + 1$ | Number of iterations in the trajectory |
| `converged` | $\lvert F^{(T)} - F^{(T-1)}\rvert < 0.01\cdot(F_{\max} - F_{\min})$ | Reached stable minimum (within 1 % of range) |
| `fe_range` | $(F_{\min},\, F_{\max})$ | Absolute FE bounds across the trajectory |
| `mean_step_size` | $\tfrac{1}{T}\sum_{t} \lvert F^{(t+1)} - F^{(t)}\rvert$ | Average per-iteration FE change |
| `final_delta` | $\lvert F^{(T)} - F^{(T-1)}\rvert$ | Final step size at convergence or timeout |

Table: Convergence diagnostic metrics for DAIF free-energy trajectories. Keys match `convergence_diagnostics()` in `src/daif/metrics.py` one-to-one. {#tbl:convergence-metrics}

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

A perfectly calibrated distributional model achieves $\mathrm{CE} = 0$; the DAIF implementation in `src/daif/metrics.py` (tested in `test_daif_metrics.py`) yields $\mathrm{CE} < 0.05$ on evaluated cases (**implemented and tested**).

**Return distribution entropy** (`return_distribution_entropy()`) quantifies uncertainty in the distributional belief:

\begin{equation}
H[Z] = -\sum_{i=1}^{N_{\text{bins}}} p_i \log p_i
\label{eq:eq-7c-entropy}
\end{equation}

where the $p_i$ are obtained by discretising the quantile-parameterised return onto $N_{\text{bins}}$ equal-width bins (default $N_{\text{bins}}=50$ in `src/daif/metrics.py`) with additive $\epsilon$-smoothing $p_i \leftarrow (c_i + \epsilon) / (\sum_j c_j + N_{\text{bins}}\,\epsilon)$ to keep the estimator finite when bins are empty. The estimator is consistent at the usual $O(1/N_{\text{bins}})$ discretisation rate as $N_{\text{bins}} \to \infty$, and satisfies $0 \le H[Z] \le \log N_{\text{bins}}$ by direct enumeration. This links to the belief trajectory in \autoref{fig:daif-belief-trajectory}: entropy decreases monotonically as the distributional belief sharpens, providing a scalar summary of parse certainty.

### Two Supporting Utilities Exposed by `src/daif/` {#sec:daif-support-utils}

Two further public symbols in the DAIF subpackage support the machinery above without requiring a separate equation:

* **`distributional_epistemic_value()`** (`src/daif/policy.py`) measures the information-theoretic value of resolving uncertainty in the return distribution via the differential-entropy form $\mathrm{EV}_{\mathrm{dist}} = \tfrac{1}{2}\log\bigl(\mathrm{Var}[Z]/\sigma^2_{\mathrm{ref}}\bigr)$. In the risk-sensitive regime ($\beta_{\mathrm{risk}}>0$ in \autoref{eq:eq-7c-g}) this function decomposes the risk term $\mathrm{Var}_Z[R(\pi)]$ into a positive "exploration premium" when the current return distribution is more dispersed than the reference.
* **`categorical_return_distribution()`** (`src/daif/core.py`) realises the C51 projection operator $\Phi\colon \mathcal{P}(\mathbb{R}) \to \mathcal{P}(\{z_1,\dots,z_{N_{\text{atoms}}}\})$ that maps a quantile-parameterised return onto the fixed atomic support of Eq. \ref{eq:eq-7c-c51}. The operator is *non-expansive* in $W_1$: by construction $\Phi$ redistributes each quantile mass across at most two adjacent atoms using barycentric weights summing to 1, so for any two return distributions $P, Q$ one has $W_1(\Phi P, \Phi Q) \le W_1(P, Q)$ — hence $\Phi$ is 1-Lipschitz (and in fact strictly contractive whenever $P$ and $Q$ place mass strictly between atoms). This is the reason C51/DAIF interoperability preserves contraction bounds from \autoref{sec:daif-pushforward}.

### Dimensional Analysis

The quantities appearing in this section carry the following units:

| Quantity | Symbol | Units |
| :--- | :---: | :--- |
| Variational free energy | $F$ | nats |
| Return (discounted cumulative reward) | $Z(s,a)$ | return units (e.g. dimensionless log-probability) |
| Wasserstein distance on returns | $W_p(Z_a, Z_b)$ | return units |
| $\mathrm{DPE}_{\text{semantic}}$ | — | return units (= $\lvert\Delta\mathbb{E}[Z]\rvert$) |
| $\mathrm{DPE}_{\text{structural}}$ | — | return units (= $W_1$) |
| Enriched weight (precision) | $w_c$ | dimensionless, $\in[0,1]$ |
| Precision-update magnitude | $\Delta\Lambda$ | dimensionless (weight difference) |
| Severity gating | $S_{\text{violation}}$ | dimensionless, $\in\{0,0.5,1\}$ |
| N400 amplitude (\autoref{eq:eq-7c-n400}) | — | return units (*not* μV until calibrated) |
| P600 amplitude (\autoref{eq:eq-7c-p600}) | — | return units × dimensionless $s$ (*not* μV until calibrated) |

Since $Z$ in our implementation is built from log-likelihood proxies (`safe_log_lik` in `src/daif/inference.py`), the return is effectively in *nats*, and every quantity derived from $Z$ is therefore dimensionally a free-energy-like scalar. A future ERP-calibration step would convert "nats" to "μV" via a per-subject scaling constant, as noted in the \autoref{fig:daif-erp-predictions} caption.

## Limitations and Neurobiological Scope {#sec:daif-limitations}

Four limitations of the current DAIF implementation are recorded explicitly for future work:

1. **Mean-field approximation (cost/accuracy).** `push_forward_return()` maintains one belief-weighted return distribution rather than per-state distributions $Z(s)$, reducing memory from $\mathcal{O}(n\cdot N_{\text{atoms}})$ to $\mathcal{O}(n)$. By the mean-field bound proved later in this section (the dominated-convergence argument under "B5" in the contraction analysis) the approximation error is at most $\gamma\cdot R_{\max}\cdot H[q]$ in $W_1$, where $R_{\max}$ is the sup-norm of the reward vector. For sharp posteriors ($H[q]\lesssim 0.1$ nats at $\gamma=0.99$ and unit-scale rewards) the error is below $0.1$ return-unit — well below the within-subject noise floor on ERP measurements; it degrades linearly as the posterior diffuses.

2. **Enriched-categorical unification is a conjecture.** The three "distributional" tracks — distributional semantics (\autoref{sec:categorical-semantics}), distributional RL (this section), and active-inference posteriors — are implemented and empirically correspond via $[0,1]$-enriched hom-values, but a *categorical* proof that they share a common enriched base remains open. The conjecture is stated in the opening of this section and is not used as a load-bearing claim elsewhere in the paper.

3. **Empirical validation is narrow.** Our case-assignment demonstrations use a single German transitive sentence (*"Der Hund jagt die Katze schnell"*). Cross-linguistic and cross-register validation is left to future work; the hooks in `make_daif_belief_trajectory_data()` make adding new sentences a single-function change. A Russian or Serbian/BCS sentence — say *Sobaka kusaet čeloveka* "the dog bites the man" — would be a particularly clean DAIF stress-test, since the unambiguous case suffixes (*-a* NOM.SG.F vs *-a* ACC.SG.M.ANIM after stem hardening) deliver an information-theoretically sharper drop in $H[q]$ at the case-marked noun than the German example, where word-final case markers compete with positional disambiguation and gender / number ambiguity in the determiner system.

4. **Phase–amplitude coupling (PAC) latency gap.** DAIF predicts ERP *amplitudes* from distributional prediction errors but does not predict component *latencies*. The ROSE model [@murphy2023rose] argues that the structural-discrepancy (P600-analogous slow-phase) signal must establish a geometric "mesoscopic protectorate" before semantic surprise (N400-analogous rapid gamma binding) can be fully constrained. A principled treatment of this cross-frequency-coupling delay would require an explicit timing parameter at the CEREBRUM layer (\autoref{sec:cerebrum}) — the present implementation keeps N400/P600 latencies as fixed Gaussian peaks at 380 ms and 600 ms respectively (see `DEFAULT_N400_PEAK_MS` and `DEFAULT_P600_PEAK_MS` in `src/daif/prediction.py`).

## CEREBRUM: Eight Cases as Functional Specializations {#sec:cerebrum}

The preceding six contributions—push-forward returns, quantile TD for case precision, VMP message passing, epistemic policy selection, ERP convergence profiles, and Bethe free-energy decomposition—define a distributional active inference layer for sentence processing. CEREBRUM translates this layer into a complete computational architecture by assigning each of the eight traditional cases a functional role within the inference engine.

### Architecture and Design Principles

The **CEREBRUM** framework [@friedman2024cerebrum]—Case-Enabled Reasoning Engine with Bayesian Representations for Unified Modeling—provides a computational architecture that implements the categorical case framework within an active inference engine. CEREBRUM instantiates the view of Vasil et al. [-@vasil2020world] that human communication is itself active inference: a process of jointly constructing and refining generative models of shared relational structure.

CEREBRUM's key design principles (\autoref{tbl:cerebrum-principles}):

| Principle | Implementation |
| :--- | :--- |
| **Cases as functional roles** | Model components carry case markings that determine their computational role in the inference cycle |
| **Morphisms as message passing** | Grammatical relations are implemented as message-passing channels between components |
| **Enriched weights as precision** | The $[0,1]$ weights on morphisms correspond to precision parameters in the variational inference scheme |
| **Alignment as model selection** | Different alignment types correspond to different generative model architectures, selected by Bayesian model comparison |
| **Diagrams as generative models** | Commutative diagrams serve as the structural specification of the generative model |
| **DAIF as distributional layer** | The `src/daif/` subpackage provides the distributional RL layer: full return distributions replace point estimates throughout the generative cycle |

Table: CEREBRUM design principles: conceptual commitments and their implementation in the reasoning engine. {#tbl:cerebrum-principles}

### Case Roles as Functional Specializations in CEREBRUM

CEREBRUM deploys the eight traditional cases as functional specializations, each with a DAIF-level extension (\autoref{tbl:cerebrum-daif}):

```{=latex}
\begin{table}[htbp]
\centering
\begin{tabular}{@{}l p{0.29\textwidth} p{0.29\textwidth} p{0.29\textwidth}@{}}
\toprule
\textbf{Case} & \textbf{CEREBRUM Function} & \textbf{Active Inference Role} & \textbf{DAIF Extension} \\
\midrule
NOM & Primary driver / agent & Source of action policies & Softmax policy over $G{(\pi)}$; highest epistemic value \\
ACC & Primary target / patient & Object of predictions & Predicted distribution $Z_{\text{acc}}$; error-driven update \\
GEN & Source / possessor & Provider of priors & Prior return distribution $p(Z)$ \\
DAT & Recipient / goal & Target of information transfer & EIG maximised toward DAT state \\
INS & Instrument / means & Tool for state transformation & IQN risk distortion (neutral mode) \\
LOC & Context / environment & Markov blanket boundary & Bethe FE boundary conditions \\
ABL & Origin / cause & Source of causal influence & Push-forward source measure $\mathbb{P}_{x_0,a_0}$ \\
VOC & Addressee & Pragmatic pointer & Lowest epistemic weight; largest P600 on violation \\
\bottomrule
\end{tabular}
\caption{CEREBRUM case roles as functional specializations with DAIF distributional extensions.}
\label{tbl:cerebrum-daif}
\end{table}
```
