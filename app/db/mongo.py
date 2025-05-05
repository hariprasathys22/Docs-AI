from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client["chat_db"]
user_collection = db["users"]
chat_collection = db["chats"]