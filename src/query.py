# src/query.py
# Grounded generation: retrieves chunks and sends to Groq LLM with strict grounding prompt

import os
import sys
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from retrieve import retrieve

client = Groq(api_key=os.environ["GROQ_API_KEY"])


def ask(question):
    # Retrieve top-5 relevant chunks
    chunks = retrieve(question, k=5)

    if not chunks:
        return {
            "answer": "I don't have enough information on that.",
            "sources": []
        }

    # Build context block with source labels
    context = "\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}"
        for c in chunks
    )

    # Deduplicated source list (programmatically guaranteed)
    sources = list(dict.fromkeys(c["source"] for c in chunks))

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a student effectiveness assistant. "
                    "Answer the user's question using ONLY the information in the provided documents. "
                    "Do not use any outside knowledge. "
                    "If the documents do not contain enough information to answer the question, "
                    "say exactly: 'I don't have enough information on that.' "
                    "Always cite the specific document(s) your answer draws from by name."
                )
            },
            {
                "role": "user",
                "content": f"Documents:\n{context}\n\nQuestion: {question}"
            }
        ]
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": sources
    }


if __name__ == "__main__":
    # Quick end-to-end test
    test_questions = [
        "What causes procrastination and how can students overcome it?",
        "What study techniques does research say are most effective for long-term retention?",
        "What is the best way to cook pasta?",  # out-of-scope — should decline
    ]

    for q in test_questions:
        print("\n" + "="*60)
        print(f"Q: {q}")
        print("="*60)
        result = ask(q)
        print(f"A: {result['answer']}")
        print(f"\nSources: {result['sources']}")