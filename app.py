# app.py
# Gradio UI for the Student Effectiveness Unofficial Guide RAG system

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

import gradio as gr
from query import ask


def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="The Student Effectiveness Guide") as demo:
    gr.Markdown("## 📚 The Student Effectiveness Unofficial Guide")
    gr.Markdown(
        "Ask questions about study techniques, habits, procrastination, and productivity. "
        "Answers are grounded in research papers, podcast transcripts, and expert blogs."
    )

    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. What study techniques are most effective for long-term retention?",
        lines=2
    )

    btn = gr.Button("Ask", variant="primary")

    answer = gr.Textbox(label="Answer", lines=10)
    sources = gr.Textbox(label="Retrieved from", lines=5)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()