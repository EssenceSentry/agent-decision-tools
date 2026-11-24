# Match the test to the promise

Write the failure at the place where a caller relies on the promise. Identify a wrong implementation that would look plausible. Choose an oracle independent enough to notice that mistake.

| Claim or failure | Discriminating check |
|---|---|
| A particular regression changes an observable result | Run a focused public-interface example on the old and corrected revisions. Confirm why it fails on the old revision. |
| A relation holds across a family of valid inputs | Generate across the important boundaries, assert the invariant and shrink failures. Check that the generator reaches the suspected failure. |
| The exact output is difficult to obtain but a transformation has a known effect | Apply a metamorphic relation. Include a case where the transformation matters. |
| An independent reference or older trusted implementation exists | Run a differential test on matched inputs and explain any intentional differences. |
| State, retries or concurrent operations affect correctness | Explore short event sequences against a model, then replay the decisive trace at the real boundary. |
| A small critical domain can be enumerated | Exhaust the supported inputs or verify a precise bounded model. |
| Input arrives from outside the trust boundary: a parser, a decoder, a request handler | Fuzz with malformed, oversized and hostile input. Assert that it fails safely and that nothing crosses the boundary unchecked. |
| A statistical algorithm promises a false-positive rate, coverage or power | Simulate under known truth, with a null and a relevant alternative. Report Monte Carlo uncertainty. |
| A new caller must discover, use or extend the supported API | Prepare a clean consumer fixture and a task stated in the caller’s terms. Check actual use and the observable result. For an authorized usability trial, give a fresh consumer the task in the caller’s words and observe which interface they actually find. |
| A published artifact must stay compatible | Use a reviewed reference artifact through an actual consumer and specify how expected changes are accepted. |

Two inverse functions with the same mistake can pass a round-trip test. A mock can assert the call that the implementation already makes. Change one input, invariant or behavior in a disposable fixture to see that the chosen check can notice a consequential failure. For costly side effects inspect an independent observable such as the persisted receipt or downstream consumer state. Scale the more expensive checks to the stakes and budget.

Where a wrong result costs money, loses data or stays silent, add two things to the row's check. Mutate the code and confirm the tests fail, because a suite that passes on broken code proves nothing. For a side effect that cannot be undone, compare against an oracle outside the code under test.
