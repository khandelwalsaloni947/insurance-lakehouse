# Databricks notebook source

# MAGIC %md
# MAGIC # 25 — Dashboard Queries
# MAGIC Preview each dashboard view.

# COMMAND ----------

catalog = "insurance_lakehouse"
gold_schema = "gold"
views = [
    "vw_executive_insurance_overview",
    "vw_claims_operations",
    "vw_policy_portfolio",
    "vw_fraud_risk_monitoring",
    "vw_agent_regional_performance",
    "vw_data_quality_monitoring"
]

for view in views:
    print(f"Previewing {view}")
    display(spark.table(f"{catalog}.{gold_schema}.{view}").limit(20))

