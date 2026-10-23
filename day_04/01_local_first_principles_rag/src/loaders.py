"""
loaders.py
Production Multi-Format Document Ingestion Engine.
Supports PDF (.pdf), Word (.docx), Markdown (.md), Plain Text (.txt), and Tabular CSV (.csv).
Supports both local file paths and in-memory uploaded byte streams (for Streamlit).
"""

import os
import csv
import io
import hashlib
from typing import List, Dict, Any, Tuple, Union
from .models import Document

class EnterpriseDocumentLoader:
    """
    Standardized multi-format loader converting diverse educational & enterprise files
    into normalized Document instances with structural metadata.
    """

    @staticmethod
    def _compute_content_hash(content: str) -> str:
        return hashlib.sha256(content.encode("utf-8", errors="ignore")).hexdigest()[:12]

    # --------------------------------------------------------------------------
    # 1. MARKDOWN LOADER
    # --------------------------------------------------------------------------
    @classmethod
    def load_markdown(cls, source: Union[str, io.BytesIO], filename: str = "document.md") -> List[Document]:
        """Loads Markdown and splits along section headers (# and ##)."""
        if isinstance(source, str):
            with open(source, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            file_name = os.path.basename(source)
        else:
            content = source.getvalue().decode("utf-8", errors="ignore")
            file_name = filename

        file_hash = cls._compute_content_hash(content)
        raw_sections = content.split("\n## ")
        documents: List[Document] = []

        for idx, sec in enumerate(raw_sections):
            text = sec.strip()
            if not text:
                continue
            if idx > 0 and not text.startswith("## "):
                text = "## " + text
            first_line = text.split("\n")[0].replace("#", "").strip()
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": file_name,
                        "file_hash": file_hash,
                        "section": first_line,
                        "format": "markdown",
                        "section_index": idx
                    }
                )
            )
        return documents

    # --------------------------------------------------------------------------
    # 2. PLAIN TEXT LOADER
    # --------------------------------------------------------------------------
    @classmethod
    def load_text(cls, source: Union[str, io.BytesIO], filename: str = "document.txt") -> List[Document]:
        """Loads plain text files and splits by double newline paragraphs."""
        if isinstance(source, str):
            with open(source, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            file_name = os.path.basename(source)
        else:
            content = source.getvalue().decode("utf-8", errors="ignore")
            file_name = filename

        file_hash = cls._compute_content_hash(content)
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        documents: List[Document] = []

        for idx, para in enumerate(paragraphs):
            documents.append(
                Document(
                    page_content=para,
                    metadata={
                        "source": file_name,
                        "file_hash": file_hash,
                        "section": f"Paragraph {idx + 1}",
                        "format": "text",
                        "section_index": idx
                    }
                )
            )
        return documents

    # --------------------------------------------------------------------------
    # 3. PDF LOADER (Using pypdf)
    # --------------------------------------------------------------------------
    @classmethod
    def load_pdf(cls, source: Union[str, io.BytesIO], filename: str = "document.pdf") -> List[Document]:
        """Loads PDF files and extracts text per page using pypdf."""
        documents: List[Document] = []
        try:
            from pypdf import PdfReader
            if isinstance(source, str):
                reader = PdfReader(source)
                file_name = os.path.basename(source)
            else:
                reader = PdfReader(source)
                file_name = filename

            for page_idx, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text() or ""
                page_text = page_text.strip()
                if page_text:
                    documents.append(
                        Document(
                            page_content=page_text,
                            metadata={
                                "source": file_name,
                                "page": page_idx,
                                "section": f"Page {page_idx}",
                                "format": "pdf",
                                "total_pages": len(reader.pages)
                            }
                        )
                    )
        except Exception as e:
            # Fallback if PDF parsing encounters an error
            err_doc = Document(
                page_content=f"[PDF extraction notice for {filename}: {str(e)}]",
                metadata={"source": filename, "format": "pdf", "error": str(e)}
            )
            documents.append(err_doc)

        return documents

    # --------------------------------------------------------------------------
    # 4. WORD (.DOCX) LOADER (Using python-docx)
    # --------------------------------------------------------------------------
    @classmethod
    def load_docx(cls, source: Union[str, io.BytesIO], filename: str = "document.docx") -> List[Document]:
        """Loads Word .docx documents, preserving paragraph and table structure."""
        documents: List[Document] = []
        try:
            import docx
            doc = docx.Document(source)
            file_name = os.path.basename(source) if isinstance(source, str) else filename

            # Group paragraphs under headings
            current_heading = "General"
            current_block: List[str] = []
            block_idx = 0

            for p in doc.paragraphs:
                text = p.text.strip()
                if not text:
                    continue
                if p.style.name.startswith("Heading"):
                    if current_block:
                        documents.append(
                            Document(
                                page_content="\n".join(current_block),
                                metadata={
                                    "source": file_name,
                                    "section": current_heading,
                                    "format": "docx",
                                    "section_index": block_idx
                                }
                            )
                        )
                        block_idx += 1
                        current_block = []
                    current_heading = text
                else:
                    current_block.append(text)

            if current_block:
                documents.append(
                    Document(
                        page_content="\n".join(current_block),
                        metadata={
                            "source": file_name,
                            "section": current_heading,
                            "format": "docx",
                            "section_index": block_idx
                        }
                    )
                )

            # Also extract tables from docx
            for t_idx, table in enumerate(doc.tables, start=1):
                table_lines = []
                for row in table.rows:
                    row_cells = [c.text.strip().replace("\n", " ") for c in row.cells]
                    table_lines.append(" | ".join(row_cells))
                if table_lines:
                    documents.append(
                        Document(
                            page_content="\n".join(table_lines),
                            metadata={
                                "source": file_name,
                                "section": f"Table {t_idx}",
                                "format": "docx_table"
                            }
                        )
                    )
        except Exception as e:
            err_doc = Document(
                page_content=f"[DOCX extraction notice for {filename}: {str(e)}]",
                metadata={"source": filename, "format": "docx", "error": str(e)}
            )
            documents.append(err_doc)

        return documents

    # --------------------------------------------------------------------------
    # 5. TABULAR CSV LOADER
    # --------------------------------------------------------------------------
    @classmethod
    def load_csv(cls, source: Union[str, io.BytesIO], filename: str = "data.csv") -> Tuple[List[Document], List[Dict[str, Any]]]:
        """
        Loads CSV files and converts each row into a descriptive semantic sentence
        for vector indexing, while also returning the raw dict rows for deterministic queries.
        """
        if isinstance(source, str):
            with open(source, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            file_name = os.path.basename(source)
        else:
            content = source.getvalue().decode("utf-8", errors="ignore")
            file_name = filename

        documents: List[Document] = []
        raw_rows: List[Dict[str, Any]] = []

        reader = csv.DictReader(io.StringIO(content))
        for row_idx, row in enumerate(reader, start=1):
            clean_row = {k.strip(): (v.strip() if v else "") for k, v in row.items() if k}
            raw_rows.append(clean_row)

            # Build readable sentence from key-value pairs
            row_parts = [f"{k}: {v}" for k, v in clean_row.items() if v]
            row_summary = " | ".join(row_parts)
            semantic_sentence = f"Record [{file_name} #{row_idx}]: {row_summary}"

            documents.append(
                Document(
                    page_content=semantic_sentence,
                    metadata={
                        "source": file_name,
                        "format": "csv_tabular",
                        "row_id": row_idx,
                        **clean_row
                    }
                )
            )

        return documents, raw_rows

    # --------------------------------------------------------------------------
    # 6. UNIVERSAL DISPATCHER
    # --------------------------------------------------------------------------
    @classmethod
    def load_any_file(cls, source: Union[str, io.BytesIO], filename: str = "") -> Tuple[List[Document], List[Dict[str, Any]]]:
        """Auto-detects file extension and invokes the corresponding parser."""
        name = filename if filename else (os.path.basename(source) if isinstance(source, str) else "unknown")
        ext = os.path.splitext(name)[1].lower()

        if ext == ".pdf":
            return cls.load_pdf(source, filename=name), []
        elif ext in [".docx", ".doc"]:
            return cls.load_docx(source, filename=name), []
        elif ext == ".csv":
            return cls.load_csv(source, filename=name)
        elif ext in [".txt", ".log"]:
            return cls.load_text(source, filename=name), []
        else:
            # Default to Markdown / Text parser
            return cls.load_markdown(source, filename=name), []

    # --------------------------------------------------------------------------
    # 7. BULK REPOSITORY LOADER
    # --------------------------------------------------------------------------
    @classmethod
    def load_all_documents(cls, data_dir: str) -> Tuple[List[Document], List[Dict[str, Any]]]:
        """Discovers and parses all supported documents in data_dir."""
        all_docs: List[Document] = []
        all_rows: List[Dict[str, Any]] = []

        if not os.path.exists(data_dir):
            raise FileNotFoundError(f"Data directory not found: {data_dir}")

        for fname in sorted(os.listdir(data_dir)):
            fpath = os.path.join(data_dir, fname)
            if os.path.isfile(fpath):
                docs, rows = cls.load_any_file(fpath, filename=fname)
                all_docs.extend(docs)
                all_rows.extend(rows)

        return all_docs, all_rows

    # Backwards compatibility alias
    load_all_enterprise_documents = load_all_documents
