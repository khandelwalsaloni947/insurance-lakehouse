# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "1"
# ///
# MAGIC %md
# MAGIC # 16 — Gold Policy Performance
# MAGIC
# MAGIC Week 11 Day 3 — Gold Analytics, Insurance KPIs, AI-Ready Features, and Performance.
# MAGIC
# MAGIC ##  Purpose
# MAGIC This table provides a business-level view of insurance policy performance across:
# MAGIC - policy type
# MAGIC - policy status
# MAGIC - sales channel
# MAGIC - bundesland
# MAGIC
# MAGIC It helps track revenue, coverage distribution, and agent-driven commission estimates.

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


silver_policies = spark.table(t(SILVER_SCHEMA, "silver_policies"))
silver_customers = spark.table(t(SILVER_SCHEMA, "silver_customers"))
policies_enriched = silver_policies.join(silver_customers.select("customer_id", "bundesland"), on="customer_id", how="left")
gold_policy_performance = policies_enriched.groupBy("policy_type", "policy_status", "sales_channel", "bundesland").agg(
    F.count("*").alias("total_policies"),
    F.sum(F.when(F.col("policy_status") == "active", 1).otherwise(0)).alias("active_policies"),
    F.round(F.sum("premium_amount"), 2).alias("premium_revenue"),
    F.round(F.avg("premium_amount"), 2).alias("average_premium"),
    F.round(F.sum("coverage_amount"), 2).alias("total_coverage")
)
gold_policy_performance.write.mode("overwrite").format("delta").saveAsTable(t(GOLD_SCHEMA, "gold_policy_performance"))
display(gold_policy_performance.limit(20))


# COMMAND ----------

gold_policy_performance.printSchema()
