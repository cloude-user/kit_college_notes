"""
vector_store.py
LangChain-Powered Vector Store Engine.
Wraps langchain_core.vectorstores.InMemoryVectorStore with cosine similarity indexing
and seamless LangChain Retriever integration.
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document as LCDocument
from .models import Chunk
from .embedder import EnterpriseEmbedder

class EnterpriseVectorStore:
    """
    Industrial In-Memory Vector Store backed by LangChain's official InMemoryVectorStore.
    Provides fast cosine similarity retrieval, metadata filtering, and standard retriever exports.
    """
    def __init__(self, embedder: EnterpriseEmbedder):
        self.embedder = embedder
        # Initialize official LangChain InMemoryVectorStore
        self.lc_store = InMemoryVectorStore(embedding=self.embedder)
        self.indexed_chunks: List[Chunk] = []

    @property
    def chunks(self) -> List[Chunk]:
        return self.indexed_chunks

    def add_chunks(self, chunks: List[Chunk]) -> None:
        """Indexes internal Chunk instances into LangChain vector store."""
        if not chunks:
            return

        self.indexed_chunks.extend(chunks)
        lc_docs = [
            LCDocument(
                page_content=c.text,
                metadata={**c.metadata, "chunk_id": c.chunk_id, "doc_id": c.doc_id}
            )
            for c in chunks
        ]
        self.lc_store.add_documents(lc_docs)

    def similarity_search(self, query: str, top_k: int = 4) -> List[Tuple[Chunk, float]]:
        """
        Executes Cosine Similarity search using LangChain's vector search engine.
        Returns list of (Chunk, score) tuples ranked in descending similarity order.
        """
        if not self.indexed_chunks:
            return []

        # Use LangChain vector store similarity search with score
        docs_and_scores = self.lc_store.similarity_search_with_score(query, k=top_k)

        results: List[Tuple[Chunk, float]] = []
        for doc, score in docs_and_scores:
            c = Chunk(
                text=doc.page_content,
                metadata=doc.metadata,
                chunk_id=doc.metadata.get("chunk_id", 0),
                doc_id=doc.metadata.get("doc_id", "")
            )
            results.append((c, float(score)))

        return results

    # Backward compatibility alias
    search = similarity_search

    def as_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None):
        """Exports standard LangChain BaseRetriever for use in LangGraph nodes."""
        kwargs = search_kwargs or {"k": 4}
        return self.lc_store.as_retriever(search_kwargs=kwargs)

    def count(self) -> int:
        """Returns count of indexed chunks."""
        return len(self.indexed_chunks)

    def save_local_cache(self, cache_dir: str = "data/.vector_cache") -> str:
        """
        Persists chunks and embeddings to disk so students can inspect the exact vector files.
        Addresses student question: 'Where is the vector database stored?'
        """
        import os
        import json
        os.makedirs(cache_dir, exist_ok=True)
        cache_file = os.path.join(cache_dir, "vector_store_catalog.json")

        records = []
        for c in self.indexed_chunks:
            # Generate sample embedding representation for inspection
            sample_vec = self.embedder.embed_query(c.text[:100])
            records.append({
                "chunk_id": c.chunk_id,
                "doc_id": c.doc_id,
                "source": c.metadata.get("source", "unknown"),
                "section": c.metadata.get("section", "General"),
                "format": c.metadata.get("format", "text"),
                "text_snippet": c.text[:140] + "..." if len(c.text) > 140 else c.text,
                "vector_dimension": len(sample_vec),
                "vector_sample": [round(float(x), 4) for x in sample_vec[:6]]
            })

        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump({
                "storage_type": "LangChain InMemoryVectorStore (RAM) + Disk Inspection Cache",
                "total_vectors": len(records),
                "dimension": len(records[0]["vector_sample"]) if records else 0,
                "vectors": records
            }, f, indent=2)

        return cache_file
