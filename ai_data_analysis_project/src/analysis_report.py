from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _save_figures(df: pd.DataFrame, sql_results: Dict[str, Any], base_dir: Path) -> None:
    figures_dir = base_dir / "reports" / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(8, 5))
    sns.histplot(df["total_fare"], bins=30, kde=True, color="steelblue")
    plt.title("Trip Fare Distribution")
    plt.xlabel("Total Fare")
    plt.tight_layout()
    plt.savefig(figures_dir / "fare_distribution.png", dpi=140)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.scatterplot(
        data=df,
        x="trip_distance_km",
        y="total_fare",
        hue="vehicle_type",
        alpha=0.7,
    )
    plt.title("Distance vs Fare by Vehicle Type")
    plt.tight_layout()
    plt.savefig(figures_dir / "distance_vs_fare.png", dpi=140)
    plt.close()

    delay_by_traffic = (
        df.groupby("traffic_level", as_index=False)["is_delayed"].mean().sort_values(by="is_delayed", ascending=False)
    )
    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=delay_by_traffic,
        x="traffic_level",
        y="is_delayed",
        hue="traffic_level",
        palette="rocket",
        legend=False,
    )
    plt.title("Delay Rate by Traffic Level")
    plt.ylabel("Delay Rate")
    plt.tight_layout()
    plt.savefig(figures_dir / "delay_by_traffic.png", dpi=140)
    plt.close()

    peak_df = pd.DataFrame(sql_results["queries"]["peak_hour_analysis"])
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=peak_df, x="pickup_hour", y="trips", marker="o", color="darkgreen")
    plt.title("Trips by Pickup Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Trip Count")
    plt.tight_layout()
    plt.savefig(figures_dir / "peak_hour_trips.png", dpi=140)
    plt.close()

    revenue_df = pd.DataFrame(sql_results["queries"]["revenue_by_vehicle_type"])
    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=revenue_df,
        x="vehicle_type",
        y="total_revenue",
        hue="vehicle_type",
        palette="viridis",
        legend=False,
    )
    plt.title("Total Revenue by Vehicle Type")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(figures_dir / "revenue_by_vehicle.png", dpi=140)
    plt.close()


def build_analysis_report(
    df: pd.DataFrame,
    metrics: Dict[str, float],
    sql_results: Dict[str, Any],
    etl_report: Dict[str, Any],
    base_dir: Path,
) -> Path:
    _save_figures(df, sql_results, base_dir)

    report_path = base_dir / "reports" / "analysis_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    top_zone = pd.DataFrame(sql_results["queries"]["avg_fare_by_zone"]).iloc[0]
    top_vehicle = pd.DataFrame(sql_results["queries"]["revenue_by_vehicle_type"]).iloc[0]
    worst_traffic = pd.DataFrame(sql_results["queries"]["delay_rate_by_traffic"]).iloc[0]

    kpis = {
        "total_trips": int(len(df)),
        "avg_fare": float(df["total_fare"].mean()),
        "avg_distance_km": float(df["trip_distance_km"].mean()),
        "delay_rate": float(df["is_delayed"].mean()),
        "top_zone_by_fare": str(top_zone["zone"]),
        "top_vehicle_by_revenue": str(top_vehicle["vehicle_type"]),
    }

    markdown = f"""# Transport Analysis Report

## Project Overview

End-to-end public transport analytics pipeline for the **Digital Egypt Pioneers Initiative (DEPI)** — AI & Data Science track. The workflow covers CSV ingestion, batch ETL (PySpark or Pandas fallback), SQL warehouse analytics, machine learning, and automated reporting.

## Key Transport KPIs

- Total trips analyzed: **{kpis["total_trips"]}**
- Average fare: **{kpis["avg_fare"]:.2f}**
- Average trip distance: **{kpis["avg_distance_km"]:.2f} km**
- Overall delay rate: **{kpis["delay_rate"]:.2%}**
- Highest-fare zone: **{kpis["top_zone_by_fare"]}**
- Top revenue vehicle type: **{kpis["top_vehicle_by_revenue"]}**

## ETL Pipeline (Batch Processing)

- Processing engine: **{etl_report["engine"]}**
- Raw rows ingested: **{etl_report["raw_rows"]}**
- Silver layer rows: **{etl_report["silver_rows"]}**
- Gold summary rows: **{etl_report["gold_rows"]}**
- Silver output: `{etl_report["silver_path"]}`
- Gold output: `{etl_report["gold_path"]}`

## SQL Analytics Highlights

- **Delay hotspot:** {worst_traffic["traffic_level"]} traffic shows the highest delay rate ({float(worst_traffic["delay_rate"]):.1%}).
- **Revenue leader:** {top_vehicle["vehicle_type"]} generated {float(top_vehicle["total_revenue"]):,.2f} in total revenue.
- **Premium zone:** {top_zone["zone"]} has the highest average fare ({float(top_zone["avg_fare"]):.2f}).

## Model Performance

- Fare prediction R²: **{metrics["fare_regression_r2"]:.3f}**
- Fare prediction MAE: **{metrics["fare_regression_mae"]:.2f}**
- Delay classification accuracy: **{metrics["delay_classification_accuracy"]:.3f}**
- Trip segment silhouette score: **{metrics["trip_clustering_silhouette"]:.3f}**
- Avg predicted fare (test split): **{metrics["avg_predicted_fare"]:.2f}**

## Insights

1. **Distance and vehicle type strongly drive fare levels**, with airport and downtown zones commanding higher average fares.
2. **Traffic and weather conditions increase delay risk**, making delay prediction useful for operations planning.
3. **Trip segmentation reveals distinct mobility patterns** (short urban hops vs longer suburban/airport routes) for targeted service optimization.

## Generated Visuals

- `reports/figures/fare_distribution.png`
- `reports/figures/distance_vs_fare.png`
- `reports/figures/delay_by_traffic.png`
- `reports/figures/peak_hour_trips.png`
- `reports/figures/revenue_by_vehicle.png`

## Output Files

- `reports/etl_report.json`
- `reports/sql_analytics.json`
- `reports/model_metrics.json`
- `reports/clustered_trips.csv`
- `sql/analytics_queries.sql`
- `data/warehouse/transport.db`
"""
    report_path.write_text(markdown, encoding="utf-8")
    return report_path
