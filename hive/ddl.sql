CREATE DATABASE IF NOT EXISTS anomaly_pipeline;

CREATE EXTERNAL TABLE IF NOT EXISTS anomaly_pipeline.refined_transactions (
    transaction_id STRING,
    account_id STRING,
    txn_ts TIMESTAMP,
    amount DOUBLE,
    currency STRING,
    merchant_category STRING,
    customer_id STRING,
    region STRING,
    dq_status STRING
)
PARTITIONED BY (txn_date DATE)
STORED AS PARQUET
LOCATION '/warehouse/anomaly_pipeline/refined_transactions';

CREATE EXTERNAL TABLE IF NOT EXISTS anomaly_pipeline.daily_anomaly_scores (
    txn_date DATE,
    account_id STRING,
    transaction_count BIGINT,
    total_amount DOUBLE,
    avg_amount DOUBLE,
    z_score DOUBLE,
    is_anomaly BOOLEAN
)
STORED AS PARQUET
LOCATION '/warehouse/anomaly_pipeline/daily_anomaly_scores';

CREATE EXTERNAL TABLE IF NOT EXISTS anomaly_pipeline.reconciliation_alerts (
    alert_type STRING,
    severity STRING,
    check_name STRING,
    entity_id STRING,
    metric_name STRING,
    metric_value DOUBLE,
    score DOUBLE,
    details STRING,
    created_at TIMESTAMP
)
STORED AS PARQUET
LOCATION '/warehouse/anomaly_pipeline/reconciliation_alerts';
