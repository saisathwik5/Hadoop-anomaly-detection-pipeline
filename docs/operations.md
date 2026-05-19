# Operations Notes

## Data Quality

- Completeness checks protect required transaction keys and measures.
- Type consistency checks prevent silent schema drift from reaching Hive.
- Referential integrity checks catch orphaned transaction account IDs.
- Partition checks ensure data lands under query-friendly date partitions.

## Anomaly Detection

- Z-score rules identify unusual daily account totals relative to the batch.
- Control-limit rules support business-defined thresholds for known risk bands.
- Alerts include severity, failed count, metric value, score, and created time.

## Airflow

- Retries are configured at the DAG level.
- Each task is isolated: ingest, Spark processing, Hive repair, export manifest.
- SLA thresholds can be added on task definitions when deployed to a managed
  Airflow environment.

## BigQuery

- The local repo writes dry-run manifests.
- In production, replace the manifest step with a BigQuery load job from GCS.
