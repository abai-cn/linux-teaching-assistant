@echo off
cd /d "%~dp0"
start msedge http://localhost:8502
.venv\Scripts\streamlit.exe run app.py --server.port 8502 --server.headless true
