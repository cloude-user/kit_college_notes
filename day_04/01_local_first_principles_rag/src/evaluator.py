"""
evaluator.py
Production RAGAS-Grade Evaluation Suite and Automated CI/CD Quality Gates.
Calculates Faithfulness, Answer Relevancy, Context Precision, and Context Recall.
"""

import re
from typing import List
from .models import RAGASMetrics

class EnterpriseRAGASEvaluator:
    """
    Automated evaluation harness for RAG pipelines.
    Enforces quality thresholds to prevent model hallucinations from entering production.
    """
    def __init__(
        self,
        min_faithfulness: float = 0.85,
        min_relevancy: float = 0.80,
        min_precision: float = 0.75,
        min_recall: float = 0.75
    ):
        self.min_faithfulness = min_faithfulness
        self.min_relevancy = min_relevancy
        self.min_precision = min_precision
        self.min_recall = min_recall

    def evaluate_sample(
        self,
        question: str,
        answer: str,
        contexts: List[str],
        ground_truth: str
    ) -> RAGASMetrics:
        """
        Evaluates a single RAG inference sample across the RAG triad metrics.
        """
        combined_context = " ".join(contexts).lower()
        ans_lower = answer.lower()
        gt_lower = ground_truth.lower()

        # ----------------------------------------------------------------------
        # 1. FAITHFULNESS (Hallucination Detection)
        # Extracts key assertions and tests if context supports them
        # ----------------------------------------------------------------------
        # Extract meaningful tokens (numbers, uppercase codes, keywords)
        facts = re.findall(r"\b(?:\$?\d+(?:\.\d+)?%?|[A-Za-z0-9_-]{5,})\b", answer)
        if not facts:
            faithfulness_score = 1.0
        else:
            supported = sum(1 for f in facts if f.lower() in combined_context)
            faithfulness_score = supported / len(facts)

        # ----------------------------------------------------------------------
        # 2. ANSWER RELEVANCY (On-Topic vs Wandering)
        # Uses morphological prefix stemming to measure semantic topical alignment
        # ----------------------------------------------------------------------
        stopwords = {"what", "is", "the", "for", "a", "an", "in", "to", "of", "and", "how", "do", "does", "by", "all", "are", "on", "what", "with", "if"}
        q_tokens = [w for w in re.findall(r"\w+", question.lower()) if w not in stopwords and len(w) > 2]
        a_tokens = [w for w in re.findall(r"\w+", ans_lower) if w not in stopwords and len(w) > 2]
        if not q_tokens:
            relevancy_score = 1.0
        else:
            q_stems = {w[:4] for w in q_tokens}
            a_stems = {w[:4] for w in a_tokens}
            common = len(q_stems.intersection(a_stems))
            relevancy_score = min(1.0, (common / len(q_stems)) * 1.25)

        # ----------------------------------------------------------------------
        # 3. CONTEXT PRECISION (Signal-to-Noise at Top Ranks)
        # ----------------------------------------------------------------------
        gt_tokens = set(re.findall(r"\w+", gt_lower))
        relevant_flags = []
        for ctx in contexts:
            c_toks = set(re.findall(r"\w+", ctx.lower()))
            overlap = len(gt_tokens.intersection(c_toks))
            relevant_flags.append(1 if overlap >= 2 else 0)

        if not relevant_flags or sum(relevant_flags) == 0:
            precision_score = 0.5
        else:
            # Average precision @ K
            running_sum = 0.0
            hits = 0
            for rank, is_rel in enumerate(relevant_flags, 1):
                if is_rel:
                    hits += 1
                    running_sum += (hits / rank)
            precision_score = running_sum / hits

        # ----------------------------------------------------------------------
        # 4. CONTEXT RECALL (Completeness of Retrieval)
        # ----------------------------------------------------------------------
        gt_facts = re.findall(r"\b(?:\$?\d+(?:\.\d+)?%?|[A-Za-z0-9_-]{5,})\b", ground_truth)
        if not gt_facts:
            recall_score = 1.0
        else:
            found = sum(1 for f in gt_facts if f.lower() in combined_context)
            recall_score = found / len(gt_facts)

        # ----------------------------------------------------------------------
        # 5. CI/CD QUALITY GATE VERIFICATION
        # ----------------------------------------------------------------------
        passed = (
            faithfulness_score >= self.min_faithfulness and
            relevancy_score >= self.min_relevancy and
            precision_score >= self.min_precision and
            recall_score >= self.min_recall
        )

        diag = "All quality gates satisfied." if passed else "Build failed quality gate thresholds."

        return RAGASMetrics(
            faithfulness=round(faithfulness_score, 3),
            answer_relevancy=round(relevancy_score, 3),
            context_precision=round(precision_score, 3),
            context_recall=round(recall_score, 3),
            passed_quality_gate=passed,
            diagnostic_message=diag
        )
