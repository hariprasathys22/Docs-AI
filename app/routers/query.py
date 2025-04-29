from fastapi import APIRouter, HTTPException
from typing import List

from app.models.schemas import QueryRequest, QueryResponse
from app.services.embedder import embed_chunks
from app.services.vector_db import search_chunks
from app.services.generator import call_deepseek

router = APIRouter()

@router.post("/", response_model = QueryResponse, summary="Ask a question over ingested docs")
async def query(req: QueryRequest):
    try:
        query_vec = embed_chunks([ req.query ])[0]
    except Exception as e:  
        raise HTTPException(status_code=500, detail=f"Error embedding query: {e}")
    
    try:
        results = await search_chunks(query_vec, top_k=req.top_k)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching vector DB: {e}")
    
    chunk_texts = [result["text"] for result in results]

    try: 
        answer = await call_deepseek(req.query, chunk_texts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {e}")
    
    sources = [
        {
            "source": result["source"],
            "chunk_index": str(result["chunk_idx"]),
            "score": result["score"],
        }
        for result in results
    ]
    return QueryResponse(answer=answer, sources=sources)