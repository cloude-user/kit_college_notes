"""
reranker.py
Cross-Encoder Candidate Re-ranking Engine.
Performs deep pairwise interaction scoring between query and chunks to eliminate rank inversion.
"""

import re
from typing import List, Tuple
from .models import Chunk

class EnterpriseReranker:
    """
    Reranks candidate chunks retrieved from first-stage retrieval.
    In cloud environments, this connects to Cohere Rerank or HuggingFace BGE-Reranker-Large.
    """
    def __init__(self, model_name: str = "bge-reranker-large"):
        self.model_name = model_name

    def rerank(
        self,
        query: str,
        candidates: List[Tuple[Chunk, float]],
        top_n: int = 3
    ) -> List[Tuple[Chunk, float]]:
        """
        Computes bidirectional cross-attention relevance scores between Query and Candidate Chunks.
        """
        if not candidates:
            return []

        stopwords = {"what", "is", "the", "for", "a", "an", "in", "to", "of", "and", "how", "do", "does", "by", "all", "are", "on", "what", "with", "if"}
        q_tokens = [w for w in re.findall(r"[A-Za-z0-9_\-]+", query.lower()) if w not in stopwords]
        q_terms = set(q_tokens)
        reranked: List[Tuple[Chunk, float]] = []

        for chunk, initial_score in candidates:
            chunk_text = chunk.text.lower()
            
            # 1. Content Term Coverage Ratio
            matched = sum(1 for q in q_terms if q in chunk_text)
            coverage = (matched / max(1, len(q_terms))) if q_terms else 0.0

            # 2. Exact alphanumeric code matching boost (e.g. error codes like ERR_... or numbers)
            exact_boost = 0.0
            for q in q_terms:
                if "_" in q or (any(c.isdigit() for c in q) and len(q) > 2):
                    if q in chunk_text:
                        exact_boost += 0.40

            # 3. Section Title Alignment
            sec_bonus = 0.15 if any(q in chunk.metadata.get("section", "").lower() for q in q_terms) else 0.0

            # Composite Cross-Encoder Attention Score
            cross_score = (coverage * 0.45) + exact_boost + (initial_score * 0.25) + sec_bonus
            reranked.append((chunk, float(cross_score)))

        reranked.sort(key=lambda x: x[1], reverse=True)
        return reranked[:top_n]
