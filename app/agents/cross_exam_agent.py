from typing import Dict, List
from app.services.llm_service import call_llm

class CrossExamAgent:
    """
    AI agent to generate cross-examination questions and analyze user answers.
    """

    def __init__(self, llm_provider: str = "gemini"):
        self.llm_provider = llm_provider

    async def generate_questions(self, user_data: Dict) -> List[str]:
        """
        Generate 5-6 personalized questions based on user's data.
        """
        prompt = f"Generate 5 concise cross-examination questions based on this user info:\n{user_data}"
        response = await call_llm(self.llm_provider, prompt)
        # Split by newlines or numbers if needed
        questions = [q.strip() for q in response.split("\n") if q.strip()]
        return questions

    async def analyze_answers(self, user_data: Dict, answers: Dict) -> str:
        """
        Analyze user's answers and summarize insights.
        """
        prompt = f"User data: {user_data}\nUser answers: {answers}\nSummarize strengths, weaknesses, gaps, and suggest improvements."
        analysis = await call_llm(self.llm_provider, prompt)
        return analysis
