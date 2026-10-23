"""
app.py
Production-Grade ChatGPT & Gemini Style Interface
KIT College Student AI Copilot (Powered by LangGraph, LangChain & Google Gemini)
"""

import os
import sys
import time
import json
import streamlit as st
from dotenv import load_dotenv

# 1. Load environment variables immediately
load_dotenv()

# Configure page metadata
st.set_page_config(
    page_title="KIT College AI Copilot",
    page_icon="🎓",
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
from src.langgraph_agent import LangGraphCollegeCopilot

# Custom Modern ChatGPT / Gemini Styling
st.markdown("""
<style>
    /* Sleek container styling */
    .stChatFloatingInputContainer {
        bottom: 20px;
    }
    .badge-route {
        background-color: #1e1b4b;
        color: #a5b4fc;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.80rem;
        border: 1px solid #4338ca;
        display: inline-block;
        margin-bottom: 6px;
    }
    .badge-latency {
        background-color: #064e3b;
        color: #6ee7b7;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.80rem;
        border: 1px solid #059669;
        display: inline-block;
        margin-bottom: 6px;
    }
    .source-card {
        background: #1e293b;
        border-left: 3px solid #38bdf8;
        padding: 8px 12px;
        border-radius: 0 6px 6px 0;
        font-size: 0.84rem;
        margin-top: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. CACHED VECTOR STORE & PIPELINE BOOTSTRAP
# ------------------------------------------------------------------------------
@st.cache_resource(show_spinner="Initializing KIT College Vector Store & LangGraph Copilot...")
def initialize_system():
    data_dir = os.path.join(BASE_DIR, "data")
    all_docs, raw_rows = EnterpriseDocumentLoader.load_all_documents(data_dir)

    # 1. LangChain Recursive Chunking
    chunker = EnterpriseRecursiveChunker(chunk_size=320, chunk_overlap=50)
    all_chunks = chunker.chunk_documents(all_docs)

    # 2. LangChain Embeddings & Vector Store
    embedder = EnterpriseEmbedder(dimension=256)
    vector_store = EnterpriseVectorStore(embedder)
    vector_store.add_chunks(all_chunks)

    # 3. Save Disk Inspection Cache (Addresses student question: Where is vector stored?)
    cache_path = os.path.join(data_dir, ".vector_cache")
    catalog_file = vector_store.save_local_cache(cache_path)

    # 4. Hybrid Retriever & Re-ranker
    retriever = EnterpriseHybridRetriever(vector_store, rrf_k=60)
    reranker = EnterpriseReranker()
    generator = EnterpriseGroundedGenerator()

    # 5. Compiled LangGraph StateGraph Copilot
    copilot = LangGraphCollegeCopilot(
        retriever=retriever,
        reranker=reranker,
        generator=generator,
        course_catalog=raw_rows
    )

    return {
        "all_docs": all_docs,
        "all_chunks": all_chunks,
        "raw_rows": raw_rows,
        "vector_store": vector_store,
        "catalog_file": catalog_file,
        "copilot": copilot
    }

system = initialize_system()

# ------------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS & VECTOR STORAGE INSPECTION
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎓 KIT College AI Copilot")
    st.caption("Powered by LangChain, LangGraph & Google Gemini")
    st.markdown("---")

    # 1. Gemini Model Tier Selection
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        chosen_model = st.selectbox(
            "⚡ Active Gemini Model Tier:",
            options=["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash-lite"],
            index=0,
            help="Select the modern Gemini model tier for grounded synthesis."
        )
        os.environ["GEMINI_MODEL"] = chosen_model
        st.success(f"Connected: **{chosen_model}**")
    else:
        st.info("💻 Engine: **Local Deterministic Fallback**\n*(Add GEMINI_API_KEY to .env to enable Gemini 3.8)*")

    # 2. Temperature Parameter (Requested by user)
    temperature = st.slider(
        "🎛️ Temperature (Creativity / Precision):",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.05,
        help="0.0 = Strictly factual & deterministic; 0.7 = Exploratory & conversational."
    )

    # 3. General Knowledge Mode (Requested by user)
    allow_general = st.toggle(
        "🌐 General Knowledge & Web Mode",
        value=True,
        help="When ON, answers both campus policy questions AND general questions (coding, science, concepts). When OFF, strictly enforces handbook boundary."
    )

    st.markdown("---")

    # 4. Where is the Vector DB Stored? (Student Educational Explainer)
    with st.expander("📁 Where is the Vector Database Stored?"):
        st.markdown("""
        **How Vector Storage Works Here:**
        1. **Runtime Execution**: Stored in **RAM memory** using LangChain's `InMemoryVectorStore`.
        2. **Why RAM?**: Ultra-fast cosine search without needing a cloud database server.
        3. **Does it convert every time?**: No! Streamlit caches it in memory via `@st.cache_resource`. It only computes embeddings once on startup.
        4. **Disk Inspection**: We also serialized the vectors to disk:
        `data/.vector_cache/vector_store_catalog.json`
        """)
        st.metric("Total Indexed Chunks", len(system["all_chunks"]))
        st.metric("Vector Dimensions", 256)

        # Inspect raw vector sample
        if st.checkbox("🔍 Inspect Sample Vector Coordinates"):
            sample_c = system["all_chunks"][0]
            st.caption(f"**Chunk 1**: {sample_c.text[:80]}...")
            sample_vec = system["vector_store"].embedder.embed_query(sample_c.text[:100])
            st.json({
                "source": sample_c.metadata.get("source"),
                "first_6_dimensions": [round(float(x), 4) for x in sample_vec[:6]],
                "total_dimensions": len(sample_vec)
            })

    st.markdown("---")

    # 5. Quick Sample Student Queries
    st.markdown("💡 **Sample Queries:**")
    sample_queries = [
        "Can I write the exam if my attendance is 68%?",
        "Who is teaching CS401 Machine Learning and credits?",
        "What is the hostel gate curfew and dinner time?",
        "What is the placement CGPA eligibility?",
        "Explain QuickSort algorithm in Python",
        "Can students bring jet skis to the pool?"
    ]
    for sq in sample_queries:
        if st.button(sq, key=f"btn_{sq[:15]}", use_container_width=True):
            st.session_state["queued_query"] = sq

    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

# ------------------------------------------------------------------------------
# 4. CHAT HISTORY INITIALIZATION
# ------------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": (
                "👋 Hello! I am your **KIT College AI Copilot**.\n\n"
                "I can assist you with:\n"
                "• **Academic Policies & Attendance**: Medical condonation rules, detention thresholds, CIA marks.\n"
                "• **Courses & Faculty**: Subject codes (e.g. `CS401`), instructor emails, credits, and exam schedules.\n"
                "• **Hostel & Placements**: Biometric curfew (8:30 PM), mess timings, Dream Offer cutoffs (10 LPA).\n"
                "• **General Knowledge**: Coding problems, engineering concepts, and general study questions.\n\n"
                "What would you like to ask today?"
            ),
            "trace": None
        }
    ]

# ------------------------------------------------------------------------------
# 5. RENDER CHAT INTERFACE (CHATGPT / GEMINI STYLE)
# ------------------------------------------------------------------------------
st.title("🎓 KIT College AI Copilot")
st.caption("A simple, production-grade conversational AI assistant powered by LangGraph StateGraph & LangChain")

# Display previous chat messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        # Collapsible Reasoning / LangGraph Trace (like Gemini / DeepSeek thought process)
        if msg.get("trace"):
            state = msg["trace"]
            with st.expander("🧠 View Reasoning & LangGraph Node Trace"):
                col_r, col_l = st.columns(2)
                with col_r:
                    st.markdown(f"<span class='badge-route'>Route: {state.get('route')}</span>", unsafe_allow_html=True)
                with col_l:
                    st.markdown(f"<span class='badge-latency'>Latency: {state.get('latency_ms', 0):.2f} ms</span>", unsafe_allow_html=True)

                st.markdown("**Trajectory Steps:**")
                for step in state.get("trace_steps", []):
                    st.markdown(f"• **{step.get('node')}**: {step.get('action')}")
                    if step.get("details"):
                        st.caption(f"  └─ {step.get('details')}")

                # Display retrieved chunks if available
                chunks = state.get("retrieved_chunks", [])
                if chunks:
                    st.markdown("**Retrieved Knowledge Chunks:**")
                    for c in chunks:
                        st.markdown(
                            f"<div class='source-card'><b>[Doc {c['rank']}] {c['source']} ({c['section']})</b><br>{c['text'][:180]}...</div>",
                            unsafe_allow_html=True
                        )

# ------------------------------------------------------------------------------
# 6. USER INPUT & EXECUTION
# ------------------------------------------------------------------------------
queued_prompt = st.session_state.pop("queued_query", None)
user_prompt = st.chat_input("Ask anything — about college rules, courses, attendance, or general questions...") or queued_prompt

if user_prompt:
    # 1. Append user message to history
    st.session_state["messages"].append({"role": "user", "content": user_prompt, "trace": None})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # 2. Execute Copilot through LangGraph StateGraph
    with st.chat_message("assistant"):
        with st.spinner("Thinking & searching knowledge base..."):
            state = system["copilot"].run(
                query=user_prompt,
                temperature=temperature,
                allow_general_knowledge=allow_general
            )

        # 3. Display Assistant Answer
        st.markdown(state["generation"])

        # 4. Display Collapsible Reasoning Trace
        with st.expander("🧠 View Reasoning & LangGraph Node Trace", expanded=False):
            col_r, col_l = st.columns(2)
            with col_r:
                st.markdown(f"<span class='badge-route'>Route: {state['route']}</span>", unsafe_allow_html=True)
            with col_l:
                st.markdown(f"<span class='badge-latency'>Latency: {state['latency_ms']:.2f} ms</span>", unsafe_allow_html=True)

            st.markdown("**Trajectory Steps:**")
            for step in state.get("trace_steps", []):
                st.markdown(f"• **{step.get('node')}**: {step.get('action')}")
                if step.get("details"):
                    st.caption(f"  └─ {step.get('details')}")

            chunks = state.get("retrieved_chunks", [])
            if chunks:
                st.markdown("**Retrieved Knowledge Chunks:**")
                for c in chunks:
                    st.markdown(
                        f"<div class='source-card'><b>[Doc {c['rank']}] {c['source']} ({c['section']})</b><br>{c['text'][:180]}...</div>",
                        unsafe_allow_html=True
                    )

        # 5. Append assistant message to session history
        st.session_state["messages"].append({
            "role": "assistant",
            "content": state["generation"],
            "trace": state
        })
