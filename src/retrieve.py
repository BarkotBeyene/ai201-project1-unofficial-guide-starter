# src/retrieve.py
# Retrieval function: takes a query, returns top-k relevant chunks with source + distance

from sentence_transformers import SentenceTransformer
import chromadb
import os
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1"

CHROMA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma_db")
COLLECTION_NAME = "unofficial_guide"

# Load model and collection once at module level
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(COLLECTION_NAME)


def retrieve(query, k=5):
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=k)

    return [
        {
            "text": doc,
            "source": meta["source"],
            "chunk_id": meta["chunk_id"],
            "distance": round(dist, 4)
        }
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )
    ]


def test_retrieval():
    # Your 3 evaluation questions
    test_queries = [
        "What study techniques does research say are most effective for long-term retention?",
        "What causes procrastination and how can students overcome it?",
        "How do I build a study habit that actually sticks over time?"
    ]

    for query in test_queries:
        print("\n" + "="*70)
        print(f"QUERY: {query}")
        print("="*70)

        results = retrieve(query, k=5)

        for i, r in enumerate(results):
            print(f"\n  Result {i+1} | Distance: {r['distance']} | Source: {r['source']}")
            print(f"  {r['text'][:300]}...")

        # Flag weak matches
        top_distance = results[0]["distance"]
        if top_distance > 0.5:
            print(f"\n  ⚠️  WARNING: Top result distance {top_distance} is above 0.5 — retrieval may be weak")
        else:
            print(f"\n  ✓ Top result distance {top_distance} is in the healthy range (below 0.5)")


if __name__ == "__main__":
    test_retrieval()