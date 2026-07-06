@echo off
cls
echo ========================================
echo   CORROSION RATE APP - PRODUCTION MODE
echo ========================================
echo.

REM Activate virtual environment
call .\test_env\Scripts\activate

echo [INFO] Installing production server (Waitress)...
pip install waitress --quiet

echo.
echo [INFO] Starting production server...
echo.
echo ╔════════════════════════════════════════════╗
echo ║  Production Server Starting...             ║
echo ║  URL: http://localhost:5000                ║
echo ║  Server: Waitress (Production-ready)       ║
echo ║                                            ║
echo ║  Press Ctrl+C to stop                      ║
echo ╚════════════════════════════════════════════╝
echo.

REM Run with Waitress production server
waitress-serve --host=0.0.0.0 --port=5000 --threads=4 wsgi:app
