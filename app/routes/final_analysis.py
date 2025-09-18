# app/routes/final_analysis.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services import mongo_service
from app.agents.cross_exam_agent import CrossExamAgent
from app.agents.resume_analyzer import ResumeAnalyzerAgent
from app.agents.interest_assessment_agent import AptitudeInterestAgent
from app.agents.gap_analyzer import GapAnalyzerAgent
from app.agents.recommender import RecommenderAgent
from app.agents.final_analyzer import FinalAnalyzerAgent

router = APIRouter()

# Initialize agents
cross_exam_agent = CrossExamAgent()
resume_agent = ResumeAnalyzerAgent()
aptitude_agent = AptitudeInterestAgent()
gap_agent = GapAnalyzerAgent()
recommender_agent = RecommenderAgent()
final_agent = FinalAnalyzerAgent()


# Pydantic request model
class FinalizeCareerRequest(BaseModel):
    email: str
    resume_text: Optional[str] = None  # optional, if user uploaded resume


@router.post("/finalize-career-path")
async def finalize_career_path(req: FinalizeCareerRequest):
    email = req.email
    resume_text = req.resume_text

    # 1️⃣ Get user data
    user_data = await mongo_service.get_user_by_email(email)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # 2️⃣ Optional: Analyze Resume or run Aptitude/Interest assessment
    if resume_text:
        resume_output = await resume_agent.analyze_resume(user_data, resume_text)
    else:
        resume_output = await aptitude_agent.assess_user(user_data)

    # 3️⃣ Run GapAnalyzerAgent
    gap_report = await gap_agent.detect_gaps(user_data, resume_output)
    await mongo_service.update_user_by_email(email, {"gapReport": gap_report})

    # 4️⃣ Generate career recommendations
    recommendations = await recommender_agent.generate_recommendations(
        user_data, resume_output, gap_report
    )
    await mongo_service.update_user_by_email(email, {"recommendations": recommendations})

    # 5️⃣ Generate final human-friendly report
    final_report = await final_agent.generate_final_report(
        user_data, resume_output, gap_report, recommendations
    )
    await mongo_service.update_final_analysis(email, final_report)

    return {
        "resume_or_aptitude_output": resume_output,
        "gap_report": gap_report,
        "recommendations": recommendations,
        "final_report": final_report,
    }
