@echo off
cls
echo ========================================
echo   CORROSION RATE APP
echo ========================================
echo.
echo Starting application...
echo.

REM Activate virtual environment
call .\test_env\Scripts\activate

echo ✅ Virtual environment activated
echo.
echo Starting Flask server...
echo.
echo ╔════════════════════════════════════════════╗
echo ║  Server will start at:                     ║
echo ║  http://localhost:5000                     ║
echo ║                                            ║
echo ║  Press Ctrl+C to stop the server          ║
echo ╚════════════════════════════════════════════╝
echo.

REM Run Flask application
python app.py
