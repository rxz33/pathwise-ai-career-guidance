from app.services.llm_service import call_llm
from app.config import AGENT_LLM_MAPPING

class ResumeAnalyzer:
    def __init__(self, email: str, provider: str = None):
        self.email = email
        self.provider = provider or AGENT_LLM_MAPPING["resume"]

    async def run(self, resume_text: str) -> str:
        prompt = f"""
        Analyze this resume text for strengths, weaknesses, and missing skills:
        {resume_text}
        """
        return await call_llm(provider=self.provider, prompt=prompt)
