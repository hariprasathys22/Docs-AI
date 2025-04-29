# backend/app/services/ingest.py

import uuid
from pathlib import Path
from app.services.converter import extract_text
from app.services.chunker   import chunk_text
from app.services.embedder  import embed_chunks
from app.services.vector_db import upsert_chunks

async def process(file_path: str):
    """
    1) Convert file → raw text
    2) Split text → overlapping chunks
    3) Embed chunks → list of vectors
    4) Upsert into Qdrant with metadata (UUID point IDs)
    """
    fn = Path(file_path).name

    # 1) Extract
    text = extract_text(file_path)

    # 2) Chunk
    chunks = chunk_text(text)  # List[{"text":..., "chunk_idx":...}]

    # 3) Embed
    texts   = [c["text"] for c in chunks]
    vectors = embed_chunks(texts)  # List[List[float]]

    # 4) Build payloads with UUIDs and upsert
    points = []
    for idx, chunk in enumerate(chunks):
        # generate a fresh UUID for this point
        point_id = str(uuid.uuid4())

        payload = {
            "text":      chunk["text"],
            "source":    fn,
            "chunk_idx": idx,
        }

        points.append({
            "id":      point_id,
            "payload": payload,
        })

    await upsert_chunks(points, vectors)
