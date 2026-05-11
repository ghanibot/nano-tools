"""
nano-proxy integration — route all LLM calls through nano-proxy.
"""
from __future__ import annotations
import os
from nano_tools.toolkit import ToolKit


def toolkit_with_proxy(
    tools: list,
    proxy_url: str | None = None,
) -> "ProxyToolKit":
    proxy_url = proxy_url or os.environ.get("NANO_PROXY_URL", "http://localhost:8765")
    return ProxyToolKit(tools, proxy_url=proxy_url)


class ProxyToolKit(ToolKit):
    """ToolKit that routes LLM calls through nano-proxy."""

    def __init__(self, tools: list, proxy_url: str = "http://localhost:8765") -> None:
        super().__init__(tools)
        self.proxy_url = proxy_url

    def run_loop(self, prompt: str, model: str = "claude-haiku-4-5-20251001", system: str = "", max_iterations: int = 10, **kwargs) -> str:
        return super().run_loop(
            prompt=prompt,
            model=model,
            system=system,
            max_iterations=max_iterations,
            base_url=f"{self.proxy_url}/anthropic",
        )

    def run_loop_openai(self, prompt: str, model: str = "gpt-4o-mini", system: str = "", max_iterations: int = 10, **kwargs) -> str:
        return super().run_loop_openai(
            prompt=prompt,
            model=model,
            system=system,
            max_iterations=max_iterations,
            base_url=f"{self.proxy_url}/openai/v1",
        )
