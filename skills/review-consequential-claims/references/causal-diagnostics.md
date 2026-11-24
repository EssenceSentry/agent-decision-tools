# What could invalidate this estimate?

Record the population, estimand, assignment and data revision. For each relevant row attach an observed result, unit and evidence link. Label an assumption violated, compatible with evidence, untested, or intrinsically untestable. A compatibility check is weaker than an identification argument. Prioritize a violation that could change the decision.

| Method | Try to expose this failure | What the finding changes |
|---|---|---|
| Randomized experiment | Reconcile assignment counts and probabilities against logs by stratum. Check enrollment after assignment, attrition, interference, compliance, sample-ratio mismatch and uncertainty at the randomization unit. Compare ITT with the selected-user analysis. | Rebuild the assignment cohort or narrow the estimand. Post-treatment engagement can manufacture an apparent effect. |
| Difference-in-differences | Plot leads and lags by adoption cohort, inspect concurrent changes and composition, test pre-period placebos and sensitivity to plausible differential trends. Check whether controls have already been treated; cluster at assignment level. | Report the supported cohorts and horizons. A nonsignificant pretrend test can have little power. |
| Instrumental variables | Inspect the first stage and weak-instrument-robust intervals. Look for instrument–outcome paths outside receipt, imbalance and a substantive challenge to monotonicity. | Weak identification can give wide or unbounded intervals. Violated exclusion changes the interpretation even with a strong first stage. Distinguish compliers from all eligible units. |
| Regression discontinuity | Inspect raw running-variable density and bunching, predetermined covariates, support, side-specific fits, bandwidth and alternative cutoffs. Verify the jump in actual treatment in a fuzzy design. | If sorting or another policy jumps at the same cutoff, qualify attribution. Limit generalization to units near the cutoff. |
| Matching and weighting | Inspect overlap, post-adjustment balance, tail weights, effective sample size, excluded units and sensitivity to unmeasured confounding. Check that adjustments predate treatment. | Report the remaining target population and sensitivity. A propensity model cannot supply a missing comparison group. |
| Synthetic control | Plot prefit and donor weights, compare pre/post gaps for placebo units with comparable prefit, and repeat leaving influential donors out. Check donor exposure and anticipation. | Poor prefit or contaminated donors undermine the counterfactual. Report alternative donor pools and limits on inference. |
| Interrupted time series | Inspect seasonality, residual autocorrelation, interventions at placebo dates and a comparable untreated series. Repeat under plausible intervention lags. Check measurement changes. | A simultaneous shock or coding change can explain the discontinuity. Qualify attribution or redesign the comparison. |
| Heterogeneous effects and policies | Separate exploratory splits from held-out confirmation. Inspect subgroup support, multiplicity, overlap, uncertainty and policy value vs simple policies on unused data. | Narrow claims to supported subgroups. Discovery-set rankings are insufficient evidence for deployment. |
| Causal diagram and adjustment | Check the time ordering and meaning of every adjustment, alternative diagrams, open back-door paths, conditioning on descendants/colliders and sample selection. | Show which path is blocked or opened. Testable implications can reject a graph; compatible observed distributions admit more than one graph. |

Before promising a diagnostic, check available packages and data, distinguishing a missing dependency from an unavailable identifying variable. Use an existing implementation when equivalent. Record skipped checks, corrections from the analyst, the remaining threats and the decision after the audit.

## Worked diagnostics

Interpret a diagnostic in the context of the identification assumptions for the chosen design. In staggered adoption use a cohort-aware event study with valid controls.
