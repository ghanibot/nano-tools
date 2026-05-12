"""
Office tools — read/write/manipulate Word, Excel, PowerPoint via OfficeCLI.
Requires OfficeCLI binary: https://github.com/iOfficeAI/OfficeCLI
"""
from __future__ import annotations
import json
import os
import shutil
import subprocess
import tempfile
from nano_tools.decorator import tool

_BINARY_NAME = "officecli"
_BINARY_FALLBACK = r"C:\Users\USER\AppData\Local\OfficeCLI\officecli.exe"


def _bin() -> str:
    found = shutil.which(_BINARY_NAME)
    if found:
        return found
    if os.path.exists(_BINARY_FALLBACK):
        return _BINARY_FALLBACK
    raise RuntimeError(
        "officecli not found. Install: irm https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.ps1 | iex"
    )


def _run(*args: str, parse_json: bool = True) -> dict | str:
    cmd = [_bin(), *args]
    if parse_json:
        cmd.append("--json")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    if parse_json:
        return json.loads(result.stdout)
    return result.stdout


@tool
def office_read(path: str, view: str = "text") -> str:
    """Read content from Word, Excel, or PowerPoint file.
    path: absolute path to .docx, .xlsx, or .pptx file
    view: output format — text (default), outline, html
    """
    return _run("view", path, view, parse_json=False)


@tool
def office_create(path: str) -> dict:
    """Create a new blank Word, Excel, or PowerPoint file.
    path: absolute path with extension .docx, .xlsx, or .pptx
    """
    return _run("create", path)


@tool
def office_get(path: str, selector: str) -> dict:
    """Get element value from Office file using path selector.
    path: absolute path to Office file
    selector: element path e.g. /sheet[1]/row[1]/cell[A1] or /slide[1]/shape[1]
    """
    return _run("get", path, selector)


@tool
def office_set(path: str, selector: str, value: str) -> dict:
    """Set text, value, or property in Office file.
    path: absolute path to Office file
    selector: element path e.g. /sheet[1]/row[1]/cell[A1]
    value: new value to set
    """
    return _run("set", path, selector, "--prop", f"value={value}")


@tool
def office_add(path: str, parent: str, element_type: str, props: str = "") -> dict:
    """Add element to Office file (slide, row, shape, table, etc).
    path: absolute path to Office file
    parent: parent selector e.g. / for root, /slide[1] for slide
    element_type: type to add — slide, shape, row, cell, table, paragraph
    props: comma-separated key=value properties e.g. title=Q4,layout=blank
    """
    args = ["add", path, parent, "--type", element_type]
    if props:
        for p in props.split(","):
            args += ["--prop", p.strip()]
    return _run(*args)


@tool
def office_remove(path: str, selector: str) -> dict:
    """Remove element from Office file.
    path: absolute path to Office file
    selector: element path to remove e.g. /slide[2]
    """
    return _run("remove", path, selector)


@tool
def office_merge(template_path: str, output_path: str, data_json: str) -> dict:
    """Merge JSON data into {{placeholder}} template file.
    template_path: path to template .docx/.xlsx/.pptx with {{key}} placeholders
    output_path: path for output file
    data_json: JSON string of key-value pairs e.g. {"name": "Alice", "date": "2026-05"}
    """
    data = json.loads(data_json)
    tmp = tempfile.mktemp(suffix=".json")
    try:
        with open(tmp, "w") as f:
            json.dump(data, f)
        return _run("merge", template_path, output_path, "--data", tmp)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


@tool
def office_screenshot(path: str, output_png: str, selector: str = "/") -> dict:
    """Render Office file page/slide/sheet to PNG image.
    path: absolute path to Office file
    output_png: output path for .png file
    selector: which page/slide to render, default / = first
    """
    return _run("view", path, "screenshot", selector, "--output", output_png)


@tool
def office_validate(path: str) -> dict:
    """Validate Office file structure and return any errors.
    path: absolute path to .docx, .xlsx, or .pptx file
    """
    return _run("validate", path)


@tool
def office_query(path: str, selector: str) -> dict:
    """Query multiple elements from Office file matching a selector pattern.
    path: absolute path to Office file
    selector: query selector e.g. /sheet[1]/row[*] to get all rows
    """
    return _run("query", path, selector)
