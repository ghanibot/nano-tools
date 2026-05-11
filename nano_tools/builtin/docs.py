from nano_tools.decorator import tool


@tool
def read_pdf(path: str) -> str:
    """Extract text content from a PDF file.
    path: Path to the PDF file
    """
    try:
        import pypdf
    except ImportError:
        return "Error: pypdf not installed. Run: pip install nano-tools[docs]"
    try:
        from pathlib import Path
        reader = pypdf.PdfReader(str(path))
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if text.strip():
                pages.append(f"[Page {i+1}]\n{text.strip()}")
        content = "\n\n".join(pages)
        if len(content) > 20000:
            return content[:20000] + f"\n\n[truncated — {len(content)} total chars, {len(reader.pages)} pages]"
        return content or "(no extractable text found)"
    except FileNotFoundError:
        return f"Error: file not found: {path}"
    except Exception as e:
        return f"Error reading PDF: {e}"


@tool
def query_sqlite(db_path: str, sql: str) -> str:
    """Execute a SQL query against a SQLite database and return results.
    db_path: Path to the .db file
    sql: SQL query to execute
    """
    import sqlite3
    import json
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.execute(sql)
        rows = cur.fetchall()
        conn.close()
        if not rows:
            return "(no rows returned)"
        data = [dict(r) for r in rows]
        result = json.dumps(data[:200], indent=2, default=str)
        if len(rows) > 200:
            result += f"\n\n[showing 200 of {len(rows)} rows]"
        return result
    except sqlite3.OperationalError as e:
        return f"SQL error: {e}"
    except Exception as e:
        return f"Error: {e}"


@tool
def list_sqlite_tables(db_path: str) -> str:
    """List all tables and their columns in a SQLite database.
    db_path: Path to the .db file
    """
    import sqlite3
    try:
        conn = sqlite3.connect(db_path)
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        lines = []
        for (table,) in tables:
            cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
            col_names = [c[1] for c in cols]
            lines.append(f"  {table} ({', '.join(col_names)})")
        conn.close()
        return "Tables:\n" + "\n".join(lines) if lines else "(no tables found)"
    except Exception as e:
        return f"Error: {e}"
