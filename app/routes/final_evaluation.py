# app/routes/final_evaluation.py
from fastapi import APIRouter, HTTPException
from app.services import mongo_service, llm_service

router = APIRouter()

@router.post("/final-evaluation")
async def final_evaluation(payload: dict):
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=422, detail="Email is required")

    user_data = await mongo_service.get_user_by_email(email)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Combine all user answers (initial + follow-ups)
    cross_exam = user_data.get("crossExam", {})
    all_answers = cross_exam.get("answers", [])
    followups = cross_exam.get("followupAnswers", [])
    all_answers_combined = all_answers + followups

    # Prepare prompt
    prompt = f"""
    You are an expert career counselor AI. Analyze the user's profile and all answers provided:
    Profile: {user_data}
    Answers: {all_answers_combined}

    1. Identify confirmed strengths and weaknesses
    2. Identify skill gaps
    3. Suggest a personalized learning roadmap
    4. Recommend top 3 career options with reasons

    Return in a structured JSON format:
    {{
        "strengths": [],
        "weaknesses": [],
        "skillGaps": [],
        "learningRoadmap": [],
        "topCareers": []
    }}
    """

    try:
        evaluation = await llm_service.call_llm("gemini", prompt)
        # Optionally parse JSON if returned as string
        import json
        evaluation_json = json.loads(evaluation)
        
        # Save final evaluation to DB
        await mongo_service.update_user_by_email(email, {"careerEvaluation": evaluation_json})

        return {"message": "Career evaluation complete", "evaluation": evaluation_json}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
