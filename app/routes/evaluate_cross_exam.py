import os
import httpx
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from string import Template
from app.services.mongo_service import get_user_by_email
from app.services.gemini_service import ask_groq
import traceback

router = APIRouter()

class EvaluationRequest(BaseModel):
    email: str
    user_summary: str

@router.post("/evaluate-cross-exam")
async def evaluate_cross_exam(data: EvaluationRequest):
    try:
        user = await get_user_by_email(data.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        full_name = user.get("fullName", "User")

        # Load prompt file
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        prompt_path = os.path.join(BASE_DIR, "app", "prompts", "cross_evaluation_prompt.txt")

        if not os.path.isfile(prompt_path):
            raise HTTPException(status_code=500, detail="Prompt file missing")

        with open(prompt_path, "r", encoding="utf-8") as f:
            raw_prompt = f.read()

        # Ensure summary is a clean string
        summary = data.user_summary.strip() if isinstance(data.user_summary, str) else ""

        # Substitute values
        prompt = Template(raw_prompt).substitute(
            fullName=full_name,
            summary=summary
        )

        print("📨 Cross Eval Prompt:\n", prompt[:300])
        gemini_output = await ask_groq(prompt)
        print("📥 Gemini Output:\n", gemini_output[:300])

        # Forward to generate-results
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post("http://localhost:8000/generate-results", json={
                    "email": data.email,
                    "evaluation": gemini_output
                })
                response.raise_for_status()
            except httpx.HTTPError as http_err:
                print("⚠️ Error calling /generate-results:", http_err)

        return {"evaluation": gemini_output}

    except Exception as e:
        print(f"🔴 Error in evaluate-cross-exam: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")
