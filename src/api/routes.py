from fastapi import APIRouter, HTTPException
from .schemas import ChatRequest, ChatResponse, RetrievedChunk

from src.rag.retrievers import get_flat_retriever, get_hierarchy_retriever
from src.rag.scoped_answer import generate_scoped_answer
from fastapi import UploadFile, File
from pathlib import Path
import shutil

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

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        return {"error": "No file uploaded"}

    # basic validation
    allowed_ext = (".pdf", ".txt", ".md")
    if not file.filename.lower().endswith(allowed_ext):
        return {"error": "Unsupported file type"}

    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "path": str(file_path)
    }

from pydantic import BaseModel
from src.api.ingestion_service import ingest_file

class IngestRequest(BaseModel):
    filename: str


@router.post("/ingest")
def ingest(req: IngestRequest):
    file_path = f"uploads/{req.filename}"

    try:
        result = ingest_file(file_path)
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }