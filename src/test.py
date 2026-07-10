from langchain_community.embeddings import OllamaEmbeddings 
embeddings=(
    OllamaEmbeddings(model="nomic-embed-text")  ##by default it ues llama2
)
embeddings
r1=embeddings.embed_documents(
    [
       "Alpha is the first letter of Greek alphabet",
       "Beta is the second letter of Greek alphabet", 
    ]
)
# print(r1[1])
# print(embeddings.embed_query("What is the second letter of Greek alphabet "))
import time 
time.sleep(15)


from langchain_core.prompts import ChatPromptTemplate

prompt=ChatPromptTemplate.from_template(
    """
Answer the following question based only on the provided context:
<context>
{context}
</context>


"""
)

document_chain=create_stuff_documents_chain(llm,prompt)
document_chain