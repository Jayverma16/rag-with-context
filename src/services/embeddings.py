import os
from functools import lru_cache

from sentence_transformers import SentenceTransformer


EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL)


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    vectors = get_embedding_model().encode(texts, normalize_embeddings=True)
    return [vector.tolist() for vector in vectors]


def embed_text(text: str) -> list[float]:
    return embed_texts([text])[0]


def embedding_dimension() -> int:
    return len(embed_text("dimension probe"))
