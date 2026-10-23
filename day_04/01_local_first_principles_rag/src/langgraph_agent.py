"""
langgraph_agent.py
StateGraph Multi-Agent Orchestrator powered by LangGraph & LangChain.
Coordinates intent classification, document RAG, deterministic course queries,
attendance condonation calculation, and citation verification.
"""

import re
import time
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, START, END

from .models import Chunk, GroundedResponse, GroundedCitation
from .hybrid_retriever import EnterpriseHybridRetriever
from .reranker import EnterpriseReranker
from .generator import EnterpriseGroundedGenerator

class CollegeCopilotState(TypedDict):
    """
    Central State Schema passed through the compiled LangGraph execution graph.
    """
    query: str
    route: str                          # "condonation_calculator" | "course_catalog" | "policy_rag"
    route_reason: str
    retrieved_chunks: List[Dict[str, Any]]
    catalog_results: List[Dict[str, Any]]
    calculator_data: Optional[Dict[str, Any]]
    generation: str
    citations: List[Dict[str, Any]]
    has_sufficient_context: bool
    confidence_score: float
    trace_steps: List[Dict[str, str]]   # Visual graph execution trace for UI
    latency_ms: float

class LangGraphCollegeCopilot:
    """
    Production Multi-Agent Copilot compiled into an executable LangGraph StateGraph.
    """
    def __init__(
        self,
        retriever: EnterpriseHybridRetriever,
        reranker: EnterpriseReranker,
        generator: EnterpriseGroundedGenerator,
        course_catalog: List[Dict[str, Any]]
    ):
        self.retriever = retriever
        self.reranker = reranker
        self.generator = generator
        self.course_catalog = course_catalog
        self.graph = self._compile_graph()

    def _compile_graph(self):
        """Constructs and compiles the directed LangGraph StateGraph."""
        builder = StateGraph(CollegeCopilotState)

        # 1. Register Graph Nodes
        builder.add_node("router_node", self._node_router)
        builder.add_node("condonation_calculator_node", self._node_condonation_calculator)
        builder.add_node("course_catalog_node", self._node_course_catalog)
        builder.add_node("policy_rag_node", self._node_policy_rag)
        builder.add_node("synthesizer_node", self._node_synthesizer)
        builder.add_node("citation_verifier_node", self._node_citation_verifier)

        # 2. Add Graph Edges
        builder.add_edge(START, "router_node")

        # Conditional branching from router based on classified intent
        builder.add_conditional_edges(
            "router_node",
            self._route_decision,
            {
                "condonation_calculator": "condonation_calculator_node",
                "course_catalog": "course_catalog_node",
                "policy_rag": "policy_rag_node"
            }
        )

        # Convergence to synthesis and verification
        builder.add_edge("condonation_calculator_node", "synthesizer_node")
        builder.add_edge("course_catalog_node", "synthesizer_node")
        builder.add_edge("policy_rag_node", "synthesizer_node")
        builder.add_edge("synthesizer_node", "citation_verifier_node")
        builder.add_edge("citation_verifier_node", END)

        return builder.compile()

    # --------------------------------------------------------------------------
    # CONDITIONAL EDGE ROUTER
    # --------------------------------------------------------------------------
    def _route_decision(self, state: CollegeCopilotState) -> str:
        return state.get("route", "policy_rag")

    # --------------------------------------------------------------------------
    # NODE 1: INTENT ROUTER NODE
    # --------------------------------------------------------------------------
    def _node_router(self, state: CollegeCopilotState) -> Dict[str, Any]:
        q = state["query"].lower()
        trace = list(state.get("trace_steps", []))

        # Check for numeric attendance or condonation inquiry
        attendance_match = re.search(r"(\d{1,3}(?:\.\d+)?)\s*%", q)
        attendance_keywords = ["attendance", "condonation", "detained", "shortage", "eligible to write", "sit for exam", "lack of attendance"]
        is_condonation_query = bool(attendance_match) or any(k in q for k in ["condonation", "detention", "detained"])

        # Check for course code or course curriculum lookup
        course_code_match = re.search(r"\b([a-z]{2}\d{3})\b", q)
        course_keywords = ["credits", "who teaches", "faculty", "professor", "prerequisite", "curriculum", "subject code", "exam date", "course code", "syllabus"]
        is_course_query = bool(course_code_match) or (any(k in q for k in course_keywords) and not is_condonation_query)

        if is_condonation_query and (attendance_match or "condonation" in q or "detained" in q or "shortage" in q):
            route = "condonation_calculator"
            reason = "Query contains attendance percentage or condonation policy inquiry. Routing to deterministic Condonation Calculator."
        elif is_course_query:
            route = "course_catalog"
            reason = "Query requests specific course code, credits, faculty, or curriculum details. Routing to Course Catalog DB."
        else:
            route = "policy_rag"
            reason = "Query inquires about general academic regulations, library, hostel, placement, or campus conduct. Routing to Hybrid Policy RAG."

        trace.append({
            "node": "🔀 Router Node",
            "action": f"Classified intent as '{route}'",
            "details": reason
        })

        return {
            "route": route,
            "route_reason": reason,
            "trace_steps": trace
        }

    # --------------------------------------------------------------------------
    # NODE 2: CONDONATION CALCULATOR NODE (Deterministic Zero-Hallucination Math)
    # --------------------------------------------------------------------------
    def _node_condonation_calculator(self, state: CollegeCopilotState) -> Dict[str, Any]:
        q = state["query"]
        trace = list(state.get("trace_steps", []))
        
        # Extract percentage if present
        pct_match = re.search(r"(\d{1,3}(?:\.\d+)?)\s*%", q)
        pct = float(pct_match.group(1)) if pct_match else None

        if pct is None:
            # Check for words like "seventy two percent" or digits
            dig_match = re.search(r"\b(\d{2})\b", q)
            if dig_match:
                pct = float(dig_match.group(1))

        calc_data = {
            "provided_percentage": pct,
            "status": "Unknown",
            "eligible": False,
            "condonation_applicable": False,
            "detained": False,
            "fee_inr": 0,
            "cia_marks": 0,
            "action_required": ""
        }

        if pct is not None:
            if pct >= 75.0:
                cia_marks = 5 if pct >= 100 else (4 if pct >= 90 else (3 if pct >= 80 else 2))
                calc_data.update({
                    "status": "Fully Eligible for SEE",
                    "eligible": True,
                    "cia_marks": cia_marks,
                    "action_required": f"No action needed. You satisfy the 75% threshold and earn {cia_marks}/5 CIA attendance marks."
                })
            elif 65.0 <= pct < 75.0:
                calc_data.update({
                    "status": "Medical Condonation Applicable",
                    "eligible": False, # until condonation granted
                    "condonation_applicable": True,
                    "fee_inr": 500,
                    "action_required": (
                        "Submit a Government Doctor Medical Certificate & discharge summary to HOD "
                        "within 3 calendar days of resuming classes, and pay ₹500 condonation processing fee per subject."
                    )
                })
            else:
                calc_data.update({
                    "status": "Detained (Grade 'DE')",
                    "eligible": False,
                    "detained": True,
                    "action_required": (
                        "Attendance is below 65.0%. As per Section 1.3, you are strictly detained and barred "
                        "from writing the Semester End Examination (SEE). You must re-register during the subsequent academic year."
                    )
                })

        trace.append({
            "node": "🧮 Condonation Calculator Node",
            "action": f"Executed attendance evaluation for {pct}%",
            "details": f"Result: {calc_data['status']}"
        })

        return {
            "calculator_data": calc_data,
            "trace_steps": trace
        }

    # --------------------------------------------------------------------------
    # NODE 3: COURSE CATALOG NODE (Deterministic Structured Lookups)
    # --------------------------------------------------------------------------
    def _node_course_catalog(self, state: CollegeCopilotState) -> Dict[str, Any]:
        q = state["query"].lower()
        trace = list(state.get("trace_steps", []))
        matched_records = []

        # Find course codes (e.g., CS401, AI502)
        code_match = re.search(r"\b([a-z]{2}\d{3})\b", q)
        target_code = code_match.group(1).upper() if code_match else None

        for row in self.course_catalog:
            code = row.get("course_code", "").upper()
            name = row.get("course_name", "").lower()
            faculty = row.get("faculty_name", "").lower()
            dept = row.get("department", "").lower()

            if target_code and target_code == code:
                matched_records.append(row)
            elif not target_code:
                # Check for topic match (e.g. machine learning, devops, networks)
                words = [w for w in q.split() if len(w) > 3]
                if any(w in name for w in words) or any(w in faculty for w in words) or any(w in dept for w in words):
                    matched_records.append(row)

        trace.append({
            "node": "📊 Course Catalog Node",
            "action": f"Queried course database for '{target_code or q}'",
            "details": f"Retrieved {len(matched_records)} matching course records from curriculum database."
        })

        return {
            "catalog_results": matched_records,
            "trace_steps": trace
        }

    # --------------------------------------------------------------------------
    # NODE 4: HYBRID POLICY RAG NODE (BM25 + Dense Retrieval + RRF Reranking)
    # --------------------------------------------------------------------------
    def _node_policy_rag(self, state: CollegeCopilotState) -> Dict[str, Any]:
        q = state["query"]
        trace = list(state.get("trace_steps", []))

        # 1. Retrieve candidates via BM25 + Dense RRF
        candidates = self.retriever.retrieve(q, top_k=6)

        # 2. Re-rank top candidates
        reranked = self.reranker.rerank(q, candidates, top_n=3)

        chunk_payloads = []
        for rank, (chunk, score) in enumerate(reranked, start=1):
            chunk_payloads.append({
                "rank": rank,
                "text": chunk.text,
                "score": float(score),
                "source": chunk.metadata.get("source", "unknown"),
                "section": chunk.metadata.get("section", "General"),
                "format": chunk.metadata.get("format", "text")
            })

        trace.append({
            "node": "📚 Policy RAG Node",
            "action": f"Retrieved and re-ranked top {len(chunk_payloads)} relevant sections",
            "details": f"Top match from: {chunk_payloads[0]['source'] if chunk_payloads else 'None'} ({chunk_payloads[0]['section'] if chunk_payloads else ''})"
        })

        return {
            "retrieved_chunks": chunk_payloads,
            "trace_steps": trace
        }

    # --------------------------------------------------------------------------
    # NODE 5: SYNTHESIZER NODE (Grounding with Bracket Citations)
    # --------------------------------------------------------------------------
    def _node_synthesizer(self, state: CollegeCopilotState) -> Dict[str, Any]:
        route = state.get("route")
        q = state["query"]
        trace = list(state.get("trace_steps", []))

        # Case A: Condonation Calculator Output
        if route == "condonation_calculator":
            calc = state.get("calculator_data", {})
            pct = calc.get("provided_percentage")
            status = calc.get("status")
            action = calc.get("action_required")

            if pct is not None:
                answer = (
                    f"### 📋 Attendance Evaluation Result: {pct}%\n\n"
                    f"**Official Academic Status**: `{status}` [Doc 1]\n\n"
                    f"**Next Steps & Official Guidelines**:\n"
                    f"• {action} [Doc 1]\n\n"
                    f"> *Source Reference: [Doc 1: kit_college_student_handbook.md — Section 1: Academic Regulations & Attendance Policy]*"
                )
            else:
                answer = (
                    "### 📋 KIT Attendance & Condonation Regulations\n\n"
                    "1. **Minimum Threshold**: Students require **75% minimum attendance** in each registered course to be eligible to appear for Semester End Examinations (SEE) [Doc 1].\n"
                    "2. **Medical Condonation (65% to 74.9%)**: Permitted upon submitting a Government Doctor Medical Certificate within **3 calendar days** of resuming classes, plus a **₹500 per subject** fee [Doc 1].\n"
                    "3. **Detention (<65%)**: Students with less than 65% attendance receive Grade **'DE' (Detained)** and are strictly barred from writing SEE [Doc 1].\n\n"
                    "> *Source Reference: [Doc 1: kit_college_student_handbook.md — Section 1.2]*"
                )

            citations = [{
                "claim": f"Attendance policy rules for {pct or 'general'} threshold",
                "doc_tag": "[Doc 1]",
                "source_file": "kit_college_student_handbook.md",
                "verified": True
            }]

            trace.append({
                "node": "✍️ Synthesizer Node",
                "action": "Synthesized deterministic attendance decision with handbook citations",
                "details": f"Generated cited response for {status}"
            })

            return {
                "generation": answer,
                "citations": citations,
                "has_sufficient_context": True,
                "confidence_score": 0.98,
                "trace_steps": trace
            }

        # Case B: Course Catalog Output
        elif route == "course_catalog":
            records = state.get("catalog_results", [])
            if not records:
                # Fallback to general RAG if no exact table record found
                candidates = self.retriever.retrieve(q, top_k=3)
                reranked = self.reranker.rerank(q, candidates, top_n=2)
                grounded = self.generator.generate(q, reranked)
                answer = grounded.answer
                citations = [c.model_dump() if hasattr(c, "model_dump") else c.__dict__ for c in grounded.citations]
            else:
                lines = ["### 📚 Course Catalog & Curriculum Specification\n"]
                for r in records:
                    code = r.get("course_code", "")
                    name = r.get("course_name", "")
                    credits = r.get("credits", "")
                    faculty = r.get("faculty_name", "")
                    email = r.get("faculty_email", "")
                    sem = r.get("semester", "")
                    lab = r.get("has_lab", "No")
                    prereq = r.get("prerequisites", "None")
                    exam = r.get("exam_date", "TBA")

                    lines.append(f"#### **{code}: {name}** (`{credits} Credits`) [Doc 1]")
                    lines.append(f"- **Instructor**: {faculty} ({email}) [Doc 1]")
                    lines.append(f"- **Semester & Lab**: {sem} | Laboratory Component: **{lab}** [Doc 1]")
                    lines.append(f"- **Prerequisites**: {prereq} [Doc 1]")
                    lines.append(f"- **Semester End Exam Date**: `{exam}` [Doc 1]\n")

                lines.append("> *Source Reference: [Doc 1: kit_courses_and_curriculum.csv — Institutional Curriculum Registry]*")
                answer = "\n".join(lines)
                citations = [{
                    "claim": f"Official course curriculum for {records[0].get('course_code', 'Course')}",
                    "doc_tag": "[Doc 1]",
                    "source_file": "kit_courses_and_curriculum.csv",
                    "verified": True
                }]

            trace.append({
                "node": "✍️ Synthesizer Node",
                "action": "Generated structured course curriculum response",
                "details": f"Generated details for {len(records)} course record(s)"
            })

            return {
                "generation": answer,
                "citations": citations,
                "has_sufficient_context": True,
                "confidence_score": 1.0,
                "trace_steps": trace
            }

        # Case C: Policy RAG Output
        else:
            chunks_data = state.get("retrieved_chunks", [])
            # Convert dict chunks back to Chunk instances for generator
            chunk_tuples = []
            for c in chunks_data:
                chunk_obj = Chunk(
                    text=c["text"],
                    metadata={
                        "source": c["source"],
                        "section": c["section"],
                        "format": c["format"]
                    }
                )
                chunk_tuples.append((chunk_obj, c["score"]))

            grounded = self.generator.generate(q, chunk_tuples)
            citations = [c.model_dump() if hasattr(c, "model_dump") else c.__dict__ for c in grounded.citations]

            trace.append({
                "node": "✍️ Synthesizer Node",
                "action": "Synthesized grounded answer using LLM & context blocks",
                "details": f"Produced answer with {len(citations)} citations"
            })

            return {
                "generation": grounded.answer,
                "citations": citations,
                "has_sufficient_context": grounded.has_sufficient_context,
                "confidence_score": grounded.confidence_score,
                "trace_steps": trace
            }

    # --------------------------------------------------------------------------
    # NODE 6: CITATION VERIFIER & QUALITY GUARD NODE
    # --------------------------------------------------------------------------
    def _node_citation_verifier(self, state: CollegeCopilotState) -> Dict[str, Any]:
        answer = state.get("generation", "")
        trace = list(state.get("trace_steps", []))
        citations = state.get("citations", [])

        # Check for bracket tags like [Doc 1], [Doc 2]
        doc_tags = re.findall(r"\[Doc\s*(\d+)\]", answer)
        verified_count = 0

        for c in citations:
            tag = c.get("doc_tag", "")
            if tag in answer:
                c["verified"] = True
                verified_count += 1

        pass_guard = (len(doc_tags) > 0 or not state.get("has_sufficient_context", True))

        trace.append({
            "node": "🛡️ Citation Verifier Node",
            "action": f"Verified {len(doc_tags)} citation tag(s) in final answer",
            "details": f"Status: {'✅ PASSED (Grounded)' if pass_guard else '⚠️ UNGROUNDED'}"
        })

        return {
            "citations": citations,
            "trace_steps": trace
        }

    # --------------------------------------------------------------------------
    # EXECUTE RUNNER
    # --------------------------------------------------------------------------
    def run(self, query: str) -> CollegeCopilotState:
        """Executes query through the compiled LangGraph StateGraph pipeline."""
        t0 = time.perf_counter()
        initial_state: CollegeCopilotState = {
            "query": query,
            "route": "policy_rag",
            "route_reason": "",
            "retrieved_chunks": [],
            "catalog_results": [],
            "calculator_data": None,
            "generation": "",
            "citations": [],
            "has_sufficient_context": True,
            "confidence_score": 1.0,
            "trace_steps": [],
            "latency_ms": 0.0
        }

        # Invoke compiled StateGraph
        final_state = self.graph.invoke(initial_state)
        final_state["latency_ms"] = (time.perf_counter() - t0) * 1000.0
        return final_state
