import subprocess
import sys
import tempfile
from pathlib import Path
from nano_tools.decorator import tool


@tool
def run_python(code: str) -> str:
    """Execute Python code in a subprocess and return stdout + stderr.
    code: Python code to execute
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        tmp = f.name
    try:
        result = subprocess.run(
            [sys.executable, tmp],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout.strip()
        errors = result.stderr.strip()
        if errors:
            return f"{output}\nSTDERR:\n{errors}" if output else f"STDERR:\n{errors}"
        return output or "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: code execution timed out (30s)"
    except Exception as e:
        return f"Error: {e}"
    finally:
        Path(tmp).unlink(missing_ok=True)


@tool
def run_shell(command: str) -> str:
    """Execute a shell command and return output. Use with caution.
    command: Shell command to run
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout.strip()
        errors = result.stderr.strip()
        if errors and result.returncode != 0:
            return f"{output}\nSTDERR:\n{errors}" if output else f"STDERR:\n{errors}"
        return output or "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: command timed out (30s)"
    except Exception as e:
        return f"Error: {e}"
