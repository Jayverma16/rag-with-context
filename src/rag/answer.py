from .llm import get_llm

SYSTEM_PROMPT = """You are a documentation assistant.
Answer the question ONLY using the provided context.
If the context is not relevant, say so clearly.
"""

def generate_answer(query: str, docs):
    llm = get_llm()

    context = "\n\n".join(d.page_content for d in docs)

    prompt = f"""{SYSTEM_PROMPT}

Context:
{context}

Question:
{query}

Answer:
"""

    return llm.invoke(prompt)
