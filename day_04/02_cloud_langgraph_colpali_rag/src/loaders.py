"""
loaders.py
Enterprise Document & Clinical Ledger Ingestion Suite.
Segments protocols, guidelines, and charters into structured DocumentPage objects.
"""

import os
from pathlib import Path
from typing import List, Tuple
from .models import DocumentPage

class ClinicalDocumentLoader:
    """Loads and formats clinical trial protocols and regulatory manuals."""

    @staticmethod
    def load_all_documents(data_dir: str) -> List[DocumentPage]:
        pages: List[DocumentPage] = []
        path = Path(data_dir)

        for file_path in path.glob("*.md"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Split document by major H2 sections (##) to treat each as a distinct visual page/layout
            sections = content.split("\n## ")
            doc_title = sections[0].split("\n")[0].replace("#", "").strip()

            # First section (Page 1)
            pages.append(
                DocumentPage(
                    doc_id=f"{file_path.stem}_p1",
                    source_file=file_path.name,
                    page_number=1,
                    text_content=sections[0].strip(),
                    visual_type="text",
                    metadata={"document_title": doc_title, "section": "Header & Overview"}
                )
            )

            # Subsequent sections
            for idx, sec in enumerate(sections[1:], 2):
                sec_text = "## " + sec
                # Detect markdown table structure (header separator with dashes and pipes)
                has_table = ("|" in sec_text) and any(marker in sec_text for marker in ["---", "-|-", "|:", ":|"])
                visual_type = "table" if has_table else "text"
                sec_title = sec.split("\n")[0].strip()
                
                pages.append(
                    DocumentPage(
                        doc_id=f"{file_path.stem}_p{idx}",
                        source_file=file_path.name,
                        page_number=idx,
                        text_content=sec_text.strip(),
                        visual_type=visual_type,
                        metadata={"document_title": doc_title, "section": sec_title}
                    )
                )

        return pages
