# MASTER CLOUD SERVICES AGREEMENT & SERVICE LEVEL AGREEMENT (SLA)
**Agreement Reference: MSA-GB-2024-8831**  
**Effective Date: February 15, 2024 | Renewal Term: 3-Year Fixed Enterprise Commitment**  
**By and Between:**  
1. **CloudCorp Technologies Inc.** ("Service Provider"), a Delaware corporation  
2. **GlobalBank N.A.** ("Enterprise Customer"), a national banking association  
**Classification: LEGALLY BINDING ENTERPRISE CONTRACT · EXECUTED EXCLUSIVELY UNDER NEW YORK LAW**

---

## 1. Scope of Enterprise Cloud Services & Telemetry Ingestion
Pursuant to this Master Services Agreement (`MSA-GB-2024-8831`), CloudCorp Technologies provisions dedicated, multi-region enterprise tenant partitions for GlobalBank's mission-critical global payments infrastructure, fraud detection inference pipeline, and real-time streaming telemetry backbone. All workloads operate across geographically isolated Tier-IV datacenter clusters in US-East (Northern Virginia), US-West (Oregon), and EU-Central (Frankfurt).

---

## 2. Platform Availability and 99.99% Multi-Region Uptime Commitment
1. CloudCorp warrants that the Production Cloud Services shall achieve a Monthly Uptime Percentage of not less than **99.99%** (the "Service Level Commitment") during each calendar month of the term.
2. "Monthly Uptime Percentage" is calculated as total minutes in the calendar month minus Downtime minutes, divided by total minutes in the calendar month, multiplied by 100.
3. Downtime excludes scheduled maintenance windows (not to exceed 4 hours per quarter, conducted between 01:00 and 05:00 UTC on Sundays with 14 calendar days advance notice).

---

## 3. Tiered Financial Service Credits for Service Level Failures
If the Monthly Uptime Percentage falls below 99.99% in any calendar month, GlobalBank shall be entitled to receive financial Service Credits credited against the next monthly invoice cycle according to the following schedule:
- **Tier 1 (99.90% to 99.98% Monthly Uptime)**: GlobalBank receives a **10% credit** of total monthly contracted subscription fees.
- **Tier 2 (99.00% to 99.89% Monthly Uptime)**: GlobalBank receives a **25% credit** of total monthly contracted subscription fees (Code: `SLA-CREDIT-TIER-2`).
- **Tier 3 (Below 99.00% Monthly Uptime)**: GlobalBank receives a **50% credit** of total monthly contracted subscription fees, and GlobalBank shall have the contractual right to terminate this Agreement without penalty within 30 calendar days of the outage.

---

## 4. Financial Accounting, Rebate Disbursement, and General Ledger Allocation
In compliance with GAAP and corporate financial governance:
1. All SLA outage credits, liquidated damages, and customer service rebates disbursed to GlobalBank under this Agreement must be officially booked under General Ledger Account `GL-5120` (*Customer SLA Penalties & Rebates*), assigned to Cost Center `CC-105` (*Customer Success & Enterprise Operations*).
2. Service credits must be applied to the invoice within 30 calendar days following the conclusion of the outage investigation and submission of the formal SLA credit request.
3. For Q3 2025, CloudCorp disbursed a Tier-2 SLA service rebate in the amount of **$1,250,000 USD** under `GL-5120` to compensate GlobalBank for a 42-minute multi-region telemetry degradation.

---

## 5. Security Standards, Regulatory Compliance, and SOC-2 Type II Attestation
1. CloudCorp shall maintain continuous compliance with SOC-2 Type II, ISO/IEC 27001, and PCI-DSS Level 1 certifications.
2. CloudCorp shall deliver annually an updated SOC-2 Type II audit report issued by an independent Big Four accounting firm within 30 days of report completion.
3. All GlobalBank data at rest must be encrypted using customer-managed encryption keys (CMEK) via FIPS 140-2 Level 3 certified Hardware Security Modules (HSMs).

---

## 6. Incident Response Time SLAs and Root Cause Analysis (RCA)
- **Severity-1 Critical Incident (Production Down)**:
  - Initial Acknowledgement: **<= 15 minutes** (24/7/365 dedicated enterprise bridge).
  - Status Updates: Provided every 30 minutes to GlobalBank Incident Management command.
  - Comprehensive Root Cause Analysis (RCA): Comprehensive written technical report delivered within **5 business days** of incident resolution.
- **Severity-2 Major Incident (Degraded Operations)**: Initial response <= 1 hour; updates every 2 hours.

---

## 7. Limitation of Liability and Cap on Liquidated Damages
1. Except for liability arising from gross negligence, willful misconduct, or breach of Section 5 (Confidentiality and Data Security), each party's maximum aggregate cumulative liability under this Agreement shall not exceed **$15,000,000 USD** or the total fees paid by GlobalBank in the preceding twelve (12) months, whichever is greater.
2. Under no circumstance shall either party be liable for indirect, incidental, punitive, or consequential damages.
