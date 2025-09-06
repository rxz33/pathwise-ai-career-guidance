from fastapi import APIRouter, HTTPException
from app.services import mongo_service

router = APIRouter(tags=["Final Analysis"])

@router.get("/get-final-analysis")
async def get_final_analysis(email: str):
    normalized_email = email.strip().lower()
    user = await mongo_service.get_user_by_email(normalized_email)
    
    if not user:
        raise HTTPException(status_code=404, detail=f"No user found for email {normalized_email}")
    
    if "finalAnalysis" not in user or not user["finalAnalysis"]:
        raise HTTPException(status_code=404, detail="Final analysis not found for this user")
    
    return {"finalAnalysis": user["finalAnalysis"]}
