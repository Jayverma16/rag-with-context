from sqlalchemy.orm import Session

from src.db.models import Chunk, Document
from src.services.chunker import chunk_pages
from src.services.embeddings import embed_texts, embedding_dimension
from src.services.pdf_parser import parse_pdf_pages
from src.services.vectorstore import get_vectorstore


def ingest_document(db: Session, document_id: str) -> Document:
    document = db.get(Document, document_id)
    if document is None:
        raise ValueError(f"Document {document_id} not found")

    document.status = "processing"
    db.query(Chunk).filter(Chunk.document_id == document_id).delete()
    db.commit()

    try:
        pages = parse_pdf_pages(document.storage_path)
        chunks = chunk_pages(pages, filename=document.filename)
        if not chunks:
            raise ValueError("No text could be extracted from the PDF")

        vector_chunks = []
        for chunk in chunks:
            payload = {
                "document_id": document.id,
                "filename": document.filename,
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
                "section": chunk["section"],
                "subsection": chunk["subsection"],
                "text": chunk["text"],
                "embedding_text": chunk["embedding_text"],
            }
            vector_chunks.append({"payload": payload})

        vector_size = embedding_dimension()
        flat_store = get_vectorstore(mode="flat")
        hierarchy_store = get_vectorstore(mode="hierarchy")
        flat_store.ensure_collection(vector_size)
        hierarchy_store.ensure_collection(vector_size)

        flat_vectors = embed_texts([chunk["text"] for chunk in chunks])
        hierarchy_vectors = embed_texts([chunk["embedding_text"] for chunk in chunks])
        flat_store.upsert_chunks(vector_chunks, flat_vectors)
        point_ids = hierarchy_store.upsert_chunks(vector_chunks, hierarchy_vectors)
        for chunk, point_id in zip(chunks, point_ids, strict=True):
            db.add(
                Chunk(
                    document_id=document.id,
                    chunk_index=chunk["chunk_index"],
                    page_number=chunk["page_number"],
                    section=chunk["section"],
                    subsection=chunk["subsection"],
                    text=chunk["text"],
                    embedding_text=chunk["embedding_text"],
                    qdrant_point_id=point_id,
                )
            )

        document.status = "ready"
        db.commit()
        db.refresh(document)
        return document
    except Exception:
        document.status = "failed"
        db.commit()
        raise
