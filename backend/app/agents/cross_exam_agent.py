from app.services.llm_service import call_llm, safe_json_parse
from app.schemas.user_data import UserData
from typing import List, Dict, Any


class CrossExamAgent:
    def __init__(self, provider: str = "groq"):
        self.provider = provider
        self.previous_rounds: Dict[str, List[str]] = {}

    async def call_llm(self, prompt: str) -> str:
        return await call_llm(self.provider, prompt)

    async def generate_questions(self, user_data: dict) -> List[str]:
        """
        Generate 5–6 deeply personalized cross-examination questions.
        """
        user = UserData(**user_data)
        email = user.email or "anonymous"

        prompt = f"""
You are acting like a human career counselor who knows this person personally.

Generate EXACTLY 5–6 short, reflective questions.
Return ONLY a JSON array of strings. No intro. No explanations.

CRITICAL INSTRUCTION:
Each question MUST explicitly reference at least ONE concrete user detail
(name, finances, city, strengths, weaknesses, preferred role, risk style).
If a detail is missing, do NOT invent it.

USER PROFILE:
Name: {user.personalInfo.fullName if user.personalInfo else ""}
Strengths: {user.strengthsAndWeaknesses.strengths if user.strengthsAndWeaknesses else ""}
Weaknesses: {user.strengthsAndWeaknesses.struggleWith if user.strengthsAndWeaknesses else ""}
Preferred Role: {user.interests.preferredRole if user.interests else ""}
Risk-taking: {user.learningRoadmap.riskTaking if user.learningRoadmap else ""}
Leadership: {user.optionalFields.leadershipRole if user.optionalFields else ""}
Field of Study: {user.personalInfo.fieldOfStudy if user.personalInfo else ""}
City: {user.personalInfo.city if user.personalInfo else ""}
Financial Status: {user.personalInfo.financialStatus if user.personalInfo else ""}

QUESTION RULES:
1. Every question must combine 2–3 real traits  
   (example: career goal + finances, weakness + role, city + opportunity).
2. Use the user's name naturally in 1–2 questions.
3. Include exactly ONE empathetic phrase such as:
   “It’s okay if this feels confusing…” OR “Take a moment and think honestly…”
4. NO generic counseling questions.
5. NO vague wording like “your situation” or “your goals”.
6. Questions should sound like:
   “Given X, how will you realistically do Y?”

OUTPUT FORMAT:
[
  "question 1",
  "question 2",
  ...
]
"""


        raw = await self.call_llm(prompt)
        questions = safe_json_parse(raw, fallback=[])

        if not isinstance(questions, list):
            questions = []

        # Clean & enforce count
        questions = [q.strip() for q in questions if isinstance(q, str) and q.strip()]
        questions = questions[:6]

        if len(questions) < 5:
            # fallback → avoid 500 crash
            questions = [
                "It’s okay if this feels confusing—what feels like the biggest gap right now between your goals and your current situation?",
                "How do your financial situation and your career goals align, and where might you need a backup plan?",
                "Given your strengths and weaknesses, what part of your preferred role feels most challenging today?",
                "How realistic is your current plan considering your location and available opportunities?",
                "What small step could you take in the next 3 months to reduce the gap between where you are and where you want to be?"
            ]

        self.previous_rounds[email] = questions
        return questions
