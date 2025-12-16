# # app/agents/base_agent.py
# from app.services.llm_service import call_llm
# from typing import Dict

# AGENT_DEFAULT_LLM = {
#     "ResumeAnalyzerAgent": "groq",
#     "CrossExamAgent": "gemini",
#     "GapAnalyzerAgent": "gemini",
#     "RecommenderAgent": "openai"
# }


# class BaseAgent:
#     def __init__(self, llm_provider="gemini"):
#         self.llm_provider = llm_provider
#         self.cache = {}

#     async def call_llm_cached(self, key: str, prompt: str) -> str:
#         if key in self.cache:
#             return self.cache[key]
#         response = await call_llm(self.llm_provider, prompt)
#         self.cache[key] = response
#         return response.strip()
# app/agents/base_agent.py
from app.services.llm_service import call_llm
from typing import Dict

AGENT_DEFAULT_LLM = {
    "SocioEconomicAgent": "groq",
    "LearningRoadmapAgent": "groq",
    "AptitudeInterestAgent": "groq",
    "ResumeAnalyzerAgent": "groq",

    "CrossExamAgent": "groq",
    "GapAnalyzerAgent": "groq",

    "RecommenderAgent": "openai"
}

class BaseAgent:
    def __init__(self, llm_provider=None):
        # If manually provided → use it.
        if llm_provider:
            self.llm_provider = llm_provider
        
        # Else auto pick based on class name
        else:
            self.llm_provider = AGENT_DEFAULT_LLM.get(
                self.__class__.__name__, 
                "groq"   # fallback LLM
            )

        self.cache: Dict[str, str] = {}

    async def call_llm_cached(self, key: str, prompt: str) -> str:
        if key in self.cache:
            return self.cache[key]

        response = await call_llm(self.llm_provider, prompt)
        cleaned = response.strip()

        self.cache[key] = cleaned
        return cleaned
