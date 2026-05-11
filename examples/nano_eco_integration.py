"""
nano-eco integration example.
Shows how nano-tools + nano-proxy + nano-orchestrator work together.
"""
import os
from nano_tools import tool, ToolKit
from nano_tools.builtin import FILE_TOOLS, WEB_TOOLS
from nano_tools.integrations import toolkit_with_proxy, toolkit_to_agent_context

# ── Custom tool for this agent ────────────────────────────────────────────────

@tool
def save_research(filename: str, content: str) -> str:
    """Save research findings to a markdown file.
    filename: Output filename e.g. research.md
    content: Research content to save
    """
    from pathlib import Path
    Path(filename).write_text(content, encoding="utf-8")
    return f"Saved to {filename}"


# ── Door 1: Direct Python (standalone) ───────────────────────────────────────

def run_direct():
    kit = ToolKit(FILE_TOOLS + WEB_TOOLS + [save_research])
    result = kit.run_loop(
        "Search for information about Python async programming and save a summary to research.md",
        model="claude-haiku-4-5-20251001",
    )
    print(result)


# ── Door 2: Via nano-proxy (nano-eco integrated) ──────────────────────────────

def run_via_proxy():
    proxy_url = os.environ.get("NANO_PROXY_URL", "http://localhost:8765")
    kit = toolkit_with_proxy(
        tools=FILE_TOOLS + WEB_TOOLS + [save_research],
        proxy_url=proxy_url,
    )
    # All LLM calls route through nano-proxy → fallback, cost tracking, caching
    result = kit.run_loop(
        "Search for information about Python async programming and save a summary to research.md",
        model="claude-haiku-4-5-20251001",
    )
    print(result)


# ── Export for nano-orchestrator agent ───────────────────────────────────────

def export_for_orchestrator():
    kit = ToolKit(FILE_TOOLS + [save_research])
    # Generate system prompt with tool descriptions
    context = toolkit_to_agent_context(kit)
    print("Inject this into your nano-orchestrator agent task:\n")
    print(context)
    # Export schemas to JSON
    from nano_tools.integrations import export_tool_schemas
    export_tool_schemas(kit, "tool_schemas.json")
    print("\nTool schemas saved to tool_schemas.json")


if __name__ == "__main__":
    print("=== Door 1: Direct ===")
    # run_direct()  # uncomment with ANTHROPIC_API_KEY

    print("\n=== Door 2: Via nano-proxy ===")
    # run_via_proxy()  # uncomment with nano-proxy running

    print("\n=== Export for nano-orchestrator ===")
    export_for_orchestrator()
