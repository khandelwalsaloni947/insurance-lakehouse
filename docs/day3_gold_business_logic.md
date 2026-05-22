#  Gold Layer Design (Insurance Lakehouse)

## 🎯 Purpose

This document defines the business logic for Gold layer tables in the Insurance Lakehouse project for **Rheinland Versicherung AG**.

Gold layer transforms trusted Silver data into business-ready analytics, KPIs, and AI-ready datasets for dashboards and machine learning.

---

#  1. gold_claims_overview

## Purpose
Provides executive-level overview of insurance claims performance across time, status, product type, and region.

---

## Grain
```text
1 row per (month + claim_status + claim_type + policy_type + bundesland)