from langchain_core.documents import Document


def flat_to_documents(flat_chunks):
    docs = []
    for chunk in flat_chunks:
        docs.append(
            Document(
                page_content=chunk["embedding_text"],
                metadata={
                    **chunk["metadata"],
                    "chunk_type": "flat"
                }
            )
        )
    return docs


def hierarchy_to_documents(hierarchy_chunks):
    docs = []
    for chunk in hierarchy_chunks:
        docs.append(
            Document(
                page_content=chunk["embedding_text"],
                metadata={
                    **chunk["metadata"],
                    "chunk_type": "hierarchy"
                }
            )
        )
    return docs
