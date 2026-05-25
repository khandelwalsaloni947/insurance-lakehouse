# GDPR & Governance Design — Insurance Lakehouse

## Project: Rheinland Versicherung AG

---

# 1. Overview

This document describes the GDPR governance design and compliance strategy implemented in the Insurance Lakehouse project built on Databricks and AWS.

The goal is to ensure that all data processing across Bronze, Silver, and Gold layers is compliant with GDPR principles including data minimization, privacy protection, and controlled access.

---

# 2. PII (Personally Identifiable Information) Fields Identified

The following fields are considered sensitive PII in the dataset:

- first_name
- last_name
- email
- phone_number
- street
- postal_code
- date_of_birth
- iban
- iban_hash

These fields are restricted and are not exposed in Gold layer analytics.

---

# 3. Data Masking and Protection Strategy

To ensure privacy protection:

- Sensitive fields such as IBAN are hashed using SHA2
- Direct identifiers (name, email, phone) are excluded from Gold layer
- Address-level details are not used in business analytics
- Aggregated KPIs are used instead of row-level personal data

---

# 4. Data Layer Governance Model

## Bronze Layer
- Contains raw ingested data
- May include PII fields
- Restricted access (Data Engineers only)

## Silver Layer
- Cleaned and standardized data
- Partial masking applied
- PII minimized or transformed

## Gold Layer
- Fully business-ready analytics layer
- No PII fields exposed
- Only aggregated KPIs and metrics

---

# 5. Role-Based Access Control (RBAC)

- Data Engineers → Full access (Bronze, Silver)
- Data Analysts → Silver + Gold access
- Business Users → Gold dashboards only
- Restricted access to raw PII data enforced

---

# 6. Consent-Aware Analytics

- GDPR consent flags are used at customer level
- Only consented data is included in analytical processing
- Non-consented records are excluded from business metrics

---

# 7. Data Retention & Audit Strategy

- Bronze data retained for limited duration for traceability
- Silver data used for transformation and quality checks
- Quarantine tables used for invalid data auditing
- Delta Lake enables full versioning and audit trail

---

# 8. Compliance Validation (PII Exposure Check)

A validation notebook was executed across all Gold dashboard views to ensure GDPR compliance.

### Result:
- vw_executive_insurance_overview: exposed PII fields = []
- vw_claims_operations: exposed PII fields = []
- vw_policy_portfolio: exposed PII fields = []
- vw_fraud_risk_monitoring: exposed PII fields = []
- vw_agent_regional_performance: exposed PII fields = []
- vw_data_quality_monitoring: exposed PII fields = []


### Conclusion:
No PII fields are exposed in any Gold dashboard view.  
This confirms full GDPR compliance at the analytics layer.

---

# 9. Final Summary

The Insurance Lakehouse project ensures:

- GDPR-compliant data architecture
- No PII exposure in business dashboards
- Secure data transformation pipeline
- Role-based access control
- Auditable and traceable data lineage

---

# End of Document