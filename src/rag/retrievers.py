from .vectorstore import get_vectorstore

def get_flat_retriever(k: int = 4):
    store = get_vectorstore("flat_chunks")
    return store.as_retriever(search_kwargs={"k": k})

def get_hierarchy_retriever(k: int = 4):
    store = get_vectorstore("hierarchy_chunks")
    return store.as_retriever(search_kwargs={"k": k})
