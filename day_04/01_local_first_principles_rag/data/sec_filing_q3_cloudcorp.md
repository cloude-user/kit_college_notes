# UNITED STATES SECURITIES AND EXCHANGE COMMISSION
**Washington, D.C. 20549**
## FORM 10-Q · QUARTERLY REPORT PURSUANT TO SECTION 13 OR 15(d) OF THE SECURITIES EXCHANGE ACT OF 1934

**For the quarterly period ended September 30, 2025**  
**Commission File Number: 001-39482**  
**Exact Name of Registrant as Specified in Its Charter: CloudCorp Technologies Inc.**  
**State of Incorporation: Delaware | IRS Employer Identification No.: 84-2938104**  
**Principal Executive Offices: 100 Enterprise Parkway, Suite 500, San Jose, California 95134**

---

## PART I — FINANCIAL INFORMATION

### Item 1. Financial Statements & Revenue Recognition (GAAP ASC-606)

#### Note 1. Description of Business and Basis of Presentation
CloudCorp Technologies Inc. ("CloudCorp", "the Company", "we", or "our") delivers an enterprise multi-tenant cloud data platform, artificial intelligence inference engine, and distributed telemetry streaming architecture. The accompanying unaudited condensed consolidated financial statements have been prepared in accordance with accounting principles generally accepted in the United States of America ("U.S. GAAP") for interim financial information and pursuant to the rules and regulations of the Securities and Exchange Commission ("SEC").

#### Note 2. Revenue Recognition Under GAAP ASC-606
The Company recognizes revenue under Accounting Standards Codification Topic 606 (*Revenue from Contracts with Customers*). Revenue is recognized upon transfer of control of promised products or services to customers in an amount that reflects the consideration the Company expects to receive.

1. **Enterprise Cloud Subscriptions (85.4% of Total Revenue)**: Cloud subscription licenses provide customers with continuous access to the hosted CloudCorp telemetry and AI inference platform. Under GAAP ASC-606, subscription revenue is recognized ratably over the contractual subscription term beginning when access to the cloud platform is provisioned. For multi-year agreements, invoices are typically issued annually in advance, with unearned amounts recorded as deferred revenue.
2. **Professional Deployment & Architectural Services (14.6% of Total Revenue)**: Professional services revenue is recognized over time as the services are rendered, measured by the input method based on labor hours incurred relative to total estimated project hours.
3. **Consumption-Based Capacity and Overages**: Enterprise telemetry data ingestion in excess of contracted baselines is billed monthly in arrears and recognized in the period in which consumption occurs.

For the three months ended September 30, 2025 (Q3 2025), total consolidated revenue was **$482.4 million**, an increase of 21.6% compared to $396.7 million for the three months ended September 30, 2024. Cloud Subscription Revenue accounted for **$412.1 million** (85.4% of total revenue), driven by an annual net dollar expansion rate of 124%. Professional deployment services generated **$70.3 million**, compared to $68.2 million in the prior year period. Gross margin for subscription services was 78.4%, while professional services delivered a gross margin of 22.1%.

#### Note 3. Remaining Performance Obligations (RPO)
As of September 30, 2025, the aggregate transaction price allocated to remaining performance obligations ("RPO")—representing contracted future revenue not yet recognized—was **$1.84 billion**, compared to $1.42 billion as of September 30, 2024. The Company expects to recognize approximately 62% of this RPO as revenue over the next 12 months, with the remaining balance recognized thereafter.

---

### Item 2. Management's Discussion and Analysis (MD&A) of Financial Condition

#### Operating Expenses & AI Infrastructure Capital Commitments
Operating expenditures for the three months ended September 30, 2025 were categorized as follows:
- **Research & Development (R&D)**: $148.6 million (30.8% of revenue), compared to $118.2 million in Q3 2024. This growth was primarily driven by non-cancellable cloud compute cluster lease commitments for 16,384 Nvidia H100/H200 SXM5 accelerators dedicated to pre-training and real-time retrieval-augmented generation (RAG) models.
- **Sales & Marketing (S&M)**: $132.1 million (27.4% of revenue), down from 34.2% of revenue in Q3 2024, demonstrating operating sales leverage across global financial enterprise accounts.
- **General & Administrative (G&A)**: $42.5 million (8.8% of revenue), including legal accruals, corporate insurance, and Sarbanes-Oxley (SOX) Section 404 audit compliance fees.

Operating income for Q3 2025 reached **$89.2 million** (representing an 18.5% operating margin), compared to $44.8 million (11.3% operating margin) for the three months ended September 30, 2024.

---

### Item 3. Risk Factors & Technical Incident Contingencies

#### Technical Failure Modes and Error Code Disclosures
Our multi-tenant distributed streaming backbone is subject to edge-case runtime conditions across high-throughput telemetry pipelines:
1. **Telemetry Ingestion Buffer Overflow (`ERR_STREAM_BUFFER_OVERFLOW_504`)**: When downstream streaming clusters experience packet fragmentation and regional network latency spikes exceeding 120ms, telemetry nodes register error code `ERR_STREAM_BUFFER_OVERFLOW_504`. Under active failover protocols, telemetry nodes automatically fail over to secondary Amazon S3 cold tiers within 180 seconds, ensuring zero loss of durable customer logs.
2. **Cryptographic Key Management Timeout (`ERR_CRYPTO_HSM_TIMEOUT_509`)**: During cross-region key synchronization across Hardware Security Modules (HSMs), failure to receive an acknowledgment within 1,500ms raises error code `ERR_CRYPTO_HSM_TIMEOUT_509`. Nodes retry with exponential backoff up to 3 times before routing encryption requests to the secondary regional KMS vault.
3. **Tenant Egress Rate Throttling (`ERR_EGRESS_BANDWIDTH_THROTTLE_429`)**: When enterprise tenants exceed their provisioned burst bandwidth limit of 100 Gbps, API gateway routers return HTTP status code 429 with error subcode `ERR_EGRESS_BANDWIDTH_THROTTLE_429`, queuing downstream packets for up to 60 seconds.

#### Customer Contract Termination, Data Portability, and SOC-2 Standards
In the event of enterprise customer contract termination or non-renewal:
- Customer data export archives must be completed and delivered via secure SFTP or signed object storage URLs within **30 calendar days** of formal termination notice.
- After 30 days, encrypted tenant partitions are cryptographically purged in compliance with SOC-2 Type II standards and NIST SP 800-88 Rev 1 guidelines. All cryptographic decryption keys associated with the tenant workspace are permanently destroyed from production HSM vaults within 14 calendar days following the 30-day export window.

---

### Item 4. Controls and Procedures & Internal Audit

#### Evaluation of Disclosure Controls and Procedures (SOX Section 302 and 404)
Our management, under the supervision and with the participation of our Chief Executive Officer (CEO) and Chief Financial Officer (CFO), evaluated the effectiveness of our disclosure controls and procedures (as defined in Rules 13a-15(e) and 15d-15(e) under the Exchange Act) as of September 30, 2025. Based on this evaluation, our CEO and CFO concluded that our disclosure controls and procedures were effective at the reasonable assurance level. No material weakness was identified during the interim period.

---

## PART II — OTHER INFORMATION

### Item 1. Legal Proceedings & Customer SLA Disputes
From time to time, the Company is involved in commercial disagreements arising in the ordinary course of business. During Q3 2025, CloudCorp recorded a service rebate settlement under General Ledger Account `GL-5120` (Customer SLA Penalties & Rebates) in the amount of **$1,250,000** in favor of GlobalBank N.A. pursuant to Master Services Agreement `MSA-GB-2024-8831` following a 42-minute multi-region telemetry degradation. The Company believes this settlement fully resolves the incident and incurs no further liability.
