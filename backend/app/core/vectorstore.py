import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./data/faiss_index")

def get_embeddings():
    """Configure and return the OpenAI Embeddings model."""
    return OpenAIEmbeddings(model="text-embedding-3-small")

def get_vector_store() -> FAISS | None:
    """
    Load the FAISS index from disk. 
    Returns None if the index hasn't been created yet.
    """
    embeddings = get_embeddings()
    if os.path.exists(VECTOR_STORE_PATH):
        return FAISS.load_local(
            folder_path=VECTOR_STORE_PATH, 
            embeddings=embeddings, 
            allow_dangerous_deserialization=True # Local known source
        )
    return None

def create_and_save_vector_store(documents: list[Document]):
    """Creates a new FAISS index from documents and saves to disk."""
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(documents, embeddings)
    
    os.makedirs(os.path.dirname(VECTOR_STORE_PATH), exist_ok=True)
    vector_store.save_local(VECTOR_STORE_PATH)
    return vector_store

def search_documents(query: str, k: int = 2) -> str:
    """
    Search the local FAISS DB for top-k closest matches.
    Returns concatenated content as a single string context.
    """
    store = get_vector_store()
    if not store:
        return "No knowledge base documents found. The FAISS database has not been initialized."
        
    results = store.similarity_search(query, k=k)
    
    # Extract only the content
    context = "\n\n".join([doc.page_content for doc in results])
    return context
