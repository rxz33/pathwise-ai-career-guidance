# app/services/mongo_service.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["pathwise_db"]
user_collection = db["user_data"]


async def update_user_by_email(email: str, update_data: dict):
    """
    Update a user by email without cleaning.
    """
    if not email:
        raise ValueError("Email is required")

    if any(k.startswith("$") for k in update_data.keys()):
        result = await user_collection.update_one(
            {"personal.email": email},
            update_data,
            upsert=True
        )
    else:
        result = await user_collection.update_one(
            {"personal.email": email},
            {"$set": update_data},
            upsert=True
        )
    return result


async def get_user_by_email(email: str):
    return await user_collection.find_one({"personal.email": email})


async def get_clean_user_data(email: str) -> dict:
    """
    Just fetch merged profile (rawUserInfo + rawResume) without cleaning.
    """
    user = await user_collection.find_one({"personal.email": email})
    if not user:
        return {}

    merged = {
        "email": email,
        "userInfo": user.get("rawUserInfo", {}),
        "resume": user.get("rawResume", {})
    }

    return merged
