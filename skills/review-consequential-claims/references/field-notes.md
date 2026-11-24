# Review by failure mode

Use a targeted pass when a particular failure could survive the baseline checks. In every pass the reviewer reads the artifacts itself, changes nothing, and gives for each finding the evidence that would withdraw it.

<a id="causal-auditor"></a>

## Audit each identifying assumption separately

State the estimand, method, assignment process and evidence available. Check the matching [method-specific diagnostics](causal-diagnostics.md). Distinguish empirical violations, compatible evidence and untestable assumptions. Record each check, result, implication and next action. Check which analysis packages are available and label skipped diagnostics. A successful diagnostic alone cannot establish identification.

<a id="adversarial-review-ledger"></a>

## Make a claimed guarantee fail at its point of use

Follow one consequential guarantee from caller to implementation. Create a realistic state where existing checks could pass but the caller sees a wrong result. Record location, input, observation, consequence, counterevidence and repair. For a consciously accepted limitation identify owner, guard and reopening trigger.

<a id="research-review"></a>

## Check the inference before polishing the report

Trace the main conclusion to original observations, design and arithmetic. Separate correctness, identification, robustness and communication. Try the strongest rival interpretation, check discrepancies in uncertainty or scope, and say whether each finding changes the decision or its wording. Return up to five ranked findings with an explicit clean scope where warranted.

<a id="spec-trace"></a>

## Trace each material promise both ways

Map requirement to implementation branch, test and public artifact. Then read the artifact back against the requirement. Look for omitted behaviors, unstated defaults and changes that escaped scope. Verify a boundary, older record or partial failure that the happy-path test misses.

<a id="tests-and-spec"></a>

## Separate contract membership from test strength

List specified behaviors and their evidence. Then ask whether each check actually fails for the claimed reason when behavior changes. Flag missing requirements, implementation-only assertions, brittle fixtures and unobserved boundary effects separately.

<a id="agent-reviewer"></a>

## Review four axes against the same baseline

Pin base revision, commits, dirty files and test state. Map changes and affected callers. Read the diff in four passes: defects (state, data loss, concurrency, errors), architecture (ownership, contracts, dependency direction), craft (clarity, complexity, duplication), and tests (failure-capable evidence and coverage). Tag evidence as observed or inferred. Verify any proposed repair addresses the trigger and the review left the tree intact.

<a id="code-review"></a>

## Compare the diff with both spec and standards

Use a resolved fixed point and merge base. Name the spec and repository standards and inspect changed commits and affected callers. Report a concrete smell only if its consequence and a simplifying change are clear, e.g. duplicated rules drifting between callers or feature envy across a boundary. Preserve separate spec and standards findings and highest severity on each axis.

<a id="ponytail-review"></a>

## Try the deletion before recommending it

Summarize what the change does. Check correctness, safety, load, tests and performance before proposing deletion. Trace every consumer and the behavior a layer protects. For each surviving finding show where, what breaks, evidence and the smallest fix. Distinguish must-fix defects, useful cuts and accepted tradeoffs.
