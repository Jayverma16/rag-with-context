from src.services.embeddings import embed_text
from src.services.vectorstore import get_vectorstore


def retrieve_chunks(
    question: str,
    mode: str = "hierarchy",
    top_k: int = 5,
    document_ids: list[str] | None = None,
) -> list[dict]:
    vector = embed_text(question)
    return get_vectorstore(mode=mode).search(
        query_vector=vector,
        top_k=top_k,
        document_ids=document_ids,
    )
