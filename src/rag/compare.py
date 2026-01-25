from .retrievers import get_flat_retriever, get_hierarchy_retriever

QUERY = "How often should SSL certificates be rotated?"

def print_results(title, docs):
    print(f"\n===== {title} =====\n")
    for i, d in enumerate(docs, 1):
        print(f"[{i}] score=N/A")  # Chroma retriever doesn’t expose scores directly
        print("METADATA:", d.metadata)
        print("CONTENT:")
        print(d.page_content)
        print("-" * 60)

def main():
    flat = get_flat_retriever()
    hier = get_hierarchy_retriever()

    flat_docs = flat.invoke(QUERY)
    hier_docs = hier.invoke(QUERY)


    print_results("FLAT RETRIEVER (❌)", flat_docs)
    print_results("HIERARCHY RETRIEVER (✅)", hier_docs)

if __name__ == "__main__":
    main()
