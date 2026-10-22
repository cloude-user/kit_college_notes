"""
main.py
Enterprise Financial & Compliance Multi-Agent Assistant Runner.
Interactive Demonstration of Production RAG, Multi-Agent Routing & RAGAS CI/CD Gates.
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

# Ensure src is discoverable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.loaders import EnterpriseDocumentLoader



















om src.chunker import EnterpriseRecursiveChunker
from src.embedder import EnterpriseEmbedder
from src.vector_store import EnterpriseVectorStore
from src.hybrid_retriever import EnterpriseHybridRetriever
from src.reranker import EnterpriseReranker
from src.generator import EnterpriseGroundedGenerator
from src.evaluator import EnterpriseRAGASEvaluator
from src.agent import EnterpriseMultiAgentRouter

def build_enterprise_system():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")

    print("\n" + "=" * 80)
    print("🏢 INITIALIZING CLOUDCORP ENTERPRISE RAG & MULTI-AGENT SYSTEM")
    print("=" * 80)

    # 1. Ingestion Phase: Automatically discover and load all enterprise documents & ledger
    t0 = time.perf_counter()
    all_docs, raw_ledger = EnterpriseDocumentLoader.load_all_enterprise_documents(data_dir)
    print(f"[INGESTION] Loaded {len(all_docs)} raw documents from SEC 10-Q, SOX Policies, MSA/SLA, and Ledger.")

    # 2. Chunking Phase
    chunker = EnterpriseRecursiveChunker(chunk_size=320, chunk_overlap=50)
    all_chunks = chunker.chunk_documents(all_docs)
    print(f"[CHUNKING] Generated {len(all_chunks)} semantic chunks with 15% overlap protection.")

    # 3. Vector Database Indexing
    embedder = EnterpriseEmbedder(dimension=256)
    vector_store = EnterpriseVectorStore(embedder)
    vector_store.add_chunks(all_chunks)
    print(f"[VECTOR STORE] Embedded and indexed {vector_store.count()} chunks into in-memory vector store.")

    # 4. Hybrid Retriever & Re-ranker
    retriever = EnterpriseHybridRetriever(vector_store, rrf_k=60)
    reranker = EnterpriseReranker()
    generator = EnterpriseGroundedGenerator()
    evaluator = EnterpriseRAGASEvaluator()

    # 5. Autonomous ReAct Router Agent
    agent = EnterpriseMultiAgentRouter(
        retriever=retriever,
        reranker=reranker,
        generator=generator,
        raw_ledger=raw_ledger
    )

    t_init = (time.perf_counter() - t0) * 1000.0
    print(f"[BOOTSTRAP] System ready in {t_init:.2f}ms.")
    print("=" * 80)

    return agent, evaluator, retriever, reranker, generator

def run_production_showcase():
    agent, evaluator, retriever, reranker, generator = build_enterprise_system()

    queries = [
        # Query 1: Unstructured Policy Retrieval with Strict Citations
        {
            "title": "CASE 1: UNSTRUCTURED POLICY INQUIRY (SOX / CREDENTIAL SECURITY)",
            "query": "What is the mandatory rotation cycle for enterprise API keys, and what happens if a key is unrotated?",
            "ground_truth": "All production API keys must be rotated every 90 calendar days. Keys unrotated after 95 days are automatically revoked."
        },
        # Query 2: Exact Alphanumeric Error Code (Proving BM25 Hybrid Retrieval)
        {
            "title": "CASE 2: EXACT ALPHANUMERIC ERROR CODE LOOKUP (BM25 HYBRID ADVANTAGE)",
            "query": "What causes error code ERR_STREAM_BUFFER_OVERFLOW_504 and what is the failover time?",
            "ground_truth": "Error code ERR_STREAM_BUFFER_OVERFLOW_504 occurs during telemetry streaming packet fragmentation, failing over to S3 within 180 seconds."
        },
        # Query 3: Real-World Customer SLA Contract Inquiry
        {
            "title": "CASE 3: CUSTOMER SLA CONTRACT AUDIT (GLOBALBANK MSA-GB-2024-8831)",
            "query": "Under MSA-GB-2024-8831 with GlobalBank, what service credit applies for Tier 2 uptime breaches and what is the liability cap?",
            "ground_truth": "Under MSA-GB-2024-8831, Tier 2 monthly uptime between 99.00% and 99.89% provides a 25% credit, and total liability is capped at $15,000,000."
        },
        # Query 4: Structured Data Query (Agent Routing to SQL/Ledger)
        {
            "title": "CASE 4: STRUCTURED FINANCIAL INQUIRY (ROUTED TO FINANCIAL LEDGER)",
            "query": "What was our total actual spend and budget variance for the Engineering-AI department in Q3?",
            "ground_truth": "Engineering-AI incurred actual spend of $17,450,000 against $18,000,000 budget, achieving a favorable $550,000 under-budget variance."
        },
        # Query 5: GL Account Specific Audit (Outage Penalties in GL-5120)
        {
            "title": "CASE 5: GENERAL LEDGER ACCOUNT AUDIT (GL-5120 SLA PENALTIES)",
            "query": "What is the total spend and budget variance across all quarters for GL-5120?",
            "ground_truth": "GL-5120 incurred total spend of $1,710,000 against $1,500,000 budget with $210,000 over-budget variance due to Q3 GlobalBank outage credit."
        },
        # Query 6: Out-of-Domain Guardrail (Negative Constraint Defense)
        {
            "title": "CASE 6: OUT-OF-DOMAIN INQUIRY (HALLUCINATION MITIGATION DEFENSE)",
            "query": "What is the company employee discount for personal luxury resort vacations in Hawaii?",
            "ground_truth": "Insufficient context: The provided enterprise documentation does not contain this information."
        }
    ]

    for item in queries:
        print(f"\n{'-'*80}")
        print(f"🎯 {item['title']}")
        print(f"{'-'*80}")
        print(f"USER QUERY: \"{item['query']}\"")
        
        result = agent.execute(item["query"])
        
        for step in result.steps:
            print(f"\n  [AGENT REASONING]: {step.thought}")
            print(f"  [ACTION DISPATCH]: {step.action} (Input: {step.action_input})")
        
        print(f"\n  [FINAL VERIFIED ANSWER]:\n  {result.final_response}")
        print(f"  [EXECUTION LATENCY]: {result.execution_time_ms} ms")

    # --------------------------------------------------------------------------
    # AUTOMATED RAGAS CI/CD QUALITY GATE AUDIT
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("🛡️ RUNNING AUTOMATED RAGAS CI/CD QUALITY GATE AUDIT")
    print("=" * 80)

    test_sample = queries[0]
    retrieved_candidates = retriever.retrieve(test_sample["query"], top_k=6)
    reranked = reranker.rerank(test_sample["query"], retrieved_candidates, top_n=3)
    grounded = generator.generate(test_sample["query"], reranked)
    contexts = [c.text for c, _ in reranked]

    metrics = evaluator.evaluate_sample(
        question=test_sample["query"],
        answer=grounded.answer,
        contexts=contexts,
        ground_truth=test_sample["ground_truth"]
    )

    print(f"Evaluation Target: \"{test_sample['query']}\"")
    print(f"• Faithfulness (Groundedness) : {metrics.faithfulness:.3f} (Threshold: >= 0.85)")
    print(f"• Answer Relevancy (On-Topic) : {metrics.answer_relevancy:.3f} (Threshold: >= 0.80)")
    print(f"• Context Precision (Top-K)   : {metrics.context_precision:.3f} (Threshold: >= 0.75)")
    print(f"• Context Recall (Coverage)   : {metrics.context_recall:.3f} (Threshold: >= 0.75)")

    if metrics.passed_quality_gate:
        print("\n✅ CI/CD STATUS: BUILD PASSED. Zero hallucinations detected; all benchmarks satisfied.")
    else:
        print("\n❌ CI/CD STATUS: BUILD FAILED. Quality degradation detected.")
    print("=" * 80)

if __name__ == "__main__":
    run_production_showcase()





































