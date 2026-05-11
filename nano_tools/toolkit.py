"""
ToolKit — collection of tools + LLM tool-call loop handler.
Supports Anthropic and OpenAI formats.
"""
from __future__ import annotations
import json
from typing import Any
from nano_tools.decorator import Tool


class ToolKit:
    def __init__(self, tools: list[Tool]) -> None:
        self._tools: dict[str, Tool] = {t.name: t for t in tools}

    def add(self, t: Tool) -> None:
        self._tools[t.name] = t

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list(self) -> list[Tool]:
        return list(self._tools.values())

    # ── Schema exports ────────────────────────────────────────────────────────

    def anthropic_tools(self) -> list[dict]:
        """Return tools in Anthropic API format."""
        return [t.schema for t in self._tools.values()]

    def openai_tools(self) -> list[dict]:
        """Return tools in OpenAI API format."""
        return [t.openai_schema for t in self._tools.values()]

    # ── Tool execution ────────────────────────────────────────────────────────

    def execute(self, name: str, inputs: dict | str) -> str:
        t = self._tools.get(name)
        if not t:
            return f"Error: tool '{name}' not found. Available: {list(self._tools)}"
        return t.run(inputs)

    # ── Anthropic tool-call loop ──────────────────────────────────────────────

    def run_loop(
        self,
        prompt: str,
        model: str = "claude-haiku-4-5-20251001",
        system: str = "",
        max_iterations: int = 10,
        base_url: str | None = None,
    ) -> str:
        """
        Run a full Anthropic tool-call loop until the model stops calling tools.
        Returns the final text response.
        Supports nano-proxy via base_url.
        """
        import anthropic

        kwargs: dict = {}
        if base_url:
            kwargs["base_url"] = base_url
        client = anthropic.Anthropic(**kwargs)

        messages: list[dict] = [{"role": "user", "content": prompt}]
        tools = self.anthropic_tools()

        for _ in range(max_iterations):
            req: dict = dict(
                model=model,
                max_tokens=4096,
                tools=tools,
                messages=messages,
            )
            if system:
                req["system"] = system

            resp = client.messages.create(**req)

            if resp.stop_reason == "end_turn":
                for block in resp.content:
                    if hasattr(block, "text"):
                        return block.text
                return ""

            if resp.stop_reason == "tool_use":
                # Append assistant message with tool use blocks
                messages.append({"role": "assistant", "content": resp.content})

                # Execute each tool call
                tool_results = []
                for block in resp.content:
                    if block.type == "tool_use":
                        result = self.execute(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        })

                messages.append({"role": "user", "content": tool_results})
                continue

            # Fallback: extract text
            for block in resp.content:
                if hasattr(block, "text"):
                    return block.text
            return ""

        return "Max iterations reached"

    # ── OpenAI tool-call loop ─────────────────────────────────────────────────

    def run_loop_openai(
        self,
        prompt: str,
        model: str = "gpt-4o-mini",
        system: str = "",
        max_iterations: int = 10,
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> str:
        """
        Run a full OpenAI tool-call loop.
        Compatible with any OpenAI-format provider (Groq, Mistral, Ollama, nano-proxy).
        """
        try:
            import openai
        except ImportError:
            raise ImportError("openai package required. Install: pip install nano-tools[openai]")

        kwargs: dict = {}
        if base_url:
            kwargs["base_url"] = base_url
        if api_key:
            kwargs["api_key"] = api_key
        client = openai.OpenAI(**kwargs)

        messages: list[dict] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        tools = self.openai_tools()

        for _ in range(max_iterations):
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )
            msg = resp.choices[0].message

            if not msg.tool_calls:
                return msg.content or ""

            messages.append(msg)

            for tc in msg.tool_calls:
                try:
                    inputs = json.loads(tc.function.arguments)
                except Exception:
                    inputs = {}
                result = self.execute(tc.function.name, inputs)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })

        return "Max iterations reached"

    def __repr__(self) -> str:
        names = list(self._tools)
        return f"ToolKit(tools={names})"
