CREATE TABLE IF NOT EXISTS warehouse.fact_machine_logs (
    machine_log_key SERIAL PRIMARY KEY,
    machine_log_id VARCHAR(20),
    date_key INT,
    machine_key INT,
    uptime_minutes INT,
    downtime_minutes INT,
    downtime_reason VARCHAR(100)
);

TRUNCATE TABLE warehouse.fact_machine_logs RESTART IDENTITY;

INSERT INTO warehouse.fact_machine_logs (
    machine_log_id,
    date_key,
    machine_key,
    uptime_minutes,
    downtime_minutes,
    downtime_reason
)
SELECT
    m.machine_log_id,
    CAST(TO_CHAR(m.log_date, 'YYYYMMDD') AS INT) AS date_key,
    dm.machine_key,
    m.uptime_minutes,
    m.downtime_minutes,
    m.downtime_reason
FROM staging.stg_machine_logs m
LEFT JOIN warehouse.dim_machine dm
    ON m.machine_id = dm.machine_id
WHERE m.machine_log_id IS NOT NULL;