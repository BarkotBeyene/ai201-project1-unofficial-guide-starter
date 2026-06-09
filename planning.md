# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

This system covers student effectiveness — the practical knowledge of how to study, build habits, maintain focus, and overcome procrastination. The sources span academic research, podcast transcripts, and personal essays, capturing both the science and the lived experience of high-performance learning. This knowledge is hard to find otherwise because it's scattered across dozens of blogs, papers, and transcripts with no single place to ask a plain-language question and get a grounded, cited answer drawn from all of them at once.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Becoming_a_Self_Regulated_Learner_Overview_by_Zimmerman.txt | Academic paper | Self-regulation strategies students use to plan, monitor, and evaluate their learning |
| 2 | Evidence_Based_Study_Strategies_Overview_by_The_Learning_Scientists.txt | Blog/Article | Practical breakdown of 6 evidence-based study strategies (spaced practice, retrieval practice, etc.) |
| 3 | How_to_Build_New_Habits_by_Taking_Advantage_of_Old_Ones_written_by_James_Clear.txt | Blog/Article | Habit stacking — attaching new behaviors to existing routines |
| 4 | How_to_Study_and_Learn_Huberman_Lab_Transcript.txt | Podcast transcript | Neuroscience of focus, alertness, and memory consolidation for learning |
| 5 | Improving_Students_Learning_With_Effective_Study_Techniques_by_Dunlosky_et_al.txt | Academic paper | Large-scale review of 10 study techniques ranked by effectiveness |
| 6 | Productivity_Methods_Overview_GTD_Time_Blocking_Pomodoro_by_Todoist.txt | Blog/Article | Overview of GTD, time blocking, Pomodoro, and Eat the Frog methods |
| 7 | The_Nature_of_Procrastination_Meta_Analysis_by_Piers_Steel.txt | Academic paper | Meta-analysis of procrastination causes, correlates, and interventions |
| 8 | The_Power_of_Testing_Memory_by_Roediger_and_Karpicke.txt | Academic paper | Foundational research on the testing effect and active recall |
| 9 | Why_learning_how_to_learn_is_the_skill_behind_all_skills_Anne_Laure_LeCunff.txt | Blog/Article | Metalearning — understanding how your own learning works |
| 10 | Why_Procrastinators_Procrastinate_by_Tim_Urban_Wait_But_Why.txt | Blog/Article | Long-form essay on the psychology of procrastination |
---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

My documents are a mix of long-form essays, academic papers, and podcast
transcripts — all multi-paragraph, substantive texts. None of them are short
reviews. This means:

**Chunk size: 500 characters** — large enough to carry a complete thought
  (a full argument, finding, or recommendation) but small enough to match a
  specific query precisely.

**Overlap: 75 characters** — ensures that sentences split across chunk
  boundaries are still retrievable from either side. Without overlap, a key
  sentence sitting at the boundary of two chunks could be missed entirely.

**Reasoning:**
My documents are long-form essays, academic papers, and podcast transcripts —
all multi-paragraph, substantive texts. A 500-character chunk is large enough
to carry a complete thought (a full argument, finding, or recommendation) but
small enough to match a specific query precisely.

Smaller chunks (e.g. 200 chars) would often contain only half a claim — not
enough semantic content for the embedding model to match it to a query. Larger
chunks (e.g. 1000 chars) risk mixing unrelated topics in one chunk, diluting
retrieval precision.

The 75-character overlap ensures sentences sitting at a chunk boundary are
still retrievable from either side. Without overlap, a key finding split across
two chunks could be missed entirely.

Expected chunk count: 10 documents × ~2,000–5,000 chars each ≈ 100–300 chunks
total, well within the healthy 50–2,000 range.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers
Runs fully locally — no API key, no rate limits, no cost. Produces
384-dimensional embeddings, fast on CPU, well-suited for English
paragraph-length text.

**Top-k:** 5 chunks per query
5 gives the LLM enough context to synthesize an answer across sources.
Fewer than 3 risks missing the most relevant chunk entirely. More than 7
risks diluting the context with loosely related material.

**Production tradeoff reflection:**
If deploying for real users at scale, I would evaluate:
- text-embedding-3-small (OpenAI) — higher accuracy, costs ~$0.02/1M tokens
- embed-english-v3.0 (Cohere) — strong domain-specific performance
- paraphrase-multilingual-MiniLM — if non-English users were expected
- Pinecone or Weaviate instead of local ChromaDB — for concurrent users,
  since ChromaDB doesn't scale beyond a single process
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What study techniques does research say are most effective for long-term retention? | Retrieval practice and spaced/distributed practice — ranked highest by Dunlosky et al. Elaborative interrogation and self-explanation also rated highly. |
| 2 | What causes procrastination and how can students overcome it? | Steel's meta-analysis identifies low self-efficacy, task aversiveness, and impulsiveness as core causes. Interventions include implementation intentions and reducing task aversiveness. |
| 3 | How do I build a study habit that actually sticks over time? | James Clear's habit stacking — attach the new habit to an existing cue. | 
| 4 | How do I build a study habit that actually sticks over time? | Habit stacking — attaching a new study habit to an existing routine cue (James Clear). Zimmerman adds that self-monitoring and setting specific goals sustain habits long-term. |
| 5 | What productivity system works best for managing a student's time? | No single best system — GTD for capturing tasks, time blocking for protecting deep work, Pomodoro for maintaining focus during sessions. |
---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Chunk boundary splitting of key arguments**
   Academic papers build multi-sentence arguments. If a finding like "retrieval
   practice outperformed rereading by 50%" is split across two chunks, neither
   chunk alone may rank highly for a relevant query. Mitigation: use 75-char
   overlap and manually inspect boundary chunks before embedding.

2. **Podcast transcript noise**
   The Huberman transcript contains filler phrases, sponsor reads, and
   conversational repetition that doesn't carry semantic value. If not cleaned,
   these dilute embeddings and cause off-topic chunks to surface. Mitigation:
   aggressively clean transcripts — strip timestamps, sponsor segments, and
   repeated filler before chunking.

3. **Source attribution ambiguity**
   Multiple documents cover overlapping topics (e.g. both Dunlosky and Roediger
   cover retrieval practice). The LLM may blend their findings without
   distinguishing which claim came from which source. Mitigation: include source
   filename in every chunk's metadata and instruct the LLM to cite sources
   explicitly in its response.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

     ```ascii
┌─────────────────────────────────────────────────────┐
│                  PIPELINE OVERVIEW                  │
└─────────────────────────────────────────────────────┘

 data/raw/*.txt
      │
      ▼
┌─────────────┐
│  INGESTION  │  ingest.py
│             │  • Load .txt files
│             │  • Strip noise (timestamps, sponsors, HTML)
│             │  • Save to data/cleaned/
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  CHUNKING   │  chunk.py
│             │  • 500-char chunks, 75-char overlap
│             │  • Output: {text, source, chunk_id}
└──────┬──────┘
       │
       ▼
┌──────────────────────────┐
│  EMBEDDING + VECTOR STORE│  embed.py
│                          │  • Model: all-MiniLM-L6-v2
│                          │  • Store: ChromaDB (./chroma_db)
│                          │  • Metadata: source filename
└──────────────┬───────────┘
               │
          [query time]
               │
               ▼
        ┌─────────────┐
        │  RETRIEVAL  │  retrieve.py
        │             │  • Embed query: all-MiniLM-L6-v2
        │             │  • top-k = 5 chunks
        │             │  • Return text + source + distance
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │  GENERATION │  query.py
        │             │  • LLM: Groq llama-3.3-70b-versatile
        │             │  • Grounded prompt (context only)
        │             │  • Output: answer + cited sources
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │     UI      │  app.py
        │             │  • Gradio Blocks
        │             │  • Input: question textbox
        │             │  • Output: answer + sources
        └─────────────┘
```

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
Tool: Claude. Input: the Documents section (file types and sources) and the
Chunking Strategy section of this file, plus Anticipated Challenge #2
(transcript noise). Expected output: ingest.py that loads all .txt files from
data/raw/, strips timestamps, filler, and HTML artifacts, and saves cleaned
text to data/cleaned/; and chunk.py with a chunk_text() function that splits
cleaned text into 500-char chunks with 75-char overlap, returning a list of
dicts with text, source, and chunk_id. I will verify by printing 5 random
chunks and confirming they are readable, self-contained, and free of artifacts.

**Milestone 4 — Embedding and retrieval:**
Tool: Claude. Input: the Retrieval Approach section and the Architecture
diagram. Expected output: embed.py that loads chunks from chunk.py, embeds
with all-MiniLM-L6-v2, and stores in ChromaDB at ./chroma_db with source
metadata; and retrieve.py with a retrieve(query, k=5) function that returns
top-k chunks with text, source, and distance score. I will verify by running
3 of my evaluation questions and confirming returned chunks are on-topic with
distance scores below 0.5.

**Milestone 5 — Generation and interface:**
Tool: Claude. Input: the Evaluation Plan section (for grounding requirements),
the Architecture diagram, and the query.py and app.py structure from the
diagram. Expected output: query.py with an ask(question) function that calls
retrieve(), formats context with source labels, and sends a grounding-enforced
prompt to Groq llama-3.3-70b-versatile; and app.py with a Gradio Blocks UI
containing a question input, answer output, and sources output. I will verify
by testing all 5 evaluation questions and confirming responses cite sources and
that out-of-scope questions are declined.
