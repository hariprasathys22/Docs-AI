import lmstudio as lms 
from app.config import EMBED_MODEL_NAME


available = lms.list_downloaded_models("embedding")

meta = next((m for m in available if m.model_key == EMBED_MODEL_NAME), None)

if meta is None:
    raise ValueError(f"❌ No embedding model found with key: '{EMBED_MODEL_NAME}'. Available keys: {[m.model_key for m in available]}")

embed_model = meta.load_new_instance()

def embed_chunks(texts: list[str]) -> list[list[float]]:
    """
    texts: List of text chunks to be embedded.
    """
    return embed_model.embed(texts)