CREATE TABLE IF NOT EXISTS marts.mart_machine_downtime (
    log_date DATE,
    machine_id VARCHAR(20),
    total_uptime_minutes BIGINT,
    total_downtime_minutes BIGINT,
    downtime_percentage NUMERIC(10,4)
);

TRUNCATE TABLE marts.mart_machine_downtime;

INSERT INTO marts.mart_machine_downtime (
    log_date,
    machine_id,
    total_uptime_minutes,
    total_downtime_minutes,
    downtime_percentage
)
SELECT
    d.full_date AS log_date,
    dm.machine_id,
    COALESCE(SUM(f.uptime_minutes), 0) AS total_uptime_minutes,
    COALESCE(SUM(f.downtime_minutes), 0) AS total_downtime_minutes,
    CASE
        WHEN COALESCE(SUM(f.uptime_minutes + f.downtime_minutes), 0) = 0 THEN 0
        ELSE ROUND(
            SUM(f.downtime_minutes)::NUMERIC /
            SUM(f.uptime_minutes + f.downtime_minutes)::NUMERIC,
            4
        )
    END AS downtime_percentage
FROM warehouse.fact_machine_logs f
LEFT JOIN warehouse.dim_date d
    ON f.date_key = d.date_key
LEFT JOIN warehouse.dim_machine dm
    ON f.machine_key = dm.machine_key
GROUP BY d.full_date, dm.machine_id
ORDER BY d.full_date, dm.machine_id;