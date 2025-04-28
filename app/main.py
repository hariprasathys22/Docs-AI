from fastapi import FastAPI

app = FastAPI(
    title = "Docs AI",
    version = "0.1.0",
    docs_url = "/docs",
    redoc_url = "/redoc"
)

@app.get("/healthz", tags=["health"])
async def health_check(): 
    return { "status": "ok" }   