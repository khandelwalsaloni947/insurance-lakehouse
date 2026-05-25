# Demo Script

## Purpose

This demo script is designed to present the German Insurance Lakehouse project in a clear, professional, and business-focused way.

The goal is to:
- explain the complete lakehouse architecture
- demonstrate Bronze, Silver, and Gold layers
- show governance and GDPR compliance
- present dashboard-ready analytics
- demonstrate AI-ready fraud feature engineering
- present the project confidently during interviews, reviews, or classroom presentations

This script avoids random notebook scrolling and provides a structured storytelling flow.

---

## Estimated Demo Length

- Short Demo Version: 5–7 minutes
- Full Technical Demo Version: 10–15 minutes

---

# Step 1 — Open README and Explain Project Purpose

Open README.md

Explain:

This project simulates a modern insurance lakehouse for a fictional German insurance company called Rheinland Versicherung AG. The goal was to build a complete cloud-based analytics platform using Databricks and AWS.

The platform supports:
- insurance KPI analytics
- fraud-risk monitoring
- GDPR-aware governance
- AI-ready feature engineering

“This project demonstrates an end-to-end Medallion Lakehouse architecture using Bronze, Silver, Quarantine, and Gold layers.”

---

# Step 2 — Show Architecture Diagram

Open architecture.md or README architecture section

Explain architecture flow:

Raw → Bronze → Silver → Quarantine → Gold

Explain each layer:

Raw:
Synthetic insurance data stored in AWS S3

Bronze:
Raw ingestion into Delta tables, data preserved exactly as received

Silver:
Cleaned and validated trusted data with GDPR-aware transformations

Quarantine:
Invalid or suspicious records isolated for audit

Gold:
Business-ready analytics and AI-ready feature tables

“Bronze proves what arrived, Silver proves what can be trusted, and Gold proves what the business can use.”

---

# Step 3 — Show Catalog Explorer (Bronze, Silver, Gold)

Open Databricks Catalog Explorer and show schemas:

Bronze tables:
- bronze_customers
- bronze_claims
- bronze_policies  
Purpose: raw ingestion layer

Silver tables:
- silver_claims
- silver_policies
- silver_customers  
Purpose: cleaned trusted data layer

Quarantine tables:
- quarantine_invalid_claims
- quarantine_invalid_payments  
Purpose: invalid data isolation

Gold tables:
- gold_claims_overview
- gold_policy_performance
- gold_claim_fraud_features  
Purpose: business analytics and AI-ready reporting

---

# Step 4 — Run Dashboard View Query

Run:

SELECT * 
FROM insurance_lakehouse.gold.vw_executive_insurance_overview;

Explain:

This is a dashboard-ready executive view built from Gold tables. It provides KPI-level insights for business users.

KPIs include:
- total policies
- premium revenue
- claims ratio
- fraud risk rate
- payment rejection rate

“This view is designed for executive-level insurance reporting.”

---

# Step 5 — Show Final Validation Summary

Show:
- Gold table validation results
- dashboard view row counts
- feature table grain validation
- KPI sanity checks

Explain:

All Gold tables are successfully created.
All dashboard views return valid rows.
Fraud feature table maintains one row per claim.
All KPI outputs are validated for correctness.

“This ensures the analytics layer is trusted and production-ready.”

---

# Step 6 — Show GDPR Governance Document

Open gdpr_governance_design.md

Explain:

- PII fields are identified and restricted
- masking and hashing applied where needed
- Gold dashboards contain no raw sensitive data
- governance rules ensure compliance with GDPR

Show validation output:

exposed PII fields = []

“This confirms no sensitive customer data is exposed in dashboard layers.”

---

# Step 7 — Show Fraud Feature Table Schema

Run:

DESCRIBE insurance_lakehouse.gold.gold_claim_fraud_features;

Explain:

This table represents one row per insurance claim and is designed for machine learning and fraud detection use cases.

It combines:
- claim attributes
- policy context
- payment behavior
- fraud indicators

Key features:
- risk_score
- suspicious_amount_flag
- duplicate_claim_flag
- late_report_flag
- claim amount

“This table is AI-ready for fraud detection models.”

---

# Step 8 — Close with Lessons Learned

Key learnings:

- Importance of trusted Silver layer
- Clean data grain design is critical
- Proper joins prevent KPI errors
- GDPR compliance is essential in real systems
- Gold layer enables business decision-making
- Lakehouse architecture supports BI + AI together

Final statement:

“This project demonstrates a complete enterprise-style insurance lakehouse using Databricks and AWS with governance, analytics, and AI-ready engineering.”