# app/agents/base_agent.py
from app.services.llm_service import call_llm
from typing import Dict

class BaseAgent:
    def __init__(self, llm_provider="gemini"):
        self.llm_provider = llm_provider
        self.cache = {}

    async def call_llm_cached(self, key: str, prompt: str) -> str:
        if key in self.cache:
            return self.cache[key]
        response = await call_llm(self.llm_provider, prompt)
        self.cache[key] = response
        return response.strip()
