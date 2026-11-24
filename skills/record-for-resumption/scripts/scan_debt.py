#!/usr/bin/env python3
"""Find shortcut markers in tracked and nonignored untracked Git files."""

import argparse
import subprocess
import sys


def main():
    """Run Git's working-tree grep and distinguish no matches from errors."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=".")
    repo = parser.parse_args().repo
    root = subprocess.run(  # noqa: S603 -- literal Git arguments.
        ["git", "-C", repo, "rev-parse", "--show-toplevel"],  # noqa: S607 -- system Git.
        check=False,
        stdout=subprocess.PIPE,
        text=True,
    )
    if root.returncode:
        return root.returncode
    result = subprocess.run(  # noqa: S603 -- literal Git arguments.
        [  # noqa: S607 -- system Git.
            "git",
            "-C",
            root.stdout.rstrip("\n"),
            "grep",
            "--untracked",
            "--exclude-standard",
            "-I",
            "-n",
            "-E",
            "(#|//|/[*])[[:space:]]*(shortcut|ponytail):",
            "--",
            ".",
        ],
        check=False,
    )
    if result.returncode == 1:
        print("No shortcut markers found.")
        return 0
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
