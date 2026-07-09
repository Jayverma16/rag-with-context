# rag-with-context

`rag-with-context` is a multi-document PDF QA app focused on a common RAG failure mode: chunks retrieved from different sections can be aggregated without enough document context, causing answers that sound plausible but mix incompatible facts.

The project keeps the original flat-vs-hierarchy retrieval idea and upgrades it into a hosted-ready stack: FastAPI, React/Vite, PyMuPDF PDF parsing, sentence-transformer embeddings, Qdrant vector search, PostgreSQL metadata, and Groq Llama chat completions.

## Why Context-Aware Chunking

Normal flat chunking embeds only the local text. That can work for simple lookup, but it loses section, page, and document context. This app stores original chunk text and a richer `embedding_text` version that includes document/page context, so hierarchy mode can retrieve passages with more grounding.

## Architecture

```text
React/Vite UI
  -> FastAPI routes
    -> uploads/ local file storage
    -> PyMuPDF page parser
    -> character chunker with overlap
    -> sentence-transformers embeddings
    -> Qdrant vectors with payload citations
    -> PostgreSQL documents/chunks/messages metadata
    -> Groq Llama grounded answer generation
```

## Features

- Upload multiple PDFs.
- Ingest each document into page-aware chunks.
- Ask questions across all ready documents or selected documents.
- Choose `flat` or `hierarchy` retrieval mode.
- Return grounded answers with filename and page citations.
- Inspect retrieved source chunks and stored chunks for debugging.

## Environment

```bash
GROQ_API_KEY=your_groq_key
GROQ_MODEL=llama-3.1-8b-instant
DATABASE_URL=postgresql+psycopg://rag:rag@localhost:5432/rag_with_context
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=rag_with_context_chunks
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

## Run With Docker

```bash
docker compose up --build
```

Services:

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- PostgreSQL: `localhost:5432`
- Qdrant: `http://localhost:6333`

## Run Locally

Start Postgres and Qdrant, then:

```bash
pip install -r requirement.txt
uvicorn src.api.main:app --reload
```

Frontend:

```bash
cd gui/frontend
npm install
npm run dev
```

## API Examples

Upload PDFs:

```bash
curl -X POST http://localhost:8000/documents/upload \
  -F "files=@paper.pdf" \
  -F "files=@manual.pdf"
```

List documents:

```bash
curl http://localhost:8000/documents
```

Ingest a document:

```bash
curl -X POST http://localhost:8000/documents/<document_id>/ingest
```

Chat:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What does the document say about access controls?",
    "document_ids": ["<document_id>"],
    "mode": "hierarchy",
    "top_k": 5
  }'
```

Inspect chunks:

```bash
curl http://localhost:8000/documents/<document_id>/chunks
```

## Future Work

- Hybrid keyword and vector search.
- Reranking.
- MinIO/S3-compatible file storage.
- Background ingestion jobs.
- Streaming chat responses.
- Authentication and per-user document collections.
