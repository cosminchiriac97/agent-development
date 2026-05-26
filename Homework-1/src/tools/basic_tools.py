#calculator, get_datetime, web_search 
import re
import json
import os
from datetime import datetime
from .registry import register_tool
from .params_models import CalculatorParams, WebSearchParams, EmptyParams


# ============== CALCULATOR ==============
@register_tool
def calculator(params: CalculatorParams) -> str:
    """Evaluates any mathematical expression. Supports +, -, *, /, **, %, and math functions (sin, cos, sqrt, etc.) Returns calculation result or error message."""
    try:
        expression = params.expression.strip()
        
        # Validation: only allowed characters
        allowed = set("0123456789.+-*/%() ")
        if not all(c in allowed or c.isalpha() for c in expression):
            return json.dumps({"error": "Expression contains disallowed characters"})
        
        # Safe evaluation with limited namespace
        namespace = {
            "sin": __import__("math").sin,
            "cos": __import__("math").cos,
            "tan": __import__("math").tan,
            "sqrt": __import__("math").sqrt,
            "log": __import__("math").log,
            "exp": __import__("math").exp,
            "pi": __import__("math").pi,
            "e": __import__("math").e,
            "__builtins__": {},
        }
        
        result = eval(expression, namespace)
        
        # Round to 10 decimals to avoid precision issues
        if isinstance(result, float):
            result = round(result, 10)
        
        return str(result)
    
    except ZeroDivisionError:
        return json.dumps({"error": "Division by zero"})
    except ValueError as e:
        return json.dumps({"error": f"Invalid mathematical value - {e}"})
    except Exception as e:
        return json.dumps({"error": f"Invalid expression - {e}"})


# ============== GET_DATETIME ==============
@register_tool
def get_datetime(params: EmptyParams) -> str:
    """Returns current date and time in ISO 8601 format."""
    return datetime.now().isoformat()


# ============== WEB_SEARCH ==============
@register_tool
def web_search(params: WebSearchParams) -> str:
    """Searches the web and returns relevant results.
    
    Simulates a web search (in production would use Google Search API).
    """
    # Simulation - in production would use Google Search API or similar
    results = [
        f"Result {i+1}: Information about '{params.query}'"
        for i in range(min(params.max_results, 5))
    ]
    return "\n".join(results)
