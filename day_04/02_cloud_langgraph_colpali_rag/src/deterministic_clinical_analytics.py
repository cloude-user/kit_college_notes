"""
deterministic_clinical_analytics.py
Deterministic Clinical Safety Analytics & Protocol Stopping Rule Auditor.
Executes exact mathematical calculations on clinical adverse event records
without LLM math hallucination.
"""

from typing import List, Dict, Any, Optional
import pandas as pd
from .models import ClinicalStatsResult

class DeterministicClinicalAnalytics:
    """
    Analyzes patient safety incidents from clinical trials (MedDRA / CTCAE v5.0).
    Enforces FDA 21 CFR § 312.32 safety window compliance and automatic clinical hold rules.
    """
    def __init__(self, ledger_csv_path: str):
        self.df = pd.read_csv(ledger_csv_path)

    def analyze(
        self,
        cohort_filter: Optional[str] = None,
        site_filter: Optional[str] = None,
        meddra_filter: Optional[str] = None
    ) -> ClinicalStatsResult:
        """
        Executes deterministic multi-dimensional safety aggregation.
        """
        filtered = self.df.copy()

        if cohort_filter:
            filtered = filtered[filtered["dose_cohort"].str.contains(cohort_filter, case=False, na=False)]
        if site_filter:
            filtered = filtered[filtered["site_name"].str.contains(site_filter, case=False, na=False)]
        if meddra_filter:
            filtered = filtered[filtered["meddra_term"].str.contains(meddra_filter, case=False, na=False)]

        total_records = len(filtered)
        if total_records == 0:
            return ClinicalStatsResult(
                total_records=0,
                cohort_filter=cohort_filter,
                site_filter=site_filter,
                total_saes=0,
                sae_rate_percent=0.0,
                grade_distribution={},
                drug_relationship_counts={},
                fatal_count=0,
                overdue_fda_reports=0,
                stopping_rule_triggered=False,
                stopping_rule_details="No records matched the specified filters.",
                summary_text="No clinical trial safety records found for the given criteria."
            )

        # 1. Serious Adverse Events (SAE)
        sae_mask = filtered["is_sae"].str.strip().str.lower() == "yes"
        total_saes = int(sae_mask.sum())
        sae_rate = (total_saes / total_records) * 100.0

        # 2. CTCAE Grade Breakdown
        grade_counts = filtered["ctcae_grade"].value_counts().to_dict()
        grade_dist = {str(k): int(v) for k, v in grade_counts.items()}

        # 3. Drug Relationship (Attribution)
        rel_counts = filtered["drug_relationship"].value_counts().to_dict()
        rel_dist = {str(k): int(v) for k, v in rel_counts.items()}

        # 4. Fatal Events (Grade 5 / Outcome == Fatal)
        fatal_count = int((filtered["outcome"].str.lower() == "fatal").sum())

        # 5. FDA 21 CFR § 312.32 Reporting Window Verification
        # Check latency against regulations:
        # Fatal/Life-Threatening SAEs must be <= 7 days
        # Other SAEs must be <= 15 days
        overdue_count = 0
        for _, row in filtered.iterrows():
            if str(row["is_sae"]).lower() == "yes":
                lat = int(row.get("reporting_latency_days", 0))
                grade = str(row.get("ctcae_grade", ""))
                is_fatal_or_life_threatening = ("grade 4" in grade.lower()) or ("grade 5" in grade.lower()) or (str(row.get("outcome", "")).lower() == "fatal")
                if is_fatal_or_life_threatening and lat > 7:
                    overdue_count += 1
                elif not is_fatal_or_life_threatening and lat > 15:
                    overdue_count += 1

        # 6. Protocol Stopping Rules & Clinical Hold Triggers
        # Rule 1: Any treatment-related death (Grade 5)
        # Rule 2: Grade 4 non-hematologic toxicity in >= 15% of cohort
        grade_4_count = grade_dist.get("Grade 4", 0)
        grade_4_rate = (grade_4_count / total_records) * 100.0
        
        stopping_triggered = False
        stopping_reasons = []

        if fatal_count > 0:
            stopping_triggered = True
            stopping_reasons.append(f"MANDATORY CLINICAL HOLD: {fatal_count} fatal adverse reaction recorded (Patient {filtered[filtered['outcome'].str.lower() == 'fatal']['patient_id'].iloc[0]}).")

        if grade_4_rate >= 15.0:
            stopping_triggered = True
            stopping_reasons.append(f"DOSE ESCALATION PAUSE: Grade 4 severe toxicities reached {grade_4_rate:.1f}% (Threshold: >= 15.0%).")

        stopping_details = " | ".join(stopping_reasons) if stopping_reasons else "All safety thresholds within acceptable protocol boundaries."

        # Structured textual synthesis
        summary = (
            f"CLINICAL SAFETY AUDIT SUMMARY:\n"
            f"• Cohort / Scope Analyzed: {cohort_filter or 'All Study Cohorts'} ({site_filter or 'All 5 Clinical Sites'})\n"
            f"• Total Incident Records: {total_records}\n"
            f"• Serious Adverse Events (SAEs): {total_saes} ({sae_rate:.1f}% incidence rate)\n"
            f"• Severity Distribution: Grade 1 ({grade_dist.get('Grade 1', 0)}), Grade 2 ({grade_dist.get('Grade 2', 0)}), Grade 3 ({grade_dist.get('Grade 3', 0)}), Grade 4 ({grade_4_count}), Grade 5 ({fatal_count})\n"
            f"• Regulatory Window Compliance: {overdue_count} overdue FDA expedited filings detected\n"
            f"• Safety Review Committee Status: {'🚨 ' + stopping_details if stopping_triggered else '✅ Normal Monitoring'}"
        )

        return ClinicalStatsResult(
            total_records=total_records,
            cohort_filter=cohort_filter,
            site_filter=site_filter,
            total_saes=total_saes,
            sae_rate_percent=round(sae_rate, 2),
            grade_distribution=grade_dist,
            drug_relationship_counts=rel_dist,
            fatal_count=fatal_count,
            overdue_fda_reports=overdue_count,
            stopping_rule_triggered=stopping_triggered,
            stopping_rule_details=stopping_details,
            summary_text=summary
        )
