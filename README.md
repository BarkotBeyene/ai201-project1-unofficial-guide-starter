# The Unofficial Guide — Project 1

---

## Domain

This system covers **student effectiveness** — the practical knowledge of how to study, build habits, maintain focus, and overcome procrastination. Sources span peer-reviewed academic papers, podcast transcripts, and expert blogs, capturing both the science and the lived experience of high-performance learning.

This knowledge is hard to find through official channels because it is scattered across dozens of papers, blogs, and transcripts with no single place to ask a plain-language question and get a grounded, cited answer drawn from all of them at once. A university website might link to a tutoring center, but it won't tell you which study techniques the research actually ranks highest, why procrastination happens at a neurological level, or how habit stacking works in practice.

---

## Document Sources

| # | Source | Type | URL or Citation |
|---|--------|------|------|
| 1 | Zimmerman, "Becoming a Self-Regulated Learner" | Academic paper | Zimmerman, B. J. (2002). Becoming a self-regulated learner: An overview. *Theory into Practice, 41*(2), 64–70. |
| 2 | The Learning Scientists, "Evidence-Based Study Strategies" | Blog/article | https://www.learningscientists.org/blog/2016/12/13-1 |
| 3 | James Clear, "How to Build New Habits by Taking Advantage of Old Ones" | Blog/article | https://jamesclear.com/habit-stacking |
| 4 | Huberman Lab, "How to Study and Learn" (transcript) | Podcast transcript | https://www.youtube.com/watch?v=mzexJPoXBCM |
| 5 | Dunlosky et al., "Improving Students' Learning With Effective Study Techniques" | Academic paper | Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T. (2013). Improving students' learning with effective learning techniques. *Psychological Science in the Public Interest, 14*(1), 4–58. |
| 6 | Todoist, "Productivity Methods Overview: GTD, Time Blocking, Pomodoro" | Blog/article | https://www.todoist.com/inspiration/personal-productivity-methods |
| 7 | Piers Steel, "The Nature of Procrastination: A Meta-Analytic Review" | Academic paper | Steel, P. (2007). The nature of procrastination: A meta-analytic and theoretical review of quintessential self-regulatory failure. *Psychological Bulletin, 133*(1), 65. |
| 8 | Roediger & Karpicke, "The Power of Testing Memory" | Academic paper | Roediger, H. L., & Karpicke, J. D. (2006). The power of testing memory: Basic research and implications for educational practice. *Perspectives on Psychological Science, 1*(3), 181–210. |
| 9 | Anne-Laure Le Cunff, "Why learning how to learn is the skill behind all skills" | Blog/article | https://nesslabs.com/learning-how-to-learn |
| 10 | Tim Urban, "Why Procrastinators Procrastinate" (Wait But Why) | Blog/article | https://waitbutwhy.com/2013/10/why-procrastinators-procrastinate.html |

---

## Chunking Strategy

**Chunk size:** 1,200 characters

**Overlap:** 150 characters

**Why these choices fit the documents:**
The corpus is a mix of long-form academic papers (Dunlosky, Steel, Roediger) and shorter blog posts and transcripts. At 500 characters (the initial choice), academic papers fragmented into half-sentences with no semantic content per chunk — Roediger alone produced 349 chunks at that size. After evaluating retrieval quality, the chunk size was increased to 1,200 characters. At this size, each chunk carries a complete argument, finding, or recommendation — enough semantic signal for the embedding model to match it to a specific query. The 150-character overlap ensures that sentences split at chunk boundaries are recoverable from either adjacent chunk.

**Preprocessing before chunking:**
Each document was run through `src/ingest.py`, which strips HTML tags, timestamps, sponsor segments, repeated navigation text, and boilerplate artifacts before saving cleaned text to `data/cleaned/`.

**Final chunk count:** 592 chunks across 10 documents

---

## Sample Chunks

**Sample 1** — `The_Power_of_Testing_Memory_by_Roediger_and_Karpicke.txt`
> Bjork and Bjork (1992) developed a theory to explain the testing effect and other effects of retrieval effort. They distinguished between storage strength, which reflects the relative permanence of a memory trace, and retrieval strength, which reflects the momentary accessibility of a memory trace. Their model assumes that retrieval strength is negatively correlated with increments in storage strength; that is, easy retrieval does not enhance storage strength, whereas more effortful retrieval practice does enhance storage strength and promotes more permanent, long-term learning.

**Sample 2** — `The_Power_of_Testing_Memory_by_Roediger_and_Karpicke.txt`
> Our results demonstrate the powerful effect testing has in enhancing later retention. The repeated-studying group showed the most forgetting (52%), followed by the SSST group (28%), and the repeated-testing group (STTT) showed the least amount of forgetting (10%) over 1 week.

**Sample 3** — `Improving_Students_Learning_With_Effective_Study_Techniques_by_Dunlosky_et_al.txt`
> Self-explanation effects on far-transfer tests (in which students are asked to solve problems that differ from practice problems not only in their surface features but also in one or more structural aspects) have been shown for the solving of math problems and pattern learning. Thus, self-explanation facilitates an impressive range of learning outcomes.

**Sample 4** — `Improving_Students_Learning_With_Effective_Study_Techniques_by_Dunlosky_et_al.txt`
> Students and teachers who are not already doing so should consider using techniques designated as high utility, because the evidence base for those techniques is strong across a wide range of learning conditions, materials, student characteristics, and criterion tasks.

**Sample 5** — `Why_learning_how_to_learn_is_the_skill_behind_all_skills_Anne_Laure_LeCunff.txt`
> Traditional education teaches us what to think, not how to think. We memorize facts for tests, then forget them. We follow instructions instead of designing our own learning paths. Nobody teaches us the most important skill of all: learning how to learn. This gap matters because skills become obsolete faster than ever.

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`

This model runs fully locally — no API key, no rate limits, no cost. It produces 384-dimensional embeddings and is optimized for English paragraph-length text, which matches this corpus well.

**Production tradeoff reflection:**
If deploying for real users at scale, I would evaluate several alternatives:

- **text-embedding-3-small (OpenAI)** — measurably higher accuracy on retrieval benchmarks, costs ~$0.02/1M tokens. The accuracy gain would matter for this corpus because academic papers use precise, field-specific vocabulary that `all-MiniLM-L6-v2` sometimes fails to distinguish.
- **embed-english-v3.0 (Cohere)** — strong domain-specific performance; designed for retrieval tasks rather than general similarity.
- **paraphrase-multilingual-MiniLM** — necessary if the system were extended to non-English student communities.
- **Pinecone or Weaviate instead of local ChromaDB** — ChromaDB is single-process only; a production system with concurrent users would need a managed vector store that handles parallel queries and horizontal scaling.

The key tradeoff is accuracy vs. operational cost and complexity. For a student project running on one machine, local `all-MiniLM-L6-v2` is the right call. For production, the OpenAI embedding API with a managed vector store would be the pragmatic choice.

---

## Retrieval Test Results

### Query 1: "What study techniques does research say are most effective for long-term retention?"

**Top returned chunks:**

| Rank | Distance | Source | Excerpt |
|------|----------|--------|---------|
| 1 | 0.674 | `The_Power_of_Testing_Memory_by_Roediger_and_Karpicke.txt` | "...the repeated-testing group (STTT) showed the least amount of forgetting (10%) over 1 week. Our results demonstrate the powerful effect testing has in enhancing later retention..." |
| 2 | 0.692 | `The_Power_of_Testing_Memory_by_Roediger_and_Karpicke.txt` | "...more effortful retrieval practice does enhance storage strength and promotes more permanent, long-term learning. However, students may elect poor study strategies because they rely on retrieval fluency..." |
| 3 | 0.707 | `The_Power_of_Testing_Memory_by_Roediger_and_Karpicke.txt` | "...equally spaced practice may lead to benefits for long-term retention because of the delayed initial test..." |

**Why these chunks are relevant:** The query asks directly about retention-enhancing techniques. All three chunks are from Roediger & Karpicke's paper on the testing effect — the foundational research on why self-testing outperforms rereading. Each chunk contains empirical findings (forgetting rates, storage strength theory) that directly answer the question. The distance scores (~0.67–0.71) are acceptable for this corpus; the content alignment is strong even if the scores aren't low.

---

### Query 2: "What causes procrastination and how can students overcome it?"

**Top returned chunks:**

| Rank | Distance | Source | Excerpt |
|------|----------|--------|---------|
| 1 | 0.464 | `The_Nature_of_Procrastination_Meta_Analysis_by_Piers_Steel.txt` | "...procrastination in the rest of world is increasing... Keywords: Procrastination, irrational delay, pathological decision-making, meta-analysis..." |
| 2 | 0.483 | `The_Nature_of_Procrastination_Meta_Analysis_by_Piers_Steel.txt` | "...integrative hybrid of expectancy theory and hyperbolic discounting. Continued research into procrastination should not be delayed, especially since its prevalence appears to be growing..." |
| 3 | 0.500 | `The_Nature_of_Procrastination_Meta_Analysis_by_Piers_Steel.txt` | "...there is a need for a comprehensive and detailed examination of the research on procrastination. With such a review, we can better elucidate the nature of procrastination..." |

**Why these chunks are relevant:** Distance scores of 0.46–0.50 are the strongest in the eval set, confirming that this query semantically aligns well with Steel's paper. The chunks are all from the correct source (the only comprehensive meta-analysis in the corpus on this topic). The retrieved content is methodological framing rather than the specific findings (impulsiveness, fear of failure), which explains why the generated answer is partially accurate rather than fully accurate — the most specific chunks are present in the collection but weren't ranked highest.

---

### Query 3: "What does Huberman say about active recall and how it helps with learning?"

**Top returned chunks:**

| Rank | Distance | Source | Excerpt |
|------|----------|--------|---------|
| 1 | 0.875 | `How_to_Study_and_Learn_Huberman_Lab_Transcript.txt` | "It was active recall. I rebuilt all of my studying... For math classes, my main study tool was a stack of white paper. 'All right, do this proof,'..." |
| 2 | 0.878 | `The_Power_of_Testing_Memory_by_Roediger_and_Karpicke.txt` | "...subjects first recalled items from the cued categories, and this act of recall inhibited their ability to access the other categories..." |
| 3 | 0.885 | `The_Power_of_Testing_Memory_by_Roediger_and_Karpicke.txt` | "...the short recall time may also explain why subjects were able to recall only about 20 of 36 words after 24 study or test trials..." |

**Why these chunks are relevant:** Chunk 1 is directly on-target: it is the passage from the Huberman transcript where he describes his personal active recall practice in detail. The Roediger chunks are relevant by topic (both are about recall and testing) but not specific to Huberman's claims. The high distance scores (~0.875) reflect that the Huberman transcript was aggressively cleaned and is short (8 chunks), so fewer chunks compete — the model retrieves the right one first, but the absolute similarity score is weaker than for denser documents.

---

## Grounded Generation

**System prompt grounding instruction:**

```
You are a student effectiveness assistant.
Answer the user's question using ONLY the information in the provided documents.
Do not use any outside knowledge.
If the documents do not contain enough information to answer the question,
say exactly: 'I don't have enough information on that.'
Always cite the specific document(s) your answer draws from by name.
```

**How source attribution is surfaced in the response:**

Attribution is enforced in two ways. First, the system prompt instructs the LLM to cite document names in its response text. Second, source filenames are extracted programmatically from the retrieved chunks before generation — regardless of whether the LLM cites them in prose, the `sources` field in the response object always lists every document that contributed context. The Gradio UI displays this list in a separate "Retrieved from" field so it is always visible to the user.

---

## Example Responses

### Response 1 — "What causes procrastination and how can students overcome it?"

> According to the documents, procrastination is a complex issue with multiple causes. The documents suggest that procrastination is linked to traits such as low conscientiousness, fear of failure, and rebelliousness (The_Nature_of_Procrastination_Meta_Analysis_by_Piers_Steel.txt, pages 49, 58). Additionally, internal and external variables such as impulsiveness, need for achievement, availability of temptations, and frequency of encountering dreaded tasks can contribute to procrastination (The_Nature_of_Procrastination_Meta_Analysis_by_Piers_Steel.txt, page 58).
>
> As for overcoming procrastination, the documents do not provide a direct answer. However, they suggest that people can learn to avoid procrastination as they age and develop schemes to overcome it (The_Nature_of_Procrastination_Meta_Analysis_by_Piers_Steel.txt, page 23). A diagnostic procedure to identify the underlying causes can help lay the foundation for treatment (The_Nature_of_Procrastination_Meta_Analysis_by_Piers_Steel.txt, page 58).

**Sources:** `The_Nature_of_Procrastination_Meta_Analysis_by_Piers_Steel.txt`

---

### Response 2 — "What does Huberman say about active recall and how it helps with learning?"

> According to "How_to_Study_and_Learn_Huberman_Lab_Transcript.txt", Huberman says that active recall is a "miraculous transformation" that completely transformed his academic performance. He rebuilt his studying approach around active recall, using techniques such as taking notes and testing himself on math proofs from scratch. He states that active recall is "brutal, but it's incredibly efficient" and that it's the way to learn new things. He also mentions that it's time-efficient, allowing him to finish studying quickly, even during finals period.

**Sources:** `How_to_Study_and_Learn_Huberman_Lab_Transcript.txt`, `The_Power_of_Testing_Memory_by_Roediger_and_Karpicke.txt`, `Improving_Students_Learning_With_Effective_Study_Techniques_by_Dunlosky_et_al.txt`

---

### Out-of-scope query — "What is the best way to cook pasta?"

> I don't have enough information on that.

**Sources:** `Becoming_a_Self_Regulated_Learner_Overview_by_Zimmerman.txt`, `Productivity_Methods_Overview_GTD_Time_Blocking_Pomodoro_by_Todoist.txt`, `How_to_Study_and_Learn_Huberman_Lab_Transcript.txt`

The system retrieved unrelated chunks (the query has no semantic match in the corpus) but correctly declined to generate an answer, demonstrating that the grounding instruction is enforced even when some chunks are returned.

---

## Query Interface

The interface is a **Gradio Blocks** web app launched with `python app.py` and accessible at `http://localhost:7860`.

**Input fields:**
- `Your question` — a multi-line textbox with a placeholder example query. Also supports Enter-to-submit.

**Output fields:**
- `Answer` — the LLM-generated response, grounded in retrieved chunks and containing inline source citations.
- `Retrieved from` — a bulleted list of the source document filenames that contributed context to the answer.

**Sample interaction transcript:**

```
Question: How do I build a study habit that actually sticks over time?

Answer:
To build a study habit that actually sticks over time, consider the strategy of
habit stacking as mentioned in "How_to_Build_New_Habits_by_Taking_Advantage_of_
Old_Ones_written_by_James_Clear.txt". This involves identifying your existing
habits and using them as a trigger to stack your new study habit on top of them.
The document suggests brainstorming a list of your current daily habits and
finding a habit with the same frequency as your desired study habit.

Additionally, "Evidence_Based_Study_Strategies_Overview_by_The_Learning_
Scientists.txt" provides evidence-based study strategies such as Spaced Practice
and Retrieval Practice that can be incorporated into your study routine.

It's also important to note that your cue should have the same frequency as your
desired habit to increase the likelihood of success.

Retrieved from:
• Evidence_Based_Study_Strategies_Overview_by_The_Learning_Scientists.txt
• How_to_Build_New_Habits_by_Taking_Advantage_of_Old_Ones_written_by_James_Clear.txt
• How_to_Study_and_Learn_Huberman_Lab_Transcript.txt
```

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What study techniques does research say are most effective for long-term retention? | Retrieval practice and spaced practice ranked highest (Dunlosky et al.); testing effect foundational (Roediger & Karpicke) | Correctly identified testing effect, spaced practice, and active recall; missed Dunlosky's explicit ranking of techniques by utility | Relevant | Partially accurate |
| 2 | What causes procrastination and how can students overcome it? | Steel's meta-analysis: low conscientiousness, impulsiveness, fear of failure as core causes; implementation intentions as intervention | Correctly named conscientiousness, fear of failure, impulsiveness, and temptation availability; acknowledged limited guidance on overcoming it | Relevant | Partially accurate |
| 3 | How do I build a study habit that actually sticks over time? | Habit stacking (James Clear) — attach new habit to existing cue of same frequency | Correctly described habit stacking from James Clear; added spaced/retrieval practice from Learning Scientists as complementary strategy | Relevant | Accurate |
| 4 | What does Huberman say about active recall and how it helps with learning? | Active recall described as transformative; "brutal but incredibly efficient"; rebuilt studying around self-testing from scratch | Accurately cited Huberman's exact quotes and personal practice description; answer is fully grounded in transcript | Relevant | Accurate |
| 5 | What productivity system works best for managing a student's time? | No single best system — GTD for capture, time blocking for deep work, Pomodoro for focus sessions | "I don't have enough information on that." — retrieved only preamble/navigation chunks from Todoist guide, not the method descriptions | Off-target | Inaccurate |

---

## Failure Case Analysis

**Question that failed:** "What productivity system works best for managing a student's time?"

**What the system returned:** "I don't have enough information on that."

**Root cause (tied to retrieval stage):**
The Todoist productivity guide is a 36,000-character document with a long preamble — table of contents, navigation guidance, and framing text — before it reaches the substantive descriptions of each method (GTD, Pomodoro, Time Blocking, etc.). At 1,200-character chunks, the document's first ~10 chunks are entirely preamble. When the query "what productivity system works best for managing a student's time" is embedded, the cosine similarity is highest against those preamble chunks (distances 0.83–0.93), because they share vocabulary like "productivity," "system," and "time." The chunks containing actual method descriptions — which would answer the question — were ranked lower and not retrieved.

This is a document structure problem: the most useful content is not front-loaded, and the query's abstract framing ("works best") semantically aligns with the document's abstract framing rather than with any specific method's description. The LLM correctly declined rather than hallucinating an answer.

**What would fix it:** Two options. First, chunk the Todoist document by section header (each method gets its own chunk regardless of length) rather than fixed character count — this would guarantee that the GTD, Pomodoro, and Time Blocking sections are each retrievable as a unit. Second, re-query with a more specific phrasing ("What is the Pomodoro technique and how does it help students focus?") which matches the language of the method descriptions rather than the abstract framing.

---

## Spec Reflection

**One way the spec helped during implementation:**
The Architecture section of `planning.md` labeled every pipeline stage with the specific tool — `all-MiniLM-L6-v2` at the embedding step, ChromaDB at the vector store, `llama-3.3-70b-versatile` at generation. When prompting Claude to generate `embed.py` and `retrieve.py`, passing that diagram directly meant the generated code used the correct libraries and API calls on the first attempt rather than requiring library corrections. The diagram acted as a contract that kept the AI-generated code aligned with the actual stack.

**One way implementation diverged from the spec, and why:**
The spec called for 500-character chunks with 75-character overlap. After running the first eval, it was clear this produced fragments — the Roediger paper alone generated 349 chunks at 500 characters, most containing half-sentences with no standalone meaning. The chunk size was increased to 1,200 characters (with 150-character overlap) after inspecting retrieval results. This brought the total chunk count from ~1,455 to 592 and measurably improved Q2, Q3, and Q4 results. The planning.md chunking strategy section was not updated before implementation began — which was a process gap the spec was designed to prevent.

---

## AI Usage

**Instance 1 — Generating the embedding and retrieval pipeline**

- *What I gave the AI:* The Retrieval Approach section of `planning.md` (model name, top-k value, ChromaDB storage path) and the ASCII architecture diagram showing the five pipeline stages with tool labels at each stage.
- *What it produced:* `src/embed.py` that loads chunks, embeds with `all-MiniLM-L6-v2`, and stores in ChromaDB with source metadata; and `src/retrieve.py` with a `retrieve(query, k=5)` function returning text, source, and distance score.
- *What I changed or overrode:* The generated `embed.py` did not clear the existing ChromaDB collection before re-embedding — it would append duplicate chunks on each run. I added a `collection.delete(where={})` call before the embedding loop so the collection stays clean across reruns. I also changed the metadata schema to include both `source` and `chunk_id` fields, since the generated code only stored `source`.

**Instance 2 — Generating the grounded generation prompt and Gradio UI**

- *What I gave the AI:* The system prompt requirement from the project spec ("answer from retrieved context only, decline if insufficient"), the Evaluation Plan section listing the 5 test questions, and the `app.py` Gradio skeleton from the spec instructions.
- *What it produced:* `src/query.py` with the grounding system prompt and `ask()` function; `app.py` with a Gradio Blocks layout containing question input, answer output, and sources output.
- *What I changed or overrode:* The generated grounding instruction said "try to answer only from the provided documents" — the word "try" creates a loophole the LLM exploits to draw on training knowledge. I rewrote it to "Answer the user's question using ONLY the information in the provided documents. Do not use any outside knowledge." I also added programmatic source deduplication (`list(dict.fromkeys(...))`) because the generated code let the LLM control source attribution entirely through prose, with no structural guarantee that sources would appear in the output.
