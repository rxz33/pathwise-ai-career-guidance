from app.services.llm_service import call_llm
import json

class GapAnalyzerAgent:
    """
    Detect gaps between user's current profile and target careers.
    """
    def __init__(self, llm_provider="gemini"):
        self.llm_provider = llm_provider

    async def detect_gaps(self, user_data: dict, agent_output: dict) -> dict:
        prompt = f"""
        You are an expert career counselor AI.
        Analyze the user's profile and the suggested career paths.
        Identify missing skills, experience, or education gaps that prevent success.

        User profile: {user_data}
        Suggested career/aptitude output: {agent_output}

        Return a JSON with:
        {{
          "missing_skills": [list of missing skills],
          "experience_gaps": [list of missing experience],
          "education_gaps": [list of missing education/training]
        }}
        """
        response = await call_llm(self.llm_provider, prompt)
        try:
            gaps = json.loads(response)
        except json.JSONDecodeError:
            gaps = json.loads(response.strip("` \n"))
        return gaps
