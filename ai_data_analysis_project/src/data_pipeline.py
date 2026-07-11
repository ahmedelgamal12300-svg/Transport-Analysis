from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd


@dataclass
class DataPaths:
    base_dir: Path

    @property
    def data_dir(self) -> Path:
        return self.base_dir / "data"

    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def dataset_path(self) -> Path:
        return self.raw_dir / "transport_trips.csv"


def generate_dataset(base_dir: Path, n_samples: int = 5000, seed: int = 42) -> pd.DataFrame:
    """Generate a synthetic public-transport trip dataset for local analysis."""
    rng = np.random.default_rng(seed)
    paths = DataPaths(base_dir)
    paths.raw_dir.mkdir(parents=True, exist_ok=True)

    vehicle_types = np.array(["Taxi", "Bus", "Metro", "RideShare"])
    zones = np.array(["Downtown", "Airport", "Suburb", "Industrial", "Coastal"])
    payments = np.array(["Cash", "Card", "Mobile"])
    weather = np.array(["Clear", "Rain", "Fog", "Heat"])
    traffic = np.array(["Low", "Medium", "High"])

    vehicle = rng.choice(vehicle_types, size=n_samples, p=[0.35, 0.25, 0.2, 0.2])
    zone = rng.choice(zones, size=n_samples, p=[0.3, 0.15, 0.25, 0.15, 0.15])
    payment_type = rng.choice(payments, size=n_samples, p=[0.2, 0.55, 0.25])
    weather_cond = rng.choice(weather, size=n_samples, p=[0.55, 0.2, 0.1, 0.15])
    traffic_level = rng.choice(traffic, size=n_samples, p=[0.3, 0.45, 0.25])

    base_distance = {
        "Taxi": rng.gamma(3.5, 2.2, n_samples),
        "Bus": rng.gamma(5.0, 3.0, n_samples),
        "Metro": rng.gamma(8.0, 1.5, n_samples),
        "RideShare": rng.gamma(4.0, 2.5, n_samples),
    }
    trip_distance_km = np.array([base_distance[v][i] for i, v in enumerate(vehicle)]).clip(0.5, 45)

    zone_multiplier = pd.Series(zone).map(
        {"Downtown": 1.1, "Airport": 1.35, "Suburb": 0.9, "Industrial": 0.85, "Coastal": 1.05}
    ).to_numpy()
    traffic_multiplier = pd.Series(traffic_level).map({"Low": 0.9, "Medium": 1.0, "High": 1.35}).to_numpy()
    weather_multiplier = pd.Series(weather_cond).map({"Clear": 1.0, "Rain": 1.15, "Fog": 1.2, "Heat": 1.05}).to_numpy()

    trip_duration_min = (
        trip_distance_km * rng.uniform(2.2, 4.8, n_samples) * traffic_multiplier * weather_multiplier
    ).clip(3, 120)

    passenger_count = np.where(
        vehicle == "Metro",
        rng.integers(1, 6, n_samples),
        np.where(vehicle == "Bus", rng.integers(5, 45, n_samples), rng.integers(1, 4, n_samples)),
    )

    rate_per_km = pd.Series(vehicle).map(
        {"Taxi": 4.2, "Bus": 1.1, "Metro": 0.9, "RideShare": 3.6}
    ).to_numpy()
    base_fare = (trip_distance_km * rate_per_km * zone_multiplier + rng.normal(0, 1.5, n_samples)).clip(2, None)
    tip_amount = np.where(
        payment_type == "Cash",
        rng.uniform(0, 2, n_samples),
        np.where(payment_type == "Card", rng.uniform(0, 5, n_samples), rng.uniform(0, 4, n_samples)),
    )
    total_fare = (base_fare + tip_amount).round(2)

    delay_minutes = (
        traffic_multiplier * rng.exponential(2.5, n_samples)
        + np.where(weather_cond == "Rain", rng.uniform(1, 6, n_samples), 0)
        + np.where(weather_cond == "Fog", rng.uniform(2, 8, n_samples), 0)
    ).round(1)
    is_delayed = (delay_minutes > 5).astype(int)

    start = pd.Timestamp("2024-01-01")
    trip_dates = start + pd.to_timedelta(rng.integers(0, 365, n_samples), unit="D")
    pickup_hour = rng.integers(0, 24, n_samples)

    df = pd.DataFrame(
        {
            "trip_id": [f"TRIP-{i:05d}" for i in range(1, n_samples + 1)],
            "trip_date": trip_dates.strftime("%Y-%m-%d"),
            "pickup_hour": pickup_hour,
            "vehicle_type": vehicle,
            "zone": zone,
            "trip_distance_km": trip_distance_km.round(2),
            "trip_duration_min": trip_duration_min.round(1),
            "passenger_count": passenger_count,
            "base_fare": base_fare.round(2),
            "tip_amount": tip_amount.round(2),
            "total_fare": total_fare,
            "payment_type": payment_type,
            "weather": weather_cond,
            "traffic_level": traffic_level,
            "delay_minutes": delay_minutes,
            "is_delayed": is_delayed,
        }
    )

    df.to_csv(paths.dataset_path, index=False)
    return df


def load_dataset(base_dir: Path) -> pd.DataFrame:
    paths = DataPaths(base_dir)
    if not paths.dataset_path.exists():
        return generate_dataset(base_dir)
    return pd.read_csv(paths.dataset_path)


def get_features_targets(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
    features = df.drop(columns=["total_fare", "is_delayed", "trip_id", "trip_date"])
    y_fare = df["total_fare"]
    y_delay = df["is_delayed"]
    return features, y_fare, y_delay
