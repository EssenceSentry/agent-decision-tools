# Durable research and engineering records

Use these records when later decisions depend on facts or rationale that might otherwise be lost.

<a id="campaign-record"></a>

## Keep the campaign legible after a failed trial

Give the campaign one entry point listing objective, baseline, allowance, active trial and next test. Append dated trials with hypothesis, observation, evidence and retain/discard decision. Preserve failed approaches and what would justify reopening. Link the best result and its verification.

<a id="contract-records"></a>

## Trace a promise into the delivered artifact

Map each material guarantee to its owner, caller, version, verification and known exception. For an accepted limitation record why it was accepted, guard, trigger and upgrade path. A later version reopens a check if its assumptions change. Point superseded contracts forward.

<a id="research-wiki-layout"></a>

## Keep separate homes for current beliefs and history

Use a short index linking the question, approach, original evidence and current decision. Keep dated events append-only, link evidence in both directions, revise live claims and retain supersession pointers. Periodically consolidate repeated notes when a reader would otherwise reconstruct them.

<a id="solved-problem-note"></a>

## Make a verified remedy discoverable from its symptom

After a remedy has been verified, capture searchable symptoms, environment, root cause, failed attempts, fix and recurrence check. Choose the most useful retrieval tag: identification, data, numerical, methodology, derivation or replication. Include exact reproduction and version where available. Link related notes and mark superseded remedies. Use the [pre-compaction checkpoint](compaction.md) for work still open.

<a id="ponytail-debt"></a>

## Check whether a deliberate shortcut has expired

Run `python3 scripts/scan_debt.py /path/to/repo` from this package. For each `shortcut:` or `ponytail:` source comment, locate the caller and extract file, line, current ceiling and upgrade action. Flag missing triggers or exceeded ceilings, record owner, and aggregate totals. If the scan is empty, report the paths and ignore rules it covered.
