from fastapi import APIRouter, HTTPException
from app.schemas.user_data import CrossExamEmail
from app.schemas.cross_exam_response import CrossExamQuestionSet
from app.services.groq_service import ask_groq
from app.database import db
import os

router = APIRouter()

@router.post("/cross-examination", response_model=CrossExamQuestionSet)
async def generate_cross_exam_questions(payload: CrossExamEmail):
    try:
        # 1. Fetch user data from MongoDB
        user_doc = await db.user_data.find_one({"personal.email": payload.email})
        if not user_doc:
            raise HTTPException(status_code=404, detail="User data not found")

        # 2. Extract only essential fields for the prompt
        variables = {
            "fullName": user_doc.get("fullName", "User"),
            "age": user_doc.get("age", "unknown"),
            "currentStatus": user_doc.get("currentStatus", "unknown"),
            "fieldOfStudy": user_doc.get("fieldOfStudy", "unknown"),
            "strengths": user_doc.get("strengths", "N/A"),
            "struggleWith": user_doc.get("struggleWith", "N/A"),
            "confidenceLevel": user_doc.get("confidenceLevel", "unknown"),
            "internshipOrProject": user_doc.get("internshipOrProject", "N/A"),
            "whatDidYouLearn": user_doc.get("whatDidYouLearn", "N/A"),
            "preferredRole": user_doc.get("preferredRole", "N/A"),
            "jobPriorities": ", ".join(user_doc.get("jobPriorities", [])),
            "riskTaking": user_doc.get("riskTaking", "N/A"),
        }

        # 3. Load and format the prompt from cross_prompt.txt
        prompt_path = os.path.join("app", "prompts", "cross_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            template = f.read()
        filled_prompt = template
        for key, value in variables.items():
            filled_prompt = filled_prompt.replace(f"${key}", str(value))

        # 4. Ask Groq
        response = await ask_groq(filled_prompt)
        if response.startswith("❌"):
            raise HTTPException(status_code=500, detail=response)

        # 5. Store and return
        questions = [q.strip() for q in response.split("\n") if q.strip()]
        await db.cross_exam.insert_one({
            "email": payload.email,
            "generated_questions": questions
        })

        return {"questions": questions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
