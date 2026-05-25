# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "1"
# ///
# MAGIC %md
# MAGIC # 24 — Dashboard Views
# MAGIC Create final dashboard-ready SQL views. Use Gold tables as inputs and avoid raw PII.

# COMMAND ----------

catalog = "insurance_lakehouse"
gold_schema = "gold"
quarantine_schema = "quarantine"

spark.sql(f"USE CATALOG {catalog}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{gold_schema}")

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE VIEW {catalog}.{gold_schema}.vw_executive_insurance_overview AS
WITH policy AS (
    SELECT
        SUM(total_policies) AS total_policies,
        SUM(active_policies) AS total_active_policies,
        ROUND(SUM(premium_revenue), 2) AS total_premium_revenue
    FROM {catalog}.{gold_schema}.gold_policy_performance
),
claims AS (
    SELECT
        SUM(total_claims) AS total_claims,
        SUM(paid_claims) AS paid_claims,
        ROUND(SUM(total_claim_amount), 2) AS total_claim_amount
    FROM {catalog}.{gold_schema}.gold_claims_overview
),
fraud AS (
    SELECT
        SUM(total_claims) AS fraud_total_claims,
        SUM(high_risk_claims) AS high_risk_claims
    FROM {catalog}.{gold_schema}.gold_fraud_risk_summary
),
payments AS (
    SELECT
        SUM(payment_count) AS total_payments,
        SUM(payment_rejection_count) AS rejected_payments
    FROM {catalog}.{gold_schema}.gold_claim_fraud_features
),
customers AS (
    SELECT
        COUNT(*) AS total_customers
    FROM {catalog}.{gold_schema}.gold_customer_risk_profile
)
SELECT
    customers.total_customers,
    policy.total_policies,
    policy.total_active_policies,
    policy.total_premium_revenue,
    claims.total_claims,
    claims.paid_claims,
    claims.total_claim_amount,
    ROUND(claims.total_claim_amount / NULLIF(policy.total_premium_revenue, 0), 4) AS claims_ratio,
    ROUND(fraud.high_risk_claims / NULLIF(fraud.fraud_total_claims, 0), 4) AS fraud_risk_rate,
    ROUND(payments.rejected_payments / NULLIF(payments.total_payments, 0), 4) AS payment_rejection_rate
FROM policy
CROSS JOIN claims
CROSS JOIN fraud
CROSS JOIN payments
CROSS JOIN customers
""")

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE VIEW {catalog}.{gold_schema}.vw_claims_operations AS
SELECT
    claim_status,
    claim_type,
    policy_type,
    bundesland,
    SUM(total_claims) AS total_claims,
    ROUND(SUM(total_claim_amount), 2) AS total_claim_amount,
    ROUND(AVG(average_claim_amount), 2) AS average_claim_amount,
    ROUND(AVG(average_risk_score), 2) AS average_risk_score
FROM {catalog}.{gold_schema}.gold_claims_overview
GROUP BY claim_status, claim_type, policy_type, bundesland
""")

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE VIEW {catalog}.{gold_schema}.vw_policy_portfolio AS
SELECT
    policy_type,
    policy_status,
    sales_channel,
    bundesland,
    SUM(total_policies) AS total_policies,
    SUM(active_policies) AS active_policies,
    SUM(CASE WHEN policy_status = 'cancelled' THEN total_policies ELSE 0 END) AS cancelled_policies,
    ROUND(SUM(premium_revenue), 2) AS premium_revenue,
    ROUND(AVG(average_premium), 2) AS average_premium,
    ROUND(SUM(total_coverage), 2) AS total_coverage
FROM {catalog}.{gold_schema}.gold_policy_performance
GROUP BY policy_type, policy_status, sales_channel, bundesland
""")

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE VIEW {catalog}.{gold_schema}.vw_fraud_risk_monitoring AS
SELECT
    bundesland,
    policy_type,
    claim_type,
    risk_band,
    SUM(total_claims) AS total_claims,
    SUM(high_risk_claims) AS high_risk_claims,
    ROUND(SUM(high_risk_claims) / NULLIF(SUM(total_claims), 0), 4) AS high_risk_rate,
    ROUND(AVG(average_risk_score), 2) AS average_risk_score,
    SUM(suspicious_amount_count) AS suspicious_amount_count,
    SUM(duplicate_claim_count) AS duplicate_claim_count,
    SUM(late_report_count) AS late_report_count
FROM {catalog}.{gold_schema}.gold_fraud_risk_summary
GROUP BY bundesland, policy_type, claim_type, risk_band
""")

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE VIEW {catalog}.{gold_schema}.vw_agent_regional_performance AS
SELECT
    agent_id,
    agent_name,
    region,
    city,
    bundesland,
    active_flag,
    total_policies_sold,
    premium_revenue,
    total_claims_linked,
    total_claim_amount,
    total_paid_amount,
    claims_ratio,
    estimated_commission
FROM {catalog}.{gold_schema}.gold_agent_performance
""")

# COMMAND ----------

spark.sql(f"""
CREATE OR REPLACE VIEW {catalog}.{gold_schema}.vw_data_quality_monitoring AS
SELECT 'customers' AS dataset, COUNT(*) AS quarantine_count
FROM {catalog}.{quarantine_schema}.quarantine_invalid_customers
UNION ALL
SELECT 'policies', COUNT(*)
FROM {catalog}.{quarantine_schema}.quarantine_invalid_policies
UNION ALL
SELECT 'claims', COUNT(*)
FROM {catalog}.{quarantine_schema}.quarantine_invalid_claims
UNION ALL
SELECT 'payments', COUNT(*)
FROM {catalog}.{quarantine_schema}.quarantine_invalid_payments
UNION ALL
SELECT 'fraud_indicators', COUNT(*)
FROM {catalog}.{quarantine_schema}.quarantine_invalid_fraud_indicators
""")

# COMMAND ----------

from pyspark.sql import Row

views = [
    "vw_executive_insurance_overview",
    "vw_claims_operations",
    "vw_policy_portfolio",
    "vw_fraud_risk_monitoring",
    "vw_agent_regional_performance",
    "vw_data_quality_monitoring"
]

rows = []

for view in views:
    full_name = f"{catalog}.{gold_schema}.{view}"
    row_count = spark.table(full_name).count()
    rows.append(Row(view_name=view, row_count=row_count, status="PASS" if row_count > 0 else "CHECK"))

display(spark.createDataFrame(rows))

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW VIEWS IN insurance_lakehouse.gold;
