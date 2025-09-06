# app/routes/cross_exam.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.services import mongo_service
from app.agents.cross_exam_agent import CrossExamAgent

router = APIRouter()
agent = CrossExamAgent(llm_provider="gemini")


class SubmitAnswersRequest(BaseModel):
    email: str
    answers: List[str]


@router.post("/generate-questions")
async def generate_questions(payload: Dict):
    """
    Generate 5–6 personalized cross-exam questions for a user.
    """
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=422, detail="Email is required")

    user_data = await mongo_service.get_user_by_email(email)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate questions with agent
    questions = await agent.generate_questions(user_data)

    # Save generated questions in DB
    await mongo_service.save_cross_exam_questions(email, questions)

    return {"questions": questions}


@router.post("/submit-answers")
async def submit_answers(req: SubmitAnswersRequest):
    """
    Receive answers, analyze them, and return either follow-ups or final analysis.
    """
    email = req.email
    answers = req.answers

    user_data = await mongo_service.get_user_by_email(email)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Save answers in DB
    await mongo_service.save_cross_exam_answers(email, answers)

    # Generate analysis from LLM
    analysis = await agent.analyze_answers(user_data, answers)
    await mongo_service.save_cross_exam_analysis(email, analysis)

    # Optionally generate follow-ups
    followup_questions: Optional[List[str]] = []
    if len(answers) < 6:  # Example condition
        followup_questions = await agent.generate_questions(user_data)
        await mongo_service.save_cross_exam_followups(email, followup_questions)

    return {
        "analysis": analysis,
        "followupQuestions": followup_questions
    }
