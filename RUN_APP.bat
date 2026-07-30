@echo off
setlocal
cls

REM Selalu bekerja dari folder skrip ini, bukan dari folder tempat cmd dibuka
cd /d "%~dp0"

REM Konsol Windows default memakai code page 437 yang tidak bisa menampilkan
REM karakter non-ASCII. Tanpa dua baris ini, pesan startup app.py (yang memakai
REM emoji) melempar UnicodeEncodeError dan aplikasi mati sebelum server jalan.
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

echo ========================================
echo   CORROSION RATE APP
echo ========================================
echo.

REM Cari interpreter: virtual environment lokal dulu, baru Python sistem.
REM Folder test_env TIDAK ikut di Git, jadi di device baru belum ada.
set "PY="
if exist "test_env\Scripts\python.exe" set "PY=test_env\Scripts\python.exe"
if not defined PY if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"

if not defined PY (
    where python >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python tidak ditemukan di komputer ini.
        echo.
        echo   1. Install Python 3.8+ dari https://www.python.org/downloads/
        echo      dan centang "Add Python to PATH".
        echo   2. Jalankan install.bat untuk menyiapkan dependensi.
        echo.
        pause
        exit /b 1
    )
    echo [INFO] Virtual environment belum ada, memakai Python sistem.
    set "PY=python"
) else (
    echo [OK] Virtual environment: %PY%
)

REM Pastikan dependensi sudah terpasang sebelum server dijalankan
"%PY%" -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Dependensi belum terpasang untuk interpreter ini.
    echo.
    echo   Jalankan install.bat lebih dulu ^(cukup sekali per komputer^),
    echo   atau: "%PY%" -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo Server: http://localhost:5000
echo Tekan Ctrl+C untuk menghentikan server.
echo.

"%PY%" app.py

REM Jendela sengaja tidak langsung ditutup, supaya pesan error tetap terbaca
echo.
echo [INFO] Server berhenti dengan exit code %ERRORLEVEL%.
pause
