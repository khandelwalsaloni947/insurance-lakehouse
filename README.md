# German Insurance Lakehouse Project

## Overview

This project builds a modern insurance lakehouse for a fictional German insurance company **Rheinland Versicherung AG** using cloud data engineering tools and best practices.

It simulates a real-world production-style data platform for insurance analytics, fraud detection, BI reporting, and AI-ready feature engineering.

---

## Project Architecture
Raw → Bronze → Silver → Quarantine → Gold


- **Raw**: Unprocessed data stored in AWS S3  
- **Bronze**: Ingested raw data into Delta tables  
- **Silver**: Cleaned, validated, GDPR-aware trusted data  
- **Quarantine**: Invalid or suspicious records  
- **Gold**: Business-ready analytics and ML feature tables  

---

## Datasets

- customers  
- policies  
- claims  
- payments  
- agents  
- fraud_indicators  

---

## Day 1 Work

- Synthetic insurance data generation using PySpark  
- Data written to AWS S3 (raw layer)  
- Bronze Delta ingestion completed  
- Basic validation and schema checks performed  
- Partitioned dataset structure created for scalability  

---

## Day 2 Work (Silver Layer)

- Silver tables created with cleaned and standardized data  
- Data quality rules applied (null checks, duplicates, validation rules)  
- Foreign key relationships validated:
  - claims ↔ policies  
  - claims ↔ customers  
  - payments ↔ claims  
- GDPR handling implemented:
  - masking / hashing of sensitive fields  
- Quarantine tables created for invalid records  
- Data quality reporting completed  
- Bronze vs Silver reconciliation performed  

---

## Day 3 Work (Gold Layer)

- Business-ready Gold analytics tables created  
- KPI-driven insurance metrics implemented  
- Fraud risk analytics developed  
- Agent and customer performance analysis added  

### Gold Tables

- gold_claims_overview  
- gold_policy_performance  
- gold_customer_risk_profile  
- gold_claims_payment_summary  
- gold_fraud_risk_summary  
- gold_agent_performance  
- gold_claim_fraud_features  

---

## AI-Ready Feature Engineering

The `gold_claim_fraud_features` table is designed for machine learning use cases:

- One row per claim (clean ML grain)  
- Combines:
  - claim features  
  - policy context  
  - customer demographics  
  - payment behavior  
  - fraud signals  

Used for:
- fraud detection models  
- risk scoring  
- anomaly detection  

---

## Performance Optimization

- Column pruning before joins applied  
- Aggregation before joins used for payments  
- Avoided one-to-many join duplication  
- Delta Lake format used for all Gold tables  
- Spark explain plan reviewed for optimization  
- Efficient join strategy followed  

---

## Business Value

This lakehouse enables:

- Insurance KPI dashboards  
- Claims performance monitoring  
- Fraud detection insights  
- Customer risk segmentation  
- Agent performance tracking  
- AI/ML-ready datasets  

---

## Technologies Used

- Databricks  
- AWS S3  
- PySpark  
- Spark SQL  
- Delta Lake  

---

## Final Summary

This project demonstrates an end-to-end modern **lakehouse architecture** including:

Raw ingestion → Data cleaning → Data governance → Analytics → AI-ready feature engineering

It simulates a real insurance analytics platform used in enterprise environments.