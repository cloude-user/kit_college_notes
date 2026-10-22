"""
vector_store.py
Enterprise In-Memory Vector Database with Cosine Matrix Operations and Metadata Filtering.
"""

from typing import List, Tuple, Dict, Any, Callable, Optional
import numpy as np
from .models import Chunk
from .embedder import EnterpriseEmbedder

class EnterpriseVectorStore:
    """
    High-performance in-memory vector database supporting pre-filtering and Top-K retrieval.
    """
    def __init__(self, embedder: EnterpriseEmbedder):
        self.embedder = embedder
        self.chunks: List[Chunk] = []
        self.vectors: Optional[np.ndarray] = None

    def add_chunks(self, chunks: List[Chunk]):
        """Embeds and indexes incoming document chunks."""
        if not chunks:
            return

        texts = [c.text for c in chunks]
        new_vecs = self.embedder.embed_batch(texts)

        if self.vectors is None:
            self.vectors = new_vecs
        else:
            self.vectors = np.vstack([self.vectors, new_vecs])

        self.chunks.extend(chunks)

    def search(
        self,
        query: str,
        top_k: int = 4,
        metadata_filter: Optional[Callable[[Dict[str, Any]], bool]] = None
    ) -> List[Tuple[Chunk, float]]:
        """
        Executes Top-K cosine similarity search against indexed vector space.
        Supports optional metadata pre-filtering lambda predicates.
        """
        if self.vectors is None or len(self.chunks) == 0:
            return []

        query_vec = self.embedder.embed_text(query)

        # Vectorized dot product (equivalent to cosine similarity on unit vectors)
        scores = np.dot(self.vectors, query_vec)

        # Apply metadata pre-filtering if provided
        candidate_indices = []
        for idx, chunk in enumerate(self.chunks):
            if metadata_filter is None or metadata_filter(chunk.metadata):
                candidate_indices.append(idx)

        if not candidate_indices:
            return []

        filtered_scores = [(self.chunks[i], float(scores[i])) for i in candidate_indices]
        filtered_scores.sort(key=lambda x: x[1], reverse=True)

        return filtered_scores[:top_k]

    def count(self) -> int:
        return len(self.chunks)
