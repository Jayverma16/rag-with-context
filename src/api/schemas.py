from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    id: str
    filename: str
    status: str
    created_at: datetime


class UploadResponse(BaseModel):
    documents: list[DocumentResponse]


class ChunkResponse(BaseModel):
    id: str
    document_id: str
    chunk_index: int
    page_number: int
    section: str | None = None
    subsection: str | None = None
    text: str
    embedding_text: str
    qdrant_point_id: str | None = None
    created_at: datetime


class ChatRequest(BaseModel):
    question: str | None = None
    query: str | None = None
    document_ids: list[str] | None = None
    mode: Literal["flat", "hierarchy"] = "hierarchy"
    top_k: int = Field(default=5, ge=1, le=20)

    @property
    def resolved_question(self) -> str:
        value = self.question or self.query or ""
        return value.strip()


class SourceResponse(BaseModel):
    document_id: str
    filename: str
    page_number: int
    section: str | None = None
    subsection: str | None = None
    chunk_text: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]
    chunks: list[SourceResponse] = []
