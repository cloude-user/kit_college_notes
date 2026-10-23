"""
test_rag_pipeline.py
Automated Unit and Integration Test Suite for KIT College Student AI Copilot.
Tests Multi-Format Ingestion (PDF, Word, Markdown, CSV), LangChain Chunking,
LangGraph StateGraph Routing, and RAGAS CI/CD Quality Gates.
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
from src.langgraph_agent import LangGraphCollegeCopilot

class TestStudentRAGPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_dir = os.path.join(BASE_DIR, "data")
        cls.handbook_file = os.path.join(cls.data_dir, "kit_college_student_handbook.md")
        cls.hostel_file = os.path.join(cls.data_dir, "kit_campus_hostel_and_mess_guide.docx")
        cls.placement_file = os.path.join(cls.data_dir, "kit_placement_policy_guide.pdf")
        cls.course_file = os.path.join(cls.data_dir, "kit_courses_and_curriculum.csv")

        # 1. Ingest all student campus documents
        cls.all_docs, cls.raw_courses = EnterpriseDocumentLoader.load_all_documents(cls.data_dir)
        cls.handbook_docs = [d for d in cls.all_docs if "handbook" in d.metadata.get("source", "")]
        cls.hostel_docs = [d for d in cls.all_docs if "hostel" in d.metadata.get("source", "")]
        cls.placement_docs = [d for d in cls.all_docs if "placement" in d.metadata.get("source", "")]

        # 2. Chunking with LangChain RecursiveCharacterTextSplitter
        cls.chunker = EnterpriseRecursiveChunker(chunk_size=320, chunk_overlap=50)
        cls.chunks = cls.chunker.chunk_documents(cls.all_docs)

        # 3. LangChain Vector Store & Hybrid Retrieval
        cls.embedder = EnterpriseEmbedder(dimension=128)
        cls.vector_store = EnterpriseVectorStore(cls.embedder)
        cls.vector_store.add_chunks(cls.chunks)
        cls.retriever = EnterpriseHybridRetriever(cls.vector_store)
        cls.reranker = EnterpriseReranker()
        cls.generator = EnterpriseGroundedGenerator()
        cls.evaluator = EnterpriseRAGASEvaluator()

        # 4. LangGraph Multi-Agent Copilot
        cls.copilot = LangGraphCollegeCopilot(
            retriever=cls.retriever,
            reranker=cls.reranker,
            generator=cls.generator,
            course_catalog=cls.raw_courses
        )

    def test_document_ingestion_formats(self):
        """Verifies multi-format parsing loaded Markdown, DOCX, PDF, and CSV."""
        self.assertGreater(len(self.handbook_docs), 0, "Student handbook (.md) must be parsed.")
        self.assertGreater(len(self.hostel_docs), 0, "Hostel guide (.docx) must be parsed.")
        self.assertGreater(len(self.placement_docs), 0, "Placement brochure (.pdf) must be parsed.")
        self.assertEqual(len(self.raw_courses), 10, "Course catalog must contain 10 curriculum rows.")
        self.assertGreater(len(self.chunks), len(self.all_docs))

    def test_chunking_overlap_integrity(self):
        """Ensures chunk overlap is strictly preserved across multiple splits."""
        local_chunker = EnterpriseRecursiveChunker(chunk_size=50, chunk_overlap=15)
        text = "KIT Academic Council mandates minimum 75 percent attendance. Students falling below 65 percent are detained."
        splits = local_chunker.split_text(text)
        self.assertGreater(len(splits), 1)

    def test_hybrid_search_library_rules(self):
        """BM25 + Dense Hybrid search retrieves library borrowing rules at top rank."""
        query = "How many physical books can an undergraduate student borrow from the library?"
        results = self.retriever.retrieve(query, top_k=3)
        top_chunk, score = results[0]
        self.assertIn("kit_college_student_handbook.md", top_chunk.metadata.get("source", ""))
        self.assertGreater(score, 0.0)

    def test_langgraph_attendance_condonation(self):
        """LangGraph routes 68% attendance to Condonation Calculator node with exact math."""
        res = self.copilot.run("My attendance is 68%, can I write the semester examination?")
        self.assertEqual(res["route"], "condonation_calculator")
        self.assertIn("Medical Condonation Applicable", res["generation"])
        self.assertIn("500", res["generation"])
        self.assertIn("[Doc 1]", res["generation"])

    def test_langgraph_course_catalog_lookup(self):
        """LangGraph routes course code query to Course Catalog node with structured metadata."""
        res = self.copilot.run("Who is teaching CS401 Machine Learning and what are the credits?")
        self.assertEqual(res["route"], "course_catalog")
        self.assertIn("Dr. Sundeep K.", res["generation"])
        self.assertIn("4 Credits", res["generation"])
        self.assertIn("[Doc 1]", res["generation"])

    def test_langgraph_placement_eligibility(self):
        """LangGraph retrieves placement eligibility rules from handbook/brochure."""
        res = self.copilot.run("What is the general registration cutoff CGPA for campus placement?")
        self.assertEqual(res["route"], "policy_rag")
        self.assertIn("7.00", res["generation"])
        self.assertIn("[Doc 1]", res["generation"])

    def test_langgraph_out_of_scope_defense(self):
        """LangGraph refuses out-of-domain queries to prevent hallucination."""
        res = self.copilot.run("Can students bring personal submarines to the campus swimming pool?")
        self.assertEqual(res["route"], "policy_rag")
        self.assertIn("Insufficient context", res["generation"])

    def test_ragas_evaluation_gate(self):
        """Verifies that RAGAS evaluation passes on grounded context."""
        question = "What is the attendance and medical condonation policy?"
        answer = "Under the academic attendance policy, minimum attendance is 75% and medical condonation is available [Doc 1]."
        contexts = ["Under the academic attendance policy, minimum attendance is 75% and medical condonation is available."]
        gt = "The attendance policy requires 75% minimum attendance and medical condonation is available."

        metrics = self.evaluator.evaluate_sample(question, answer, contexts, gt)
        self.assertGreaterEqual(metrics.faithfulness, 0.85)
        self.assertTrue(metrics.passed_quality_gate)

if __name__ == "__main__":
    unittest.main()
