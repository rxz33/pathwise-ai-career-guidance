from app.services.llm_service import call_llm, safe_json_parse
from app.schemas.user_data import UserData
from typing import List, Dict, Any

class CrossExamAgent:
    def __init__(self, provider: str = "groq", model: str = "llama3-8b-8192"):
        self.provider = provider
        self.model = model
        self.previous_rounds: Dict[str, List[str]] = {}

    async def call_llm(self, prompt: str) -> str:
        return await call_llm(self.provider, prompt)

    async def generate_questions(self, user_data: dict) -> List[str]:
        """
        Generate 5–6 personalized cross-examination questions based on user's data.
        """
        user = UserData(**user_data)
        email = user.email or "anonymous"

        prompt = f"""
You are a warm, practical career counselor. Generate 5–8 short, personalized 
cross-examination questions based ONLY on the user's real data below. Your goal is 
to gently help them reflect on the gap between their dreams and their actual situation.

Use the user’s data directly in your questions. If a data point is empty, you must avoid using it in the question.

--- USER DATA ---
- Full Name: {user.personalInfo.fullName if user.personalInfo else ""}
- Strengths: {user.strengthsAndWeaknesses.strengths if user.strengthsAndWeaknesses else ""}
- Weaknesses: {user.strengthsAndWeaknesses.struggleWith if user.strengthsAndWeaknesses else ""}
- Preferred Role / Interests: {user.interests.preferredRole if user.interests else ""}
- Risk-taking: {user.learningRoadmap.riskTaking if user.learningRoadmap else ""}
- Leadership: {user.optionalFields.leadershipRole if user.optionalFields else "No prior leadership experience"}
- Academic Field: {user.personalInfo.fieldOfStudy if user.personalInfo else ""}
- Location: {user.personalInfo.city if user.personalInfo else ""}
- Financial Capacity: {user.personalInfo.financialStatus if user.personalInfo else ""}
---

RULES:
1. Every question MUST combine 2–3 traits (e.g., interest + weakness + finances).
2. Use the user’s name in 1–2 questions.
3. Use an empathetic tone in 1–2 questions (“It’s okay if this feels confusing…”).
4. Ask practical feasibility questions:
   - If career goal is costly and finances are low → ask about coping strategy.
   - If city lacks opportunities → ask about relocation or online alternatives.
   - If weaknesses contradict the dream role → ask about plan to overcome them.
5. NO generic questions. Each question must sound tailored to THIS user’s life.
6. Output ONLY a JSON array of plain text questions.
"""



        try:
            raw = await self.call_llm(prompt)
            questions = safe_json_parse(raw, fallback=[])
            if not isinstance(questions, list):
                questions = []
        except Exception as e:
            print(f"[CrossExamAgent] Failed to parse questions: {e} | Raw: {raw[:200] if 'raw' in locals() else ''}")
            questions = []

        # Limit to 5–6 questions
        questions = questions[:6] if len(questions) > 6 else questions
        if len(questions) < 5:
            raise RuntimeError("AI did not generate enough questions for a single round.")

        # Save for this user
        self.previous_rounds[email] = questions
        return questions

    async def analyze_answers(self, user_data: dict, answers: List[str]) -> Dict[str, Any]:
        """
        Analyze user's answers and generate structured summary.
        """
        user = UserData(**user_data)
        email = user.email or "anonymous"
        previous_questions = self.previous_rounds.get(email, [])

        prompt = f"""
        You are a career counselor. Analyze the user's answers critically.
        User profile:
        Name: {user.personalInfo.fullName if user.personalInfo else ""}
        Strengths: {user.strengthsAndWeaknesses.strengths if user.strengthsAndWeaknesses else ""}
        Weaknesses: {user.strengthsAndWeaknesses.struggleWith if user.strengthsAndWeaknesses else ""}
        Preferred Role: {user.interests.preferredRole if user.interests else ""}
        Risk-taking: {user.learningRoadmap.riskTaking if user.learningRoadmap else ""}
        Leadership: {user.optionalFields.leadershipRole if user.optionalFields else ""}

        Questions asked: {previous_questions}
        User's answers: {answers}

        Return ONLY JSON with:
        - strengths (updated)
        - weaknesses (updated)
        - skill_gaps
        - suggestions
        - next_steps
        - friendly_summary (short, clear for user)
        """

        try:
            raw = await self.call_llm(prompt)
            analysis = safe_json_parse(raw, fallback={
                "strengths": [],
                "weaknesses": [],
                "skill_gaps": [],
                "suggestions": [],
                "next_steps": [],
                "friendly_summary": "Analysis failed or invalid JSON."
            })
        except Exception as e:
            print(f"[CrossExamAgent] Failed to analyze answers: {e}")
            analysis = {
                "strengths": [],
                "weaknesses": [],
                "skill_gaps": [],
                "suggestions": [],
                "next_steps": [],
                "friendly_summary": "Analysis failed due to exception."
            }

        return analysis 
