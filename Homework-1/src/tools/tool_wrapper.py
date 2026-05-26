# ToolWrapper.call() + ToolWrapper.catalog_gemini() for Gemini
from .registry import TOOL_REGISTRY


class ToolWrapper:
    @staticmethod
    def call(name: str, args: dict) -> str:
        # 1. Lookup in registry
        if name not in TOOL_REGISTRY:
            return f"Error: tool '{name}' does not exist."

        tool = TOOL_REGISTRY[name]

        # 2. Validate — Pydantic validates types and constraints
        try:
            params = tool["params_model"](**args)
        except Exception as e:
            return f"Validation error for '{name}': {e}"

        # 3. Execute + 4. Return
        try:
            return str(tool["func"](params))
        except Exception as e:
            return f"Execution error for '{name}': {e}"

    @staticmethod
    def catalog_gemini() -> list[dict]:
        # Iterate registry → JSON Schema per tool (Gemini format)
        return [
            {
                "name": name,
                "description": tool["description"],
                "parameters": tool["params_model"].model_json_schema(),
            }
            for name, tool in TOOL_REGISTRY.items()
        ]
