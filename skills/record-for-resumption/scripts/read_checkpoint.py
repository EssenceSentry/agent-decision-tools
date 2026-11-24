#!/usr/bin/env python3
"""Read a recovery snapshot or explicitly clear a single host session."""

import argparse
import sys
from pathlib import Path

import checkpoint_store as store


def main():
    """Resolve a project and host without guessing between multiple sessions."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host", choices=("codex", "claude"))
    parser.add_argument("project", type=Path)
    parser.add_argument("--state-dir", type=Path, default=store.state_dir())
    parser.add_argument("--session-key")
    parser.add_argument("--clear", action="store_true")
    args = parser.parse_args()
    root = args.state_dir / store.digest(args.project.resolve(strict=True))
    if not root.is_dir():
        raise ValueError("No checkpoint found for this host and project.")
    with store.locked(root):
        sessions = sorted(
            p.name
            for p in root.iterdir()
            if store.SESSION.fullmatch(p.name)
            and p.name.startswith(args.host + "-")
            and not p.is_symlink()
            and store.owned(p / "latest")
        )
        if not sessions:
            raise ValueError("No checkpoint found for this host and project.")
        if not args.session_key and len(sessions) > 1:
            print("Choose a session with --session-key:", *sessions, sep="\n")
            return
        key = args.session_key or sessions[0]
        if key not in sessions:
            raise ValueError("Unknown session key for this project.")
        folder = root / key
        if args.clear:
            files = list(folder.iterdir())
            if not all(store.owned(p) for p in files):
                raise ValueError(
                    "Session contains unrecognized files. Review it before clearing."
                )
            for p in files:
                p.unlink()
            folder.rmdir()
            print("Cleared " + key)
            return
        filename = (folder / "latest").read_text().strip()
        if not store.SNAPSHOT.fullmatch(filename) or not store.owned(folder / filename):
            raise ValueError("Invalid snapshot pointer.")
        sys.stdout.write((folder / filename).read_text())


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        sys.exit(str(error))
