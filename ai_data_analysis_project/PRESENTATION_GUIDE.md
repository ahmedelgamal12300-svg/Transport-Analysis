# Transport Analysis — Outstanding Presentation Guide

**Duration:** 12–15 minutes (+ 3 min live demo + Q&A)  
**Files:** `Transport_Analysis_Presentation.pptx` | `wideo.mp4` | Live dashboard

---

## Before you present

1. Run the pipeline (fresh data):
   ```bash
   py src/main.py
   ```
2. Regenerate slides (if metrics changed):
   ```bash
   py create_presentation.py
   ```
3. Open dashboard in a browser tab (don't show yet):
   ```bash
   py -m streamlit run dashboard.py
   ```
4. Open PowerPoint in **Presenter View** (Alt+F5) — speaker notes appear on your screen only.

---

## Slide-by-slide script (what to say)

### Slide 1 — Title (45 sec)
> "Good morning/afternoon. We are proud to present **Transport Analysis** — an intelligent public transport analytics platform built for the **Digital Egypt Pioneers Initiative**, AI and Data Science track.
>
> Our mission: transform raw transport trip data into **trusted insights, predictions, and an interactive dashboard** that helps operators make faster, smarter decisions."

---

### Slide 2 — Team (20 sec)
> "This project was delivered by our team of six, covering data engineering, analytics, business intelligence, and project management — every DEPI milestone from ingestion to final demo."

---

### Slide 3 — Agenda (25 sec)
> "We'll cover the problem, our architecture, the full pipeline, machine learning results, key insights, and a **live dashboard demonstration**."

---

### Slide 4 — Problem (60 sec)
> "Transport companies generate huge volumes of trip data — vehicle type, zone, distance, fare, traffic, weather, delays. But raw CSV files don't answer executive questions.
>
> Spreadsheets don't scale. Delays cost money. Peak hours overload fleets. Decision-makers need **one automated pipeline** from data to decisions — that's what we built."

---

### Slide 5 — Objectives (45 sec)
> "Our objectives align with DEPI requirements: ingest and preprocess transport data, build batch ETL, run SQL warehouse analytics, apply machine learning, and deliver a dashboard anyone can use — no coding required."

---

### Slide 6 — Architecture (75 sec)
> "Here's our end-to-end flow:
> **CSV ingestion** → **batch ETL** with PySpark or Pandas → **SQL warehouse** → **machine learning** → **Streamlit dashboard**.
>
> Each module is independent but orchestrated by a single `main.py` command — fully reproducible and automation-ready."

---

### Slide 7 — Tech Stack (45 sec)
> "We used industry-standard tools: Python, Pandas, PySpark, Parquet, SQLite, scikit-learn, and Streamlit. This mirrors real data teams — the same categories as BigQuery, Snowflake, and modern BI platforms."

---

### Slide 8 — ETL (60 sec)
> "We implemented **Medallion architecture**:
> - **Bronze** — raw trips CSV  
> - **Silver** — cleaned data with engineered features like speed and revenue per kilometer  
> - **Gold** — daily business summaries by vehicle, zone, and date  
>
> This is how production data platforms are built at scale."

---

### Slide 9 — SQL Analytics (45 sec)
> "We loaded cleaned data into a SQLite warehouse and ran six analytical queries: revenue by vehicle, fares by zone, delays by traffic, peak hours, and weather impact. Results export to JSON and reusable SQL files."

---

### Slide 10 — Machine Learning (60 sec)
> "We didn't stop at descriptive analytics. We built three models:
> 1. **Fare regression** — R² of 0.98, MAE under $2  
> 2. **Delay classification** — 78% accuracy  
> 3. **Trip segmentation** — clusters for targeted service planning  
>
> This enables **prediction**, not just reporting."

---

### Slide 11 — KPIs (45 sec)
> "On 5,000 trips: average fare $28, delay rate 31%, Airport is the premium zone, Taxi leads revenue. These are the metrics executives care about — and they update every pipeline run."

---

### Slides 12–15 — Charts (30 sec each)
**Revenue:** "Taxi dominates revenue — optimize pricing and availability there first."  
**Delays:** "High traffic = highest delay rate. Operations should prioritize congestion response."  
**Peak hours:** "Morning and evening peaks are predictable — schedule fleets proactively."  
**Distance vs fare:** "Fare grows with distance but vehicle type matters — supports dynamic pricing."

---

### Slide 16 — Strategic Insights (45 sec)
> "Three takeaways: premium zones exist, traffic drives delays, peaks are forecastable. These aren't academic — they guide pricing, fleet deployment, and scheduling."

---

### Slide 17 — Dashboard Demo (90 sec) — **SWITCH TO LIVE DEMO**
> "Now the live product. I'll open our Streamlit dashboard at localhost:8501."

**Do this live:**
1. Show KPI cards at the top  
2. Filter **High** traffic → point at delay rate increase  
3. Filter **Airport** zone → show fare patterns  
4. Select only **Taxi** → show revenue chart change  
5. Scroll to trip table — "drill-down to individual records"

> "Every filter updates instantly. A manager can explore data without writing SQL or Python."

---

### Slide 18 — Challenges (30 sec)
> "We handled scale with PySpark plus Pandas fallback, automated cleaning, and a no-code dashboard for stakeholders."

---

### Slide 19 — Future Work (30 sec)
> "Next steps: cloud warehouse deployment, real-time streaming, geospatial maps, and MLOps monitoring."

---

### Slide 20 — Thank You (20 sec)
> "Transport Analysis — from raw data to decisions. Thank you. We're happy to take questions or run the demo again."

---

## Presentation tips (stand out)

| Tip | Why |
|-----|-----|
| **Start with the problem, not the code** | Judges care about impact first |
| **Use Presenter View** | Speaker notes keep you confident |
| **Do the live demo** | Separates good from outstanding projects |
| **Pause on one insight** | e.g. "38% delays in high traffic" — let it land |
| **Know your numbers** | R² 0.98, 5,000 trips, 31% delay rate |
| **Dress rehearsal once** | Run full 15 min with timer |

---

## Tough questions — ready answers

**Q: Is the data real?**  
> "We use a realistic synthetic dataset that mirrors public transport patterns. The pipeline works identically on real TLC or operator CSV exports."

**Q: Why SQLite instead of BigQuery?**  
> "SQLite simulates the warehouse layer locally for the DEPI demo. The SQL queries transfer directly to BigQuery or Snowflake with minimal changes."

**Q: Why Pandas instead of Spark?**  
> "PySpark activates automatically when Java is installed. Pandas fallback ensures the project runs on any machine — we designed for reliability."

**Q: What's the business value?**  
> "Operators can predict delays, optimize fleet during peaks, and identify high-revenue zones — reducing cost and improving passenger experience."

**Q: What was your role?**  
> Prepare your specific contribution: e.g. pipeline, ML, dashboard, documentation, or project coordination.

---

## Files checklist

| File | Purpose |
|------|---------|
| `Transport_Analysis_Presentation.pptx` | Main graduation slides |
| `PRESENTATION_GUIDE.md` | This speaking script |
| `wideo.mp4` | Backup video demo if live fails |
| `dashboard.py` | Live interactive demo |
| `reports/analysis_report.md` | Technical backup report |

---

## Emergency backup

If live demo fails:
1. Play `wideo.mp4`  
2. Show screenshots in `reports/figures/`  
3. Walk through `reports/analysis_report.md`

**You are prepared. Deliver with confidence.**
