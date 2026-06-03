import os
from langchain_community.vectorstores import FAISS

BASE_PATH = "vector_store/faiss_index"

def create_vector_store(docs, embeddings):
    return FAISS.from_documents(docs, embeddings)

def save_vector_store(db, session_id):
    path = os.path.join(BASE_PATH, session_id)
    os.makedirs(path, exist_ok=True)
    db.save_local(path)

def load_vector_store(embeddings, session_id):
    path = os.path.join(BASE_PATH, session_id)
    if not os.path.exists(path):
        return None
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)

def merge_vector_stores(db1, db2):
    db1.merge_from(db2)
    return db1