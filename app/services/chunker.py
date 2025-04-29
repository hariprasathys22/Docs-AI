def chunk_text(text: str, chunk_size: int = 250, overlap: int = 100) -> list[dict]:
    words = text.split()
    chunks = []
    start = 0
    index = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunks.append({"text": " ".join(chunk_words), "chunk_index": index})
        index += 1
        start += chunk_size - overlap
    return chunks