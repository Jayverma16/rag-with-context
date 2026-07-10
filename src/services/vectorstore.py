import os
import uuid
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchAny,
    PointStruct,
    VectorParams,
)


QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "rag_with_context_chunks")


class VectorStore:
    def __init__(
        self,
        url: str = QDRANT_URL,
        collection_name: str = QDRANT_COLLECTION,
        mode: str = "hierarchy",
    ):
        self.client = QdrantClient(url=url)
        suffix = "flat" if mode == "flat" else "hierarchy"
        self.collection_name = f"{collection_name}_{suffix}"

    def ensure_collection(self, vector_size: int) -> None:
        collections = self.client.get_collections().collections
        exists = any(item.name == self.collection_name for item in collections)
        if exists:
            return
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

    def upsert_chunks(self, chunks: list[dict], vectors: list[list[float]]) -> list[str]:
        point_ids = [str(uuid.uuid4()) for _ in chunks]
        points = []
        for point_id, chunk, vector in zip(point_ids, chunks, vectors, strict=True):
            points.append(PointStruct(id=point_id, vector=vector, payload=chunk["payload"]))
        self.client.upsert(collection_name=self.collection_name, points=points)
        return point_ids

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
        document_ids: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        qdrant_filter = None
        if document_ids:
            qdrant_filter = Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchAny(any=document_ids),
                    )
                ]
            )

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=qdrant_filter,
            limit=top_k,
            with_payload=True,
        )
        return [
            {
                "score": result.score,
                "payload": result.payload or {},
                "point_id": str(result.id),
            }
            for result in results
        ]


def get_vectorstore(mode: str = "hierarchy") -> VectorStore:
    return VectorStore(mode=mode)
