# Transport Analysis

**Digital Egypt Pioneers Initiative (DEPI)** — AI & Data Science track graduation project.

End-to-end analytics pipeline for large public transport datasets using **Python**, **Pandas**, **PySpark**, **SQL**, and **scikit-learn**.

## Project Structure

```
ai_data_analysis_project/
├── src/
│   ├── main.py              # Full pipeline orchestrator
│   ├── data_pipeline.py     # CSV ingestion & synthetic transport data
│   ├── spark_etl.py         # Bronze → Silver → Gold batch ETL
│   ├── sql_analytics.py     # SQLite warehouse + SQL queries
│   ├── train_ai_model.py    # Fare, delay, and segmentation models
│   └── analysis_report.py   # KPIs, plots, Markdown report
├── data/
│   ├── raw/                 # transport_trips.csv
│   ├── silver/              # Cleaned Parquet (ETL output)
│   ├── gold/                # Daily aggregated summaries
│   └── warehouse/           # transport.db (SQL analytics)
├── sql/
│   └── analytics_queries.sql
└── reports/                 # JSON metrics, CSV clusters, figures, report
```

## Pipeline Stages

| Stage | Description |
|-------|-------------|
| **1. Data Ingestion** | Load/generate transport CSV (trips, fares, delays, zones) |
| **2. Batch ETL** | PySpark transforms raw data into silver/gold Parquet layers |
| **3. SQL Analytics** | Load warehouse and run analytical SQL queries |
| **4. Machine Learning** | Fare regression, delay classification, trip clustering |
| **5. Reporting** | Automated KPI summary, charts, and Markdown report |

## Quick Start

```bash
py -m pip install -r requirements.txt
py src/main.py
```

## Website (Interactive Dashboard)

```bash
py -m streamlit run dashboard.py
```

Or double-click `run_website.bat`. The dashboard opens at **http://localhost:8501**

Features: KPIs, filters (vehicle, zone, traffic, weather, date), interactive charts, ML metrics, and trip table.

## Demo Video

Generate `wideo.mp4` (project walkthrough slideshow):

```bash
py create_demo_video.py
```

## Graduation Presentation

Generate **22-slide PowerPoint** with speaker notes:

```bash
py create_presentation.py
```

Opens: `Transport_Analysis_Presentation.pptx`  
Speaking script: `PRESENTATION_GUIDE.md` (12–15 min + live demo)

## System Requirements

- Python 3.10+
- **PySpark** requires Java 8+ (`JAVA_HOME` set). If Java is not installed, the pipeline automatically falls back to a Pandas-based ETL with identical outputs.

## Outputs

After running:

- `data/raw/transport_trips.csv`
- `data/silver/transport_trips.parquet`
- `data/gold/daily_transport_summary.parquet`
- `data/warehouse/transport.db`
- `reports/analysis_report.md`
- `reports/etl_report.json`
- `reports/sql_analytics.json`
- `reports/model_metrics.json`
- `reports/clustered_trips.csv`
- `reports/figures/*.png`

## Team

Ahmed El-Gamal, Youssef Mustafa, Maryam Khaled, Mariam Tarek, Mostafa Fouad, Nada Ahmed

## Program

Digital Egypt Pioneers Initiative (DEPI) — Transport Analysis Project
