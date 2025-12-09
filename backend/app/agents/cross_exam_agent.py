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
You are a warm, practical career counselor. Begin with a short, gentle intro message 
that uses the user's name naturally to help them feel comfortable. 

For example:
"{user.personalInfo.fullName if user.personalInfo else 'Hey there'}, before we explore a few 
reflective questions, I want you to know this is a safe space. There are no right or wrong answers. 
Take your time, be honest with yourself, and treat this like a small conversation that can help you 
understand your own path better."

After the intro, generate 5–8 short, deeply personalized cross-examination questions 
using ONLY the user’s real data below.

Your goal: help the user reflect on gaps between their aspirations and their real situation 
(finances, city, weaknesses, academic field, leadership ability, strengths, etc.) 
in a gentle, supportive, non-judgmental way.

If a field is empty or missing, DO NOT mention it or make assumptions.

--- USER DATA ---
Full Name: {user.personalInfo.fullName if user.personalInfo else ""}
Strengths: {user.strengthsAndWeaknesses.strengths if user.strengthsAndWeaknesses else ""}
Weaknesses: {user.strengthsAndWeaknesses.struggleWith if user.strengthsAndWeaknesses else ""}
Preferred Role / Interests: {user.interests.preferredRole if user.interests else ""}
Risk-taking: {user.learningRoadmap.riskTaking if user.learningRoadmap else ""}
Leadership Experience: {user.optionalFields.leadershipRole if user.optionalFields else ""}
Academic Field: {user.personalInfo.fieldOfStudy if user.personalInfo else ""}
Location: {user.personalInfo.city if user.personalInfo else ""}
Financial Capacity: {user.personalInfo.financialStatus if user.personalInfo else ""}
------------------

RULES:
1. First print the intro paragraph (1–2 lines) using the user’s name naturally.
2. Then print the questions ONLY inside a JSON array.
3. Every question MUST combine 2–3 real traits (e.g., interest + weakness + finances).
4. Use the user’s name in 1 of the questions to maintain warmth.
5. Include 1–2 empathetic lines like:
   - “It’s okay if this feels confusing…”
   - “Take your time with this…”
6. Questions must be practical and scenario-based:
   - Costly goals + low finances → ask about coping strategy.
   - City limitations → ask about relocation or alternatives.
   - Weaknesses contradicting career → ask about improvement plan.
   - Low leadership + leadership-heavy roles → ask about skill-building.
7. Make each question feel conversational, human, supportive — never generic.
8. DO NOT mention missing or empty fields.
9. After the intro, output ONLY a JSON array of questions (no explanation).
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
