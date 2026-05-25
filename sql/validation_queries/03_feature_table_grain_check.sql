SELECT claim_id, COUNT(*) AS row_count
FROM insurance_lakehouse.gold.gold_claim_fraud_features
GROUP BY claim_id
HAVING COUNT(*) > 1;
