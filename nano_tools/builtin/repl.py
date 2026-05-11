"""
Persistent Python REPL — state (variables, imports, functions) survives between calls.
Each ToolKit instance has its own isolated namespace.
"""
from __future__ import annotations
import io
import sys
import traceback
from contextlib import redirect_stdout, redirect_stderr
from nano_tools.decorator import tool

# Global persistent namespace — shared within one process session
_REPL_NS: dict = {"__builtins__": __builtins__}


def _run_in_ns(code: str, ns: dict) -> str:
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    try:
        with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
            exec(compile(code, "<repl>", "exec"), ns)  # noqa: S102
        out = stdout_buf.getvalue().strip()
        err = stderr_buf.getvalue().strip()
        result = []
        if out:
            result.append(out)
        if err:
            result.append(f"STDERR:\n{err}")
        return "\n".join(result) or "(executed, no output)"
    except Exception:
        return f"Error:\n{traceback.format_exc()}"


@tool
def python_repl(code: str) -> str:
    """Execute Python code in a persistent REPL. Variables and imports survive between calls.
    code: Python code to execute. Variables defined here are available in future calls.
    """
    return _run_in_ns(code, _REPL_NS)


@tool
def repl_vars() -> str:
    """List all variables currently defined in the persistent Python REPL."""
    skip = {"__builtins__", "__doc__", "__name__", "__package__", "__spec__", "__loader__"}
    items = {k: v for k, v in _REPL_NS.items() if k not in skip}
    if not items:
        return "(no variables defined yet)"
    lines = []
    for k, v in items.items():
        type_name = type(v).__name__
        try:
            preview = repr(v)[:80]
        except Exception:
            preview = "<unprintable>"
        lines.append(f"  {k} ({type_name}) = {preview}")
    return "\n".join(lines)


@tool
def repl_reset() -> str:
    """Clear all variables in the persistent Python REPL and start fresh."""
    global _REPL_NS
    _REPL_NS.clear()
    _REPL_NS["__builtins__"] = __builtins__
    return "REPL state cleared"
