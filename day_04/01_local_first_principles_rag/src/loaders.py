"""
loaders.py
Production Multi-Format Document Ingestion Engine.
Handles Markdown documents, structural section extraction, and tabular CSV rows.
"""

import os
import csv
import hashlib
from typing import List, Dict, Any, Tuple
from .models import Document

class EnterpriseDocumentLoader:
    """
    Standardized enterprise loader converting diverse files into Document instances.
    """
    
    @staticmethod
    def _compute_file_hash(content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()[:12]

    @classmethod
    def load_markdown_file(cls, file_path: str) -> List[Document]:
        """
        Loads markdown documents and splits by top-level section headers (# and ##)
        to maintain semantic locality.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        file_name = os.path.basename(file_path)
        file_hash = cls._compute_file_hash(content)

        # Split along markdown header boundaries (e.g., "\n## ")
        raw_sections = content.split("\n## ")
        documents: List[Document] = []

        for idx, sec in enumerate(raw_sections):
            text = sec.strip()
            if not text:
                continue
            
            # Re-attach the header marker if it was split
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

    @classmethod
    def load_csv_as_semantic_documents(cls, file_path: str) -> Tuple[List[Document], List[Dict[str, Any]]]:
        """
        Loads CSV files and converts each row into a descriptive semantic sentence
        for vector indexing, while also returning the raw dict rows for SQL analytics.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_name = os.path.basename(file_path)
        documents: List[Document] = []
        raw_rows: List[Dict[str, Any]] = []

        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row_idx, row in enumerate(reader, start=1):
                raw_rows.append(dict(row))
                
                # Build rich natural-language semantic representation
                txn_id = row.get("transaction_id", f"TXN-{row_idx:04d}")
                gl_acct = row.get("gl_account", "")
                cost_center = row.get("cost_center", "")
                dept = row.get("department_name", "Unknown")
                quarter = row.get("quarter", "")
                cat = row.get("category", "")
                budget = row.get("allocated_budget_usd", "0")
                spend = row.get("actual_spend_usd", "0")
                status = row.get("status", "")
                variance_pct = row.get("variance_percent", "0")
                notes = row.get("notes", "")

                gl_part = f", {gl_acct}" if gl_acct else ""
                cc_part = f", {cost_center}" if cost_center else ""
                notes_part = f" Notes: {notes}." if notes else ""

                semantic_sentence = (
                    f"Financial Ledger Record [{txn_id}]: Department '{dept}' ({quarter}{cc_part}{gl_part}) incurred actual spend of ${spend} "
                    f"against allocated budget ${budget} for category '{cat}'. Variance: {variance_pct}% (Status: {status}).{notes_part}"
                )

                documents.append(
                    Document(
                        page_content=semantic_sentence,
                        metadata={
                            "source": file_name,
                            "format": "csv_tabular",
                            "row_id": row_idx,
                            "transaction_id": txn_id,
                            "gl_account": gl_acct,
                            "cost_center": cost_center,
                            "department": dept,
                            "quarter": quarter,
                            "category": cat
                        }
                    )
                )
        return documents, raw_rows

    @classmethod
    def load_all_enterprise_documents(cls, data_dir: str) -> Tuple[List[Document], List[Dict[str, Any]]]:
        """
        Discovers and ingests all enterprise documents in the specified directory:
        - SEC 10-Q / 10-K filings (.md)
        - Corporate Compliance & Security Policies (.md)
        - Master Services Agreements & SLAs (.md)
        - General Ledger Transactions (.csv)
        """
        all_docs: List[Document] = []
        raw_ledger: List[Dict[str, Any]] = []

        if not os.path.exists(data_dir):
            raise FileNotFoundError(f"Data directory not found: {data_dir}")

        for fname in sorted(os.listdir(data_dir)):
            fpath = os.path.join(data_dir, fname)
            if fname.endswith(".md"):
                docs = cls.load_markdown_file(fpath)
                all_docs.extend(docs)
            elif fname.endswith(".csv"):
                tab_docs, ledger = cls.load_csv_as_semantic_documents(fpath)
                all_docs.extend(tab_docs)
                raw_ledger.extend(ledger)

        return all_docs, raw_ledger

