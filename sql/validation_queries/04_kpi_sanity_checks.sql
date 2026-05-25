SELECT COUNT(*) AS negative_premium_rows
FROM insurance_lakehouse.gold.gold_policy_performance
WHERE premium_revenue < 0;

SELECT COUNT(*) AS invalid_risk_score_rows
FROM insurance_lakehouse.gold.gold_claim_fraud_features
WHERE risk_score < 0 OR risk_score > 100;
