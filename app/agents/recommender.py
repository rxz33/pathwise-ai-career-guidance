from app.services.llm_service import call_llm
from app.config import AGENT_LLM_MAPPING

class RecommenderAgent:
    def __init__(self, email: str, provider: str = None):
        self.email = email
        self.provider = provider or AGENT_LLM_MAPPING["recommender"]

    async def run(self, results: dict) -> str:
        prompt = f"""
        Using this student analysis: {results},
        suggest the top 3 most suitable career pathways with reasoning,
        and provide a short roadmap for each.
        """
        return await call_llm(provider=self.provider, prompt=prompt)
