# 🏁 Final Project Inventory — Insurance Lakehouse

## 📊 Expected Final Object Inventory

### 🟤 Bronze Layer


| Layer        | Object                          | Purpose                     | Exists? | Rows (approx) |
|--------------|--------------------------------|----------------------------|--------|---------------|
| Bronze       | bronze_claims                  | Raw ingested claims        | yes    | 50,000        |
| Bronze       | bronze_policies                | Raw ingested policies      | yes    | 25,000        |
| Bronze       | bronze_customers               | Raw ingested customers     | yes    | 10,000        |
| Bronze       | bronze_payments                | Raw ingested payments      | yes    | 50,000        |
| Bronze       | bronze_agents                  | Raw ingested agents        | yes    | 1,000         |
| Bronze       | bronze_fraud_indicators        | Raw fraud signals          | yes    | 50,000        |

### ⚪ SILVER LAYER INVENTORY


| Object | Purpose | Exists? | Rows (approx) |
|--------|--------|--------|---------------|
| silver_claims | Cleaned claims data | yes | ~50,000 |
| silver_policies | Cleaned policies | yes | ~25,000 |
| silver_customers | Cleaned customers | yes | ~10,000 |
| silver_payments | Cleaned payments | yes | ~50,000 |
| silver_agents | Cleaned agents | yes | ~1,000 |
| silver_fraud_indicators | Cleaned fraud signals | yes | ~50,000 |

### 🟡 Gold Layer

| Object | Purpose | Exists? | Rows (approx) |
|--------|--------|--------|---------------|
| gold_claims_overview | Claims KPIs | yes | ~50,000 |
| gold_policy_performance | Policy analytics | yes | ~25,000+ |
| gold_customer_risk_profile | Customer risk scoring | yes | ~10,000 |
| gold_claims_payment_summary | Payment analysis | yes | ~50,000 |
| gold_fraud_risk_summary | Fraud analytics | yes | aggregated |
| gold_agent_performance | Agent KPIs | yes | ~1,000 |
| gold_claim_fraud_features | AI-ready ML features | yes | ~50,000 |

## 🚨 Quarantine Layer

| Object | Purpose | Exists? | Rows (approx) |
|--------|--------|--------|---------------|
| quarantine_invalid_claims | Invalid claims | yes | low volume |
| quarantine_invalid_policies | Invalid policies | yes | low volume |
| quarantine_invalid_customers | Invalid customers | yes | low volume |
| quarantine_invalid_payments | Invalid payments | yes | low volume |

#### 🧠 Notes

- All Bronze tables store raw ingested data from S3 without transformations.
- Silver layer contains cleaned, validated, and GDPR-compliant data.
- Gold layer provides business-ready analytics, KPIs, and AI-ready features.
- Quarantine tables store invalid or rejected records for data quality tracking.
- Dashboard views are aggregated SQL layers used for BI tools like Databricks SQL.
- Row counts are based on synthetic dataset generated in Day 1 notebook.
- Gold tables are derived from Silver transformations using joins and aggregations.