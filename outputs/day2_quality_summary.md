# Day 2 — Data Quality Summary

## Overview

This report summarizes Bronze, Silver, and Quarantine data quality results for the Insurance Lakehouse pipeline.

---

## 📊 Dataset Quality Table

| Dataset | Bronze Rows | Silver Rows | Quarantine Rows | Status |
|---|---:|---:|---:|---|
| Customers | 10000 | 10000 | 0 | ✅ Clean |
| Policies | 25000 | 25000 | 0 | ✅ Clean |
| Claims | 50000 | 50000 | 0 | ✅ Clean |
| Payments | 50000 | 18354 | 31646 | ⚠️ Needs Review |
| Agents | 1000 | 1000 | 0 | ✅ Clean |
| Fraud Indicators | 50000 | 31531 | 0 | ⚠️ Partially Clean |

---

## 🔍 Key Observations

- Customers, Policies, Claims are fully clean
- Payments have highest rejection due to:
  - invalid claim references
  - payment date rules
  - negative/invalid amounts
- Fraud indicators mostly valid but need stricter risk validation

---

## 🚀 Final Status

👉 Data is **READY for Day 3 Gold Layer**, but:
- Payment rules should be improved
- Fraud scoring needs calibration