from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from typing import List
import hashlib
import math

class LightweightEmbeddings(Embeddings):
    def __init__(self, dim=384):
        self.dim = dim

    def _embed(self, text: str) -> List[float]:
        words = text.lower().split()
        vector = [0.0] * self.dim
        for word in words:
            h = int(hashlib.md5(word.encode()).hexdigest(), 16)
            idx = h % self.dim
            vector[idx] += 1.0
        norm = math.sqrt(sum(x*x for x in vector)) or 1.0
        return [x/norm for x in vector]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed(t) for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._embed(text)

def create_vectorstore(chunks):
    embeddings = LightweightEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore