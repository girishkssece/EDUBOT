from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.embeddings.base import Embeddings
import os
from typing import List

class GroqEmbeddings(Embeddings):
    def __init__(self):
        self.client = ChatGroq(
            model="llama-4-scout-17b-16e-instruct",
            groq_api_key=os.environ.get("GROQ_API_KEY")
        )
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        from groq import Groq
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        embeddings = []
        for text in texts:
            response = client.embeddings.create(
                model="nomic-embed-text-v1_5",
                input=text[:512]
            )
            embeddings.append(response.data[0].embedding)
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]

def create_vectorstore(chunks):
    embeddings = GroqEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore