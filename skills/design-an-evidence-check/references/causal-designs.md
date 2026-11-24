# Select a design from the assignment process

Write the intervention, feasible counterfactual, decision, eligible population, start, follow-up and effect scale. Ask whether units were exposed earlier, how uptake differs from assignment, when the effect should appear, who else is affected and which events coincided with rollout. Inspect actual assignment and outcome logs. Separate the design that identifies an effect from the estimator that calculates it.

| Observed opportunity | Design worth pricing | Evidence needed before committing |
|---|---|---|
| Assignment can be randomized | Individual or cluster trial, randomized encouragement, or switchback if assignment must change over time | Randomization unit, spillovers, washout, power from independent units, compliance and outcome collection. For a fully exposed cohort, consider a withdrawal experiment and distinguish withdrawal from initial adoption. |
| Known assignment probabilities differ by experiment or stratum | Estimate within design strata and aggregate for a declared target, or use design weights | Numerators, denominators and probabilities by stratum. Marginal pooling can reverse the sign. |
| External adoption dates differ across units | Difference-in-differences with cohort/time effects | Untreated or not-yet-treated comparison at each horizon, plausible parallel untreated trends and no anticipation. Exclude invalid already-treated comparisons. |
| One or a few treated series and plausible donors | Synthetic control | Sufficient pretreatment history, donor fit and untreated donors untouched by spillovers. A short pre-period or universal shock can defeat the comparison. |
| Long outcome series with a dated intervention | Interrupted time series, with a control series if possible | Stable measurement, pretrend, seasonality, serial correlation, event lag and concurrent shocks. Designate the diagnostic that would force an associative conclusion. |
| An assignment cutoff actually governs receipt | Sharp or fuzzy regression discontinuity | Observable running variable on both sides, credible continuity, sufficient local data, no sorting and, for fuzzy assignment, a first stage. Estimate the local effect. |
| Credible exogenous encouragement changes uptake | Instrumental variables | First stage, independence, exclusion and assumptions supporting a complier interpretation. ITT may still answer the policy decision when uptake is low. |
| Exchangeability might hold given baseline covariates | Matching, standardization, weighting or doubly robust estimation | Substantive adjustment set, measured pretreatment confounders and common support. When support is absent, narrow the target or report extrapolation explicitly. |
| Benefit may vary and the decision is whom to treat | Prespecified subgroup effects or honestly evaluated heterogeneous effects | An identified base design, adequate overlap and independent evaluation of the proposed policy. Compare policy value with treat-all and treat-none. |

Use a causal diagram to record timing, common causes, mediators, colliders and selection before adjusting. Report assumptions without a diagnostic as substantive assumptions. If a new experiment or different comparison can resolve the decisive uncertainty, price it against the current option. If no credible design identifies the effect, deliver the descriptive comparison and name the missing evidence.

For an implementation discrepancy, compare assignment, adjustment and denominators against the design. Check the interface of the version in use.
