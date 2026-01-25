from fastapi import APIRouter, HTTPException
from .schemas import ChatRequest, ChatResponse, RetrievedChunk

from src.rag.retrievers import get_flat_retriever, get_hierarchy_retriever
from src.rag.scoped_answer import generate_scoped_answer

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

    if req.mode not in ("flat", "hierarchy"):
        raise HTTPException(status_code=400, detail="mode must be flat or hierarchy")

    retriever = (
        get_flat_retriever()
        if req.mode == "flat"
        else get_hierarchy_retriever()
    )

    docs = retriever.invoke(req.query)

    answer = generate_scoped_answer(req.query, docs)

    chunks = [
        RetrievedChunk(
            content=d.page_content,
            metadata=d.metadata
        )
        for d in docs
    ]

    return ChatResponse(
        answer=answer,
        chunks=chunks
    )
