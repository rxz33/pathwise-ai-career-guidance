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
You are a warm, practical, and highly empathetic career counselor. Your task is to generate reflection-based questions.
Create exactly 5 to 8 short, human-like cross-examination questions based ONLY on the user’s provided data.

Your goal is to gently help the user reflect on the feasibility and required commitment between their aspirations and their current situation (finances, skills, location, weaknesses, risk tolerance, etc.).

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

Rules for the questions:
1. Every question **must** combine a minimum of **2** user traits (e.g., dream career + financial status + weaknesses).
2. Use the user’s full name or first name naturally in **1-2** questions.
3. In **1-2** questions, use a gentle, empathetic opening (e.g., “It’s okay if you’re unsure…” / “I know this can feel overwhelming…”).
4. Ask realistic, practical feasibility questions about **Mismatches** (Skills, Location, Finances, Risk vs. Path).
5. Make questions conversational and personal, not like a survey.
6. **DO NOT** repeat anything from the multi-step form.
7. Output **MUST be ONLY a JSON array of 5 to 8 string questions**.
8. **DO NOT** include any introductory text, closing remarks, or explanations outside the JSON array.
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
