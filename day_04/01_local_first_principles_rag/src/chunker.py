"""
chunker.py
Production Recursive Character Text Splitter with Overlap Management.
Prevents context tearing at document boundaries and enriches chunks with metadata.
"""

from typing import List, Dict, Any
from .models import Document, Chunk

class EnterpriseRecursiveChunker:
    """
    Splits documents into semantic chunks using hierarchical separators.
    Preserves paragraph context, sentence structure, and metadata lineage.
    """
    def __init__(
        self,
        chunk_size: int = 350,
        chunk_overlap: int = 60,
        separators: List[str] = None
    ):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be strictly less than chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", "; ", ", ", " ", ""]

    def split_text(self, text: str) -> List[str]:
        """Splits raw string into overlapping chunks."""
        pieces: List[str] = []
        self._split_recursive(text, self.separators, pieces)
        return self._merge_pieces_with_overlap(pieces)

    def _split_recursive(self, text: str, separators: List[str], pieces: List[str]):
        if len(text) <= self.chunk_size:
            pieces.append(text)
            return

        separator = separators[-1]
        new_separators = []
        for i, sep in enumerate(separators):
            if sep == "":
                separator = ""
                break
            if sep in text:
                separator = sep
                new_separators = separators[i + 1:]
                break

        splits = text.split(separator) if separator != "" else list(text)

        for s in splits:
            s_clean = s.strip()
            if not s_clean:
                continue
            if len(s_clean) <= self.chunk_size or not new_separators:
                pieces.append(s_clean)
            else:
                self._split_recursive(s_clean, new_separators, pieces)

    def _merge_pieces_with_overlap(self, pieces: List[str]) -> List[str]:
        chunks: List[str] = []
        current_chunk: List[str] = []
        current_len = 0

        for piece in pieces:
            piece_len = len(piece)
            if current_len + piece_len + 1 > self.chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                
                # Compute overlap window from tail
                overlap_chars = 0
                overlap_pieces = []
                for p in reversed(current_chunk):
                    if overlap_chars + len(p) <= self.chunk_overlap:
                        overlap_pieces.insert(0, p)
                        overlap_chars += len(p) + 1
                    else:
                        break
                current_chunk = overlap_pieces
                current_len = sum(len(p) + 1 for p in current_chunk)

            current_chunk.append(piece)
            current_len += piece_len + 1

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def chunk_documents(self, documents: List[Document]) -> List[Chunk]:
        """Converts high-level Document objects into indexed, lineage-tracked Chunks."""
        all_chunks: List[Chunk] = []

        for doc_idx, doc in enumerate(documents):
            text_splits = self.split_text(doc.page_content)
            for chunk_idx, text in enumerate(text_splits):
                meta = doc.metadata.copy()
                meta["chunk_index"] = chunk_idx
                meta["total_document_chunks"] = len(text_splits)
                
                all_chunks.append(
                    Chunk(
                        text=text,
                        metadata=meta,
                        chunk_id=len(all_chunks),
                        doc_id=f"doc_{doc_idx}_chunk_{chunk_idx}"
                    )
                )
        return all_chunks
