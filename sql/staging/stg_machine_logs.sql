CREATE TABLE IF NOT EXISTS staging.stg_machine_logs (
    machine_log_id VARCHAR(20),
    machine_id VARCHAR(20),
    log_date DATE,
    uptime_minutes INT,
    downtime_minutes INT,
    downtime_reason VARCHAR(100)
);