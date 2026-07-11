"""
Generate light-themed UML diagrams for Transport Analysis presentation.
Output: reports/uml/*.png
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

BASE = Path(__file__).resolve().parent
OUT_DIR = BASE / "reports" / "uml"

NAVY = "#1e3a5f"
TEAL = "#0f766e"
SLATE = "#334155"
MUTED = "#64748b"
WHITE = "#ffffff"
BG = "#f8fafc"
LINE = "#cbd5e1"
CARD = "#ffffff"
SOFT = "#f0fdfa"


def _setup(figsize=(12, 6.8)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.8)
    ax.axis("off")
    ax.set_facecolor(BG)
    fig.patch.set_facecolor(BG)
    return fig, ax


def _box(ax, x, y, w, h, title, lines=None, header=TEAL, fontsize=8):
    body = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor=CARD, edgecolor=LINE, linewidth=1.2, zorder=2,
    )
    ax.add_patch(body)
    hdr_h = 0.42
    hdr = FancyBboxPatch(
        (x, y + h - hdr_h), w, hdr_h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor=header, edgecolor=header, linewidth=0, zorder=3,
    )
    ax.add_patch(hdr)
    ax.text(x + w / 2, y + h - hdr_h / 2, title, ha="center", va="center",
            fontsize=fontsize + 1, fontweight="bold", color=WHITE, zorder=4)
    if lines:
        for i, line in enumerate(lines):
            ax.text(x + 0.12, y + h - hdr_h - 0.28 - i * 0.28, line,
                    ha="left", va="top", fontsize=fontsize, color=SLATE, zorder=4)


def _arrow(ax, x1, y1, x2, y2, style="-|>", color=MUTED):
    arr = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, mutation_scale=12,
        color=color, linewidth=1.3, zorder=1,
    )
    ax.add_patch(arr)


def component_diagram(path: Path) -> None:
    fig, ax = _setup()
    ax.text(0.4, 6.45, "UML Component Diagram — Transport Analysis", fontsize=14,
            fontweight="bold", color=NAVY)

    # Orchestrator
    _box(ax, 4.6, 5.5, 2.8, 0.9, "main.py", ["Orchestrator"], header=NAVY, fontsize=9)

    modules = [
        (0.4, 3.8, "data_pipeline.py", ["load_dataset()", "generate_dataset()"]),
        (2.5, 3.8, "spark_etl.py", ["run_batch_etl()", "PySpark / Pandas"]),
        (4.6, 3.8, "sql_analytics.py", ["run_sql_analytics()", "6 SQL queries"]),
        (6.7, 3.8, "train_ai_model.py", ["train_and_evaluate()", "RF + KMeans"]),
        (8.8, 3.8, "analysis_report.py", ["build_analysis_report()", "Charts + MD"]),
    ]
    for x, y, title, lines in modules:
        _box(ax, x, y, 1.9, 1.35, title, lines, fontsize=7)

    _box(ax, 4.6, 2.0, 2.8, 1.0, "dashboard.py", ["Streamlit UI", "Separate entry point"], header=TEAL, fontsize=8)

    # Data stores
    stores = [
        (0.5, 0.5, "data/raw", ["transport_trips.csv"]),
        (2.8, 0.5, "data/silver · gold", ["Parquet layers"]),
        (5.1, 0.5, "data/warehouse", ["transport.db"]),
        (7.4, 0.5, "reports/", ["JSON · CSV · figures"]),
    ]
    for x, y, title, lines in stores:
        _box(ax, x, y, 2.0, 1.0, title, lines, header=SLATE, fontsize=7)

    # Arrows orchestrator -> modules
    for cx in [1.35, 3.45, 5.95, 7.65, 9.75]:
        _arrow(ax, 6.0, 5.5, cx, 5.15)

    # Modules -> stores
    _arrow(ax, 1.35, 3.8, 1.5, 1.5)
    _arrow(ax, 3.45, 3.8, 3.8, 1.5)
    _arrow(ax, 5.95, 3.8, 6.1, 1.5)
    _arrow(ax, 7.65, 3.8, 8.4, 1.5)
    _arrow(ax, 9.75, 3.8, 8.4, 1.5)
    _arrow(ax, 6.0, 2.0, 1.5, 1.5, color=TEAL)

    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


def class_diagram(path: Path) -> None:
    fig, ax = _setup(figsize=(12, 7.2))
    ax.set_ylim(0, 7.2)
    ax.text(0.4, 6.85, "UML Class Diagram — Core Modules", fontsize=14,
            fontweight="bold", color=NAVY)

    classes = [
        (0.3, 5.0, "DataPaths", "<<dataclass>>", [
            "- base_dir: Path",
            "+ data_dir, raw_dir",
            "+ dataset_path",
        ]),
        (2.6, 5.0, "data_pipeline", "", [
            "+ generate_dataset()",
            "+ load_dataset()",
            "+ get_features_targets()",
        ]),
        (5.0, 5.0, "spark_etl", "", [
            "+ run_batch_etl()",
            "- _engineer_features()",
            "- _pandas_etl() / _spark_etl()",
        ]),
        (7.6, 5.0, "sql_analytics", "", [
            "+ run_sql_analytics()",
            "- QUERIES: dict",
            "- _load_silver_dataframe()",
        ]),
        (10.0, 5.0, "train_ai_model", "", [
            "+ train_and_evaluate()",
            "- _build_preprocessor()",
            "  RandomForest + KMeans",
        ]),
        (2.0, 2.2, "analysis_report", "", [
            "+ build_analysis_report()",
            "- _save_figures()",
            "  KPIs + Markdown",
        ]),
        (5.5, 2.2, "dashboard", "", [
            "+ main()",
            "+ apply_filters()",
            "+ chart_*() / kpi_row()",
        ]),
        (8.8, 2.2, "main", "", [
            "+ main()",
            "  orchestrates pipeline",
        ]),
    ]

    for x, y, name, stereotype, attrs in classes:
        h = 0.38 + len(attrs) * 0.3 + 0.2
        _box(ax, x, y, 2.1, h, name, [stereotype] + attrs if stereotype else attrs, fontsize=7)

    # Relationships (uses)
    rels = [
        (2.4, 5.6, 2.6, 5.6),   # main uses data_pipeline - will draw from main at bottom
        (4.7, 5.6, 5.0, 5.6),
        (7.1, 5.6, 7.6, 5.6),
        (9.7, 5.6, 10.0, 5.6),
        (9.9, 5.0, 4.1, 3.2),
        (3.1, 5.0, 3.1, 3.2),
        (9.9, 4.2, 6.6, 3.2),
    ]
    for x1, y1, x2, y2 in rels:
        _arrow(ax, x1, y1, x2, y2, style="-|>", color=MUTED)

    # main at bottom center connections
    _arrow(ax, 9.9, 2.2, 3.7, 5.0)
    _arrow(ax, 9.9, 2.2, 6.05, 5.0)
    _arrow(ax, 9.9, 2.2, 8.65, 5.0)
    _arrow(ax, 9.9, 2.2, 11.05, 5.0)
    _arrow(ax, 9.9, 2.2, 3.05, 3.2)

    ax.text(0.4, 0.35, "«uses» dashed arrows show module dependencies orchestrated by main.py",
            fontsize=8, color=MUTED, style="italic")

    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


def sequence_diagram(path: Path) -> None:
    fig, ax = _setup(figsize=(12, 7.0))
    ax.set_ylim(0, 7.0)
    ax.text(0.4, 6.65, "UML Sequence Diagram — Pipeline Execution (py src/main.py)",
            fontsize=14, fontweight="bold", color=NAVY)

    actors = [
        (1.0, "User"),
        (3.0, "main.py"),
        (5.0, "data_pipeline"),
        (7.0, "spark_etl"),
        (9.0, "sql_analytics"),
        (11.0, "ML + Report"),
    ]
    for x, name in actors:
        ax.plot([x, x], [0.8, 6.0], color=LINE, linewidth=1.5, linestyle="--", zorder=1)
        _box(ax, x - 0.75, 6.05, 1.5, 0.45, name, header=NAVY if name == "main.py" else TEAL, fontsize=7)

    steps = [
        (1.0, 3.0, 5.5, "run main.py"),
        (3.0, 5.0, 5.2, "load_dataset()"),
        (5.0, 3.0, 4.9, "return DataFrame"),
        (3.0, 7.0, 4.6, "run_batch_etl()"),
        (7.0, 3.0, 4.3, "Silver + Gold Parquet"),
        (3.0, 9.0, 4.0, "run_sql_analytics()"),
        (9.0, 3.0, 3.7, "transport.db + JSON"),
        (3.0, 11.0, 3.4, "train_and_evaluate()"),
        (11.0, 3.0, 3.1, "model_metrics.json"),
        (3.0, 11.0, 2.8, "build_analysis_report()"),
        (11.0, 3.0, 2.5, "figures + analysis_report.md"),
        (3.0, 1.0, 2.2, "print success summary"),
        (1.0, 3.0, 1.9, "pipeline complete"),
    ]

    for x1, x2, y, label in steps:
        color = TEAL if x1 < x2 else NAVY
        ax.annotate(
            "", xy=(x2, y), xytext=(x1, y),
            arrowprops=dict(arrowstyle="-|>", color=color, lw=1.4),
            zorder=2,
        )
        mid = (x1 + x2) / 2
        ax.text(mid, y + 0.12, label, ha="center", va="bottom", fontsize=7, color=SLATE)

    # Return dashed arrows
    for x1, x2, y in [(5.0, 3.0, 4.9), (7.0, 3.0, 4.3), (9.0, 3.0, 3.7), (11.0, 3.0, 3.1), (11.0, 3.0, 2.5)]:
        ax.annotate(
            "", xy=(x2, y), xytext=(x1, y),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0, linestyle="dashed"),
            zorder=2,
        )

    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


def generate_all() -> dict[str, Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "component": OUT_DIR / "uml_component.png",
        "class": OUT_DIR / "uml_class.png",
        "sequence": OUT_DIR / "uml_sequence.png",
    }
    component_diagram(paths["component"])
    class_diagram(paths["class"])
    sequence_diagram(paths["sequence"])
    return paths


if __name__ == "__main__":
    result = generate_all()
    for k, p in result.items():
        print(f"{k}: {p}")
