"""
langgraph_workflow.py
Enterprise Multi-Agent Orchestration via LangGraph StateGraph.
Coordinates:
1. Intent Classification Router Node
2. ColPali Visual-Language Document Retrieval Node
3. Deterministic Clinical Safety Analytics Node
4. Medical Monitor Supervisor Node (Citations & Evidence Synthesis)
5. Human-in-the-Loop (HITL) Safety Checkpoint Gate
"""

import time
import re
from typing import Dict, Any, List, Optional, Callable
from dataclasses import asdict

from .models import ClinicalAgentState, LangGraphAgentStep, RetrievalHit, ClinicalStatsResult
from .colpali_engine import ColPaliEngine
from .deterministic_clinical_analytics import DeterministicClinicalAnalytics
from .cloud_vector_store import BaseCloudVectorStore

# Attempt official LangGraph import; fall back to embedded StateGraph engine if not yet pip installed
try:
    from langgraph.graph import StateGraph, END
    _HAS_OFFICIAL_LANGGRAPH = True
except ImportError:
    _HAS_OFFICIAL_LANGGRAPH = False
    END = "__END__"

    class StateGraph:
        """Embedded production-compatible StateGraph runner."""
        def __init__(self, state_schema):
            self.state_schema = state_schema
            self.nodes: Dict[str, Callable] = {}
            self.edges: Dict[str, str] = {}
            self.conditional_edges: Dict[str, Tuple[Callable, Dict[str, str]]] = {}
            self.entry_point: Optional[str] = None

        def add_node(self, name: str, action: Callable):
            self.nodes[name] = action

        def set_entry_point(self, name: str):
            self.entry_point = name

        def add_edge(self, start_node: str, end_node: str):
            self.edges[start_node] = end_node

        def add_conditional_edges(self, start_node: str, condition: Callable, mapping: Dict[str, str]):
            self.conditional_edges[start_node] = (condition, mapping)

        def compile(self):
            return CompiledGraph(self)

    class CompiledGraph:
        def __init__(self, graph: StateGraph):
            self.graph = graph

        def invoke(self, state: ClinicalAgentState) -> ClinicalAgentState:
            current = self.graph.entry_point
            max_iterations = 15
            iter_count = 0

            while current and current != END and iter_count < max_iterations:
                iter_count += 1
                node_fn = self.graph.nodes.get(current)
                if not node_fn:
                    break

                # Execute node function
                state = node_fn(state)

                # Determine next node via conditional edges or direct edges
                if current in self.graph.conditional_edges:
                    cond_fn, mapping = self.graph.conditional_edges[current]
                    route_key = cond_fn(state)
                    current = mapping.get(route_key, END)
                elif current in self.graph.edges:
                    current = self.graph.edges[current]
                else:
                    current = END

            return state


class EnterpriseClinicalRAGWorkflow:
    """
    Constructs and executes the LangGraph multi-agent workflow for BioPharma RAG.
    """
    def __init__(
        self,
        colpali_engine: ColPaliEngine,
        indexed_pages: List[Any],
        analytics_engine: DeterministicClinicalAnalytics,
        cloud_vector_store: BaseCloudVectorStore
    ):
        self.colpali = colpali_engine
        self.indexed_pages = indexed_pages
        self.analytics = analytics_engine
        self.cloud_store = cloud_vector_store
        self.workflow = self._build_graph()

    def _build_graph(self):
        """Assembles the state machine directed graph."""
        builder = StateGraph(ClinicalAgentState)

        # 1. Register Nodes
        builder.add_node("router_node", self._router_node)
        builder.add_node("colpali_retriever_node", self._colpali_retriever_node)
        builder.add_node("clinical_analytics_node", self._clinical_analytics_node)
        builder.add_node("safety_supervisor_node", self._safety_supervisor_node)
        builder.add_node("human_in_the_loop_node", self._human_in_the_loop_node)

        # 2. Set Entry Point
        builder.set_entry_point("router_node")

        # 3. Conditional Branching from Router
        def route_intent(state: ClinicalAgentState) -> str:
            if state.intent == "clinical_analytics":
                return "clinical_analytics_node"
            elif state.intent == "hitl_dose_escalation":
                return "human_in_the_loop_node"
            return "colpali_retriever_node"

        builder.add_conditional_edges(
            "router_node",
            route_intent,
            {
                "clinical_analytics_node": "clinical_analytics_node",
                "colpali_retriever_node": "colpali_retriever_node",
                "human_in_the_loop_node": "human_in_the_loop_node"
            }
        )

        # 4. Processing Edges to Supervisor
        builder.add_edge("colpali_retriever_node", "safety_supervisor_node")
        builder.add_edge("clinical_analytics_node", "safety_supervisor_node")
        builder.add_edge("human_in_the_loop_node", "safety_supervisor_node")
        builder.add_edge("safety_supervisor_node", END)

        return builder.compile()

    # --------------------------------------------------------------------------
    # NODE 1: ROUTER NODE
    # --------------------------------------------------------------------------
    def _router_node(self, state: ClinicalAgentState) -> ClinicalAgentState:
        q_lower = state.user_query.lower()
        
        # Check for dose escalation or protocol amendment requiring Medical Monitor sign-off
        is_escalation = any(term in q_lower for term in [
            "escalate dose", "increase dose", "resume 450", "resume 300", "re-escalate",
            "overrule safety hold", "protocol waiver"
        ])
        
        # Check for numeric statistical queries (incident rates, counts, SAEs, grades, overdue)
        is_analytics = any(term in q_lower for term in [
            "how many", "incidence rate", "grade 4", "grade 3", "fatal", "deaths",
            "overdue", "sae count", "adverse events", "breakdown", "ledger", "cohort 3"
        ]) and any(term in q_lower for term in ["sae", "events", "patients", "rate", "percent", "count", "toxicity"])

        if is_escalation:
            intent = "hitl_dose_escalation"
            thought = "User inquiry requests clinical dose modification or protocol waiver. Routing to Human-in-the-Loop Gate."
        elif is_analytics:
            intent = "clinical_analytics"
            thought = "User inquiry requires deterministic aggregation across patient safety records. Routing to Clinical Analytics Node."
        else:
            intent = "regulatory_rag"
            thought = "User inquiry relates to FDA protocols, 21 CFR regulations, or Investigator Brochure. Routing to ColPali Multi-Vector Retriever."

        state.intent = intent
        state.trace.append(
            LangGraphAgentStep(
                node_name="router_node",
                thought=thought,
                action_taken=f"dispatched_to_{intent}",
                payload={"classified_intent": intent}
            )
        )
        return state

    # --------------------------------------------------------------------------
    # NODE 2: COLPALI RETRIEVER NODE (MULTI-VECTOR LATE-INTERACTION)
    # --------------------------------------------------------------------------
    def _colpali_retriever_node(self, state: ClinicalAgentState) -> ClinicalAgentState:
        hits = self.colpali.retrieve(state.user_query, self.indexed_pages, top_k=3)
        state.retrieved_hits = hits

        citations = []
        for i, hit in enumerate(hits, 1):
            citations.append(f"[Doc {i}: {hit.source_file} (Page {hit.page_number}) - MaxSim: {hit.maxsim_score:.2f}]")
        state.citations = citations

        state.trace.append(
            LangGraphAgentStep(
                node_name="colpali_retriever_node",
                thought=f"Executed ColPali visual patch MaxSim late-interaction scoring across {len(self.indexed_pages)} indexed protocol pages.",
                action_taken="retrieved_top_visual_candidates",
                payload={"top_hits": [h.doc_id for h in hits], "top_maxsim_score": hits[0].maxsim_score if hits else 0.0}
            )
        )
        return state

    # --------------------------------------------------------------------------
    # NODE 3: CLINICAL ANALYTICS NODE (DETERMINISTIC ZERO-HALLUCINATION)
    # --------------------------------------------------------------------------
    def _clinical_analytics_node(self, state: ClinicalAgentState) -> ClinicalAgentState:
        q_lower = state.user_query.lower()
        
        cohort_filter = None
        for c in ["cohort 1", "cohort 2", "cohort 3"]:
            if c in q_lower:
                cohort_filter = c.title()
                break

        site_filter = None
        for s in ["memorial sloan", "md anderson", "dana-farber", "mayo clinic", "johns hopkins"]:
            if s in q_lower:
                site_filter = s.title()
                break

        stats = self.analytics.analyze(cohort_filter=cohort_filter, site_filter=site_filter)
        state.clinical_stats = stats
        state.citations = ["Clinical Trial Safety Incident Ledger (FORM-FDA-3500A Records)"]

        state.trace.append(
            LangGraphAgentStep(
                node_name="clinical_analytics_node",
                thought=f"Calculated exact deterministic rates across {stats.total_records} patient records.",
                action_taken="computed_safety_metrics",
                payload={
                    "total_saes": stats.total_saes,
                    "sae_rate_percent": stats.sae_rate_percent,
                    "fatal_count": stats.fatal_count,
                    "stopping_rule_triggered": stats.stopping_rule_triggered
                }
            )
        )
        return state

    # --------------------------------------------------------------------------
    # NODE 4: HUMAN-IN-THE-LOOP (HITL) CHECKPOINT GATE
    # --------------------------------------------------------------------------
    def _human_in_the_loop_node(self, state: ClinicalAgentState) -> ClinicalAgentState:
        state.requires_hitl = True
        state.hitl_status = "PENDING_APPROVAL"
        state.hitl_reason = (
            "SAFETY CRITICAL GATE: Protocol ABX-702 Section 3.0 explicitly states: "
            "'Dose escalations within an individual patient are strictly prohibited. "
            "Dose reductions are permanent; re-escalation is not permitted.' "
            "Execution paused pending certified Medical Monitor dual sign-off (21 CFR Part 11)."
        )

        state.trace.append(
            LangGraphAgentStep(
                node_name="human_in_the_loop_node",
                thought="Detected high-risk clinical modification breaching protocol boundary. Intercepting execution.",
                action_taken="gated_for_human_physician_signoff",
                payload={"requires_hitl": True, "hitl_reason": state.hitl_reason}
            )
        )
        return state

    # --------------------------------------------------------------------------
    # NODE 5: SAFETY SUPERVISOR NODE (SYNTHESIS & CITATIONS)
    # --------------------------------------------------------------------------
    def _safety_supervisor_node(self, state: ClinicalAgentState) -> ClinicalAgentState:
        if state.requires_hitl and state.hitl_status == "PENDING_APPROVAL":
            state.final_response = (
                f"⚠️ **ACTION INTERCEPTED BY CLINICAL SAFETY GATE**\n\n"
                f"{state.hitl_reason}\n\n"
                f"**Mandatory Protocol Citation**: [Protocol ABX-702 Section 3: Dose Modification & Toxicity Matrix]\n"
                f"**Audit Status**: Awaiting electronic signature from Sponsor Medical Monitor."
            )
            return state

        if state.clinical_stats:
            stats = state.clinical_stats
            ans_parts = [
                f"**VERIFIED CLINICAL TRIAL SAFETY AUDIT**",
                f"",
                f"• **Scope Analyzed**: {stats.cohort_filter or 'All Cohorts'} across {stats.site_filter or 'All Participating Clinical Sites'}",
                f"• **Total Incident Records**: `{stats.total_records}`",
                f"• **Serious Adverse Events (SAEs)**: `{stats.total_saes}` ({stats.sae_rate_percent}% incidence rate)",
                f"• **CTCAE Severity Breakdown**: Grade 1: `{stats.grade_distribution.get('Grade 1', 0)}`, Grade 2: `{stats.grade_distribution.get('Grade 2', 0)}`, Grade 3: `{stats.grade_distribution.get('Grade 3', 0)}`, Grade 4: `{stats.grade_distribution.get('Grade 4', 0)}`, Grade 5 (Fatal): `{stats.fatal_count}`",
                f"• **FDA Expedited 7-Day / 15-Day Overdue Filings**: `{stats.overdue_fda_reports}` overdue incidents detected",
                f"• **Safety Review Committee Protocol Status**: {'🚨 ' + stats.stopping_rule_details if stats.stopping_rule_triggered else '✅ Normal Monitoring Boundaries Maintained'}"
            ]
            state.final_response = "\n".join(ans_parts)
            return state

        if state.retrieved_hits:
            top_hit = state.retrieved_hits[0]
            ans_parts = [
                f"**AUTHORITATIVE REGULATORY & PROTOCOL RESPONSE**",
                f"",
                f"{top_hit.text_content.strip()} [Doc 1: {top_hit.source_file}]",
                f"",
                f"**Supporting Visual Grounding**:",
                f"• MaxSim Alignment Score: `{top_hit.maxsim_score:.2f}`",
                f"• Referenced Document: `{top_hit.source_file}` (Page {top_hit.page_number})",
                f"• Top Contributing Query Tokens: `{', '.join(list(top_hit.token_alignment.keys())[:5]) if top_hit.token_alignment else 'N/A'}`"
            ]
            state.final_response = "\n".join(ans_parts)
            return state

        state.final_response = "Insufficient context: The provided clinical protocols and regulatory guidelines do not contain this information."
        return state

    def execute(self, query: str) -> ClinicalAgentState:
        """Executes the full compiled LangGraph workflow."""
        t0 = time.perf_counter()
        initial_state = ClinicalAgentState(user_query=query)
        result_state = self.workflow.invoke(initial_state)
        result_state.execution_time_ms = round((time.perf_counter() - t0) * 1000.0, 2)
        return result_state
