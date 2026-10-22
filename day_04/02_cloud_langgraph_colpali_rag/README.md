# BioPharma Clinical Trial Safety & FDA Regulatory Multi-Agent Copilot
**Production-Grade AI Engineering Capstone · Module 04 (Cloud, LangGraph & ColPali Edition)**

---

## 🎯 Executive Overview & Industry Context
In BioPharma, Medical Device, and Clinical Healthcare environments, applying toy RAG scripts fails catastrophically:
1. **Clinical Protocols and Toxicity Grids** feature complex visual multi-column matrices, Kaplan-Meier curves, and RECIST grids that OCR text chunkers completely mangle.
2. **FDA 21 CFR § 312.32 Mandates** enforce strict, non-negotiable legal timelines (7-day expedited alerts for fatal/life-threatening SUSARs vs. 15-day expedited reports).
3. **Patient Safety Incidents & MedDRA Codes** require exact deterministic statistical math (calculating SAE rates, CTCAE Grade 1-5 severity, and dose interruption rates) with zero tolerance for LLM math hallucination.
4. **Human-in-the-Loop (HITL) Protocol Safeguards** are legally mandated: An AI assistant cannot autonomously authorize dose escalations or waive protocol safety holds without certified Medical Monitor dual sign-off (FDA 21 CFR Part 11).

This production system implements the architecture for **AuraBio Therapeutics Inc.** during its registrational **Phase III Oncology Trial (Protocol ABX-702-CLIN-301)** for metastatic Non-Small Cell Lung Cancer.

---

## 🏗️ Architecture & Technology Stack

```
                                      ┌────────────────────────────────────────────────────────┐
                                      │   AURABIO MULTI-AGENT STATEGRAPH ARCHITECTURE (LANGGRAPH)  │
                                      └────────────────────────────────────────────────────────┘

                                                          ┌──────────────┐
                                                          │ User Inquiry │
                                                          └──────┬───────┘
                                                                 │
                                                                 ▼
                                                    ┌───────────────────────────┐
                                                    │    INTENT ROUTER NODE     │
                                                    │ (Query Classification)    │
                                                    └─────────────┬─────────────┘
                                                                 │
                           ┌─────────────────────────────────────┼─────────────────────────────────────┐
                           │ (Regulatory / Protocol)             │ (Safety Stats / Ledger)             │ (Dose Escalation / Waiver)
                           ▼                                     ▼                                     ▼
            ┌─────────────────────────────┐       ┌─────────────────────────────┐       ┌─────────────────────────────┐
            │   COLPALI RETRIEVER NODE    │       │   CLINICAL ANALYTICS NODE   │       │   HUMAN-IN-THE-LOOP NODE    │
            │  (Visual Multi-Vector MaxSim│       │   (Deterministic MedDRA     │       │  (21 CFR Part 11 Medical    │
            │   over 2D Protocol Grids)   │       │    & CTCAE Aggregations)    │       │   Monitor Electronic Gate)  │
            └──────────────┬──────────────┘       └──────────────┬──────────────┘       └──────────────┬──────────────┘
                           │                                     │                                     │
                           └─────────────────────────────────────┼─────────────────────────────────────┘
                                                                 ▼
                                                  ┌─────────────────────────────┐
                                                  │   SAFETY SUPERVISOR NODE    │
                                                  │ (Evidence Synthesis & Ground│
                                                  │   Citations [Protocol p.X]) │
                                                  └──────────────┬──────────────┘
                                                                 │
                                                                 ▼
                                                  ┌─────────────────────────────┐
                                                  │ VERIFIED CLINICAL AUDIT ANS │
                                                  └─────────────────────────────┘
```

### 1. ColPali Vision-Language Multi-Vector Retrieval
Standard RAG loses spatial relationships and table headers during text extraction. **ColPali** embeds whole document page layouts as patch embeddings and uses late-interaction MaxSim scoring:
$$\text{Score}(Q, D) = \sum_{i \in Q} \max_{j \in D} (q_i \cdot d_j)$$
This preserves toxicity tables, RECIST dosing algorithms, and FDA submission forms with visual token alignment heatmaps.

### 2. LangGraph StateGraph Multi-Agent Orchestration
The multi-agent workflow is modeled as a compiled directed graph (`StateGraph`) with conditional routing between:
- `router_node`: Determines whether an inquiry is regulatory, statistical, or a high-risk modification.
- `colpali_retriever_node`: Executes visual multi-vector scoring.
- `clinical_analytics_node`: Executes deterministic pandas calculation on the clinical safety ledger.
- `human_in_the_loop_node`: Intercepts unauthorized dose escalations and halts execution in `PENDING_APPROVAL` status.
- `safety_supervisor_node`: Synthesizes evidence with mandatory bracket citations.

### 3. Pluggable AWS Cloud Vector Store Suite
Includes unified connectors for AWS production environments:
- **Amazon OpenSearch Serverless (AOSS)**: Connects via `opensearch-py` with AWS SigV4 IAM signing.
- **AWS RDS PostgreSQL (`pgvector`)**: Low-cost, production-recommended choice (~$15/mo or AWS Free Tier).
- **Pinecone Serverless (AWS us-east-1)**: Zero-maintenance pay-per-query.
- **Offline Dev Cloud Simulator**: Instant zero-cost local testing with simulated cloud network roundtrips.

---

## 📂 Project Directory Structure

```
day_04/02_cloud_langgraph_colpali_rag/
├── data/
│   ├── fda_clinical_trial_protocol_abx702.md   # Phase III Protocol & Toxicity Grid
│   ├── fda_21cfr_part312_ich_gcp_guidelines.md # 7-day/15-day SUSAR Mandates & 21 CFR 11
│   ├── investigator_brochure_safety_charter.md  # AESI Algorithms & $25M Indemnity
│   └── clinical_trial_safety_ledger.csv        # 25 Patient Adverse Event Records
├── src/
│   ├── models.py                               # Core Data Models & State Types
│   ├── config.py                               # Cloud Credentials & Environment
│   ├── loaders.py                              # Document & Visual Page Splitter
│   ├── colpali_engine.py                       # Multi-Vector MaxSim Retrieval Engine
│   ├── cloud_vector_store.py                   # AWS OpenSearch / pgvector / Pinecone Adapter
│   ├── deterministic_clinical_analytics.py     # Zero-Hallucination Statistical Math
│   ├── langgraph_workflow.py                   # Compiled StateGraph & HITL Nodes
│   └── quality_guardrails.py                   # FDA 21 CFR Part 11 Audit Trail Harness
├── tests/
│   └── test_cloud_rag_pipeline.py              # Automated Unit & Integration Tests
├── main.py                                     # Interactive CLI Demonstration
├── app.py                                      # Modern Streamlit Cloud Dashboard
├── requirements.txt                            # Enterprise Python Dependencies
└── .env.example                                # AWS & Model Credentials Template
```

---

## 🚀 Quickstart & Execution

### 1. Run the Automated Unit Tests
```bash
python -m unittest tests/test_cloud_rag_pipeline.py
```

### 2. Run the Production CLI Demonstration
```bash
python main.py
```

### 3. Launch the Interactive Cloud Dashboard
```bash
streamlit run app.py
```
