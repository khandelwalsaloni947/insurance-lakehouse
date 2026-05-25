# KPI Definitions (Gold Layer)

## Purpose

This document defines all business KPIs used in the Gold layer of the Insurance Lakehouse project for **Rheinland Versicherung AG**.

Each KPI includes:
- Business meaning
- Formula
- Input Silver tables
- Data quality risks

This ensures transparency, consistency, and auditability across all analytics outputs.

---

# 👥 Customer KPIs

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
COUNT(CASE WHEN policy_status = 'active' THEN 1 END)

### Input Tables
- silver_policies

### Data Quality Risks
- Incorrect status values
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
Estimated earnings for agents.

### Formula
SUM(premium_amount * commission_rate)

### Input Tables
- silver_policies
- silver_agents

### Data Quality Risks
- Missing commission_rate
- Incorrect mapping

---

# 🚨 Claims KPIs

## total_claims

### Business Meaning
Total number of insurance claims filed.

### Formula
COUNT(claim_id)

### Input Tables
- silver_claims

### Data Quality Risks
- Duplicate claims
- Missing claim_id

---

## open_claims

### Business Meaning
Claims currently under processing.

### Formula
COUNT(CASE WHEN claim_status = 'open' THEN 1 END)

### Input Tables
- silver_claims

### Data Quality Risks
- Wrong status values
- Delayed updates

---

## approved_claims

### Business Meaning
Claims approved for payout.

### Formula
COUNT(CASE WHEN claim_status = 'approved' THEN 1 END)

### Input Tables
- silver_claims

### Data Quality Risks
- Late updates
- Wrong approvals

---

## rejected_claims

### Business Meaning
Claims rejected after checks.

### Formula
COUNT(CASE WHEN claim_status = 'rejected' THEN 1 END)

### Input Tables
- silver_claims

### Data Quality Risks
- Wrong classification
- Missing reason

---

## paid_claims

### Business Meaning
Claims fully paid.

### Formula
COUNT(CASE WHEN claim_status = 'paid' THEN 1 END)

### Input Tables
- silver_claims

### Data Quality Risks
- Missing payment updates

---

## total_claim_amount

### Business Meaning
Total claim cost.

### Formula
SUM(claim_amount)

### Input Tables
- silver_claims

### Data Quality Risks
- Negative values
- Duplicates

---

## average_claim_amount

### Business Meaning
Average claim size.

### Formula
AVG(claim_amount)

### Input Tables
- silver_claims

### Data Quality Risks
- Outliers
- Missing values

---

# 💰 Payment KPIs

## total_paid_amount

### Business Meaning
Total paid money.

### Formula
SUM(CASE WHEN payment_status = 'paid' THEN payment_amount ELSE 0 END)

### Input Tables
- silver_payments

### Data Quality Risks
- Missing status
- Duplicate payments

---

## payment_rejection_rate

### Business Meaning
Rejected payment ratio.

### Formula
COUNT(CASE WHEN payment_status = 'rejected' THEN 1 END) / COUNT(*)

### Input Tables
- silver_payments

### Data Quality Risks
- Wrong status values
- Missing records

---

## average_payment_delay_days

### Business Meaning
Average payment delay.

### Formula
AVG(DATEDIFF(payment_date, claim_date))

### Input Tables
- silver_claims
- silver_payments

### Data Quality Risks
- Missing dates
- Negative values

---

# ⚠️ Fraud KPIs

## fraud_risk_rate

### Business Meaning
Fraud probability ratio.

### Formula
COUNT(CASE WHEN fraud_flag = true THEN 1 END) / COUNT(*)

### Input Tables
- silver_claims

### Data Quality Risks
- Wrong fraud labeling
- Bias

---

## average_risk_score

### Business Meaning
Average fraud risk score.

### Formula
AVG(risk_score)

### Input Tables
- silver_fraud_indicators

### Data Quality Risks
- Missing values
- Skewed scores

---

# 📉 Business Ratio KPIs

## claims_ratio

### Business Meaning
Loss ratio of insurance.

### Formula
SUM(claim_amount) / SUM(premium_amount)

### Input Tables
- silver_claims
- silver_policies

### Data Quality Risks
- Join duplication
- Wrong aggregation

---

# 🧠 KPI GOVERNANCE RULE

- Use only Silver data
- No duplicates
- Validate before Gold
- Ensure correct grain

---

# 🚀 RESULT

This KPI layer enables:
- Dashboards
- Fraud detection
- Risk analysis
- AI/ML features