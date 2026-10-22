"""
models.py
Enterprise Data Models and Type Definitions for BioPharma Multi-Agent RAG.
FDA 21 CFR Part 312 / 11 Clinical Protocol & Safety Architecture.
"""

from typing import List, Dict, Any, Optional, Literal
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class DocumentPage:
    """Represents a discrete document page or visual layout element."""
    doc_id: str
    source_file: str
    page_number: int
    text_content: str
    visual_type: Literal["text", "table", "flowchart", "dosing_grid", "kaplan_meier"] = "text"
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ColPaliEmbeddingResult:
    """Multi-vector patch representation for ColPali late-interaction."""
    doc_id: str
    page_number: int
    source_file: str
    patch_embeddings: Any # np.ndarray shape (num_patches, embedding_dim)
    text_content: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RetrievalHit:
    """A scored retrieval candidate with multi-vector late-interaction match details."""
    doc_id: str
    source_file: str
    page_number: int
    text_content: str
    maxsim_score: float
    token_alignment: Optional[Dict[str, float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ClinicalStatsResult:
    """Deterministic analytics aggregated from the clinical safety ledger."""
    total_records: int
    cohort_filter: Optional[str]
    site_filter: Optional[str]
    total_saes: int
    sae_rate_percent: float
    grade_distribution: Dict[str, int]
    drug_relationship_counts: Dict[str, int]
    fatal_count: int
    overdue_fda_reports: int
    stopping_rule_triggered: bool
    stopping_rule_details: str
    summary_text: str

@dataclass
class LangGraphAgentStep:
    """Trace of an individual agent step within the LangGraph StateGraph."""
    node_name: str
    thought: str
    action_taken: str
    payload: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class ClinicalAgentState:
    """State object passed between nodes in the LangGraph StateGraph."""
    user_query: str
    intent: str = "unknown"
    retrieved_hits: List[RetrievalHit] = field(default_factory=list)
    clinical_stats: Optional[ClinicalStatsResult] = None
    final_response: str = ""
    citations: List[str] = field(default_factory=list)
    requires_hitl: bool = False
    hitl_status: Literal["NOT_REQUIRED", "PENDING_APPROVAL", "APPROVED", "REJECTED"] = "NOT_REQUIRED"
    hitl_reason: str = ""
    trace: List[LangGraphAgentStep] = field(default_factory=list)
    execution_time_ms: float = 0.0
