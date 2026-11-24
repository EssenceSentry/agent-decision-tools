# A source note another reader can use

Use only the fields that affect this decision. Put the note in the existing project record when the search needs to survive the session.

| Claim and current status | Source, date/revision and exact locator | What was inspected | Source reliability and claim credibility |
|---|---|---|---|
| A maintenance job currently runs nightly | Scheduler configuration at the deployed revision and the latest completed run | The active schedule and run timestamps | The scheduler owns the configured cadence. The run history supports actual execution only over the inspected dates. |
| An upstream report attributes a change in outcome to that job | The original analysis and its comparison window | Full methods and table, if accessible | The author measured the outcome. A contemporaneous change in traffic mix makes the attribution unresolved. |

These are illustrative entries. A second summary of the same measurement adds a citation path and no independent observation. Keep the alternative explanation and name what would resolve it. Under gaps, give the exact query and scope, separated into searched with no relevant hit, inaccessible, and unexamined.

For code, start from the literal consumer entry point. A reproducible first pass against a Git working tree can use these commands.

```sh
git rev-parse HEAD
git status --short
git grep -n -I --untracked -F -e 'read_snapshot' -- .
```

Record the relevant calls and definitions, open the matching lines, inspect the version consumers actually use, and check indirect uses such as serialized names or dynamic dispatch when consequential. A text match only establishes where to look. If a public reader checks a manifest or selects the last committed snapshot, a direct file read can return different data even when a happy-path example passes.

For the next search, consider a hypothetical 12-minute contract probe. Three matched *successful* reuse attempts avoided 30, 60 and 90 minutes respectively. With zero savings on a miss, the search breaks even at 12 / 60 = 20%. A success-only archive supports the conditional savings but leaves the hit rate unknown. If the contract is mandatory, verify it through the cheapest reliable route anyway.
