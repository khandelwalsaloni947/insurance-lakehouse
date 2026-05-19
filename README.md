# German Insurance Lakehouse Project

## Overview
This project builds a modern insurance lakehouse using:
- AWS S3
- Databricks
- PySpark
- Delta Lake

## Project Architecture
Raw → Bronze → Silver → Quarantine → Gold

## Datasets
- customers
- policies
- claims
- payments
- agents
- fraud_indicators

## Day 1 Completed
- Synthetic data generation
- Raw data write to S3
- Bronze Delta ingestion
- Validation checks

## Day 2 Completed
- Silver layer created with data validation
- GDPR & PII handling implemented (hashing + masking)
- Quarantine layer implemented for invalid records
- Data quality checks (Bronze vs Silver comparison)
- Foreign key validations (claims, policies, customers, payments)
- Payment + fraud validation rules applied
- Data quality summary report generated
- GDPR documentation completed

## Technologies Used
- Databricks
- AWS S3
- PySpark
- Delta Lake