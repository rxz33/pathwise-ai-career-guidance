from app.services.llm_service import call_llm
from app.config import AGENT_LLM_MAPPING
import json

class RecommenderAgent:
    """
    Suggest top career paths, courses, and skill improvements.
    """
    def __init__(self, llm_provider="gemini"):
        self.llm_provider = llm_provider

    async def generate_recommendations(self, user_data: dict, agent_output: dict, gap_report: dict) -> dict:
        prompt = f"""
        You are an expert career counselor AI.
        Based on user's profile, suggested careers, and detected gaps,
        recommend top 3 careers with match score (0-1) and courses/skills to improve.

        User profile: {user_data}
        Previous analysis: {agent_output}
        Gap report: {gap_report}

        Return as valid JSON only:
        {{
          "top_careers": [
            {{
              "career": "career name",
              "match_score": 0.0-1.0,
              "recommended_courses": [list of courses/skills]
            }}
          ]
        }}
        """
        response = await call_llm(self.llm_provider, prompt)
        try:
            recommendations = json.loads(response)
        except json.JSONDecodeError:
            recommendations = json.loads(response.strip("` \n"))
        return recommendations
