"""
Generate a printable PDF explaining every project module and its code.
Output: reports/Transport_Analysis_Code_Documentation.pdf
"""
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR / "reports" / "Transport_Analysis_Code_Documentation.pdf"

NAVY = colors.HexColor("#1e3a5f")
TEAL = colors.HexColor("#0f766e")
SLATE = colors.HexColor("#334155")
CODE_BG = colors.HexColor("#f1f5f9")
LIGHT_ROW = colors.HexColor("#f8fafc")
BORDER = colors.HexColor("#cbd5e1")


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontSize=24,
                              textColor=NAVY, spaceAfter=10, alignment=TA_CENTER,
                              leading=30, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontSize=11,
                              textColor=SLATE, alignment=TA_CENTER, spaceAfter=6, leading=15))
    styles.add(ParagraphStyle(name="H1Doc", parent=styles["Heading1"], fontSize=15,
                              textColor=NAVY, spaceBefore=16, spaceAfter=8, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="H2Doc", parent=styles["Heading2"], fontSize=12,
                              textColor=TEAL, spaceBefore=12, spaceAfter=6, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="BodyDoc", parent=styles["Normal"], fontSize=9.5,
                              textColor=SLATE, alignment=TA_JUSTIFY, spaceAfter=7, leading=13))
    styles.add(ParagraphStyle(name="CodeBlock", parent=styles["Code"], fontName="Courier",
                              fontSize=7.5, textColor=colors.HexColor("#1e293b"),
                              backColor=CODE_BG, leftIndent=4, rightIndent=4,
                              spaceBefore=5, spaceAfter=8, leading=10))
    styles.add(ParagraphStyle(name="Caption", parent=styles["Normal"], fontSize=8,
                              textColor=colors.HexColor("#64748b"), spaceAfter=8,
                              fontName="Helvetica-Oblique"))
    styles.add(ParagraphStyle(name="TOCEntry", parent=styles["Normal"], fontSize=10,
                              textColor=SLATE, spaceAfter=5, leading=14))
    return styles


def code_block(text: str, styles) -> Preformatted:
    return Preformatted(text.replace("\t", "    ").rstrip() + "\n", styles["CodeBlock"], maxLineLength=95)


def header_footer(canvas, doc):
    canvas.saveState()
    page_w, page_h = A4
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(1.5)
    canvas.line(1.8 * cm, page_h - 1.2 * cm, page_w - 1.8 * cm, page_h - 1.2 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(1.8 * cm, page_h - 1.0 * cm, "Transport Analysis — Code Documentation")
    canvas.drawRightString(page_w - 1.8 * cm, page_h - 1.0 * cm, "DEPI AI & Data Science")
    canvas.line(1.8 * cm, 1.4 * cm, page_w - 1.8 * cm, 1.4 * cm)
    canvas.drawCentredString(page_w / 2, 0.9 * cm, f"Page {doc.page}")
    canvas.restoreState()


def make_table(data, col_widths=None):
    t = Table(data, colWidths=col_widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("TEXTCOLOR", (0, 1), (-1, -1), SLATE),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_ROW, colors.white]),
    ]))
    return t


def build():
    styles = build_styles()
    story = []

    # Cover
    story.append(Spacer(1, 3.2 * cm))
    story.append(Paragraph("Transport Analysis", styles["CoverTitle"]))
    story.append(Paragraph("What Each Code File Does", styles["CoverTitle"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "Digital Egypt Pioneers Initiative (DEPI) — AI &amp; Data Science Track",
        styles["CoverSub"]))
    story.append(Paragraph(
        "Detailed explanation of every module, function, and data flow.",
        styles["CoverSub"]))
    story.append(Spacer(1, 1 * cm))
    story.append(make_table([
        ["Item", "Details"],
        ["Pipeline command", "py src/main.py"],
        ["Dashboard command", "py -m streamlit run dashboard.py"],
        ["Team", "Ahmed El-Gamal, Youssef Mustafa, Maryam Khaled,"],
        ["", "Mariam Tarek, Mostafa Fouad, Nada Ahmed"],
    ], col_widths=[4.5 * cm, 11.5 * cm]))
    story.append(PageBreak())

    # TOC
    story.append(Paragraph("1. Table of Contents", styles["H1Doc"]))
    for item in [
        "1. Table of Contents",
        "2. Project Overview",
        "3. How to Run",
        "4. Folder Structure",
        "5. main.py — Orchestrator",
        "6. data_pipeline.py — Data Ingestion",
        "7. spark_etl.py — Batch ETL",
        "8. sql_analytics.py — SQL Warehouse",
        "9. train_ai_model.py — Machine Learning",
        "10. analysis_report.py — Charts &amp; Report",
        "11. dashboard.py — Streamlit Website",
        "12. Data Flow Summary",
    ]:
        story.append(Paragraph(f"•  {item}", styles["TOCEntry"]))
    story.append(PageBreak())

    # Overview
    story.append(Paragraph("2. Project Overview", styles["H1Doc"]))
    story.append(Paragraph(
        "This project is an end-to-end public transport analytics system. It loads trip data, "
        "cleans it through a medallion ETL pipeline, runs SQL analytics in SQLite, trains "
        "machine-learning models, writes a Markdown report with charts, and provides an "
        "interactive Streamlit dashboard.",
        styles["BodyDoc"]))
    story.append(make_table([
        ["Stage", "Module", "Role"],
        ["1. Ingestion", "data_pipeline.py", "Load or generate transport_trips.csv"],
        ["2. Batch ETL", "spark_etl.py", "Bronze → Silver → Gold Parquet layers"],
        ["3. SQL Analytics", "sql_analytics.py", "SQLite warehouse + 6 SQL queries"],
        ["4. Machine Learning", "train_ai_model.py", "Fare, delay, and clustering models"],
        ["5. Reporting", "analysis_report.py", "KPIs, PNG charts, Markdown report"],
        ["6. Dashboard", "dashboard.py", "Interactive filters, charts, trip table"],
    ], col_widths=[3.2 * cm, 4.2 * cm, 8.6 * cm]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "<b>main.py</b> runs stages 1–5. <b>dashboard.py</b> is a separate website entry point.",
        styles["BodyDoc"]))

    # How to run
    story.append(Paragraph("3. How to Run", styles["H1Doc"]))
    story.append(code_block(
        "py -m pip install -r requirements.txt\n"
        "py src/main.py\n"
        "py -m streamlit run dashboard.py", styles))
    story.append(Paragraph(
        "PySpark needs Java. If Java is missing, ETL automatically uses Pandas instead.",
        styles["BodyDoc"]))

    # Structure
    story.append(Paragraph("4. Folder Structure", styles["H1Doc"]))
    story.append(code_block("""Transport Analysis/
├── src/
│   ├── main.py              # Pipeline orchestrator
│   ├── data_pipeline.py     # CSV ingestion & synthetic data
│   ├── spark_etl.py         # Bronze → Silver → Gold ETL
│   ├── sql_analytics.py     # SQLite warehouse + SQL queries
│   ├── train_ai_model.py    # Fare, delay, clustering models
│   └── analysis_report.py   # KPIs, plots, Markdown report
├── data/raw · silver · gold · warehouse
├── sql/analytics_queries.sql
├── reports/                 # Metrics, figures, report
└── dashboard.py             # Streamlit website""", styles))
    story.append(PageBreak())

    # main.py
    story.append(Paragraph("5. main.py — Pipeline Orchestrator", styles["H1Doc"]))
    story.append(Paragraph(
        "<b>File:</b> <font face='Courier'>src/main.py</font><br/>"
        "<b>Purpose:</b> Single entry point that runs the full analysis pipeline in order.",
        styles["BodyDoc"]))
    story.append(Paragraph(
        "1. Resolves project root (<font face='Courier'>base_dir</font>).<br/>"
        "2. Loads the transport dataset.<br/>"
        "3. Runs batch ETL and captures the ETL report.<br/>"
        "4. Runs SQL warehouse analytics.<br/>"
        "5. Trains ML models, then builds the Markdown report.<br/>"
        "6. Prints engine, trip count, and report path.",
        styles["BodyDoc"]))
    story.append(code_block('''def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    dataset = load_dataset(base_dir)
    etl_report = run_batch_etl(dataset, base_dir)
    sql_results = run_sql_analytics(base_dir)
    metrics = train_and_evaluate(dataset, base_dir)
    report_path = build_analysis_report(
        dataset, metrics, sql_results, etl_report, base_dir
    )
    print(f"ETL engine: {etl_report['engine']}")
    print(f"Trips processed: {len(dataset)}")
    print(f"Report saved to: {report_path}")''', styles))
    story.append(PageBreak())

    # data_pipeline
    story.append(Paragraph("6. data_pipeline.py — Data Ingestion", styles["H1Doc"]))
    story.append(Paragraph(
        "<b>File:</b> <font face='Courier'>src/data_pipeline.py</font><br/>"
        "<b>Purpose:</b> Define paths, generate synthetic trips if needed, and load the CSV.",
        styles["BodyDoc"]))

    story.append(Paragraph("6.1 DataPaths", styles["H2Doc"]))
    story.append(Paragraph(
        "Dataclass that exposes <font face='Courier'>data/</font>, "
        "<font face='Courier'>data/raw/</font>, and "
        "<font face='Courier'>transport_trips.csv</font> from the project root.",
        styles["BodyDoc"]))

    story.append(Paragraph("6.2 generate_dataset()", styles["H2Doc"]))
    story.append(Paragraph(
        "Creates <b>5,000</b> synthetic trips with seed <b>42</b> (reproducible). "
        "Samples vehicle, zone, payment, weather, and traffic, then derives distance, "
        "duration, fare, and delay with domain rules.",
        styles["BodyDoc"]))
    story.append(Paragraph(
        "• Distance ~ Gamma per vehicle (clipped 0.5–45 km)<br/>"
        "• Duration = distance × random factor × traffic × weather<br/>"
        "• Fare = distance × rate_per_km × zone multiplier + tip<br/>"
        "• Delay from traffic/weather; <font face='Courier'>is_delayed = 1</font> if delay &gt; 5 min",
        styles["BodyDoc"]))
    story.append(code_block('''def generate_dataset(base_dir, n_samples=5000, seed=42) -> pd.DataFrame:
    # sample categories, compute distance/duration/fare/delay
    df = pd.DataFrame({...})
    df.to_csv(paths.dataset_path, index=False)
    return df''', styles))

    story.append(Paragraph("6.3 load_dataset()", styles["H2Doc"]))
    story.append(code_block('''def load_dataset(base_dir: Path) -> pd.DataFrame:
    paths = DataPaths(base_dir)
    if not paths.dataset_path.exists():
        return generate_dataset(base_dir)
    return pd.read_csv(paths.dataset_path)''', styles))

    story.append(Paragraph("6.4 get_features_targets()", styles["H2Doc"]))
    story.append(Paragraph(
        "Drops ID/date/target columns and returns features plus "
        "<font face='Courier'>total_fare</font> and <font face='Courier'>is_delayed</font>.",
        styles["BodyDoc"]))
    story.append(PageBreak())

    # spark_etl
    story.append(Paragraph("7. spark_etl.py — Batch ETL", styles["H1Doc"]))
    story.append(Paragraph(
        "<b>File:</b> <font face='Courier'>src/spark_etl.py</font><br/>"
        "<b>Purpose:</b> Transform raw CSV into Silver (cleaned) and Gold (aggregated) Parquet. "
        "Uses PySpark when Java is available; otherwise Pandas.",
        styles["BodyDoc"]))
    story.append(make_table([
        ["Layer", "Output", "Meaning"],
        ["Bronze", "transport_trips.csv", "Raw as-ingested trips"],
        ["Silver", "transport_trips.parquet", "Cleaned + engineered features"],
        ["Gold", "daily_transport_summary.parquet", "Daily aggregates by vehicle/zone"],
    ], col_widths=[2.8 * cm, 6.5 * cm, 6.7 * cm]))

    story.append(Paragraph("7.1 _spark_available()", styles["H2Doc"]))
    story.append(Paragraph(
        "Checks for a <font face='Courier'>java</font> binary, then tries to start/stop a "
        "tiny SparkSession. Returns False on any failure so the pipeline never crashes.",
        styles["BodyDoc"]))

    story.append(Paragraph("7.2 _engineer_features()", styles["H2Doc"]))
    story.append(code_block('''out["speed_kmh"] = distance / (duration_min / 60)
out["revenue_per_km"] = total_fare / distance
out["is_peak_hour"] = 1 if hour in 7–9 or 17–19 else 0''', styles))

    story.append(Paragraph("7.3 _pandas_etl() / _spark_etl()", styles["H2Doc"]))
    story.append(Paragraph(
        "Drop nulls, engineer features, write Silver Parquet, then group by "
        "date/vehicle/zone for Gold metrics (trip_count, total_revenue, avg_fare, "
        "avg_distance_km, avg_duration_min, delay_rate).",
        styles["BodyDoc"]))

    story.append(Paragraph("7.4 run_batch_etl()", styles["H2Doc"]))
    story.append(code_block('''def run_batch_etl(raw_df, base_dir):
    if _spark_available():
        result = _spark_etl(raw_df, base_dir)
    else:
        result = _pandas_etl(raw_df, base_dir)
    # write reports/etl_report.json
    return result''', styles))
    story.append(PageBreak())

    # sql_analytics
    story.append(Paragraph("8. sql_analytics.py — SQL Warehouse", styles["H1Doc"]))
    story.append(Paragraph(
        "<b>File:</b> <font face='Courier'>src/sql_analytics.py</font><br/>"
        "<b>Purpose:</b> Load Silver data into SQLite, run six analytical queries, export JSON + SQL file.",
        styles["BodyDoc"]))
    story.append(make_table([
        ["Query name", "Business question"],
        ["daily_trip_volume", "Trips and revenue per day?"],
        ["avg_fare_by_zone", "Which zones have highest average fares?"],
        ["delay_rate_by_traffic", "How does traffic affect delays?"],
        ["revenue_by_vehicle_type", "Which vehicle type earns the most?"],
        ["peak_hour_analysis", "When are trips densest / most delayed?"],
        ["weather_impact", "How does weather change delay risk?"],
    ], col_widths=[5 * cm, 11 * cm]))

    story.append(Paragraph("8.1 run_sql_analytics()", styles["H2Doc"]))
    story.append(code_block('''def run_sql_analytics(base_dir):
    df = _load_silver_dataframe(base_dir)  # Silver Parquet or raw CSV
    with sqlite3.connect(db_path) as conn:
        df.to_sql("transport_trips", conn, if_exists="replace", index=False)
        for name, query in QUERIES.items():
            frame = pd.read_sql_query(query, conn)
            results["queries"][name] = frame.to_dict(orient="records")
    # write sql_analytics.json + analytics_queries.sql
    return results''', styles))
    story.append(PageBreak())

    # train_ai_model
    story.append(Paragraph("9. train_ai_model.py — Machine Learning", styles["H1Doc"]))
    story.append(Paragraph(
        "<b>File:</b> <font face='Courier'>src/train_ai_model.py</font><br/>"
        "<b>Purpose:</b> Train fare regression, delay classification, and trip clustering.",
        styles["BodyDoc"]))

    story.append(Paragraph("9.1 _build_preprocessor()", styles["H2Doc"]))
    story.append(Paragraph(
        "Scales numeric features (hour, distance, duration, passengers) and one-hot encodes "
        "categoricals (vehicle, zone, payment, weather, traffic).",
        styles["BodyDoc"]))

    story.append(Paragraph("9.2 train_and_evaluate() — three models", styles["H2Doc"]))
    story.append(make_table([
        ["Model", "Algorithm", "Target / input", "Metric (latest)"],
        ["Fare regression", "RandomForestRegressor", "total_fare", "R² ≈ 0.981, MAE ≈ $1.91"],
        ["Delay classifier", "RandomForestClassifier", "is_delayed", "Accuracy ≈ 77.9%"],
        ["Trip clustering", "KMeans (k=4)", "distance, duration, fare, delay", "Silhouette ≈ 0.323"],
    ], col_widths=[3.5 * cm, 4.2 * cm, 4.5 * cm, 3.8 * cm]))
    story.append(Paragraph(
        "Uses 80/20 train-test split (seed=42). Saves "
        "<font face='Courier'>model_metrics.json</font> and "
        "<font face='Courier'>clustered_trips.csv</font> (with trip_segment labels).",
        styles["BodyDoc"]))
    story.append(code_block('''# Fare: Pipeline(preprocessor + RandomForestRegressor(200 trees))
# Delay: Pipeline(preprocessor + RandomForestClassifier(200 trees))
# Clusters: StandardScaler + KMeans(n_clusters=4) on
#           [distance, duration, fare, delay_minutes]''', styles))
    story.append(PageBreak())

    # analysis_report
    story.append(Paragraph("10. analysis_report.py — Charts &amp; Report", styles["H1Doc"]))
    story.append(Paragraph(
        "<b>File:</b> <font face='Courier'>src/analysis_report.py</font><br/>"
        "<b>Purpose:</b> Create PNG charts and a Markdown summary of KPIs, ETL, SQL, and ML.",
        styles["BodyDoc"]))
    story.append(make_table([
        ["File", "Chart"],
        ["fare_distribution.png", "Histogram of total fare"],
        ["distance_vs_fare.png", "Scatter: distance vs fare by vehicle"],
        ["delay_by_traffic.png", "Bar: delay rate by traffic level"],
        ["peak_hour_trips.png", "Line: trips by pickup hour (from SQL)"],
        ["revenue_by_vehicle.png", "Bar: revenue by vehicle type (from SQL)"],
    ], col_widths=[5 * cm, 11 * cm]))
    story.append(Paragraph(
        "<font face='Courier'>build_analysis_report()</font> computes KPIs, pulls SQL "
        "highlights (worst traffic, top vehicle, premium zone), embeds ML metrics, and "
        "writes <font face='Courier'>reports/analysis_report.md</font>.",
        styles["BodyDoc"]))
    story.append(PageBreak())

    # dashboard
    story.append(Paragraph("11. dashboard.py — Streamlit Website", styles["H1Doc"]))
    story.append(Paragraph(
        "<b>File:</b> <font face='Courier'>dashboard.py</font> (project root)<br/>"
        "<b>Purpose:</b> Interactive browser dashboard at http://localhost:8501",
        styles["BodyDoc"]))
    story.append(make_table([
        ["Function", "Role"],
        ["load_transport_data()", "Load trips (cached with @st.cache_data)"],
        ["load_metrics()", "Load ML scores from model_metrics.json"],
        ["apply_filters()", "Sidebar: vehicle, zone, traffic, weather, date"],
        ["kpi_row()", "Five KPI cards on filtered data"],
        ["chart_trips_over_time()", "Daily trips bars + revenue line"],
        ["chart_revenue_by_vehicle()", "Revenue by vehicle type"],
        ["chart_fare_by_zone()", "Average fare by zone"],
        ["chart_peak_hours()", "Trips & delay rate by hour"],
        ["chart_delay_by_traffic()", "Delay rate by traffic"],
        ["chart_distance_vs_fare()", "Scatter sample by vehicle"],
        ["chart_weather_impact()", "Donut: trip share by weather"],
        ["trips_table()", "Sortable trip records table"],
        ["main()", "Page layout: KPIs → metrics → charts → table"],
    ], col_widths=[5.5 * cm, 10.5 * cm]))
    story.append(PageBreak())

    # Flow
    story.append(Paragraph("12. Data Flow Summary", styles["H1Doc"]))
    story.append(code_block("""[Start] py src/main.py
    |
    v
load_dataset()        →  data/raw/transport_trips.csv
    |
    v
run_batch_etl()       →  Silver + Gold Parquet + etl_report.json
    |
    v
run_sql_analytics()   →  transport.db + sql_analytics.json + .sql
    |
    v
train_and_evaluate()  →  model_metrics.json + clustered_trips.csv
    |
    v
build_analysis_report() → figures/*.png + analysis_report.md
    |
    v
[Done]

Separate UI:
py -m streamlit run dashboard.py
    → filters / KPIs / Plotly charts / trip table""", styles))
    story.append(Paragraph(
        "In short: <b>main.py</b> wires the offline pipeline; each "
        "<font face='Courier'>src/</font> module owns one stage; "
        "<b>dashboard.py</b> is the interactive front end.",
        styles["BodyDoc"]))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph("— End of Code Documentation —", styles["CoverSub"]))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH), pagesize=A4,
        leftMargin=1.8 * cm, rightMargin=1.8 * cm,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title="Transport Analysis — Code Documentation",
        author="DEPI Transport Analysis Team",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    return OUTPUT_PATH


if __name__ == "__main__":
    path = build()
    print(f"PDF written to: {path}")
