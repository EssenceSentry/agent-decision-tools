# Will caching a build save time?

Estimate net minutes saved across a fixed number of identical runs. Each uncached run rebuilds. With caching, the first run builds and the batch incurs one setup cost. Build duration is uncertain and shared across these runs. Each avoided build saves that duration. The function accepts the duration as an input distribution, so the same calculation works with measured timings or a grounded range.

## Run the forward estimate

Paste this example into the [Squiggle playground](https://www.squiggle-language.com/playground). The last line returns the distribution. All numbers below are synthetic inputs for checking the arithmetic.

```squiggle
minutesSaved(runs, setupMinutes, buildMinutes) =
  (runs - 1) * buildMinutes - setupMinutes

buildMinutes = lognormal({p10: 2, p90: 8})
minutesSaved(4, 12, buildMinutes)
```

For a real decision, take the planned run count from the job manifest and the setup cost from a measurement or grounded range. Use timing logs from comparable builds where available. Given a nonempty list of comparable durations named `loggedMinutes`, use `List.map(loggedMinutes, {|m| minutesSaved(4, 12, m)})` with the run count and setup cost for your case. Each row yields one possible savings value. The resulting list preserves the observed frequencies exactly. Document the workload and period the timings cover. If different jobs have different costs, preserve matched observations when comparing the cached and uncached alternatives.

When eliciting a range, document what supports each endpoint. Here `p10` and `p90` describe a central 80% interval under a lognormal assumption. The positive `a to b` shorthand in Squiggle denotes the 5th and 95th percentiles. [Distribution creation](https://www.squiggle-language.com/docs/Guides/DistributionCreation)

## Check the result

The implied median build duration is 4 minutes. At four runs, net savings are three times the build duration minus 12 minutes. The theoretical 10th, 50th and 90th percentiles are therefore −6, 0 and 12 minutes, and the probability of positive savings is 50%. Change the run count to one and the answer must be −12 minutes for every draw. Sampling more tightly around 50% would add little here. A better measurement of setup time could change the decision.

The decomposition, factor-by-factor justification, remainder and dependence checks come from the [original Fermi worksheet](https://github.com/product-on-purpose/thinking-framework-skills/blob/6ab95db2d6469e4b65f3eb3ed265e46a6a1e69a8/skills/think-fermi-estimation/SKILL.md).
