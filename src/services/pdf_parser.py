from pathlib import Path

import fitz


def parse_pdf_pages(path: str | Path) -> list[dict]:
    pdf_path = Path(path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"{pdf_path} not found")

    pages = []
    with fitz.open(pdf_path) as document:
        for index, page in enumerate(document, start=1):
            text = " ".join(page.get_text("text").split())
            if text:
                pages.append({"page_number": index, "text": text})
    return pages
