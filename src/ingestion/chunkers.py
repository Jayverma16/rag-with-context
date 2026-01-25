from typing import List, Dict


def flat_chunker(nodes: List[Dict]) -> List[Dict]:
    """
    Simulates standard flat chunking used by most RAG tools.
    """
    chunks = []

    for node in nodes:
        chunks.append({
            "embedding_text": node["text"],
            "metadata": {
                "document": node["document"]
            }
        })

    return chunks


def hierarchy_aware_chunker(nodes: List[Dict]) -> List[Dict]:
    """
    Hierarchy-aware chunking using contextual prefixing.
    """
    chunks = []

    for node in nodes:
        prefix = f"Document: {node['document']}\n"

        if node["section"]:
            prefix += f"Section: {node['section']}"
        if node["subsection"]:
            prefix += f" > {node['subsection']}"
        prefix += "\n"

        chunks.append({
            "embedding_text": prefix + node["text"],
            "metadata": {
                "document": node["document"],
                "section": f"{node['section']} > {node['subsection']}"
            }
        })

    return chunks
