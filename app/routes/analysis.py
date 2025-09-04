# routes/analysis.py

from fastapi import APIRouter
from services.agentic_orchestrator import AgenticOrchestrator

router = APIRouter()
orchestrator = AgenticOrchestrator()

@router.post("/analyze")
async def analyze_user(user_data: dict):
    """
    Input: {
      "fullName": "Rashi Gupta",
      "resume": "Your resume text here..."
    }
    """
    return orchestrator.orchestrate(user_data)
