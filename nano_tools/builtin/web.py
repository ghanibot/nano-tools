from nano_tools.decorator import tool


@tool
def http_get(url: str) -> str:
    """Fetch content from a URL and return the response text.
    url: The URL to fetch
    """
    try:
        import httpx
    except ImportError:
        return "Error: httpx not installed. Run: pip install nano-tools[search]"
    try:
        resp = httpx.get(url, timeout=15, follow_redirects=True, headers={"User-Agent": "nano-tools/0.1"})
        return resp.text[:8000]
    except Exception as e:
        return f"Error fetching {url}: {e}"


@tool
def web_search(query: str) -> str:
    """Search DuckDuckGo and return top results as text.
    query: Search query string
    """
    try:
        import httpx
    except ImportError:
        return "Error: httpx not installed. Run: pip install nano-tools[search]"
    try:
        url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
        resp = httpx.get(url, timeout=15, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
        # Extract result snippets from HTML
        import re
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', resp.text, re.DOTALL)
        titles = re.findall(r'class="result__a"[^>]*>(.*?)</a>', resp.text, re.DOTALL)
        results = []
        for i, (t, s) in enumerate(zip(titles[:5], snippets[:5])):
            clean_t = re.sub(r"<[^>]+>", "", t).strip()
            clean_s = re.sub(r"<[^>]+>", "", s).strip()
            results.append(f"{i+1}. {clean_t}\n   {clean_s}")
        return "\n\n".join(results) if results else "No results found"
    except Exception as e:
        return f"Search error: {e}"
