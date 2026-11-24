#!/usr/bin/env python3
"""Run ordered tests separately and locate the first to leave a watched path."""

import argparse
import json
import os
import subprocess
import sys


def main():
    """Return 0 for absent, 1 for observed, or 2 for an inconclusive trial."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runner", required=True)
    parser.add_argument("--watch", required=True)
    parser.add_argument("--arg", action="append", default=[])
    parser.add_argument("--timeout-ms", type=int, default=30_000)
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()
    if args.timeout_ms <= 0:
        parser.error("--timeout-ms must be positive")
    if os.path.lexists(args.watch):
        parser.error("Watched path already exists before the first test.")
    for name in args.files:
        try:
            subprocess.run(  # noqa: S603 -- caller selects the test runner, without a shell.
                [args.runner, *args.arg, name],
                check=True,
                timeout=args.timeout_ms / 1000,
                stdin=subprocess.DEVNULL,
                stdout=sys.stderr,
                stderr=sys.stderr,
            )
        except (subprocess.SubprocessError, OSError) as error:
            print(
                f"Inconclusive runner for {name} ({error}). "
                "Inspect the fixture before resuming.",
                file=sys.stderr,
            )
            return 2
        if os.path.lexists(args.watch):
            print(
                json.dumps(
                    {"status": "observed", "test": name, "path": args.watch, "code": 1}
                )
            )
            return 1
    print(json.dumps({"status": "absent", "trials": len(args.files), "code": 0}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
