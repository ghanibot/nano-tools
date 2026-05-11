"""
@tool decorator — wrap any Python function into an LLM-callable tool.
Auto-generates JSON schema from type hints + docstring.
"""
from __future__ import annotations
import inspect
import json
from functools import wraps
from typing import Any, Callable, get_type_hints


_TYPE_MAP = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
}


def _py_type_to_json(t: Any) -> str:
    return _TYPE_MAP.get(t, "string")


def _build_schema(fn: Callable) -> dict:
    sig = inspect.signature(fn)
    hints = get_type_hints(fn)
    doc = inspect.getdoc(fn) or ""

    # Parse param descriptions from docstring "param: description" lines
    param_docs: dict[str, str] = {}
    for line in doc.splitlines():
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            if key in sig.parameters:
                param_docs[key] = val.strip()

    properties: dict[str, dict] = {}
    required: list[str] = []

    for name, param in sig.parameters.items():
        if name == "self":
            continue
        ptype = hints.get(name, str)
        prop: dict = {"type": _py_type_to_json(ptype)}
        if name in param_docs:
            prop["description"] = param_docs[name]
        properties[name] = prop
        if param.default is inspect.Parameter.empty:
            required.append(name)

    # First line of docstring = tool description
    description = doc.split("\n")[0].strip() if doc else fn.__name__

    return {
        "name": fn.__name__,
        "description": description,
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
    }


def _build_openai_schema(fn: Callable) -> dict:
    schema = _build_schema(fn)
    return {
        "type": "function",
        "function": {
            "name": schema["name"],
            "description": schema["description"],
            "parameters": schema["input_schema"],
        },
    }


class Tool:
    def __init__(self, fn: Callable) -> None:
        self._fn = fn
        self.name: str = fn.__name__
        self.schema: dict = _build_schema(fn)
        self.openai_schema: dict = _build_openai_schema(fn)

    def __call__(self, **kwargs: Any) -> Any:
        return self._fn(**kwargs)

    def run(self, input: dict | str) -> str:
        if isinstance(input, str):
            try:
                input = json.loads(input)
            except Exception:
                input = {"input": input}
        try:
            result = self._fn(**input)
            return str(result)
        except Exception as e:
            return f"Error: {e}"

    def __repr__(self) -> str:
        return f"Tool(name={self.name!r})"


def tool(fn: Callable) -> Tool:
    """
    Decorator — convert a Python function into an LLM-callable Tool.

    Usage:
        @tool
        def search_web(query: str) -> str:
            \"\"\"Search the web for current information.\"\"\"
            ...
    """
    return Tool(fn)
