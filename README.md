# 🎓 KIT College of Engineering & Technology
## Generative AI, Full-Stack LLM Engineering & Applied Multi-Agent Systems
> Comprehensive curriculum notes, practical industry labs, architecture diagrams, and progressive day-by-day learning track.

---

## 📌 Repository Overview

Welcome to the official repository for the **Generative AI & LLM Systems Specialization** at **KIT College of Engineering & Technology**. This repository contains production-ready lab implementations, interactive Streamlit dashboards, pedagogical Jupyter notebooks, and end-to-end architectures designed to take students from foundational prompt engineering to enterprise-grade Multi-Agent Retrieval-Augmented Generation (RAG).

```
kit_college_notes/
├── day_01/                  # Day 01: Foundations of Generative AI & Prompt Engineering
├── day_02/                  # Day 02: Advanced Prompting, In-Context Learning & Guardrails
├── day_03/                  # Day 03: Multi-Turn Streamlit AI Chatbot with Gemini 3.x & Security Guardrails
├── day_04/                  # Day 04: Production RAG, Embeddings, Vector Stores & LangGraph Multi-Agent
├── day_05/                  # Day 05: Autonomous Tool Calling, API Integrations & Function Execution
├── day_06/                  # Day 06: Fine-Tuning, Parameter-Efficient Adaptation (LoRA/QLoRA) & Datasets
├── day_07/                  # Day 07: LLMOps, CI/CD, RAGAS Quality Benchmarking & Observability
├── day_08/                  # Day 08: Capstone Deployments, Security Hardening & Containerization
└── presentations_&_pdfs/    # Slide decks, reference architectures & lecture transcripts
```

---

## 🗺️ Curriculum Roadmap & Modules

| Module | Core Topics & Hands-on Work | Key Tools & Frameworks | Status |
| :--- | :--- | :--- | :--- |
| [**Day 01**](./day_01/) | LLM architectures, tokens, temperature, top-k/top-p sampling, zero-shot and few-shot prompting | Python, Google Gemini SDK, Jupyter | Available |
| [**Day 02**](./day_02/) | Chain-of-Thought (CoT), System Prompts, ReAct reasoning, output parsing, schema enforcement | Python, Pydantic, JSON Schema | Available |
| [**Day 03**](./day_03/) | Multi-turn streaming AI chatbot, `venv` vs `uv` environment mastery, OWASP LLM security guardrails | Streamlit, Google GenAI 3.8/3.6, `uv`, dotenv | Available |
| [**Day 04**](./day_04/) | Campus Student AI Copilot, document loaders (PDF, Docx, MD), BM25 + Dense Hybrid RRF, LangGraph `StateGraph` | LangChain, LangGraph, Streamlit, RAGAS | Available |
| [**Day 05**](./day_05/) | Function calling, real-time external APIs, ReAct routing, deterministic data computation | Google GenAI SDK, REST APIs, LangChain | Available |
| [**Day 06**](./day_06/) | Instruction dataset creation, PEFT / LoRA fine-tuning concepts, synthetic data generation | Hugging Face, Datasets, PyTorch | Available |
| [**Day 07**](./day_07/) | Automated evaluation gates, RAG Triad (Faithfulness, Relevancy, Precision, Recall), LLMOps | RAGAS, GitHub Actions, Unittest | Available |
| [**Day 08**](./day_08/) | Production serving, Docker containerization, security hardening, cloud deployment readiness | Docker, Streamlit Cloud / Cloud Run | Available |

---

## ⚡ Quick Start & Environment Setup

This repository supports both standard Python **`venv`** and ultra-fast **`uv`** (Rust-based).

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/kit_college_notes.git
cd kit_college_notes
```

### 2. Environment Setup

<<<<<<< HEAD
#### Track A: Traditional Python `venv` + `pip` Workflow
```powershell
# Create an isolated virtual environment
python -m venv .venv

# Activate the virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1
# (On macOS / Linux: source .venv/bin/activate)

# Upgrade pip and install root dependencies
pip install -r day_03/requirements.txt
```

> **Note**: To resolve PowerShell script execution restrictions, run:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
=======
#### Track B: Modern Ultra-Fast `uv` (Rust-Based Industry Workflow)
```powershell
# Create virtual environment in milliseconds
uv venv

# Run applications directly with automatic environment detection (No activation required!)
uv run streamlit run day_03/streamlit_gemini_chatbot_app.py

# Or install module-specific dependencies at lightning speed
uv pip install -r day_04/01_local_first_principles_rag/requirements.txt
```

> **Recommended**: Modern enterprise AI teams prefer `uv` for 10x-100x faster package resolution and deterministic caching.
>>>>>>> feature/modern-tooling-setup

---

## 🔐 API Key Configuration

To run the interactive Google Gemini apps and notebooks:

1. Obtain a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Create a local `.env` file in the module folder (e.g., `day_03/.env` or `day_04/01_local_first_principles_rag/.env`):
   ```env
   GEMINI_API_KEY=AIzaSyYourActualKeyHere
   ```
3. Never commit `.env` files to git repository branches. Pre-configured `.gitignore` prevents secret leakage.

---

## 🚀 Featured Showcase Applications

<<<<<<< HEAD
### 1. Day 03: Enterprise Generative AI Chatbot & Security Sandbox
- **Interface**: Interactive Streamlit Web App (`day_03/streamlit_gemini_chatbot_app.py`)
- **Key Capabilities**: Real-time token streaming with Gemini 3.8 / 3.6 Flash, multi-turn conversation memory, and live OWASP LLM01/LLM06 security guardrail inspector.
- **Run Command**:
  ```powershell
  python -m streamlit run day_03/streamlit_gemini_chatbot_app.py
  ```
=======
### 1. Day 03: Multi-Turn Streamlit Assistant with Live Threat Simulator
- **Interface**: Streamlit Web UI (`day_03/streamlit_gemini_chatbot_app.py`)
- **Key Capabilities**: Fluid typewriter streaming, model tier switcher (Gemini 3.8 / 3.6 / 3.5), persona presets, and simulated attack injections (DAN jailbreak, prompt exfiltration, PII masking).
- **Run Command (via uv)**:
  ```powershell
  uv run streamlit run day_03/streamlit_gemini_chatbot_app.py
  ```
>>>>>>> feature/module-showcase-updates

### 2. Day 04: Campus Student Copilot (Multi-Agent Hybrid RAG)
- **Interface**: Streamlit Dashboard (`day_04/01_local_first_principles_rag/app.py`)
- **Key Capabilities**: LangGraph directed `StateGraph` multi-agent routing, hybrid search (BM25 + Cosine Vector RRF), drag-and-drop lecture notes parser, attendance condonation calculator, and RAGAS CI/CD audit.
- **Run Command**:
  ```powershell
  cd day_04/01_local_first_principles_rag
  uv run streamlit run app.py
  ```

---

## 🧑‍🏫 Teaching Guide: How to Demonstrate PR Conflict Resolution

This repository is intentionally structured to teach software engineering best practices, including Git branching and Pull Request conflict resolution.

### The Conflict Scenario
When multiple student teams work on parallel features—such as updating documentation, adding dependencies, or modifying core logic—merge conflicts occur when Git cannot automatically reconcile diverging changes to identical lines.

<<<<<<< HEAD
### Resolution Strategy: Keep Traditional Workflow
```markdown
1. Open the file in VS Code or your editor.
2. Locate the conflict markers: `<<<<<<< HEAD`, `=======`, and `>>>>>>>`.
3. Choose "Accept Current Change" to preserve the standard venv/pip guidelines.
4. Delete conflict marker tags, stage the file (`git add README.md`), and commit.
```
=======
### Resolution Strategy: Combine Both Perspectives (Best Practice)
```markdown
1. Review both incoming and current changes.
2. Rather than discarding one branch, synthesize both: document both Traditional `venv` and Modern `uv` workflows side-by-side.
3. Remove the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
4. Stage and commit: `git commit -m "docs: resolve merge conflict by incorporating both venv and uv workflows"`.
```
>>>>>>> feature/pr-conflict-teaching-demo

### Quick Conflict Resolution Steps for Students:
1. **Identify the conflicting file**: Check `git status`. Conflicting files will be marked as `both modified`.
2. **Inspect Conflict Markers**:
   - `<<<<<<< HEAD`: Changes on your current branch.
   - `=======`: The dividing boundary between changes.
   - `>>>>>>> <branch-name>`: Incoming changes from the branch being merged / PR.
3. **Resolve the Conflict**: Edit the file to the desired clean version and remove all marker lines.
4. **Stage and Finalize**:
   ```bash
   git add README.md
   git commit -m "docs: resolve merge conflicts in README"
   git push origin <your-branch>
   ```

---

## 🤝 Contribution Guidelines

1. Fork the repository & create your feature branch: `git checkout -b feature/day-XX-enhancement`.
2. Test code and notebooks locally before committing.
3. Ensure `.env` or sensitive API keys are never staged.
4. Open a Pull Request targeting `main` with a clear explanation of your changes.

---

*KIT College of Engineering & Technology · Department of Computer Science & Generative AI Hub*
