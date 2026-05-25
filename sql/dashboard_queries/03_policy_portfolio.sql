CREATE OR REPLACE VIEW insurance_lakehouse.gold.vw_policy_portfolio AS
SELECT
    policy_type,
    policy_status,
    sales_channel,
    bundesland,
    SUM(total_policies) AS total_policies,
    SUM(active_policies) AS active_policies,
    SUM(cancelled_policies) AS cancelled_policies,
    ROUND(SUM(premium_revenue), 2) AS premium_revenue
FROM insurance_lakehouse.gold.gold_policy_performance
GROUP BY policy_type, policy_status, sales_channel, bundesland;
