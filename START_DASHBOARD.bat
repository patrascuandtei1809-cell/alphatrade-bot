@echo off
REM AlphaTrade Dashboard Startup Script for Windows

echo ======================================
echo AlphaTrade Dashboard - Startup
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

REM Check if venv exists, if not create it
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install/upgrade requirements
echo Installing required packages...
pip install -q -r requirements.txt

REM Start dashboard
echo.
echo ======================================
echo Starting Dashboard on http://localhost:8501
echo ======================================
echo.
streamlit run dashboard.py

pause
