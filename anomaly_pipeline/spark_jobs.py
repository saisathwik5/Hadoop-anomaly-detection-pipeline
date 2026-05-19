"""Spark entrypoint for validation, anomaly scoring, and curated outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def create_spark() -> SparkSession:
    return (
        SparkSession.builder.appName("hadoop-anomaly-pipeline")
        .enableHiveSupport()
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .getOrCreate()
    )


def run_job(transactions_path: str, accounts_path: str, output_path: str) -> None:
    spark = create_spark()
    transactions = (
        spark.read.option("header", True).option("inferSchema", True).csv(transactions_path)
    )
    accounts = spark.read.option("header", True).option("inferSchema", True).csv(accounts_path)

    refined = (
        transactions.join(
            accounts.select("account_id", "customer_id", "region"), "account_id", "left"
        )
        .withColumn("txn_date", F.to_date("txn_ts"))
        .withColumn("amount", F.col("amount").cast("double"))
        .withColumn(
            "dq_status",
            F.when(F.col("transaction_id").isNull(), "MISSING_TRANSACTION_ID")
            .when(F.col("account_id").isNull(), "MISSING_ACCOUNT_ID")
            .when(F.col("customer_id").isNull(), "REFERENTIAL_INTEGRITY_FAILURE")
            .when(F.col("amount").isNull(), "INVALID_AMOUNT")
            .otherwise("VALID"),
        )
    )

    daily_metrics = (
        refined.filter(F.col("dq_status") == "VALID")
        .groupBy("txn_date", "account_id")
        .agg(
            F.count("*").alias("transaction_count"),
            F.round(F.sum("amount"), 2).alias("total_amount"),
            F.round(F.avg("amount"), 2).alias("avg_amount"),
        )
    )

    stats = daily_metrics.agg(
        F.avg("total_amount").alias("mean_total"),
        F.stddev_pop("total_amount").alias("std_total"),
    ).first()
    mean_total = stats["mean_total"] or 0.0
    std_total = stats["std_total"] or 0.0

    scored = daily_metrics.withColumn(
        "z_score",
        F.when(F.lit(std_total) == 0, F.lit(0.0)).otherwise(
            F.abs((F.col("total_amount") - F.lit(mean_total)) / F.lit(std_total))
        ),
    ).withColumn("is_anomaly", F.col("z_score") >= 3.0)

    output = Path(output_path)
    refined.write.mode("overwrite").partitionBy("txn_date").parquet(
        str(output / "refined_transactions")
    )
    scored.write.mode("overwrite").parquet(str(output / "daily_anomaly_scores"))
    spark.stop()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Hadoop anomaly Spark job.")
    parser.add_argument("--transactions", required=True)
    parser.add_argument("--accounts", required=True)
    parser.add_argument("--output", default="output")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_job(args.transactions, args.accounts, args.output)
