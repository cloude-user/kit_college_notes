"""
chunker.py
Production Document Chunking Engine powered by LangChain's RecursiveCharacterTextSplitter.
Prevents semantic boundary tearing and preserves metadata lineage across all chunks.
"""

from typing import List, Dict, Any
from langchain_core.documents import Document as LCDocument
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .models import Document, Chunk

class EnterpriseRecursiveChunker:
    """
    Industrial chunker utilizing LangChain's RecursiveCharacterTextSplitter.
    Hierarchically splits text on paragraph, sentence, and word boundaries.
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
        self.separators = separators or ["\n## ", "\n### ", "\n\n", "\n", ". ", "; ", ", ", " ", ""]
        
        # Initialize official LangChain text splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
            length_function=len,
            is_separator_regex=False
        )

    def split_text(self, text: str) -> List[str]:
        """Splits raw string into overlapping chunks using LangChain splitter."""
        return self.splitter.split_text(text)

    def chunk_documents(self, documents: List[Document]) -> List[Chunk]:
        """
        Converts internal Document instances into semantic Chunk instances,
        preserving metadata lineage and chunk IDs.
        """
        all_chunks: List[Chunk] = []
        global_chunk_id = 0

        for doc_idx, doc in enumerate(documents):
            sub_texts = self.split_text(doc.page_content)
            for idx, text in enumerate(sub_texts):
                chunk_meta = dict(doc.metadata)
                chunk_meta["chunk_index"] = idx
                chunk_meta["total_subchunks"] = len(sub_texts)
                chunk_meta["char_length"] = len(text)
                
                src_clean = doc.metadata.get("source", f"doc_{doc_idx}")
                all_chunks.append(
                    Chunk(
                        text=text,
                        metadata=chunk_meta,
                        chunk_id=global_chunk_id,
                        doc_id=f"{src_clean}_chunk_{global_chunk_id}"
                    )
                )
                global_chunk_id += 1

        return all_chunks

    def chunk_to_langchain_documents(self, documents: List[Document]) -> List[LCDocument]:
        """
        Directly transforms documents into official LangChain Document instances.
        """
        chunks = self.chunk_documents(documents)
        lc_docs: List[LCDocument] = []
        for c in chunks:
            lc_docs.append(
                LCDocument(
                    page_content=c.text,
                    metadata=c.metadata
                )
            )
        return lc_docs
