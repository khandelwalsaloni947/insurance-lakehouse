# Databricks notebook source

# MAGIC %md
# MAGIC # 28 — Final Project Documentation
# MAGIC Use this notebook as a checklist for your final README and documentation files.

# COMMAND ----------

required_docs = [
    "README.md",
    "docs/data_dictionary.md",
    "docs/kpi_definitions.md",
    "docs/data_quality_report.md",
    "docs/gdpr_governance_design.md",
    "docs/performance_notes.md",
    "docs/final_project_summary.md",
    "architecture/lakehouse_architecture.md",
    "architecture/s3_folder_design.md"
]
for doc in required_docs:
    print("[ ]", doc)

