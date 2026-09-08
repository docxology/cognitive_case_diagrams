# Case Systems and Alignment {#sec:case-systems}

Comparative case analysis separates argument roles from their marking. We use S for the sole argument of a canonical intransitive predicate, A for the more agent-like argument of a canonical transitive predicate, and P for its more patient-like argument. Alignment describes how a specified marking system groups these roles. Case marking of full noun phrases, pronouns, and verbal person marking can differ within a language [@comrie2013alignment].

| Pattern | Grouping in the simplified representation |
| :--- | :--- |
| Nominative–accusative | S and A together; P separate |
| Ergative–absolutive | S and P together; A separate |
| Tripartite | S, A, and P distinct |
| Neutral | S, A, and P marked alike |
| Active–stative / split-S | Subclasses of S pattern differently |
| Fluid-S | Some S marking varies with construal or context |

Table: Schematic alignment patterns. These are not an exhaustive classification of language-wide behavior. {#tbl:alignment-types}

Historical accounts of semantic participation, deep case, dependency, and proto-roles motivate different choices of analytical unit. They should not be treated as interchangeable theories simply because a diagram can display their labels. In particular, a morphological case system does not determine a unique category of semantic relations.

The software's standard inventory is ${standard_inventory_names}. ${alignment_extra_label_names} are additional enum labels used in alignment examples, beyond the ${standard_inventory_count} standard members. The standard inventory is a convenience, not a universal ${standard_inventory_count_word}-case ontology. English names in the examples carry assigned grammatical-role metadata; most English full noun phrases do not inflect for nominative versus accusative case.

![Synthetic Fluid-S weight sweep. The plotted probabilities are supplied by the example generator and illustrate a context-dependent mapping; they are not estimated volitionality judgments or language-specific frequencies.](output/figures/fluid_s_volition_landscape.png){#fig:fluid-s}

A context probability in the Fluid-S API specifies a mixture between two case-label assignments. The numerical mixture is well-defined once its endpoints are supplied. Establishing that this mixture describes a language would require documented constructions, annotator agreement, and predictive evaluation. Language names in legacy convenience functions identify the motivating analogy rather than a validated grammar.
