from dotenv import load_dotenv
import os 


load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
VECTOR_DIM = 768
COLLECTION_NAME = "documents"
EMBED_MODEL_NAME = os.getenv(
    "EMBED_MODEL_NAME",
    "text-embedding-nomic-embed-text-v11"
)
LMSTUDIO_HOST = os.getenv("LMSTUDIO_HOST", "localhost")
LMSTUDIO_PORT = os.getenv("LMSTUDIO_PORT", "1234")
LM_MODEL_NAME = os.getenv(
    "LM_MODEL_NAME",
    "deepseek-r1-distill-qwen-7b"
)
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://hariprasathys:22Sep2002.@docsai.vdmih1r.mongodb.net/")
JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")