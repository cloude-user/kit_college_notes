# 📓 Day 4: Interactive RAG & LangGraph Notebook Curriculum

Welcome to the hands-on interactive laboratory for **Day 4: Retrieval-Augmented Generation (RAG) & Agentic AI**.

This directory contains **6 progressive Jupyter Notebooks** engineered specifically for students at **KIT College of Engineering & Technology**. These notebooks take you from raw file parsing to autonomous multi-agent state machines using **LangChain**, **LangGraph**, and **Google Gemini (3.7 / 3.6 / 3.5)**.

---

## 🗺️ Notebook Roadmap & Learning Path

```
  ┌────────────────────────────────────────────────────────┐
  │  01_document_loaders_and_chunking_strategies.ipynb     │
  │  Ingest PDF, Word, Markdown, CSV + Recursive Chunking  │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │  02_vector_embeddings_and_vector_databases.ipynb       │
  │  Cosine Sim Math + LangChain InMemoryVectorStore       │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │  03_hybrid_search_and_reranking.ipynb                  │
  │  Sparse BM25 + Dense Vector + Reciprocal Rank Fusion   │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │  04_grounded_generation_and_hallucination_guardrails.ipynb
  │  Hardened Prompts + Bracket Citations + Gemini 3.7     │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │  05_rag_evaluation_with_ragas_and_ci_cd.ipynb          │
  │  RAG Triad: Faithfulness, Relevancy, Precision, Recall │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │  06_agentic_rag_and_multi_tool_react_agents.ipynb      │
  │  Autonomous LangGraph StateGraph Multi-Tool Agent      │
  └────────────────────────────────────────────────────────┘
```

---

## 📋 Detailed Breakdown: What Each Notebook Does & What You Need To Do

### 1. `01_document_loaders_and_chunking_strategies.ipynb`
- **What it does**:
  - Implements real-world multi-format parsing for college files:
    - Markdown (`kit_college_student_handbook.md`)
    - Word DOCX (`kit_campus_hostel_and_mess_guide.docx`)
    - PDF (`kit_placement_policy_guide.pdf`)
    - CSV (`kit_courses_and_curriculum.csv`)
  - Demonstrates LangChain's `RecursiveCharacterTextSplitter` preserving semantic boundaries (`\n## `, `\n### `, `\n\n`, `\n`).
  - Explores the physics of **Chunk Overlap (10%–20%)** to prevent context tearing on multi-clause policies.
- **What you need to do**:
  - Run through each cell sequentially.
  - Experiment with `chunk_size` (try `150` vs `400`) and observe how attendance condonation rules split.
  - Inspect the generated metadata dictionary (`source`, `section`, `format`).

---

### 2. `02_vector_embeddings_and_vector_databases.ipynb`
- **What it does**:
  - Demystifies vector math: Calculates **Cosine Similarity**, **Dot Product**, and **Euclidean ($L_2$) Distance** using pure `numpy`.
  - Compares Google Gemini `text-embedding-004` (768 dimensions) with local normalized vector projections.
  - Wraps LangChain's official `InMemoryVectorStore` to index college chunks.
  - Performs Top-K semantic similarity search with score thresholding.
- **What you need to do**:
  - Run the distance calculation cell with different query vectors.
  - Query the vector store with student queries:
    - *"Can I write exams if I was sick and my attendance is 68%?"*
    - *"What is the hostel biometric curfew time?"*
  - Compare the returned similarity scores.

---

### 3. `03_hybrid_search_and_reranking.ipynb`
- **What it does**:
  - Proves the **Vector Blindspot**: Pure dense vector search often misses exact codes like `CS401`, fine amounts `₹500`, and CGPA cutoffs `7.00`.
  - Implements an **Okapi BM25 sparse keyword retriever**.
  - Blends dense vector ranks and sparse keyword ranks using **Reciprocal Rank Fusion (RRF)**:
    $$RRF\_Score(d) = \frac{1}{60 + \text{rank}_{dense}(d)} + \frac{1}{60 + \text{rank}_{bm25}(d)}$$
  - Demonstrates how hybrid retrieval provides the best of both worlds (semantic understanding + exact token matching).
- **What you need to do**:
  - Test keyword-heavy queries like *"exam date CS401"* vs semantic queries like *"late night studying in library"*.
  - Observe how RRF elevates the correct chunk to Rank 1.

---

### 4. `04_grounded_generation_and_hallucination_guardrails.ipynb`
- **What it does**:
  - Constructs a **Grounded Context Prompt** with numbered citation tags (`[Doc 1]`, `[Doc 2]`).
  - Enforces **Bracket Citations**: Forcing the LLM to attribute every asserted claim to a reference document.
  - Implements **Defensive Out-of-Context Guardrails**: If asked *"What is the tuition fee for B.Tech CSE?"*, the model explicitly states *"I do not have sufficient information in the official documents"* rather than hallucinating plausible numbers.
  - Connects to Google Gemini 3.7 / 3.6 Flash (with offline deterministic fallback).
- **What you need to do**:
  - Ask in-scope questions (attendance, curfew, courses) and verify bracket citations.
  - Ask out-of-scope adversarial questions and verify that the guardrail refuses to guess.

---

### 5. `05_rag_evaluation_with_ragas_and_ci_cd.ipynb`
- **What it does**:
  - Demonstrates why classical metrics like BLEU and ROUGE fail on RAG answers due to semantic paraphrasing.
  - Implements the **RAG Triad**:
    - **Faithfulness**: Are claims strictly derived from context?
    - **Answer Relevancy**: Does the answer address the student's question?
    - **Context Precision**: Are relevant chunks ranked at top positions?
    - **Context Recall**: Did retrieval find all facts required for ground truth?
  - Establishes automated CI/CD assertion gates (`assert faithfulness >= 0.85`).
- **What you need to do**:
  - Run the automated evaluation suite.
  - Intentionally inject a hallucinated fact into an answer and observe the Faithfulness score plummet.

---

### 6. `06_agentic_rag_and_multi_tool_react_agents.ipynb`
- **What it does**:
  - Moves from static 1-shot RAG to an **Autonomous Multi-Agent Copilot** using **LangGraph**.
  - Constructs a complete `StateGraph` with:
    - **Router Node**: Classifies query intent.
    - **Condonation Calculator Node**: Deterministic math calculation ($75\% - \text{attendance}\%$, checks 65% floor, outputs ₹500 fee and 3-day doctor note rules).
    - **Course Catalog Node**: Exact structured tabular search across curriculum records.
    - **Policy RAG Node**: LangChain vector retrieval.
    - **Citation Verifier Node**: Validates bracket citation integrity.
- **What you need to do**:
  - Trace the graph execution path for 3 student queries:
    1. *"I have 68% attendance due to illness, what can I do?"* ➔ `condonation_calc`
    2. *"Who teaches CS401 and when is the exam?"* ➔ `course_lookup`
    3. *"What is the hostel gate closing time?"* ➔ `policy_rag`
  - Experiment with adding a new custom tool node (e.g., Library Fine Calculator).

---

## ⚡ How to Run the Notebooks

Make sure your virtual environment is active:
```powershell
# Navigate to the project directory
cd f:\KIT\notes\kit_college_notes\day_04\01_local_first_principles_rag

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Launch Jupyter Lab or VS Code Notebooks
jupyter notebook ..\notebooks
```
*(Or simply click on any `.ipynb` file in VS Code / Antigravity IDE and select the `.venv` Python kernel).*
