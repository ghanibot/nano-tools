import json
from nano_tools.decorator import tool


@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression safely and return the result.
    expression: Math expression e.g. '2 + 2', '100 * 0.15', 'sqrt(144)'
    """
    import math
    allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
    allowed.update({"abs": abs, "round": round, "int": int, "float": float})
    try:
        result = eval(expression, {"__builtins__": {}}, allowed)  # noqa: S307
        return str(result)
    except Exception as e:
        return f"Error evaluating '{expression}': {e}"


@tool
def parse_json(text: str) -> str:
    """Parse a JSON string and return formatted output.
    text: JSON string to parse
    """
    try:
        data = json.loads(text)
        return json.dumps(data, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"JSON parse error: {e}"


@tool
def current_datetime() -> str:
    """Return the current date and time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def http_post(url: str, body: str) -> str:
    """Send an HTTP POST request with a JSON body and return the response.
    url: Target URL
    body: JSON body as a string
    """
    try:
        import httpx
        resp = httpx.post(
            url,
            content=body,
            headers={"Content-Type": "application/json"},
            timeout=15,
            follow_redirects=True,
        )
        return resp.text[:8000]
    except ImportError:
        return "Error: httpx not installed. Run: pip install nano-tools[search]"
    except Exception as e:
        return f"Error: {e}"
