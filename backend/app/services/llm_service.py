# app/services/llm_service.py
from ..llm.groq_service import ask_groq
from ..llm.gemini_service import ask_gemini
from ..llm.openai_service import ask_openai
import re
import json
from typing import Any, Dict

def _clean_response(text: str) -> str:
    if not text:
        return ""

    text = text.strip()

    # Remove Markdown fences like ```json ... ```
    if text.startswith("```"):
        match = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1).strip()

    return text

def safe_json_parse(text: str, fallback: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Tries to parse JSON from LLM output safely.
    Cleans markdown fences and falls back to default dict if parsing fails.
    """
    if not text:
        return fallback or {}

    cleaned = _clean_response(text)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to extract JSON inside curly braces
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        return fallback or {"error": f"Invalid JSON: {cleaned[:200]}"}

async def call_llm(provider: str, prompt: str, **kwargs) -> str:
    if provider == "groq":
        return _clean_response(await ask_groq(prompt, **kwargs))

    elif provider == "gemini":
        return _clean_response(await ask_gemini(prompt, **kwargs))

    elif provider == "openai":
        return _clean_response(await ask_openai(prompt, **kwargs))

    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
