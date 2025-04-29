from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class SourceMeta(BaseModel):
    source: str
    chunk_index: str
    score: float

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceMeta]