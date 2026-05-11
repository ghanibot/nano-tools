"""
Memory tools — remember/recall facts across tool calls.

Standalone: in-process dict (no deps).
nano-memory backend: if nano-memory installed + NANO_MEMORY_NS set, persist across sessions.
"""
from __future__ import annotations
import os
from nano_tools.decorator import tool

# In-process store — survives within one agent session
_STORE: dict[str, str] = {}


def _get_nano_memory():
    """Return nano_memory.Memory instance if available, else None."""
    ns = os.environ.get("NANO_MEMORY_NS", "")
    if not ns:
        return None
    try:
        from nano_memory import Memory
        return Memory(namespace=ns)
    except ImportError:
        return None


@tool
def remember(key: str, value: str) -> str:
    """Store a fact or piece of information for later recall.
    key: Short label for this memory e.g. 'user_name', 'project_goal'
    value: Content to remember
    """
    _STORE[key] = value

    mem = _get_nano_memory()
    if mem:
        mem.save(f"{key}: {value}", type="fact")
        return f"Remembered '{key}' (persisted to nano-memory)"
    return f"Remembered '{key}'"


@tool
def recall(key: str) -> str:
    """Recall a previously stored fact by key.
    key: Label used when storing the memory
    """
    # Check in-process store first
    if key in _STORE:
        return _STORE[key]

    # Fallback: search nano-memory
    mem = _get_nano_memory()
    if mem:
        results = mem.search(key, top_k=3)
        if results:
            return "\n".join(f"[{r.score:.2f}] {r.text}" for r in results)
        return f"No memory found for '{key}'"

    return f"No memory found for '{key}'. Use remember() first."


@tool
def recall_search(query: str) -> str:
    """Search all memories semantically for relevant information.
    query: Natural language search query
    """
    mem = _get_nano_memory()
    if mem:
        results = mem.search(query, top_k=5)
        if results:
            return "\n".join(f"[{r.score:.2f}] {r.text}" for r in results)
        return "No relevant memories found."

    # Fallback: substring search in local store
    matches = [(k, v) for k, v in _STORE.items() if query.lower() in k.lower() or query.lower() in v.lower()]
    if matches:
        return "\n".join(f"{k}: {v}" for k, v in matches)
    return "No matching memories found."


@tool
def forget(key: str) -> str:
    """Remove a stored memory by key.
    key: Label of memory to remove
    """
    if key in _STORE:
        del _STORE[key]
        return f"Forgot '{key}'"
    return f"No memory with key '{key}' found"


@tool
def list_memories() -> str:
    """List all currently stored memory keys."""
    if not _STORE:
        return "(no memories stored in this session)"
    return "\n".join(f"- {k}: {v[:80]}{'...' if len(v)>80 else ''}" for k, v in _STORE.items())
