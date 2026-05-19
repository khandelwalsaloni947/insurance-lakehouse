# Day 2 — Data Quality Report

## 1. Pipeline Overview

The pipeline processes insurance data through 3 layers:

- Bronze → Raw ingestion
- Silver → Clean + validated data
- Quarantine → Invalid records

---

## 2. Data Quality Rules Applied

### Customers
- GDPR validation
- Duplicate removal
- Email/phone hashing

### Policies
- FK validation with customers
- Premium > 0 check
- Coverage > Premium

### Claims
- FK validation (policy + customer)
- Positive claim amounts
- Status standardization

### Payments
- Claim existence check
- Payment date >= claim date
- Valid payment methods

### Fraud Indicators
- Claim reference validation
- Risk score range: 0–100

---

## 3. Major Data Issues

### Payments Dataset
- 31,646 records failed validation
- Main reasons:
  - invalid claim references
  - incorrect payment dates
  - invalid amounts

### Fraud Dataset
- Some records missing proper risk calibration

---

## 4. Data Quality Assessment

| Layer | Quality |
|------|--------|
| Bronze | Raw / Unvalidated |
| Silver | Trusted / Cleaned |
| Quarantine | Invalid / Audited |

---

## 5. Final Conclusion

The dataset is **ready for Gold Layer analytics**, but payment validation rules should be refined for production readiness.