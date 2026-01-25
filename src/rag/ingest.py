from pathlib import Path
from src.ingestion.markdown_parser import parse_markdown
from src.ingestion.chunkers import flat_chunker, hierarchy_aware_chunker
from .documents import flat_to_documents, hierarchy_to_documents
from .vectorstore import get_vectorstore


def ingest_docs():
    md_text = Path("docs/admin_guide.md").read_text()

    nodes = parse_markdown(md_text)

    # Phase 2 pipelines
    flat_chunks = flat_chunker(nodes)
    hierarchy_chunks = hierarchy_aware_chunker(nodes)

    # Convert to LangChain Documents
    flat_docs = flat_to_documents(flat_chunks)
    hierarchy_docs = hierarchy_to_documents(hierarchy_chunks)

    # Vector stores
    flat_store = get_vectorstore("flat_chunks")
    hierarchy_store = get_vectorstore("hierarchy_chunks")

    # Store embeddings
    flat_store.add_documents(flat_docs)
    hierarchy_store.add_documents(hierarchy_docs)

    print("✅ Ingestion complete")

if __name__ == "__main__":
    ingest_docs()

