# Agent Decision Tools: notes for coding agents

Price evidence, plan bounded investigations and compare decisions under uncertainty.

## Layout

- `src/agent_decision_tools/core.py` dispatches validated requests to the decision, evidence, scheduling, record and Fermi modules.
- `src/agent_decision_tools/cli.py` is a thin command line over `core`.
- `tests/` mirrors the modules; `docs/` is Sphinx with MyST Markdown.
- `skills/bayesian-fermi-estimation/` contains the Squiggle skill and its Node.js runtime.
- `scripts/` holds repository checks that run as hooks.

## Commands

```bash
uv sync --locked                                          # Python environment
npm ci --ignore-scripts --prefix skills/bayesian-fermi-estimation
npm --prefix skills/bayesian-fermi-estimation test
uv run pytest                                             # tests with coverage
uv run pre-commit run --all-files                         # every commit gate
uv run pre-commit run --all-files --hook-stage pre-push   # tests and docs build
```

Run both pre-commit commands before saying a change is done; CI runs exactly
these hooks.

## Rules

- Keep every gate green, and never weaken one to get there: don't lower the
  coverage floor or the complexity limit, and don't add `# type: ignore`,
  `# noqa` or `pyright: ignore` without a comment saying why it is needed.
- Library code is type-checked in strict mode. Give every public function and
  class a numpy-style docstring; the docs build fails on a broken reference.
- Write a failing test first for new behavior or a bug fix.
- `core` must not import the command line or the service; import-linter
  enforces it.
- Add dependencies with `uv add` (runtime) or `uv add --group dev`, so
  `uv.lock` stays in step.
- Commit messages never credit an AI assistant as an author; a commit-msg hook
  rejects them. Stage explicit paths, never `git add -A` or `git add .`.
