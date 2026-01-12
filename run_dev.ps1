# Activate virtual environment (if exists)
if (Test-Path "venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
}

Write-Host "Starting FastAPI backend..."
Start-Process powershell -ArgumentList "uvicorn backend.main:app --reload"

Write-Host "Starting Streamlit frontend..."
Start-Process powershell -ArgumentList "streamlit run frontend/streamlit_app.py"
