# Day 1 Setup Notes

## Databricks Trial Setup

Successfully opened the Databricks trial environment using the AWS option.

Preferred setup approach:

* AWS Marketplace / existing AWS account integration

Verified access to:

* Workspace
* Compute
* SQL Editor
* Workflows
* Catalog Explorer

---

## AWS Environment Preparation

Prepared AWS environment for the insurance lakehouse project.

Planned S3 bucket structure:

```text
raw/
bronze/
silver/
gold/
checkpoints/
quarantine/
```

---

## Cost-Control Review

Reviewed cloud cost-management responsibilities before starting the project.

Cost-control actions:

* Use only one S3 bucket
* Start with small data mode only
* Use small or medium compute clusters
* Stop compute clusters when not in use
* Avoid leaving clusters running overnight
* Monitor AWS billing dashboard
* Review AWS budget alerts
* Avoid unnecessary long-running jobs

---

## Security Practices

Security rules acknowledged:

* Never hardcode AWS credentials in notebooks
* Avoid committing secrets to GitHub
* Use secure authentication methods where possible

---

## Day 1 Readiness Status

Environment readiness confirmed for:

* Databricks notebooks
* AWS S3 integration
* Delta Lake ingestion
* PySpark data generation
* Bronze layer implementation

