# CloudCorp Global Compliance, Security & Procurement Policy Manual
**Document ID: POL-FIN-SEC-2025-V2**  
**Effective Date: January 1, 2025 | Revision: 4.2**  
**Applies To: All Global Subsidiaries, Employees, Contractors & Cloud Workspaces**  
**Classification: INTERNAL BUSINESS CONFIDENTIAL · SOX & SOC-2 COMPLIANCE MANDATE**

---

## 1. Vendor Procurement & Capital Expenditure Authorization Thresholds
Procurement of software licenses, AI cloud computing infrastructure (Nvidia GPU clusters, InfiniBand switches), and third-party SaaS applications is strictly governed by enterprise dollar authorization levels:
- **Level 1 (Under $25,000 USD)**: Requires sole approval of Department Direct Manager. Purchase orders can be auto-approved via the Workday ERP procurement workflow.
- **Level 2 ($25,000 to $100,000 USD)**: Requires Vice President (VP) approval and Financial Controller sign-off. At least two competitive vendor price benchmarks must be documented in the procurement request.
- **Level 3 ($100,000 to $500,000 USD)**: Requires Chief Financial Officer (CFO) and Chief Information Security Officer (CISO) dual authorization, accompanied by a formal cybersecurity vendor risk assessment (SOC-2 Type II audit report).
- **Level 4 (Exceeding $500,000 USD)**: Requires formal Board of Directors Audit Committee approval and competitive bidding with at least three independent vendor proposals (RFP process) submitted to the Global Strategic Sourcing committee.

---

## 2. API Key Governance, Cryptographic Secrets, and IAM Security
All cryptographic tokens, cloud API keys (OpenAI, Google Gemini, Anthropic Claude, AWS IAM credentials), and database connection strings must comply with the following standards:
1. Under no circumstance may production credentials, private SSH keys, or API tokens be committed to git repositories, test scripts, or environment variables in client-side bundles. Any detected secret leak triggers an automated Severity-1 Security Incident, immediate token revocation within 15 minutes, and mandatory security audit disclosure.
2. All production API keys and asymmetric certificates must be stored in HashiCorp Vault or AWS Secrets Manager protected by FIPS 140-2 Level 3 Hardware Security Modules (HSMs).
3. API credentials must be rotated on a mandatory **90-calendar-day cycle**. Keys unrotated after 95 days are automatically revoked by IAM policy enforcement scripts. Temporary extension waivers require written approval from the CISO and cannot exceed 14 calendar days.

---

## 3. Sarbanes-Oxley (SOX) Section 404 Financial Reporting & Audit Integrity
To ensure strict adherence to SOX Section 404 requirements regarding internal controls over financial reporting:
1. All ledger entries, journal adjustments, and revenue recognition schedules exceeding **$50,000 USD** must include supporting vendor invoices, purchase orders, and dual-signoff from the Senior Director of Accounting and the Financial Controller.
2. Segregation of Duties (SoD) is strictly enforced: engineers or managers who initiate purchase requisitions are prohibited from approving invoice disbursements or posting journal entries in NetSuite ERP.
3. Financial audit logs and ERP transactional journals are write-once-read-many (WORM) compliant and preserved for a mandatory minimum retention period of **7 years**. Automated deletion guards block any administrative truncation of ledger history.

---

## 4. Hardware Replacement, Logistics, and RMA Service Level Agreements
If enterprise infrastructure hardware components (servers, top-of-rack switches, NVMe storage bays, GPU accelerators) arrive damaged or experience hardware failure upon delivery:
1. Defect notifications must be logged in the logistics ERP portal within **14 calendar days** of physical receipt at any CloudCorp data center facility.
2. Verified defect claims receive an expedited replacement unit dispatched via overnight freight with zero surcharge to the originating department.
3. Damaged units must be securely boxed and returned using the provided prepaid return merchandise authorization (RMA) shipping label within **30 calendar days** of replacement delivery.
4. Serialized chain-of-custody tracking must be maintained in the CMDB (Configuration Management Database) to ensure hardware asset reconciliation under ISO 27001 Annex A.8.

---

## 5. Data Privacy, GDPR Article 33 Breach Notification, and SOC-2 Retention
CloudCorp adheres to the highest international data privacy and security frameworks, including EU GDPR, California CCPA, and SOC-2 Type II:
1. **Breach Notification SLA**: In the event of confirmed unauthorized access to customer data or personally identifiable information (PII), the Security Incident Response Team (SIRT) must notify relevant regulatory supervisory authorities within **72 hours** of becoming aware of the breach, pursuant to GDPR Article 33.
2. **Customer Tenant Data Purge**: In the event of customer contract termination, tenant data export archives must be completed within 30 calendar days. After 30 days, encrypted tenant partitions are cryptographically sanitized in compliance with NIST SP 800-88 Rev 1 (Purge standard), and all customer encryption keys are permanently destroyed.

---

## 6. Incident Classification, Severity Levels, and Escalation Matrix
- **Severity-1 (Critical Outage)**: Total platform unavailability, data loss, or active credential compromise. Initial executive incident response time: **<= 15 minutes**. Status page updates required every 30 minutes until resolution.
- **Severity-2 (Major Degradation)**: Core functionality impaired with degraded performance (e.g., telemetry latency > 200ms). Initial response: **<= 1 hour**.
- **Severity-3 (Minor Defect)**: Non-critical feature anomaly with administrative workaround available. Initial response: **<= 8 business hours**.
