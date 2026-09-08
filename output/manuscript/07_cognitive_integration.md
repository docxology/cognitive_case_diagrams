# Bayesian Case-Role Beliefs and Active-Inference Motivation {#sec:cognitive-integration}

Active inference supplies a motivation for relating generative models, uncertainty, and action [@friston2017active]. The implemented cognitive core is narrower: finite categorical beliefs, Bayesian likelihood updates, KL divergence, variational free-energy evaluation, and caller-defined policy scores.

For prior probabilities $p_i$ and nonnegative likelihoods $L_i$ with positive evidence $e=\sum_i p_iL_i$, the update is $q_i=p_iL_i/e$. Likelihoods need not sum to one over states. A negative likelihood is invalid even where the prior is zero, and an all-zero or disjoint-support likelihood is an error rather than a reason to invent a uniform posterior.

For a fixed generative pair $(p,L)$,

$$
F(q)=D_{\mathrm{KL}}(q\Vert p)-\sum_i q_i\log L_i
    =D_{\mathrm{KL}}(q\Vert p(\cdot\mid o))-\log e.
$$ {#eq:variational-bound}

The identity holds with consistent support conventions. It establishes the usual bound for this fixed model; it does not imply that free energies computed under different incoming priors and observations must decrease. Zero-probability terms are masked rather than evaluated as $0\log0$.

![Synthetic filtering over candidate alignment-frame labels. Likelihood vectors are hand-selected; the plot demonstrates the supplied update rule rather than an empirically inferred change in a language's alignment.](output/figures/active_inference_belief.png){#fig:active-inference-belief}

`sequential_belief_update()` consumes each supplied likelihood once. `distributional_case_assignment()` repeatedly consumes the same likelihood, optionally with a Markov prediction step; its iteration parameter is therefore an evidence-repetition choice, not just an optimizer budget. A single categorical belief indexes the candidates declared by the caller. It cannot simultaneously stand for every noun's case, the whole parse tree, and an alignment system without an explicit joint model.

Policy selection utilities evaluate supplied surprise, information-value, and utility vectors. A full active-inference model would need a specified generative process, observation predictions under policies, and preferences. Those components are not inferred from the graph drawing.
