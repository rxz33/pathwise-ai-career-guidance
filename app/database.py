# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["pathwise_db"]  # Your main database

# Ensure index on email inside "personal" field
async def create_indexes():
    await db.user_data.create_index("personal.email", unique=True)
