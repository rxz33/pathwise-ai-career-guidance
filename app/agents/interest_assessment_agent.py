# app/agents/aptitude_interest_agent.py
from .base_agent import BaseAgent
from typing import Dict
from app.services.llm_service import safe_json_parse
from app.schemas.user_data import UserData

class AptitudeInterestAgent(BaseAgent):
    async def analyze_tests(self, tests: Dict, interests: Dict, personal_info: Dict = None) -> Dict:
        prompt = f"""
        Analyze user's tests and interests to suggest career domains.
        Personal info: {personal_info}
        Tests: {tests}
        Interests: {interests}
        Return JSON summary only with: suggested_domains, recommendations.
        """
        raw = await self.call_llm_cached("aptitude_interest_summary", prompt)
        return safe_json_parse(raw, fallback={})
