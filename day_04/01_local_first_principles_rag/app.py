"""
app.py
Production-Grade Streamlit Interactive Demonstration Dashboard
Enterprise Financial & Compliance Multi-Agent RAG Assistant (Module 4)
"""

import os
import sys
import time
import pandas as pd
import streamlit as st

# Configure page metadata
st.set_page_config(
    page_title="CloudCorp Enterprise Compliance & Financial RAG Copilot",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.loaders import EnterpriseDocumentLoader
from src.chunker import EnterpriseRecursiveChunker
from src.embedder import EnterpriseEmbedder
from src.vector_store import EnterpriseVectorStore
from src.hybrid_retriever import EnterpriseHybridRetriever
from src.reranker import EnterpriseReranker
from src.generator import EnterpriseGroundedGenerator
from src.evaluator import EnterpriseRAGASEvaluator
from src.agent import EnterpriseMultiAgentRouter

# Custom Modern Styling
st.markdown("""
<style>
    .reportview-container {
        background-color: #0f172a;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px;
        color: #f8fafc;
        margin-bottom: 12px;
    }
    .badge-pass {
        background-color: #065f46;
        color: #34d399;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-fail {
        background-color: #7f1d1d;
        color: #f87171;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .citation-tag {
        background-color: #1e3a8a;
        color: #93c5fd;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: bold;
        font-family: monospace;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b;
        border-radius: 6px 6px 0 0;
        color: #94a3b8;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def initialize_system():
    """Initializes and caches the enterprise RAG components."""
    data_dir = os.path.join(BASE_DIR, "data")
    all_docs, raw_ledger = EnterpriseDocumentLoader.load_all_enterprise_documents(data_dir)
    
    chunker = EnterpriseRecursiveChunker(chunk_size=320, chunk_overlap=50)
    chunks = chunker.chunk_documents(all_docs)

    embedder = EnterpriseEmbedder(dimension=256)
    vector_store = EnterpriseVectorStore(embedder)
    vector_store.add_chunks(chunks)

    retriever = EnterpriseHybridRetriever(vector_store, rrf_k=60)
    reranker = EnterpriseReranker()
    generator = EnterpriseGroundedGenerator()
    evaluator = EnterpriseRAGASEvaluator()

    agent = EnterpriseMultiAgentRouter(
        retriever=retriever,
        reranker=reranker,
        generator=generator,
        raw_ledger=raw_ledger
    )

    return {
        "all_docs": all_docs,
        "raw_ledger": raw_ledger,
        "chunks": chunks,
        "vector_store": vector_store,
        "retriever": retriever,
        "reranker": reranker,
        "generator": generator,
        "evaluator": evaluator,
        "agent": agent,
        "data_dir": data_dir
    }

sys_state = initialize_system()

# Sidebar: System Status & Presets
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
    st.title("Enterprise RAG")
    st.caption("Module 4: Multi-Agent Financial & Compliance Copilot")
    st.markdown("---")

    st.subheader("📊 Ingested Knowledge Base")
    st.write(f"• **Raw Documents**: `{len(sys_state['all_docs'])}`")
    st.write(f"• **Indexed Chunks**: `{len(sys_state['chunks'])}`")
    st.write(f"• **Ledger Records**: `{len(sys_state['raw_ledger'])}`")
    st.write(f"• **Retrieval Architecture**: `Dense + BM25 + RRF + BGE Re-ranker`")
    st.markdown("---")

    st.subheader("🎯 Real-World Scenarios")
    preset_scenarios = {
        "Scenario 1: API Key & Secrets Governance": {
            "query": "What is the mandatory rotation cycle for enterprise API keys, and what happens if a key is unrotated?",
            "ground_truth": "All production API keys must be rotated every 90 calendar days. Keys unrotated after 95 days are automatically revoked."
        },
        "Scenario 2: SRE Error Code Ingestion Failure": {
            "query": "What causes error code ERR_STREAM_BUFFER_OVERFLOW_504 and what is the failover time?",
            "ground_truth": "Error code ERR_STREAM_BUFFER_OVERFLOW_504 occurs during telemetry streaming packet fragmentation, failing over to S3 within 180 seconds."
        },
        "Scenario 3: GlobalBank Cloud Contract & SLA": {
            "query": "Under MSA-GB-2024-8831 with GlobalBank, what service credit applies for Tier 2 uptime breaches and what is the liability cap?",
            "ground_truth": "Under MSA-GB-2024-8831, Tier 2 monthly uptime between 99.00% and 99.89% provides a 25% credit, and total liability is capped at $15,000,000."
        },
        "Scenario 4: Engineering-AI Q3 Ledger Variance": {
            "query": "What was our total actual spend and budget variance for the Engineering-AI department in Q3?",
            "ground_truth": "Engineering-AI incurred actual spend of $17,450,000 against $18,000,000 budget, achieving a favorable $550,000 under-budget variance."
        },
        "Scenario 5: GL Account 5120 Outage Penalties": {
            "query": "What is the total spend and budget variance across all quarters for GL-5120?",
            "ground_truth": "GL-5120 incurred total spend of $1,710,000 against $1,500,000 budget with $210,000 over-budget variance due to Q3 GlobalBank outage credit."
        },
        "Scenario 6: Procurement Approval Validator": {
            "query": "What authorization tier and approvals are required to procure a $350,000 GPU cluster?",
            "ground_truth": "Authorization Tier 3: CFO and CISO dual authorization required for $350,000."
        },
        "Scenario 7: Out-of-Domain Guardrail Defense": {
            "query": "What is the company employee discount for personal luxury resort vacations in Hawaii?",
            "ground_truth": "Insufficient context: The provided enterprise documentation does not contain this information."
        }
    }

    selected_preset_key = st.selectbox(
        "Select an Enterprise Test Scenario:",
        list(preset_scenarios.keys()),
        index=0
    )
    selected_preset = preset_scenarios[selected_preset_key]

# Main Header
st.title("🏢 CloudCorp Enterprise Compliance & Financial Copilot")
st.markdown(
    "**Production Multi-Agent RAG System** combining **Hybrid BM25 + Vector Retrieval**, "
    "**Cross-Encoder Reranking**, **Exact Deterministic Ledger Math**, and **Automated RAGAS Quality Gates**."
)

tab_copilot, tab_retrieval, tab_ledger, tab_ragas, tab_corpus = st.tabs([
    "💬 Audit Copilot & Agent Reasoning",
    "🔍 Hybrid Search & Reranking Deep-Dive",
    "📊 General Ledger Analytics (SQL/Deterministic)",
    "🛡️ RAGAS CI/CD Quality Gate",
    "📂 Enterprise Documents & Contracts"
])

# ------------------------------------------------------------------------------
# TAB 1: AUDIT COPILOT & AGENT REASONING
# ------------------------------------------------------------------------------
with tab_copilot:
    st.subheader("Autonomous ReAct Audit Assistant")
    
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        user_query = st.text_input(
            "Enter Auditor or Compliance Question:",
            value=selected_preset["query"]
        )
    with col_btn:
        st.write("")
        st.write("")
        run_query = st.button("🚀 Execute Audit", use_container_width=True, type="primary")

    if run_query or user_query:
        t_start = time.perf_counter()
        agent_result = sys_state["agent"].execute(user_query)
        latency_ms = (time.perf_counter() - t_start) * 1000.0

        st.markdown("### 🤖 Autonomous Agent ReAct Trajectory")
        for step in agent_result.steps:
            with st.container():
                st.info(f"**🧠 Agent Thought:** {step.thought}")
                col_act, col_inp = st.columns(2)
                with col_act:
                    st.success(f"**⚡ Action Dispatched:** `{step.action}`")
                with col_inp:
                    st.code(f"Input: {step.action_input}", language="json")

        st.markdown("### 📋 Verified Enterprise Response")
        st.markdown(f"> {agent_result.final_response}")

        st.caption(f"⚡ Total End-to-End Latency: **{latency_ms:.2f} ms** | Dispatched Tool: `{agent_result.steps[0].action}`")

# ------------------------------------------------------------------------------
# TAB 2: HYBRID SEARCH & RERANKING DEEP-DIVE
# ------------------------------------------------------------------------------
with tab_retrieval:
    st.subheader("Dual-Engine Retrieval & Cross-Encoder Reranking Analysis")
    st.markdown(
        "Demonstrates how **Sparse BM25** protects against lexical miss for exact error codes or contract identifiers, "
        "while **Dense Vectors** capture conceptual semantics, fused via **Reciprocal Rank Fusion (RRF)**."
    )

    query_to_analyze = st.text_input(
        "Analyze Retrieval for Query:",
        value=user_query if user_query else selected_preset["query"],
        key="retrieval_analysis_query"
    )

    if query_to_analyze:
        retriever = sys_state["retriever"]
        reranker = sys_state["reranker"]

        cands = retriever.retrieve(query_to_analyze, top_k=6)
        reranked = reranker.rerank(query_to_analyze, cands, top_n=4)

        st.markdown("#### 🏆 Top Candidates After Cross-Encoder Reranking")
        for rank, (chunk, rerank_score) in enumerate(reranked, 1):
            source = chunk.metadata.get("source", "unknown")
            section = chunk.metadata.get("section", "General")
            
            with st.expander(f"Rank #{rank} | Rerank Score: {rerank_score:.3f} | {source} ({section})", expanded=(rank == 1)):
                st.markdown(f"**Content:**\n\n{chunk.text}")
                st.json({
                    "doc_id": chunk.doc_id,
                    "source_file": source,
                    "section": section,
                    "rerank_score": round(rerank_score, 4)
                })

# ------------------------------------------------------------------------------
# TAB 3: GENERAL LEDGER ANALYTICS (DETERMINISTIC)
# ------------------------------------------------------------------------------
with tab_ledger:
    st.subheader("General Ledger ERP Transactions & Deterministic SQL Analytics")
    st.markdown(
        "Enterprise financial inquiries are never passed to an ungrounded LLM for mathematical calculation. "
        "The ReAct Router executes deterministic aggregation across the immutable chart of accounts."
    )

    df_ledger = pd.DataFrame(sys_state["raw_ledger"])
    # Convert numeric columns
    for col in ["allocated_budget_usd", "actual_spend_usd", "variance_usd", "variance_percent"]:
        if col in df_ledger.columns:
            df_ledger[col] = pd.to_numeric(df_ledger[col], errors="coerce")

    # Filters
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        dept_options = ["All Departments"] + sorted(df_ledger["department_name"].unique().tolist())
        selected_dept = st.selectbox("Filter Department:", dept_options)
    with col_f2:
        qtr_options = ["All Quarters"] + sorted(df_ledger["quarter"].unique().tolist())
        selected_qtr = st.selectbox("Filter Quarter:", qtr_options)
    with col_f3:
        status_options = ["All Statuses"] + sorted(df_ledger["status"].unique().tolist())
        selected_status = st.selectbox("Filter Status:", status_options)

    filtered_df = df_ledger.copy()
    if selected_dept != "All Departments":
        filtered_df = filtered_df[filtered_df["department_name"] == selected_dept]
    if selected_qtr != "All Quarters":
        filtered_df = filtered_df[filtered_df["quarter"] == selected_qtr]
    if selected_status != "All Statuses":
        filtered_df = filtered_df[filtered_df["status"] == selected_status]

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    tot_budget = filtered_df["allocated_budget_usd"].sum()
    tot_spend = filtered_df["actual_spend_usd"].sum()
    net_var = tot_spend - tot_budget
    over_budget_count = (filtered_df["status"] == "Over-Budget").sum()

    col_m1.metric("Total Budget", f"${tot_budget:,.2f}")
    col_m2.metric("Actual Spend", f"${tot_spend:,.2f}")
    col_m3.metric("Net Variance", f"${net_var:+,.2f}", delta_color="inverse")
    col_m4.metric("Over-Budget Lines", f"{over_budget_count}")

    st.dataframe(filtered_df, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 4: RAGAS CI/CD QUALITY GATE
# ------------------------------------------------------------------------------
with tab_ragas:
    st.subheader("Automated RAGAS CI/CD Quality Gate Audit")
    st.markdown(
        "Continuous evaluation framework measuring the **RAG Triad** (Faithfulness, Answer Relevancy, "
        "Context Precision, and Context Recall) with hard assertion thresholds to block hallucinated releases."
    )

    col_eval_q, col_eval_gt = st.columns(2)
    with col_eval_q:
        eval_q = st.text_input("Evaluation Question:", value=selected_preset["query"], key="ragas_eval_q")
    with col_eval_gt:
        eval_gt = st.text_input("Target Ground Truth:", value=selected_preset["ground_truth"], key="ragas_eval_gt")

    if st.button("🛡️ Run Automated RAGAS Audit", type="primary"):
        retriever = sys_state["retriever"]
        reranker = sys_state["reranker"]
        generator = sys_state["generator"]
        evaluator = sys_state["evaluator"]

        cands = retriever.retrieve(eval_q, top_k=6)
        reranked = reranker.rerank(eval_q, cands, top_n=3)
        grounded = generator.generate(eval_q, reranked)
        contexts = [c.text for c, _ in reranked]

        metrics = evaluator.evaluate_sample(
            question=eval_q,
            answer=grounded.answer,
            contexts=contexts,
            ground_truth=eval_gt
        )

        col_g1, col_g2, col_g3, col_g4 = st.columns(4)
        col_g1.metric("Faithfulness", f"{metrics.faithfulness:.3f}", delta=">= 0.85 Target")
        col_g2.metric("Answer Relevancy", f"{metrics.answer_relevancy:.3f}", delta=">= 0.80 Target")
        col_g3.metric("Context Precision", f"{metrics.context_precision:.3f}", delta=">= 0.75 Target")
        col_g4.metric("Context Recall", f"{metrics.context_recall:.3f}", delta=">= 0.75 Target")

        if metrics.passed_quality_gate:
            st.success("✅ **CI/CD STATUS: BUILD PASSED.** Zero hallucinations detected; all benchmarks satisfied.")
        else:
            st.error("❌ **CI/CD STATUS: BUILD FAILED.** Quality metrics breached minimum thresholds.")

        with st.expander("Inspect Evaluated Answer & Retrieved Grounding Contexts", expanded=True):
            st.markdown(f"**Synthesized Answer:**\n> {grounded.answer}")
            st.markdown("**Grounding Contexts:**")
            for i, ctx in enumerate(contexts, 1):
                st.write(f"**Context {i}:** {ctx}")

# ------------------------------------------------------------------------------
# TAB 5: ENTERPRISE DOCUMENTS & CONTRACTS
# ------------------------------------------------------------------------------
with tab_corpus:
    st.subheader("Authoritative Corporate Corpus")
    
    doc_choice = st.radio(
        "Select Enterprise Document:",
        [
            "SEC Form 10-Q (sec_filing_q3_cloudcorp.md)",
            "Corporate Compliance Policy (corporate_compliance_policy.md)",
            "Master Services Agreement & SLA (enterprise_cloud_msa_and_sla.md)",
            "Financial Ledger 2025 (financial_ledger_2025.csv)"
        ],
        horizontal=True
    )

    fname_map = {
        "SEC Form 10-Q (sec_filing_q3_cloudcorp.md)": "sec_filing_q3_cloudcorp.md",
        "Corporate Compliance Policy (corporate_compliance_policy.md)": "corporate_compliance_policy.md",
        "Master Services Agreement & SLA (enterprise_cloud_msa_and_sla.md)": "enterprise_cloud_msa_and_sla.md",
        "Financial Ledger 2025 (financial_ledger_2025.csv)": "financial_ledger_2025.csv"
    }

    target_path = os.path.join(sys_state["data_dir"], fname_map[doc_choice])
    if os.path.exists(target_path):
        with open(target_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        if target_path.endswith(".csv"):
            st.dataframe(pd.read_csv(target_path), use_container_width=True)
        else:
            st.markdown(file_content)
