from fastapi import FastAPI

app = FastAPI(
    title="RAG-Based Documentation Assistant API",
    description="API for ingesting company documentation and answering natural language queries.",
    version="0.0.1"
)

@app.get("/health", tags=["Health Check"])
async def health_check():
    """Checks the health of the application."""
    return {"status": "ok", "message": "API is running smoothly!"}

