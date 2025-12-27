@echo off
echo ========================================
echo Starting Hyperlocal Intelligence Platform - Frontend
echo ========================================
echo.

echo Checking Node.js installation...
node --version
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    pause
    exit /b 1
)

cd frontend

echo.
echo Installing Node dependencies...
call npm install

echo.
echo Starting Frontend Dashboard...
echo Dashboard will be available at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev

pause
