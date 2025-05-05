from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class ChatEntry(BaseModel):
    user_id: str
    chat_id: str
    role: Literal["query", "response"]
    text: str
    timestamp: datetime