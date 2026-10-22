"""
test_cloud_rag_pipeline.py
Automated Unit and Integration Test Suite for BioPharma Multi-Agent RAG.
Tests ColPali Late-Interaction, Cloud Vector Store, Deterministic Analytics, and LangGraph Workflow.
"""

import unittest
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from src.loaders import ClinicalDocumentLoader
from src.colpali_engine import ColPaliEngine
from src.cloud_vector_store import MockCloudVectorStore
from src.deterministic_clinical_analytics import DeterministicClinicalAnalytics
from src.langgraph_workflow import EnterpriseClinicalRAGWorkflow

class TestBioPharmaCloudRAGPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_dir = os.path.join(BASE_DIR, "data")
        cls.ledger_path = os.path.join(cls.data_dir, "clinical_trial_safety_ledger.csv")

        # 1. Load documents
        cls.pages = ClinicalDocumentLoader.load_all_documents(cls.data_dir)

        # 2. Initialize ColPali Engine & index pages
        cls.colpali = ColPaliEngine(dimension=128)
        cls.indexed_pages = [cls.colpali.embed_page(p) for p in cls.pages]

        # 3. Initialize Cloud Vector Store
        cls.cloud_store = MockCloudVectorStore()
        cls.cloud_store.initialize_index(dimension=128)

        # 4. Initialize Deterministic Analytics
        cls.analytics = DeterministicClinicalAnalytics(cls.ledger_path)

        # 5. Build LangGraph Workflow
        cls.workflow = EnterpriseClinicalRAGWorkflow(
            colpali_engine=cls.colpali,
            indexed_pages=cls.indexed_pages,
            analytics_engine=cls.analytics,
            cloud_vector_store=cls.cloud_store
        )

    def test_document_ingestion(self):
        """Verifies clinical protocol documents are split into valid visual pages."""
        self.assertGreater(len(self.pages), 5)
        # Check that table visual types are detected
        tables = [p for p in self.pages if p.visual_type == "table"]
        self.assertGreater(len(tables), 0)

    def test_colpali_late_interaction_maxsim(self):
        """Verifies ColPali MaxSim scores clinical terms with high precision."""
        query = "What is the mandatory 7-day reporting alert for fatal SUSARs under 21 CFR 312?"
        hits = self.colpali.retrieve(query, self.indexed_pages, top_k=2)
        self.assertGreater(len(hits), 0)
        self.assertIn("312", hits[0].text_content)
        self.assertGreater(hits[0].maxsim_score, 0.0)

    def test_deterministic_clinical_analytics(self):
        """Verifies exact deterministic math on safety ledger."""
        res = self.analytics.analyze()
        self.assertEqual(res.total_records, 25)
        self.assertGreater(res.total_saes, 0)
        self.assertGreater(res.sae_rate_percent, 0.0)
        # Check that fatal event triggers mandatory clinical hold stopping rule
        self.assertTrue(res.stopping_rule_triggered)
        self.assertIn("MANDATORY CLINICAL HOLD", res.stopping_rule_details)

    def test_langgraph_clinical_analytics_routing(self):
        """LangGraph must route adverse event frequency queries to Analytics Node."""
        res = self.workflow.execute("How many serious adverse events and fatal events occurred in Cohort 3?")
        self.assertEqual(res.intent, "clinical_analytics")
        self.assertIsNotNone(res.clinical_stats)
        self.assertIn("Cohort 3", res.final_response)

    def test_langgraph_hitl_dose_escalation_gate(self):
        """LangGraph must intercept dose escalation requests and enforce Human-in-the-Loop status."""
        res = self.workflow.execute("Can we escalate dose or resume 450 mg for patient with pneumonitis?")
        self.assertEqual(res.intent, "hitl_dose_escalation")
        self.assertTrue(res.requires_hitl)
        self.assertEqual(res.hitl_status, "PENDING_APPROVAL")
        self.assertIn("ACTION INTERCEPTED BY CLINICAL SAFETY GATE", res.final_response)

if __name__ == "__main__":
    unittest.main()
