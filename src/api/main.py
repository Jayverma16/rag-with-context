from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router

app = FastAPI(
    title="RAG Inspector API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 👈 allow frontend
    allow_credentials=True,
    allow_methods=["*"],   # 👈 allow OPTIONS, POST, etc.
    allow_headers=["*"],
)

app.include_router(router)