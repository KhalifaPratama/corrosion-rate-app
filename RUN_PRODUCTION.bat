@echo off
setlocal
cls

cd /d "%~dp0"
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

echo ========================================
echo   CORROSION RATE APP - PRODUCTION MODE
echo ========================================
echo.

set "PY="
if exist "test_env\Scripts\python.exe" set "PY=test_env\Scripts\python.exe"
if not defined PY if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"

if not defined PY (
    where python >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python tidak ditemukan. Jalankan install.bat lebih dulu.
        echo.
        pause
        exit /b 1
    )
    echo [INFO] Virtual environment belum ada, memakai Python sistem.
    set "PY=python"
) else (
    echo [OK] Virtual environment: %PY%
)

echo [INFO] Memastikan waitress dan flask-compress terpasang...
"%PY%" -m pip install waitress flask-compress --quiet
if errorlevel 1 (
    echo.
    echo [ERROR] Gagal memasang waitress/flask-compress.
    echo.
    pause
    exit /b 1
)

echo.
echo   Production server : Waitress ^(8 threads, gzip^)
echo   URL               : http://localhost:5000
echo   Stop              : Ctrl+C
echo.

REM Dipanggil sebagai modul, bukan lewat waitress-serve.exe, supaya tetap jalan
REM walau folder Scripts tidak ada di PATH
"%PY%" -m waitress --host=0.0.0.0 --port=5000 --threads=8 --channel-timeout=60 --connection-limit=500 wsgi:app

echo.
echo [INFO] Server berhenti dengan exit code %ERRORLEVEL%.
pause
