# Day 3 Performance Notes

## Scope

This document records the main performance considerations applied during the Day 3 Gold layer implementation for the Rheinland Versicherung AG insurance lakehouse project.

The focus was on building scalable and business-ready Gold analytics tables while following Spark and Delta Lake best practices for joins, aggregations, and analytical workloads.

The review included Spark execution plan inspection, join optimization, aggregation strategy, Delta Lake storage optimization, and Gold table scalability considerations.

---

# Performance Observation 1 — Column Pruning Before Joins

For Gold tables such as:
- gold_claims_payment_summary
- gold_customer_risk_profile
- gold_claim_fraud_features

only the required columns were selected before joins instead of selecting all columns from Silver tables.

This reduced:
- shuffle size
- memory usage
- unnecessary metadata transfer

It also prevented duplicate technical columns such as:
- ingest_run_id
- ingest_timestamp
- source_file_name

During development, an earlier version of the feature table failed because duplicate ingestion metadata columns were carried through multiple joins.

Column pruning solved this issue and improved performance and pipeline stability.

---

# Performance Observation 2 — Payments Aggregated Before Joining to Claims

The payments dataset contains multiple payment records per claim.

Joining raw payment rows directly to claims can create:
- one-to-many duplication
- incorrect KPI calculations
- inflated claim totals

To avoid this, payments were first aggregated at claim level using:
- groupBy()
- sum()
- count()

The aggregated payment dataset was then joined to claims.

## Benefits

- preserves correct claim grain
- reduces join complexity
- avoids duplicate analytical rows
- improves aggregation performance

---

# Performance Observation 3 — Delta Lake Storage for Gold Tables

All Gold outputs were stored using Delta Lake format.

## Benefits

- ACID transactional reliability
- scalable analytics performance
- schema consistency
- optimized reads for BI tools
- support for future optimizations

The Gold tables are suitable for:
- BI dashboards
- Databricks SQL analytics
- fraud-risk reporting
- AI-ready feature engineering

---

# Performance Observation 4 — Spark Explain Plan Review

The Spark execution plan was reviewed using:

```python
gold_claim_fraud_features.explain(True)