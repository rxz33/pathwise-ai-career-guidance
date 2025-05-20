from fastapi import APIRouter, HTTPException
from app.services.mongo_service import get_user_by_email 

router = APIRouter()

@router.get("/get-final-analysis")
async def get_final_analysis(email: str):
    user = await get_user_by_email(email)
    if not user or "finalAnalysis" not in user:
        raise HTTPException(status_code=404, detail="Final analysis not found")
    
    return {"finalAnalysis": user["finalAnalysis"]}
