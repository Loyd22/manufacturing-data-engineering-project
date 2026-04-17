SELECT 'missing_inspection_id' AS check_name, COUNT(*) AS issue_count
FROM staging.stg_quality_inspections
WHERE inspection_id IS NULL

UNION ALL

SELECT 'negative_defect_count' AS check_name, COUNT(*) AS issue_count
FROM staging.stg_quality_inspections
WHERE defect_count < 0

UNION ALL

SELECT 'negative_inspected_units' AS check_name, COUNT(*) AS issue_count
FROM staging.stg_quality_inspections
WHERE inspected_units < 0

UNION ALL

SELECT 'defect_greater_than_inspected' AS check_name, COUNT(*) AS issue_count
FROM staging.stg_quality_inspections
WHERE defect_count > inspected_units

UNION ALL

SELECT 'duplicate_inspection_id' AS check_name, COUNT(*) AS issue_count
FROM (
    SELECT inspection_id
    FROM staging.stg_quality_inspections
    WHERE inspection_id IS NOT NULL
    GROUP BY inspection_id
    HAVING COUNT(*) > 1
) dup;