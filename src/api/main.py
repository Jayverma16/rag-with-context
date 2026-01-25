from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="RAG Inspector API",
    description="Hierarchy-aware RAG with debug visibility",
    version="0.1.0"
)

app.include_router(router)
