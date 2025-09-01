# app/services/mongo_service.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["pathwise_db"]
user_collection = db["user_data"]

async def update_user_by_email(email: str, update_data: dict):
    """
    Updates a user by email. Creates a new document if not exists.
    Merges nested objects like tests instead of overwriting them.
    """
    if "personal" not in update_data:
        update_data["personal"] = {}
    update_data["personal"]["email"] = email

    # Prepare $set with nested keys
    set_data = {}
    for key, value in update_data.items():
        if isinstance(value, dict):
            for sub_key, sub_val in value.items():
                set_data[f"{key}.{sub_key}"] = sub_val
        else:
            set_data[key] = value

    return await user_collection.update_one(
        {"personal.email": email},
        {"$set": set_data},
        upsert=True
    )


# async def update_user_by_email(email: str, update_data: dict):
#     """
#     Updates a user by email. If the user doesn't exist, creates a new document.
#     Ensures all test results go under the same document for this email.
#     """
#     # Ensure email is part of the update
#     if "personal" not in update_data:
#         update_data["personal"] = {}
#     update_data["personal"]["email"] = email

#     # Use $set to update only fields in update_data without replacing the whole document
#     result = await user_collection.update_one(
#         {"personal.email": email},
#         {"$set": update_data},
#         upsert=True
#     )
#     return result


async def get_user_by_email(email: str):
    """
    Fetch a user by email.
    """
    user = await user_collection.find_one({"personal.email": email})
    return user
