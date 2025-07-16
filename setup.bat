@echo off
REM AI Ethics Assignment Setup Script
REM This script sets up the Python environment and downloads required data

echo ======================================
echo AI Ethics Assignment - Setup Script
echo ======================================

echo.
echo 1. Creating Python virtual environment...
python -m venv ai_ethics_env
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    echo Please ensure Python is installed and accessible
    pause
    exit /b 1
)

echo.
echo 2. Activating virtual environment...
call ai_ethics_env\Scripts\activate.bat

echo.
echo 3. Upgrading pip...
python -m pip install --upgrade pip

echo.
echo 4. Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install packages
    echo Please check requirements.txt and your internet connection
    pause
    exit /b 1
)

echo.
echo 5. Downloading COMPAS dataset...
python download_data.py
if %errorlevel% neq 0 (
    echo WARNING: Dataset download failed
    echo You may need to download manually or check internet connection
)

echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo To get started:
echo 1. Activate environment: ai_ethics_env\Scripts\activate.bat
echo 2. Run bias audit: python compas_audit.py
echo 3. Open Jupyter notebook: jupyter notebook ai_ethics_analysis.ipynb
echo.
echo Files created:
echo - ai_ethics_analysis.ipynb (Main analysis notebook)
echo - compas_audit.py (Standalone audit script)
echo - theoretical_answers.md (Written answers)
echo - ethical_reflection.md (Personal reflection)
echo - data/ (Dataset directory)
echo - results/ (Output directory)
echo.
pause
