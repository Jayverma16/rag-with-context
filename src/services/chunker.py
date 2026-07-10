from __future__ import annotations


def _normalize(text: str) -> str:
    return " ".join(text.split())


def _window_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    clean = _normalize(text)
    if not clean:
        return []

    chunks = []
    start = 0
    while start < len(clean):
        end = min(start + chunk_size, len(clean))
        chunk = clean[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(clean):
            break
        start = max(end - overlap, start + 1)
    return chunks


def chunk_pages(
    pages: list[dict],
    filename: str,
    chunk_size: int = 800,
    overlap: int = 150,
) -> list[dict]:
    output = []
    chunk_index = 0

    for page in pages:
        page_number = page["page_number"]
        for chunk_text in _window_text(page["text"], chunk_size, overlap):
            context = f"Document: {filename}\nPage: {page_number}\n"
            output.append(
                {
                    "chunk_index": chunk_index,
                    "page_number": page_number,
                    "section": None,
                    "subsection": None,
                    "text": chunk_text,
                    "embedding_text": context + chunk_text,
                }
            )
            chunk_index += 1

    return output
