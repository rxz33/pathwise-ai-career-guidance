# routes/analysis.py

from fastapi import APIRouter
from app.services.agentic_orchestrator import AgenticOrchestrator
from pydantic import BaseModel

router = APIRouter()
orchestrator = AgenticOrchestrator()

class UserDataRequest(BaseModel):
    fullName: str
    resume: str

@router.post("/analyze")
async def analyze_user(user_data: UserDataRequest):
    """
    Input: {
      "fullName": "Rashi Gupta",
      "resume": "Your resume text here..."
    }
    """
    return orchestrator.orchestrate(user_data.dict())
