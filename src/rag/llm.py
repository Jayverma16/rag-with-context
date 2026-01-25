from langchain_ollama import OllamaLLM

def get_llm():
    return OllamaLLM(
        model="llama3:8b",
        base_url="http://localhost:11434",
        temperature=0
    )
