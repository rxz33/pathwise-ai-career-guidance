# app/routes/cross_exam.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from app.services import mongo_service
from app.agents.cross_exam_agent import CrossExamAgent
import json
import re

router = APIRouter()
agent = CrossExamAgent(llm_provider="gemini", max_followup_rounds=2)


class SubmitAnswersRequest(BaseModel):
    email: str
    answers: List[str]
    round_number: Optional[int] = 1  # track which round of follow-ups


def safe_json_parse(text: str) -> Dict[str, Any]:
    """
    Safely extract and parse JSON from LLM output.
    If parsing fails, return fallback structure.
    """
    if not text or not text.strip():
        return {
            "accuracy": 0.0,
            "strengths": [],
            "weaknesses": [],
            "gaps": [],
            "summary": "Empty response from AI"
        }

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try extracting JSON inside text
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        # If parsing fails, return fallback
        return {
            "accuracy": 0.0,
            "strengths": [],
            "weaknesses": [],
            "gaps": [],
            "summary": f"Invalid JSON received: {text[:200]}"
        }


def safe_list_parse(obj) -> List[str]:
    """
    Ensure response is parsed into a list of strings.
    Handles both string (JSON) and list inputs.
    """
    if not obj:
        return []

    # If already a list
    if isinstance(obj, list):
        return [str(item).strip() for item in obj if str(item).strip()]

    # If string, try parsing JSON
    if isinstance(obj, str):
        if not obj.strip():
            return []
        try:
            data = json.loads(obj)
            if isinstance(data, list):
                return [str(item).strip() for item in data if str(item).strip()]
        except json.JSONDecodeError:
            # Try extracting list from text
            import re
            match = re.search(r"\[.*\]", obj, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group())
                    if isinstance(data, list):
                        return [str(item).strip() for item in data if str(item).strip()]
                except json.JSONDecodeError:
                    pass
        # If still fails, return empty
        return []

    # Fallback: convert to string
    return [str(obj).strip()] if str(obj).strip() else []



@router.post("/generate-questions")
async def generate_questions(payload: Dict[str, Any]):
    """
    Generate 5–6 personalized cross-exam questions for a user.
    """
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=422, detail="Email is required")

    user_data = await mongo_service.get_user_by_email(email)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate questions using the agent
    raw_questions = await agent.generate_questions(user_data)
    questions = safe_list_parse(raw_questions)

    # Save generated questions in DB
    await mongo_service.save_cross_exam_questions(email, questions)

    return {"questions": questions}


@router.post("/submit-answers")
async def submit_answers(req: SubmitAnswersRequest):
    """
    Receive answers, analyze them, and return follow-ups or final analysis.
    """
    email = req.email
    answers = req.answers
    round_number = req.round_number or 1

    user_data = await mongo_service.get_user_by_email(email)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Save user answers
    await mongo_service.save_cross_exam_answers(email, answers)

    # Analyze answers (safe JSON parsing)
    raw_analysis = await agent.analyze_answers(user_data, answers)
    analysis = safe_json_parse(raw_analysis)
    await mongo_service.save_cross_exam_analysis(email, analysis)

    # Generate follow-up questions if needed
    followup_questions: List[str] = []
    if round_number <= agent.max_followup_rounds:
        raw_followups = await agent.generate_followups(user_data, answers, round_number)
        followup_questions = safe_list_parse(raw_followups)

        if followup_questions:
            await mongo_service.save_cross_exam_followups(email, followup_questions)

    return {
        "analysis": analysis,
        "followupQuestions": followup_questions
    }
