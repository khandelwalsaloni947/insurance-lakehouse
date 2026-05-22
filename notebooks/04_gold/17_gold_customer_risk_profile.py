# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "1"
# ///
# MAGIC %md
# MAGIC # 17 — Gold Customer Risk Profile
# MAGIC
# MAGIC Week 11 Day 3 — Gold Analytics, Insurance KPIs, AI-Ready Features, and Performance.
# MAGIC
# MAGIC ## Purpose
# MAGIC Customer-level insurance risk profile table.
# MAGIC
# MAGIC Used for:
# MAGIC - fraud investigation
# MAGIC - customer segmentation
# MAGIC - future AI/ML risk modeling

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


silver_customers = spark.table(t(SILVER_SCHEMA, "silver_customers"))
silver_policies = spark.table(t(SILVER_SCHEMA, "silver_policies"))
silver_claims = spark.table(t(SILVER_SCHEMA, "silver_claims"))
silver_fraud = spark.table(t(SILVER_SCHEMA, "silver_fraud_indicators"))

policy_agg = silver_policies.groupBy("customer_id").agg(F.count("*").alias("total_policies"), F.round(F.sum("premium_amount"), 2).alias("total_premium_amount"))
claims_agg = silver_claims.join(silver_fraud.select("claim_id", "risk_score"), on="claim_id", how="left").groupBy("customer_id").agg(
    F.count("*").alias("total_claims"),
    F.round(F.sum("claim_amount"), 2).alias("total_claim_amount"),
    F.round(F.avg("risk_score"), 2).alias("average_risk_score"),
    F.sum(F.when(F.col("risk_score") >= 70, 1).otherwise(0)).alias("high_risk_claims")
)
gold_customer_risk_profile = silver_customers.join(policy_agg, "customer_id", "left").join(claims_agg, "customer_id", "left").fillna(0)
gold_customer_risk_profile.write.mode("overwrite").format("delta").saveAsTable(t(GOLD_SCHEMA, "gold_customer_risk_profile"))
display(gold_customer_risk_profile.limit(20))
