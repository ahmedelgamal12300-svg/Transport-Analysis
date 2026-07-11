"""
Generate project demo video: wideo.mp4
Run: py create_demo_video.py
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, concatenate_videoclips

BASE_DIR = Path(__file__).resolve().parent
OUTPUT = BASE_DIR / "wideo.mp4"
FIGURES = BASE_DIR / "reports" / "figures"
METRICS_PATH = BASE_DIR / "reports" / "model_metrics.json"

W, H = 1280, 720
BG = (22, 58, 88)
ACCENT = (230, 126, 34)
WHITE = (255, 255, 255)
LIGHT = (210, 225, 240)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        trial = " ".join(current + [word])
        if draw.textlength(trial, font=font) <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def make_slide(title: str, body_lines: list[str], subtitle: str = "", duration: float = 5.0) -> tuple[Image.Image, float]:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (W, 10)], fill=ACCENT)
    draw.rectangle([(0, H - 6), (W, H)], fill=ACCENT)

    draw.text((80, 80), title, font=_font(48, bold=True), fill=WHITE)
    y = 155
    if subtitle:
        draw.text((80, y), subtitle, font=_font(26), fill=ACCENT)
        y += 50

    for line in body_lines:
        for wline in _wrap(draw, line, _font(30), W - 160):
            draw.text((100, y), f"• {wline}", font=_font(30), fill=LIGHT)
            y += 42
            if y > H - 90:
                break

    draw.text((80, H - 55), "Transport Analysis  |  DEPI  |  AI & Data Science", font=_font(18), fill=(140, 170, 200))
    return img, duration


def make_chart_slide(chart_path: Path, caption: str, insight: str, duration: float = 5.5) -> tuple[Image.Image, float]:
    img = Image.new("RGB", (W, H), (245, 247, 250))
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (W, 80)], fill=BG)
    draw.text((50, 22), caption, font=_font(32, bold=True), fill=WHITE)

    chart = Image.open(chart_path).convert("RGB")
    chart.thumbnail((720, 480), Image.Resampling.LANCZOS)
    img.paste(chart, (50, 100))

    draw.text((800, 120), "Insight", font=_font(24, bold=True), fill=ACCENT)
    y = 165
    for wline in _wrap(draw, insight, _font(20), 420):
        draw.text((800, y), wline, font=_font(20), fill=(50, 60, 75))
        y += 30

    return img, duration


def build_slides(temp_dir: Path) -> list[tuple[Path, float]]:
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8")) if METRICS_PATH.exists() else {}

    slides: list[tuple[Image.Image, float]] = [
        make_slide(
            "Transport Analysis",
            [
                "Digital Egypt Pioneers Initiative (DEPI)",
                "AI & Data Science — Graduation Project",
                "From raw transport data to intelligent decisions",
            ],
            "Intelligent Public Transport Analytics",
            6.0,
        ),
        make_slide(
            "The Problem",
            [
                "Transport operators collect massive trip data",
                "Spreadsheets cannot scale to thousands of records",
                "Delays and congestion need data-driven responses",
            ],
            "Why We Built This",
            5.0,
        ),
        make_slide(
            "Our Solution",
            [
                "1. CSV Ingestion — transport trip records",
                "2. Batch ETL — Bronze → Silver → Gold layers",
                "3. SQL Warehouse — 6 analytical queries",
                "4. Machine Learning — fare, delay, segmentation",
                "5. Streamlit Dashboard — interactive website",
            ],
            "5-Stage Pipeline",
            6.0,
        ),
        make_slide(
            "Results That Matter",
            [
                "5,000+ trips analyzed",
                f"Fare model R²: {metrics.get('fare_regression_r2', 0.98):.3f}",
                f"Delay prediction: {metrics.get('delay_classification_accuracy', 0.779):.1%} accuracy",
                f"Overall delay rate: {metrics.get('overall_delay_rate', 0.307):.1%}",
                "Airport = highest fares | Taxi = top revenue",
            ],
            "Key Performance Indicators",
            5.5,
        ),
    ]

    chart_items = [
        (FIGURES / "revenue_by_vehicle.png", "Revenue by Vehicle", "Taxi leads total revenue — prioritize fleet and pricing."),
        (FIGURES / "delay_by_traffic.png", "Delays by Traffic", "High traffic causes the highest delay rate."),
        (FIGURES / "peak_hour_trips.png", "Peak Hour Demand", "Morning and evening peaks guide fleet scheduling."),
        (FIGURES / "distance_vs_fare.png", "Fare Intelligence", "Fare scales with distance; vehicle type matters."),
        (FIGURES / "fare_distribution.png", "Fare Distribution", "Most trips cluster at mid-range fares."),
    ]
    for chart, caption, insight in chart_items:
        if chart.exists():
            slides.append(make_chart_slide(chart, caption, insight))

    slides.extend(
        [
            make_slide(
                "Live Dashboard",
                [
                    "Run: py -m streamlit run dashboard.py",
                    "Filter by vehicle, zone, traffic, weather, date",
                    "KPIs and charts update instantly",
                    "No coding required for end users",
                ],
                "Interactive Demo",
                5.5,
            ),
            make_slide(
                "Thank You",
                [
                    "Transport Analysis — From Data to Decisions",
                    "Python | Pandas | PySpark | SQL | ML | Streamlit",
                    "Questions & Live Demo Welcome",
                ],
                "",
                6.0,
            ),
        ]
    )

    paths: list[tuple[Path, float]] = []
    for i, (img, dur) in enumerate(slides):
        p = temp_dir / f"frame_{i:02d}.png"
        p.parent.mkdir(parents=True, exist_ok=True)
        img.save(p)
        paths.append((p, dur))
    return paths


def main() -> None:
    temp_dir = BASE_DIR / "reports" / "video_slides"
    slide_paths = build_slides(temp_dir)
    clips = [ImageClip(str(p)).with_duration(d) for p, d in slide_paths]
    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile(str(OUTPUT), fps=24, codec="libx264", audio=False, logger=None)
    print(f"Demo video saved to: {OUTPUT}")


if __name__ == "__main__":
    main()
