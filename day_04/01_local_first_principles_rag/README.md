# Enterprise Financial & Compliance Multi-Agent RAG Assistant
**Production-Grade AI Engineering Capstone · Module 04: RAG & Multi-Agent Systems**

---

## 🎯 Executive Overview & Real-World Industry Context
In enterprise environments (Banking, FinTech, Healthcare, Cloud SaaS), deploying a simple "toy" RAG script fails because:
1. **Financial figures and error codes** require exact keyword matching (which pure dense vector search fails at).
2. **Regulatory and compliance audits** require strict legal citations (`[Doc 1]`) and zero hallucinations.
3. **Structured data (CSV/SQL)** cannot be queried reliably with pure text vector embeddings; it requires an **Agentic Router** that executes deterministic aggregation without math hallucination.
4. **CI/CD Quality Gates** must automatically reject model regressions using automated **RAGAS** evaluations (Faithfulness $\ge 0.85$, Answer Relevancy $\ge 0.80$, Context Precision $\ge 0.75$, Context Recall $\ge 0.75$).

This production project implements the complete, battle-tested architecture for **CloudCorp Technologies Inc.**, handling real-world enterprise documents, SEC filings, SOX compliance manuals, customer SLAs, and ERP general ledgers.

---

## 🏛️ Authentic Real-World Enterprise Documents
Rather than synthetic stubs, this system ingests genuine enterprise-grade documents:

1. **SEC Form 10-Q Quarterly Report** (`data/sec_filing_q3_cloudcorp.md`):
   - Commission File No. `001-39482`
   - GAAP ASC-606 Revenue Recognition, Remaining Performance Obligations ($1.84 Billion RPO).
   - Capital commitments for 16,384 Nvidia H100/H200 GPU compute clusters under 3-year operating leases.
   - SRE telemetry failover error code disclosures (`ERR_STREAM_BUFFER_OVERFLOW_504`, `ERR_CRYPTO_HSM_TIMEOUT_509`).
   - SOX Section 302 and 404 internal control assessments.

2. **Corporate Compliance & Governance Manual** (`data/corporate_compliance_policy.md`):
   - Document ID: `POL-FIN-SEC-2025-V2`
   - Multi-tier procurement authorization thresholds (Tier 1 <$25K, Tier 2 $25K-$100K, Tier 3 $100K-$500K, Tier 4 >$500K Board of Directors Audit Committee).
   - API key rotation cycle (mandatory 90 calendar days, automatic revocation after 95 days).
   - SOX Section 404 WORM audit log retention (7-year immutable storage) and dual-signoff for journal entries exceeding $50,000.
   - Hardware RMA defect replacement SLAs (14-day notice, overnight replacement, 30-day RMA return).
   - GDPR Article 33 breach notification SLA (72 hours) and SOC-2 Type II NIST SP 800-88 cryptographic sanitization.

3. **Master Cloud Services Agreement & SLA with GlobalBank N.A.** (`data/enterprise_cloud_msa_and_sla.md`):
   - Agreement Reference: `MSA-GB-2024-8831`
   - 99.99% multi-region high availability commitment across US-East, US-West, and EU-Central.
   - Tiered service credits: Tier 1 (10%), Tier 2 (25% credit under `SLA-CREDIT-TIER-2`), Tier 3 (50% credit + termination right).
   - Liquidated damages booked under General Ledger Account `GL-5120` (*Customer SLA Penalties & Rebates*).
   - $15,000,000 aggregate liability cap.

4. **Multi-Quarter Enterprise General Ledger** (`data/financial_ledger_2025.csv`):
   - 21 realistic ledger records across 7 departments (Engineering-AI, Cloud-Infrastructure, Security-Compliance, Sales-Enterprise, Customer-Success, Legal-Regulatory, Data-Platform) for Q1, Q2, and Q3 2025.
   - Includes GL accounts (`GL-6100`, `GL-5120`, `GL-7100`, etc.), cost centers, budget vs. actual spend, variance percentage, and auditor notes.

---

## 🏗️ System Architecture

```
                                  ┌──────────────────────────────────────────────┐
                                  │      ENTERPRISE MULTI-AGENT ARCHITECTURE     │
                                  └──────────────────────────────────────────────┘

                                                   ┌──────────────┐
                                                   │ User Query   │
                                                   └──────┬───────┘
                                                          │
                                                          ▼
                                            ┌───────────────────────────┐
                                            │   AUTONOMOUS ROUTER AGENT │
                                            │ (Intent & Schema Dispatch)│
                                            └─────────────┬─────────────┘
                                                          │
                    ┌─────────────────────────────────────┼─────────────────────────────────────┐
                    ▼                                     ▼                                     ▼
     ┌─────────────────────────────┐       ┌─────────────────────────────┐       ┌─────────────────────────────┐
     │  HYBRID UNSTRUCTURED RAG    │       │  STRUCTURED DATA ANALYTICS  │       │   PROCUREMENT VALIDATOR     │
     │  (SEC 10-Q, Policies, SLA)  │       │   (Financial Ledger CSV)    │       │  (Capital Expense Tiers)    │
     └──────────────┬──────────────┘       └──────────────┬──────────────┘       └──────────────┬──────────────┘
                    │                                     │                                     │
                    ▼                                     │                                     │
     ┌─────────────────────────────┐                      │                                     │
     │   BM25 + Dense Vector (RRF) │                      │                                     │
     │   + Cross-Encoder Reranker  │                      │                                     │
     └──────────────┬──────────────┘                      │                                     │
                    │                                     │                                     │
                    ▼                                     ▼                                     │
     ┌─────────────────────────────┐       ┌─────────────────────────────┐                      │
     │ Grounded Context Generator  │       │ Aggregated SQL/Pandas Stats │                      │
     │ (Bracket Citation Enforcer) │       │ (Exact Ledger Calculations) │                      │
     └──────────────┬──────────────┘       └──────────────┬──────────────┘                      │
                    │                                     │                                     │
                    └──────────────────┬──────────────────┘                                     │
                                       ▼                                                        │
                        ┌─────────────────────────────┐                                         │
                        │ RAGAS Quality Gate Audit    │ <───────────────────────────────────────┘
                        │ (Faithfulness >= 0.85 Check)│
                        └──────────────┬──────────────┘
                                       │
                                       ▼
                        ┌─────────────────────────────┐
                        │   VERIFIED ENTERPRISE ANS   │
                        │     + SOURCE CITATIONS      │
                        └─────────────────────────────┘
```

---

## 📂 Project Directory Structure

```
enterprise_financial_compliance_rag/
├── README.md                      # Comprehensive architecture blueprint & usage guide
├── main.py                        # Production showcase runner & RAGAS CI/CD audit loop
├── app.py                         # Interactive Streamlit classroom demonstration dashboard
│
├── data/                          # Authentic enterprise knowledge base
│   ├── sec_filing_q3_cloudcorp.md # Real-world SEC Form 10-Q quarterly report
│   ├── corporate_compliance_policy.md # Internal corporate SOX compliance manual
│   ├── enterprise_cloud_msa_and_sla.md # Master Services Agreement & SLA with GlobalBank
│   └── financial_ledger_2025.csv  # Multi-quarter General Ledger with GL accounts
│
├── src/                           # Enterprise modular source package
│   ├── __init__.py
│   ├── models.py                  # Pydantic schemas (Document, Chunk, GroundedResponse, Metrics)
│   ├── loaders.py                 # Multi-format ingestion (Markdown & Tabular CSV)
│   ├── chunker.py                 # RecursiveCharacterTextSplitter with overlap & metadata
│   ├── embedder.py                # Dual Cloud/Local normalized vector embedding engine
│   ├── vector_store.py            # Cosine similarity vector store with metadata filtering
│   ├── hybrid_retriever.py        # Dense Vector + BM25 Reciprocal Rank Fusion (RRF)
│   ├── reranker.py                # Cross-Encoder candidate re-ranking module
│   ├── generator.py               # Prompt synthesis with bracket citations & guardrails
│   ├── evaluator.py               # Automated RAGAS evaluation suite & CI/CD quality gate
│   └── agent.py                   # Multi-Tool ReAct Router Agent
│
└── tests/
    └── test_rag_pipeline.py       # Automated unit & integration test suite (7 tests)
```

---

## 🚀 Quickstart & Execution

### 1. Run the Full Production Showcase & CI/CD Audit (CLI)
```bash
python day_04/enterprise_financial_compliance_rag/main.py
```
Outputs complete step-by-step agent reasoning, tool dispatching, grounded responses with bracket citations, and the automated RAGAS CI/CD quality gate audit (`BUILD PASSED`).

### 2. Run the Unit & Integration Test Suite
```bash
python -m unittest day_04/enterprise_financial_compliance_rag/tests/test_rag_pipeline.py
```
Executes 7 unit tests covering document ingestion, chunk overlap integrity, BM25 exact error code retrieval, agent routing, GL account aggregations, procurement tiers, and RAGAS thresholds.

### 3. Launch the Interactive Classroom Demonstration App (Streamlit)
```bash
streamlit run day_04/enterprise_financial_compliance_rag/app.py
```
Opens a high-end web dashboard featuring:
- **Audit Copilot**: Real-time ReAct agent trajectory inspection.
- **Hybrid Search Deep-Dive**: Side-by-side Dense Vector vs. BM25 vs. RRF vs. Re-ranker score inspection.
- **General Ledger Analytics**: Interactive ERP pivot tables and variance metrics.
- **Live RAGAS Audit**: Real-time evaluation scorecard measuring Faithfulness, Relevancy, Precision, and Recall.
- **Document Explorer**: Full text inspection of SEC filings, policies, and contracts.

---

## 🛡️ Enterprise Evaluation Benchmarks (RAGAS Triad)
Every commit is validated against four strict assertions:
| Metric | Threshold | Focus Area |
|---|---|---|
| **Faithfulness** | $\ge 0.85$ | Groundedness in retrieved reference text; zero hallucinations |
| **Answer Relevancy** | $\ge 0.80$ | Query alignment without conversational wandering |
| **Context Precision** | $\ge 0.75$ | Signal-to-noise ratio at top retrieval ranks |
| **Context Recall** | $\ge 0.75$ | Completeness of retrieved facts against ground truth |
