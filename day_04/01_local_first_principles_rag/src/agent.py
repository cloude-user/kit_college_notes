"""
agent.py
Autonomous Multi-Agent Router and ReAct Execution Engine.
Routes queries to Unstructured Hybrid RAG, Structured Financial Analytics, or Compliance Audits.
"""

import time
from typing import List, Dict, Any, Optional
from .models import AgentStep, AgentRunResult, GroundedResponse
from .hybrid_retriever import EnterpriseHybridRetriever
from .reranker import EnterpriseReranker
from .generator import EnterpriseGroundedGenerator

class EnterpriseMultiAgentRouter:
    """
    Autonomous ReAct agent that classifies intent and coordinates specialized enterprise tools.
    """
    def __init__(
        self,
        retriever: EnterpriseHybridRetriever,
        reranker: EnterpriseReranker,
        generator: EnterpriseGroundedGenerator,
        raw_ledger: List[Dict[str, Any]]
    ):
        self.retriever = retriever
        self.reranker = reranker
        self.generator = generator
        self.raw_ledger = raw_ledger

    # --------------------------------------------------------------------------
    # SPECIALIZED TOOL 1: UNSTRUCTURED HYBRID RAG
    # --------------------------------------------------------------------------
    def tool_unstructured_rag(self, query: str) -> GroundedResponse:
        """Retrieves and generates verified answers from SEC filings and policy manuals."""
        candidates = self.retriever.retrieve(query, top_k=6)
        reranked = self.reranker.rerank(query, candidates, top_n=3)
        return self.generator.generate(query, reranked)

    # --------------------------------------------------------------------------
    # SPECIALIZED TOOL 2: STRUCTURED FINANCIAL LEDGER ANALYTICS
    # --------------------------------------------------------------------------
    def tool_structured_analytics(
        self,
        department: Optional[str] = None,
        quarter: Optional[str] = None,
        gl_account: Optional[str] = None
    ) -> str:
        """Performs exact deterministic aggregation on the financial transactions ledger."""
        filtered = self.raw_ledger
        if department:
            filtered = [r for r in filtered if department.lower() in r.get("department_name", "").lower()]
        if quarter:
            filtered = [r for r in filtered if quarter.lower() == r.get("quarter", "").lower()]
        if gl_account:
            filtered = [r for r in filtered if gl_account.lower() in r.get("gl_account", "").lower()]

        if not filtered:
            return "No ledger entries found matching specified department, quarter, or GL account filters."

        total_budget = sum(float(r.get("allocated_budget_usd", 0)) for r in filtered)
        total_spend = sum(float(r.get("actual_spend_usd", 0)) for r in filtered)
        net_variance = total_spend - total_budget
        over_budget_depts = [f"{r['department_name']} ({r.get('quarter', '')})" for r in filtered if r.get("status") == "Over-Budget"]
        notes_list = [r.get("notes") for r in filtered if r.get("notes")]

        summary_lines = [
            "Structured Financial Ledger Analysis:",
            f"• Records Analyzed: {len(filtered)}",
            f"• Total Allocated Budget: ${total_budget:,.2f}",
            f"• Total Actual Spend: ${total_spend:,.2f}",
            f"• Net Variance: ${net_variance:+,.2f} ({'OVER BUDGET' if net_variance > 0 else 'UNDER BUDGET'})",
            f"• Departments Flagged Over-Budget: {', '.join(set(over_budget_depts)) if over_budget_depts else 'None'}"
        ]
        if notes_list and len(notes_list) <= 3:
            summary_lines.append(f"• Auditor Notes: {' | '.join(notes_list)}")

        return "\n".join(summary_lines)

    # --------------------------------------------------------------------------
    # SPECIALIZED TOOL 3: PROCUREMENT THRESHOLD VALIDATOR
    # --------------------------------------------------------------------------
    def tool_procurement_validator(self, amount_usd: float) -> str:
        """Calculates mandatory sign-off tier for corporate expenditures."""
        if amount_usd < 25000:
            return f"Authorization Tier 1: Direct Manager sole sign-off required for ${amount_usd:,.2f}."
        elif amount_usd <= 100000:
            return f"Authorization Tier 2: Vice President (VP) and Finance Controller sign-off required for ${amount_usd:,.2f}."
        elif amount_usd <= 500000:
            return f"Authorization Tier 3: CFO and CISO dual authorization required for ${amount_usd:,.2f}."
        else:
            return f"Authorization Tier 4: Formal Board of Directors Audit Committee approval and 3 competitive bids required for ${amount_usd:,.2f}."

    # --------------------------------------------------------------------------
    # AUTONOMOUS REACT DISPATCH LOOP
    # --------------------------------------------------------------------------
    def execute(self, user_query: str) -> AgentRunResult:
        start_time = time.perf_counter()
        steps: List[AgentStep] = []
        q_lower = user_query.lower()
        import re

        # Step 1: Reason about intent
        # Check if query is structured numeric analytics (spend, budget, ledger, variance, GL account)
        is_gl_query = bool(re.search(r"gl[-\s]?\d{4}", q_lower))
        is_ledger_query = any(term in q_lower for term in ["spend", "budget", "ledger", "variance", "actual spend", "total spend"])

        if is_gl_query or is_ledger_query:
            thought = "User inquiry requires deterministic aggregation across numeric ledger records. Routing to Structured Analytics Tool."
            action = "tool_structured_analytics"

            # Parse GL code
            gl_match = re.search(r"gl[-\s]?\d{4}", q_lower)
            gl_code = gl_match.group(0).upper().replace(" ", "-") if gl_match else None

            # Parse Quarter
            quarter = None
            for q in ["q1", "q2", "q3", "q4"]:
                if q in q_lower:
                    quarter = q
                    break

            # Parse Department
            dept = None
            dept_map = {
                "ai": "Engineering-AI",
                "engineering": "Engineering-AI",
                "infrastructure": "Cloud-Infrastructure",
                "cloud": "Cloud-Infrastructure",
                "security": "Security-Compliance",
                "compliance": "Security-Compliance",
                "sales": "Sales-Enterprise",
                "customer success": "Customer-Success",
                "sla": "Customer-Success" if "penalty" in q_lower or "penalties" in q_lower else None,
                "legal": "Legal-Regulatory",
                "data": "Data-Platform",
                "platform": "Data-Platform"
            }
            for k, v in dept_map.items():
                if v and k in q_lower:
                    dept = v
                    break

            action_input = {"department": dept, "quarter": quarter, "gl_account": gl_code}
            observation = self.tool_structured_analytics(**action_input)
            final_ans = observation

        elif any(term in q_lower for term in ["approval", "procure", "authorization tier", "buy", "threshold", "purchase order"]) and any(char.isdigit() for char in user_query):
            thought = "User inquiry relates to dollar authorization thresholds. Routing to Procurement Validator Tool."
            action = "tool_procurement_validator"
            nums = re.findall(r"\d[\d,]*", user_query.replace("$", ""))
            amount = float(nums[0].replace(",", "")) if nums else 50000.0
            action_input = {"amount_usd": amount}
            observation = self.tool_procurement_validator(amount)
            final_ans = observation

        else:
            thought = "User inquiry relates to qualitative corporate policy, SEC filings, or hardware warranty. Routing to Unstructured Hybrid RAG."
            action = "tool_unstructured_rag"
            action_input = {"query": user_query}
            grounded_resp = self.tool_unstructured_rag(user_query)
            observation = f"Retrieved {len(grounded_resp.citations)} verified citations. Answer: {grounded_resp.answer}"
            final_ans = grounded_resp.answer

        steps.append(
            AgentStep(
                thought=thought,
                action=action,
                action_input=action_input,
                observation=observation
            )
        )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return AgentRunResult(
            user_query=user_query,
            steps=steps,
            final_response=final_ans,
            execution_time_ms=round(elapsed_ms, 2)
        )
