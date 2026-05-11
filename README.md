<div align="center">

<img src="banner/nano-tools-banner.png" alt="nano-tools" width="800"/>

<br/>

**LLM tool framework for AI agents — 31 built-in tools, `@tool` decorator, persistent REPL, vision, memory. Built for nano-eco.**

[![Python](https://img.shields.io/badge/python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-22c55e.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-6366f1.svg)]()
[![Windows](https://img.shields.io/badge/windows-first-0078D4.svg?logo=windows&logoColor=white)]()
[![Tools](https://img.shields.io/badge/built--in%20tools-31-ff6b35.svg)]()

</div>

---

## The Problem

AI agents that can only chat are useless in production. They need to read files, run code, search the web, analyze images, remember context, query databases, and commit to git. Existing frameworks (LangChain, pydantic-ai) ship 100+ dependencies, require complex setup, lock you to one provider, and break on Windows.

**nano-tools fixes all of it — one `@tool` decorator, 31 ready-to-use tools, works with any LLM.**

---

## What Makes It Different

| Problem with others | nano-tools solution |
|---|---|
| Complex tool definition — classes, schemas, decorators across 3 files | **One `@tool` decorator** — schema auto-generated from type hints + docstring |
| Framework lock-in — tools only work with LangChain or pydantic-ai | **Provider-agnostic** — Anthropic + OpenAI format, works with any SDK |
| No tool-call loop — manage back-and-forth yourself | **Built-in loop** — `kit.run_loop()` handles multi-step tool calls automatically |
| No built-in tools — build everything from scratch | **31 ready tools** — files, code, REPL, web, vision, memory, git, docs, SQL |
| Stateless code execution — variables lost between calls | **Persistent REPL** — `python_repl` keeps state across the entire session |
| No memory between agent runs | **Memory tools** — standalone dict or nano-memory backend, semantic search |
| No vision support | **Image analysis** — Claude + GPT-4o, auto-routes through nano-proxy |
| No integration with LLM proxy | **nano-proxy integration** — 1 env var routes everything |
| Windows support broken | **Windows-first** — tested on PowerShell, no POSIX assumptions |

---

## Quick Start

```bash
# Install
pip install git+https://github.com/ghanibot/nano-tools.git

# With all optional deps
pip install "git+https://github.com/ghanibot/nano-tools.git#egg=nano-tools[all]"

# List all 31 built-in tools
nano-tools list

# Run a tool directly
nano-tools run calculator '{"expression": "sqrt(144) * 7"}'
nano-tools run current_datetime '{}'

# Ask LLM with tools
nano-tools ask "Read README.md and summarize it" --tools file
nano-tools ask "What is 15% of 3200?" --tools util
nano-tools ask "Show git log for current directory" --tools git
```

---

## `@tool` Decorator

Convert any Python function into an LLM-callable tool. Schema auto-generated — no manual JSON.

```python
from nano_tools import tool, ToolKit

@tool
def get_stock_price(ticker: str) -> str:
    """Get current stock price for a ticker symbol.
    ticker: Stock ticker e.g. AAPL, TSLA, MSFT
    """
    return f"{ticker}: $182.50"

@tool
def send_notification(channel: str, message: str) -> str:
    """Send a notification to a Slack channel.
    channel: Slack channel name e.g. #alerts
    message: Message text to send
    """
    return f"Sent to {channel}: {message}"

kit = ToolKit([get_stock_price, send_notification])

# Run with full tool-call loop — handles multi-step automatically
result = kit.run_loop(
    "Check AAPL price and send it to #alerts",
    model="claude-haiku-4-5-20251001",
)
print(result)
```

---

## All 31 Built-in Tools

### 📁 File Tools
```python
from nano_tools.builtin import FILE_TOOLS
```
| Tool | What it does |
|---|---|
| `read_file(path)` | Read file, truncates at 16k chars |
| `write_file(path, content)` | Write file, auto-creates parent dirs |
| `list_files(directory)` | List files + sizes in directory |
| `append_file(path, content)` | Append to existing file |

### 💻 Code Tools
```python
from nano_tools.builtin import CODE_TOOLS
```
| Tool | What it does |
|---|---|
| `run_python(code)` | Execute Python in subprocess, isolated, 30s timeout |
| `run_shell(command)` | Run shell command, 30s timeout |

### 🔁 REPL Tools — Persistent State
```python
from nano_tools.builtin import REPL_TOOLS
```
| Tool | What it does |
|---|---|
| `python_repl(code)` | **Persistent** Python REPL — variables survive between calls |
| `repl_vars()` | List all variables in current REPL session |
| `repl_reset()` | Clear REPL state, start fresh |

```python
# Variables persist across calls within one session:
kit.run_loop("Define x=100 and y=[1,2,3] using python_repl")
kit.run_loop("Now print x + sum(y) using python_repl")  # → 106
```

### 🌐 Web Tools
```python
from nano_tools.builtin import WEB_TOOLS
```
| Tool | What it does |
|---|---|
| `http_get(url)` | Fetch URL, return first 8k chars |
| `web_search(query)` | DuckDuckGo search, return top 5 results |
| `http_post(url, body)` | POST request with JSON body |

### 🔧 Utility Tools
```python
from nano_tools.builtin import UTIL_TOOLS
```
| Tool | What it does |
|---|---|
| `calculator(expression)` | Safe math — `sqrt`, `sin`, `pow`, `log` |
| `parse_json(text)` | Parse + pretty-print JSON |
| `current_datetime()` | Return current date and time |

### 📄 Document Tools
```python
from nano_tools.builtin import DOC_TOOLS
# pip install nano-tools[docs]
```
| Tool | What it does |
|---|---|
| `read_pdf(path)` | Extract text from PDF, page by page |
| `query_sqlite(db_path, sql)` | Run SQL query, return JSON results |
| `list_sqlite_tables(db_path)` | Show all tables + columns in SQLite DB |

### 🔀 Git Tools
```python
from nano_tools.builtin import GIT_TOOLS
```
| Tool | What it does |
|---|---|
| `git_status(repo_path)` | Show working tree status |
| `git_diff(repo_path)` | Show unstaged changes |
| `git_log(repo_path)` | Show last 10 commits |
| `git_commit(repo_path, message)` | Stage all + commit |
| `git_read_file(repo_path, file_path, ref)` | Read file at specific git ref |

### 👁️ Vision Tools
```python
from nano_tools.builtin import VISION_TOOLS
```
| Tool | What it does |
|---|---|
| `analyze_image(image_path, question)` | Analyze image with Claude (claude-opus-4-7) |
| `analyze_image_openai(image_path, question)` | Analyze image with GPT-4o |
| `read_image_base64(image_path)` | Return base64 encoding of image |

Vision tools auto-route through nano-proxy if `NANO_PROXY_URL` is set.

### 🧠 Memory Tools
```python
from nano_tools.builtin import MEMORY_TOOLS
```
| Tool | What it does |
|---|---|
| `remember(key, value)` | Store a fact for this session |
| `recall(key)` | Retrieve stored fact by key |
| `recall_search(query)` | Semantic search across all memories |
| `forget(key)` | Remove a stored memory |
| `list_memories()` | List all stored memory keys |

**With nano-memory backend** (persists across sessions):
```bash
export NANO_MEMORY_NS=my-agent   # set namespace → auto-uses nano-memory
```
```python
# Now remember() persists to SQLite + vector index
# recall_search() uses semantic similarity, not just string match
```

---

## Door 1 — Direct Python (Standalone)

```python
from nano_tools import tool, ToolKit
from nano_tools.builtin import FILE_TOOLS, REPL_TOOLS, MEMORY_TOOLS

@tool
def lookup_customer(customer_id: str) -> str:
    """Look up customer by ID.
    customer_id: Customer identifier
    """
    return f"Customer {customer_id}: name=Alice, plan=Pro, since=2024"

kit = ToolKit(FILE_TOOLS + REPL_TOOLS + MEMORY_TOOLS + [lookup_customer])

result = kit.run_loop(
    "Look up customer C-1042, remember their plan, then write a summary to customer_report.md",
    model="claude-haiku-4-5-20251001",
)
print(result)
```

---

## Door 2 — Via nano-proxy (nano-eco Integrated)

Set one env var — all LLM calls route through nano-proxy automatically:

```bash
export NANO_PROXY_URL=http://localhost:8766   # nano-cache → nano-proxy
export NANO_MEMORY_NS=my-agent               # persist memories to nano-memory
```

```python
import os
from nano_tools.integrations import toolkit_with_proxy
from nano_tools.builtin import ALL_TOOLS

kit = toolkit_with_proxy(ALL_TOOLS)

# LLM calls: nano-cache → nano-proxy → best available provider
# Memory: persisted to nano-memory SQLite store
# Cost: tracked in nano-proxy cost report
result = kit.run_loop("Analyze the repo, write a summary, commit it")
```

Or use `run_loop_openai` to target Groq, Mistral, Ollama:
```python
result = kit.run_loop_openai(
    "Search the web and summarize AI news",
    model="llama-3.1-70b-versatile",
    base_url="http://localhost:8765/groq/v1",
)
```

---

## Integration with nano-orchestrator

```python
from nano_tools import ToolKit
from nano_tools.builtin import FILE_TOOLS, WEB_TOOLS, GIT_TOOLS
from nano_tools.integrations import toolkit_to_agent_context, export_tool_schemas

kit = ToolKit(FILE_TOOLS + WEB_TOOLS + GIT_TOOLS)

# System prompt for agent
system = toolkit_to_agent_context(kit)

# Export schemas → load in orchestrator config
export_tool_schemas(kit, "tool_schemas.json")
```

```yaml
# nano-orchestrator pipeline.yaml
agents:
  - id: dev-agent
    type: claude-code
    task: |
      Research best practices for the feature, implement it,
      write tests, and commit the result.
      Tools available: read_file, write_file, web_search, git_commit
```

---

## Architecture

```
nano_tools/
├── @tool decorator      — type hints + docstring → JSON schema (Anthropic + OpenAI format)
├── ToolKit              — tool collection + multi-step tool-call loop
│   ├── run_loop()           — Anthropic format (Claude)
│   └── run_loop_openai()    — OpenAI format (GPT, Groq, Mistral, Ollama, nano-proxy)
├── builtin/ (31 tools)
│   ├── files.py         — read_file, write_file, list_files, append_file
│   ├── code.py          — run_python, run_shell
│   ├── repl.py          — python_repl (persistent), repl_vars, repl_reset
│   ├── web.py           — http_get, web_search, http_post
│   ├── utils.py         — calculator, parse_json, current_datetime
│   ├── docs.py          — read_pdf, query_sqlite, list_sqlite_tables
│   ├── git_tools.py     — git_status, git_diff, git_log, git_commit, git_read_file
│   ├── vision.py        — analyze_image (Claude), analyze_image_openai (GPT-4o)
│   └── memory.py        — remember/recall/search/forget + nano-memory backend
└── integrations/
    ├── nano_proxy.py        — ProxyToolKit: route via nano-proxy
    └── nano_orchestrator.py — export context + schemas for orchestrator agents
```

---

## Tool Groups

```python
from nano_tools.builtin import (
    ALL_TOOLS,      # all 31
    SAFE_TOOLS,     # read-only, no code execution
    FILE_TOOLS,     # read_file, write_file, list_files, append_file
    CODE_TOOLS,     # run_python, run_shell
    REPL_TOOLS,     # python_repl, repl_vars, repl_reset
    WEB_TOOLS,      # http_get, web_search, http_post
    UTIL_TOOLS,     # calculator, parse_json, current_datetime
    DOC_TOOLS,      # read_pdf, query_sqlite, list_sqlite_tables
    GIT_TOOLS,      # git_status, git_diff, git_log, git_commit, git_read_file
    VISION_TOOLS,   # analyze_image, analyze_image_openai, read_image_base64
    MEMORY_TOOLS,   # remember, recall, recall_search, forget, list_memories
)
```

---

## nano-eco Ecosystem Position

```
nano-orchestrator  — coordinate multi-agent pipelines
       │
       ├── nano-tools  ← you are here (31 tools for any agent)
       │   ├── memory tools  ──────────────────────────────┐
       │   └── vision tools  ──────────────────────────────┤
       │                                                    ▼
       ├── nano-memory        — persistent memory (nano-memory backend)
       │
       └── all LLM calls
           └── nano-cache → nano-proxy → Anthropic/OpenAI/Groq/Gemini/Ollama/Mistral
```

---

## CLI Reference

```bash
nano-tools list                                  # List all 31 tools
nano-tools run <tool> '<json>'                   # Run tool directly
nano-tools schema <tool> --format openai         # Print JSON schema
nano-tools ask "<prompt>" --tools all            # all|safe|file|code|repl|web|util|doc|git|vision|memory
nano-tools ask "<prompt>" --proxy http://...     # Route through nano-proxy
nano-tools ask "<prompt>" --model gpt-4o-mini    # Custom model
```

---

## Environment Variables

```bash
ANTHROPIC_API_KEY=sk-ant-...          # for Claude tools
OPENAI_API_KEY=sk-...                 # for OpenAI vision + run_loop_openai
NANO_PROXY_URL=http://localhost:8765  # route all LLM calls through nano-proxy
NANO_MEMORY_NS=my-agent              # persist memory tools to nano-memory
```

---

## Install by Feature

```bash
pip install nano-tools                  # core (Anthropic, file, code, git, memory, repl)
pip install nano-tools[search]          # + web_search, http_get/post
pip install nano-tools[docs]            # + read_pdf
pip install nano-tools[openai]          # + run_loop_openai, analyze_image_openai
pip install nano-tools[all]             # everything
```

---

## Contributing

```bash
git clone https://github.com/ghanibot/nano-tools
cd nano-tools
pip install -e ".[dev,all]"
pytest
```

---

## License

MIT — see [LICENSE](LICENSE)
