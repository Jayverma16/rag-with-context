from pydantic import BaseModel
from typing import List, Dict

class ChatRequest(BaseModel):
    query: str
    mode: str  # "flat" or "hierarchy"

class RetrievedChunk(BaseModel):
    content: str
    metadata: Dict

class ChatResponse(BaseModel):
    answer: str
    chunks: List[RetrievedChunk]
