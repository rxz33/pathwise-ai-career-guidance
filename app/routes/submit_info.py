from fastapi import APIRouter, Request, HTTPException
from app.database import db  # Your MongoDB client (Motor)

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

        # Upsert: Insert new or update existing based on email
        result = await db.user_data.update_one(
            {"personal.email": email},
            {"$set": data},
            upsert=True
        )

        print("✅ Data upserted for email:", email)
        return {
            "message": "User information stored successfully",
            "email": email
        }

    except Exception as e:
        print("❌ Backend Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to store user info: {str(e)}")
