# Transport Analysis Report

## Project Overview

End-to-end public transport analytics pipeline for the **Digital Egypt Pioneers Initiative (DEPI)** — AI & Data Science track. The workflow covers CSV ingestion, batch ETL (PySpark or Pandas fallback), SQL warehouse analytics, machine learning, and automated reporting.

## Key Transport KPIs

- Total trips analyzed: **5000**
- Average fare: **28.18**
- Average trip distance: **10.82 km**
- Overall delay rate: **30.70%**
- Highest-fare zone: **Airport**
- Top revenue vehicle type: **Taxi**

## ETL Pipeline (Batch Processing)

- Processing engine: **pyspark**
- Raw rows ingested: **5000**
- Silver layer rows: **5000**
- Gold summary rows: **3522**
- Silver output: `C:\Users\Mariam\Downloads\ai_data_analysis_project\data\silver\transport_trips.parquet`
- Gold output: `C:\Users\Mariam\Downloads\ai_data_analysis_project\data\gold\daily_transport_summary.parquet`

## SQL Analytics Highlights

- **Delay hotspot:** High traffic shows the highest delay rate (38.4%).
- **Revenue leader:** Taxi generated 65,181.88 in total revenue.
- **Premium zone:** Airport has the highest average fare (35.47).

## Model Performance

- Fare prediction R²: **0.981**
- Fare prediction MAE: **1.90**
- Delay classification accuracy: **0.779**
- Trip segment silhouette score: **0.323**
- Avg predicted fare (test split): **27.78**

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
