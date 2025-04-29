from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from app.config import QDRANT_URL, COLLECTION_NAME, VECTOR_DIM, QDRANT_API_KEY


client = QdrantClient(
    url = QDRANT_URL,
    api_key= QDRANT_API_KEY or None
)

client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=rest.VectorParams(
        size=VECTOR_DIM,
        distance=rest.Distance.COSINE,
    ),
)

async def upsert_chunks(chunks: list[dict], vectors: list[list[float]]):
    """
    chunks: List of metadata dicts, e.g. [{"id": cid, "payload": {"text": "...", "source": "file.pdf", "chunk": 3}}, ...]
    vectors: List of same‐length embedding vectors.
    """
    points = [ 
        rest.PointStruct(
            id = chunk["id"],
            vector = vectors[i],
            payload = chunk["payload"], 
        )
        for i, chunk in enumerate(chunks)
    ]
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

async def search_chunks(query_vector: list[float], top_k: int = 5):
    """
    query_vector: The embedding vector of the query.
    top_k: The number of nearest neighbors to return.
    """
    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
    )
    print(search_result)
    return [
        {
            "id": p.id,
            "score": p.score,
            **p.payload,
        }
        for p in search_result
    ]
