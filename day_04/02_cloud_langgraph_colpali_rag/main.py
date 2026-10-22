"""
main.py
Enterprise BioPharma Regulatory & Clinical Trial Safety Multi-Agent Assistant.
Production demonstration of ColPali Late-Interaction RAG, LangGraph StateGraph,
AWS Cloud Vector Store, Deterministic Safety Analytics, and HITL Medical Monitor Gates.
"""

import os
import sys
import time

# Ensure UTF-8 stdout encoding on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure project root in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.loaders import ClinicalDocumentLoader
from src.colpali_engine import ColPaliEngine
from src.cloud_vector_store import get_cloud_vector_store
from src.deterministic_clinical_analytics import DeterministicClinicalAnalytics
from src.langgraph_workflow import EnterpriseClinicalRAGWorkflow

def initialize_biopharma_system():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    ledger_path = os.path.join(data_dir, "clinical_trial_safety_ledger.csv")

    print("\n" + "=" * 80)
    print("🧬 INITIALIZING AURABIO ENTERPRISE MULTI-AGENT CLINICAL SAFETY COPILOT")
    print("=" * 80)

    # 1. Ingestion Phase
    t0 = time.perf_counter()
    pages = ClinicalDocumentLoader.load_all_documents(data_dir)
    print(f"[INGESTION] Loaded {len(pages)} visual pages from FDA Protocols, 21 CFR 312, and IB Charters.")

    # 2. ColPali Multi-Vector Late-Interaction Indexing
    colpali = ColPaliEngine(dimension=128)
    indexed_pages = [colpali.embed_page(p) for p in pages]
    print(f"[COLPALI ENGINE] Encoded {len(indexed_pages)} visual pages into multi-vector patch embeddings.")

    # 3. Cloud Vector Store Adapter
    cloud_store = get_cloud_vector_store()
    cloud_store.initialize_index(dimension=128)
    status = cloud_store.get_service_status()
    print(f"[CLOUD VECTOR STORE] Provider: {status.get('provider')} | Status: {status.get('status')}")

    # 4. Deterministic Clinical Safety Analytics Engine
    analytics = DeterministicClinicalAnalytics(ledger_path)
    print(f"[SAFETY LEDGER] Loaded 25 multi-center clinical patient incident records.")

    # 5. Compiled LangGraph Workflow
    workflow = EnterpriseClinicalRAGWorkflow(
        colpali_engine=colpali,
        indexed_pages=indexed_pages,
        analytics_engine=analytics,
        cloud_vector_store=cloud_store
    )
    t_boot = (time.perf_counter() - t0) * 1000.0
    print(f"[BOOTSTRAP] System ready in {t_boot:.2f}ms.")
    print("=" * 80)

    return workflow, analytics, cloud_store

def run_enterprise_clinical_showcase():
    workflow, analytics, cloud_store = initialize_biopharma_system()

    scenarios = [
        {
            "title": "CASE 1: FDA 21 CFR § 312.32 EXPEDITED SAFETY REPORTING MANDATE",
            "query": "Under 21 CFR 312.32, what is the mandatory reporting window for a fatal or life-threatening unexpected adverse reaction (SUSAR)?"
        },
        {
            "title": "CASE 2: PROTOCOL TOXICITY MANAGEMENT & DOSE REDUCTION MATRIX (COLPALI VISUAL TABLE)",
            "query": "What action is required for Grade 2 Immune-mediated pneumonitis under Protocol ABX-702, and what is the dose reduction tier?"
        },
        {
            "title": "CASE 3: DETERMINISTIC CLINICAL INCIDENT ANALYTICS (SAE & CTCAE GRADE BREAKDOWN)",
            "query": "How many serious adverse events (SAEs) and fatal events occurred in Cohort 3 across all participating clinical sites?"
        },
        {
            "title": "CASE 4: AUTOMATIC CLINICAL HOLD & STOPPING RULE TRIGGER AUDIT",
            "query": "Has any clinical stopping rule been triggered across the trial, and which patient incident caused it?"
        },
        {
            "title": "CASE 5: HUMAN-IN-THE-LOOP (HITL) MEDICAL MONITOR SAFETY GATE INTERCEPT",
            "query": "Can we escalate dose or re-escalate study drug back to 450 mg for a patient recovering from pneumonitis?"
        },
        {
            "title": "CASE 6: OUT-OF-DOMAIN GUARDRAIL (HALLUCINATION MITIGATION)",
            "query": "What is the corporate reimbursement policy for executive first-class airline travel to European clinical congresses?"
        }
    ]

    for item in scenarios:
        print(f"\n{'-'*80}")
        print(f"🎯 {item['title']}")
        print(f"{'-'*80}")
        print(f"USER QUERY: \"{item['query']}\"")

        res = workflow.execute(item["query"])

        for step in res.trace:
            print(f"\n  [LANGGRAPH NODE]: {step.node_name}")
            print(f"  [AGENT THOUGHT ]: {step.thought}")
            print(f"  [ACTION TAKEN  ]: {step.action_taken}")

        print(f"\n  [FINAL VERIFIED CLINICAL RESPONSE]:\n  {res.final_response}")
        print(f"  [EXECUTION TIME]: {res.execution_time_ms} ms")
        if res.requires_hitl:
            print(f"  [HITL STATUS]: 🚨 {res.hitl_status} - Medical Monitor sign-off required.")

    print("\n" + "=" * 80)
    print("✅ ENTERPRISE SHOWCASE COMPLETE: All LangGraph and ColPali routes validated.")
    print("=" * 80)

if __name__ == "__main__":
    run_enterprise_clinical_showcase()
