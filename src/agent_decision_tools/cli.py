"""JSON command line for the decision toolkit."""

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from . import __version__
from .core import evaluate, schema, tools


def main(argv: Sequence[str] | None = None) -> int:
    """Discover, describe or run a calculation.

    Parameters
    ----------
    argv : sequence of str or None
        Arguments following the executable, or the process argument list.

    Returns
    -------
    int
        Zero on success or two for an invalid request.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="list operations and their purpose")
    commands.add_parser("schema", help="print the JSON input schema").add_argument(
        "tool"
    )
    run = commands.add_parser("run", help="evaluate JSON from a file or stdin")
    run.add_argument("tool")
    run.add_argument("path", nargs="?", default="-", help="input file or - for stdin")
    args = parser.parse_args(argv)
    try:
        if args.command == "run":
            source = (
                sys.stdin.read() if args.path == "-" else Path(args.path).read_text()
            )
            result = evaluate(args.tool, json.loads(source))
        elif args.command == "schema":
            result = schema(args.tool)
        else:
            result = dict(tools())
        print(json.dumps(result, indent=2, allow_nan=False))
    except (ValueError, OSError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 2
    return 0
