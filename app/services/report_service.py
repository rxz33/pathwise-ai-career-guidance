# app/services/career_guidance_orchestrator.py
from app.agents.cross_exam_agent import CrossExamAgent
from app.agents.gap_analyzer import GapAnalyzerAgent
from app.agents.interest_assessment_agent import AptitudeInterestAgent
from app.agents.learning_roadmap_agent import LearningRoadmapAgent
from app.agents.resume_analyzer import ResumeAnalyzerAgent
from app.agents.socioeconomic_agent import SocioEconomicAgent
from app.schemas.user_data import UserData
from typing import Dict, Any
import asyncio

class CareerGuidanceOrchestrator:
    def __init__(self):
        self.socio_agent = SocioEconomicAgent()
        self.resume_agent = ResumeAnalyzerAgent()
        self.aptitude_agent = AptitudeInterestAgent()
        self.learning_agent = LearningRoadmapAgent()
        self.cross_agent = CrossExamAgent()
        self.gap_agent = GapAnalyzerAgent()

    async def run(self, user_data: dict) -> Dict[str, Any]:
        user = UserData(**user_data)
        insights: Dict[str, Any] = {}

        # 1️⃣ Socio-economic summary
        try:
            insights["socio_summary"] = await self.socio_agent.generate_summary(
                personal_info=user.personalInfo.dict() if user.personalInfo else {},
                optional_fields=user.optionalFields.dict() if user.optionalFields else {}
            )
        except Exception as e:
            insights["socio_summary"] = {"error": str(e)}

        # 2️⃣ Resume analysis (only if resume exists)
        try:
            if user.resume and user.resume.extractedText:
                insights["resume_summary"] = await self.resume_agent.analyze_resume(
                    resume_text=user.resume.extractedText,
                    strengths_and_weaknesses=user.strengthsAndWeaknesses.dict() if user.strengthsAndWeaknesses else {},
                    preferred_role=user.interests.preferredRole if user.interests else ""
                )
            else:
                insights["resume_summary"] = {}
        except Exception as e:
            insights["resume_summary"] = {"error": str(e)}

        # 3️⃣ Aptitude & interest analysis (tests + interests)
        try:
            tests_dict = user.tests.dict() if user.tests else {}
            interests_dict = user.interests.dict() if user.interests else {}
            insights["aptitude_summary"] = await self.aptitude_agent.analyze_tests(
                tests=tests_dict,
                interests=interests_dict,
                personal_info=user.personalInfo.dict() if user.personalInfo else {}
            )
        except Exception as e:
            insights["aptitude_summary"] = {"error": str(e)}

        # 4️⃣ Learning roadmap analysis
        try:
            learning_data = user.learningRoadmap.dict() if user.learningRoadmap else {}
            strengths_weaknesses = user.strengthsAndWeaknesses.dict() if user.strengthsAndWeaknesses else {}
            insights["learning_summary"] = await self.learning_agent.analyze_learning(
                learning_data=learning_data,
                strengths_and_weaknesses=strengths_weaknesses
            )
        except Exception as e:
            insights["learning_summary"] = {"error": str(e)}

        # 5️⃣ Cross-examination analysis
        try:
            cross_questions = await self.cross_agent.generate_questions(user_data)
            insights["cross_questions"] = cross_questions
            # Optionally you can analyze answers if provided
            # insights["cross_summary"] = await self.cross_agent.analyze_answers(user_data, answers)
        except Exception as e:
            insights["cross_questions"] = []
            insights["cross_summary"] = {"error": str(e)}

        # 6️⃣ Gap & final report consolidation
        try:
            insights["final_report"] = await self.gap_agent.generate_final_report(
                socio_summary=insights.get("socio_summary", {}),
                resume_summary=insights.get("resume_summary", {}),
                learning_summary=insights.get("learning_summary", {}),
                aptitude_summary=insights.get("aptitude_summary", {}),
                cross_summary=insights.get("cross_summary", {}),
                personal_info=user.personalInfo.dict() if user.personalInfo else {},
                optional_fields=user.optionalFields.dict() if user.optionalFields else {}
            )
        except Exception as e:
            insights["final_report"] = {"error": str(e)}

        return insights
