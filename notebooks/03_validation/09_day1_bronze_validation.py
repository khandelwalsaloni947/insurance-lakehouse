# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "1"
# ///
# MAGIC %md
# MAGIC # 09 — Day 1 Bronze Validation

# COMMAND ----------

from pyspark.sql import functions as F

S3_BUCKET = "s3a://insurance-lakehouse-project-saumya/"
RAW_BASE_PATH = f"{S3_BUCKET}/raw"
CATALOG_NAME = "insurance_lakehouse"
BRONZE_SCHEMA = "bronze"

datasets = ["customers", "policies", "claims", "payments", "agents", "fraud_indicators"]

results = []
for dataset in datasets:
    raw_path = f"{RAW_BASE_PATH}/{dataset}"
    bronze_table = f"{CATALOG_NAME}.{BRONZE_SCHEMA}.bronze_{dataset}"
    raw_count = spark.read.option("header", True).csv(raw_path).count()
    bronze_count = spark.table(bronze_table).count()
    status = "PASS" if raw_count == bronze_count else "FAIL"
    results.append((dataset, raw_count, bronze_count, status))

validation_df = spark.createDataFrame(results, ["dataset", "raw_count", "bronze_count", "status"])
display(validation_df)

metadata_results = []
for dataset in datasets:
    bronze_table = f"{CATALOG_NAME}.{BRONZE_SCHEMA}.bronze_{dataset}"
    columns = spark.table(bronze_table).columns
    metadata_results.append((
        dataset,
        "ingest_timestamp" in columns,
        "ingest_run_id" in columns,
        "source_file_name" in columns
    ))

metadata_df = spark.createDataFrame(metadata_results, ["dataset", "has_ingest_timestamp", "has_ingest_run_id", "has_source_file_name"])
display(metadata_df)

validation_df.withColumn("validation_timestamp", F.current_timestamp()).write.format("delta").mode("overwrite").saveAsTable(
    f"{CATALOG_NAME}.{BRONZE_SCHEMA}.day1_bronze_validation_summary"
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN insurance_lakehouse.bronze
