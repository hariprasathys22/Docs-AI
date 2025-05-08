from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from datetime import datetime

from app.models.schemas import QueryRequest,QueryResponse
from app.services.embedder import embed_chunks
from app.services.vector_db import search_chunks
from app.services.generator import call_deepseek
from app.db.mongo import chat_collection
from app.dependencies import get_current_user

from typing import Any
import uuid

router = APIRouter()

@router.post("/chat", response_model = QueryResponse)
async def chat_endpoint(req: QueryRequest, user: dict = Depends(get_current_user), chat_id: str = None):
    user_id = str(user["_id"])
    try: 
        query_vec = embed_chunks([req.query])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error embedding query")
    try: 
        results = await search_chunks(query_vec, top_k=req.top_k)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error searching chunks")
    
    chunk_texts = [result["text"] for result in results]
    try: 
        answer = call_deepseek(req.query, chunk_texts)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error generating answer")
    
    chats = chat_collection
    if not chat_id:
        chat_id = str(uuid.uuid4())
    message_ts = datetime.utcnow()

    user_msg = {
        "user_id": user_id,
        "chat_id": chat_id,
        "role": "query",
        "content": req.query,
        "timestamp": message_ts,
    }
    assistant_msg = {
        "user_id": user_id,
        "chat_id": chat_id,
        "role": "response",
        "content": answer,
        "timestamp": message_ts,
    }
    await chats.insert_many([user_msg, assistant_msg])
    sources = [{
        "source" : result["source"],
        "chunk_idx": str(result["chunk_idx"]),
        "score": result["score"],
    }
    for result in results]
    return QueryResponse(
        answer=answer,
        sources=sources,
    )

