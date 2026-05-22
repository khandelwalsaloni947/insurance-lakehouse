# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "1"
# ///
# MAGIC %md
# MAGIC # 21 — Gold Claim Fraud Features
# MAGIC
# MAGIC Week 11 Day 3 — Gold Analytics, Insurance KPIs, AI-Ready Features, and Performance.
# MAGIC
# MAGIC Replace catalog/schema names if your environment uses different names.

# COMMAND ----------


from pyspark.sql import functions as F

CATALOG = "insurance_lakehouse"
SILVER_SCHEMA = "silver"
GOLD_SCHEMA = "gold"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{GOLD_SCHEMA}")

def t(schema, table):
    return f"{CATALOG}.{schema}.{table}"

# COMMAND ----------

silver_claims = (
    spark.table(t(SILVER_SCHEMA, "silver_claims"))
    .select(
        "claim_id",
        "policy_id",
        "customer_id",
        "claim_date",
        "claim_type",
        "claim_status",
        "claim_amount",
        "fraud_flag"
    )
)

silver_policies = (
    spark.table(t(SILVER_SCHEMA, "silver_policies"))
    .select(
        "policy_id",
        "policy_type",
        "start_date",
        "premium_amount",
        "coverage_amount"
    )
)

silver_customers = (
    spark.table(t(SILVER_SCHEMA, "silver_customers"))
    .select(
        "customer_id",
        "customer_age",
        "bundesland"
    )
)

silver_payments = (
    spark.table(t(SILVER_SCHEMA, "silver_payments"))
    .select(
        "claim_id",
        "payment_date",
        "payment_amount",
        "payment_status"
    )
)

silver_fraud = (
    spark.table(t(SILVER_SCHEMA, "silver_fraud_indicators"))
    .select(
        "claim_id",
        "previous_claims_count",
        "suspicious_amount_flag",
        "duplicate_claim_flag",
        "late_report_flag",
        "high_risk_region_flag",
        "risk_score"
    )
)


# COMMAND ----------

payments_by_claim = (
    silver_payments
    .groupBy("claim_id")
    .agg(
        F.min("payment_date").alias("first_payment_date"),
        F.round(F.sum("payment_amount"), 2).alias("total_paid_amount"),
        F.count("*").alias("payment_count"),
        F.sum(F.when(F.col("payment_status") == "rejected", 1).otherwise(0)).alias("payment_rejection_count")
    )
)

# COMMAND ----------

gold_claim_fraud_features = (
    silver_claims
    .join(silver_policies, "policy_id", "left")
    .join(silver_customers, "customer_id", "left")
    .join(payments_by_claim, "claim_id", "left")
    .join(silver_fraud, "claim_id", "left")
    .withColumn(
        "claim_amount_to_coverage_ratio",
        F.when(
            (F.col("coverage_amount").isNull()) | (F.col("coverage_amount") == 0),
            None
        ).otherwise(F.col("claim_amount") / F.col("coverage_amount"))
    )
    .withColumn(
        "policy_age_days",
        F.greatest(F.datediff(F.col("claim_date"), F.col("start_date")), F.lit(0))
    )
    .withColumn(
        "payment_delay_days",
        F.datediff(F.col("first_payment_date"), F.col("claim_date"))
    )
    .fillna(
        {
            "total_paid_amount": 0.0,
            "payment_count": 0,
            "payment_rejection_count": 0,
            "previous_claims_count": 0,
            "suspicious_amount_flag": False,
            "duplicate_claim_flag": False,
            "late_report_flag": False,
            "high_risk_region_flag": False,
            "risk_score": 0
        }
    )
    .withColumn(
        "risk_band",
        F.when(F.col("risk_score") < 30, "low")
         .when(F.col("risk_score") < 70, "medium")
         .otherwise("high")
    )
    .select(
        "claim_id",
        "policy_id",
        "customer_id",
        "claim_date",
        "claim_type",
        "claim_status",
        "claim_amount",
        "policy_type",
        "premium_amount",
        "coverage_amount",
        "claim_amount_to_coverage_ratio",
        "policy_age_days",
        "customer_age",
        "bundesland",
        "total_paid_amount",
        "payment_count",
        "payment_rejection_count",
        "first_payment_date",
        "payment_delay_days",
        "previous_claims_count",
        "suspicious_amount_flag",
        "duplicate_claim_flag",
        "late_report_flag",
        "high_risk_region_flag",
        "risk_score",
        "risk_band",
        "fraud_flag"
    )
    .dropDuplicates(["claim_id"])
)


# COMMAND ----------

gold_claim_fraud_features.write.mode("overwrite").format("delta").option("overwriteSchema", "true").saveAsTable(
    t(GOLD_SCHEMA, "gold_claim_fraud_features")
)

display(gold_claim_fraud_features.limit(20))
