from __future__ import annotations
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich import box

app = typer.Typer(name="nano-tools", add_completion=False)
console = Console(force_terminal=True)


@app.command()
def list():
    """List all built-in tools."""
    from nano_tools.builtin import ALL_TOOLS
    table = Table(box=box.SIMPLE, show_header=True, header_style="bold")
    table.add_column("Tool")
    table.add_column("Description")
    table.add_column("Parameters")
    for t in ALL_TOOLS:
        params = list(t.schema["input_schema"].get("properties", {}).keys())
        table.add_row(t.name, t.schema["description"], ", ".join(params) or "(none)")
    console.print(f"\n[bold]nano-tools[/bold] — {len(ALL_TOOLS)} built-in tools\n")
    console.print(table)


@app.command()
def run(
    tool_name: str = typer.Argument(..., help="Tool name to run"),
    inputs: str = typer.Argument("{}", help="JSON inputs e.g. '{\"path\": \"file.txt\"}'"),
):
    """Run a single built-in tool directly from CLI."""
    from nano_tools.builtin import ALL_TOOLS
    import json
    tool_map = {t.name: t for t in ALL_TOOLS}
    if tool_name not in tool_map:
        console.print(f"[red]Tool '{tool_name}' not found.[/red] Run [bold]nano-tools list[/bold] to see available tools.")
        raise typer.Exit(1)
    try:
        parsed = json.loads(inputs)
    except Exception:
        console.print(f"[red]Invalid JSON inputs: {inputs}[/red]")
        raise typer.Exit(1)
    result = tool_map[tool_name].run(parsed)
    console.print(result)


@app.command()
def schema(
    tool_name: str = typer.Argument(..., help="Tool name"),
    fmt: str = typer.Option("anthropic", "--format", "-f", help="anthropic | openai"),
):
    """Print JSON schema for a tool."""
    from nano_tools.builtin import ALL_TOOLS
    import json
    tool_map = {t.name: t for t in ALL_TOOLS}
    if tool_name not in tool_map:
        console.print(f"[red]Tool '{tool_name}' not found.[/red]")
        raise typer.Exit(1)
    t = tool_map[tool_name]
    s = t.schema if fmt == "anthropic" else t.openai_schema
    console.print(json.dumps(s, indent=2))


@app.command()
def ask(
    prompt: str = typer.Argument(..., help="Prompt to send to LLM with tools"),
    model: str = typer.Option("claude-haiku-4-5-20251001", "--model", "-m"),
    proxy: Optional[str] = typer.Option(None, "--proxy", help="nano-proxy URL e.g. http://localhost:8765"),
    tools: str = typer.Option("safe", "--tools", "-t", help="all | safe | file | code | web | util"),
):
    """Run a prompt with tools via LLM (tool-call loop)."""
    from nano_tools.builtin import (
        ALL_TOOLS, SAFE_TOOLS, FILE_TOOLS, CODE_TOOLS, WEB_TOOLS, UTIL_TOOLS,
        DOC_TOOLS, GIT_TOOLS, VISION_TOOLS, MEMORY_TOOLS, REPL_TOOLS,
    )
    from nano_tools.toolkit import ToolKit

    tool_sets = {
        "all": ALL_TOOLS, "safe": SAFE_TOOLS,
        "file": FILE_TOOLS, "code": CODE_TOOLS, "web": WEB_TOOLS,
        "util": UTIL_TOOLS, "doc": DOC_TOOLS, "git": GIT_TOOLS,
        "vision": VISION_TOOLS, "memory": MEMORY_TOOLS, "repl": REPL_TOOLS,
    }
    selected = tool_sets.get(tools, SAFE_TOOLS)
    kit = ToolKit(selected)

    base_url = None
    if proxy:
        base_url = f"{proxy.rstrip('/')}/anthropic"
    elif __import__("os").environ.get("NANO_PROXY_URL"):
        base_url = f"{__import__('os').environ['NANO_PROXY_URL'].rstrip('/')}/anthropic"

    console.print(f"\n[dim]Tools: {[t.name for t in selected]}[/dim]")
    console.print(f"[dim]Model: {model}  Proxy: {base_url or 'direct'}[/dim]\n")

    result = kit.run_loop(prompt, model=model, base_url=base_url)
    console.print(result)
