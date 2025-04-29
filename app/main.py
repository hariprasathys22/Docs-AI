from fastapi import FastAPI
from app.routers.ingest import router as ingest_router
from app.routers.query import router as query_router
app = FastAPI(
    title = "Docs AI",
    version = "0.1.0",
    docs_url = "/docs",
    redoc_url = "/redoc"
)

app.include_router(ingest_router, prefix= "/ingest", tags=["ingestion"])
app.include_router(query_router, prefix="/query", tags=["query"])

@app.get("/healthz", tags=["health"])
async def health_check(): 
    return { "status": "ok" }   