from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict

import pandas as pd


QUERIES = {
    "daily_trip_volume": """
        SELECT trip_date, COUNT(*) AS trip_count, ROUND(SUM(total_fare), 2) AS daily_revenue
        FROM transport_trips
        GROUP BY trip_date
        ORDER BY trip_date
    """,
    "avg_fare_by_zone": """
        SELECT zone,
               ROUND(AVG(total_fare), 2) AS avg_fare,
               ROUND(AVG(trip_distance_km), 2) AS avg_distance_km,
               COUNT(*) AS trips
        FROM transport_trips
        GROUP BY zone
        ORDER BY avg_fare DESC
    """,
    "delay_rate_by_traffic": """
        SELECT traffic_level,
               ROUND(AVG(is_delayed), 3) AS delay_rate,
               ROUND(AVG(delay_minutes), 2) AS avg_delay_min,
               COUNT(*) AS trips
        FROM transport_trips
        GROUP BY traffic_level
        ORDER BY delay_rate DESC
    """,
    "revenue_by_vehicle_type": """
        SELECT vehicle_type,
               COUNT(*) AS trips,
               ROUND(SUM(total_fare), 2) AS total_revenue,
               ROUND(AVG(total_fare), 2) AS avg_fare
        FROM transport_trips
        GROUP BY vehicle_type
        ORDER BY total_revenue DESC
    """,
    "peak_hour_analysis": """
        SELECT pickup_hour,
               COUNT(*) AS trips,
               ROUND(AVG(total_fare), 2) AS avg_fare,
               ROUND(AVG(is_delayed), 3) AS delay_rate
        FROM transport_trips
        GROUP BY pickup_hour
        ORDER BY pickup_hour
    """,
    "weather_impact": """
        SELECT weather,
               COUNT(*) AS trips,
               ROUND(AVG(delay_minutes), 2) AS avg_delay_min,
               ROUND(AVG(is_delayed), 3) AS delay_rate
        FROM transport_trips
        GROUP BY weather
        ORDER BY delay_rate DESC
    """,
}


def _load_silver_dataframe(base_dir: Path) -> pd.DataFrame:
    silver_path = base_dir / "data" / "silver" / "transport_trips.parquet"
    if silver_path.exists():
        return pd.read_parquet(silver_path)
    return pd.read_csv(base_dir / "data" / "raw" / "transport_trips.csv")


def run_sql_analytics(base_dir: Path) -> Dict[str, Any]:
    """Load cleaned transport data into a local SQLite warehouse and run SQL analytics."""
    df = _load_silver_dataframe(base_dir)
    warehouse_dir = base_dir / "data" / "warehouse"
    warehouse_dir.mkdir(parents=True, exist_ok=True)
    db_path = warehouse_dir / "transport.db"

    with sqlite3.connect(db_path) as conn:
        df.to_sql("transport_trips", conn, if_exists="replace", index=False)
        results: Dict[str, Any] = {"database": str(db_path), "queries": {}}
        for name, query in QUERIES.items():
            frame = pd.read_sql_query(query, conn)
            results["queries"][name] = frame.to_dict(orient="records")

    reports_dir = base_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "sql_analytics.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

    sql_dir = base_dir / "sql"
    sql_dir.mkdir(parents=True, exist_ok=True)
    sql_text = "\n\n".join(f"-- {name}\n{query.strip()};" for name, query in QUERIES.items())
    (sql_dir / "analytics_queries.sql").write_text(sql_text + "\n", encoding="utf-8")

    return results
