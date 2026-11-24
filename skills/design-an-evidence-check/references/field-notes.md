# Evidence design by claim

Use only the sections that match what the proposed evidence must establish. The experiment, causal-claim and historical-data checklists are in [research checks](research-checks.md).

<a id="causal-planner"></a>

## Choose identification from assignment

Write the decision, unit, eligibility, exposure history, time zero, outcome and comparison. Determine who controlled assignment and when. A pooled set of randomized trials with different treatment rates needs within-trial comparisons or known assignment probabilities. For prior universal exposure, ask whether a randomized removal would answer the current question. Route through the [assignment and diagnostic table](causal-designs.md) before choosing software. Record the strongest supportable fallback if the design fails.

<a id="evidence-gate"></a>

## Write the action after every outcome

Include an ambiguous result and false alarm. Price collecting, waiting, interpreting and following up. If all observations lead to the same choice, the optional test buys no decision value. Bound any pivotal unknown with break-even or a grounded distribution. Record how the forecast will resolve.

<a id="property-test-rule"></a>

## Make a general property falsifiable

State the domain and observable invariant. Generate valid edge and typical cases. Show the generator visits the risky behavior. Try a plausible mutant or independent oracle: two mutually inverse mistakes can pass a round-trip test. Shrink a failure into a permanent example.

<a id="testing-strategies"></a>

## Choose the cheapest test with a decisive oracle

Use examples for specified behavior, properties for families, transformations for metamorphic checks, differential comparison against an independent reference, and state machines for retries/interleavings. Use exhaustive checks on small finite domains, known-truth simulation for statistical claims and reviewed goldens for formats. Specify who relies on the output and where to observe failure.

<a id="sql-data-correctness"></a>

## Test the data contract at the join

Declare one-row-per keys on both sides. Count rows, distinct and NULL keys, and reconcile additive amounts by key before rolling up. Test unmatched parents, filtered outer joins, three-valued logic, soft deletion and complete days in the business time zone. Trace changed types, signs, precision and names to real consumers. Use the [worked SQL probes](sql-probes.md). Confirm environment and freshness from the owning project.

<a id="test-driven-development"></a>

## Freeze expected behavior before making a fix

For an agreed behavior, write a coherent set of happy, edge and failure cases. Show each fails on the old implementation for the intended reason. Preserve the oracle while implementing. If the expectation was wrong, explain the contract change before editing it. Test at the public seam and run affected callers.

<a id="tdd"></a>

## Build one vertical slice when the interface is uncertain

Exercise one caller-visible behavior through the real interface. Watch it fail, implement the smallest working slice, then add the next behavior. Prefer real internal collaborators. Fake slow, external or nondeterministic boundaries with contract-faithful data. A private method rename should leave a behavior check green.

<a id="superpowers-test-driven-development"></a>

## Verify both red and green

Check the failure message before editing code: a setup exception gives no evidence about the missing behavior. Run the same check unchanged after the minimal implementation, then the related suite. Refactor only on green. Reject mocks that merely reproduce the implementation, production methods created solely for tests, and single-path fixtures that hide missing fields.

<a id="think-fermi-estimation"></a>

## Propagate grounded uncertainty through one forward model

Define a resolvable quantity and unit. Break it into better-known factors with evidence or explicit elicitation bounds. Model shared drivers once. Use one small Squiggle function, including sums, caps or conditional branches where needed. Report quantiles, probability of crossing the action threshold and which input matters. Check an independent route or limiting case. Use the decision-tools Fermi skill for runnable examples.

<a id="think-reference-class-forecasting"></a>

## Anchor the forecast in comparable completed cases

Choose the inclusion rule and horizon before observing outcomes. Report count, dates, inclusion of failures, denominator, outcome distribution and relevance to the present case. Quantify any documented adjustment and show the unadjusted result. Sparse or selected history earns wider uncertainty. Keep an outcome-resolution date.
