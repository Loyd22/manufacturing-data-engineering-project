CREATE TABLE IF NOT EXISTS marts.mart_quality_trends (
    inspection_date DATE,
    product_id VARCHAR(20),
    total_defects BIGINT,
    total_inspected_units BIGINT,
    defect_rate NUMERIC(10,4)
);

TRUNCATE TABLE marts.mart_quality_trends;

INSERT INTO marts.mart_quality_trends (
    inspection_date,
    product_id,
    total_defects,
    total_inspected_units,
    defect_rate
)
SELECT
    d.full_date AS inspection_date,
    dp.product_id,
    COALESCE(SUM(f.defect_count), 0) AS total_defects,
    COALESCE(SUM(f.inspected_units), 0) AS total_inspected_units,
    CASE
        WHEN COALESCE(SUM(f.inspected_units), 0) = 0 THEN 0
        ELSE ROUND(SUM(f.defect_count)::NUMERIC / SUM(f.inspected_units)::NUMERIC, 4)
    END AS defect_rate
FROM warehouse.fact_quality f
LEFT JOIN warehouse.dim_date d
    ON f.date_key = d.date_key
LEFT JOIN warehouse.dim_product dp
    ON f.product_key = dp.product_key
GROUP BY d.full_date, dp.product_id
ORDER BY d.full_date, dp.product_id;