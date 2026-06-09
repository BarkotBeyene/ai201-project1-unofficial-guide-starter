# src/chunk.py
# Splits cleaned .txt files into 1200-char chunks with 150-char overlap
# Each chunk: {"text": "...", "source": "filename.txt", "chunk_id": 0}

import os
import json

CLEANED_DIR = "data/cleaned"
CHUNK_SIZE = 1200
OVERLAP = 150


def chunk_text(text, source, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        # Skip empty or near-empty chunks
        if len(chunk) > 50:
            chunks.append({
                "text": chunk,
                "source": source,
                "chunk_id": len(chunks)
            })

        start += chunk_size - overlap

    return chunks


def chunk_all():
    files = [f for f in os.listdir(CLEANED_DIR) if f.endswith('.txt')]

    if not files:
        print(f"No cleaned files found in {CLEANED_DIR}. Run ingest.py first.")
        return []

    all_chunks = []

    for filename in files:
        path = os.path.join(CLEANED_DIR, filename)

        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()

        chunks = chunk_text(text, source=filename)
        all_chunks.extend(chunks)

        print(f"✓ {filename}: {len(chunks)} chunks")

    print(f"\nTotal chunks: {len(all_chunks)}")
    return all_chunks


def inspect_chunks(chunks, n=5):
    print("\n" + "="*60)
    print(f"INSPECTING {n} SAMPLE CHUNKS")
    print("="*60)

    import random
    samples = random.sample(chunks, min(n, len(chunks)))

    for i, chunk in enumerate(samples):
        print(f"\n--- Chunk {i+1} | Source: {chunk['source']} | ID: {chunk['chunk_id']} ---")
        print(chunk['text'])
        print()


if __name__ == "__main__":
    all_chunks = chunk_all()

    if all_chunks:
        inspect_chunks(all_chunks, n=5)

        # Validation check
        print("="*60)
        print("VALIDATION")
        print("="*60)
        if len(all_chunks) < 50:
            print("⚠️  WARNING: Fewer than 50 chunks — chunks may be too large")
        elif len(all_chunks) > 2000:
            print("⚠️  WARNING: More than 2000 chunks — chunks may be too small")
        else:
            print(f"✓ Chunk count ({len(all_chunks)}) is in the healthy range (50–2000)")