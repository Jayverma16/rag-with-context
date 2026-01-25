from typing import List, Dict


def parse_markdown(md_text: str) -> List[Dict]:
    document = None
    section = None
    subsection = None
    buffer = []

    nodes = []

    for line in md_text.splitlines():
        line = line.strip()

        if line.startswith("# "):
            document = line[2:]
        elif line.startswith("## "):
            section = line[3:]
            subsection = None
        elif line.startswith("### "):
            subsection = line[4:]
        elif line:
            buffer.append(line)
        else:
            if buffer:
                nodes.append({
                    "document": document,
                    "section": section,
                    "subsection": subsection,
                    "text": " ".join(buffer)
                })
                buffer = []

    if buffer:
        nodes.append({
            "document": document,
            "section": section,
            "subsection": subsection,
            "text": " ".join(buffer)
        })

    return nodes
