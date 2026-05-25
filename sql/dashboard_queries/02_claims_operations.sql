CREATE OR REPLACE VIEW insurance_lakehouse.gold.vw_claims_operations AS
SELECT
    claim_status,
    claim_type,
    policy_type,
    bundesland,
    SUM(total_claims) AS total_claims,
    ROUND(SUM(total_claim_amount), 2) AS total_claim_amount,
    ROUND(AVG(average_claim_amount), 2) AS average_claim_amount
FROM insurance_lakehouse.gold.gold_claims_overview
GROUP BY claim_status, claim_type, policy_type, bundesland;
