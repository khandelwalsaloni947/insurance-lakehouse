CREATE OR REPLACE VIEW insurance_lakehouse.gold.vw_executive_insurance_overview AS
SELECT
    SUM(active_policies) AS total_active_policies,
    SUM(total_policies) AS total_policies,
    ROUND(SUM(premium_revenue), 2) AS total_premium_revenue
FROM insurance_lakehouse.gold.gold_policy_performance;
