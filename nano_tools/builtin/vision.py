"""
Vision tools — analyze images using vision-capable LLMs.
Works with: claude-3-*, gpt-4o, gemini-1.5-*, any model with vision support.
Routes through nano-proxy if NANO_PROXY_URL is set.
"""
import base64
import os
from pathlib import Path
from nano_tools.decorator import tool


def _encode_image(path: str) -> tuple[str, str]:
    """Return (base64_data, media_type)."""
    p = Path(path)
    ext = p.suffix.lower()
    mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
                ".gif": "image/gif", ".webp": "image/webp"}
    media_type = mime_map.get(ext, "image/png")
    data = base64.standard_b64encode(p.read_bytes()).decode("utf-8")
    return data, media_type


@tool
def analyze_image(image_path: str, question: str) -> str:
    """Analyze an image using a vision-capable LLM and answer a question about it.
    image_path: Path to image file (jpg, png, gif, webp)
    question: Question to ask about the image
    """
    import anthropic

    try:
        data, media_type = _encode_image(image_path)
    except FileNotFoundError:
        return f"Error: image not found: {image_path}"
    except Exception as e:
        return f"Error reading image: {e}"

    kwargs: dict = {}
    proxy_url = os.environ.get("NANO_PROXY_URL")
    if proxy_url:
        kwargs["base_url"] = f"{proxy_url.rstrip('/')}/anthropic"

    client = anthropic.Anthropic(**kwargs)

    resp = client.messages.create(
        model="claude-opus-4-7",  # use most capable vision model
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": media_type, "data": data},
                },
                {"type": "text", "text": question},
            ],
        }],
    )
    return resp.content[0].text


@tool
def analyze_image_openai(image_path: str, question: str) -> str:
    """Analyze an image using OpenAI GPT-4o vision.
    image_path: Path to image file (jpg, png, gif, webp)
    question: Question to ask about the image
    """
    try:
        import openai
    except ImportError:
        return "Error: openai not installed. Run: pip install nano-tools[openai]"

    try:
        data, media_type = _encode_image(image_path)
    except FileNotFoundError:
        return f"Error: image not found: {image_path}"
    except Exception as e:
        return f"Error reading image: {e}"

    kwargs: dict = {}
    proxy_url = os.environ.get("NANO_PROXY_URL")
    if proxy_url:
        kwargs["base_url"] = f"{proxy_url.rstrip('/')}/openai/v1"

    client = openai.OpenAI(**kwargs)
    resp = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{data}"}},
                {"type": "text", "text": question},
            ],
        }],
    )
    return resp.choices[0].message.content or ""


@tool
def read_image_base64(image_path: str) -> str:
    """Read an image file and return its base64 encoding with media type.
    image_path: Path to image file
    """
    try:
        data, media_type = _encode_image(image_path)
        size = Path(image_path).stat().st_size
        return f"media_type: {media_type}\nsize: {size:,} bytes\nbase64: {data[:100]}... [{len(data)} chars total]"
    except Exception as e:
        return f"Error: {e}"
