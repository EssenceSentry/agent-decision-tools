# Discriminating explanations and designs

Use these checks when one piece of evidence or one interface choice carries the decision.

<a id="compare-two-designs"></a>

## Compare real calls and extensions

Write the same concrete client task against two different interfaces. Walk a partial failure and a likely extension through both. Compare how many callers must know ordering, defaults and recovery, and which must change. Keep a spike for the question that paper cannot answer.

<a id="evidence-cruxes"></a>

## Trace the weakest link

For each candidate conclusion, write observation → assumption → inference → action. Record the exact location when interpretation matters. Mark shared data or citations once. State the weakest premise, the counterevidence that would overturn it and the least expensive way to obtain it.

<a id="rival-predictions"></a>

## Make opponents predict the same test

Freeze what was observed and how cases entered the sample. Include a mundane artifact if plausible. For each rival, predict a concrete outcome under a new common condition. Mark results that would change the action, disconfirm a model or leave the question unresolved.

<a id="codebase-design"></a>

## Test interface depth and locality

Imagine deleting the abstraction. Trace where each invariant, ordering rule and error recovery step would reappear. Prefer the interface that concentrates correctness knowledge and is exercised by real consumers. Separate variation that already has a second adapter from hypothetical extension. For IO-heavy designs, compare an in-process implementation and an integration check at the real boundary. Retire redundant lower-level tests only when callers still have discriminating coverage.

<a id="competing-hypotheses"></a>

## Remove the strongest observation

Build an evidence-by-hypothesis matrix, coding expected, inconsistent or neutral. Drop rows that every rival predicts from the comparison. Consider absence only when the collection process would have detected the missing indicator. Then remove or reinterpret the most influential observation and compare the preferred explanation **and** the resulting action. If either flips, flag the fragile premise and price independent confirmation. If every model conflicts with credible evidence, reopen the candidate set.
