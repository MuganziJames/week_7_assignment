# AI Ethics Assignment Setup Script (PowerShell)
# This script sets up the Python environment and downloads required data

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "AI Ethics Assignment - Setup Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "1. Creating Python virtual environment..." -ForegroundColor Yellow
try {
    python -m venv ai_ethics_env
    Write-Host "✅ Virtual environment created successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Failed to create virtual environment" -ForegroundColor Red
    Write-Host "Please ensure Python is installed and accessible" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "2. Activating virtual environment..." -ForegroundColor Yellow
& "ai_ethics_env\Scripts\Activate.ps1"

Write-Host ""
Write-Host "3. Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host ""
Write-Host "4. Installing required packages..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    Write-Host "✅ Packages installed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Failed to install packages" -ForegroundColor Red
    Write-Host "Please check requirements.txt and your internet connection" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "5. Downloading COMPAS dataset..." -ForegroundColor Yellow
try {
    python download_data.py
    Write-Host "✅ Dataset downloaded successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠️ WARNING: Dataset download failed" -ForegroundColor Yellow
    Write-Host "You may need to download manually or check internet connection" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "To get started:" -ForegroundColor White
Write-Host "1. Activate environment: ai_ethics_env\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "2. Run bias audit: python compas_audit.py" -ForegroundColor Gray
Write-Host "3. Open Jupyter notebook: jupyter notebook ai_ethics_analysis.ipynb" -ForegroundColor Gray

Write-Host ""
Write-Host "Files created:" -ForegroundColor White
Write-Host "- ai_ethics_analysis.ipynb (Main analysis notebook)" -ForegroundColor Gray
Write-Host "- compas_audit.py (Standalone audit script)" -ForegroundColor Gray
Write-Host "- theoretical_answers.md (Written answers)" -ForegroundColor Gray
Write-Host "- ethical_reflection.md (Personal reflection)" -ForegroundColor Gray
Write-Host "- data/ (Dataset directory)" -ForegroundColor Gray
Write-Host "- results/ (Output directory)" -ForegroundColor Gray

Write-Host ""
Read-Host "Press Enter to continue"
