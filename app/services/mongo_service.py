# app/services/mongo_service.py

from motor.motor_asyncio import AsyncIOMotorClient
import os
from app.database import db  # or your MongoDB connection logic

# Use your actual MongoDB URI here or from environment
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)

db = client["pathwise_db"]  # replace with your actual DB name
user_collection = db["user_data"]  # replace with your actual collection name

async def get_user_by_email(email: str):
    user = await user_collection.find_one({"personal.email": email})
    # TEMP: Add this inside get_user_by_email to print the user
    print("User data:", user)

    return user

async def update_user_by_email(email: str, update_data: dict):
    return await user_collection.update_one({"personal.email": email}, {"$set": update_data})
