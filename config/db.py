from pymongo import MongoClient
from decouple import config  # To read environment variables safely
import os

# Replace with your connection string (you can use MongoDB Atlas or local MongoDB)
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

client = MongoClient(MONGODB_URL)

# Create or connect to your database
db = client["pathwise"]
