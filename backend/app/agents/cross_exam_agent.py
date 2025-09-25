# from app.services.llm_service import call_llm, safe_json_parse
# from app.schemas.user_data import UserData
# from typing import List, Dict, Any
# import json

# class CrossExamAgent:
#     def __init__(self, provider: str = "groq", model: str = "llama3-8b-8192"):
#         self.provider = provider
#         self.model = model
#         self.previous_rounds: Dict[str, List[str]] = {}

#     async def call_llm(self, prompt: str) -> str:
#         return await call_llm(self.provider, prompt)

#     async def generate_questions(self, user_data: dict) -> List[str]:
#         """
#         Generate a single round of 5–6 AI-based critical questions.
#         """
#         user = UserData(**user_data)

#         prompt = f"""
#         You are a career counselor. Generate exactly 5–6 cross-examination questions 
#         to validate user's strengths, weaknesses, interests, risk-taking, and leadership.
#         Respond ONLY with a JSON array of plain text questions. Do not include any extra text.

#         User Info:
#           Name: {user.personalInfo.fullName if user.personalInfo else ""}
#           Email: {user.email or ""}
#           Academic: {user.personalInfo.fieldOfStudy if user.personalInfo else ""}
#           Strengths: {user.strengthsAndWeaknesses.strengths if user.strengthsAndWeaknesses else ""}
#           Weaknesses: {user.strengthsAndWeaknesses.struggleWith if user.strengthsAndWeaknesses else ""}
#           Preferred Role: {user.interests.preferredRole if user.interests else ""}
#           Risk-taking: {user.learningRoadmap.riskTaking if user.learningRoadmap else ""}
#           Leadership: {user.optionalFields.leadershipRole if user.optionalFields else ""}
#         """

#         questions: List[str] = []
#         try:
#             raw = await self.call_llm(prompt)
#             questions = safe_json_parse(raw, fallback=[])
#             # Ensure it's a list
#             if not isinstance(questions, list):
#                 questions = []
#         except Exception as e:
#             print(f"[CrossExamAgent] ❌ Failed to parse questions: {e} | Raw: {raw[:200] if 'raw' in locals() else ''}")

#         # Ensure exactly 5–6 questions
#         questions = questions[:6] if len(questions) > 6 else questions
#         if len(questions) < 5:
#             raise RuntimeError("AI did not generate enough questions for the single round.")

#         # Save in memory for this user
#         email = user.email or "anonymous"
#         self.previous_rounds[email] = questions

#         return questions

#     async def analyze_answers(self, user_data: dict, answers: List[str]) -> Dict[str, Any]:
#         """
#         Analyze the answers to the AI-generated cross-exam questions.
#         """
#         user = UserData(**user_data)
#         email = user.email or "anonymous"
#         previous_answers = self.previous_rounds.get(email, [])

#         strengths = user.strengthsAndWeaknesses.strengths if user.strengthsAndWeaknesses else ""
#         weaknesses = user.strengthsAndWeaknesses.struggleWith if user.strengthsAndWeaknesses else ""
#         preferred_role = user.interests.preferredRole if user.interests else ""
#         full_name = user.personalInfo.fullName if user.personalInfo else ""
#         risk_taking = user.learningRoadmap.riskTaking if user.learningRoadmap else ""
#         leadership = user.optionalFields.leadershipRole if user.optionalFields else ""

#         prompt = f"""
#         Analyze the user's answers from a career cross-exam.
#         User Info: Name={full_name}, Strengths={strengths}, Weaknesses={weaknesses},
#         Preferred Role={preferred_role}, Risk={risk_taking}, Leadership={leadership}
#         Answers: {answers}
#         Previous Q&A: {previous_answers}
#         Return a JSON summary with: strengths, weaknesses, skill_gaps, suggestions, next_steps, friendly_summary.
#         """

#         try:
#             raw = await self.call_llm(prompt)
#             analysis = safe_json_parse(raw, fallback={
#                 "strengths": [], "weaknesses": [], "skill_gaps": [],
#                 "suggestions": [], "next_steps": [], "friendly_summary": "Analysis failed or invalid JSON."
#             })
#         except Exception as e:
#             print(f"[CrossExamAgent] ❌ Failed to analyze answers: {e}")
#             analysis = {
#                 "strengths": [], "weaknesses": [], "skill_gaps": [],
#                 "suggestions": [], "next_steps": [], "friendly_summary": "Analysis failed due to exception."
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
preferences, and circumstances. Each question should feel like it comes from a human 
counselor guiding them to think critically about their career path.  

Use the user data below to make the questions **specific and practical**:

- Full Name: {user.personalInfo.fullName if user.personalInfo else ""}
- Strengths: {user.strengthsAndWeaknesses.strengths if user.strengthsAndWeaknesses else ""}
- Weaknesses: {user.strengthsAndWeaknesses.struggleWith if user.strengthsAndWeaknesses else ""}
- Preferred Role / Interests: {user.interests.preferredRole if user.interests else ""}
- Risk-taking: {user.learningRoadmap.riskTaking if user.learningRoadmap else ""}
- Leadership: {user.optionalFields.leadershipRole if user.optionalFields else ""}
- Academic Field: {user.personalInfo.fieldOfStudy if user.personalInfo else ""}
- Location: {user.personalInfo.hometown if user.personalInfo else ""}
- Financial Capacity: {user.optionalFields.financialCapacity if user.optionalFields else ""}
- Prior Experience / Optional Info: {user.optionalFields.additionalInfo if user.optionalFields else ""}

**Guidelines:**
- Merge 1–2 fields to ask practical, scenario-based questions (e.g., financial + location: "You want an engineering course in a costly city; how will you manage financially?")
- Highlight contradictions (strengths vs weaknesses, risk-taking vs stability preference)
- Include location and financial considerations
- Include prior experience if relevant
- Friendly, guiding, not criticizing
- Respond ONLY with a JSON array of plain text questions. No extra text.
"""



        try:
            raw = await self.call_llm(prompt)
            questions = safe_json_parse(raw, fallback=[])
            if not isinstance(questions, list):
                questions = []
        except Exception as e:
            print(f"[CrossExamAgent] ❌ Failed to parse questions: {e} | Raw: {raw[:200] if 'raw' in locals() else ''}")
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
            print(f"[CrossExamAgent] ❌ Failed to analyze answers: {e}")
            analysis = {
                "strengths": [],
                "weaknesses": [],
                "skill_gaps": [],
                "suggestions": [],
                "next_steps": [],
                "friendly_summary": "Analysis failed due to exception."
            }

        return analysis
