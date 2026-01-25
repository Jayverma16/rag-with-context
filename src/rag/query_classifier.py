def is_scope_question(query: str) -> bool:
    keywords = [
        "which",
        "does",
        "do",
        "apply",
        "applies",
        "required",
        "require",
        "where",
        "belongs"
    ]
    q = query.lower()
    return any(k in q for k in keywords)
