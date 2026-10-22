"""
hybrid_retriever.py
Hybrid Retrieval Architecture combining Dense Vectors with Sparse BM25 Keyword Search.
Uses Reciprocal Rank Fusion (RRF) to merge rankings without score calibration artifacts.
"""

import math
import re
from collections import Counter
from typing import List, Tuple, Dict, Any, Optional
from .models import Chunk
from .vector_store import EnterpriseVectorStore

class SimpleBM25:
    """
    In-memory BM25 Okapi implementation for exact lexical keyword matching.
    """
    STOPWORDS = {
        "what", "is", "the", "for", "a", "an", "in", "to", "of", "and", "how", "do",
        "does", "by", "all", "are", "on", "with", "if", "during", "happens", "where",
        "when", "which", "our", "we", "this", "that", "these", "those", "from"
    }

    def __init__(self, corpus: List[str], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus)
        self.tokenized_corpus = [self._tokenize(doc) for doc in corpus]
        self.doc_lens = [len(doc) for doc in self.tokenized_corpus]
        self.avg_doc_len = (sum(self.doc_lens) / (self.corpus_size or 1)) or 1.0
        self.doc_freqs = Counter()
        for doc in self.tokenized_corpus:
            self.doc_freqs.update(set(doc))

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        # Keeps alphanumeric tokens and underscores (e.g. error codes ERR_504)
        return re.findall(r"[A-Za-z0-9_\-]+", text.lower())

    def get_scores(self, query: str) -> List[float]:
        raw_tokens = self._tokenize(query)
        q_tokens = [w for w in raw_tokens if w not in self.STOPWORDS] or raw_tokens
        scores = [0.0] * self.corpus_size

        for token in q_tokens:
            if token not in self.doc_freqs:
                continue
            df = self.doc_freqs[token]
            idf = math.log((self.corpus_size - df + 0.5) / (df + 0.5) + 1.0)
            
            # Boost exact alphanumeric identifiers (e.g. error codes or codes like GL-5120)
            is_exact_code = ("_" in token) or (any(c.isdigit() for c in token) and len(token) > 3)
            code_weight = 3.0 if is_exact_code else 1.0

            for i, doc in enumerate(self.tokenized_corpus):
                tf = doc.count(token)
                if tf > 0:
                    num = tf * (self.k1 + 1.0)
                    denom = tf + self.k1 * (1.0 - self.b + self.b * (self.doc_lens[i] / self.avg_doc_len))
                    scores[i] += idf * (num / denom) * code_weight
        return scores


class EnterpriseHybridRetriever:
    """
    Orchestrates Dense Semantic Search + Sparse BM25 via Reciprocal Rank Fusion.
    """
    def __init__(self, vector_store: EnterpriseVectorStore, rrf_k: int = 60):
        self.vector_store = vector_store
        self.rrf_k = rrf_k
        self._build_bm25_index()

    def _build_bm25_index(self):
        corpus_texts = [c.text for c in self.vector_store.chunks]
        self.bm25 = SimpleBM25(corpus_texts)

    def retrieve(
        self,
        query: str,
        top_k: int = 4,
        dense_weight: float = 0.5,
        bm25_weight: float = 0.5
    ) -> List[Tuple[Chunk, float]]:
        """
        Executes hybrid retrieval and fuses ranks via weighted RRF.
        Only items with positive relevance scores receive reciprocal rank contributions.
        """
        total_chunks = len(self.vector_store.chunks)
        if total_chunks == 0:
            return []

        # 1. Dense Semantic Retrieval
        dense_results = self.vector_store.search(query, top_k=total_chunks)
        dense_rank_map = {chunk.doc_id: rank for rank, (chunk, _) in enumerate(dense_results, 1)}

        # 2. Sparse Lexical BM25 Retrieval (Only positive hits receive BM25 rank)
        bm25_scores = self.bm25.get_scores(query)
        positive_bm25 = [(idx, score) for idx, score in enumerate(bm25_scores) if score > 0]
        positive_bm25.sort(key=lambda x: x[1], reverse=True)
        bm25_rank_map = {
            self.vector_store.chunks[idx].doc_id: rank
            for rank, (idx, _) in enumerate(positive_bm25, 1)
        }

        # 3. Reciprocal Rank Fusion (RRF)
        chunk_map = {c.doc_id: c for c in self.vector_store.chunks}
        fused_scores: Dict[str, float] = {}

        for doc_id, chunk in chunk_map.items():
            dense_rank = dense_rank_map.get(doc_id, total_chunks)
            rrf_dense = 1.0 / (self.rrf_k + dense_rank)
            rrf_bm25 = (1.0 / (self.rrf_k + bm25_rank_map[doc_id])) if doc_id in bm25_rank_map else 0.0

            composite_score = (dense_weight * rrf_dense) + (bm25_weight * rrf_bm25)
            fused_scores[doc_id] = composite_score

        # 4. Sort Descending
        sorted_docs = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
        return [(chunk_map[doc_id], score) for doc_id, score in sorted_docs[:top_k]]

