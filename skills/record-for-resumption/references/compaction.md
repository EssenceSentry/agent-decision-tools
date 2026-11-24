# Keep a recovery copy at compaction and read it back

The checkpoint is a recovery copy for the case where compaction loses something. The owning record stays the authority, and a session that keeps its record current may never read a checkpoint. The handler has been exercised with event fixtures for both hosts. It has not yet been observed through a live compaction in either host.

Register the checkpoint only for a project where automatic recovery snapshots are wanted. Run the corresponding line from the installed skill directory. Use an existing project-relative owning record, or omit `--record` to use visible progress. `--print` previews the native settings.

```sh
python3 scripts/register_hook.py codex /absolute/project --record notes/current.md
python3 scripts/register_hook.py claude /absolute/project --record notes/current.md
python3 scripts/register_hook.py claude /absolute/project --record notes/current.md --progress 0 --keep 3 --max-age-days 14
```

`--progress N` sets how many recent visible assistant messages are copied, from 0 to 8, default 3. Use 0 where the transcript may hold material that should not be copied to the state directory. The explicit handoff block is saved either way. `--keep N` keeps the newest N snapshots of a session, default 5. `--max-age-days D` removes the checkpoints of sessions in the same project that have had no snapshot for D days, default 30.

To upgrade a registration created by the Node version at this same installation path, rerun the registrar with the original options. If you also moved the installation, replace the old command in the project settings with the command from `--print`.

The [registrar](../scripts/register_hook.py) preserves other project settings. Codex reads `.codex/hooks.json` in a trusted project. Claude Code reads `.claude/settings.local.json`. Open or reload the host in that project. In Codex, inspect the entry in `/hooks` and approve its current command when the host asks. The executable path refers to this copy of the skill. Update the registration if the copy moves.

Keep the owning record current when evidence changes. If there is no record, include a fenced `handoff-state` block in visible progress at a natural milestone. Populate the applicable fields from actual work:

- Current question, owner, accepted scope, remaining allowance and agreed next action.
- Data revision, eligibility, transformations, working commands, package versions and artifact location.
- Identification assumptions, decisive estimate and uncertainty, comparison, convergence and sensitivity.
- For a derivation, last justified step, regularity conditions and unresolved gap.
- For engineering, caller, delivered revision, public contract, failing or passing check and diagnostics.
- Abandoned attempts and decisive counterevidence, unresolved method or submission status, first command to rerun and expected observation.

The [checkpoint handler](../hooks/checkpoint.py) accepts automatic and manual PreCompact events. It saves the final 32 KiB of the nominated record, the last explicit handoff in the final 4 MiB of transcript and the recent visible assistant messages allowed by `--progress`. It then prunes older snapshots as registered. It makes no model call. Keep credentials out of those records. It cannot infer an unrecorded failed trial. With no usable evidence it leaves the preceding checkpoint intact.

The host output names the saved Markdown file. To recover later, use the [read-back command](../scripts/read_checkpoint.py). Give the same project and host, and the same `--state-dir` if registration used one. With multiple sessions, select one of the listed keys. Inspect the primary artifact and run the verifying action before relying on reported progress.

```sh
python3 scripts/read_checkpoint.py codex /absolute/project
python3 scripts/read_checkpoint.py codex /absolute/project --session-key KEY_FROM_LIST
python3 scripts/read_checkpoint.py codex /absolute/project --session-key KEY_FROM_LIST --clear
```

`--clear` deletes that session's snapshots once its state is back in the owning record.

Snapshots live under `$XDG_STATE_HOME/agent-process/checkpoints`, falling back to `~/.local/state/agent-process/checkpoints`. Each project and host session has its own pointer and content-addressed files, readable only by the owner. Repeating the same event preserves the same contents.

Host contracts and trust settings are documented in [Codex hooks](https://developers.openai.com/codex/hooks/) and [Claude Code hooks](https://code.claude.com/docs/en/hooks#precompact).
