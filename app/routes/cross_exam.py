from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
from app.services import mongo_service
from app.agents.cross_exam_agent import CrossExamAgent

router = APIRouter()
agent = CrossExamAgent(provider="groq")  # single-round only

# ---------------- Pydantic Models ----------------
class GenerateQuestionsRequest(BaseModel):
    email: EmailStr

class SubmitAnswersRequest(BaseModel):
    email: EmailStr
    answers: List[str]

# ---------------- Routes ----------------
@router.post("/generate-questions")
async def generate_questions(payload: GenerateQuestionsRequest):
    email = payload.email

    # Fetch user data
    user_data = await mongo_service.get_user_by_email(email)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate AI-based critical questions (5–6 questions)
    questions = await agent.generate_questions(user_data)
    questions = [q.strip() for q in questions if q.strip()]

    # Ensure we have at least 5 questions, max 6
    if len(questions) < 5:
        raise HTTPException(status_code=500, detail="Failed to generate enough questions")
    questions = questions[:6]

    # Save questions to user document (single round)
    await mongo_service.update_user_by_email(email, {
        "aiInsights.partials.crossExam.questions": questions
    })

    return {"questions": questions}

@router.post("/submit-answers")
async def submit_answers(req: SubmitAnswersRequest):
    email = req.email
    answers = req.answers

    # Fetch user
    user_data = await mongo_service.get_user_by_email(email)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Save answers only (analysis can be done in next step)
    await mongo_service.update_user_by_email(email, {
        "aiInsights.partials.crossExam.answers": answers
    })

    return {"message": "Answers submitted successfully"}
