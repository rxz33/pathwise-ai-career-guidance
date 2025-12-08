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
You are a friendly, supportive career counselor. Generate **5–9 personalized questions** 
to help the user identify gaps or inconsistencies in their career choices, skills, 
preferences, and circumstances.Detect inconsistencies and traits where user need reflection, 
also keep user data in mind to generate question so user reflects on that area of their life  

Use the user data below to make the questions **specific and practical**:

- Full Name: {user.personalInfo.fullName if user.personalInfo else ""}
- Strengths: {user.strengthsAndWeaknesses.strengths if user.strengthsAndWeaknesses else ""}
- Weaknesses: {user.strengthsAndWeaknesses.struggleWith if user.strengthsAndWeaknesses else ""}
- Preferred Role / Interests: {user.interests.preferredRole if user.interests else ""}
- Risk-taking: {user.learningRoadmap.riskTaking if user.learningRoadmap else ""}
- Leadership: {user.optionalFields.leadershipRole if user.optionalFields else ""}
- Academic Field: {user.personalInfo.fieldOfStudy if user.personalInfo else ""}
- Location: {user.personalInfo.city if user.personalInfo else ""}
- Financial Capacity: {user.personalInfo.financialStatus if user.optionalFields else ""}

**Guidelines:**
- Merge 1–2 fields to ask practical, scenario-based questions (e.g., financial + location: "You want an engineering course in a costly city; how will you manage financially?")
- Highlight contradictions (strengths vs weaknesses, risk-taking vs stability preference)
- Include location and financial considerations 
- Include user's name in 1-2 question
- Respond ONLY with a JSON array of plain text questions. No extra text.
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