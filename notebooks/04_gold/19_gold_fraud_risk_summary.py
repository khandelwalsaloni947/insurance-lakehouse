# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "1"
# ///
# MAGIC %md
# MAGIC # 19 — Gold Fraud Risk Summary
# MAGIC
# MAGIC Week 11 Day 3 — Gold Analytics, Insurance KPIs, AI-Ready Features, and Performance.
# MAGIC
# MAGIC ## Purpose
# MAGIC Fraud-risk analytics summary across:
# MAGIC - risk bands
# MAGIC - claim types
# MAGIC - policy types
# MAGIC
# MAGIC This table supports:
# MAGIC - fraud monitoring
# MAGIC - investigation prioritization
# MAGIC - operational risk analytics

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql import Window

CATALOG = "insurance_lakehouse"
SILVER_SCHEMA = "silver"
GOLD_SCHEMA = "gold"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{GOLD_SCHEMA}")

def t(schema, table):
    return f"{CATALOG}.{schema}.{table}"

# COMMAND ----------


silver_claims = spark.table(t(SILVER_SCHEMA, "silver_claims"))
silver_fraud = spark.table(t(SILVER_SCHEMA, "silver_fraud_indicators"))
silver_policies = spark.table(t(SILVER_SCHEMA, "silver_policies"))
silver_customers = spark.table(t(SILVER_SCHEMA, "silver_customers"))

fraud_enriched = (
    silver_claims.join(silver_fraud, "claim_id", "left")
    .join(silver_policies.select("policy_id", "policy_type"), "policy_id", "left")
    .join(silver_customers.select("customer_id", "bundesland"), "customer_id", "left")
    .withColumn("risk_band", F.when(F.col("risk_score") < 30, "low").when(F.col("risk_score") < 70, "medium").otherwise("high"))
)
gold_fraud_risk_summary = fraud_enriched.groupBy("bundesland", "policy_type", "claim_type", "risk_band").agg(
    F.count("*").alias("total_claims"),
    F.sum(F.when(F.col("risk_band") == "high", 1).otherwise(0)).alias("high_risk_claims"),
    F.round(F.avg("risk_score"), 2).alias("average_risk_score"),
    F.sum(F.when(F.col("suspicious_amount_flag") == True, 1).otherwise(0)).alias("suspicious_amount_count"),
    F.sum(F.when(F.col("duplicate_claim_flag") == True, 1).otherwise(0)).alias("duplicate_claim_count"),
    F.sum(F.when(F.col("late_report_flag") == True, 1).otherwise(0)).alias("late_report_count")
)
gold_fraud_risk_summary.write.mode("overwrite").format("delta").saveAsTable(t(GOLD_SCHEMA, "gold_fraud_risk_summary"))
display(gold_fraud_risk_summary.limit(20))
