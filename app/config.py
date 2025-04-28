from dotenv import load_dotenv
import os 


load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
VECTOR_DIM = 768
COLLECTION_NAME = "documents"