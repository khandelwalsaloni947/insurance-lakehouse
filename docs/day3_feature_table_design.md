# Day 3 Feature Table Design — AI-Ready Fraud Features

## Project
Industrial Insurance Lakehouse on Databricks and AWS

Company: Rheinland Versicherung AG

---

# 1. Purpose of Feature Table

The table `gold_claim_fraud_features` is designed as an AI-ready dataset for future machine learning models.

Its main purpose is to enable fraud detection and risk prediction at claim level.

This table will be used for:
- fraud detection models
- risk scoring models
- anomaly detection
- insurance claim behavior analysis

---

# 2. Grain of the Table

Each row represents:

> One claim (claim_id level grain)

This ensures:
- no duplication of claims
- consistent ML training dataset structure
- easy model interpretability

---

# 3. Input Tables (Silver Layer)

The feature table is built using the following Silver tables:

- silver_claims  
- silver_policies  
- silver_customers  
- silver_payments  
- silver_fraud_indicators  

These tables provide:
- claim details
- policy context
- customer demographics
- payment behavior
- fraud signals

---

# 4. Feature Engineering Logic

## Claim-based Features
- claim_amount
- claim_type
- claim_status
- fraud_flag

## Policy-based Features
- policy_type
- premium_amount
- coverage_amount
- policy_age_days

## Customer-based Features
- customer_age
- bundesland (region)

## Payment Features
- total_paid_amount
- payment_count
- payment_delay_days

## Fraud Signals
- previous_claims_count
- suspicious_amount_flag
- duplicate_claim_flag
- late_report_flag
- high_risk_region_flag
- risk_score

---

# 5. Derived AI Features

## Claim Coverage Ratio
Formula:
> claim_amount / coverage_amount

Used to detect unusually high claims compared to coverage.

---

## Policy Age Feature
Formula:
> claim_date - policy_start_date

Used to understand how early fraud happens after policy creation.

---

## Customer Age Feature
Formula:
> (claim_date - date_of_birth) / 365.25

Used to segment risk by age groups.

---

## Payment Delay Feature
Formula:
> first_payment_date - claim_date

Used to detect suspicious delays or processing patterns.

---

# 6. Data Quality Considerations

The following checks were important:

- missing claim_id → removed or fixed in Silver
- null payment values → handled with default aggregation
- duplicate claims → avoided via claim-level grain
- invalid ratios → protected using null-safe calculations

---

# 7. Why This Table is AI-Ready

This feature table is designed for machine learning because:

- all features are numeric or encoded
- no duplicate grain
- no raw PII exposed
- consistent claim-level structure
- combines behavioral + financial + demographic signals

---

# 8. Future Use Cases

This table can support:

- Fraud classification model
- Risk scoring engine
- Real-time anomaly detection
- Insurance claim automation systems

---

# 9. Summary

The `gold_claim_fraud_features` table is the foundation of AI-driven insurance analytics in the lakehouse architecture.

It transforms raw insurance data into structured, model-ready features for advanced analytics and machine learning.