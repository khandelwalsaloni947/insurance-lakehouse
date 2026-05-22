# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "1"
# ///
# MAGIC %md
# MAGIC # 18 — Gold Claims Payment Summary
# MAGIC
# MAGIC Week 11 Day 3 — Gold Analytics, Insurance KPIs, AI-Ready Features, and Performance.
# MAGIC
# MAGIC Replace catalog/schema names if your environment uses different names.
# MAGIC
# MAGIC ##Purpose
# MAGIC This table provides a claim-level financial summary combining:
# MAGIC - claim details
# MAGIC - policy context
# MAGIC - payment behavior
# MAGIC
# MAGIC It is used to analyze settlement efficiency, payment delays, and payout ratios.

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
silver_payments = spark.table(t(SILVER_SCHEMA, "silver_payments"))
silver_policies = spark.table(t(SILVER_SCHEMA, "silver_policies"))


payments_by_claim = (
    silver_payments
    .groupBy("claim_id")
    .agg(
        F.count("*").alias("payment_count"),

        F.round(
            F.sum("payment_amount"),
            2
        ).alias("total_paid_amount"),

        F.sum(
            F.when(
                F.col("payment_status") == "rejected",
                1
            ).otherwise(0)
        ).alias("rejected_payment_count"),

        F.min("payment_date").alias("first_payment_date")
    )
)

# ---------------------------------------------
# Join Claims + Policies + Payments
# ---------------------------------------------
base_df = (
    silver_claims

    .join(
        silver_policies.select(
            "policy_id",
            "policy_type",
            "premium_amount",
            "coverage_amount"
        ),
        on="policy_id",
        how="left"
    )

    .join(
        payments_by_claim,
        on="claim_id",
        how="left"
    )
)

# ---------------------------------------------
# Gold Feature Engineering
# ---------------------------------------------
gold_claims_payment_summary = (

    base_df

    # Null-safe payment metrics
    .withColumn(
        "payment_count",
        F.coalesce(F.col("payment_count"), F.lit(0))
    )

    .withColumn(
        "total_paid_amount",
        F.coalesce(F.col("total_paid_amount"), F.lit(0.0))
    )

    .withColumn(
        "rejected_payment_count",
        F.coalesce(F.col("rejected_payment_count"), F.lit(0))
    )

    # Payment delay calculation
    .withColumn(
        "payment_delay_days",
        F.when(
            F.col("first_payment_date").isNull(),
            F.lit(None)
        ).otherwise(
            F.datediff(
                F.col("first_payment_date"),
                F.col("claim_date")
            )
        )
    )

    # Safe financial ratio
    .withColumn(
        "claim_to_payment_ratio",
        F.when(
            F.col("claim_amount") == 0,
            F.lit(None)
        ).otherwise(
            F.round(
                F.col("total_paid_amount") /
                F.col("claim_amount"),
                4
            )
        )
    )

    # Settlement classification
    .withColumn(
        "settlement_status",
        F.when(
            F.col("payment_count") > 0,
            F.lit("PAID")
        ).otherwise(
            F.lit("UNPAID")
        )
    )

)

# ---------------------------------------------
# Write Gold Delta Table
# ---------------------------------------------
spark.sql(f"""
DROP TABLE IF EXISTS {CATALOG}.{GOLD_SCHEMA}.gold_claims_payment_summary
""")

gold_claims_payment_summary.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable(
        t(GOLD_SCHEMA, "gold_claims_payment_summary")
    )

# ---------------------------------------------
# Validation
# ---------------------------------------------
print("Gold table created successfully")

print("Total rows:")
print(gold_claims_payment_summary.count())

print("Settlement Status Distribution:")
display(
    gold_claims_payment_summary.groupBy("settlement_status").count()
)

# ---------------------------------------------
# Preview Output
# ---------------------------------------------
display(
    gold_claims_payment_summary.limit(20)
)

# COMMAND ----------

spark.sql(f"DROP TABLE IF EXISTS {GOLD_SCHEMA}.gold_claims_payment_summary")

# COMMAND ----------

silver_payments.count()


# COMMAND ----------

silver_payments.select("claim_id").distinct().count()


# COMMAND ----------

silver_claims.select("claim_id").count()
