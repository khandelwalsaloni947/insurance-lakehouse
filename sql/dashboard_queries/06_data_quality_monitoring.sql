CREATE OR REPLACE VIEW insurance_lakehouse.gold.vw_data_quality_monitoring AS
SELECT 'customers' AS dataset, COUNT(*) AS quarantine_count
FROM insurance_lakehouse.quarantine.quarantine_invalid_customers
UNION ALL
SELECT 'policies', COUNT(*) FROM insurance_lakehouse.quarantine.quarantine_invalid_policies
UNION ALL
SELECT 'claims', COUNT(*) FROM insurance_lakehouse.quarantine.quarantine_invalid_claims
UNION ALL
SELECT 'payments', COUNT(*) FROM insurance_lakehouse.quarantine.quarantine_invalid_payments;
