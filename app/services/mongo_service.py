# app/services/mongo_service.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["pathwise_db"]
user_collection = db["user_data"]

async def update_user_by_email(email: str, update_data: dict):
    """
    Update user document by email.
    """
    result = await user_collection.update_one({"personal.email": email}, {"$set": update_data})
    return result

async def get_user_by_email(email: str):
    """
    Fetch user document by email.
    """
    user = await user_collection.find_one({"personal.email": email})
    return user

async def update_final_analysis(email: str, analysis: dict):
    """
    Store final career analysis under 'finalAnalysis' field.
    """
    result = await user_collection.update_one(
        {"personal.email": email},
        {"$set": {"finalAnalysis": analysis}}
    )
    return result
