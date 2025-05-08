from fastapi import FastAPI
from app.routers.ingest import router as ingest_router
# from app.routers.query import router as query_router
from app.routers.chat import router as chat_router
from app.routers.auth import router as auth_router
app = FastAPI(
    title = "Docs AI",
    version = "0.1.0",
    docs_url = "/docs",
    redoc_url = "/redoc"
)

app.include_router(ingest_router, prefix= "/ingest", tags=["ingestion"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

@app.get("/healthz", tags=["health"])
async def health_check(): 
    return { "status": "ok" }   