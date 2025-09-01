# app/routes/user_info.py
from fastapi import APIRouter, Request, HTTPException
from app.services.mongo_service import update_user_by_email  # <-- use your service

router = APIRouter()

@router.post("/submit-info")
async def submit_user_info(request: Request):
    try:
        data = await request.json()
        print("📥 Incoming Data:", data)

        if not data:
            raise HTTPException(status_code=400, detail="No data received")

        email = data.get("personal", {}).get("email")
        if not email:
            raise HTTPException(status_code=422, detail="Email is required inside 'personal' field")

        # 🔒 Use encryption-aware update function
        await update_user_by_email(email, data)

        print("✅ Data upserted (encrypted) for email:", email)
        return {
            "message": "User information stored successfully",
            "email": email
        }

    except Exception as e:
        print("❌ Backend Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to store user info: {str(e)}")
