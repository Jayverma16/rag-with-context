from pathlib import Path
from src.ingestion.markdown_parser import parse_markdown
from src.ingestion.chunkers import flat_chunker, hierarchy_aware_chunker
from .documents import flat_to_documents, hierarchy_to_documents
from .vectorstore import get_vectorstore

from pathlib import Path

def ingest_docs(file_path: str):
    try:
        # 1️⃣ Read file
        path = Path(file_path)
        if not path.exists():
            return {"status": "error", "message": "File not found"}

        text = path.read_text()

        # 2️⃣ Parse markdown → nodes
        nodes = parse_markdown(text)

        # 3️⃣ Chunking pipelines
        flat_chunks = flat_chunker(nodes)
        hierarchy_chunks = hierarchy_aware_chunker(nodes)

        # 4️⃣ Convert to LangChain Documents
        flat_docs = flat_to_documents(flat_chunks)
        hierarchy_docs = hierarchy_to_documents(hierarchy_chunks)

        # 5️⃣ Vector stores
        flat_store = get_vectorstore("flat_chunks")
        hierarchy_store = get_vectorstore("hierarchy_chunks")

        # 6️⃣ Store embeddings
        flat_store.add_documents(flat_docs)
        hierarchy_store.add_documents(hierarchy_docs)

        return {
            "status": "success",
            "message": "Ingestion complete",
            "flat_chunks": len(flat_docs),
            "hierarchy_chunks": len(hierarchy_docs),
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }

if __name__ == "__main__":
    ingest_docs("/home/jay/Projects/rag-with-context/uploads/war-and-peace.pdf")
    import time
    # time.sleep(10)