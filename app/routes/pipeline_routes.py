from fastapi import APIRouter, Body
from app.services.agent_pipeline import AgentPipeline

router = APIRouter(prefix="/pipeline", tags=["pipeline"])

@router.post("/run")
async def run_pipeline(email: str = Body(...), payload: dict = Body(...)):
    pipeline = AgentPipeline(email)
    results = await pipeline.run_pipeline(payload)
    return {"status": "success", "email": email, "pipeline_results": results}
