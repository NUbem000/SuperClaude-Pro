"""SuperClaude Pro - Professional framework extending Claude Code capabilities."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("superclaude-pro")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

__all__ = [
    "__version__",
    "core",
    "commands",
    "personas",
    "mcp",
    "orchestrator",
]

# Lazy imports to improve startup time
def __getattr__(name):
    if name == "core":
        from . import core
        return core
    elif name == "commands":
        from . import commands
        return commands
    elif name == "personas":
        from . import personas
        return personas
    elif name == "mcp":
        from . import mcp
        return mcp
    elif name == "orchestrator":
        from . import orchestrator
        return orchestrator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")