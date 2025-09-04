# app/routes/user_info.py
from fastapi import APIRouter, Request, HTTPException
from app.services.mongo_service import update_user_by_email

router = APIRouter()

@router.post("/submit-info")
async def submit_user_info(request: Request):
    try:
        data = await request.json()
        email = data.get("personal", {}).get("email")
        if not email:
            raise HTTPException(status_code=422, detail="Email is required")

        # Save raw user info only
        await update_user_by_email(email, {"rawUserInfo": data})

        return {"message": "User info stored successfully", "email": email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
