from .answer import generate_answer
from .query_classifier import is_scope_question

""" 
    This is to solve the probelm of Cross-section aggregation hallucination that is basically it was taking multiple 
    Hirerlinker chunks which is in then get murged and llm giving wrong answer.
"""

def generate_scoped_answer(query, docs):
    """
    If the query is scope-sensitive, answer using only the top-1 chunk.
    Otherwise, allow multi-chunk context.
    """
    if is_scope_question(query):
        docs = docs[:1]  # 🔑 critical fix

    return generate_answer(query, docs)
