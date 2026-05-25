CREATE OR REPLACE VIEW insurance_lakehouse.gold.vw_fraud_risk_monitoring AS
SELECT
    bundesland,
    policy_type,
    claim_type,
    risk_band,
    SUM(total_claims) AS total_claims,
    SUM(high_risk_claims) AS high_risk_claims,
    ROUND(AVG(average_risk_score), 2) AS average_risk_score,
    ROUND(SUM(high_risk_claims) / NULLIF(SUM(total_claims), 0), 4) AS high_risk_rate
FROM insurance_lakehouse.gold.gold_fraud_risk_summary
GROUP BY bundesland, policy_type, claim_type, risk_band;
