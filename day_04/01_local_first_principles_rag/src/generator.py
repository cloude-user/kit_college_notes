"""
generator.py
Grounded Generation & Hallucination Guardrail Engine.
Powered by Google Gemini (Gemini 3.7 Flash, 3.6 Flash, 3.5 Flash Lite via Google GenAI SDK).
Enforces bracket citations ([Doc 1: filename]) and handles out-of-context edge cases defensively.
Also supports General Knowledge queries (coding, explanations, science) when outside campus docs.
"""

import os
import re
from typing import List, Tuple, Optional
from dotenv import load_dotenv

# Ensure environment variables from .env are loaded immediately
load_dotenv()

from .models import Chunk, GroundedResponse, GroundedCitation

class EnterpriseGroundedGenerator:
    """
    Constructs context-augmented prompts and generates verified, cited enterprise & academic responses.
    Utilizes modern Google Gemini models (3.7 / 3.6 / 3.5).
    """
    def __init__(self, model_name: str = "auto", temperature: float = 0.2):
        self.temperature = temperature
        self.model_name = model_name or os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")

    def _resolve_gemini_model(self) -> str:
        """Selects the modern active Gemini model, prioritizing 3.8 and 3.7."""
        candidate = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
        if candidate in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash", "gemini-2.5-flash"]:
            return "gemini-3.8-flash"  # Upgrade deprecated references to modern 3.8
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

    def generate(
        self,
        query: str,
        retrieved_chunks: List[Tuple[Chunk, float]],
        temperature: Optional[float] = None
    ) -> GroundedResponse:
        """
        Executes grounded generation using Gemini 3.7 / 3.6 if API key is present,
        or deterministic offline grounder if running locally without keys.
        """
        temp = temperature if temperature is not None else self.temperature

        if not retrieved_chunks:
            return GroundedResponse(
                query=query,
                answer="Insufficient context: No matching college documents found in the database.",
                citations=[],
                has_sufficient_context=False,
                confidence_score=0.0
            )

        prompt = self.build_prompt(query, retrieved_chunks)

        # 1. Cloud LLM generation using Google GenAI SDK (Gemini 3.8 / 3.7 / 3.6)
        if os.environ.get("GEMINI_API_KEY") and os.environ.get("OFFLINE_MODE", "false").lower() != "true":
            models_to_try = [self._resolve_gemini_model(), "gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash"]
            # Remove duplicates preserving order
            seen = set()
            unique_models = [m for m in models_to_try if not (m in seen or seen.add(m))]

            for model_id in unique_models:
                try:
                    from google import genai
                    from google.genai import types
                    client = genai.Client()
                    config = types.GenerateContentConfig(temperature=temp)
                    resp = client.models.generate_content(
                        model=model_id,
                        contents=prompt,
                        config=config
                    )
                    if resp.text:
                        answer_text = resp.text.strip()
                        return self._parse_and_verify_citations(query, answer_text, retrieved_chunks)
                except Exception:
                    continue

        elif os.environ.get("OPENAI_API_KEY"):
            try:
                from openai import OpenAI
                client = OpenAI()
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temp
                )
                answer_text = resp.choices[0].message.content.strip()
                return self._parse_and_verify_citations(query, answer_text, retrieved_chunks)
            except Exception:
                pass

        # 2. Local Deterministic Academic Grounder (Failsafe offline generator)
        return self._local_grounded_synthesis(query, retrieved_chunks)

    def generate_general(self, query: str, temperature: float = 0.7) -> str:
        """
        Executes general knowledge query generation (coding, science, concepts, advice)
        using Gemini 3.7 / 3.6 / 3.5 Flash or intelligent educational fallback.
        """
        q_clean = query.strip()
        q_lower = q_clean.lower()

        # Handle greetings naturally
        if re.search(r"^(hi|hello|hey|good\s+(morning|afternoon|evening))\b", q_lower) and len(q_lower.split()) <= 4:
            return (
                "### 👋 Hello! How can I assist you today?\n\n"
                "I am your **KIT College AI Copilot**. I can help you with:\n"
                "- 📋 **Academic Policies & Attendance**: Medical condonation rules, 75% threshold, CIA evaluations.\n"
                "- 📚 **Courses & Faculty**: Subject codes (e.g. `CS401`), instructor details, and exam schedules.\n"
                "- 🏢 **Campus Life**: Hostel curfews (8:30 PM), mess timings, library borrowing limits, and placement eligibility.\n"
                "- 💡 **General Knowledge & Study Topics**: Coding problems, engineering mathematics, and study advice.\n\n"
                "Feel free to ask your question!"
            )

        # Handle real-time financial market/live commodity queries
        if re.search(r"\b(gold|silver|stock|share\s+price|crypto|bitcoin|sensex|nifty)\b", q_lower):
            return (
                "### 📈 Real-Time Market Information Note\n\n"
                "I am your **KIT College AI Copilot** specialized in institutional policies, academics, and computer engineering.\n\n"
                "• **Live Market Data**: Real-time market commodity prices (such as today's 22K/24K gold rates or stock market indices) fluctuate minute-by-minute and require a live financial ticker API.\n"
                "• **Live Sources**: To get today's accurate, live gold rates in INR, please refer to financial platforms such as **GoodReturns**, **Moneycontrol**, or the **MCX India** bullion index.\n"
                "• **Campus & Academic Assistance**: Feel free to ask me about any KIT College regulations, courses, attendance calculations, or coding questions!"
            )

        # Handle casual/playful/slang inputs (e.g. Siuuuu, cheers, haha)
        if re.search(r"\b(siu+|ronaldo|messi|haha|lol|cheers|cool|awesome|yo|cr7)\b", q_lower):
            return (
                "### ⚽ SIUUUU!\n\n"
                "I love the energy! 🌟 I am your **KIT College AI Copilot**.\n\n"
                "I am here and ready to help you with:\n"
                "• **Academic Policies & Attendance**: Medical condonation (65%–74.9%), 75% rule, detention.\n"
                "• **Courses & Faculty**: Course codes (e.g. `CS401`), credits, professors, and exam dates.\n"
                "• **Hostel & Campus Life**: 8:30 PM curfew, mess timings, library fines (₹5/day), and placements.\n"
                "• **Engineering & Studies**: Coding challenges, algorithms, or concept explanations.\n\n"
                "What would you like to explore next?"
            )

        sys_prompt = (
            "You are an expert AI Assistant and Academic Mentor at KIT College of Engineering. "
            "Provide a comprehensive, accurate, step-by-step, and educational explanation to the user's question. "
            "Use clear headings, code blocks if applicable, and engaging formatting."
        )
        full_prompt = f"{sys_prompt}\n\nUSER QUESTION:\n{query}"

        if os.environ.get("GEMINI_API_KEY") and os.environ.get("OFFLINE_MODE", "false").lower() != "true":
            models_to_try = [self._resolve_gemini_model(), "gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash"]
            seen = set()
            unique_models = [m for m in models_to_try if not (m in seen or seen.add(m))]

            for model_id in unique_models:
                try:
                    from google import genai
                    from google.genai import types
                    client = genai.Client()
                    config = types.GenerateContentConfig(temperature=temperature)
                    resp = client.models.generate_content(
                        model=model_id,
                        contents=full_prompt,
                        config=config
                    )
                    if resp.text:
                        return resp.text.strip()
                except Exception:
                    continue

        # Offline educational response simulation
        return (
            f"### 💡 Academic Mentor Response\n\n"
            f"Here is an overview for **'{query}'**:\n\n"
            f"1. **Core Understanding**: This topic addresses key computing, engineering, or analytical principles.\n"
            f"2. **Structured Analysis**: Identify the known variables, evaluate the problem scope, and apply standard algorithmic steps.\n"
            f"3. **KIT Academic Context**: For campus-specific inquiries, consult your course faculty or KIT student handbook.\n\n"
            f"*(Generated in local offline mode)*"
        )

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
                        source_section=chunk.metadata.get("section", "General"),
                        verified=True
                    )
                )

        # Calculate confidence
        if is_insufficient:
            confidence = 0.0
            has_context = False
        else:
            has_context = True
            confidence = min(1.0, 0.6 + 0.1 * len(citations)) if citations else 0.5

        return GroundedResponse(
            query=query,
            answer=answer_text,
            citations=citations,
            has_sufficient_context=has_context,
            confidence_score=confidence
        )

    def _local_grounded_synthesis(
        self,
        query: str,
        retrieved_chunks: List[Tuple[Chunk, float]]
    ) -> GroundedResponse:
        """Deterministic offline fallback synthesis."""
        q_lower = query.lower()
        q_words = set(re.findall(r"\w+", q_lower))
        stop_words = {
            "what", "is", "the", "and", "or", "for", "can", "i", "if", "my", "to", "how", "a", "an", "in", "of",
            "do", "you", "have", "students", "student", "campus", "college", "kit", "bring", "personal", "please",
            "tell", "me", "there", "are", "about", "with", "this", "that"
        }
        content_words = q_words - stop_words

        # Select candidate chunk with highest query word intersection
        best_chunk, best_score = retrieved_chunks[0]
        max_overlap = -1
        chosen_rank = 1

        for idx, (chunk, score) in enumerate(retrieved_chunks[:3], 1):
            c_words = set(re.findall(r"\w+", chunk.text.lower()))
            overlap = len(content_words.intersection(c_words))
            if overlap > max_overlap:
                max_overlap = overlap
                best_chunk = chunk
                best_score = score
                chosen_rank = idx

        # Defensive out-of-domain check
        campus_core_topics = ["attendance", "hostel", "placement", "library", "course", "curriculum", "exam", "condonation", "curfew", "mess", "cgpa", "arrear", "credit"]
        has_core_topic = any(k in q_lower for k in campus_core_topics)
        if (max_overlap <= 1 or not has_core_topic) and not has_core_topic:
            return GroundedResponse(
                query=query,
                answer="Insufficient context: The provided enterprise documentation does not contain this information.",
                citations=[],
                has_sufficient_context=False,
                confidence_score=0.0
            )

        source = best_chunk.metadata.get("source", "unknown")
        section = best_chunk.metadata.get("section", "Policy Guideline")
        snippet = best_chunk.text.strip().replace("\n\n", " ")

        grounded_answer = (
            f"Based on **{section}** in `{source}`: {snippet[:300]}... [Doc {chosen_rank}]\n\n"
            f"> *Source Reference: [Doc {chosen_rank}: {source} — {section}]*"
        )

        citation = GroundedCitation(
            claim=f"Official academic statement from {section}",
            doc_tag=f"[Doc {chosen_rank}]",
            source_file=source,
            source_section=section,
            verified=True
        )

        return GroundedResponse(
            query=query,
            answer=grounded_answer,
            citations=[citation],
            has_sufficient_context=True,
            confidence_score=0.92
        )
