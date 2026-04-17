CREATE TABLE IF NOT EXISTS warehouse.dim_machine (
    machine_key SERIAL PRIMARY KEY,
    machine_id VARCHAR(20) UNIQUE,
    machine_name VARCHAR(100),
    machine_type VARCHAR(100),
    production_line VARCHAR(100),
    is_active BOOLEAN
);

TRUNCATE TABLE warehouse.dim_machine RESTART IDENTITY;

INSERT INTO warehouse.dim_machine (
    machine_id,
    machine_name,
    machine_type,
    production_line,
    is_active
)
SELECT DISTINCT
    machine_id,
    'Machine ' || machine_id AS machine_name,
    'General Machine' AS machine_type,
    'Main Line' AS production_line,
    TRUE AS is_active
FROM (
    SELECT machine_id FROM staging.stg_production_orders
    UNION
    SELECT machine_id FROM staging.stg_machine_logs
) m
WHERE machine_id IS NOT NULL; 