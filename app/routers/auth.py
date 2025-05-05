from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from app.models.user_schemas import UserCreate, UserLogin
from app.db.mongo import user_collection
from app.config import JWT_SECRET
import jwt
from datetime import datetime, timedelta

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"])


def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(days=7)
    return jwt.encode(payload, JWT_SECRET, algorithm= "HS256")


@router.post("/signup")
async def signup(user: UserCreate):
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already Exists')

    hashed_password = pwd_context.hash(user.password)
    await user_collection.insert_one({
        "email": user.email, 
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    })
    return {"message": "User created successfully"}

@router.post("/login")
async def login(user: UserLogin):
    user_doc = await user_collection.find_one({"email": user.email})
    if not user_doc:
        raise HTTPException(status_code=400, detail='Invalid email or password')
    
    if not pwd_context.verify(user.password, user_doc["hashed_password"]):
        raise HTTPException(status_code=400, detail='Invalid email or password')
    
    token = create_token({"user_id": str(user_doc["_id"]), "email": user_doc["email"]})
    return {
        "token": token,
    }