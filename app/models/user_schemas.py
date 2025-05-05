from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    id: str = Field(..., alias="_id")
    email: EmailStr
    hashed_password: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)