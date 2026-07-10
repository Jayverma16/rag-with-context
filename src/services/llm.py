import os

import requests


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.1-8b-instant"
UNKNOWN_ANSWER = "I do not know based on the uploaded documents."


def build_prompt(question: str, sources: list[dict]) -> str:
    context_blocks = []
    for index, source in enumerate(sources, start=1):
        payload = source["payload"]
        context_blocks.append(
            "\n".join(
                [
                    f"[Source {index}]",
                    f"Document: {payload.get('filename', 'Unknown')}",
                    f"Page: {payload.get('page_number', 'Unknown')}",
                    f"Text: {payload.get('text', '')}",
                ]
            )
        )

    context = "\n\n".join(context_blocks)
    return f"""
You are a careful document QA assistant.
Answer only from the provided context.
If the context is insufficient, say exactly: "{UNKNOWN_ANSWER}"
Keep the answer concise.
Mention sources using document name and page number.

Context:
{context}

Question:
{question}
""".strip()


def answer_question(question: str, sources: list[dict]) -> str:
    if not sources:
        return UNKNOWN_ANSWER

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return UNKNOWN_ANSWER

    model = os.getenv("GROQ_MODEL", DEFAULT_MODEL)
    prompt = build_prompt(question, sources)
    response = requests.post(
        GROQ_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
