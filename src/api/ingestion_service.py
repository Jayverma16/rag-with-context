from pathlib import Path
from src.rag.ingest import ingest_docs

def ingest_file(file_path: str):
    """
    Ingest a single uploaded file.
    For now, we assume text/markdown.
    Later: PDF support.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"{file_path} not found")

    # 🔑 TEMPORARY DESIGN CHOICE
    # We reuse your existing ingestion logic.
    # Next phase we will make this file-specific.
    ingest_docs()

    return {
        "status": "success",
        "message": f"Ingested {path.name}"
    }
