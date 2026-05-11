"""
nano-orchestrator integration — export ToolKit as agent task config.
"""
from __future__ import annotations
import json
from nano_tools.toolkit import ToolKit


def toolkit_to_agent_context(kit: ToolKit) -> str:
    """
    Generate a system prompt fragment listing available tools.
    Inject into nano-orchestrator agent task to give it tool awareness.
    """
    tools = kit.list()
    lines = ["You have access to the following tools:\n"]
    for t in tools:
        schema = t.schema
        params = list(schema["input_schema"].get("properties", {}).keys())
        lines.append(f"- {t.name}({', '.join(params)}): {schema['description']}")
    lines.append("\nCall tools using the standard tool_use format.")
    return "\n".join(lines)


def export_tool_schemas(kit: ToolKit, path: str) -> None:
    """Export all tool schemas to JSON — usable by any orchestrator."""
    schemas = {
        "anthropic": kit.anthropic_tools(),
        "openai": kit.openai_tools(),
    }
    import json
    from pathlib import Path
    Path(path).write_text(json.dumps(schemas, indent=2), encoding="utf-8")
