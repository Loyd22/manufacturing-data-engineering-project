CREATE TABLE IF NOT EXISTS staging.stg_quality_inspections (
    inspection_id VARCHAR(20),
    production_order_id VARCHAR(20),
    inspection_date DATE,
    defect_count INT,
    inspected_units INT,
    defect_type VARCHAR(100),
    passed BOOLEAN
);