# Distributional Utilities and Synthetic Filtering {#sec:daif-results}

Distributional active inference is an existing research programme [@akgul2026distributional]. The local `src/daif/` package is a collection of experimental utilities inspired by distributional representations; it is not a reproduction of that paper's complete algorithm. Several compatibility names predate the present clarification. This section defines the quantities actually computed.

## Finite score distributions and projection {#sec:daif-pushforward}

For role probabilities $q$, a row-stochastic transition matrix $T$, dimensionless score vector $R$, and $\gamma\in[0,1]$, `push_forward_return()` forms

$$
z=R+\gamma T^Tq,\qquad \mu=\sum_i q_i\delta_{z_i}.
$$ {#eq:eq-7-1}

The mass at $z_i$ is $q_i$. Mean and variance use exact finite weighted sums. The stored quantile values use the generalized inverse of this discrete CDF, removing zero-mass support. They do not interpolate new values between distinct atoms. For equal mass at the support endpoints ${daif_projection_support_min} and ${daif_projection_support_max}, the midpoint levels ${daif_projection_levels} yield ${daif_projection_values}.

Despite its legacy name, `distributional_bellman_operator()` propagates beliefs and repeats this score calculation. It does not back up state-conditioned future-return distributions or sum discounted rewards. In the canonical counterexample configuration — uniform transition entry ${daif_bellman_example_transition}, uniform two-state belief, reward entries ${daif_bellman_example_reward_first} and ${daif_bellman_example_reward_second}, and discount ${daif_bellman_example_gamma} — its score mean is ${daif_bellman_example_score_mean}. The true infinite-horizon expected return for that Markov reward process, computed from $(I-\gamma T)^{-1}R$, is ${daif_bellman_example_true_return}. This counterexample rules out treating the utility as a Bellman solver; both quoted numbers are recomputed from the same declared configuration at build time.

`categorical_return_distribution()` and `DistributionalReturn.to_categorical()` share a C51-style projection: clip supplied samples to fixed support, then split each sample's mass between adjacent atoms. Values outside the support contribute to endpoint atoms rather than disappearing. Stored quantiles do not reconstruct every property of the original law; projection of equally weighted quantile samples is an explicit approximation.

## Pairwise quantile regression and distortion {#sec:daif-quantile}

For current values $\theta_i$, target samples $y_j$, and midpoint levels $\tau_i$, the update uses every pair $\delta_{ij}=y_j-\theta_i$, as motivated by quantile regression [@dabney2018distributional]. Define $H_\kappa$ as the ordinary Huber loss. The implemented coordinate update is

$$
\theta_i' = \theta_i + \alpha\frac1M\sum_j
 |\tau_i-\mathbf1_{\delta_{ij}<0}|\,
 \operatorname{clip}(\delta_{ij},-\kappa,\kappa).
$$ {#eq:eq-7c-qr}

Here the Huber loss is unnormalized: its derivative is clipped at $\kappa$. The learning-rate convention absorbs averaging over current coordinates. Comparing with a paper or implementation using $H_\kappa/\kappa$ requires corresponding rescaling of $\alpha$. The output is sorted to retain quantile order. Current and target sample counts can differ.

`implicit_quantile_network_update()` applies pairwise Huber updates with distorted current probability levels; it contains no neural network. Target values are equally weighted samples; supplied target levels are validated metadata, not quadrature weights. The IQN literature concerns learning quantile functions [@dabney2018implicit]. In this helper, for $0<\eta<1$, optimistic distortion $1-(1-\tau)^{1/\eta}$ emphasizes upper values, while pessimistic distortion $\tau^{1/\eta}$ emphasizes lower values. Both reduce to the identity at $\eta=1$; the direction reverses if $\eta>1$, so the mode name alone is insufficient without its parameter.

## Filtering, single-factor messages, and factor scores {#sec:daif-vmp}

At each filter step the code computes $p^-=T^Tq$ and $q'=L\odot p^-/\sum_i L_i p^-_i$. It stores the updated belief before any stopping decision. Diagnostics include the complete posterior trajectory, the number of updates, and `stop_reason`. Stopping requires small changes in both belief and free energy; an increase in free energy alone is not an error because successive priors change.

`variational_message_passing()` is a single-factor calculation with an implicit uniform prior:

$$
q_i=\operatorname{softmax}_i(\lambda_{\mathrm{lik},i}o_i).
$$ {#eq:eq-7c-vmp}

It also returns $\lambda_{\mathrm{prior}}+\lambda_{\mathrm{lik}}$ as bookkeeping. Prior precision does not determine a nonuniform categorical prior. Because the incoming message is constant, extra sweeps do not perform general loopy inference.

The legacy `bethe_free_energy()` is now also exposed as `factor_consistency_score()`. Its actual formula is

$$
C(q)=\sum_a D_{\mathrm{KL}}(q\Vert\widehat f_a)
      -\left(\sum_i(d_i-1)\right)H(q).
$$ {#eq:eq-7c-bethe}

There is only one categorical distribution $q$, and $\widehat f_a$ is a normalized supplied vector. This is not a Bethe free energy: no joint factor marginals, individual variable marginals, or factor potentials are represented. Adjacency must be binary, and negative factor weights are rejected.

`expected_information_gain()` returns each observation's contribution $p(o)D_{\mathrm{KL}}(q(\cdot\mid o)\Vert q)$. Its sum is mutual information only if the supplied likelihood columns sum to one across a complete observation alphabet. An arbitrary list of candidate likelihood vectors is not automatically such an alphabet.

![Computed per-update free energy and its KL/data-fit decomposition for synthetic repeated-observation filtering. Each evidence vector is used for up to ${daif_assignment_iterations} updates before the next vector. There is no fitted convergence envelope or fixed-objective convergence claim.](output/figures/daif_free_energy_convergence.png){#fig:daif-free-energy}

![A separate sequence consumes ${daif_trajectory_evidence_count} hand-selected likelihood vectors once each. Panels show probabilities, entropy, and total variation between adjacent posteriors for one latent role. The first displayed change is a zero placeholder; it is not a measured change from an omitted prior. No percentile bands or token-specific parses are inferred.](output/figures/daif_belief_trajectory.png){#fig:daif-belief-trajectory}

## Caller-defined policy scores {#sec:daif-policy}

`G_policy()` evaluates $-q\cdot\ell-q\cdot e-\gamma q\cdot u+\beta\operatorname{Var}(Z)$ for supplied finite vectors $\ell,e,u$. This can express a chosen surprise, information-value, utility, and risk tradeoff. It is not a general expected-free-energy derivation. Expected log likelihood of one observation is not ambiguity entropy, and posterior entropy is not information gain. Units must be made compatible by the coefficients.

Policy probabilities are computed by a stable softmax of negative scores. Subtraction precedes temperature scaling to avoid overflow. Low temperature concentrates mass on minima, including equal treatment of tied minima; no optimality theorem about the environment follows.

## Prediction-error and ERP-inspired proxies {#sec:daif-erp}

The scalar error is weighted surprisal $-w\log q_i$, with a small positive probability floor in the compatibility API. A separate function uses $wW_1$ between two reconstructed quantile distributions. These are distinct mismatches, not interchangeable derivations of one physiological observable.

The N400-inspired proxy is $-s\lambda|m-m_0|$. The P600-inspired proxy is $s k\max(0,\lambda_{\mathrm{post}}-\lambda_{\mathrm{prior}})\mathrm{DPE}$. Severity $s$, scaling $k$, and precision values are caller inputs. The waveform utility places these amplitudes in Gaussian templates with specified millisecond centers and widths. Millisecond timing labels do not calibrate amplitude to microvolts; compatibility fields ending in `_uV` still contain uncalibrated values.

![Synthetic prediction-error and amplitude proxies across role labels. Hand-selected weights, beliefs, and severity values determine the outputs. Amplitudes are model units; no EEG dataset, empirical error bars, or comparison with literature microvolt ranges is shown.](output/figures/daif_erp_predictions.png){#fig:daif-erp-predictions}

## Metrics and reconstruction conventions {#sec:daif-metrics}

Wasserstein distance uses both stored probability-level grids, even when their lengths match. Between levels it linearly interpolates quantiles and holds tails constant to zero and one. Integration for orders one and two is exact for these reconstructed laws. It is not exact for an unknown originating distribution, and no universal convergence rate is asserted.

Histogram KL and entropy depend on the binning and smoothing parameters. `quantile_coverage()` compares observations with supplied quantiles; calling it does not itself create held-out calibration data. `convergence_diagnostics()` reports changes in a supplied series; a small change is not proof of a unique fixed point.

## Scope and extensions {#sec:daif-limitations}

A genuine distributional-control experiment would need a reward process, state-conditioned return laws, a justified Bellman or inference operator, parameter learning, baseline comparisons, and independent evaluation data. An EEG experiment would additionally require physiological calibration. Neither is supplied here. The present utilities are useful as explicit numerical examples because these missing steps are visible. The seeded synthetic computations in [@sec:synthetic-statistics] characterize the filtering, calibration, projection, and sensitivity behavior of these utilities on their declared inputs; they remain synthetic and add no empirical evidence.

## CEREBRUM as a design vocabulary {#sec:cerebrum}

The ${standard_inventory_count} familiar case labels can organize a proposed agent architecture: actor, affected content, recipient, instrument, context, source, possession, and address. This analogy does not establish ${standard_inventory_count_word} neural modules or a universal factorization of cognition. The software does not implement a complete CEREBRUM agent. Proposed architectural mappings should be evaluated as engineering choices with explicit interfaces and tasks.
