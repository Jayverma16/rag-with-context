from pathlib import Path
import shutil

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from src.api.schemas import (
    ChatRequest,
    ChatResponse,
    ChunkResponse,
    DocumentResponse,
    SourceResponse,
    UploadResponse,
)
from src.db.database import get_db
from src.db.models import Chunk, Document
from src.services.ingestion import ingest_document
from src.services.llm import answer_question
from src.services.retriever import retrieve_chunks


router = APIRouter()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def _document_response(document: Document) -> DocumentResponse:
    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        status=document.status,
        created_at=document.created_at,
    )


def _chunk_response(chunk: Chunk) -> ChunkResponse:
    return ChunkResponse(
        id=chunk.id,
        document_id=chunk.document_id,
        chunk_index=chunk.chunk_index,
        page_number=chunk.page_number,
        section=chunk.section,
        subsection=chunk.subsection,
        text=chunk.text,
        embedding_text=chunk.embedding_text,
        qdrant_point_id=chunk.qdrant_point_id,
        created_at=chunk.created_at,
    )


@router.get("/")
def health():
    return {"message": "rag-with-context API is healthy"}


@router.post("/documents/upload", response_model=UploadResponse)
async def upload_documents(
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    created = []
    for file in files:
        if not file.filename:
            continue
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        destination = UPLOAD_DIR / file.filename
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        document = Document(
            filename=file.filename,
            storage_path=str(destination),
            status="uploaded",
        )
        db.add(document)
        created.append(document)

    if not created:
        raise HTTPException(status_code=400, detail="No files uploaded")

    db.commit()
    for document in created:
        db.refresh(document)

    return UploadResponse(documents=[_document_response(document) for document in created])


@router.post("/upload")
async def upload_legacy(file: UploadFile = File(...), db: Session = Depends(get_db)):
    response = await upload_documents([file], db)
    document = response.documents[0]
    return {
        "message": "File uploaded successfully",
        "id": document.id,
        "filename": document.filename,
        "status": document.status,
    }


@router.get("/documents", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).order_by(Document.created_at.desc()).all()
    return [_document_response(document) for document in documents]


@router.post("/documents/{document_id}/ingest", response_model=DocumentResponse)
def ingest_document_endpoint(document_id: str, db: Session = Depends(get_db)):
    try:
        document = ingest_document(db, document_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return _document_response(document)


@router.post("/ingest")
def ingest_legacy(payload: dict, db: Session = Depends(get_db)):
    document_id = payload.get("document_id")
    filename = payload.get("filename")
    if not document_id and filename:
        document = db.query(Document).filter(Document.filename == filename).first()
        document_id = document.id if document else None
    if not document_id:
        raise HTTPException(status_code=400, detail="document_id or filename is required")
    document = ingest_document_endpoint(document_id, db)
    return {"status": "success", "document": document}


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    question = req.resolved_question
    if not question:
        raise HTTPException(status_code=400, detail="question is required")

    retrieved = retrieve_chunks(
        question=question,
        mode=req.mode,
        top_k=req.top_k,
        document_ids=req.document_ids,
    )

    sources = []
    for item in retrieved:
        payload = item["payload"]
        chunk_text = (
            payload.get("embedding_text", "")
            if req.mode == "hierarchy"
            else payload.get("text", "")
        )
        sources.append(
            SourceResponse(
                document_id=payload.get("document_id", ""),
                filename=payload.get("filename", ""),
                page_number=int(payload.get("page_number", 0)),
                section=payload.get("section"),
                subsection=payload.get("subsection"),
                chunk_text=chunk_text,
                score=float(item["score"]),
            )
        )

    answer = answer_question(question, retrieved)
    return ChatResponse(answer=answer, sources=sources, chunks=sources)


@router.get("/documents/{document_id}/chunks", response_model=list[ChunkResponse])
def document_chunks(document_id: str, db: Session = Depends(get_db)):
    chunks = (
        db.query(Chunk)
        .filter(Chunk.document_id == document_id)
        .order_by(Chunk.chunk_index.asc())
        .all()
    )
    return [_chunk_response(chunk) for chunk in chunks]
