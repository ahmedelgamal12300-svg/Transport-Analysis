from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pandas as pd


def _spark_available() -> bool:
    import shutil

    if not shutil.which("java"):
        return False

    try:
        from pyspark.sql import SparkSession

        spark = (
            SparkSession.builder.appName("transport_probe")
            .master("local[1]")
            .config("spark.ui.enabled", "false")
            .config("spark.ui.showConsoleProgress", "false")
            .getOrCreate()
        )
        spark.stop()
        return True
    except Exception:
        return False


def _engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["speed_kmh"] = (out["trip_distance_km"] / (out["trip_duration_min"] / 60)).round(2)
    out["revenue_per_km"] = (out["total_fare"] / out["trip_distance_km"]).round(2)
    out["is_peak_hour"] = out["pickup_hour"].between(7, 9) | out["pickup_hour"].between(17, 19)
    out["is_peak_hour"] = out["is_peak_hour"].astype(int)
    return out


def _pandas_etl(raw_df: pd.DataFrame, base_dir: Path) -> Dict[str, Any]:
    silver_dir = base_dir / "data" / "silver"
    gold_dir = base_dir / "data" / "gold"
    silver_dir.mkdir(parents=True, exist_ok=True)
    gold_dir.mkdir(parents=True, exist_ok=True)

    cleaned = raw_df.dropna().copy()
    cleaned = _engineer_features(cleaned)
    cleaned.to_parquet(silver_dir / "transport_trips.parquet", index=False)

    daily = (
        cleaned.groupby(["trip_date", "vehicle_type", "zone"], as_index=False)
        .agg(
            trip_count=("trip_id", "count"),
            total_revenue=("total_fare", "sum"),
            avg_fare=("total_fare", "mean"),
            avg_distance_km=("trip_distance_km", "mean"),
            avg_duration_min=("trip_duration_min", "mean"),
            delay_rate=("is_delayed", "mean"),
        )
        .round(3)
    )
    daily.to_parquet(gold_dir / "daily_transport_summary.parquet", index=False)

    return {
        "engine": "pandas",
        "raw_rows": int(len(raw_df)),
        "silver_rows": int(len(cleaned)),
        "gold_rows": int(len(daily)),
        "silver_path": str(silver_dir / "transport_trips.parquet"),
        "gold_path": str(gold_dir / "daily_transport_summary.parquet"),
    }


def _spark_etl(raw_df: pd.DataFrame, base_dir: Path) -> Dict[str, Any]:
    from pyspark.sql import SparkSession
    from pyspark.sql import functions as F

    silver_dir = base_dir / "data" / "silver"
    gold_dir = base_dir / "data" / "gold"
    silver_dir.mkdir(parents=True, exist_ok=True)
    gold_dir.mkdir(parents=True, exist_ok=True)

    spark = (
        SparkSession.builder.appName("TransportAnalysisETL")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    raw_path = base_dir / "data" / "raw" / "transport_trips.csv"
    bronze = spark.read.option("header", True).option("inferSchema", True).csv(str(raw_path))

    silver = (
        bronze.dropna()
        .withColumn("speed_kmh", F.round(F.col("trip_distance_km") / (F.col("trip_duration_min") / 60), 2))
        .withColumn("revenue_per_km", F.round(F.col("total_fare") / F.col("trip_distance_km"), 2))
        .withColumn(
            "is_peak_hour",
            (
                ((F.col("pickup_hour") >= 7) & (F.col("pickup_hour") <= 9))
                | ((F.col("pickup_hour") >= 17) & (F.col("pickup_hour") <= 19))
            ).cast("int"),
        )
    )
    silver.write.mode("overwrite").parquet(str(silver_dir / "transport_trips.parquet"))

    gold = (
        silver.groupBy("trip_date", "vehicle_type", "zone")
        .agg(
            F.count("trip_id").alias("trip_count"),
            F.sum("total_fare").alias("total_revenue"),
            F.round(F.avg("total_fare"), 3).alias("avg_fare"),
            F.round(F.avg("trip_distance_km"), 3).alias("avg_distance_km"),
            F.round(F.avg("trip_duration_min"), 3).alias("avg_duration_min"),
            F.round(F.avg("is_delayed"), 3).alias("delay_rate"),
        )
    )
    gold.write.mode("overwrite").parquet(str(gold_dir / "daily_transport_summary.parquet"))

    result = {
        "engine": "pyspark",
        "raw_rows": int(bronze.count()),
        "silver_rows": int(silver.count()),
        "gold_rows": int(gold.count()),
        "silver_path": str(silver_dir / "transport_trips.parquet"),
        "gold_path": str(gold_dir / "daily_transport_summary.parquet"),
    }
    spark.stop()
    return result


def run_batch_etl(raw_df: pd.DataFrame, base_dir: Path) -> Dict[str, Any]:
    """Run bronze -> silver -> gold batch ETL using PySpark when Java is available."""
    if _spark_available():
        result = _spark_etl(raw_df, base_dir)
    else:
        result = _pandas_etl(raw_df, base_dir)

    reports_dir = base_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "etl_report.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result
