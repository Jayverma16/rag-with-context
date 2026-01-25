from .retrievers import get_flat_retriever, get_hierarchy_retriever
from .answer import generate_answer

QUERY = "How often should SSL certificates be rotated?"
QUERY = "Does SSL certificate rotation apply to OAuth authentication?"
QUERY = "Is certificate rotation required for OAuth tokens?"
QUERY = "Which security components require certificate rotation?"


def main():
    flat = get_flat_retriever()
    hier = get_hierarchy_retriever()
    print(f"QUERY IS : {QUERY} ")
    flat_docs = flat.invoke(QUERY)
    hier_docs = hier.invoke(QUERY)

    print("\n================ FLAT ANSWER (❌) ================\n")
    flat_answer = generate_answer(QUERY, flat_docs)
    print(flat_answer)

    print("\n============= HIERARCHY ANSWER (✅) ==============\n")
    hier_answer = generate_answer(QUERY, hier_docs)
    print(hier_answer)

if __name__ == "__main__":
    main()
