# Day 3 Performance Notes

## Scope

This document records the main performance considerations applied during the Day 3 Gold layer implementation for the Rheinland Versicherung AG insurance lakehouse project.

The focus was on building scalable and business-ready Gold analytics tables while following Spark and Delta Lake best practices for joins, aggregations, and analytical workloads.

The review included Spark execution plan inspection, join optimization, aggregation strategy, Delta Lake storage optimization, and Gold table scalability considerations.

---

# Performance Observation 1 — Column Pruning Before Joins

For Gold tables such as gold_claims_payment_summary, gold_customer_risk_profile, and gold_claim_fraud_features, only the required columns were selected before joins instead of selecting all columns from Silver tables.

This reduced shuffle size, memory usage, and unnecessary metadata transfer.

It also prevented duplicate technical columns such as ingest_run_id, ingest_timestamp, and source_file_name.

During development, an earlier version of the feature table failed because duplicate ingestion metadata columns were carried through multiple joins.

Column pruning solved this issue and improved performance and stability of the pipeline.

---

# Performance Observation 2 — Payments Aggregated Before Joining to Claims

The payments dataset contains multiple payment records per claim.

Joining raw payment rows directly to claims can create one-to-many duplication and incorrect KPI calculations.

To avoid this, payments were first aggregated at claim level using groupBy and aggregation functions like sum and count.

The aggregated payment table was then joined to claims.

Benefits:
- preserves correct claim grain  
- reduces join complexity  
- avoids duplicate analytical rows  
- improves aggregation performance  

---

# Performance Observation 3 — Delta Lake Storage for Gold Tables

All Gold outputs were stored using Delta Lake format.

Benefits:
- transactional reliability  
- scalable analytics performance  
- schema consistency  
- optimized reads for BI tools  
- support for future optimizations  

The Gold tables are suitable for BI dashboards, Databricks SQL analytics, fraud-risk reporting, and AI-ready feature engineering.

---

# Explain Plan Review

The Spark execution plan was reviewed using:

gold_claim_fraud_features.explain(True)

The execution plan showed:
- Parsed Logical Plan  
- Optimized Logical Plan  
- Physical Plan  
- Photon execution support  
- Parquet-based Delta scan  

Key observations:
- Spark successfully optimized the query  
- Photon engine supported full execution  
- optimizer statistics were available  
- no execution issues were detected  

---

# Optimizer Statistics

Optimizer statistics were available for the Gold feature table.

Benefits:
- better query planning  
- improved join optimization  
- efficient execution strategies  

---

# Row Count Validation

Gold tables validated:

- gold_claims_payment_summary → 50000  
- gold_claim_fraud_features → 50000  
- gold_customer_risk_profile → 10000  

All claim-level tables maintained correct one-row-per-entity grain.

---

# OPTIMIZE / ZORDER Review

OPTIMIZE was successfully executed in the environment.

Future improvement option:

OPTIMIZE insurance_lakehouse.gold.gold_claim_fraud_features  
ZORDER BY (claim_id, risk_score)

Benefits:
- faster fraud-risk queries  
- better filtering performance  
- improved dashboard speed  

---

# Performance Conclusion

The Day 3 Gold layer was built using scalable Spark and Delta Lake best practices.

It supports:
- insurance KPI analytics  
- claims reporting  
- fraud-risk analysis  
- BI dashboards  
- AI-ready feature engineering  

The Gold layer is optimized for business analytics with clean data modeling and scalable performance design.