from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.services.agent_pipeline import AgentPipeline

router = APIRouter()

# ✅ Request model
class PipelineRequest(BaseModel):
    email: EmailStr
    cross_exam_answers: dict

# ✅ Response model (optional, can extend later)
class PipelineResponse(BaseModel):
    results: dict

@router.post("/pipeline/run", response_model=PipelineResponse)
async def run_pipeline(request: PipelineRequest):
    try:
        pipeline = AgentPipeline(email=request.email)
        results = await pipeline.run_pipeline(request.dict())
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
