"""
Transport Analysis Dashboard — DEPI AI & Data Science track
Run: py -m streamlit run dashboard.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "src"))

from data_pipeline import load_dataset  # noqa: E402


@st.cache_data
def load_transport_data() -> pd.DataFrame:
    df = load_dataset(BASE_DIR)
    df["trip_date"] = pd.to_datetime(df["trip_date"])
    return df


@st.cache_data
def load_metrics() -> dict:
    path = BASE_DIR / "reports" / "model_metrics.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")

    vehicles = sorted(df["vehicle_type"].unique())
    zones = sorted(df["zone"].unique())
    traffic_levels = sorted(df["traffic_level"].unique())
    weather_opts = sorted(df["weather"].unique())
    min_date = df["trip_date"].min().date()
    max_date = df["trip_date"].max().date()

    sel_vehicles = st.sidebar.multiselect("Vehicle type", vehicles, default=vehicles)
    sel_zones = st.sidebar.multiselect("Zone", zones, default=zones)
    sel_traffic = st.sidebar.multiselect("Traffic level", traffic_levels, default=traffic_levels)
    sel_weather = st.sidebar.multiselect("Weather", weather_opts, default=weather_opts)
    date_range = st.sidebar.date_input(
        "Trip date",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    filtered = df[
        df["vehicle_type"].isin(sel_vehicles)
        & df["zone"].isin(sel_zones)
        & df["traffic_level"].isin(sel_traffic)
        & df["weather"].isin(sel_weather)
    ]
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
        filtered = filtered[
            (filtered["trip_date"].dt.date >= start) & (filtered["trip_date"].dt.date <= end)
        ]
    return filtered


def kpi_row(df: pd.DataFrame) -> None:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Trips", f"{len(df):,}")
    c2.metric("Avg Fare", f"${df['total_fare'].mean():.2f}")
    c3.metric("Avg Distance", f"{df['trip_distance_km'].mean():.1f} km")
    c4.metric("Delay Rate", f"{df['is_delayed'].mean():.1%}")
    c5.metric("Total Revenue", f"${df['total_fare'].sum():,.0f}")


def chart_trips_over_time(df: pd.DataFrame) -> None:
    daily = (
        df.groupby(df["trip_date"].dt.date)
        .agg(trips=("trip_id", "count"), revenue=("total_fare", "sum"))
        .reset_index()
        .rename(columns={"trip_date": "date"})
    )
    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=daily["date"], y=daily["trips"], name="Trips", marker_color="#1a5276")
    )
    fig.add_trace(
        go.Scatter(
            x=daily["date"],
            y=daily["revenue"],
            name="Revenue",
            yaxis="y2",
            mode="lines",
            line=dict(color="#e67e22", width=2),
        )
    )
    fig.update_layout(
        title="Daily Trips & Revenue",
        xaxis_title="Date",
        yaxis=dict(title="Trips"),
        yaxis2=dict(title="Revenue ($)", overlaying="y", side="right"),
        height=400,
        legend=dict(orientation="h", y=1.1),
    )
    st.plotly_chart(fig, use_container_width=True)


def chart_revenue_by_vehicle(df: pd.DataFrame) -> None:
    rev = (
        df.groupby("vehicle_type")
        .agg(trips=("trip_id", "count"), revenue=("total_fare", "sum"), avg_fare=("total_fare", "mean"))
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    fig = px.bar(
        rev,
        x="vehicle_type",
        y="revenue",
        color="vehicle_type",
        title="Revenue by Vehicle Type",
        labels={"revenue": "Total Revenue ($)", "vehicle_type": "Vehicle"},
        text_auto=",.0f",
    )
    fig.update_layout(showlegend=False, height=380)
    st.plotly_chart(fig, use_container_width=True)


def chart_fare_by_zone(df: pd.DataFrame) -> None:
    zone = (
        df.groupby("zone")
        .agg(avg_fare=("total_fare", "mean"), trips=("trip_id", "count"))
        .reset_index()
        .sort_values("avg_fare", ascending=True)
    )
    fig = px.bar(
        zone,
        y="zone",
        x="avg_fare",
        orientation="h",
        title="Average Fare by Zone",
        labels={"avg_fare": "Avg Fare ($)", "zone": "Zone"},
        color="trips",
        color_continuous_scale="Teal",
    )
    fig.update_layout(height=380, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def chart_peak_hours(df: pd.DataFrame) -> None:
    hourly = (
        df.groupby("pickup_hour")
        .agg(trips=("trip_id", "count"), delay_rate=("is_delayed", "mean"))
        .reset_index()
    )
    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=hourly["pickup_hour"], y=hourly["trips"], name="Trips", marker_color="#117a65")
    )
    fig.add_trace(
        go.Scatter(
            x=hourly["pickup_hour"],
            y=hourly["delay_rate"],
            name="Delay Rate",
            yaxis="y2",
            mode="lines+markers",
            line=dict(color="#c0392b", width=2),
        )
    )
    fig.update_layout(
        title="Trips & Delay Rate by Hour",
        xaxis_title="Pickup Hour",
        yaxis=dict(title="Trips"),
        yaxis2=dict(title="Delay Rate", overlaying="y", side="right", tickformat=".0%"),
        height=400,
        legend=dict(orientation="h", y=1.1),
    )
    st.plotly_chart(fig, use_container_width=True)


def chart_delay_by_traffic(df: pd.DataFrame) -> None:
    delay = (
        df.groupby("traffic_level")
        .agg(delay_rate=("is_delayed", "mean"), avg_delay=("delay_minutes", "mean"))
        .reset_index()
    )
    fig = px.bar(
        delay,
        x="traffic_level",
        y="delay_rate",
        color="traffic_level",
        title="Delay Rate by Traffic Level",
        labels={"delay_rate": "Delay Rate", "traffic_level": "Traffic"},
        text_auto=".1%",
    )
    fig.update_layout(showlegend=False, height=380, yaxis_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)


def chart_distance_vs_fare(df: pd.DataFrame) -> None:
    sample = df.sample(min(800, len(df)), random_state=42) if len(df) > 800 else df
    fig = px.scatter(
        sample,
        x="trip_distance_km",
        y="total_fare",
        color="vehicle_type",
        title="Trip Distance vs Fare",
        labels={"trip_distance_km": "Distance (km)", "total_fare": "Fare ($)"},
        opacity=0.7,
    )
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)


def chart_weather_impact(df: pd.DataFrame) -> None:
    weather = (
        df.groupby("weather")
        .agg(trips=("trip_id", "count"), delay_rate=("is_delayed", "mean"))
        .reset_index()
    )
    fig = px.pie(
        weather,
        names="weather",
        values="trips",
        title="Trip Share by Weather",
        hole=0.4,
    )
    fig.update_layout(height=380)
    st.plotly_chart(fig, use_container_width=True)


def trips_table(df: pd.DataFrame) -> None:
    st.subheader("Trip Records")
    display = df[
        [
            "trip_id",
            "trip_date",
            "pickup_hour",
            "vehicle_type",
            "zone",
            "trip_distance_km",
            "total_fare",
            "traffic_level",
            "weather",
            "is_delayed",
        ]
    ].sort_values("trip_date", ascending=False)
    st.dataframe(display, use_container_width=True, hide_index=True)


def main() -> None:
    st.set_page_config(
        page_title="Transport Analysis",
        page_icon="🚌",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("Transport Analysis Dashboard")
    st.caption("Digital Egypt Pioneers Initiative (DEPI) — AI & Data Science track")

    df = load_transport_data()
    filtered = apply_filters(df)

    if filtered.empty:
        st.warning("No trips match the selected filters.")
        return

    st.subheader("Key Performance Indicators")
    kpi_row(filtered)

    metrics = load_metrics()
    if metrics:
        st.divider()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Fare Model R²", f"{metrics.get('fare_regression_r2', 0):.3f}")
        m2.metric("Fare Model MAE", f"${metrics.get('fare_regression_mae', 0):.2f}")
        m3.metric("Delay Model Accuracy", f"{metrics.get('delay_classification_accuracy', 0):.1%}")
        m4.metric("Trip Segments", f"{metrics.get('trip_clustering_silhouette', 0):.3f} silhouette")

    st.divider()
    chart_trips_over_time(filtered)

    col_a, col_b = st.columns(2)
    with col_a:
        chart_revenue_by_vehicle(filtered)
    with col_b:
        chart_fare_by_zone(filtered)

    chart_peak_hours(filtered)

    col_c, col_d = st.columns(2)
    with col_c:
        chart_delay_by_traffic(filtered)
    with col_d:
        chart_weather_impact(filtered)

    chart_distance_vs_fare(filtered)
    trips_table(filtered)


if __name__ == "__main__":
    main()
