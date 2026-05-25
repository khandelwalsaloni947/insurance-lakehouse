SELECT 'vw_executive_insurance_overview' AS view_name, COUNT(*) AS row_count FROM insurance_lakehouse.gold.vw_executive_insurance_overview
UNION ALL SELECT 'vw_claims_operations', COUNT(*) FROM insurance_lakehouse.gold.vw_claims_operations
UNION ALL SELECT 'vw_policy_portfolio', COUNT(*) FROM insurance_lakehouse.gold.vw_policy_portfolio
UNION ALL SELECT 'vw_fraud_risk_monitoring', COUNT(*) FROM insurance_lakehouse.gold.vw_fraud_risk_monitoring
UNION ALL SELECT 'vw_agent_regional_performance', COUNT(*) FROM insurance_lakehouse.gold.vw_agent_regional_performance
UNION ALL SELECT 'vw_data_quality_monitoring', COUNT(*) FROM insurance_lakehouse.gold.vw_data_quality_monitoring;
