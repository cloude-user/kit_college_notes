"""
generator.py
Grounded Generation & Hallucination Guardrail Engine.
Powered by Google Gemini (Gemini 3.7 Flash, 3.6 Flash, 3.5 Flash Lite via Google GenAI SDK).
Enforces bracket citations ([Doc 1: filename]) and handles out-of-context edge cases defensively.
"""

import os
import re
from typing import List, Tuple
from .models import Chunk, GroundedResponse, GroundedCitation

class EnterpriseGroundedGenerator:
    """
    Constructs context-augmented prompts and generates verified, cited enterprise & academic responses.
    Utilizes modern Google Gemini models (3.7 / 3.6 / 3.5).
    """
    def __init__(self, model_name: str = "auto", temperature: float = 0.1):
        self.temperature = temperature
        self.model_name = model_name or os.environ.get("GEMINI_MODEL", "gemini-3.7-flash")

    def _resolve_gemini_model(self) -> str:
        """Selects the modern active Gemini model, prioritizing 3.7 and 3.6."""
        candidate = os.environ.get("GEMINI_MODEL", "gemini-3.7-flash")
        if candidate in ["gemini-1.5-flash", "gemini-1.5-pro"]:
            return "gemini-3.7-flash"  # Upgrade deprecated 1.5 references
        return candidate

    def build_prompt(self, query: str, chunks: List[Tuple[Chunk, float]]) -> str:
        """Assembles authoritative context blocks with bracket citation identifiers."""
        context_blocks = []
        for rank, (chunk, score) in enumerate(chunks, 1):
            source = chunk.metadata.get("source", "unknown")
            section = chunk.metadata.get("section", "General")
            context_blocks.append(
                f"[Doc {rank}] (Source: {source} | Section: {section} | Score: {score:.3f}):\n{chunk.text}"
            )

        context_payload = "\n\n".join(context_blocks)

        system_prompt = f"""SYSTEM INSTRUCTION:
You are an authoritative, helpful Academic Mentor and Institutional Policy Advisor for KIT College of Engineering.
Answer the student's inquiry strictly and solely using the provided reference context below.

MANDATORY RULES:
1. Every single factual statement, numeric threshold, fee, percentage, or deadline must include
   an explicit bracket citation pointing to the source document, e.g., [Doc 1], [Doc 2].
2. If the reference context does not contain adequate evidence to answer the question, you MUST reply:
   "Insufficient context: The provided enterprise documentation does not contain this information."
3. Do not extrapolate, assume, or inject ungrounded external rumors or rules.

---
REFERENCE CONTEXT:
{context_payload}
---

STUDENT INQUIRY:
{query}
"""
        return system_prompt

    def generate(self, query: str, retrieved_chunks: List[Tuple[Chunk, float]]) -> GroundedResponse:
        """
        Executes grounded generation using Gemini 3.7 / 3.6 if API key is present,
        or deterministic offline grounder if running locally without keys.
        """
        if not retrieved_chunks:
            return GroundedResponse(
                query=query,
                answer="Insufficient context: No matching college documents found in the database.",
                citations=[],
                has_sufficient_context=False,
                confidence_score=0.0
            )

        prompt = self.build_prompt(query, retrieved_chunks)

        # 1. Cloud LLM generation using Google GenAI SDK (Gemini 3.7 / 3.6 / 3.5)
        if "GEMINI_API_KEY" in os.environ and os.environ.get("OFFLINE_MODE", "false").lower() != "true":
            try:
                from google import genai
                client = genai.Client()
                model_id = self._resolve_gemini_model()
                
                resp = client.models.generate_content(
                    model=model_id,
                    contents=prompt
                )
                answer_text = resp.text.strip()
                return self._parse_and_verify_citations(query, answer_text, retrieved_chunks)
            except Exception:
                # If selected 3.7 model fails (e.g. rate limit or region), attempt 3.6-flash fallback
                try:
                    from google import genai
                    client = genai.Client()
                    resp = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )
                    answer_text = resp.text.strip()
                    return self._parse_and_verify_citations(query, answer_text, retrieved_chunks)
                except Exception:
                    pass  # Fallback to local grounder

        elif "OPENAI_API_KEY" in os.environ:
            try:
                from openai import OpenAI
                client = OpenAI()
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature
                )
                answer_text = resp.choices[0].message.content.strip()
                return self._parse_and_verify_citations(query, answer_text, retrieved_chunks)
            except Exception:
                pass

        # 2. Local Deterministic Academic Grounder (Failsafe offline generator)
        return self._local_grounded_synthesis(query, retrieved_chunks)

    def _parse_and_verify_citations(
        self,
        query: str,
        answer_text: str,
        retrieved_chunks: List[Tuple[Chunk, float]]
    ) -> GroundedResponse:
        """Extracts [Doc X] citation tags and verifies against retrieved chunk metadata."""
        doc_tags = re.findall(r"\[Doc\s*(\d+)\]", answer_text)
        citations: List[GroundedCitation] = []
        is_insufficient = "insufficient context" in answer_text.lower()

        for tag_num_str in set(doc_tags):
            tag_num = int(tag_num_str)
            if 1 <= tag_num <= len(retrieved_chunks):
                chunk, _ = retrieved_chunks[tag_num - 1]
                citations.append(
                    GroundedCitation(
                        claim=f"Information referenced from context block {tag_num}",
                        doc_tag=f"[Doc {tag_num}]",
                        source_file=chunk.metadata.get("source", "unknown"),
                        verified=True
                    )
                )

        return GroundedResponse(
            query=query,
            answer=answer_text,
            citations=citations,
            has_sufficient_context=not is_insufficient,
            confidence_score=0.98 if not is_insufficient else 0.10
        )

    def _local_grounded_synthesis(
        self,
        query: str,
        retrieved_chunks: List[Tuple[Chunk, float]]
    ) -> GroundedResponse:
        """High-precision local template synthesizer for offline execution."""
        q_lower = query.lower()
        # Check for out-of-domain / irrelevant query using content terms and match ratio
        stopwords = {"what", "is", "the", "for", "a", "an", "in", "to", "of", "and", "how", "do", "does", "by", "all", "are", "on", "what", "with", "if", "college", "campus"}
        content_terms = [t for t in re.findall(r"[A-Za-z0-9_\-]+", q_lower) if t not in stopwords and len(t) > 3]

        # Select best chunk with highest term intersection among top candidates
        best_chunk, best_score = retrieved_chunks[0]
        max_matches = 0
        for chunk, score in retrieved_chunks[:3]:
            matches_count = sum(1 for t in content_terms if t in chunk.text.lower())
            if matches_count > max_matches:
                max_matches = matches_count
                best_chunk = chunk
                best_score = score

        matches = [t for t in content_terms if t in best_chunk.text.lower()]
        match_ratio = (len(matches) / max(1, len(content_terms))) if content_terms else 1.0

        if match_ratio < 0.28:
            return GroundedResponse(
                query=query,
                answer="Insufficient context: The provided enterprise documentation does not contain this information.",
                citations=[],
                has_sufficient_context=False,
                confidence_score=0.0
            )

        citations = [
            GroundedCitation(
                claim=best_chunk.text[:80] + "...",
                doc_tag="[Doc 1]",
                source_file=best_chunk.metadata.get("source", "unknown"),
                verified=True
            )
        ]

        cleaned_text = best_chunk.text.strip().replace("\n\n", " ").replace("\n", " ")
        if len(cleaned_text) > 280:
            cleaned_text = cleaned_text[:280] + "..."

        answer_text = f"{cleaned_text} [Doc 1]"

        return GroundedResponse(
            query=query,
            answer=answer_text,
            citations=citations,
            has_sufficient_context=True,
            confidence_score=0.92
        )
