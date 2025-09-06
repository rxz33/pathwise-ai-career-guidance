# app/services/mongo_service.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["pathwise_db"]
user_collection = db["user_data"]


# ---------- Generic Helpers ----------

async def update_user_by_email(email: str, update_data: dict, create_if_missing: bool = True):
    """
    Update user document by email with flexible fields.
    Normalizes email and supports upsert (create if not exists).
    """
    normalized_email = email.strip().lower()

    result = await user_collection.update_one(
        {"$or": [{"email": normalized_email}, {"personal.email": normalized_email}]},
        {"$set": update_data, "$setOnInsert": {"email": normalized_email}},
        upsert=create_if_missing
    )

    if result.matched_count == 0 and not result.upserted_id:
        print(f"[MongoDB] ❌ No user found/created for {normalized_email}")
    elif result.upserted_id:
        print(f"[MongoDB] 🆕 Created new user for {normalized_email}")
    else:
        print(f"[MongoDB] ✅ Updated user {normalized_email} with {update_data.keys()}")

    return result


async def get_user_by_email(email: str):
    """
    Fetch full user document by email.
    """
    normalized_email = email.strip().lower()
    user = await user_collection.find_one(
        {"$or": [{"email": normalized_email}, {"personal.email": normalized_email}]}
    )
    if not user:
        print(f"[MongoDB] ❌ No user found with {normalized_email}")
    else:
        print(f"[MongoDB] ✅ Retrieved user {normalized_email}")
    return user


# ---------- Cross Exam Specific Helpers ----------

async def save_cross_exam_questions(email: str, questions: list):
    return await update_user_by_email(email, {"crossExam.questions": questions})


async def save_cross_exam_answers(email: str, answers: list):
    return await update_user_by_email(email, {"crossExam.answers": answers})


async def save_cross_exam_analysis(email: str, analysis: str):
    return await update_user_by_email(email, {"crossExam.analysis": analysis})


async def save_cross_exam_followups(email: str, followups: list):
    return await update_user_by_email(email, {"crossExam.followups": followups})


# ---------- Final Career Analysis ----------

async def update_final_analysis(email: str, analysis: dict):
    normalized_email = email.strip().lower()
    result = await update_user_by_email(normalized_email, {"finalAnalysis": analysis}, create_if_missing=True)
    if result.upserted_id:
        print(f"[MongoDB] 🆕 Created new user and stored finalAnalysis for {normalized_email}")
    else:
        print(f"[MongoDB] ✅ Updated finalAnalysis for {normalized_email}")
    return result
