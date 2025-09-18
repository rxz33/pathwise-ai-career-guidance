from app.services.llm_service import call_llm
import json

class FinalAnalyzerAgent:
    """
    Generate human-friendly career guidance report from all intermediate outputs.
    """
    def __init__(self, llm_provider="gemini"):
        self.llm_provider = llm_provider

    async def generate_final_report(self, user_data: dict, agent_output: dict, gap_report: dict, recommendations: dict) -> dict:
        prompt = f"""
        You are an expert career counselor AI.
        Consolidate all the user's data, resume/aptitude analysis, gap report, and career recommendations.
        Generate a human-friendly report for the user including:
          - Top 3 career options
          - Skill, education, or experience gaps
          - Recommended learning and action plan
          - Motivating, supportive, and encouraging tone (avoid criticism)
        
        User profile: {user_data}
        Previous analysis: {agent_output}
        Gap report: {gap_report}
        Recommendations: {recommendations}
        
        Return as a JSON object:
        {{
          "final_report": "..."
        }}
        """
        response = await call_llm(self.llm_provider, prompt)
        try:
            final_report = json.loads(response)
        except json.JSONDecodeError:
            final_report = json.loads(response.strip("` \n"))
        return final_report
