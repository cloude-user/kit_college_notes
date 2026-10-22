"""
app.py
Enterprise BioPharma Regulatory & Clinical Trial Safety Multi-Agent Copilot.
Production Streamlit Interactive Dashboard (Module 4 - Cloud & LangGraph Edition).
Demonstrating ColPali Visual-Language Late-Interaction, AWS Cloud Vector DB,
Deterministic Safety Analytics, and LangGraph Human-in-the-Loop Gates.
"""

import os
import sys
import time
import pandas as pd
import streamlit as st

# Configure page metadata
st.set_page_config(
    page_title="AuraBio Clinical Safety & Regulatory RAG Copilot",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure project root in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.loaders import ClinicalDocumentLoader
from src.colpali_engine import ColPaliEngine
from src.cloud_vector_store import get_cloud_vector_store
from src.deterministic_clinical_analytics import DeterministicClinicalAnalytics
from src.langgraph_workflow import EnterpriseClinicalRAGWorkflow

# Modern Clinical Dashboard Styling
st.markdown("""
<style>
    .reportview-container {
        background-color: #0b1120;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        color: #f8fafc;
        margin-bottom: 12px;
    }
    .badge-fda-pass {
        background-color: #064e3b;
        color: #34d399;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-fda-hold {
        background-color: #7f1d1d;
        color: #fca5a5;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .colpali-token-badge {
        background-color: #0369a1;
        color: #e0f2fe;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: bold;
        font-family: monospace;
        margin-right: 4px;
        display: inline-block;
    }
    .hitl-alert-box {
        background: #450a0a;
        border: 2px solid #ef4444;
        border-radius: 10px;
        padding: 16px;
        color: #fecaca;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def initialize_system():
    data_dir = os.path.join(BASE_DIR, "data")
    ledger_path = os.path.join(data_dir, "clinical_trial_safety_ledger.csv")

    pages = ClinicalDocumentLoader.load_all_documents(data_dir)
    colpali = ColPaliEngine(dimension=128)
    indexed_pages = [colpali.embed_page(p) for p in pages]

    cloud_store = get_cloud_vector_store()
    cloud_store.initialize_index(dimension=128)

    analytics = DeterministicClinicalAnalytics(ledger_path)
    workflow = EnterpriseClinicalRAGWorkflow(
        colpali_engine=colpali,
        indexed_pages=indexed_pages,
        analytics_engine=analytics,
        cloud_vector_store=cloud_store
    )

    return {
        "data_dir": data_dir,
        "ledger_path": ledger_path,
        "pages": pages,
        "indexed_pages": indexed_pages,
        "colpali": colpali,
        "cloud_store": cloud_store,
        "analytics": analytics,
        "workflow": workflow
    }

sys_state = initialize_system()

# Sidebar: System Status & Presets
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/dna-helix.png", width=64)
    st.title("AuraBio Copilot")
    st.caption("Module 4: Enterprise Cloud & LangGraph Visual RAG")
    st.markdown("---")

    cloud_status = sys_state["cloud_store"].get_service_status()
    st.subheader("☁️ Cloud Vector Infrastructure")
    st.write(f"• **Provider**: `{cloud_status.get('provider')}`")
    st.write(f"• **Status**: `{cloud_status.get('status')}`")
    st.write(f"• **Visual Pages Indexed**: `{len(sys_state['indexed_pages'])}`")
    st.write(f"• **Retrieval Engine**: `ColPali Multi-Vector (MaxSim)`")
    st.markdown("---")

    st.subheader("🎯 Real-World Clinical Presets")
    preset_scenarios = {
        "Scenario 1: FDA 21 CFR § 312.32 7-Day Alert": {
            "query": "Under 21 CFR 312.32, what is the mandatory reporting window for a fatal or life-threatening unexpected adverse reaction (SUSAR)?"
        },
        "Scenario 2: ColPali Visual Toxicity Matrix": {
            "query": "What action is required for Grade 2 Immune-mediated pneumonitis under Protocol ABX-702, and what is the dose reduction tier?"
        },
        "Scenario 3: Deterministic Cohort 3 SAE Statistics": {
            "query": "How many serious adverse events (SAEs) and fatal events occurred in Cohort 3 across all participating clinical sites?"
        },
        "Scenario 4: Protocol Stopping Rule & Clinical Hold": {
            "query": "Has any clinical stopping rule been triggered across the trial, and which patient incident caused it?"
        },
        "Scenario 5: Human-in-the-Loop Dose Escalation Gate": {
            "query": "Can we escalate dose or re-escalate study drug back to 450 mg for a patient recovering from pneumonitis?"
        },
        "Scenario 6: Out-of-Domain Guardrail Mitigation": {
            "query": "What is the corporate reimbursement policy for executive first-class airline travel to European clinical congresses?"
        }
    }

    selected_preset_key = st.selectbox(
        "Select a Clinical Audit Scenario:",
        list(preset_scenarios.keys()),
        index=0
    )
    selected_preset = preset_scenarios[selected_preset_key]

# Main Header
st.title("🧬 AuraBio Oncology Phase III Clinical & Regulatory Copilot")
st.markdown(
    "**Enterprise Multi-Agent RAG System** combining **ColPali Visual Late-Interaction**, "
    "**LangGraph Directed StateGraph**, **AWS Cloud Vector Store Connectors**, "
    "**Exact Deterministic Safety Math**, and **Human-in-the-Loop (HITL) Medical Monitor Gates**."
)

tab_copilot, tab_colpali, tab_ledger, tab_cloud, tab_corpus = st.tabs([
    "💬 Autonomous Clinical Copilot (LangGraph)",
    "👁️ ColPali Visual Late-Interaction",
    "📊 Patient Incident Safety Analytics",
    "☁️ AWS Cloud Vector Store Architecture",
    "📂 FDA Protocols & Regulatory Repository"
])

# ------------------------------------------------------------------------------
# TAB 1: AUTONOMOUS CLINICAL COPILOT & LANGGRAPH TRAJECTORY
# ------------------------------------------------------------------------------
with tab_copilot:
    st.subheader("LangGraph Multi-Agent Clinical Safety Assistant")

    col_inp, col_btn = st.columns([4, 1])
    with col_inp:
        user_query = st.text_input(
            "Enter Regulatory, Protocol, or Clinical Safety Question:",
            value=selected_preset["query"]
        )
    with col_btn:
        st.write("")
        st.write("")
        run_query = st.button("🚀 Execute Audit", use_container_width=True, type="primary")

    if run_query or user_query:
        workflow = sys_state["workflow"]
        state_result = workflow.execute(user_query)

        # HITL Alert Banner if triggered
        if state_result.requires_hitl and state_result.hitl_status == "PENDING_APPROVAL":
            st.markdown(f"""
            <div class="hitl-alert-box">
                <h4>🚨 HUMAN-IN-THE-LOOP (HITL) MEDICAL MONITOR INTERCEPT</h4>
                <p>{state_result.hitl_reason}</p>
                <b>Status:</b> <code>PENDING_PHYSICIAN_AUTHORIZATION</code> (21 CFR Part 11)
            </div>
            """, unsafe_allow_html=True)

            col_auth1, col_auth2 = st.columns(2)
            with col_auth1:
                if st.button("✍️ Electronically Sign Protocol Waiver (Physician Sign-Off)", type="primary"):
                    st.success("✅ Protocol Amendment Authorization Signed: Medical Monitor ID #DR-8841-ONC.")
            with col_auth2:
                if st.button("❌ Reject Dose Modification & Enforce Protocol Discontinuation"):
                    st.info("🛑 Protocol Discontinuation Enforced. Patient remaining on standard supportive care.")

        st.markdown("### 🤖 LangGraph Multi-Agent Execution Trajectory")
        for step in state_result.trace:
            with st.container():
                st.info(f"**📍 LangGraph Node:** `{step.node_name}`\n\n**🧠 Agent Reasoning:** {step.thought}")
                col_act, col_pay = st.columns([1, 2])
                with col_act:
                    st.success(f"**⚡ Action Taken:** `{step.action_taken}`")
                with col_pay:
                    st.json(step.payload)

        st.markdown("### 📋 Verified Regulatory & Clinical Response")
        st.markdown(f"> {state_result.final_response}")

        st.caption(f"⚡ Total End-to-End Latency: **{state_result.execution_time_ms:.2f} ms** | Classified Intent: `{state_result.intent}`")

# ------------------------------------------------------------------------------
# TAB 2: COLPALI VISUAL LATE-INTERACTION DEEP DIVE
# ------------------------------------------------------------------------------
with tab_colpali:
    st.subheader("ColPali Vision-Language Late-Interaction Scoring (MaxSim)")
    st.markdown(
        "ColPali eliminates OCR parsing loss on multi-column protocols and toxicity grids by embedding "
        "entire page layouts as multi-vector patch embeddings. Queries score candidate pages using **MaxSim**:"
    )
    st.latex(r"\text{Score}(Q, D) = \sum_{i \in Q} \max_{j \in D} (q_i \cdot d_j)")

    colpali_query = st.text_input(
        "Enter Query to Inspect Visual Patch Token Alignment:",
        value=user_query if user_query else selected_preset["query"],
        key="colpali_inspect_query"
    )

    if colpali_query:
        colpali = sys_state["colpali"]
        indexed = sys_state["indexed_pages"]
        hits = colpali.retrieve(colpali_query, indexed, top_k=3)

        st.markdown("#### 🏆 Top ColPali Visual Candidates")
        for rank, hit in enumerate(hits, 1):
            with st.expander(f"Rank #{rank} | MaxSim Score: {hit.maxsim_score:.2f} | {hit.source_file} (Page {hit.page_number})", expanded=(rank == 1)):
                st.markdown(f"**Document Page Content ({hit.metadata.get('section', 'General')}):**")
                st.markdown(hit.text_content)

                st.markdown("**🔍 Query Token Late-Interaction Alignment Map:**")
                if hit.token_alignment:
                    badge_html = " ".join([f'<span class="colpali-token-badge">{tok}: {score:.2f}</span>' for tok, score in list(hit.token_alignment.items())[:8]])
                    st.markdown(badge_html, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 3: PATIENT INCIDENT SAFETY ANALYTICS (DETERMINISTIC)
# ------------------------------------------------------------------------------
with tab_ledger:
    st.subheader("Patient Safety Incident Ledger & Deterministic Analytics")
    st.markdown(
        "Clinical safety statistics are strictly computed deterministically over raw adverse event records "
        "to guarantee zero math hallucination for FDA MedWatch Form 3500A reporting."
    )

    df_safety = pd.read_csv(sys_state["ledger_path"])

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        cohort_opts = ["All Cohorts"] + sorted(df_safety["dose_cohort"].unique().tolist())
        sel_cohort = st.selectbox("Filter Dose Cohort:", cohort_opts)
    with col_f2:
        site_opts = ["All Sites"] + sorted(df_safety["site_name"].unique().tolist())
        sel_site = st.selectbox("Filter Clinical Site:", site_opts)

    filt_df = df_safety.copy()
    if sel_cohort != "All Cohorts":
        filt_df = filt_df[filt_df["dose_cohort"] == sel_cohort]
    if sel_site != "All Sites":
        filt_df = filt_df[filt_df["site_name"] == sel_site]

    tot_incidents = len(filt_df)
    tot_sae = (filt_df["is_sae"].str.lower() == "yes").sum()
    tot_fatal = (filt_df["outcome"].str.lower() == "fatal").sum()
    gr4_count = (filt_df["ctcae_grade"] == "Grade 4").sum()

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Total Incident Records", f"{tot_incidents}")
    col_m2.metric("Serious Adverse Events (SAE)", f"{tot_sae}")
    col_m3.metric("Grade 4 Severe Toxicities", f"{gr4_count}")
    col_m4.metric("Fatalities (Grade 5)", f"{tot_fatal}")

    if tot_fatal > 0 or (tot_incidents > 0 and (gr4_count / tot_incidents) >= 0.15):
        st.error("🚨 **PROTOCOL STOPPING CRITERIA BREACHED**: Safety Review Committee automatic clinical hold triggered.")
    else:
        st.success("✅ **SAFETY BOUNDARIES COMPLIANT**: Within allowable dose escalation tolerances.")

    st.dataframe(filt_df, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 4: AWS CLOUD VECTOR STORE ARCHITECTURE
# ------------------------------------------------------------------------------
with tab_cloud:
    st.subheader("Enterprise Cloud Vector Architecture on AWS")
    st.markdown(
        "This project features a pluggable cloud vector adapter with native connectors for AWS production environments:"
    )

    st.markdown("""
    | Vector Store Target | AWS Implementation | Pricing Profile | Best Used For |
    | :--- | :--- | :--- | :--- |
    | **Amazon OpenSearch Serverless (AOSS)** | `opensearch-py` + SigV4 IAM Authentication | Minimum 4 OCUs (~$700/mo) | High-volume enterprise cloud search |
    | **AWS RDS PostgreSQL + pgvector** | `psycopg2` + HNSW cosine index | Low-Cost (~$15-$25/mo or Free Tier) | **Recommended for cost-effective production** |
    | **Pinecone Serverless (AWS us-east-1)** | `pinecone-client` | Pay-per-query ($0 free tier) | Serverless fast prototyping |
    | **Dev Cloud Simulator** | Pure NumPy Vectorized Engine | $0 / Offline | Development, CI/CD, and Local testing |
    """)

    st.json(sys_state["cloud_store"].get_service_status())

# ------------------------------------------------------------------------------
# TAB 5: REGULATORY & PROTOCOL REPOSITORY
# ------------------------------------------------------------------------------
with tab_corpus:
    st.subheader("Authoritative Clinical Protocol Repository")

    doc_sel = st.radio(
        "Select Clinical Regulatory Document:",
        [
            "FDA Clinical Trial Protocol (ABX-702-CLIN-301)",
            "FDA 21 CFR Part 312 & ICH GCP Guidelines",
            "Investigator Brochure & Clinical Safety Charter",
            "Clinical Safety Incident Ledger (CSV)"
        ],
        horizontal=True
    )

    file_map = {
        "FDA Clinical Trial Protocol (ABX-702-CLIN-301)": "fda_clinical_trial_protocol_abx702.md",
        "FDA 21 CFR Part 312 & ICH GCP Guidelines": "fda_21cfr_part312_ich_gcp_guidelines.md",
        "Investigator Brochure & Clinical Safety Charter": "investigator_brochure_safety_charter.md",
        "Clinical Safety Incident Ledger (CSV)": "clinical_trial_safety_ledger.csv"
    }

    target_file = os.path.join(sys_state["data_dir"], file_map[doc_sel])
    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()
        if target_file.endswith(".csv"):
            st.dataframe(pd.read_csv(target_file), use_container_width=True)
        else:
            st.markdown(content)
