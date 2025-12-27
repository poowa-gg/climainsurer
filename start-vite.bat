@echo off
echo ========================================
echo Starting Hyperlocal Intelligence Platform - Vite Frontend
echo ========================================
echo.

cd frontend-vite

echo Installing dependencies (this will be FAST with Vite!)...
call npm install

echo.
echo Starting Vite dev server...
echo Dashboard will be available at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev

pause
