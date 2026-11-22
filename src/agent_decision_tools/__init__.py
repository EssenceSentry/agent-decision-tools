"""Decision tools for bounded research and engineering work."""

from importlib.metadata import PackageNotFoundError, version

from .core import evaluate, schema, tools

try:
    __version__ = version("agent-decision-tools")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"

__all__ = ["__version__", "evaluate", "schema", "tools"]
