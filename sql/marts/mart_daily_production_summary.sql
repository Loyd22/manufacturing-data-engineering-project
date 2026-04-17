CREATE TABLE IF NOT EXISTS marts.mart_daily_production_summary (
    production_date DATE,
    total_orders INT,
    total_quantity_planned BIGINT,
    total_quantity_produced BIGINT,
    production_efficiency NUMERIC(10,4)
);

TRUNCATE TABLE marts.mart_daily_production_summary;

INSERT INTO marts.mart_daily_production_summary (
    production_date,
    total_orders,
    total_quantity_planned,
    total_quantity_produced,
    production_efficiency
)
SELECT
    d.full_date AS production_date,
    COUNT(f.production_order_id)::INT AS total_orders,
    COALESCE(SUM(f.quantity_planned), 0) AS total_quantity_planned,
    COALESCE(SUM(f.quantity_produced), 0) AS total_quantity_produced,
    CASE
        WHEN COALESCE(SUM(f.quantity_planned), 0) = 0 THEN 0
        ELSE ROUND(SUM(f.quantity_produced)::NUMERIC / SUM(f.quantity_planned)::NUMERIC, 4)
    END AS production_efficiency
FROM warehouse.fact_production f
LEFT JOIN warehouse.dim_date d
    ON f.date_key = d.date_key
GROUP BY d.full_date
ORDER BY d.full_date;