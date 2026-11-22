# Releases

Versions are commit snapshots: `0.0.1.devN+g<sha>`, where `N` counts commits
on the history and `<sha>` names the commit. Every commit is a version and no
tags are needed.

Snapshots can contain breaking changes. Anything that depends on this project
should pin a commit:

```bash
uv add "agent-decision-tools @ git+file:///absolute/path/to/agent-decision-tools@<commit>"
```

The package carries the `Private :: Do Not Upload` classifier, so PyPI refuses
it even if someone tries to publish it.
