from __future__ import annotations

from pathlib import Path

from analysis_report import build_analysis_report
from data_pipeline import load_dataset
from spark_etl import run_batch_etl
from sql_analytics import run_sql_analytics
from train_ai_model import train_and_evaluate


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent

    print("Step 1/4: Loading transport dataset...")
    dataset = load_dataset(base_dir)

    print("Step 2/4: Running batch ETL (PySpark / Pandas)...")
    etl_report = run_batch_etl(dataset, base_dir)

    print("Step 3/4: Running SQL warehouse analytics...")
    sql_results = run_sql_analytics(base_dir)

    print("Step 4/4: Training ML models and building report...")
    metrics = train_and_evaluate(dataset, base_dir)
    report_path = build_analysis_report(dataset, metrics, sql_results, etl_report, base_dir)

    print("\nTransport Analysis completed successfully.")
    print(f"ETL engine: {etl_report['engine']}")
    print(f"Trips processed: {len(dataset)}")
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()
