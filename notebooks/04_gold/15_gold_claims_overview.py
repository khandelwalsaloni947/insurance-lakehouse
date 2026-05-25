# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "1"
# ///
# MAGIC %md
# MAGIC # 15 — Gold Claims Overview
# MAGIC
# MAGIC Week 11 Day 3 — Gold Analytics, Insurance KPIs, AI-Ready Features, and Performance.
# MAGIC
# MAGIC Replace catalog/schema names if your environment uses different names.
# MAGIC
# MAGIC Claims Analytics Summary Table
# MAGIC
# MAGIC ## 🎯 Purpose
# MAGIC This table provides a monthly claims performance overview across:
# MAGIC - claim status
# MAGIC - claim type
# MAGIC - policy type
# MAGIC - bundesland
# MAGIC
# MAGIC It helps in tracking claims volume, approval rates, and risk exposure.

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

# DBTITLE 1,Load Silver Tables
silver_claims = spark.table(t(SILVER_SCHEMA, "silver_claims"))
silver_policies = spark.table(t(SILVER_SCHEMA, "silver_policies"))
silver_customers = spark.table(t(SILVER_SCHEMA, "silver_customers"))
silver_fraud = spark.table(t(SILVER_SCHEMA, "silver_fraud_indicators"))

# COMMAND ----------

# DBTITLE 1,Enrichment Logic
claims_enriched = (
    silver_claims
    .join(silver_policies.select("policy_id", "policy_type"), on="policy_id", how="left")
    .join(silver_customers.select("customer_id", "bundesland"), on="customer_id", how="left")
    .join(silver_fraud.select("claim_id", "risk_score"), on="claim_id", how="left")
    .withColumn("claim_month", F.date_trunc("month", F.col("claim_date")).cast("date"))
)

# COMMAND ----------

# DBTITLE 1,Gold Aggregation (Main Table)
gold_claims_overview = (
    claims_enriched.groupBy(
        "claim_month",
        "claim_status",
        "claim_type",
        "policy_type",
        "bundesland"
    )
    .agg(
        F.count("*").alias("total_claims"),
        F.sum(F.when(F.col("claim_status") == "open", 1).otherwise(0)).alias("open_claims"),
        F.sum(F.when(F.col("claim_status") == "approved", 1).otherwise(0)).alias("approved_claims"),
        F.sum(F.when(F.col("claim_status") == "rejected", 1).otherwise(0)).alias("rejected_claims"),
        F.sum(F.when(F.col("claim_status") == "paid", 1).otherwise(0)).alias("paid_claims"),
        F.round(F.sum("claim_amount"), 2).alias("total_claim_amount"),
        F.round(F.avg("claim_amount"), 2).alias("average_claim_amount"),
        F.round(F.avg("risk_score"), 2).alias("average_risk_score")
    )
)

# COMMAND ----------

# DBTITLE 1,Write to Gold Table
gold_claims_overview.write.mode("overwrite") \
    .format("delta") \
    .saveAsTable(t(GOLD_SCHEMA, "gold_claims_overview"))

# COMMAND ----------

display(gold_claims_overview.limit(20))

# COMMAND ----------


silver_claims = spark.table(t(SILVER_SCHEMA, "silver_claims"))
silver_policies = spark.table(t(SILVER_SCHEMA, "silver_policies"))
silver_customers = spark.table(t(SILVER_SCHEMA, "silver_customers"))
silver_fraud = spark.table(t(SILVER_SCHEMA, "silver_fraud_indicators"))

claims_enriched = (
    silver_claims
    .join(silver_policies.select("policy_id", "policy_type"), on="policy_id", how="left")
    .join(silver_customers.select("customer_id", "bundesland"), on="customer_id", how="left")
    .join(silver_fraud.select("claim_id", "risk_score"), on="claim_id", how="left")
    .withColumn("claim_month", F.date_trunc("month", F.col("claim_date")).cast("date"))
)

gold_claims_overview = (
    claims_enriched.groupBy("claim_month", "claim_status", "claim_type", "policy_type", "bundesland")
    .agg(
        F.count("*").alias("total_claims"),
        F.sum(F.when(F.col("claim_status") == "open", 1).otherwise(0)).alias("open_claims"),
        F.sum(F.when(F.col("claim_status") == "approved", 1).otherwise(0)).alias("approved_claims"),
        F.sum(F.when(F.col("claim_status") == "rejected", 1).otherwise(0)).alias("rejected_claims"),
        F.sum(F.when(F.col("claim_status") == "paid", 1).otherwise(0)).alias("paid_claims"),
        F.round(F.sum("claim_amount"), 2).alias("total_claim_amount"),
        F.round(F.avg("claim_amount"), 2).alias("average_claim_amount"),
        F.round(F.avg("risk_score"), 2).alias("average_risk_score")
    )
)
gold_claims_overview.write.mode("overwrite").format("delta").saveAsTable(t(GOLD_SCHEMA, "gold_claims_overview"))
display(gold_claims_overview.limit(10))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM insurance_lakehouse.gold.vw_executive_insurance_overview;
