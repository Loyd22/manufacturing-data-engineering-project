SELECT 'missing_product_key_in_fact_production' AS check_name, COUNT(*) AS issue_count
FROM warehouse.fact_production
WHERE product_key IS NULL

UNION ALL

SELECT 'missing_machine_key_in_fact_production' AS check_name, COUNT(*) AS issue_count
FROM warehouse.fact_production
WHERE machine_key IS NULL

UNION ALL

SELECT 'missing_supplier_key_in_fact_production' AS check_name, COUNT(*) AS issue_count
FROM warehouse.fact_production
WHERE supplier_key IS NULL

UNION ALL

SELECT 'negative_quantity_planned_in_fact' AS check_name, COUNT(*) AS issue_count
FROM warehouse.fact_production
WHERE quantity_planned < 0

UNION ALL

SELECT 'negative_quantity_produced_in_fact' AS check_name, COUNT(*) AS issue_count
FROM warehouse.fact_production
WHERE quantity_produced < 0;