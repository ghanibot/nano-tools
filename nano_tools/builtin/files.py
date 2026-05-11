from pathlib import Path
from nano_tools.decorator import tool


@tool
def read_file(path: str) -> str:
    """Read and return the contents of a file.
    path: File path to read
    """
    try:
        content = Path(path).read_text(encoding="utf-8")
        if len(content) > 16000:
            return content[:16000] + f"\n\n[truncated — {len(content)} total chars]"
        return content
    except FileNotFoundError:
        return f"Error: file not found: {path}"
    except Exception as e:
        return f"Error reading {path}: {e}"


@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file, creating parent directories if needed.
    path: File path to write
    content: Text content to write
    """
    try:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Written {len(content)} chars to {path}"
    except Exception as e:
        return f"Error writing {path}: {e}"


@tool
def list_files(directory: str) -> str:
    """List files and directories in a given path.
    directory: Directory path to list
    """
    try:
        p = Path(directory)
        if not p.exists():
            return f"Error: path does not exist: {directory}"
        entries = sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name))
        lines = []
        for entry in entries[:100]:
            icon = "📄" if entry.is_file() else "📁"
            size = f"  ({entry.stat().st_size:,} bytes)" if entry.is_file() else ""
            lines.append(f"{icon} {entry.name}{size}")
        if len(list(p.iterdir())) > 100:
            lines.append("... (truncated at 100 entries)")
        return "\n".join(lines) if lines else "(empty directory)"
    except Exception as e:
        return f"Error listing {directory}: {e}"


@tool
def append_file(path: str, content: str) -> str:
    """Append content to an existing file (or create if not exists).
    path: File path to append to
    content: Text content to append
    """
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        return f"Appended {len(content)} chars to {path}"
    except Exception as e:
        return f"Error appending to {path}: {e}"
