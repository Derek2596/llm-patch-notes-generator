import os
import asyncio
from typing import Optional
from .prompts import SYSTEM_PROMPT, build_user_prompt
from .config import cfg
from google import genai
from dotenv import load_dotenv

load_dotenv()  # Load .env into os.environ

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def generate_patch_notes(
    bullets: str,
    style: str = "concise",
    version: Optional[str] = None,
    date_str: Optional[str] = None,
) -> str:

    user_prompt = build_user_prompt(
        bullets=bullets,
        style=style,
        version=version,
        date_str=date_str,
    )

    full_prompt = f"{SYSTEM_PROMPT}\n\nUSER INPUT:\n{user_prompt}"

    try:
        # Wrap sync Gemini call in a thread for async FastAPI
        resp = await asyncio.to_thread(
            client.models.generate_content,
            model=cfg.GEMINI_MODEL,
            contents=full_prompt
        )
    except Exception as e:
        raise RuntimeError(f"Gemini API error: {str(e)}")

    text = resp.text.strip() if resp and hasattr(resp, "text") else ""

    # Basic fallback if output missing required headers
    if "Changes" not in text and "Version" not in text:
        return f"Version {version or 'Unversioned'}\n\nChanges:\n{bullets}"

    return text