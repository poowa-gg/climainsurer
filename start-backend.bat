@echo off
echo ========================================
echo Starting Hyperlocal Intelligence Platform - Backend
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting Backend API on port 8080...
echo API will be available at: http://localhost:8080
echo API Documentation at: http://localhost:8080/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python -m backend.main

pause
