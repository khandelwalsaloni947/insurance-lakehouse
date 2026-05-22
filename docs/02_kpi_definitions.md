#  KPI Definitions (Gold Layer)

##  Purpose

This document defines all business KPIs used in the Gold layer of the Insurance Lakehouse project for **Rheinland Versicherung AG**.

Each KPI includes:
- Business meaning
- Formula
- Input Silver tables
- Data quality risks

This ensures transparency, consistency, and auditability across all analytics outputs.

---

# 👥 Customer KPIs

---

## total_customers

### Business Meaning
Total number of unique customers in the insurance system.

### Formula
COUNT(DISTINCT customer_id)

### Input Tables
- silver_customers

### Data Quality Risks
- Duplicate customer records
- Missing customer_id

---

# 📑 Policy KPIs

---

## total_policies

### Business Meaning
Total number of insurance policies issued.

### Formula
COUNT(DISTINCT policy_id)

### Input Tables
- silver_policies

### Data Quality Risks
- Duplicate policies due to ingestion retries
- Invalid policy IDs

---

## active_policies

### Business Meaning
Number of currently active insurance policies.

### Formula
COUNT(policy_id WHERE policy_status = 'active')

### Input Tables
- silver_policies

### Data Quality Risks
- Incorrect status values (typos, inconsistent casing)
- Missing policy_status

---

## premium_revenue

### Business Meaning
Total revenue generated from insurance premiums.

### Formula
SUM(premium_amount)

### Input Tables
- silver_policies

### Data Quality Risks
- Negative or zero premium values
- Currency inconsistencies

---

## estimated_commission

### Business Meaning
Estimated earnings for agents based on policy premiums.

### Formula
SUM(premium_amount * commission_rate)

### Input Tables
- silver_policies
- silver_agents

### Data Quality Risks
- Missing commission_rate
- Incorrect agent-policy mapping

---

# 🚨 Claims KPIs

---

## total_claims

### Business Meaning
Total number of insurance claims filed.

### Formula
COUNT(claim_id)

### Input Tables
- silver_claims

### Data Quality Risks
- Duplicate claim entries
- Missing claim_id

---

## open_claims

### Business Meaning
Claims currently under processing.

### Formula
COUNT(claim_id WHERE claim_status = 'open')

### Input Tables
- silver_claims

### Data Quality Risks
- Invalid claim_status values
- Status not updated in time

---

## approved_claims

### Business Meaning
Claims approved for payout.

### Formula
COUNT(claim_id WHERE claim_status = 'approved')

### Input Tables
- silver_claims

### Data Quality Risks
- Delayed status updates
- Incorrect approvals due to bad data

---

## rejected_claims

### Business Meaning
Claims rejected after validation or fraud checks.

### Formula
COUNT(claim_id WHERE claim_status = 'rejected')

### Input Tables
- silver_claims

### Data Quality Risks
- Misclassification of claim status
- Missing rejection reason

---

## paid_claims

### Business Meaning
Claims fully settled and paid.

### Formula
COUNT(claim_id WHERE claim_status = 'paid')

### Input Tables
- silver_claims

### Data Quality Risks
- Payment not reflected in status
- Partial payments not tracked

---

## total_claim_amount

### Business Meaning
Total financial exposure from insurance claims.

### Formula
SUM(claim_amount)

### Input Tables
- silver_claims

### Data Quality Risks
- Negative claim amounts
- Duplicate claims inflating totals

---

## average_claim_amount

### Business Meaning
Average claim size across all claims.

### Formula
AVG(claim_amount)

### Input Tables
- silver_claims

### Data Quality Risks
- Outliers skewing average
- Missing claim amounts

---

# 💰 Payment KPIs

---

## total_paid_amount

### Business Meaning
Total money paid out for insurance claims.

### Formula
SUM(payment_amount WHERE payment_status = 'paid')

### Input Tables
- silver_payments

### Data Quality Risks
- Missing payment_status
- Duplicate payment records
- Partial payments not reconciled

---

## payment_rejection_rate

### Business Meaning
Percentage of rejected payments.

### Formula
COUNT(rejected payments) / COUNT(all payments)

### Input Tables
- silver_payments

### Data Quality Risks
- Incorrect payment status values
- Missing payment records

---

## average_payment_delay_days

### Business Meaning
Average time taken to process claim payments.

### Formula
AVG(payment_date - claim_date)

### Input Tables
- silver_claims
- silver_payments

### Data Quality Risks
- Missing dates
- Negative delays due to bad timestamps

---

# ⚠️ Fraud & Risk KPIs

---

## fraud_risk_rate

### Business Meaning
Proportion of claims flagged as potentially fraudulent.

### Formula
COUNT(fraud_flag = true) / COUNT(all claims)

### Input Tables
- silver_claims

### Data Quality Risks
- Incorrect fraud_flag assignment
- Bias in fraud detection rules

---

## average_risk_score

### Business Meaning
Average risk score of claims based on fraud indicators.

### Formula
AVG(risk_score)

### Input Tables
- silver_fraud_indicators

### Data Quality Risks
- Missing risk scores
- Improper scoring distribution

---

# 📉 Business Ratio KPIs

---

## claims_ratio

### Business Meaning
Measures insurance profitability and risk exposure.

### Formula
SUM(claim_amount) / SUM(premium_amount)

### Input Tables
- silver_claims
- silver_policies

### Data Quality Risks
- Mismatched joins between claims and policies
- Inflation due to duplicate records

---

# 🧠 FINAL NOTES

- Every KPI must be traceable to Silver layer
- No KPI should mix inconsistent grains
- All formulas must be validated before Gold aggregation
- Data quality risks must be documented for audit and governance

---

# 🚀 OUTCOME

This KPI layer enables:
- Executive dashboards
- Financial reporting
- Fraud monitoring
- Risk analytics
- AI/ML feature engineering