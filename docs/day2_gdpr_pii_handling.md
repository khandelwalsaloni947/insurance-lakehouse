# Day 2 — GDPR and PII Handling

## 1. Overview

This document explains how GDPR-sensitive customer data and PII (Personally Identifiable Information) were handled in the Insurance Lakehouse project.

The goal is to protect customer privacy while still enabling analytics and reporting.

---

## 2. PII Fields Identified

The following fields are considered direct or sensitive PII:

| Dataset | PII Fields |
|---|---|
| Customers | first_name, last_name, email, phone_number, street |
| Policies | customer_id |
| Claims | customer_id |
| Payments | iban_hash |
| Agents | agent_name |

---

## 3. Fields Hashed in Silver Layer

The following fields were hashed for privacy protection:

| Original Field | Hashed Field |
|---|---|
| email | email_hash |
| phone_number | phone_hash |
| customer_id | customer_hash |

Hashing method used:
- SHA-256

---

## 4. Fields Removed from Silver Layer

The following raw PII fields were removed from Silver tables:

| Removed Fields |
|---|
| email |
| phone_number |
| street |

Reason:
- reduce exposure of direct customer identifiers
- improve GDPR compliance

---

## 5. Fields Restricted from Gold Dashboards

The following fields should NOT appear in Gold dashboards or BI reports:

| Restricted Fields |
|---|
| first_name |
| last_name |
| email |
| phone_number |
| street |
| iban_hash |

Gold dashboards should use:
- aggregated metrics
- anonymized identifiers
- regional summaries

---

## 6. GDPR Consent Handling

The `gdpr_consent` field must be respected during analytics and downstream usage.

Rules:
- customers without consent should not be used for personalized analytics
- marketing use requires consent
- AI training datasets should exclude non-consented customer records

---

## 7. Access Control Recommendations

### Raw PII Access

Only these roles should access raw PII:

- Data Engineers
- Security Administrators
- Compliance Officers

---

### Anonymized / Aggregated Access

The following roles should only access anonymized or aggregated data:

- BI Analysts
- Business Users
- Data Scientists
- External Reporting Teams

---

## 8. Final GDPR Assessment

The Silver layer applies:
- hashing
- PII removal
- GDPR-aware filtering
- restricted exposure of customer identifiers

The dataset is suitable for analytics while reducing direct exposure of sensitive customer information.