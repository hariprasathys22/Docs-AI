from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.config import JWT_SECRET
from app.db.mongo import user_collection
from bson import ObjectId

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("user_id")
        if not user_id:
            raise credentials_exception

        user = await user_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise credentials_exception
        
        user["_id"] = str(user["_id"])  # Optional: make it JSON serializable
        return user

    except (JWTError, ValueError):  # ValueError can catch ObjectId errors
        raise credentials_exception
