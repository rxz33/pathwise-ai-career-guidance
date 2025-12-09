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
You are a warm, practical career counselor.

Generate ONLY a JSON array of 5–8 deeply personalized cross-examination questions.
No intro. No text outside JSON. STRICT JSON array only.

Use ONLY the user's real data. If a field is empty, ignore it completely.

USER DATA:
Full Name: {user.personalInfo.fullName if user.personalInfo else ""}
Strengths: {user.strengthsAndWeaknesses.strengths if user.strengthsAndWeaknesses else ""}
Weaknesses: {user.strengthsAndWeaknesses.struggleWith if user.strengthsAndWeaknesses else ""}
Preferred Role: {user.interests.preferredRole if user.interests else ""}
Risk-taking: {user.learningRoadmap.riskTaking if user.learningRoadmap else ""}
Leadership: {user.optionalFields.leadershipRole if user.optionalFields else ""}
Academic Field: {user.personalInfo.fieldOfStudy if user.personalInfo else ""}
Location: {user.personalInfo.city if user.personalInfo else ""}
Financial Capacity: {user.personalInfo.financialStatus if user.personalInfo else ""}

RULES:
1. Output ONLY a JSON array. No intro, no explanations.
2. Each question MUST combine 2–3 real traits (e.g., preferred role + weakness + finances).
3. Use the user's name naturally in 1 question (if available).
4. Add 1–2 empathetic tones across the questions:
   - “It’s okay if this feels confusing…”
   - “Take your time with this…”
5. Questions must be conversational, warm, and practical:
   - If finances are “Lower Class” + dream is expensive → ask about coping strategy.
   - If city lacks opportunities → ask about relocation / online options.
   - If weaknesses contradict role → ask about improvement plan.
   - If leadership = 'No' but role needs it → ask about building credibility.
6. DO NOT mention missing fields.
7. DO NOT wrap inside an object. ONLY output a JSON array of questions.
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
