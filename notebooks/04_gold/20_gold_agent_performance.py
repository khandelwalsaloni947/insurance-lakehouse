# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "1"
# ///
# MAGIC %md
# MAGIC # 20 — Gold Agent Performance
# MAGIC
# MAGIC Week 11 Day 3 — Gold Analytics, Insurance KPIs, AI-Ready Features, and Performance.
# MAGIC
# MAGIC Replace catalog/schema names if your environment uses different names.

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


silver_agents = spark.table(t(SILVER_SCHEMA, "silver_agents"))
silver_policies = spark.table(t(SILVER_SCHEMA, "silver_policies"))
silver_claims = spark.table(t(SILVER_SCHEMA, "silver_claims"))
silver_payments = spark.table(t(SILVER_SCHEMA, "silver_payments"))
policies_by_agent = silver_policies.groupBy("agent_id").agg(F.count("*").alias("total_policies_sold"), F.round(F.sum("premium_amount"), 2).alias("premium_revenue"))
claims_by_agent = silver_claims.join(silver_policies.select("policy_id", "agent_id"), "policy_id", "left").groupBy("agent_id").agg(F.count("*").alias("total_claims_linked"), F.round(F.sum("claim_amount"), 2).alias("total_claim_amount"))
payments_by_agent = silver_payments.join(silver_claims.select("claim_id", "policy_id"), "claim_id", "left").join(silver_policies.select("policy_id", "agent_id"), "policy_id", "left").groupBy("agent_id").agg(F.round(F.sum("payment_amount"), 2).alias("total_paid_amount"))
gold_agent_performance = (
    silver_agents.join(policies_by_agent, "agent_id", "left").join(claims_by_agent, "agent_id", "left").join(payments_by_agent, "agent_id", "left").fillna(0)
    .withColumn("claims_ratio", F.when(F.col("premium_revenue") == 0, None).otherwise(F.col("total_claim_amount") / F.col("premium_revenue")))
    .withColumn("estimated_commission", F.col("premium_revenue") * F.col("commission_rate"))
)
gold_agent_performance.write.mode("overwrite").format("delta").saveAsTable(t(GOLD_SCHEMA, "gold_agent_performance"))
display(gold_agent_performance.limit(20))
