import chromadb
import os

KNOWLEDGE_BASE_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base", "loan_policies.txt")
CHROMA_PATH         = os.path.join(os.path.dirname(__file__), "../../chroma_db")
COLLECTION_NAME     = "loan_policies"


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks for better retrieval."""
    words  = text.split()
    chunks = []
    i      = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


def ingest():
    client     = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    with open(KNOWLEDGE_BASE_PATH, "r") as f:
        text = f.read()

    chunks = chunk_text(text)

    # Clear existing docs and re-ingest
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    collection.add(
        documents=chunks,
        ids=[f"policy_chunk_{i}" for i in range(len(chunks))]
    )

    print(f"✅ Ingested {len(chunks)} chunks into ChromaDB collection '{COLLECTION_NAME}'")


if __name__ == "__main__":
    ingest()
