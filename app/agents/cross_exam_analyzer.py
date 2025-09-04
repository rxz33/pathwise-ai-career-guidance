from app.services.llm_service import call_llm
from app.config import AGENT_LLM_MAPPING

class CrossExamAnalyzer:
    def __init__(self, email: str, provider: str = None):
        self.email = email
        self.provider = provider or AGENT_LLM_MAPPING["cross_exam"]

    async def run(self, answers: dict) -> str:
        prompt = f"""
        Based on these cross-exam answers: {answers},
        analyze consistency and generate follow-up insights.
        """
        return await call_llm(provider=self.provider, prompt=prompt)
