# Choose checks by the proposed claim

First write which question it is: describing what happened, predicting, or claiming that one thing caused another. Many errors begin by answering a causal question with a descriptive or predictive analysis.

Use the checks that could change this study. Set choices that depend on the outcome before looking at it.

<a id="controlled-intervention"></a>

## 1. Controlled intervention

Write a design note before collecting outcomes.

1. The decision: the action for each possible result, including an inconclusive one. If no result changes the action, do not run it.
2. One primary outcome and its guardrails, named now, with treatment, comparator and eligible population.
3. The unit that is assigned and the unit that is analysed. Where they differ, the variance estimate accounts for it. Count the independent units of assignment.
4. Interference: whether treated units can affect comparison units through a shared budget, market, audience or queue. If so, assign at a level that contains it: clusters, regions, time blocks.
5. The smallest effect worth acting on and the power to detect it. If underpowered, state what the run can still show.
6. Noise reduction: a pre-period covariate, or pairing and stratifying before assignment.
7. Duration and stopping rule, covering whole cycles and any carryover. No stopping on a favourable day unless the method allows planned looks.
8. The analysis: estimator, exclusions, primary comparison, segments. Anything else is labelled exploratory.
9. Checks that it ran as designed: the allocation matches the planned ratio, the groups were alike before treatment, exposure happened, a placebo through the same pipeline finds nothing.
10. The number of comparisons (outcomes, segments, looks) and how they are handled.
11. A surprising result is checked as a bug before it is believed.
12. What the result will not show: other periods, other populations, the effect when everyone is treated.

<a id="causal-claim-from-history"></a>

## 2. Causal claim from history

Write a claim note before interpreting an observational difference as an effect.

1. The trial you would have run: eligibility, treatment strategies, comparison, time zero, outcome, follow-up.
2. Why these units were treated and the others were not. If someone chose on performance, that choice is the main threat.
3. The variables sorted: common causes of treatment and outcome (adjust), consequences of treatment (never adjust), and anything the sample was selected on.
4. The design, chosen from the assignment mechanism, and the one assumption it rests on in a plain sentence: no unmeasured common cause; the groups would have moved in parallel; nothing else changed on that date; nobody sorted around the cutoff; the instrument acts only through the treatment.
5. The tests that assumption allows: trends before treatment, a placebo outcome, date or group, support and overlap. A failed one reveals a violation. A passed one does not establish identification.
6. Regression to the mean: whether units were treated because they were extreme. They would have moved back anyway.
7. Timing: every unit's clock starts at the same defined moment, and nobody enters the sample because of their outcome.
8. A staggered rollout gets an estimator built for one. Spillover to comparison units is examined.
9. How strong a hidden common cause would have to be to erase the result.
10. Uncertainty at the level where treatment was assigned. With few treated units, permutation inference.
11. The defensible specifications, listed before any is run. All are reported, with the spread and where the chosen one sits.
12. A known answer: where a past experiment exists, check that the method reproduces it. Otherwise plant an effect in simulated data and check the method recovers it.
13. The wording: "consistent with", the assumption named, the experiment that would settle it, and the weaker descriptive or predictive claim that stands if the assumption fails.

<a id="historical-records"></a>

## 3. Description or prediction from historical records

Write a data note before reporting.

1. How the records came to exist and what is missing: selection, units that disappeared, censoring, changes in recording practice.
2. The definitions (population, unit, period, numerator, denominator, eligibility) and whether they changed over the period. Preserve the query, the data revision and the date.
3. The grain: what one row is. Reconcile row and distinct-unit counts around each join and filter. Check duplicates and missingness.
4. Composition: whether the total moved because the mix moved. Mean of ratios or ratio of means, and weighted by what.
5. Concentration: whether a few units carry the result. Report with and without them, and quantiles beside means.
6. Time: season, trend, calendar. A before-and-after comparison needs a stated counterfactual.
7. Leakage: for prediction, reconstruct what was known at the historical time of decision. Nothing from the future in features, tuning or the assessment set. Splits by group and by time.
8. A naive baseline beside every model or rule.
9. Uncertainty on every number that drives the decision, resampled at the level of independent units.
10. Exploration and confirmation on different data. Patterns found after looking, and unplanned subgroup searches, are labelled.
11. Whether the measure captures the thing wanted: proxies, label noise.
12. In the write-up, what was observed, what was inferred and what was assumed are kept apart.
13. Every reported number traces to output newer than the code that produced it.

For an effect estimator or test, known-truth simulation and a null control reveal pipeline mistakes before a live study.
