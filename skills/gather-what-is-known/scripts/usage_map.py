"""Map Python imports, public re-exports and potential consumer calls offline."""

from __future__ import annotations

import argparse
import ast
import json
import os
import tokenize
from importlib.util import resolve_name
from pathlib import Path


def sources(root):
    """Yield ordinary Python source files, skipping dependencies and generated trees."""
    ignored = {"venv", "node_modules", "__pycache__", "build", "dist", "site-packages"}
    for folder, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d not in ignored)
        for name in sorted(files):
            file = Path(folder, name)
            if name.endswith(".py") and not file.is_symlink():
                yield file


def imports(node, package):
    """Yield local binding name, requested path and the prefix bound to the name."""
    if isinstance(node, ast.Import):
        for alias in node.names:
            first = alias.name.split(".")[0]
            yield (
                alias.asname or first,
                alias.name,
                alias.name if alias.asname else first,
            )
    elif isinstance(node, ast.ImportFrom):
        prefix = "." * node.level + (node.module or "")
        if node.level:
            try:
                prefix = resolve_name(prefix, package)
            except (ValueError, ImportError):
                return
        for alias in node.names:
            target = f"{prefix}.{alias.name}"
            yield alias.asname or alias.name, target, target


def chain(node):
    """Read a dotted name without evaluating expressions."""
    tail = []
    while isinstance(node, ast.Attribute):
        tail.append(node.attr)
        node = node.value
    return [node.id, *reversed(tail)] if isinstance(node, ast.Name) else []


def owner(target, exports, definitions):
    """Resolve explicit imports and re-exports to a declaration when one is known."""
    seen = set()
    while True:
        if target in definitions:
            return target
        parts = target.split(".")
        prefix = next(
            (
                ".".join(parts[:i])
                for i in range(len(parts), 0, -1)
                if ".".join(parts[:i]) in exports
            ),
            None,
        )
        if prefix is None or prefix in seen:
            break
        seen.add(prefix)
        target = exports[prefix] + target[len(prefix) :]
    return None


def inspect_file(file, module, package, name, result):
    """Read one source file and enumerate imports and possible calls."""
    try:
        with tokenize.open(file) as handle:
            tree = ast.parse(handle.read(), str(file))
    except (OSError, SyntaxError, UnicodeError) as exc:
        result["gaps"].append({"file": str(file), "reason": str(exc)})
        return {}, set()

    direct = set(tree.body)
    aliases = {}
    declared = {module} if module else set()
    rows = result["internal_imports" if module else "consumer_imports"]
    for node in ast.walk(tree):
        if (
            module
            and node in direct
            and isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
        ):
            declared.add(f"{module}.{node.name}")
        for binding, target, bound in imports(node, package):
            if target.split(".")[0] != name:
                continue
            rows.append(
                {
                    "file": str(file),
                    "line": node.lineno,
                    "module": module,
                    "binding": binding,
                    "requested": target,
                }
            )
            if binding == "*":
                result["gaps"].append(
                    {
                        "file": str(file),
                        "line": node.lineno,
                        "reason": "star import requires inspection",
                    }
                )
            elif node in direct:
                aliases.setdefault(binding, set()).add(bound)
    exported = {
        f"{module}.{binding}": next(iter(targets))
        for binding, targets in aliases.items()
        if module and len(targets) == 1
    }
    # Locations are candidates for tracing. Avoid selecting between repeated imports.
    if not module:
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                parts = chain(node.func)
                options = aliases.get(parts[0], set()) if parts else set()
                if len(options) == 1:
                    target = ".".join([next(iter(options)), *parts[1:]])
                    result["calls"].append(
                        {"file": str(file), "line": node.lineno, "requested": target}
                    )
    return exported, declared


def main():
    """Print a JSON usage map for one import package and named consumer trees."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library", type=Path, required=True, help="Package directory")
    parser.add_argument("--consumer", type=Path, required=True, action="append")
    args = parser.parse_args()
    lib = args.library.resolve()
    consumers = [p.resolve() for p in args.consumer]
    if not lib.name.isidentifier() or not all(p.is_dir() for p in [lib, *consumers]):
        parser.error("supply a Python package directory and existing consumer trees")
    result = {
        "library": str(lib),
        "consumers": [str(p) for p in consumers],
        "internal_imports": [],
        "consumer_imports": [],
        "calls": [],
        "gaps": [],
        "scope": (
            "Static imports and candidate calls. Check local shadowing, dynamic "
            "dispatch and consumers outside these roots."
        ),
    }
    exports, definitions = {}, set()
    for file in sources(lib):
        parts = list(file.relative_to(lib.parent).with_suffix("").parts)
        is_init = parts[-1] == "__init__"
        module = ".".join(parts[:-1] if is_init else parts)
        package = module if is_init else module.rpartition(".")[0]
        bindings, declarations = inspect_file(file, module, package, lib.name, result)
        exports.update(bindings)
        definitions.update(declarations)
    for file in sorted({p for folder in consumers for p in sources(folder)}):
        if lib not in file.parents:
            inspect_file(file, "", "", lib.name, result)
    for kind in ("internal_imports", "consumer_imports", "calls"):
        for row in result[kind]:
            row["owner"] = owner(row["requested"], exports, definitions)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
