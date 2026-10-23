# 🎓 KIT College Student AI Copilot
**Production-Grade Multi-Agent RAG Assistant · Module 04**  
*Orchestrated with LangChain, LangGraph (`StateGraph`), and Google Gemini (3.7 / 3.6 / 3.5)*

---

## 📌 Executive Summary
This capstone project is an enterprise-grade, student-centric **Retrieval-Augmented Generation (RAG)** assistant and **Autonomous Multi-Agent Copilot**. It is built specifically for **KIT College of Engineering & Technology** to resolve real student inquiries regarding academic policies, examination grading, attendance condonation, course curriculums, library loans, hostel curfews, and campus placements.

Unlike basic naive RAG scripts that suffer from arithmetic hallucinations and context tearing, this architecture combines:
- **LangChain** for multi-format document chunking (`RecursiveCharacterTextSplitter`), standardized embeddings, and vector stores (`InMemoryVectorStore`).
- **LangGraph** for multi-agent state orchestration (`StateGraph`) with deterministic conditional routing.
- **Google GenAI SDK** powering the latest **Gemini 3.7 Flash** (high reasoning tier), **Gemini 3.6 Flash**, and **Gemini 3.5 Flash Lite** models alongside `text-embedding-004`.
- **Automated RAGAS CI/CD Quality Gates** verifying Faithfulness, Answer Relevancy, Context Precision, and Context Recall on every run.

---

## 🏛️ Knowledge Base Directory (`data/`)
All outdated corporate enterprise files have been removed. The knowledge base contains **only authentic, student-relevant campus documents**:

| File Name | Format | Ingestion Engine | Topics Covered |
|---|---|---|---|
| [`kit_college_student_handbook.md`](./data/kit_college_student_handbook.md) | **Markdown (.md)** | Section-Aware Markdown Parser | 75% attendance rule, 65%–74.9% medical condonation, CAT-1/CAT-2 grading, library fines (₹5/day), placement criteria. |
| [`kit_campus_hostel_and_mess_guide.docx`](./data/kit_campus_hostel_and_mess_guide.docx) | **Word (.docx)** | `python-docx` Document Parser | Biometric hostel curfew (8:30 PM), library extension pass, 4-meal mess schedule, 24x7 Wi-Fi. |
| [`kit_placement_policy_guide.pdf`](./data/kit_placement_policy_guide.pdf) | **PDF (.pdf)** | `pypdf` Multi-Page Extractor | CGPA 7.00 cutoff, Tier-1 Dream offers ($\ge$ ₹10 LPA), mandatory 8-week summer internship. |
| [`kit_courses_and_curriculum.csv`](./data/kit_courses_and_curriculum.csv) | **CSV Tabular** | Python CSV & Pandas DataFrames | Course codes (`CS401 Machine Learning`), faculty (*Dr. Sundeep K.*), credits (4), and exam dates. |

---

## 📂 Source Code Breakdown: What Each File Does

Every module in the [`src/`](./src) directory is dedicated to a distinct production responsibility:

```
src/
├── models.py            # Pydantic & Dataclass domain schemas
├── loaders.py           # Multi-format ingestion (PDF, Word, Markdown, CSV)
├── chunker.py           # LangChain RecursiveCharacterTextSplitter engine
├── embedder.py          # LangChain Embeddings adapter (Gemini text-embedding-004)
├── vector_store.py      # LangChain InMemoryVectorStore adapter
├── hybrid_retriever.py  # Dense Vector + Okapi BM25 Reciprocal Rank Fusion (RRF)
├── reranker.py          # Cross-candidate re-ranking module
├── generator.py         # Grounded generator powered by Gemini 3.7 / 3.6 with bracket citations
├── langgraph_agent.py   # Compiled LangGraph StateGraph Multi-Agent Copilot
├── evaluator.py         # Automated RAGAS evaluation harness (RAG Triad)
└── agent.py             # ReAct router with tool calling
```

### Detailed File Responsibilities:
1. [**`models.py`**](./src/models.py): Defines type-safe schemas including `Document`, `Chunk`, `GroundedCitation`, `GroundedResponse`, and `RAGASMetrics`.
2. [**`loaders.py`**](./src/loaders.py): Reads raw files from disk or in-memory byte streams (PDF via `pypdf`, Word via `python-docx`, Markdown via header splitting, CSV via DictReader).
3. [**`chunker.py`**](./src/chunker.py): Wraps LangChain's `RecursiveCharacterTextSplitter` to hierarchically partition text while preserving metadata (`source`, `section`, `format`, `chunk_id`).
4. [**`embedder.py`**](./src/embedder.py): Implements LangChain's `Embeddings` interface using Google GenAI `text-embedding-004` (with offline normalized semantic projection fallback).
5. [**`vector_store.py`**](./src/vector_store.py): Implements LangChain's `InMemoryVectorStore`, providing cosine similarity search and standard `as_retriever()` export.
6. [**`hybrid_retriever.py`**](./src/hybrid_retriever.py): Combines dense vector search with sparse Okapi BM25 keyword matching via Reciprocal Rank Fusion ($RRF = \frac{1}{60 + \text{rank}}$).
7. [**`reranker.py`**](./src/reranker.py): Scores candidate chunks based on lexical overlap, positional proximity, and exact keyword matches.
8. [**`generator.py`**](./src/generator.py): Injects context blocks into a hardened prompt and calls **Gemini 3.7 Flash** / **Gemini 3.6 Flash** to generate answers with mandatory `[Doc 1]` bracket citations.
9. [**`langgraph_agent.py`**](./src/langgraph_agent.py): Compiles the directed `StateGraph` multi-agent workflow:
   - `🔀 Router Node`: Detects query intent.
   - `🧮 Condonation Calculator Node`: Deterministic attendance calculation (zero math hallucination).
   - `📊 Course Catalog Node`: Exact tabular search across curriculum records.
   - `📚 Policy RAG Node`: LangChain hybrid vector retrieval.
   - `✍️ Synthesizer Node`: Context-grounded response generation.
   - `🛡️ Citation Verifier Node`: Validates citation integrity.
10. [**`evaluator.py`**](./src/evaluator.py): Evaluates Faithfulness, Answer Relevancy, Context Precision, and Context Recall against strict thresholds.
11. [**`app.py`**](./app.py): Modern Streamlit interactive classroom dashboard featuring live LangGraph execution traces, drag-and-drop document upload, and an attendance simulator.
12. [**`main.py`**](./main.py): CLI automated runner showcasing all 5 student test cases and the CI/CD quality gate.

---

## 📓 Interactive Classroom Jupyter Notebooks (`notebooks/`)

Located in [`day_04/notebooks/`](../notebooks/), these 6 progressive notebooks walk students through RAG engineering step-by-step:

| Notebook | Topic | Key Student Learning Takeaways |
|---|---|---|
| [**`01_document_loaders_and_chunking_strategies.ipynb`**](../notebooks/01_document_loaders_and_chunking_strategies.ipynb) | **Ingestion & Chunking** | Parsing PDF, Word, and Markdown; comparing Character, Token, and LangChain Recursive splitting; understanding the physics of chunk overlap ($10\% - 20\%$). |
| [**`02_vector_embeddings_and_vector_databases.ipynb`**](../notebooks/02_vector_embeddings_and_vector_databases.ipynb) | **Embeddings & Vector Stores** | High-dimensional geometric vector spaces, Cosine Similarity math, LangChain `InMemoryVectorStore`, and dense retrieval. |
| [**`03_hybrid_search_and_reranking.ipynb`**](../notebooks/03_hybrid_search_and_reranking.ipynb) | **Hybrid Search & RRF** | Why dense search fails on exact course codes (`CS401`); implementing Okapi BM25 and blending rankings with Reciprocal Rank Fusion. |
| [**`04_grounded_generation_and_hallucination_guardrails.ipynb`**](../notebooks/04_grounded_generation_and_hallucination_guardrails.ipynb) | **Grounded Generation** | Prompt framing, enforcing bracket citations (`[Doc 1]`), and defensive out-of-context refusal to prevent hallucinations. |
| [**`05_rag_evaluation_with_ragas_and_ci_cd.ipynb`**](../notebooks/05_rag_evaluation_with_ragas_and_ci_cd.ipynb) | **RAGAS CI/CD Gates** | Measuring the RAG Triad: Faithfulness, Answer Relevancy, Context Precision, and Context Recall with automated pass/fail thresholds. |
| [**`06_agentic_rag_and_multi_tool_react_agents.ipynb`**](../notebooks/06_agentic_rag_and_multi_tool_react_agents.ipynb) | **LangGraph & Multi-Agent** | Designing StateGraphs, defining TypedDict schemas, conditional branching edges, and deterministic tool execution. |

---

## 🛠️ Student Virtual Environment Setup Guide

Students can follow either setup method below:

### Track 1: Standard Python `venv`
```powershell
# 1. Navigate to the project directory
cd f:\KIT\notes\kit_college_notes\day_04\01_local_first_principles_rag

# 2. Create the virtual environment
python -m venv .venv

# 3. Activate the environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1
# (On macOS / Linux: source .venv/bin/activate)

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure API Key
copy .env.example .env
# Open .env and insert your GEMINI_API_KEY
```

### Track 2: Ultra-Fast `uv` (Rust-Based Workflow)
```powershell
cd f:\KIT\notes\kit_college_notes\day_04\01_local_first_principles_rag
uv venv
.\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
copy .env.example .env
```

---

## 🚀 Execution & Verification

### 1. Launch Interactive Streamlit Classroom App
```powershell
python -m streamlit run app.py
```
*Web Dashboard Features:*
- **💬 Student Copilot**: Live chat displaying **real-time LangGraph node execution trace badges** (`START` ➔ `🔀 Router` ➔ `🧮 Calculator` ➔ `✍️ Synthesizer` ➔ `🛡️ Verifier`).
- **📤 Drag & Drop Uploader**: Upload any `.pdf`, `.docx`, or `.txt` file to dynamically chunk and query it.
- **🧮 Attendance Simulator**: Interactive slider showing exact rules and medical condonation requirements.
- **📚 Course Catalog Explorer**: Filterable schedule of subjects, credits, and faculty.
- **🔬 LangGraph Inspector**: Interactive architecture diagram and RAGAS metric scorecard.

### 2. Run the Full CLI Showcase
```powershell
python main.py
```
Executes all 5 test cases (Attendance Condonation, Course Code Lookup, Library Rules, Placement Criteria, and Out-of-Domain Defense) and runs the automated RAGAS audit loop.

### 3. Run Automated Unit Test Suite (8 Tests)
```powershell
python -m unittest tests/test_rag_pipeline.py
```

---

## 🛡️ Automated RAGAS CI/CD Quality Gate Benchmarks

Every commit and build is validated against four strict assertions:
| Metric | Threshold | Current Score | Focus Area |
|---|---|---|---|
| **Faithfulness** | $\ge 0.85$ | **1.000** | Groundedness in reference text; zero hallucinations |
| **Answer Relevancy** | $\ge 0.80$ | **0.833** | Query alignment without conversational wandering |
| **Context Precision** | $\ge 0.75$ | **1.000** | Signal-to-noise ratio at top retrieval ranks |
| **Context Recall** | $\ge 0.75$ | **0.875** | Completeness of retrieved facts against ground truth |
