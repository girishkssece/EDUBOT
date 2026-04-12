from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def create_vectorstore(chunks):
    # Load HuggingFace embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # Create FAISS vector store from chunks
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore