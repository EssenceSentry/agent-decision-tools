# Create a dated decision record

When the project already has a decision record generator, use its convention. Otherwise the bundled Python helper creates a dated Markdown draft with slots for owner, premises, alternatives and reopening. It discovers an existing decisions directory or accepts one explicitly. Run it from the project in which the record belongs, place the title in quotes, and fill the draft with real evidence.

```sh
python3 "$SKILL_DIR/scripts/new_adr.py" --repo-root . --dir docs/decisions --title "Keep the local reader contract" --json
```

`SKILL_DIR` names this skill's directory. Add `--update-index` when this project maintains a Markdown index and you intend to update it. Serialize index updates when more than one writer is active. An existing same-day record with the same slug is preserved. If an index update fails after the record was written, inspect the reported failure and add its link to the index. The generated file is a draft until the actual decision owner accepts it.

The generator derives from Vercel's ADR skill. This copy uses exclusive creation for the decision file and a project-specific template. The package includes the upstream license. [Pinned source](https://github.com/vercel/ai/blob/d55f3cfc456d1b7bc7db3a4b70fbf602ddc8647d/skills/adr-skill/scripts/new_adr.js)
