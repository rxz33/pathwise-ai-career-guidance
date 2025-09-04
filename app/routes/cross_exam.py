# app/routes/cross_exam.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.mongo_service import get_user_by_email, update_user_by_email
from app.services.llm_service import call_llm

router = APIRouter()

# ---------- Pydantic schema ----------
class SubmitAnswersPayload(BaseModel):
    email: str
    answers: List[str]

class CrossExamResponse(BaseModel):
    evaluation: dict
    followupQuestions: Optional[List[str]] = []

# ---------- Backend Route ----------
@router.post("/submit-answers", response_model=CrossExamResponse)
async def submit_cross_exam(payload: SubmitAnswersPayload):
    try:
        email = payload.email
        answers = payload.answers

        # 1️⃣ Fetch user data
        user_doc = await get_user_by_email(email)
        if not user_doc:
            raise HTTPException(status_code=404, detail="User not found")

        # 2️⃣ Save answers in MongoDB
        await update_user_by_email(email, {"crossExamAnswers": answers})

        # 3️⃣ Prepare LLM prompt
        # You can refine this prompt based on your cross-exam design
        prompt = f"""
You are a career guidance AI. The user has submitted the following answers to cross-examination questions:
{answers}

User profile data:
{user_doc}

Generate:
1. A detailed evaluation of the user.
2. If needed, 5-6 follow-up questions to verify or refine their responses.

Return JSON only in the format:
{{
  "evaluation": {{...}},
  "followupQuestions": ["question1", "question2", ...]
}}
"""

        # 4️⃣ Call the LLM (choose provider: "gemini" for speed + quality)
        llm_response = await call_llm(provider="gemini", prompt=prompt)

        # 5️⃣ Parse LLM output
        import json
        try:
            result = json.loads(llm_response)
        except Exception:
            # fallback: wrap raw text into evaluation
            result = {"evaluation": {"text": llm_response}, "followupQuestions": []}

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
