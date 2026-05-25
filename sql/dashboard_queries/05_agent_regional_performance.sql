CREATE OR REPLACE VIEW insurance_lakehouse.gold.vw_agent_regional_performance AS
SELECT
    agent_id,
    agent_name,
    region,
    bundesland,
    SUM(total_policies_sold) AS total_policies_sold,
    ROUND(SUM(premium_revenue), 2) AS premium_revenue,
    ROUND(SUM(total_claim_amount), 2) AS total_claim_amount,
    ROUND(SUM(total_claim_amount) / NULLIF(SUM(premium_revenue), 0), 4) AS claims_ratio
FROM insurance_lakehouse.gold.gold_agent_performance
GROUP BY agent_id, agent_name, region, bundesland;
