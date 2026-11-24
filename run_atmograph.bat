@echo off
title AtmoGraph - Supply Chain Ripple Effect Predictor
color 0b
echo ===================================================================
echo   AtmoGraph: Supply Chain Ripple Effect Predictor
echo   B.Tech Final-Year Project in AI & Data Science
echo ===================================================================
echo.
echo [1/2] Launching AtmoGraph Live Web Dashboard...
echo       Opening http://localhost:8080 in your browser...
start http://localhost:8080
echo.
echo [2/2] Starting Universal Backend Server on Port 8080...
echo       Press Ctrl+C to stop the server anytime.
echo.
python "%~dp0scripts\run_server.py"
pause
