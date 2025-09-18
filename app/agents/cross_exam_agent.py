from typing import Dict, List
from app.services.llm_service import call_llm


class CrossExamAgent:
    """
    AI agent to:
    - Generate cross-examination questions
    - Analyze answers (raw text output)
    - Generate follow-ups
    - Summarize and suggest next career steps

    Agent returns raw LLM text (string).
    JSON parsing happens outside in the route (with safe_json_parse).
    """

    def __init__(self, llm_provider: str = "gemini", max_followup_rounds: int = 2):
        self.llm_provider = llm_provider
        self.max_followup_rounds = max_followup_rounds

    async def generate_questions(self, user_data: Dict) -> List[str]:
        """
        Generate 5–6 friendly, human-sounding questions.
        """
        prompt = f"""
        You are a friendly and supportive career counselor AI.
        Generate 5–6 personalized questions to better understand this user's
        skills, strengths, interests, and career aspirations.
        Use a positive and encouraging tone.
        Return as a numbered list (plain text).
        
        User data: {user_data}
        """
        response = await call_llm(self.llm_provider, prompt)
        questions = [q.strip() for q in response.split("\n") if q.strip()]
        return questions

    async def analyze_answers(self, user_data: Dict, answers: Dict) -> str:
        """
        Return raw JSON-like text from the LLM.
        Parsing is handled in the route.
        """
        prompt = f"""
        You are a friendly career counselor AI.
        Analyze the user's profile and answers to identify:
        - Strengths
        - Weaknesses
        - Skill gaps
        Provide output ONLY as JSON in this schema:

        {{
          "strengths": [list of strengths],
          "weaknesses": [list of weaknesses],
          "skill_gaps": [list of missing or weak skills],
          "suggestions": [list of recommended actions],
          "friendly_summary": "A human-sounding explanation",
          "next_steps": [list of actionable career guidance]
        }}

        Profile: {user_data}
        Answers: {answers}
        """
        response = await call_llm(self.llm_provider, prompt)
        return response.strip()  # return raw text only

    async def generate_followups(
        self, user_data: Dict, answers: Dict, round_number: int = 1
    ) -> str:
        """
        Generate follow-up questions if inconsistencies exist.
        Returns raw JSON-like text (route parses it).
        """
        if round_number > self.max_followup_rounds:
            return ""

        prompt = f"""
        You are a friendly career counselor AI.
        Based on the user's profile and answers, identify areas that need clarification,
        examples, or expansion.
        Generate 2–3 follow-up questions in this format (valid JSON array):

        [
          {{
            "question": "string",
            "type": "verification | expansion | clarification",
            "confidence": 0–1
          }}
        ]

        Profile: {user_data}
        Answers: {answers}
        """
        followup_text = await call_llm(self.llm_provider, prompt)
        return followup_text.strip()  # return raw text
