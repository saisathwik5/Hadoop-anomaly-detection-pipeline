from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


DEFAULT_ARGS = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="transaction_anomaly_pipeline",
    default_args=DEFAULT_ARGS,
    description="Validate Hadoop transaction data and publish anomaly alerts.",
    start_date=datetime(2025, 2, 1),
    schedule="@daily",
    catchup=False,
    tags=["hadoop", "spark", "data-quality", "anomaly-detection"],
) as dag:
    ingest_to_hdfs = BashOperator(
        task_id="ingest_to_hdfs",
        bash_command=(
            "hdfs dfs -mkdir -p /data/raw/transactions/{{ ds }} && "
            "hdfs dfs -put -f /opt/airflow/data/transactions.csv "
            "/data/raw/transactions/{{ ds }}/"
        ),
    )

    run_spark_validation = BashOperator(
        task_id="run_spark_validation_and_anomaly_detection",
        bash_command=(
            "spark-submit /opt/airflow/jobs/spark_jobs.py "
            "--transactions /data/raw/transactions/{{ ds }}/transactions.csv "
            "--accounts /data/reference/accounts.csv "
            "--output /warehouse/anomaly_pipeline/{{ ds }}"
        ),
    )

    repair_hive_partitions = BashOperator(
        task_id="repair_hive_partitions",
        bash_command="hive -e 'MSCK REPAIR TABLE anomaly_pipeline.refined_transactions'",
    )

    export_bigquery_manifest = BashOperator(
        task_id="export_bigquery_manifest",
        bash_command=(
            "python /opt/airflow/jobs/export_manifest.py "
            "--table analytics.daily_anomaly_scores "
            "--source-uri gs://example-bucket/anomaly_pipeline/{{ ds }}/*.parquet"
        ),
    )

    ingest_to_hdfs >> run_spark_validation >> repair_hive_partitions >> export_bigquery_manifest
