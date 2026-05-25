CREATE OR REPLACE VIEW insurance_lakehouse.gold.vw_consent_customer_analytics AS
SELECT *
FROM insurance_lakehouse.gold.gold_customer_risk_profile
WHERE gdpr_consent = true;
