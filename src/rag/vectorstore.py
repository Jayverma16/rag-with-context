from langchain_chroma import Chroma
from .embeddings import get_embeddings

CHROMA_DIR = "chroma_db"

def get_vectorstore(collection_name: str):
    return Chroma(
        collection_name=collection_name,
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_DIR
    )
