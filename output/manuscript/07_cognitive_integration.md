# Active Inference as a Process Theory of Case {#sec:cognitive-integration}

**Where we are in the argument.** \autoref{sec:case-systems}–\autoref{sec:topos-theory} have given the framework a *structural* theory — objects, morphisms, functors, enriched weights, and topos-theoretic bridges. This chapter supplies the missing *process* theory: active inference recasts case assignment as variational Bayesian inference over a generative model whose state variable is the case-role posterior, whose precision parameters are the enriched weights of \autoref{sec:enriched-categories}, and whose free-energy descent turns "parsing a sentence" into a sequence of belief updates — the dynamics that \autoref{sec:diagrammatic-cognition} exploits to derive ERP predictions.

## Static Categories Are Not Enough

The preceding sections constructed a mathematical infrastructure for analyzing case systems—categorical, type-logical, distributional, enriched, and topos-theoretic. Yet these frameworks remain *static*: they describe the structure of case grammar without explaining how a cognitive agent *deploys* that structure during real-time comprehension and production. Bridging this gap requires a dynamic *process theory* of case-marked relational reasoning. Active inference [@namjoshi2026fundamentals; @friston2017active] provides exactly this missing dynamic computational layer.

## Surprise Minimization Drives Case-Frame Inference

### Free Energy Bounds Surprisal

Active inference is the primary process theory derived from the free energy principle (FEP): every self-organizing system maintains its structural integrity by minimizing the surprisal (negative log-probability) of its sensory observations under an internal *generative model* of its environment [-@friston2010free]. The system executes this minimization through two complementary strategies:

1. **Perceptual inference**: Update internal beliefs to better predict current observations (reduce prediction error)
2. **Active inference**: Act on the environment to bring observations in line with predictions (reduce expected prediction error)

Recent extensions of active inference to linguistics and cognitive science have modeled language comprehension and production as forms of sequential Bayesian inference. As Donnarumma, Frosolone, and Pezzulo (2023) demonstrate in their integration of large language models and active inference for modelling eye movements in reading, linguistic processing constitutes "inference over a hierarchical generative model, facilitating predictions and inferences at various levels of granularity, from syllables to sentences" [-@donnarumma2023integrating]. Similarly, Friston et al. (2021) have demonstrated how communication emerges between synthetic subjects: "linguistic outcomes (specifically, the spoken word)... are selected to minimise the free energy given current beliefs" via "high-order interactions among abstract (discrete) states in deep (hierarchical) models" [-@friston2021understanding; -@friston2020generative].

Both strategies minimize the same mathematical quantity—variational free energy—and both draw from a single generative model encoding the system's prior expectations about the relational structure of its world.

Critically, recent neurolinguistic evidence directly supports this prediction-error account. Li and Futrell [-@li2023decomposition; -@li2024shallow] decompose surprisal into two orthogonal components: *heuristic surprise* ("shallow surprisal"), which tracks the N400 brain potential and reflects lexical-associative prediction error, and a *discrepancy signal* ("deep surprisal"), which tracks the P600 and reflects structural reanalysis when the true parse diverges from the initially inferred structure. This decomposition maps directly onto our enriched case framework: the N400 corresponds to distributional prediction error *within* a case-role subspace (semantic mismatch), while the P600 corresponds to structural prediction error *between* case-diagram topologies (morphosyntactic reanalysis requiring a change in the generative model's case assignments). The formal equations in \autoref{sec:daif-results} (\autoref{eq:eq-7c-n400}–\autoref{eq:eq-7c-p600}) instantiate exactly this dual decomposition.

#### Generative Models of Relational Structure

Under this paradigm, language understanding manifests as *active inference over relational structure*: the listener maintains a generative model anticipating who-does-what-to-whom, and each incoming word supplies evidence that updates this model. Morphological case marking provides high-precision evidence—for example, a nominative suffix predicts that the noun phrase functions as the agent, reducing uncertainty about the relational structure of the unfolding event.

#### S-HAI: The Case Diagram as the Abstract "Schema" Level

These relational generative models find their formal articulation in recent advances such as **Schema-Based Hierarchical Active Inference (S-HAI)** [@maele2026schema]. Unifying predictive processing with schema theory, S-HAI employs a dual-level POMDP structure to model rapid generalization across environments. In the linguistic domain, the "Level 2" model encodes abstract, hidden relational goals---which corresponds exactly to the *case diagram structure* we describe here. The "Level 1" model encodes concrete sensorimotor navigation---for linguistics, this maps to the sequential parsing of surface word forms.

Just as S-HAI explains sudden "zero-shot" behavioral remapping in novel environments by preserving the high-level schema mapping while updating the "grounding likelihoods" to new observables, a case frame enables an agent to rapidly generalize the relational structure of a complex sentence regardless of novel vocabulary pairings. The abstract string diagram is the schema; case inflection is the grounding likelihood.

### The Five-Step Prior–Observation–Update–Prediction–Action Loop

The process unfolds as follows:

1. **Prior**: The listener has a prior belief about the relational structure (a "case diagram" encoding expected roles and their connections)
2. **Observation**: Each word provides sensory evidence—its form, its case marking, its distributional properties
3. **Update**: The listener updates the case diagram to accommodate the evidence, using approximate Bayesian inference (typically variational message passing)
4. **Prediction**: The updated diagram generates predictions about upcoming words (case-marked NPs, verb valency patterns)
5. **Action**: In production, the speaker selects words and case markers that minimize expected free energy—choosing expressions that are informative, contextually appropriate, and syntactically well-formed

### Case Diagrams as Instantiated Situations

This dynamic active inference perspective connects naturally to **situation semantics** (Barwise and Perry [-@barwise1983situations]), which treats linguistic meaning as structured situations—specific configurations of individuals, relations typed by arity, and spatiotemporal locations, grounded in an ecological realism where meanings are recurring relational patterns that organisms attune to. Translated into our categorical framework, a **situation** is an instantiated case diagram: a specific assignment of entities to roles with particular morphisms activated; the **situation type** is the structural case category itself, the abstract pattern that any particular situation instantiates; and **information flow** between situations is a functorial mapping between case categories. Where classical situation semantics left the dynamics implicit, active inference supplies the computational engine: the agent moves through situations in real time, updating its case diagram with each incoming word and using the updated diagram to predict which situation will arise next.

### Belief Dynamics Over Competing Case Frames

\autoref{fig:active-inference-belief} shows a minimal **scalar-belief** simulation: the agent holds a `CaseDiagramBelief` over alternative alignment frames (NOM--ACC vs. ERG--ABS). As syntactic evidence arrives, variational free energy and entropy track the discrete update loop that \autoref{sec:daif-results} extends to full return distributions in DAIF. Generated programmatically from `src/visualization/active_inference_plots.plot_alignment_frame_belief_dynamics()` (belief trajectory from `sequential_belief_update()` in `src/cognitive/belief_updating.py`).

![Variational free energy drives convergence to the correct case frame during belief updating. The agent begins with a uniform prior over possible case frames (NOM--ACC vs. ERG--ABS, $H[q] = \log 2$). **Top**: stacked $P(\text{frame})$ over evidence steps (including the prior column). **Middle**: entropy $H[q]$ in nats, with the steepest drop annotated at the most informative step. **Bottom**: variational free energy $F[q]$ after each update (per-step curve) and its running minimum $\min_{\tau\leq t} F[q_\tau]$ (non-increasing envelope), with dashed vertical markers at each evidence index (same convention as word arrivals in \autoref{fig:daif-free-energy}). Likelihoods are synthetic categorical draws consistent with a TQNN-evaluated diagram. Generated programmatically from `src/visualization/active_inference_plots.plot_alignment_frame_belief_dynamics()` (PNG from `scripts/generate_cognitive_figures.py`).](output/figures/active_inference_belief.png){#fig:active-inference-belief}
