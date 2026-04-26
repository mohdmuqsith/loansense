import chromadb
import os

CHROMA_PATH     = os.path.join(os.path.dirname(__file__), "../../chroma_db")
COLLECTION_NAME = "loan_policies"


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(name=COLLECTION_NAME)


def retrieve(query: str, n_results: int = 3) -> str:
    """
    Query ChromaDB with a natural language query.
    Returns the top matching policy chunks as a single string.
    """
    collection = get_collection()

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    docs = results.get("documents", [[]])[0]

    if not docs:
        return "No relevant policy found."

    return "\n\n".join(docs)
