# from app.services.llm_service import call_llm, safe_json_parse
# from app.schemas.user_data import UserData
# from typing import List, Dict, Any

# class CrossExamAgent:
#     def __init__(self, provider: str = "groq", model: str = "llama3-8b-8192"):
#         self.provider = provider
#         self.model = model
#         self.previous_rounds: Dict[str, List[str]] = {}

#     async def call_llm(self, prompt: str) -> str:
#         return await call_llm(self.provider, prompt)

#     async def generate_questions(self, user_data: dict) -> List[str]:
#         """
#         Generate 5–6 personalized cross-examination questions based on user's data.
#         """
#         user = user_data  
#         email = user.get("personal", {}).get("email", "anonymous")


#         prompt = f"""
# You are an expert career counselor. Generate 5–9 cross-examination questions based ONLY on the user’s data.

# The questions must feel warm and human. 
# • Use the user’s name (“{user.personalInfo.fullName}”) naturally in 1–3 questions.
# • Include 1–2 soft, empathetic lines such as “It’s okay if you’re unsure…” or 
#   “I understand this part can feel confusing…”.

# Goal: uncover contradictions, unclear goals, unrealistic expectations, missing details, emotional hesitation, or practical constraints.

# User Data:
# - Name: {user.personalInfo.fullName}
# - Strengths: {user.strengthsAndWeaknesses.strengths}
# - Weaknesses: {user.strengthsAndWeaknesses.struggleWith}
# - Preferred Role: {user.interests.preferredRole}
# - Risk-taking: {user.learningRoadmap.riskTaking}
# - Field of Study: {user.personalInfo.fieldOfStudy}
# - Hometown: {user.personalInfo.city}
# - Willing to Move: {user.personalInfo.mobility}
# - Financial Capacity: {user.personalInfo.financialStatus}
# - Leadership/Team Role: {user.optionalFields.leadershipRole}

# Guidelines:
# - Merge 1–2 traits to form scenario-based questions.
# - Gently highlight contradictions (skills vs interest, risk-taking vs stability preference, financial limits vs expensive paths, etc.).
# - Include at least one question about hometown, relocation, or financial feasibility.
# - Empathetic tone in 1–2 questions, not all.
# - Output MUST be a pure JSON array of questions (strings only).

# """



#         try:
#             raw = await self.call_llm(prompt)
#             questions = safe_json_parse(raw, fallback=[])
#             if not isinstance(questions, list):
#                 questions = []
#         except Exception as e:
#             print(f"[CrossExamAgent] Failed to parse questions: {e} | Raw: {raw[:200] if 'raw' in locals() else ''}")
#             questions = []

#         # Limit to 5–6 questions
#         questions = questions[:6] if len(questions) > 6 else questions
#         if len(questions) < 5:
#             raise RuntimeError("AI did not generate enough questions for a single round.")

#         # Save for this user
#         self.previous_rounds[email] = questions
#         return questions

#     async def analyze_answers(self, user_data: dict, answers: List[str]) -> Dict[str, Any]:
#         """
#         Analyze user's answers and generate structured summary.
#         """
#         user = UserData(**user_data)
#         email = user.email or "anonymous"
#         previous_questions = self.previous_rounds.get(email, [])

#         prompt = f"""
#         You are a career counselor. Analyze the user's answers critically.
#         User profile:
#         Name: {user.personalInfo.fullName if user.personalInfo else ""}
#         Strengths: {user.strengthsAndWeaknesses.strengths if user.strengthsAndWeaknesses else ""}
#         Weaknesses: {user.strengthsAndWeaknesses.struggleWith if user.strengthsAndWeaknesses else ""}
#         Preferred Role: {user.interests.preferredRole if user.interests else ""}
#         Risk-taking: {user.learningRoadmap.riskTaking if user.learningRoadmap else ""}
#         Leadership: {user.optionalFields.leadershipRole if user.optionalFields else ""}

#         Questions asked: {previous_questions}
#         User's answers: {answers}

#         Return ONLY JSON with:
#         - strengths (updated)
#         - weaknesses (updated)
#         - skill_gaps
#         - suggestions
#         - next_steps
#         - friendly_summary (short, clear for user)
#         """

#         try:
#             raw = await self.call_llm(prompt)
#             analysis = safe_json_parse(raw, fallback={
#                 "strengths": [],
#                 "weaknesses": [],
#                 "skill_gaps": [],
#                 "suggestions": [],
#                 "next_steps": [],
#                 "friendly_summary": "Analysis failed or invalid JSON."
#             })
#         except Exception as e:
#             print(f"[CrossExamAgent] Failed to analyze answers: {e}")
#             analysis = {
#                 "strengths": [],
#                 "weaknesses": [],
#                 "skill_gaps": [],
#                 "suggestions": [],
#                 "next_steps": [],
#                 "friendly_summary": "Analysis failed due to exception."
#             }

#         return analysis


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

Based on the user's profile, write 5–8 SHORT, specific questions that help them reflect on:
- the gap between their dreams and their real situation (money, marks, location, time)
- contradictions in their own data (strengths vs weaknesses, risk vs stability, etc.)
- concrete next steps they can actually take

Use this profile DIRECTLY in your questions:
- Name: {user.personalInfo.fullName if user.personalInfo else ""}
- Strengths: {user.strengthsAndWeaknesses.strengths if user.strengthsAndWeaknesses else ""}
- Weaknesses: {user.strengthsAndWeaknesses.struggleWith if user.strengthsAndWeaknesses else ""}
- Preferred Role / Dream Careers: {user.interests.preferredRole if user.interests else ""}
- Risk-taking Style: {user.learningRoadmap.riskTaking if user.learningRoadmap else ""}
- Leadership / Responsibilities: {user.optionalFields.leadershipRole if user.optionalFields else ""}
- Academic Field / Background: {user.personalInfo.fieldOfStudy if user.personalInfo else ""}
- City / Location: {user.personalInfo.city if user.personalInfo else ""}
- Financial Situation: {user.personalInfo.financialStatus if user.personalInfo else ""}
- Extra Info (family, pressure, health, etc.): {user.optionalFields.additionalInfo if user.optionalFields else ""}

Question style rules:
1) Every question must feel like a real conversation, not an exam.
2) Use the user's own details inside the question (goals, money, city, strengths, weaknesses, etc.).
   - If the user has low or struggling finances but wants an expensive or long study career
     (e.g. doctor, foreign studies, IIT, big city degrees), ask HOW they imagine managing fees,
     time, entrance exams, and family responsibilities.
3) In at least 3 questions, MERGE 2–3 fields. Example patterns (do not copy text):
   - dream career + financialStatus
   - dream career + marks/skills + family/pressure
   - riskTaking + preferredRole + stability/income
4) Mention the user's name in 1–2 questions to make it feel personal.
5) In 2–3 questions, sound gently empathetic and safe, for example:
   - “I know this can feel heavy sometimes…”,
   - “It’s okay if you’re unsure right now, {user.personalInfo.fullName}…”
6) Ask about feasibility, trade-offs and Plan B when dreams are very risky or costly
   compared to their current reality.
7) Do NOT repeat questions that were already asked in a normal form (like “What are your strengths?”).
   Always build ON TOP of the info they already gave.

Respond ONLY with a valid JSON array of plain text questions, for example:
[
  "question 1...",
  "question 2..."
]
No extra keys, no commentary, no markdown.
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