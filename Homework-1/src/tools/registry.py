# TOOL_REGISTRY + @register_tool
import inspect
from pydantic import BaseModel
from functools import wraps

TOOL_REGISTRY = {}
def register_tool(func):
    sig = inspect.signature(func)
    params = list(sig.parameters.values())

    # Validation 1: single parameter of BaseModel type required
    if len(params) != 1 or not issubclass(
        params[0].annotation, BaseModel
    ):
        raise TypeError(
            f"{func.__name__}: single parameter of BaseModel type required"
        )

    # Validation 2: docstring required (becomes description for LLM)
    docstring = (func.__doc__ or "").strip()
    if not docstring:
        raise ValueError(
            f"{func.__name__}: docstring required — becomes "
            f"visible description for LLM."
        )
    if len(docstring) < 15:
        raise ValueError(
            f"{func.__name__}: docstring too short ({len(docstring)} "
            f"characters). LLM needs minimum 15 to decide."
        )

    TOOL_REGISTRY[func.__name__] = {
        "func": func,
        "params_model": params[0].annotation,
        "description": docstring,  # ← this is what LLM receives
    }
    return func
