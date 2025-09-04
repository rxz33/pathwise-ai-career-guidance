from app.services.llm_service import call_llm
from app.config import AGENT_LLM_MAPPING

class GapAnalyzer:
    def __init__(self, email: str, provider: str = None):
        self.email = email
        self.provider = provider or AGENT_LLM_MAPPING["gap_analysis"]

    async def run(self, results: dict) -> str:
        prompt = f"""
        Based on cross-exam and resume analysis:
        {results},
        identify the most critical career gaps, missing skills, and growth areas.
        """
        return await call_llm(provider=self.provider, prompt=prompt)
