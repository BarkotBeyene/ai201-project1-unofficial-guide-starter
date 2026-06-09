# src/eval.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query import ask
from retrieve import retrieve

questions = [
    "What study techniques does research say are most effective for long-term retention?",
    "What causes procrastination and how can students overcome it?",
    "How do I build a study habit that actually sticks over time?",
    "What does Huberman say about active recall and how it helps with learning?",
    "What productivity system works best for managing a student's time?"
]

for i, q in enumerate(questions, 1):
    print(f"\n{'='*70}")
    print(f"QUESTION {i}: {q}")
    print(f"{'='*70}")

    # Show retrieved chunks
    chunks = retrieve(q, k=5)
    print(f"\n--- TOP 3 RETRIEVED CHUNKS ---")
    for j, c in enumerate(chunks[:3]):
        print(f"\nChunk {j+1} | Distance: {c['distance']} | Source: {c['source']}")
        print(c['text'][:200])

    # Show generated answer
    result = ask(q)
    print(f"\n--- GENERATED ANSWER ---")
    print(result['answer'])
    print(f"\nSources: {result['sources']}")