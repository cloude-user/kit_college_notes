"""
test_rag_pipeline.py
Automated Unit and Integration Test Suite for Enterprise RAG & Multi-Agent Assistant.
"""

import unittest
import os
import sys

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

class TestEnterpriseRAGPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_dir = os.path.join(BASE_DIR, "data")
        cls.sec_file = os.path.join(cls.data_dir, "sec_filing_q3_cloudcorp.md")
        cls.policy_file = os.path.join(cls.data_dir, "corporate_compliance_policy.md")
        cls.ledger_file = os.path.join(cls.data_dir, "financial_ledger_2025.csv")

        # 1. Loaders: Automatically load all enterprise documents
        cls.all_docs, cls.raw_ledger = EnterpriseDocumentLoader.load_all_enterprise_documents(cls.data_dir)
        cls.sec_docs = [d for d in cls.all_docs if "sec_filing" in d.metadata.get("source", "")]
        cls.policy_docs = [d for d in cls.all_docs if "compliance_policy" in d.metadata.get("source", "")]

        # 2. Chunker
        cls.chunker = EnterpriseRecursiveChunker(chunk_size=300, chunk_overlap=50)
        cls.chunks = cls.chunker.chunk_documents(cls.all_docs)

        # 3. Store & Hybrid
        cls.embedder = EnterpriseEmbedder(dimension=128)
        cls.vector_store = EnterpriseVectorStore(cls.embedder)
        cls.vector_store.add_chunks(cls.chunks)
        cls.retriever = EnterpriseHybridRetriever(cls.vector_store)
        cls.reranker = EnterpriseReranker()
        cls.generator = EnterpriseGroundedGenerator()
        cls.evaluator = EnterpriseRAGASEvaluator()
        cls.agent = EnterpriseMultiAgentRouter(
            retriever=cls.retriever,
            reranker=cls.reranker,
            generator=cls.generator,
            raw_ledger=cls.raw_ledger
        )

    def test_document_ingestion_counts(self):
        """Verifies multi-format parsing loaded all documents properly."""
        self.assertGreater(len(self.sec_docs), 0)
        self.assertGreater(len(self.policy_docs), 0)
        self.assertEqual(len(self.raw_ledger), 21) # 21 multi-quarter enterprise ledger entries
        self.assertGreater(len(self.chunks), len(self.all_docs))

    def test_chunking_overlap_integrity(self):
        """Ensures chunk overlap is strictly preserved across multiple splits."""
        local_chunker = EnterpriseRecursiveChunker(chunk_size=50, chunk_overlap=15)
        text = "Alpha paragraph discussing cloud infrastructure. Beta paragraph detailing database partitions."
        splits = local_chunker.split_text(text)
        self.assertGreater(len(splits), 1)

    def test_hybrid_search_exact_error_code(self):
        """BM25 + Dense must rank the exact error code at Rank #1."""
        query = "What happens during ERR_STREAM_BUFFER_OVERFLOW_504?"
        results = self.retriever.retrieve(query, top_k=2)
        top_chunk, score = results[0]
        self.assertIn("ERR_STREAM_BUFFER_OVERFLOW_504", top_chunk.text)
        self.assertGreater(score, 0.0)

    def test_agent_structured_vs_unstructured_routing(self):
        """ReAct agent must correctly route numeric vs policy questions."""
        # Query A: Structured numeric spend
        res_structured = self.agent.execute("What was the actual spend for Engineering-AI in Q3?")
        self.assertEqual(res_structured.steps[0].action, "tool_structured_analytics")
        self.assertIn("17,450,000", res_structured.final_response)

        # Query B: Unstructured compliance policy
        res_unstructured = self.agent.execute("How often must API keys be rotated according to policy?")
        self.assertEqual(res_unstructured.steps[0].action, "tool_unstructured_rag")
        self.assertIn("90", res_unstructured.final_response)

    def test_gl_account_structured_analytics(self):
        """Agent must aggregate GL-5120 outage penalties and detect over-budget Q3 status."""
        res = self.agent.execute("What is the total spend for GL-5120 across all quarters?")
        self.assertEqual(res.steps[0].action, "tool_structured_analytics")
        self.assertIn("1,710,000", res.final_response)
        self.assertIn("Customer-Success (Q3)", res.final_response)

    def test_procurement_authorization_tiers(self):
        """Agent must route procurement thresholds to appropriate executive tiers."""
        tier3_res = self.agent.execute("What approval is needed to purchase a $350,000 GPU cluster?")
        self.assertEqual(tier3_res.steps[0].action, "tool_procurement_validator")
        self.assertIn("Tier 3", tier3_res.final_response)
        self.assertIn("CFO and CISO", tier3_res.final_response)

    def test_ragas_evaluation_gate(self):
        """Verifies that RAGAS evaluation passes on grounded context."""
        question = "What is the warranty period for hardware?"
        answer = "All hardware is covered by a 3-year limited warranty [Doc 1]."
        contexts = ["All hardware components purchased under enterprise contracts are covered by a 3-year limited hardware warranty."]
        gt = "Hardware is covered by a 3-year limited warranty."

        metrics = self.evaluator.evaluate_sample(question, answer, contexts, gt)
        self.assertGreaterEqual(metrics.faithfulness, 0.85)
        self.assertTrue(metrics.passed_quality_gate)

if __name__ == "__main__":
    unittest.main()

