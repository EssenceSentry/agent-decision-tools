#!/usr/bin/env python3
"""Register a project-local PreCompact recovery hook for Claude or Codex."""

import argparse
import json
import os
import shlex
import sys
from pathlib import Path

import checkpoint_store as store

HANDLER = Path(__file__).resolve().parents[1] / "hooks/checkpoint.py"


def merge(groups, desired, args):
    """Upgrade our legacy command in place and retain unrelated host hooks."""
    for group in groups:
        for entry in group.get("hooks", []):
            if entry.get("type") != "command":
                continue
            try:
                existing = shlex.split(entry.get("command", ""))
            except ValueError:
                continue
            if len(existing) < 6 or existing[2:6] != args[2:6]:
                continue
            if existing[1] not in (str(HANDLER), str(HANDLER.with_suffix(".mjs"))):
                continue
            if existing[6:] != args[6:]:
                raise ValueError(
                    "An existing registration uses different options. "
                    "Review and replace its command in the project settings."
                )
            if existing == args:
                return False
            entry["command"] = desired["hooks"][0]["command"]
            return True
    groups.append(desired)
    return True


def main():
    """Print the registration or atomically merge it into native host settings."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host", choices=("codex", "claude"))
    parser.add_argument("project", type=Path)
    parser.add_argument("--record", type=Path)
    parser.add_argument("--state-dir", type=Path, default=store.state_dir())
    parser.add_argument("--print", action="store_true")
    for name in store.LIMITS:
        parser.add_argument("--" + name)
    opts = parser.parse_args()
    project = opts.project.resolve(strict=True)
    if opts.record and (opts.record.is_absolute() or ".." in opts.record.parts):
        raise ValueError("Choose a record inside the project")
    args = [
        sys.executable,
        str(HANDLER),
        "--host",
        opts.host,
        "--project",
        str(project),
        "--state-dir",
        str(opts.state_dir.resolve()),
    ]
    if opts.record:
        args.extend(("--record", str(opts.record)))
    for name, count in store.checked_limits(opts).items():
        args.extend(("--" + name, str(count)))
    group = {
        "matcher": "manual|auto",
        "hooks": [{"type": "command", "command": shlex.join(args), "timeout": 15}],
    }
    if opts.print:
        print(json.dumps({"hooks": {"PreCompact": [group]}}, indent=2))
        return
    config = project / (
        ".codex/hooks.json" if opts.host == "codex" else ".claude/settings.local.json"
    )
    config.parent.mkdir(exist_ok=True)
    if (
        config.parent.is_symlink()
        or config.is_symlink()
        or (config.exists() and not config.is_file())
    ):
        raise ValueError("Host settings must use a regular file and directory")
    lock = config.with_name(config.name + ".merge-lock")
    lock.touch(exist_ok=False, mode=0o600)
    try:
        original = config.read_bytes() if config.exists() else None
        settings = json.loads(original) if original is not None else {}
        groups = settings.setdefault("hooks", {}).setdefault("PreCompact", [])
        if not isinstance(groups, list):
            raise ValueError("Unexpected PreCompact configuration")
        if merge(groups, group, args):
            mode = (config.stat().st_mode & 0o777) if original is not None else 0o600
            if (config.read_bytes() if config.exists() else None) != original:
                raise ValueError("Host settings changed during registration")
            store.atomic_text(config, json.dumps(settings, indent=2) + "\n", mode)
    finally:
        lock.unlink()
    print(os.fspath(config))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        sys.exit(str(error))
