@echo off
cd /d "%~dp0"
echo === Transport Analysis Website ===
echo Open http://localhost:8501 in your browser
py -m streamlit run dashboard.py
