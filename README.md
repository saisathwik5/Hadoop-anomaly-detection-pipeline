# Distributed Data Pipeline with Anomaly Detection on Hadoop

Production-style ELT project for transactional data on Hadoop using HDFS, Hive,
Spark, Airflow, data quality validation, anomaly detection, reconciliation
alerts, and BigQuery-ready exports.

The repo is built to show data engineering discipline: partition-aware schemas,
Parquet/Avro ingestion, referential integrity checks, statistical process
control, SLA-aware orchestration, retry behavior, and CI regression tests.

## Architecture

```text
Transactional Parquet/Avro files
        |
        v
HDFS raw zone
        |
        v
Spark validation job
  - completeness checks
  - type consistency
  - referential integrity
  - partition checks
        |
        v
Hive refined tables
        |
        v
Spark MLlib/statistical anomaly detection
        |
        v
Reconciliation alerts + BigQuery export
```

## Key Features

- HDFS/Hive-style raw, refined, and analytics zones.
- Partition-aware schema validation for transactional datasets.
- Data quality checks for completeness, type consistency, and referential
  integrity.
- Statistical process control anomaly detection using z-score and control-limit
  rules.
- Reconciliation alert payloads for downstream monitoring.
- Airflow DAG with scheduling, dependencies, retries, and SLA threshold comments.
- BigQuery export module with a dry-run mode for local development.
- Docker Compose for Hadoop NameNode/DataNode, Hive Metastore, Postgres, and
  Airflow.
- Pytest suite and GitHub Actions CI.

## Project Structure

```text
hadoop-anomaly-pipeline/
├── anomaly_pipeline/
│   ├── validation.py       # Data quality checks
│   ├── anomaly.py          # Statistical process control
│   ├── reconciliation.py   # Alert generation
│   ├── bigquery_export.py  # Export interface
│   └── spark_jobs.py       # Spark job entrypoint
├── airflow/dags/transaction_anomaly_dag.py
├── hive/ddl.sql
├── sample_data/
├── docker/docker-compose.yml
├── tests/
└── docs/
```

## Quickstart

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pytest tests -v
```

Start local orchestration infrastructure:

```bash
cd docker
docker compose up -d
```

Run the local Spark job against sample data:

```bash
spark-submit anomaly_pipeline/spark_jobs.py \
  --transactions sample_data/transactions.csv \
  --accounts sample_data/accounts.csv \
  --output output
```

## Resume Bullets

- Built a Hadoop ELT pipeline ingesting transactional data into HDFS/Hive with
  partition-aware schema validation and data quality enforcement across pipeline
  stages.
- Implemented anomaly detection with statistical process control in Python and
  Spark-compatible logic, generating reconciliation alerts for high-risk data
  quality violations.
- Orchestrated the pipeline with Apache Airflow using scheduled DAG tasks,
  dependency management, retries, and CI-backed regression tests.

