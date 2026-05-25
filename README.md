# German Insurance Lakehouse Project

## Overview

This project builds a modern insurance lakehouse for a fictional German insurance company **Rheinland Versicherung AG** using cloud data engineering tools and best practices.

It simulates a real-world production-style data platform for insurance analytics, fraud detection, BI reporting, and AI-ready feature engineering.

## Architecture

Bronze → Silver → Quarantine → Gold

- **Bronze**: Ingested raw data from AWS S3 in Delta format  
- **Silver**: Cleaned, validated, and GDPR-aware trusted data  
- **Quarantine**: Invalid or suspicious records isolated for audit  
- **Gold**: Business-ready analytics and AI/ML feature tables  

## Datasets
- customers  
- policies  
- claims  
- payments  
- agents  
- fraud_indicators  

## 🟢 Day 1 — Data Creation & Bronze Layer 

- Synthetic insurance data generation using PySpark  
- Raw data stored in AWS S3  
- Bronze Delta ingestion completed  
- Partitioned scalable dataset design  
- Initial validation checks  

I generated synthetic insurance data and created Bronze layer tables in Databricks

https://dbc-41a10911-9515.cloud.databricks.com/editor/files/2977085487728008?o=7474651570114183

## Day 1 Summary

On Day 1, I built the foundation of the insurance lakehouse.

- Generated synthetic insurance data using PySpark
- Stored raw data in AWS S3
- Created Bronze layer tables in Databricks
- Validated initial dataset structure and partitions

👉 Result: Raw insurance data successfully landed and Bronze layer was created.


## 🟡 Day 2 — Silver Layer & GDPR

- Silver tables created with cleaned data  
- Data quality rules applied  
- FK validation:
  - claims ↔ policies  
  - claims ↔ customers  
  - payments ↔ claims  
- GDPR implemented:
  - masking & hashing of PII fields  
- Quarantine tables created for invalid records  
- Data quality reporting completed  

📸 **Screenshot to add here:**  
Silver or Quarantine table output showing cleaned data

## Day 2 Summary

On Day 2, I focused on data cleaning and governance.

- Created Silver layer with cleaned and standardized data
- Applied data quality rules (null checks, duplicates, validation)
- Established relationships between claims, policies, and customers
- Implemented GDPR compliance (masking/hashing sensitive fields)
- Created quarantine tables for invalid records

👉 Result: Trusted and clean Silver data was created with governance controls.



## 🔵 Day 3 — Gold Layer & Analytics 

- Business-ready Gold analytics tables created  
- Insurance KPIs implemented  
- Fraud risk analytics developed  
- Agent performance metrics built  

### Gold Tables

- gold_claims_overview  
- gold_policy_performance  
- gold_customer_risk_profile  
- gold_claims_payment_summary  
- gold_fraud_risk_summary  
- gold_agent_performance  
- gold_claim_fraud_features  

📸 **Screenshot to add here:**  
✔ Gold KPI table output OR dashboard view


## 🤖 AI-Ready Feature Engineering

The `gold_claim_fraud_features` table is designed for machine learning use cases:

- One row per claim (clean ML grain)
- Combines:
  - claim features  
  - policy context  
  - customer attributes  
  - payment behavior  
  - fraud signals  

Used for:
- Fraud detection models  
- Risk scoring  
- Anomaly detection  

---

## ⚙️ Performance Optimization

- Column pruning before joins  
- Pre-aggregation for performance  
- Avoided many-to-many join duplication  
- Delta Lake format for all tables  
- Efficient Spark execution plans  

## Day 3 Summary

On Day 3, I built business-ready analytics layers.

- Created Gold tables for insurance KPIs
- Built claims, policies, fraud, and customer analytics
- Developed agent performance metrics
- Created AI-ready fraud feature dataset

👉 Result: Business-ready Gold layer was created for dashboards and AI use cases.



## 🟣 Governance & GDPR 

- PII fields identified and restricted  
- Hashing applied to sensitive identifiers  
- Role-based access model implemented  
- Gold layer contains no raw PII  
- Compliance validated using exposure checks  

📸 **Screenshot to add here:**  
✔ exposed PII fields = []

## Governance Summary

- Verified that no PII fields are exposed in Gold views
- Ensured GDPR compliance across all dashboard layers
- Confirmed secure data design with no sensitive leakage

👉 Result: Fully GDPR-compliant analytics layer.

## 📊 Business Value

This lakehouse enables:

- Insurance KPI dashboards  
- Claims performance monitoring  
- Fraud detection insights  
- Customer risk segmentation  
- Agent performance tracking  
- AI/ML-ready datasets  

## Final Project Summary

This project demonstrates an end-to-end cloud data engineering pipeline built using Databricks and AWS, covering data ingestion, transformation, governance, analytics, and AI-ready feature engineering.

👉 Result: Production-style insurance lakehouse ready for BI and ML use cases.

