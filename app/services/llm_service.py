# services/llm_service.py
from llm.groq_service import ask_groq
from llm.gemini_service import ask_gemini
from llm.openai_service import ask_openai

async def call_llm(provider: str, prompt: str, **kwargs) -> str:
    if provider == "groq":
        return await ask_groq(prompt, **kwargs)
    elif provider == "gemini":
        return await ask_gemini(prompt, **kwargs)
    elif provider == "openai":
        return await ask_openai(prompt, **kwargs)
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
