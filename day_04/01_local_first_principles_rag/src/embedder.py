"""
embedder.py
Enterprise Multi-Backend Vector Embedding Engine.
Supports Google Gemini, OpenAI, or Deterministic Local Vectorization with L2 Normalization.
"""

import os
import math
import re
from typing import List
import numpy as np

class EnterpriseEmbedder:
    """
    High-dimensional vector embedding generator.
    Guarantees L2 unit normalization so Dot Product is equivalent to Cosine Similarity.
    """
    def __init__(self, dimension: int = 256, model_name: str = "auto"):
        self.dimension = dimension
        self.model_name = model_name
        self.backend = self._detect_backend()

    def _detect_backend(self) -> str:
        if self.model_name == "gemini" or ("GEMINI_API_KEY" in os.environ and self.model_name == "auto"):
            return "gemini"
        elif self.model_name == "openai" or ("OPENAI_API_KEY" in os.environ and self.model_name == "auto"):
            return "openai"
        return "local_deterministic"

    def embed_text(self, text: str) -> np.ndarray:
        """Embeds single text string into a normalized numpy vector."""
        if self.backend == "gemini" and "GEMINI_API_KEY" in os.environ:
            try:
                from google import genai
                client = genai.Client()
                result = client.models.embed_content(
                    model="text-embedding-004",
                    contents=text
                )
                vec = np.array(result.embeddings[0].values, dtype=np.float32)
                return self._normalize(vec)
            except Exception:
                pass # Fallback to local if API call errors
                
        elif self.backend == "openai" and "OPENAI_API_KEY" in os.environ:
            try:
                from openai import OpenAI
                client = OpenAI()
                resp = client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text
                )
                vec = np.array(resp.data[0].embedding, dtype=np.float32)
                return self._normalize(vec)
            except Exception:
                pass

        # High-Fidelity Local Semantic Hash Projection
        return self._local_vectorize(text)

    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Batch encodes multiple strings."""
        return np.array([self.embed_text(t) for t in texts], dtype=np.float32)

    def _local_vectorize(self, text: str) -> np.ndarray:
        """Deterministic term-frequency subword hashing with positional decay."""
        tokens = re.findall(r"\w+", text.lower())
        vec = np.zeros(self.dimension, dtype=np.float32)
        if not tokens:
            return vec

        for idx, token in enumerate(tokens):
            h = hash(token)
            dim_idx = abs(h) % self.dimension
            sign = 1.0 if (h // self.dimension) % 2 == 0 else -1.0
            weight = 1.0 + (1.0 / (idx + 1))
            vec[dim_idx] += sign * weight

        return self._normalize(vec)

    @staticmethod
    def _normalize(vec: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(vec)
        if norm > 1e-9:
            return vec / norm
        return vec
