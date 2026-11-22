"""A common Python and JSON interface to decision calculations."""

from .decisions import BreakEven, Decision, Robust
from .evidence import Calibration, Interim, Panel
from .fermi import Fermi
from .models import Request
from .records import Revisit
from .scheduling import Schedule

_REGISTRY: dict[str, type[Request]] = {
    "fermi": Fermi,
    "decide": Decision,
    "robust": Robust,
    "breakeven": BreakEven,
    "interim": Interim,
    "panel": Panel,
    "calibrate": Calibration,
    "schedule": Schedule,
    "revisit": Revisit,
}


def _tool(name: str) -> type[Request]:
    try:
        return _REGISTRY[name]
    except KeyError as error:
        raise ValueError(
            f"Unknown tool {name!r}. Choose from: {', '.join(_REGISTRY)}"
        ) from error


def tools() -> dict[str, str]:
    """List operations and the questions they answer.

    Returns
    -------
    dict
        Operation names mapped to short descriptions.
    """
    return {
        name: (operation.__doc__ or "").strip() for name, operation in _REGISTRY.items()
    }


def schema(tool: str) -> dict[str, object]:
    """Describe the complete input object for a tool.

    Parameters
    ----------
    tool : str
        Registered operation name.

    Returns
    -------
    dict
        JSON Schema including defaults, bounds and required fields.
    """
    return _tool(tool).model_json_schema()


def evaluate(tool: str, payload: object) -> dict[str, object]:
    """Validate a request and return its decision metrics.

    Parameters
    ----------
    tool : str
        Registered operation name.
    payload : object
        Native dictionary or decoded JSON input for that operation.

    Returns
    -------
    dict
        Operation name, supplied evidence basis and calculation results.
    """
    request = _tool(tool).model_validate(payload)
    return {"tool": tool, "basis": request.basis, **request.calculate()}
