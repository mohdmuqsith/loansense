import chromadb
import os

CHROMA_PATH     = os.path.join(os.path.dirname(__file__), "../../chroma_db")
COLLECTION_NAME = "loan_policies"


def get_chroma_client() -> chromadb.PersistentClient:
    return chromadb.PersistentClient(path=CHROMA_PATH)


def get_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(name=COLLECTION_NAME)
