# Search and reuse checks

Use these procedures for a contested claim or a code search with several plausible owners.

<a id="deep-research"></a>

## Investigate separate gaps, then reconcile the findings

Split a broad question into complementary gaps. For each, vary short queries, open the complete promising record, and capture takeaway, corroboration or contradiction, inference, and missing evidence. At synthesis, check each consequential sentence against its cited passage. Remove unsupported precision, explain disagreements and put the decision-relevant answer first. The same agent can alternate between searching and editing.

<a id="primary-source-research"></a>

## Follow the claim to its owner

A press release may own the announcement date while a methods appendix owns the reported estimate. Cite the precise passage that supports each, with population, period and version. Record which unresolved link would change the decision.

<a id="reuse-before-writing"></a>

## Try the smaller path at the caller

Remove the proposed operation in a scratch example. If the caller still needs it, exercise the nearest supported project API, standard facility or adopted dependency on the input most likely to break the fit. Record each rejected match and the observed gap.

<a id="usage-map"></a>

## Regenerate a symbol-level map

For Python, run the [usage mapper](../scripts/usage_map.py) with the package directory and one or more consumer roots. Follow the reported import, public alias and candidate call to its definition and tests. Record checkout revisions, persisted formats and dynamic or external callers. Classify apparent duplicates only after comparing behavior and origin. For other languages use the project symbol index and the same evidence fields. Example from the skill directory:

```sh
git -C /path/to/library rev-parse HEAD
git -C /path/to/consumer rev-parse HEAD
python3 scripts/usage_map.py --library /path/to/library/src/metrics --consumer /path/to/consumer
```

Pass the importable package directory for the library, then repeat `--consumer` for additional roots. Treat star imports, local aliases, generated bindings and dynamic calls as coverage gaps. Check dirty working trees when recording revisions.

<a id="research"></a>

## Keep the cited note where it will be found

Write findings beside the project’s existing research notes. Link each decision-bearing statement to the owning specification, code or measurement. When returning to the same question, open the latest note and search for what changed.
