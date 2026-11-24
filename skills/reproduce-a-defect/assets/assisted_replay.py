#!/usr/bin/env python3
"""Copy this template and adapt the prompts to your local reproduction."""

import sys


def step(instruction):
    """Pause while the participant carries out the instruction."""
    print(f"\n>>> {instruction}")
    input("    [Enter when done] ")


def capture(question):
    """Read one visible, nonsensitive observation."""
    print(f"\n>>> {question}")
    return input("    > ")


def main():
    """Print machine-readable observations only after the replay finishes."""
    step("Open the local test fixture at the revision recorded for this replay.")
    errored = capture("Click the 'Export' button. Did it throw an error? (y/n)")
    category = capture(
        "Record the visible error category (or 'none'), omitting private data:"
    )
    print(f"\n--- Captured ---\nERRORED={errored}\nERROR_MSG={category}")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        sys.exit("Replay interrupted before all observations were captured.")
