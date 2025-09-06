from typing import Dict, List
from app.services.llm_service import call_llm
import json


class CrossExamAgent:
    """
    AI agent to generate cross-examination questions, analyze answers,
    and generate follow-up clarifications.
    """

    def __init__(self, llm_provider: str = "gemini"):
        self.llm_provider = llm_provider

    async def generate_questions(self, user_data: Dict) -> List[str]:
        """
        Generate 5-6 personalized questions based on user's data.
        """
        prompt = f"""
        You are an expert career counselor AI.
        Generate 5-6 personalized cross-examination questions for this user.
        Focus on verifying strengths, weaknesses, skills, and interests.
        Return the output as a numbered list.

        User data: {user_data}
        """
        response = await call_llm(self.llm_provider, prompt)
        questions = [q.strip() for q in response.split("\n") if q.strip()]
        return questions

    async def analyze_answers(self, user_data: Dict, answers: Dict) -> Dict:
        """
        Analyze user's answers and summarize insights in structured JSON.
        """
        prompt = f"""
        You are an expert career counselor AI.
        Analyze the following user profile and answers.

        Profile: {user_data}
        Answers: {answers}

        Summarize in **valid JSON only** with this schema:
        {{
          "strengths": [list of strengths],
          "weaknesses": [list of weaknesses],
          "skill_gaps": [list of missing or weak skills],
          "suggestions": [list of improvements and recommendations]
        }}
        Do not include explanations outside JSON.
        """
        response = await call_llm(self.llm_provider, prompt)

        try:
            analysis = json.loads(response)
        except json.JSONDecodeError:
            # fallback: try cleaning up malformed response
            cleaned = response.strip("` \n")  # remove markdown ticks if present
            analysis = json.loads(cleaned)

        return analysis

    async def generate_followups(self, user_data: Dict, answers: Dict) -> List[str]:
        """
        Generate 2-3 clarifying follow-up questions based on contradictions or missing info.
        """
        prompt = f"""
        You are an expert career counselor AI.
        Compare the user's profile and answers. Identify contradictions, gaps, or vague info.
        Then generate 2-3 clarifying follow-up questions to validate their strengths,
        weaknesses, or skills. Return as a numbered list only.

        Profile: {user_data}
        Answers: {answers}
        """
        followup_text = await call_llm(self.llm_provider, prompt)
        followup_questions = [q.strip() for q in followup_text.split("\n") if q.strip()]
        return followup_questions
