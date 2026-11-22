# Using a Fermi estimate to decide what to buy

These two examples come from the planning discussion about a 20-minute repository probe and the cost of a second expert opinion. The records and counts below are synthetic. The decision logic and field definitions can be reused with real evidence. Each Squiggle block runs independently.

## 1. How much rework could a repository probe avert?

**When to use it.** A developer can spend 20 active minutes looking for a supported helper or start implementing three caller changes. The rough claim is that finding the helper would save two hours. Estimate the active minutes actually saved **conditional on finding a compatible helper**. Work that both implementations require cancels out.

**Where the inputs come from.** In this example the change list identifies three comparable callers. A summary of 30 matched past changes reports 20 and 80 minutes as the 10th and 90th percentiles of *additional active effort per caller* for the local implementation over integration with a helper. Only these summary quantiles are available. The estimator assumes a positive lognormal distribution and that all three callers share the same underlying integration difficulty. The 20-minute probe is costed at its full allowance. In a real estimate, check whether the historical work included a one-time task that would be paid only once across callers.

If the timing summary is missing, build the per-caller estimate from the number of extra edit-and-check cycles visible in comparable changes and the active minutes measured for a representative cycle. Carry the resulting distribution into the same function.

```squiggle
minutesSavedIfFound(callers, extraMinutesPerCaller) = callers * extraMinutesPerCaller

saved = minutesSavedIfFound(3, lognormal({p10: 20, p90: 80}))
{
  minutesSavedIfFound: saved,
  breakEvenChanceOfFindingHelper: 20 / mean(saved)
}
```

**How to read it.** Conditional savings have a median of 120 minutes, a central 80% interval of 60–240 minutes and a mean of about 139 minutes. If an unsuccessful search saves zero time, the probe pays in expected active time when its chance of finding the helper exceeds about **14.4%** under the specified lognormal model. The mean belongs in this calculation because the decision is about expected time. Treating the two-hour median as a fixed saving would give a one-in-six threshold. If there is little evidence about search success, report the threshold and look for outcomes of comparable past searches before assigning odds.

## 2. How often would a second reviewer change the decision?

**When to use it.** A team is considering a second model review of work already accepted by its first reviewer. Estimate how often the extra review produces a verified change in the accept/rework decision. Count each verified change once, however many comments it generated.

**Where the inputs come from.** In this example a historical replay sent every sampled first-pass acceptance to a second reviewer. Independent adjudication established which additional findings warranted changing the decision. Each row below is one comparable review period. `Changed` counts cases with at least one such finding, and `Seen` counts *all* eligible cases reviewed in that stratum. Today’s queue contains 12 routine and 8 high-risk cases. Both strata use the same risk definition across periods.

```squiggle
changeRate(routine, highRisk, period) = {
  routineRate = period.routineChanged / period.routineSeen
  highRiskRate = period.highRiskChanged / period.highRiskSeen
  (routine * routineRate + highRisk * highRiskRate) / (routine + highRisk)
}

periods = [
  {routineChanged: 3, routineSeen: 60, highRiskChanged: 6, highRiskSeen: 20},
  {routineChanged: 6, routineSeen: 60, highRiskChanged: 3, highRiskSeen: 20},
  {routineChanged: 0, routineSeen: 60, highRiskChanged: 4, highRiskSeen: 20},
  {routineChanged: 3, routineSeen: 60, highRiskChanged: 5, highRiskSeen: 20}
]
List.map(periods, {|p| changeRate(12, 8, p)})
```

**How to read it.** The four historical conditions imply **15%, 12%, 8% and 13%** for today’s queue. Their mean is **12%** if the periods are equally relevant. Applying each period as a whole preserves co-movement between the two strata. The spread describes shifts across these historical conditions. Predicting the realized count in a future batch would also require accounting for finite historical samples and case-to-case variation. The same records imply average rates of **5%** for routine cases and **22.5%** for high-risk cases. A decision about where to buy reviews can use these rates alongside the value of a corrected decision, the review price and the cost of handling false alarms. If only disputed cases had received a second review in the archive, representative data on accepted cases would be needed to estimate these rates.
