# app/routes/cross_exam.py
from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.services import mongo_service
from app.services.llm_service import call_llm

router = APIRouter()

@router.post("/submit-answers")
async def submit_answers(payload: dict):
    """
    Store user answers and generate final analysis using AI.
    """
    email = payload.get("email")
    user_summary = payload.get("user_summary")

    if not email or not user_summary:
        raise HTTPException(status_code=400, detail="Missing email or summary")

    try:
        # 1️⃣ Call AI to generate final career analysis
        final_analysis_text = await call_llm(
            provider="gemini",  # or your preferred LLM
            prompt=f"Analyze this user summary and provide a detailed career analysis:\n{user_summary}"
        )

        final_analysis = {
            "text": final_analysis_text,
            "generated_at": str(datetime.utcnow())
        }

        # 2️⃣ Store final analysis in MongoDB
        await mongo_service.update_final_analysis(email, final_analysis)

        return {"message": "Answers submitted and final analysis stored", "finalAnalysis": final_analysis}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
