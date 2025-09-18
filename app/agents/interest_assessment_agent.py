from typing import Dict
from app.services.llm_service import call_llm
import json

class AptitudeInterestAgent:
    """
    AI agent to suggest potential career domains based on user's aptitude, interests, and cross-exam answers.
    """

    def __init__(self, llm_provider: str = "gemini"):
        self.llm_provider = llm_provider

    async def suggest_domains(self, user_data: Dict) -> Dict:
        """
        Input: user_data
        Output: recommended domains, aptitude scores, and interest tags
        """
        prompt = f"""
        You are an expert career counselor AI.
        Suggest suitable career domains based on user profile, aptitude, and interests.
        Return JSON with:
        - recommended_domains: list of career domains
        - aptitude_scores: mapping of skills/aptitudes to 0-10
        - interest_tags: relevant interests

        User Data: {user_data}
        """
        response = await call_llm(self.llm_provider, prompt)
        try:
            suggestion = json.loads(response)
        except json.JSONDecodeError:
            suggestion = json.loads(response.strip("` \n"))
        return suggestion
