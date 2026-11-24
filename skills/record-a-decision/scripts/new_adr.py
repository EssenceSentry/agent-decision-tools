#!/usr/bin/env python3
"""Create a dated architecture decision record and optionally index it."""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

DIRECTORIES = (
    "contributing/decisions",
    "docs/decisions",
    "adr",
    "docs/adr",
    "docs/adrs",
    "decisions",
)


def update_index(index, title, output, date):
    """Insert under the ADRs heading, or append if the heading is absent."""
    link = os.path.relpath(output, index.parent).replace(os.sep, "/")
    content = index.read_text() if index.exists() else "# ADR Log\n\n"
    if link in content:
        return False
    lines = content.splitlines()
    position = len(lines)
    for start, line in enumerate(lines):
        if re.fullmatch(r"##\s+ADRs\s*", line, re.I):
            end = next(
                (
                    i
                    for i in range(start + 1, len(lines))
                    if re.match(r"##\s+", lines[i])
                ),
                len(lines),
            )
            position = next(
                (
                    i + 1
                    for i in reversed(range(start + 1, end))
                    if re.match(r"[-*]\s+", lines[i])
                ),
                end,
            )
            break
    lines.insert(position, f"- [{title}]({link}) ({date})")
    index.parent.mkdir(parents=True, exist_ok=True)
    index.write_text("\n".join(lines) + ("\n" if content.endswith("\n") else ""))
    return True


def main():
    """Create the record exclusively and print its path or the JSON result."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--dir")
    parser.add_argument("--no-create-dir", action="store_true")
    parser.add_argument("--update-index", action="store_true")
    parser.add_argument("--index-file")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.repo_root.resolve(strict=True)
    folder = (
        root / args.dir
        if args.dir
        else next((root / d for d in DIRECTORIES if (root / d).is_dir()), root / "adr")
    )
    if not args.no_create_dir:
        folder.mkdir(parents=True, exist_ok=True)
    title = args.title.strip()
    slug = (
        re.sub(r"[^a-z0-9]+", "-", re.sub(r"['\x22\x60]", "", title.lower())).strip("-")
        or "decision"
    )
    date = time.strftime("%Y-%m-%d", time.gmtime())
    output = folder / f"{date}-{slug}.md"
    template = Path(__file__).resolve().parents[1] / "assets/templates/adr-simple.md"
    content = template.read_text().replace("{TITLE}", title).rstrip() + "\n"
    with output.open("x") as record:
        record.write(content)
    index = None
    changed = False
    if args.update_index:
        index = (
            root / args.index_file
            if args.index_file
            else next(
                (
                    folder / n
                    for n in ("README.md", "index.md")
                    if (folder / n).exists()
                ),
                folder / "README.md",
            )
        )
        changed = update_index(index, title, output, date)
    result = {
        "repoRoot": str(root),
        "adrDir": str(folder),
        "createdAdrPath": str(output),
        "createdAdrRelPath": os.path.relpath(output, root),
        "title": title,
        "date": date,
        "indexUpdated": index is not None,
        "indexChanged": changed,
        "indexPath": str(index) if index else None,
        "indexRelPath": os.path.relpath(index, root) if index else None,
    }
    print(json.dumps(result) if args.json else output)


if __name__ == "__main__":
    try:
        main()
    except OSError as error:
        sys.exit(str(error))
