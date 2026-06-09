# src/embed.py
# Embeds all chunks and stores them in ChromaDB with source metadata

from sentence_transformers import SentenceTransformer
import chromadb
import sys
import os
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from chunk import chunk_all

CHROMA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma_db")
COLLECTION_NAME = "unofficial_guide"

def embed_and_store():
    print("Loading chunks...")
    all_chunks = chunk_all()

    if not all_chunks:
        print("No chunks found. Run ingest.py first.")
        return

    print(f"\nLoading embedding model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Delete existing collection to avoid duplicate IDs on re-runs
    try:
        client.delete_collection(COLLECTION_NAME)
        print("Cleared existing collection.")
    except:
        pass

    collection = client.get_or_create_collection(COLLECTION_NAME)

    print(f"\nEmbedding {len(all_chunks)} chunks...")

    # Embed in batches of 100 for speed
    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i + batch_size]
        texts = [c["text"] for c in batch]
        embeddings = model.encode(texts, show_progress_bar=False).tolist()

        collection.add(
            ids=[f"{c['source']}__{c['chunk_id']}" for c in batch],
            embeddings=embeddings,
            documents=texts,
            metadatas=[{"source": c["source"], "chunk_id": c["chunk_id"]} for c in batch]
        )

        print(f"  Stored chunks {i+1}–{min(i+batch_size, len(all_chunks))}")

    print(f"\n✓ Done. {len(all_chunks)} chunks embedded and stored in {CHROMA_PATH}/")
    print(f"  Collection: '{COLLECTION_NAME}'")
    print(f"  Total stored: {collection.count()}")

if __name__ == "__main__":
    embed_and_store()