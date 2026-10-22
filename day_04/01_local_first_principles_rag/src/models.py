"""
models.py
Enterprise Domain Schemas and Pydantic Data Models.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from pydantic import BaseModel, Field

@dataclass
class Document:
    page_content: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Chunk:
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    chunk_id: int = 0
    doc_id: str = ""

class GroundedCitation(BaseModel):
    claim: str = Field(description="The factual claim asserted")
    doc_tag: str = Field(description="The source bracket tag, e.g. [Doc 1]")
    source_file: str = Field(description="The file name where the fact resides")
    verified: bool = Field(default=True, description="Whether citation was verified in context")

class GroundedResponse(BaseModel):
    query: str
    answer: str
    citations: List[GroundedCitation] = Field(default_factory=list)
    has_sufficient_context: bool = True
    confidence_score: float = 1.0

class RAGASMetrics(BaseModel):
    faithfulness: float = Field(ge=0.0, le=1.0)
    answer_relevancy: float = Field(ge=0.0, le=1.0)
    context_precision: float = Field(ge=0.0, le=1.0)
    context_recall: float = Field(ge=0.0, le=1.0)
    passed_quality_gate: bool = True
    diagnostic_message: str = "Quality benchmarks satisfied."

class AgentStep(BaseModel):
    thought: str
    action: str
    action_input: Dict[str, Any]
    observation: str

class AgentRunResult(BaseModel):
    user_query: str
    steps: List[AgentStep] = Field(default_factory=list)
    final_response: str
    execution_time_ms: float = 0.0
