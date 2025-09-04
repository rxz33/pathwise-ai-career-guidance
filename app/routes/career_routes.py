from fastapi import APIRouter
from services.agent_pipeline import run_pipeline

router = APIRouter()

@router.post("/analyze-career")
async def analyze_career(user_data: dict):
    result = await run_pipeline(user_data)
    return result
