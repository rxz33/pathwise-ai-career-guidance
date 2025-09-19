# app/routes/career_result.py
from fastapi import APIRouter, HTTPException, Query
from app.services import mongo_service

router = APIRouter()

@router.get("/get-final-analysis")
async def get_final_analysis(email: str = Query(..., description="User email")):
    """
    Fetch the final analysis text for a given email.
    """
    user = await mongo_service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    final_analysis = user.get("finalAnalysis")  # Make sure this field exists in your DB
    if not final_analysis:
        raise HTTPException(status_code=404, detail="Final analysis not found")

    return {"finalAnalysis": final_analysis}
