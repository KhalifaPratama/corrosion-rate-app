@echo off
cls
echo ========================================
echo   CORROSION RATE APP - PRODUCTION MODE
echo ========================================
echo.

REM Activate virtual environment
call .\test_env\Scripts\activate

echo [INFO] Installing production dependencies...
pip install waitress flask-compress --quiet

echo.
echo [INFO] Starting production server...
echo.
echo ╔════════════════════════════════════════════╗
echo ║  Production Server Starting...             ║
echo ║  URL: http://localhost:5000                ║
echo ║  Server: Waitress (Production-ready)       ║
echo ║  Threads: 8 (optimized for performance)    ║
echo ║  Compression: Enabled (gzip)               ║
echo ║                                            ║
echo ║  Press Ctrl+C to stop                      ║
echo ╚════════════════════════════════════════════╝
echo.

REM Run with Waitress production server
REM Increased threads from 4 to 8 for better concurrency
REM Added connection limits for stability
waitress-serve --host=0.0.0.0 --port=5000 --threads=8 --channel-timeout=60 --connection-limit=500 wsgi:app
