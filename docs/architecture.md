# Insurance Lakehouse Architecture

## Project Overview

This project builds a modern **Insurance Lakehouse Architecture** for a fictional company:

**Rheinland Versicherung AG (Germany)**

It follows a multi-layer data architecture pattern used in real cloud data platforms.

---

# 🏗️ Architecture Flow

Raw Data → Bronze Layer → Silver Layer → Quarantine → Gold Layer → Dashboards / AI

---

# 📦 1. Raw Layer (AWS S3)

## Purpose
- Stores original synthetic insurance data
- Acts as landing zone

## Data Sources
- Customers
- Policies
- Claims
- Payments
- Agents
- Fraud Indicators

## Storage
- AWS S3 bucket

## Key Point
- No transformation
- No cleaning
- Just raw ingestion

---

# 🥉 2. Bronze Layer (Databricks Delta)

## Purpose
- First structured ingestion layer
- Converts raw data into Delta tables

## Features
- Schema applied
- Partitioned data
- Basic validation

## Example Tables
- bronze_customers
- bronze_claims
- bronze_policies
- bronze_payments

## Key Point
- “As-is” data from source system

---

# 🥈 3. Silver Layer (Clean & Trusted Data)

## Purpose
- Cleaned and validated data
- Business-ready for analysis

## Transformations
- Remove duplicates
- Fix null values
- Standardize formats
- Validate relationships
  - claims ↔ policies
  - claims ↔ customers

## GDPR Handling
- Masking / hashing PII fields
- Removing sensitive data exposure

## Example Tables
- silver_customers
- silver_claims
- silver_policies
- silver_payments

## Key Point
- Trusted data for analytics

---

# ⚠️ 4. Quarantine Layer

## Purpose
- Stores invalid or suspicious records

## Examples
- Missing customer_id
- Invalid claim_amount
- Broken relationships

## Example Tables
- quarantine_invalid_customers
- quarantine_invalid_claims
- quarantine_invalid_policies

## Key Point
- Data quality tracking and audit trail

---

# 🥇 5. Gold Layer (Business & Analytics Layer)

## Purpose
- Business-ready aggregated data
- Used for dashboards and reporting

## Outputs
- KPIs
- Analytics tables
- AI-ready features

## Example Tables

- gold_claims_overview
- gold_policy_performance
- gold_customer_risk_profile
- gold_claims_payment_summary
- gold_fraud_risk_summary
- gold_agent_performance
- gold_claim_fraud_features

## Key Point
- Final layer for business users

---

# 📊 6. Dashboard Layer (Views)

## Purpose
- SQL views for BI dashboards

## Example Views
- vw_executive_insurance_overview
- vw_claims_operations
- vw_policy_portfolio
- vw_fraud_risk_monitoring
- vw_agent_regional_performance
- vw_data_quality_monitoring

## Key Point
- No PII exposure
- Aggregated business metrics only

---

# 🤖 7. AI / ML Layer

## Purpose
- Feature engineering for machine learning

## Example
- gold_claim_fraud_features

## Features Include
- Claim behavior
- Customer profile
- Policy context
- Payment patterns
- Fraud indicators

## Use Cases
- Fraud detection
- Risk scoring
- Anomaly detection

---

# 🔐 Governance & GDPR

## Key Principles
- No raw PII in Gold layer
- Sensitive fields masked or hashed
- Access control via roles
- Data lineage maintained

## PII Examples
- name
- email
- phone number
- address
- IBAN

---

# ⚙️ Technologies Used

- Databricks (Spark)
- AWS S3
- Delta Lake
- PySpark
- SQL

---

# 🚀 Final Summary

This architecture demonstrates a real-world **modern Lakehouse design**:

✔ Scalable ingestion (S3)  
✔ Structured storage (Bronze)  
✔ Clean trusted data (Silver)  
✔ Audit & quarantine layer  
✔ Business analytics (Gold)  
✔ Dashboard-ready views  
✔ AI/ML feature engineering  
✔ GDPR compliance  

---

## 🎯 Result

A production-style insurance data platform for analytics, fraud detection, and AI use cases.